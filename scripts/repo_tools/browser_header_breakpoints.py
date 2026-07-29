"""Exact responsive-state seams for the semantic civic header."""

from __future__ import annotations

from typing import Any

from scripts.repo_tools.browser_header_states import _active_matches

_LOCAL_STATE_TIMEOUT_MS = 1_000

_BREAKPOINT_STATE_EXPRESSION = """
(expected = null) => {
  const visible = (selector) => {
    const element = document.querySelector(selector);
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return style.display !== "none" && rect.width > 0 && rect.height > 0;
  };
  const drawer = document.querySelector(".md-sidebar--primary");
  const search = document.querySelector("#opi-search");
  const state = {
    menuVisible: visible("[data-opi-drawer-open]"),
    searchButtonVisible: visible("[data-opi-search-open]"),
    drawerRole: drawer?.getAttribute("role"),
    drawerInert: drawer?.inert,
    drawerChecked: document.querySelector("#__drawer")?.checked,
    searchRole: search?.getAttribute("role"),
    searchLabel: search?.getAttribute("aria-label"),
    searchInert: search?.inert,
    brandFocused:
      document.activeElement?.matches(".opi-header__brand") === true,
  };
  return expected === null
    ? state
    : JSON.stringify(state) === JSON.stringify(expected);
}
"""


def _settle_animation_frames(page: Any) -> None:
    """Wait for focus work scheduled by responsive controller callbacks."""

    page.evaluate(
        """() => new Promise(
          (resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))
        )"""
    )


def _wait_for_active(page: Any, selector: str) -> bool:
    """Wait briefly for one local responsive focus handoff."""

    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

    try:
        page.wait_for_function(
            "(target) => document.activeElement?.matches(target) === true",
            arg=selector,
            timeout=_LOCAL_STATE_TIMEOUT_MS,
        )
    except PlaywrightTimeoutError:
        return False
    return True


def _breakpoint_issues(page: Any) -> list[str]:
    """Prove CSS, controller state, and focus agree at the exact seams."""

    issues: list[str] = []

    def state_at(width: int, expected: dict[str, Any]) -> dict[str, Any]:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

        page.set_viewport_size({"width": width, "height": 900})
        try:
            page.wait_for_function(
                _BREAKPOINT_STATE_EXPRESSION,
                arg=expected,
                polling=50,
                timeout=_LOCAL_STATE_TIMEOUT_MS,
            )
        except PlaywrightTimeoutError:
            pass
        _settle_animation_frames(page)
        return dict(page.evaluate(_BREAKPOINT_STATE_EXPRESSION))

    expected_by_width = {
        959: {
            "menuVisible": True,
            "searchButtonVisible": True,
            "drawerRole": "dialog",
            "drawerInert": True,
            "drawerChecked": False,
            "searchRole": "dialog",
            "searchLabel": "Search",
            "searchInert": True,
            "brandFocused": False,
        },
        960: {
            "menuVisible": True,
            "searchButtonVisible": False,
            "drawerRole": "dialog",
            "drawerInert": True,
            "drawerChecked": False,
            "searchRole": None,
            "searchLabel": None,
            "searchInert": False,
            "brandFocused": False,
        },
        1219: {
            "menuVisible": True,
            "searchButtonVisible": False,
            "drawerRole": "dialog",
            "drawerInert": True,
            "drawerChecked": False,
            "searchRole": None,
            "searchLabel": None,
            "searchInert": False,
            "brandFocused": False,
        },
    }
    for width, expected in expected_by_width.items():
        actual = state_at(width, expected)
        if actual != expected:
            issues.append(
                f"Semantic header ({width}px seam): state was {actual}, expected {expected}."
            )

    page.locator("[data-opi-drawer-open]").click(
        no_wait_after=True,
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    page.wait_for_function(
        "() => document.querySelector('#__drawer')?.checked === true",
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    page.wait_for_function(
        "() => document.activeElement?.matches('[data-opi-drawer-close]') === true",
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    expected = {
        "menuVisible": False,
        "searchButtonVisible": False,
        "drawerRole": None,
        "drawerInert": False,
        "drawerChecked": False,
        "searchRole": None,
        "searchLabel": None,
        "searchInert": False,
        "brandFocused": True,
    }
    actual = state_at(1220, expected)
    if actual != expected:
        issues.append(f"Semantic header (1220px seam): state was {actual}, expected {expected}.")

    page.set_viewport_size({"width": 1219, "height": 900})
    page.wait_for_function(
        "() => document.querySelector('.md-sidebar--primary')?.getAttribute('role') === 'dialog'",
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    page.locator("[data-opi-drawer-open]").click(
        no_wait_after=True,
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    page.wait_for_function(
        "() => document.querySelector('#__drawer')?.checked === true",
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    persistent_link = page.locator(".md-sidebar--primary a.md-nav__link--active[href]").first
    persistent_link.focus()
    page.set_viewport_size({"width": 1220, "height": 900})
    page.wait_for_function(
        """() =>
          document.querySelector("#__drawer")?.checked === false &&
          document.querySelector(".md-sidebar--primary")?.getAttribute("role") === null
        """,
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    _settle_animation_frames(page)
    if not _active_matches(
        page,
        ".md-sidebar--primary a.md-nav__link--active[href]",
    ):
        issues.append(
            "Semantic header (1220px seam): widening stole focus from a "
            "navigation link that remained visible."
        )

    page.set_viewport_size({"width": 1219, "height": 900})
    if not _wait_for_active(page, "[data-opi-drawer-open]"):
        issues.append(
            "Semantic header (1219px seam): collapsing persistent navigation "
            "did not move focus to its visible menu control."
        )

    page.set_viewport_size({"width": 1220, "height": 900})
    if not _wait_for_active(page, ".opi-header__brand"):
        issues.append(
            "Semantic header (1220px seam): hiding the focused menu control "
            "did not move focus to the home lockup."
        )

    page.set_viewport_size({"width": 1219, "height": 900})
    page.wait_for_function(
        "() => document.querySelector('.md-sidebar--primary')?.getAttribute('role') === 'dialog'",
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    _settle_animation_frames(page)
    page.locator("[data-opi-drawer-open]").focus()
    page.evaluate("() => document.activeElement?.blur()")
    if not _active_matches(page, "body"):
        issues.append(
            "Semantic header (1219px seam): explicit blur did not return focus to the body."
        )
    page.set_viewport_size({"width": 1220, "height": 900})
    page.wait_for_function(
        "() => document.querySelector('.md-sidebar--primary')?.getAttribute('role') === null",
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    _settle_animation_frames(page)
    if not _active_matches(page, "body"):
        issues.append(
            "Semantic header (1220px seam): resize resurrected focus after explicit blur."
        )

    page.set_viewport_size({"width": 1219, "height": 900})
    _settle_animation_frames(page)
    page.locator("[data-opi-drawer-open]").focus()
    page.set_viewport_size({"width": 1220, "height": 900})
    page.set_viewport_size({"width": 1219, "height": 900})
    _settle_animation_frames(page)
    if not _active_matches(page, "[data-opi-drawer-open]"):
        issues.append(
            "Semantic header (1219px seam): stale widening callback won "
            "after a rapid breakpoint recross."
        )

    page.set_viewport_size({"width": 959, "height": 900})
    page.wait_for_function(
        "() => document.querySelector('#opi-search')?.getAttribute('role') === 'dialog'",
        timeout=_LOCAL_STATE_TIMEOUT_MS,
    )
    _settle_animation_frames(page)
    page.locator("[data-opi-search-open]").focus()
    if not _wait_for_active(page, "[data-opi-search-open]"):
        issues.append(
            "Semantic header (959px seam): mobile search control could not receive focus."
        )
    page.set_viewport_size({"width": 960, "height": 900})
    if not _wait_for_active(page, ".md-search__input"):
        issues.append(
            "Semantic header (960px seam): hiding the focused search control "
            "did not move focus to the inline search field."
        )

    page.set_viewport_size({"width": 1440, "height": 900})
    return issues
