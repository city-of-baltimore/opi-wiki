"""No-JavaScript progressive-enhancement proof for the civic header."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

from scripts.repo_tools.browser_routes import (
    PAGE_CONTENT_SELECTOR,
    check_page_load,
    navigate_to_ready_page,
)

_TOP_LEVEL_DESTINATIONS = (
    "Home",
    "About Us",
    "How We Work",
    "What We Do",
    "Resources",
)


def _fallback_geometry_issues(page: Any) -> list[str]:
    """Require a visible top-level nav with no off-canvas focus surface."""

    state = page.evaluate(
        """
        () => {
          const visible = (element) => {
            if (!element) return false;
            const style = getComputedStyle(element);
            const rect = element.getBoundingClientRect();
            return style.display !== "none" &&
              style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 &&
              rect.width > 0 &&
              rect.height > 0;
          };
          const links = [...document.querySelectorAll(".md-tabs__link")].map(
            (link) => {
              const rect = link.getBoundingClientRect();
              return {
                text: link.textContent.trim().replace(/\\s+/g, " "),
                width: rect.width,
                height: rect.height,
                left: rect.left,
                right: rect.right,
                top: rect.top,
                bottom: rect.bottom,
              };
            }
          );
          return {
            rootIsNoJavaScript:
              document.documentElement.classList.contains("no-js"),
            fallbackMenuVisible: visible(
              document.querySelector(".opi-header__fallback-drawer")
            ),
            nativeMenuVisible: visible(
              document.querySelector("[data-opi-drawer-open]")
            ),
            sidebarVisible: visible(
              document.querySelector(".md-sidebar--primary")
            ),
            overlayVisible: visible(document.querySelector(".md-overlay")),
            tabsVisible: visible(document.querySelector(".md-tabs")),
            tabsLabel: document.querySelector(".md-tabs")?.getAttribute("aria-label"),
            links,
            pageOverflow: document.documentElement.scrollWidth > innerWidth,
            viewportWidth: innerWidth,
            viewportHeight: innerHeight,
          };
        }
        """
    )

    issues: list[str] = []
    if not state["rootIsNoJavaScript"]:
        issues.append("Semantic header (no JavaScript): root fallback state was absent.")
    for key, label in (
        ("fallbackMenuVisible", "label-based menu control"),
        ("nativeMenuVisible", "unbound native menu control"),
        ("sidebarVisible", "off-canvas navigation"),
        ("overlayVisible", "drawer overlay"),
    ):
        if state[key]:
            issues.append(f"Semantic header (no JavaScript): {label} remained visible.")
    if not state["tabsVisible"]:
        issues.append("Semantic header (no JavaScript): top-level navigation was not visible.")
    if not state["tabsLabel"]:
        issues.append(
            "Semantic header (no JavaScript): top-level navigation had no accessible name."
        )
    if state["pageOverflow"]:
        issues.append("Semantic header (no JavaScript): fallback navigation caused page overflow.")

    rendered_destinations = tuple(link["text"] for link in state["links"])
    if rendered_destinations != _TOP_LEVEL_DESTINATIONS:
        issues.append(
            "Semantic header (no JavaScript): top-level destinations were "
            f"{rendered_destinations}, expected {_TOP_LEVEL_DESTINATIONS}."
        )
    for link in state["links"]:
        if link["height"] < 44 or link["width"] < 44:
            issues.append(
                "Semantic header (no JavaScript): "
                f"{link['text']} target was {link['width']}×{link['height']}px."
            )
        if (
            link["left"] < 0
            or link["right"] > state["viewportWidth"]
            or link["top"] < 0
            or link["bottom"] > state["viewportHeight"]
        ):
            issues.append(f"Semantic header (no JavaScript): {link['text']} was offscreen.")
    return issues


def _fallback_keyboard_issues(page: Any) -> list[str]:
    """Walk real Tab order and reject hidden or offscreen focus targets."""

    page.evaluate("() => document.activeElement?.blur()")
    visited: list[str] = []
    issues: list[str] = []
    for _ in range(12):
        page.keyboard.press("Tab")
        active = page.evaluate(
            """
            () => {
              const element = document.activeElement;
              const rect = element?.getBoundingClientRect();
              return {
                text: element?.textContent.trim().replace(/\\s+/g, " ") || "",
                isTopLevel: element?.matches(".md-tabs__link") === true,
                inSidebar:
                  element?.closest(".md-sidebar--primary") !== null,
                visible:
                  !!rect &&
                  rect.width > 0 &&
                  rect.height > 0 &&
                  rect.left >= 0 &&
                  rect.right <= innerWidth &&
                  rect.top >= 0 &&
                  rect.bottom <= innerHeight,
              };
            }
            """
        )
        if active["inSidebar"]:
            issues.append(
                "Semantic header (no JavaScript): hidden drawer content "
                "entered sequential focus order."
            )
            break
        if not active["visible"]:
            issues.append(
                "Semantic header (no JavaScript): keyboard focus moved "
                f"offscreen on {active['text']!r}."
            )
            break
        if active["isTopLevel"]:
            visited.append(str(active["text"]))
            if tuple(visited) == _TOP_LEVEL_DESTINATIONS:
                break

    if tuple(visited) != _TOP_LEVEL_DESTINATIONS:
        issues.append(
            "Semantic header (no JavaScript): keyboard reached top-level "
            f"destinations {tuple(visited)}, expected {_TOP_LEVEL_DESTINATIONS}."
        )
        return issues

    page.keyboard.press("Tab")
    post_navigation_focus = page.evaluate(
        """
        () => {
          const element = document.activeElement;
          const rect = element?.getBoundingClientRect();
          return {
            text: element?.textContent.trim().replace(/\\s+/g, " ") || "",
            inSidebar: element?.closest(".md-sidebar--primary") !== null,
            visible:
              !!rect &&
              rect.width > 0 &&
              rect.height > 0 &&
              // Focus scrolling can settle a fraction of one CSS pixel at the
              // document edge. This tolerance is intentionally confined to
              // the post-navigation content target; header stops stay exact.
              rect.left >= -1 &&
              rect.right <= innerWidth + 1 &&
              rect.top >= -1 &&
              rect.bottom <= innerHeight + 1,
          };
        }
        """
    )
    if post_navigation_focus["inSidebar"] or not post_navigation_focus["visible"]:
        issues.append(
            "Semantic header (no JavaScript): focus after top-level navigation "
            f"was hidden or offscreen on {post_navigation_focus['text']!r}."
        )
    page.keyboard.press("Shift+Tab")
    if not page.evaluate(
        "() => document.activeElement?.matches('.md-tabs__link') === true && "
        "document.activeElement.textContent.trim() === 'Resources'"
    ):
        issues.append(
            "Semantic header (no JavaScript): reverse focus did not return "
            "to Resources across the hidden drawer seam."
        )
    return issues


def _no_javascript_fallback_issues(page: Any, base_url: str) -> list[str]:
    """Prove keyboard navigation and safe search suppression without JavaScript."""

    issues = navigate_to_ready_page(page, base_url, "Semantic header", "no JavaScript")
    if issues:
        return issues

    issues.extend(_fallback_geometry_issues(page))
    keyboard_issues = _fallback_keyboard_issues(page)
    issues.extend(keyboard_issues)
    for selector, label in (
        (".opi-header__fallback-search", "fallback"),
        ("[data-opi-search-open]", "unbound native"),
    ):
        if page.locator(selector).is_visible():
            issues.append(
                f"Search (no JavaScript): {label} control was visible without a search runtime."
            )
    if not keyboard_issues:
        destination = urljoin(base_url, "resources/")
        with page.expect_navigation(wait_until="load") as navigation:
            page.keyboard.press("Enter")
        navigation_issues = check_page_load(
            page,
            navigation.value,
            destination,
            "Semantic header",
            "no-JavaScript keyboard navigation",
        )
        issues.extend(navigation_issues)
        if not navigation_issues:
            page.locator(PAGE_CONTENT_SELECTOR).first.wait_for(state="visible")
    return issues
