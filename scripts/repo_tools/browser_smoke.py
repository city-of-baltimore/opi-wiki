"""Browser smoke checks for critical shared docs UI behaviors."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from scripts.repo_tools.browser_resources import BrowserResourceObserver
from scripts.repo_tools.browser_routes import (
    BrowserTarget,
    browser_route_url,
    create_browser_context,
    navigate_to_instant_page,
    navigate_to_ready_page,
    resolved_browser_target,
)
from scripts.repo_tools.browser_smoke_states import (
    _check_card_focus_state,
    _check_mobile_nav_state,
    _check_org_chart_state,
    _check_table_focus_state,
)
from scripts.repo_tools.browser_smoke_targets import (
    ORG_READY_SELECTOR,
    ORG_SOURCE_PATH,
    ORG_TARGET_PATH,
    SEARCH_TARGET_SELECTOR,
    SMOKE_TARGETS,
    TABLE_FOCUS_SOURCE_PATH,
    TABLE_FOCUS_TARGET_PATH,
    TABLE_READY_SELECTOR,
)


def _check_table_focus_after_instant_navigation(page: Any, base_url: str, scheme: str) -> list[str]:
    """Navigate through Material's instant loader and validate its document hook."""

    source_url = urljoin(base_url, TABLE_FOCUS_SOURCE_PATH.lstrip("/"))
    target_url = urljoin(base_url, TABLE_FOCUS_TARGET_PATH.lstrip("/"))
    issues = navigate_to_ready_page(page, source_url, "Table focus source", scheme)
    if issues:
        return issues

    target_link = page.locator('.md-content a[href*="service-definition/"]').first
    if target_link.count() == 0:
        issues.append(f"Table scroll region ({scheme}, instant navigation): link was not found.")
        return issues

    transition_issues = navigate_to_instant_page(
        page,
        target_link,
        target_url,
        "Table scroll region (instant navigation)",
        scheme,
        ready_selector=TABLE_READY_SELECTOR,
    )
    issues.extend(transition_issues)
    if transition_issues:
        return issues
    issues.extend(_check_table_focus_state(page, scheme, "instant navigation"))
    return issues


def _check_org_chart_after_instant_navigation(page: Any, base_url: str, scheme: str) -> list[str]:
    """Navigate to the organization chart through Material's instant loader."""

    source_url = urljoin(base_url, ORG_SOURCE_PATH.lstrip("/"))
    target_url = urljoin(base_url, ORG_TARGET_PATH.lstrip("/"))
    issues = navigate_to_ready_page(page, source_url, "Organization source", scheme)
    if issues:
        return issues
    target_link = page.locator('.md-content a[href*="org-structure/"]').first
    if target_link.count() == 0:
        issues.append(f"Organization chart ({scheme}, instant navigation): link was not found.")
        return issues

    transition_issues = navigate_to_instant_page(
        page,
        target_link,
        target_url,
        "Organization chart (instant navigation)",
        scheme,
        ready_selector=ORG_READY_SELECTOR,
    )
    issues.extend(transition_issues)
    if transition_issues:
        return issues
    issues.extend(_check_org_chart_state(page, scheme, "instant navigation"))
    return issues


def _check_search_workflow(page: Any, base_url: str, scheme: str) -> list[str]:
    """Search for a stable site term and navigate to an accessible result."""

    issues = navigate_to_ready_page(page, base_url, "Search home", scheme)
    if issues:
        return issues
    search_toggle = page.locator('label.md-header__button[for="__search"]').first
    if search_toggle.count() == 0:
        return [*issues, f"Search ({scheme}): search toggle was not found."]
    search_toggle.click(no_wait_after=True)

    search_input = page.locator("input.md-search__input").first
    # Material 9.6 listens to key events, so fill() changes the value without
    # starting a search. Real keystrokes exercise the user-facing contract.
    search_input.press_sequentially("CitiStat", delay=20)
    result_link = page.locator("a.md-search-result__link", has_text="CitiStat").first
    result_link.wait_for(state="visible")
    accessible_name = result_link.inner_text().strip()
    href = result_link.get_attribute("href")
    if not accessible_name or href is None:
        issues.append(f"Search ({scheme}): result link had no accessible name or target.")
        return issues

    target_url = urljoin(str(page.url), href)
    issues.extend(
        navigate_to_instant_page(
            page,
            result_link,
            target_url,
            "Search result",
            scheme,
            ready_selector=SEARCH_TARGET_SELECTOR,
        )
    )
    return issues


def _crawl_canonical_routes(browser: Any, target: BrowserTarget) -> list[str]:
    """Load every canonical route and capture status, redirect, and runtime errors."""

    if not target.routes:
        return []
    context = create_browser_context(
        browser,
        target,
        viewport={"width": 1440, "height": 900},
    )
    issues: list[str] = []
    current_route = {"value": "/"}
    resource_observer = BrowserResourceObserver(target, issues, "Canonical /")
    resource_observer.attach(context)
    page = context.new_page()

    def record_console(message: Any) -> None:
        if message.type == "error" and not message.text.startswith("Failed to load resource:"):
            issues.append(f"Canonical {current_route['value']}: console error: {message.text}")

    def record_page_error(error: Any) -> None:
        issues.append(f"Canonical {current_route['value']}: page error: {error}")

    page.on("console", record_console)
    page.on("pageerror", record_page_error)
    try:
        for route in target.routes:
            current_route["value"] = route
            resource_observer.set_scope(f"Canonical {route}")
            requested_url = browser_route_url(target.base_url, route)
            issues.extend(
                navigate_to_ready_page(
                    page,
                    requested_url,
                    f"Canonical {route}",
                    "desktop",
                )
            )
    finally:
        context.close()
    return issues


def _collect_browser_smoke_issues(
    sync_playwright: Any,
    target: BrowserTarget,
) -> list[str]:
    """Run the actual browser interactions against one resolved target."""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            issues = _crawl_canonical_routes(browser, target)
            for scheme in ("light", "dark"):
                context = create_browser_context(
                    browser,
                    target,
                    color_scheme=scheme,
                    viewport={"width": 390, "height": 844},
                    is_mobile=True,
                )
                resource_observer = BrowserResourceObserver(
                    target,
                    issues,
                    f"Smoke interactions ({scheme})",
                )
                resource_observer.attach(context)
                page = context.new_page()
                try:
                    for smoke_target in SMOKE_TARGETS:
                        resource_observer.set_scope(
                            f"{smoke_target.section} ({scheme}, mobile navigation)"
                        )
                        requested_url = urljoin(
                            target.base_url,
                            smoke_target.path.lstrip("/"),
                        )
                        navigation_issues = navigate_to_ready_page(
                            page,
                            requested_url,
                            smoke_target.section,
                            scheme,
                        )
                        issues.extend(navigation_issues)
                        if navigation_issues:
                            continue
                        issues.extend(_check_mobile_nav_state(page, smoke_target, scheme))

                    resource_observer.set_scope(f"Table focus ({scheme}, direct load)")
                    table_url = urljoin(
                        target.base_url,
                        TABLE_FOCUS_TARGET_PATH.lstrip("/"),
                    )
                    navigation_issues = navigate_to_ready_page(
                        page,
                        table_url,
                        "Table focus",
                        scheme,
                        ready_selector=TABLE_READY_SELECTOR,
                    )
                    issues.extend(navigation_issues)
                    if not navigation_issues:
                        issues.extend(_check_table_focus_state(page, scheme, "direct load"))
                    resource_observer.set_scope(
                        f"Table scroll region ({scheme}, instant navigation)"
                    )
                    issues.extend(
                        _check_table_focus_after_instant_navigation(
                            page,
                            target.base_url,
                            scheme,
                        )
                    )

                    resource_observer.set_scope(f"Organization chart ({scheme}, direct load)")
                    org_url = urljoin(
                        target.base_url,
                        ORG_TARGET_PATH.lstrip("/"),
                    )
                    navigation_issues = navigate_to_ready_page(
                        page,
                        org_url,
                        "Organization chart",
                        scheme,
                        ready_selector=ORG_READY_SELECTOR,
                    )
                    issues.extend(navigation_issues)
                    if not navigation_issues:
                        issues.extend(_check_org_chart_state(page, scheme, "direct load"))
                    resource_observer.set_scope(
                        f"Organization chart ({scheme}, instant navigation)"
                    )
                    issues.extend(
                        _check_org_chart_after_instant_navigation(
                            page,
                            target.base_url,
                            scheme,
                        )
                    )
                    resource_observer.set_scope(f"Search ({scheme})")
                    issues.extend(_check_search_workflow(page, target.base_url, scheme))

                    resource_observer.set_scope(f"Home cards ({scheme})")
                    navigation_issues = navigate_to_ready_page(
                        page,
                        target.base_url,
                        "Home",
                        scheme,
                    )
                    issues.extend(navigation_issues)
                    if not navigation_issues:
                        issues.extend(_check_card_focus_state(page, scheme))
                finally:
                    context.close()
            return issues
        finally:
            browser.close()


def find_browser_smoke_issues(site_dir: Path, base_url: str | None = None) -> list[str]:
    """Run lightweight browser smoke checks against the built site."""

    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Playwright is not installed. Run 'uv sync' and "
            "'uv run playwright install chromium' first."
        ) from error

    with resolved_browser_target(site_dir, base_url) as target:
        return _collect_browser_smoke_issues(sync_playwright, target)
