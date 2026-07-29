"""Browser accessibility assurance across every canonical documentation route."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.repo_tools.browser_resources import BrowserResourceObserver
from scripts.repo_tools.browser_routes import (
    BrowserTarget,
    browser_route_url,
    create_browser_context,
    navigate_to_ready_page,
    resolved_browser_target,
)


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


def _run_axe(axe: Any, page: Any) -> dict[str, Any]:
    """Run axe without analyzer-generated stylesheet refetches.

    The hermetic target already loads every release-critical stylesheet from
    the exact artifact. Axe's optional CSSOM preload would separately refetch
    external font stylesheets as XHRs, which is analyzer traffic rather than a
    product dependency and would blur the context-wide resource boundary.
    """

    result = axe.run(
        page,
        options={
            "resultTypes": ["violations"],
            "preload": False,
        },
    )
    return dict(result.response)


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
    issues = navigate_to_ready_page(page, base_url, "Skip link", profile.name)
    if issues:
        return issues
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
    issues = navigate_to_ready_page(page, base_url, "Interactive home", profile.name)
    if issues:
        return issues

    drawer_toggle = page.locator('label.md-header__button[for="__drawer"]').first
    drawer_toggle.click(no_wait_after=True)
    issues.extend(
        _format_axe_violations(
            "/",
            profile,
            _run_axe(axe, page),
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
    search_toggle.click(no_wait_after=True)
    issues.extend(
        _format_axe_violations(
            "/",
            profile,
            _run_axe(axe, page),
            state="search open",
        )
    )
    return issues


def _collect_browser_accessibility_issues(
    sync_playwright: Any,
    axe_factory: Any,
    target: BrowserTarget,
) -> list[str]:
    """Run the accessibility matrix against one resolved browser target."""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        axe = axe_factory()
        issues: list[str] = []
        try:
            for profile in AUDIT_PROFILES:
                context = create_browser_context(
                    browser,
                    target,
                    color_scheme=profile.color_scheme,
                    viewport={"width": profile.width, "height": profile.height},
                    is_mobile=profile.mobile,
                )
                resource_observer = BrowserResourceObserver(
                    target,
                    issues,
                    f"Accessibility ({profile.name})",
                )
                resource_observer.attach(context)
                page = context.new_page()
                try:
                    for route in target.routes:
                        resource_observer.set_scope(f"Accessibility {route} ({profile.name})")
                        requested_url = browser_route_url(target.base_url, route)
                        navigation_issues = navigate_to_ready_page(
                            page,
                            requested_url,
                            f"Accessibility {route}",
                            profile.name,
                        )
                        issues.extend(navigation_issues)
                        if navigation_issues:
                            continue
                        issues.extend(
                            _format_axe_violations(
                                route,
                                profile,
                                _run_axe(axe, page),
                            )
                        )
                        issues.extend(_check_document_reflow(page, route, profile))
                    resource_observer.set_scope(f"Skip link ({profile.name})")
                    issues.extend(_check_skip_link(page, target.base_url, profile))
                    resource_observer.set_scope(f"Interactive home ({profile.name})")
                    issues.extend(
                        _check_mobile_interactive_states(
                            page,
                            axe,
                            target.base_url,
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

    try:
        from axe_playwright_python.sync_playwright import Axe
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Browser accessibility dependencies are missing. Run 'uv sync' and "
            "'uv run playwright install chromium' first."
        ) from error

    with resolved_browser_target(site_dir, base_url) as target:
        return _collect_browser_accessibility_issues(sync_playwright, Axe, target)
