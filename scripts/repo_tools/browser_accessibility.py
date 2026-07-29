"""Browser accessibility assurance across every canonical documentation route."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.repo_tools.browser_routes import (
    browser_route_url,
    canonical_route_paths,
    local_site_server,
    normalize_base_url,
)
from scripts.repo_tools.browser_routes import check_page_load as _check_page_load


@dataclass(frozen=True)
class _AuditProfile:
    """One viewport and color-scheme combination in the accessibility matrix."""

    name: str
    width: int
    height: int
    color_scheme: str
    mobile: bool


AUDIT_PROFILES = (
    _AuditProfile("desktop-light", 1440, 900, "light", False),
    _AuditProfile("desktop-dark", 1440, 900, "dark", False),
    _AuditProfile("reflow-light", 320, 800, "light", True),
    _AuditProfile("reflow-dark", 320, 800, "dark", True),
)


def _format_axe_violations(
    route: str,
    profile: _AuditProfile,
    response: dict[str, Any],
    *,
    state: str = "page",
) -> list[str]:
    """Convert axe results into concise, route-specific evidence."""

    issues: list[str] = []
    for violation in response.get("violations", []):
        rule_id = str(violation.get("id", "unknown-rule"))
        impact = str(violation.get("impact") or "unscored")
        help_text = str(violation.get("help", "Accessibility rule failed"))
        help_url = str(violation.get("helpUrl", ""))
        nodes = violation.get("nodes") or [{}]
        for node in nodes:
            targets = node.get("target") or ["unknown target"]
            target = " > ".join(str(part) for part in targets)
            failure = " ".join(str(node.get("failureSummary", "")).split())
            details = f" {failure}" if failure else ""
            issues.append(
                f"{route} ({profile.name}, {state}): axe {rule_id} [{impact}] "
                f"at {target}: {help_text}.{details} {help_url}".strip()
            )
    return issues


def _check_document_reflow(page: Any, route: str, profile: _AuditProfile) -> list[str]:
    """Require 320 CSS-pixel layouts to avoid document-level horizontal scrolling."""

    if profile.width != 320:
        return []
    result = page.evaluate(
        """
        () => ({
          viewportWidth: document.documentElement.clientWidth,
          documentWidth: Math.max(
            document.documentElement.scrollWidth,
            document.body?.scrollWidth || 0
          ),
        })
        """
    )
    if result["documentWidth"] <= result["viewportWidth"] + 1:
        return []
    return [
        f"{route} ({profile.name}): document width was {result['documentWidth']}px "
        f"inside a {result['viewportWidth']}px viewport; WCAG 2.2 AA reflow "
        "requires page-level horizontal scrolling to remain absent."
    ]


def _check_skip_link(page: Any, base_url: str, profile: _AuditProfile) -> list[str]:
    """Prove the first desktop Tab reveals a working main-content skip link."""

    if profile.mobile:
        return []
    response = page.goto(base_url, wait_until="networkidle")
    issues = _check_page_load(page, response, base_url, "Skip link", profile.name)
    page.evaluate(
        """
        () => {
          document.activeElement?.blur();
          document.body.setAttribute("tabindex", "-1");
          document.body.focus();
          document.body.removeAttribute("tabindex");
        }
        """
    )
    page.keyboard.press("Tab")
    page.wait_for_timeout(300)
    state = page.evaluate(
        """
        () => {
          const active = document.activeElement;
          if (!(active instanceof HTMLAnchorElement)) return null;
          const style = getComputedStyle(active);
          const rect = active.getBoundingClientRect();
          const targetUrl = new URL(active.href);
          const currentUrl = new URL(window.location.href);
          return {
            className: active.className,
            href: active.href,
            sameDocument:
              targetUrl.origin === currentUrl.origin &&
              targetUrl.pathname === currentUrl.pathname &&
              targetUrl.search === currentUrl.search,
            targetExists:
              Boolean(targetUrl.hash) &&
              document.querySelector(targetUrl.hash) !== null,
            visible:
              style.display !== "none" &&
              style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 &&
              rect.width > 0 &&
              rect.height > 0,
          };
        }
        """
    )
    if state is None or "md-skip" not in state["className"].split():
        issues.append(f"Skip link ({profile.name}): first Tab did not focus the skip link.")
        return issues
    if not state["visible"]:
        issues.append(f"Skip link ({profile.name}): focused skip link was not visible.")
    if not state["sameDocument"] or not state["targetExists"]:
        issues.append(
            f"Skip link ({profile.name}): target {state['href']!r} did not resolve "
            "to content in the current document."
        )
    return issues


def _check_mobile_interactive_states(
    page: Any,
    axe: Any,
    base_url: str,
    profile: _AuditProfile,
) -> list[str]:
    """Audit the mobile drawer and search after users expose those regions."""

    if not profile.mobile:
        return []
    issues: list[str] = []
    response = page.goto(base_url, wait_until="networkidle")
    issues.extend(_check_page_load(page, response, base_url, "Interactive home", profile.name))

    drawer_toggle = page.locator('label.md-header__button[for="__drawer"]').first
    drawer_toggle.click()
    issues.extend(
        _format_axe_violations(
            "/",
            profile,
            axe.run(page).response,
            state="navigation drawer open",
        )
    )

    drawer_overlay = page.locator('label.md-overlay[for="__drawer"]').first
    overlay_bounds = drawer_overlay.bounding_box()
    if overlay_bounds is None:
        issues.append(f"/ ({profile.name}): navigation drawer overlay was not visible.")
        return issues
    page.mouse.click(
        overlay_bounds["x"] + overlay_bounds["width"] - 8,
        overlay_bounds["y"] + (overlay_bounds["height"] / 2),
    )

    search_toggle = page.locator('label.md-header__button[for="__search"]').first
    search_toggle.click()
    issues.extend(
        _format_axe_violations(
            "/",
            profile,
            axe.run(page).response,
            state="search open",
        )
    )
    return issues


def _collect_browser_accessibility_issues(
    sync_playwright: Any,
    axe_factory: Any,
    base_url: str,
    routes: tuple[str, ...],
) -> list[str]:
    """Run the accessibility matrix against a resolved site URL."""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        axe = axe_factory()
        issues: list[str] = []
        try:
            for profile in AUDIT_PROFILES:
                context = browser.new_context(
                    color_scheme=profile.color_scheme,
                    viewport={"width": profile.width, "height": profile.height},
                    is_mobile=profile.mobile,
                )
                context.set_default_timeout(5000)
                page = context.new_page()
                try:
                    for route in routes:
                        requested_url = browser_route_url(base_url, route)
                        response = page.goto(requested_url, wait_until="networkidle")
                        issues.extend(
                            _check_page_load(
                                page,
                                response,
                                requested_url,
                                f"Accessibility {route}",
                                profile.name,
                            )
                        )
                        issues.extend(
                            _format_axe_violations(
                                route,
                                profile,
                                axe.run(page).response,
                            )
                        )
                        issues.extend(_check_document_reflow(page, route, profile))
                    issues.extend(_check_skip_link(page, base_url, profile))
                    issues.extend(
                        _check_mobile_interactive_states(
                            page,
                            axe,
                            base_url,
                            profile,
                        )
                    )
                finally:
                    context.close()
            return issues
        finally:
            browser.close()


def find_browser_accessibility_issues(
    site_dir: Path,
    base_url: str | None = None,
) -> list[str]:
    """Audit canonical routes with axe, reflow, skip-link, and interactive-state checks."""

    if not site_dir.is_dir():
        raise FileNotFoundError(f"Built site directory was not found: {site_dir}")

    try:
        from axe_playwright_python.sync_playwright import Axe
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Browser accessibility dependencies are missing. Run 'uv sync' and "
            "'uv run playwright install chromium' first."
        ) from error

    routes = tuple(canonical_route_paths(site_dir))
    if not routes:
        raise RuntimeError(
            f"Built sitemap contains no canonical routes: {site_dir / 'sitemap.xml'}"
        )
    if base_url is not None:
        return _collect_browser_accessibility_issues(
            sync_playwright,
            Axe,
            normalize_base_url(base_url),
            routes,
        )

    with local_site_server(site_dir) as server_base_url:
        return _collect_browser_accessibility_issues(
            sync_playwright,
            Axe,
            server_base_url,
            routes,
        )
