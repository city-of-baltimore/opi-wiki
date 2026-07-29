"""Focused browser proof for the shared semantic civic header."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

from scripts.repo_tools.browser_header_fallback import _no_javascript_fallback_issues
from scripts.repo_tools.browser_header_responsive import (
    _desktop_header_issues,
    _mobile_geometry_issues,
    _text_spacing_issues,
)
from scripts.repo_tools.browser_header_states import (
    _DRAWER_CLOSE,
    _DRAWER_CONTROL,
    _DRAWER_SURFACE,
    _PALETTE_CONTROL,
    _SEARCH_CLOSE,
    _SEARCH_CONTROL,
    _SEARCH_SURFACE,
    _active_matches,
    _below_fold_focus_issues,
    _close_state_issues,
    _closed_surface_issues,
    _destination_focus_issues,
    _focus_indicator_issues,
    _focus_trap_issues,
    _modal_state_issues,
    _palette_enter_issues,
)
from scripts.repo_tools.browser_resources import BrowserResourceObserver
from scripts.repo_tools.browser_routes import (
    BrowserTarget,
    create_browser_context,
    navigate_to_instant_page,
    navigate_to_ready_page,
)
from scripts.repo_tools.browser_smoke_targets import (
    REPOSITORY_NAME,
    REPOSITORY_URL,
    SEARCH_TARGET_SELECTOR,
)

_PAGE_CONTENT = "article.md-content__inner"


def _mobile_header_journey(page: Any, base_url: str) -> list[str]:
    """Exercise each mobile header risk once at its authoritative layer."""

    issues = navigate_to_ready_page(page, base_url, "Semantic header", "mobile")
    if issues:
        return issues

    issues.extend(_mobile_geometry_issues(page, 390, expect_seal=True))

    # First Tab reaches the skip link; second reaches the native menu button.
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    if not _active_matches(page, _DRAWER_CONTROL):
        issues.append("Navigation drawer: menu button was not second in keyboard order.")
        return issues
    issues.extend(_focus_indicator_issues(page, _DRAWER_CONTROL, "Navigation drawer"))

    page.keyboard.press("Enter")
    page.wait_for_function("() => document.querySelector('#__drawer')?.checked === true")
    issues.extend(
        _modal_state_issues(
            page,
            name="Navigation drawer",
            toggle_selector="#__drawer",
            control_selector=_DRAWER_CONTROL,
            surface_selector=_DRAWER_SURFACE,
            initial_focus_selector=_DRAWER_CLOSE,
        )
    )
    repository_link = page.locator(f'.md-nav__source a.md-source[href="{REPOSITORY_URL}"]').first
    if repository_link.count() == 0 or not repository_link.is_visible():
        issues.append("Navigation drawer: visible repository link was not found.")
    elif REPOSITORY_NAME not in repository_link.inner_text():
        issues.append("Navigation drawer: repository name was not visible in its link.")
    if page.locator('[data-md-component="source"]').count() != 0:
        issues.append("Navigation drawer: repository stats component was still active.")
    page.set_viewport_size({"width": 390, "height": 360})
    issues.extend(_below_fold_focus_issues(page))
    page.set_viewport_size({"width": 390, "height": 844})
    issues.extend(
        _focus_trap_issues(
            page,
            name="Navigation drawer",
            surface_selector=_DRAWER_SURFACE,
            first_focus_selector=".md-sidebar--primary .opi-drawer__title a",
        )
    )
    page.locator(_DRAWER_CLOSE).click(no_wait_after=True)
    page.wait_for_function("() => document.querySelector('#__drawer')?.checked === false")
    issues.extend(
        _close_state_issues(
            page,
            name="Navigation drawer",
            toggle_selector="#__drawer",
            control_selector=_DRAWER_CONTROL,
            surface_selector=_DRAWER_SURFACE,
        )
    )

    # Brand and theme are the two controls between menu and mobile search.
    for _ in range(3):
        page.keyboard.press("Tab")
    if not _active_matches(page, _SEARCH_CONTROL):
        issues.append("Search: native search button was not in the expected keyboard order.")
        return issues

    page.keyboard.press("Space")
    page.wait_for_function("() => document.querySelector('#__search')?.checked === true")
    issues.extend(
        _modal_state_issues(
            page,
            name="Search",
            toggle_selector="#__search",
            control_selector=_SEARCH_CONTROL,
            surface_selector=_SEARCH_SURFACE,
            initial_focus_selector=".md-search__input",
        )
    )
    issues.extend(
        _focus_trap_issues(
            page,
            name="Search",
            surface_selector=_SEARCH_SURFACE,
            first_focus_selector=".md-search__input",
        )
    )
    page.locator(_SEARCH_CLOSE).click(no_wait_after=True)
    page.wait_for_function("() => document.querySelector('#__search')?.checked === false")
    issues.extend(
        _close_state_issues(
            page,
            name="Search",
            toggle_selector="#__search",
            control_selector=_SEARCH_CONTROL,
            surface_selector=_SEARCH_SURFACE,
        )
    )

    # Theme state remains Material-owned; the newly revealed button keeps focus.
    page.keyboard.press("Shift+Tab")
    if not _active_matches(page, _PALETTE_CONTROL):
        issues.append("Theme: native palette button was not before search in keyboard order.")
        return issues
    original_scheme = page.locator("body").get_attribute("data-md-color-scheme")
    page.keyboard.press("Space")
    page.wait_for_function(
        "(scheme) => document.body.getAttribute('data-md-color-scheme') !== scheme",
        arg=original_scheme,
    )
    if not _active_matches(page, _PALETTE_CONTROL):
        issues.append("Theme: focus did not follow the newly revealed palette button.")
    issues.extend(_focus_indicator_issues(page, _PALETTE_CONTROL, "Theme"))
    issues.extend(_palette_enter_issues(page, original_scheme))

    # Material's global shortcut bypasses the native button. Preserve its exact
    # invoker while the closed mobile dialog is inert.
    page.locator(".opi-header__brand").focus()
    page.keyboard.press("/")
    page.wait_for_function("() => document.querySelector('#__search')?.checked === true")
    issues.extend(
        _modal_state_issues(
            page,
            name="Search",
            toggle_selector="#__search",
            control_selector=_SEARCH_CONTROL,
            surface_selector=_SEARCH_SURFACE,
            initial_focus_selector=".md-search__input",
        )
    )
    page.keyboard.press("Escape")
    page.wait_for_function("() => document.querySelector('#__search')?.checked === false")
    issues.extend(
        _close_state_issues(
            page,
            name="Search shortcut",
            toggle_selector="#__search",
            control_selector=_SEARCH_CONTROL,
            surface_selector=_SEARCH_SURFACE,
            focus_selector=".opi-header__brand",
        )
    )

    page.set_viewport_size({"width": 320, "height": 800})
    issues.extend(_mobile_geometry_issues(page, 320, expect_seal=False))
    issues.extend(_text_spacing_issues(page, 320, expect_seal=False))
    page.set_viewport_size({"width": 374, "height": 844})
    issues.extend(_text_spacing_issues(page, 374, expect_seal=False))
    page.set_viewport_size({"width": 375, "height": 844})
    issues.extend(_text_spacing_issues(page, 375, expect_seal=True))
    page.set_viewport_size({"width": 390, "height": 844})

    # One pointer companion path also proves search results and two instant
    # document replacements without multiplying the light/dark route matrix.
    search_control = page.locator(_SEARCH_CONTROL)
    search_control.click(no_wait_after=True)
    search_input = page.locator(".md-search__input")
    search_input.press_sequentially("CitiStat", delay=10)
    result_link = page.locator("a.md-search-result__link", has_text="CitiStat").first
    result_link.wait_for(state="visible")
    issues.extend(
        _focus_trap_issues(
            page,
            name="Search with results",
            surface_selector=_SEARCH_SURFACE,
            first_focus_selector=".md-search__input",
        )
    )
    result_href = result_link.get_attribute("href")
    if result_href is None:
        issues.append("Search: CitiStat result had no destination.")
        return issues
    result_url = urljoin(str(page.url), result_href)
    transition_issues = navigate_to_instant_page(
        page,
        result_link,
        result_url,
        "Semantic header search result",
        "mobile",
        ready_selector=SEARCH_TARGET_SELECTOR,
    )
    issues.extend(transition_issues)
    if transition_issues:
        return issues
    page.wait_for_timeout(180)
    destination_issues = _destination_focus_issues(page, "Semantic header search result")
    issues.extend(destination_issues)
    if destination_issues:
        return issues

    page.locator(_DRAWER_CONTROL).click(no_wait_after=True)
    page.wait_for_function("() => document.querySelector('#__drawer')?.checked === true")
    drawer_home = page.locator(".opi-drawer__title a").first
    transition_issues = navigate_to_instant_page(
        page,
        drawer_home,
        base_url,
        "Semantic header drawer transition",
        "mobile",
        ready_selector=_PAGE_CONTENT,
        activation="keyboard",
    )
    issues.extend(transition_issues)
    if transition_issues:
        return issues
    page.wait_for_timeout(180)
    destination_issues = _destination_focus_issues(page, "Semantic header drawer transition")
    issues.extend(destination_issues)
    if destination_issues:
        return issues

    page.evaluate(
        """
        () => {
          window.__opiHeaderDrawerChanges = 0;
          document.querySelector("#__drawer").addEventListener(
            "change",
            () => window.__opiHeaderDrawerChanges += 1
          );
        }
        """
    )
    page.locator(_DRAWER_CONTROL).click(no_wait_after=True)
    page.wait_for_timeout(300)
    activation = page.evaluate(
        """
        () => ({
          checked: document.querySelector("#__drawer").checked,
          changes: window.__opiHeaderDrawerChanges,
        })
        """
    )
    if activation != {"checked": True, "changes": 1}:
        issues.append(
            "Semantic header: one activation after instant navigation produced "
            f"{activation}, expected one open transition."
        )
    page.keyboard.press("/")
    page.wait_for_function(
        """() =>
          document.querySelector("#__search")?.checked === true &&
          document.querySelector("#__drawer")?.checked === false
        """
    )
    issues.extend(
        _modal_state_issues(
            page,
            name="Search",
            toggle_selector="#__search",
            control_selector=_SEARCH_CONTROL,
            surface_selector=_SEARCH_SURFACE,
            initial_focus_selector=".md-search__input",
        )
    )
    issues.extend(
        _closed_surface_issues(
            page,
            name="Modal exclusivity",
            toggle_selector="#__drawer",
            control_selector=_DRAWER_CONTROL,
            surface_selector=_DRAWER_SURFACE,
        )
    )
    page.keyboard.press("Escape")
    page.wait_for_function("() => document.querySelector('#__search')?.checked === false")
    issues.extend(
        _close_state_issues(
            page,
            name="Search after drawer handoff",
            toggle_selector="#__search",
            control_selector=_SEARCH_CONTROL,
            surface_selector=_SEARCH_SURFACE,
        )
    )
    return issues


def _check_semantic_header(browser: Any, target: BrowserTarget) -> list[str]:
    """Run the bounded enhanced and fallback header proof in one launch."""

    issues: list[str] = []
    mobile_context = create_browser_context(
        browser,
        target,
        color_scheme="light",
        viewport={"width": 390, "height": 844},
        is_mobile=True,
    )
    mobile_observer = BrowserResourceObserver(target, issues, "Semantic header (mobile)")
    mobile_observer.attach(mobile_context)
    mobile_page = mobile_context.new_page()
    try:
        issues.extend(_mobile_header_journey(mobile_page, target.base_url))
    finally:
        mobile_context.close()

    desktop_context = create_browser_context(
        browser,
        target,
        color_scheme="light",
        viewport={"width": 1440, "height": 900},
    )
    desktop_observer = BrowserResourceObserver(target, issues, "Semantic header (desktop)")
    desktop_observer.attach(desktop_context)
    desktop_page = desktop_context.new_page()
    try:
        issues.extend(_desktop_header_issues(desktop_page, target.base_url))
    finally:
        desktop_context.close()

    fallback_context = create_browser_context(
        browser,
        target,
        viewport={"width": 320, "height": 800},
        java_script_enabled=False,
    )
    fallback_observer = BrowserResourceObserver(
        target,
        issues,
        "Semantic header (no JavaScript)",
    )
    fallback_observer.attach(fallback_context)
    fallback_page = fallback_context.new_page()
    try:
        issues.extend(_no_javascript_fallback_issues(fallback_page, target.base_url))
    finally:
        fallback_context.close()
    return issues
