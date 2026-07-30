"""Browser smoke checks for critical shared docs UI behaviors."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from scripts.repo_tools.browser_header import _check_semantic_header
from scripts.repo_tools.browser_home_states import (
    _check_card_focus_state,
    _check_home_hero_reflow_state,
)
from scripts.repo_tools.browser_home_tools import (
    _check_home_page_tools_focus_state,
    _check_home_page_tools_layout_state,
)
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
    _check_mobile_nav_active_state,
    _check_org_chart_state,
    _check_table_focus_state,
)
from scripts.repo_tools.browser_smoke_targets import (
    ORG_READY_SELECTOR,
    ORG_SOURCE_PATH,
    ORG_TARGET_PATH,
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
            navigation_issues = navigate_to_ready_page(
                page,
                requested_url,
                f"Canonical {route}",
                "desktop",
            )
            issues.extend(navigation_issues)
            if route == "/" and not navigation_issues:
                issues.extend(_check_home_hero_reflow_state(page, "desktop", 1440))
                issues.extend(_check_home_page_tools_layout_state(page, "desktop", 1440))
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
            issues.extend(_check_semantic_header(browser, target))
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
                        issues.extend(_check_mobile_nav_active_state(page, smoke_target, scheme))

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
                        issues.extend(_check_home_page_tools_focus_state(page, scheme))
                        if scheme == "light":
                            issues.extend(
                                _check_home_hero_reflow_state(
                                    page,
                                    "reflow-light",
                                    390,
                                )
                            )
                            issues.extend(
                                _check_home_page_tools_layout_state(
                                    page,
                                    "reflow-light",
                                    390,
                                )
                            )
                            page.set_viewport_size({"width": 320, "height": 800})
                            issues.extend(
                                _check_home_hero_reflow_state(
                                    page,
                                    "reflow-light",
                                    320,
                                )
                            )
                            issues.extend(
                                _check_home_page_tools_layout_state(
                                    page,
                                    "reflow-light",
                                    320,
                                )
                            )
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
