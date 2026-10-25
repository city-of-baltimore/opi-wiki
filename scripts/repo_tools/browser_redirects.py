"""Follow every old wiki address in a real browser, offline, to its new page.

Ownership: repository tooling for the retired wiki; the browser half of the
redirect checks. :mod:`scripts.repo_tools.redirect_stubs` proves each stub's
markup; this proves what Chromium does with it.

How it runs: the built ``site/`` is served at the wiki's real address
(https://city-of-baltimore.github.io/opi-wiki/) through
:func:`scripts.repo_tools.browser_artifact_routes.install_canonical_artifact_route`,
and every request to the new home is answered by a placeholder page. Nothing
reaches either live site, so the check measures the artifact alone.

Invariants:

1. **With JavaScript,** each old address opened with a fragment lands on its new
   page with the same fragment.
2. **Without JavaScript,** each old address lands on its new page through the
   refresh (no fragment: only the script can carry it).
3. ``404.html`` keeps the reader on the page, links to the new home, and passes
   axe.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts.repo_tools.browser_artifact_routes import install_canonical_artifact_route
from scripts.repo_tools.redirect_stubs import (
    ADDRESSES_FILE,
    NEW_HOME,
    NEW_ORIGIN,
    NOT_FOUND_PAGE,
    OLD_BASE,
    read_addresses,
    stub_targets,
)

#: A fragment no page defines, so a landing proves the stub carried it rather
#: than the new page supplying it.
FRAGMENT = "cutover-check"
NAVIGATION_TIMEOUT_MS = 10_000
_PLACEHOLDER = b"<!doctype html><title>OPI Foundations</title><p>Placeholder for the new home."


def old_url(address: str, *, javascript: bool) -> str:
    """Return the URL to open for one old address."""

    return f"{address}#{FRAGMENT}" if javascript else address


def expected_landing(target: str, *, javascript: bool) -> str:
    """Return where the browser must end up for one stub's target."""

    return f"{target}#{FRAGMENT}" if javascript else target


def fulfill_new_home(route: Any) -> None:
    """Answer one request to the new home with a placeholder; nothing leaves the browser."""

    route.fulfill(status=200, content_type="text/html; charset=utf-8", body=_PLACEHOLDER)


def _new_context(browser: Any, site_dir: Path, *, javascript: bool) -> Any:
    """Return a browser context that serves ``site_dir`` at the wiki's address, offline."""

    context = browser.new_context(java_script_enabled=javascript)
    install_canonical_artifact_route(context, canonical_base_url=OLD_BASE, site_dir=site_dir)
    # Playwright runs the most recently registered matching route first, so this
    # answers the new home ahead of the artifact route's catch-all 404.
    context.route(f"{NEW_ORIGIN}/**", fulfill_new_home)
    context.set_default_timeout(NAVIGATION_TIMEOUT_MS)
    return context


def _landing_issues(page: Any, address: str, target: str, *, javascript: bool) -> list[str]:
    """Open one old address and report it unless it lands exactly where expected."""

    mode = "with JavaScript" if javascript else "without JavaScript"
    expected = expected_landing(target, javascript=javascript)
    try:
        page.goto(old_url(address, javascript=javascript), wait_until="commit")
        page.wait_for_url(expected, wait_until="load")
    except Exception as error:  # noqa: BLE001 - every failure is a finding, by name
        return [f"{address} ({mode}): did not land on {expected}: {error}".splitlines()[0]]
    if page.url != expected:
        return [f"{address} ({mode}): landed on {page.url}, not {expected}"]
    return []


def _not_found_page_issues(browser: Any, axe: Any, site_dir: Path) -> list[str]:
    """Open ``404.html`` and check it stays put, links home, and passes axe."""

    context = _new_context(browser, site_dir, javascript=True)
    try:
        page = context.new_page()
        url = f"{OLD_BASE}{NOT_FOUND_PAGE}"
        page.goto(url, wait_until="load")
        issues = []
        if page.url != url:
            issues.append(f"{NOT_FOUND_PAGE} navigated away to {page.url}")
        if page.locator(f'a[href="{NEW_HOME}"]').count() != 1:
            issues.append(f"{NOT_FOUND_PAGE} has no single link to {NEW_HOME}")
        response = dict(
            axe.run(page, options={"resultTypes": ["violations"], "preload": False}).response
        )
        for violation in response.get("violations", []):
            issues.append(
                f"{NOT_FOUND_PAGE}: axe {violation.get('id', 'unknown-rule')} "
                f"[{violation.get('impact') or 'unscored'}]: {violation.get('help', '')}"
            )
        return issues
    finally:
        context.close()


def collect_browser_redirect_issues(
    sync_playwright: Any,
    axe_factory: Any,
    site_dir: Path,
    targets: dict[str, str | None],
) -> list[str]:
    """Drive Chromium through every old address, both ways, then the 404 page."""

    issues = [f"{address}: no clean stub to follow" for address, t in targets.items() if not t]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for javascript in (True, False):
                context = _new_context(browser, site_dir, javascript=javascript)
                try:
                    page = context.new_page()
                    for address, target in targets.items():
                        if target:
                            issues += _landing_issues(page, address, target, javascript=javascript)
                finally:
                    context.close()
            issues += _not_found_page_issues(browser, axe_factory(), site_dir)
        finally:
            browser.close()
    return issues


def find_browser_redirect_issues(repo_root: Path, site_dir: Path) -> list[str]:
    """Return every old address that a real browser does not land as built."""

    try:
        from axe_playwright_python.sync_playwright import Axe
        from playwright.sync_api import sync_playwright
    except ImportError as error:  # pragma: no cover - the dev group installs both
        raise RuntimeError(f"The browser check needs Playwright and axe: {error}") from error

    site = repo_root / site_dir
    if not site.is_dir():
        return [f"{site} is missing; run `task build` first"]
    addresses, issues = read_addresses(repo_root / ADDRESSES_FILE)
    return issues + collect_browser_redirect_issues(
        sync_playwright, Axe, site, stub_targets(site, addresses)
    )
