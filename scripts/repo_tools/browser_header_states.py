"""Low-level state assertions for the semantic civic header journey."""

from __future__ import annotations

from typing import Any

_DRAWER_CONTROL = "[data-opi-drawer-open]"
_DRAWER_CLOSE = "[data-opi-drawer-close]"
_DRAWER_SURFACE = ".md-sidebar--primary"
_SEARCH_CONTROL = "[data-opi-search-open]"
_SEARCH_CLOSE = "[data-opi-search-close]"
_SEARCH_SURFACE = "#opi-search"
_PALETTE_CONTROL = "[data-opi-palette-toggle]:not([hidden])"


def _active_matches(page: Any, selector: str) -> bool:
    """Return whether the active element matches one exact selector."""

    return bool(
        page.evaluate(
            "(selector) => document.activeElement?.matches(selector) === true",
            selector,
        )
    )


def _active_is_within(page: Any, selector: str) -> bool:
    """Return whether keyboard focus remains inside one surface."""

    return bool(
        page.evaluate(
            """
            (selector) => {
              const surface = document.querySelector(selector);
              return surface?.contains(document.activeElement) === true;
            }
            """,
            selector,
        )
    )


def _focus_indicator_issues(page: Any, selector: str, label: str) -> list[str]:
    """Require a real, three-pixel keyboard focus indicator."""

    result = page.locator(selector).evaluate(
        """
        (element) => {
          const style = getComputedStyle(element);
          return {
            outlineStyle: style.outlineStyle,
            outlineWidth: parseFloat(style.outlineWidth),
          };
        }
        """
    )
    if result["outlineStyle"] == "none" or result["outlineWidth"] < 3:
        return [
            f"{label}: focus outline was {result['outlineStyle']} "
            f"{result['outlineWidth']}px, expected at least 3px."
        ]
    return []


def _palette_enter_issues(page: Any, original_scheme: str | None) -> list[str]:
    """Prove one captured Enter activation produces one palette transition."""

    page.evaluate(
        """
        () => {
          window.__opiHeaderPaletteChanges = 0;
          document.querySelector("[data-md-component='palette']").addEventListener(
            "change",
            () => window.__opiHeaderPaletteChanges += 1
          );
        }
        """
    )
    page.keyboard.press("Enter")
    page.wait_for_function("() => window.__opiHeaderPaletteChanges >= 1")
    page.wait_for_timeout(75)
    actual = page.evaluate(
        """
        () => ({
          scheme: document.body.getAttribute("data-md-color-scheme"),
          changes: window.__opiHeaderPaletteChanges,
          focused: document.activeElement?.matches(
            "[data-opi-palette-toggle]:not([hidden])"
          ) === true,
        })
        """
    )
    expected = {
        "scheme": original_scheme,
        "changes": 1,
        "focused": True,
    }
    if actual == expected:
        return []
    return [f"Theme: one Enter activation produced {actual}, expected {expected}."]


def _modal_state_issues(
    page: Any,
    *,
    name: str,
    toggle_selector: str,
    control_selector: str,
    surface_selector: str,
    initial_focus_selector: str,
) -> list[str]:
    """Validate canonical state, dialog projection, and initial focus."""

    result = page.evaluate(
        """
        ([toggleSelector, controlSelector, surfaceSelector, focusSelector]) => {
          const toggle = document.querySelector(toggleSelector);
          const control = document.querySelector(controlSelector);
          const surface = document.querySelector(surfaceSelector);
          const controlled = document.getElementById(
            control?.getAttribute("aria-controls")
          );
          return {
            checked: toggle?.checked,
            expanded: control?.getAttribute("aria-expanded"),
            controlsSurface: controlled === surface,
            inert: surface?.inert,
            role: surface?.getAttribute("role"),
            label: surface?.getAttribute("aria-label"),
            modal: surface?.getAttribute("aria-modal"),
            hidden: surface?.getAttribute("aria-hidden"),
            focused: document.activeElement?.matches(focusSelector),
          };
        }
        """,
        [toggle_selector, control_selector, surface_selector, initial_focus_selector],
    )
    expected = {
        "checked": True,
        "expanded": "true",
        "controlsSurface": True,
        "inert": False,
        "role": "dialog",
        "label": name if name == "Search" else "Primary navigation",
        "modal": "true",
        "hidden": "false",
        "focused": True,
    }
    if result == expected:
        return []
    return [f"{name}: open modal state was {result}, expected {expected}."]


def _focus_trap_issues(
    page: Any,
    *,
    name: str,
    surface_selector: str,
    first_focus_selector: str,
) -> list[str]:
    """Prove reverse and forward focus wrapping without walking every link."""

    first = page.locator(first_focus_selector)
    first.focus()
    page.keyboard.press("Shift+Tab")
    issues: list[str] = []
    if not _active_is_within(page, surface_selector):
        issues.append(f"{name}: Shift+Tab escaped the open modal surface.")
        return issues
    if page.evaluate("() => document.activeElement?.tabIndex < 0"):
        issues.append(f"{name}: focus trap included a control removed from sequential focus.")
        return issues

    page.keyboard.press("Tab")
    if not _active_matches(page, first_focus_selector):
        issues.append(f"{name}: Tab did not wrap from the last control to the first.")
    return issues


def _below_fold_focus_issues(page: Any) -> list[str]:
    """Require sequential focus to reach a root drawer link below the viewport."""

    target_count = page.evaluate(
        """
        () => {
          const surface = document.querySelector(".md-sidebar--primary");
          const surfaceRect = surface.getBoundingClientRect();
          const links = [
            ...document.querySelectorAll(
              ".md-nav--primary a.md-nav__link[href]"
            )
          ].filter((link) => {
            const style = getComputedStyle(link);
            const rect = link.getBoundingClientRect();
            return style.display !== "none" && style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0 &&
              rect.right > surfaceRect.left && rect.left < surfaceRect.right &&
              link.tabIndex >= 0;
          });
          const targets = links.filter(
            (link) => link.getBoundingClientRect().bottom > innerHeight
          );
          targets.forEach(
            (target) => target.setAttribute("data-opi-below-fold-target", "")
          );
          return targets.length;
        }
        """
    )
    if target_count == 0:
        return ["Navigation drawer: no rendered link began below the reduced viewport."]

    page.locator(_DRAWER_CLOSE).focus()
    focusable_upper_bound = page.locator(
        ".md-sidebar--primary a[href], "
        ".md-sidebar--primary button:not([disabled]), "
        ".md-sidebar--primary input:not([disabled]):not([type='hidden']), "
        ".md-sidebar--primary [tabindex]:not([tabindex='-1'])"
    ).count()
    for _ in range(focusable_upper_bound + 1):
        page.keyboard.press("Tab")
        if _active_matches(page, "[data-opi-below-fold-target]"):
            return []
        if _active_matches(page, _DRAWER_CLOSE):
            break
    return ["Navigation drawer: Tab wrapped before reaching a below-fold link."]


def _closed_surface_state(
    page: Any,
    *,
    toggle_selector: str,
    control_selector: str,
    surface_selector: str,
    focus_selector: str | None,
) -> dict[str, Any]:
    """Read one closed surface's canonical, projected, and optional focus state."""

    return dict(
        page.evaluate(
            """
            ([toggleSelector, controlSelector, surfaceSelector, focusSelector]) => {
              const toggle = document.querySelector(toggleSelector);
              const control = document.querySelector(controlSelector);
              const surface = document.querySelector(surfaceSelector);
              return {
                checked: toggle?.checked,
                expanded: control?.getAttribute("aria-expanded"),
                inert: surface?.inert,
                hidden: surface?.getAttribute("aria-hidden"),
                invokerFocused: focusSelector === null
                  ? null
                  : document.activeElement?.matches(focusSelector) === true,
              };
            }
            """,
            [toggle_selector, control_selector, surface_selector, focus_selector],
        )
    )


def _closed_surface_issues(
    page: Any,
    *,
    name: str,
    toggle_selector: str,
    control_selector: str,
    surface_selector: str,
) -> list[str]:
    """Require a surface displaced by another modal to be closed and inert."""

    result = _closed_surface_state(
        page,
        toggle_selector=toggle_selector,
        control_selector=control_selector,
        surface_selector=surface_selector,
        focus_selector=None,
    )
    expected = {
        "checked": False,
        "expanded": "false",
        "inert": True,
        "hidden": "true",
        "invokerFocused": None,
    }
    if result == expected:
        return []
    return [f"{name}: closed surface state was {result}, expected {expected}."]


def _close_state_issues(
    page: Any,
    *,
    name: str,
    toggle_selector: str,
    control_selector: str,
    surface_selector: str,
    focus_selector: str | None = None,
) -> list[str]:
    """Require a closed, inert surface and focus restoration to its invoker."""

    result = _closed_surface_state(
        page,
        toggle_selector=toggle_selector,
        control_selector=control_selector,
        surface_selector=surface_selector,
        focus_selector=focus_selector or control_selector,
    )
    expected = {
        "checked": False,
        "expanded": "false",
        "inert": True,
        "hidden": "true",
        "invokerFocused": True,
    }
    if result == expected:
        return []
    return [f"{name}: closed modal state was {result}, expected {expected}."]


def _destination_focus_issues(page: Any, label: str) -> list[str]:
    """Require instant navigation to place focus on the new page heading."""

    result = page.evaluate(
        """
        () => ({
          tag: document.activeElement?.tagName,
          className: document.activeElement?.className,
          text: document.activeElement?.textContent?.trim().slice(0, 80),
          isHeading: document.activeElement?.matches(".md-content h1") === true,
        })
        """
    )
    if result["isHeading"]:
        return []
    return [f"{label}: destination focus was {result}, expected the page heading."]
