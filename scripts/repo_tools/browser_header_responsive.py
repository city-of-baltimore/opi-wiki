"""Responsive geometry and breakpoint proof for the semantic civic header."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

from scripts.repo_tools.browser_header_breakpoints import _breakpoint_issues
from scripts.repo_tools.browser_header_markers import _active_location_marker_issues
from scripts.repo_tools.browser_header_states import (
    _active_matches,
    _focus_indicator_issues,
)
from scripts.repo_tools.browser_routes import navigate_to_ready_page


def _mobile_geometry_issues(page: Any, width: int, *, expect_seal: bool) -> list[str]:
    """Validate the intentional narrow lockup and utility-control geometry."""

    result = page.evaluate(
        """
        () => {
          const brand = document.querySelector(".opi-header__brand");
          const product = document.querySelector(".md-header__product");
          const seal = document.querySelector(".opi-header__seal");
          const header = document.querySelector(".md-header__inner");
          const visible = (element) => {
            const style = getComputedStyle(element);
            const rect = element.getBoundingClientRect();
            return style.display !== "none" && style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
          };
          const controls = [
            ...document.querySelectorAll(
              "[data-opi-drawer-open], " +
              "[data-opi-palette-toggle]:not([hidden]), " +
              "[data-opi-search-open]"
            )
          ].filter(visible).map((element) => {
            const rect = element.getBoundingClientRect();
            return {
              name: element.getAttribute("aria-label"),
              x: rect.x,
              y: rect.y,
              width: rect.width,
              height: rect.height,
              right: rect.right,
              bottom: rect.bottom,
            };
          });
          const sealStyle = getComputedStyle(seal);
          const headerRect = header.getBoundingClientRect();
          const brandRect = brand.getBoundingClientRect();
          return {
            brandText: product.textContent.trim(),
            brandOverflow: brand.scrollWidth > brand.clientWidth,
            brandTarget: {
              width: brandRect.width,
              height: brandRect.height,
            },
            sealVisible: sealStyle.display !== "none",
            headerHeight: headerRect.height,
            controls,
            pageOverflow: document.documentElement.scrollWidth > innerWidth,
            viewportHeight: innerHeight,
          };
        }
        """
    )

    issues: list[str] = []
    label = f"Semantic header ({width}px)"
    if result["brandText"] != "OPI Foundations":
        issues.append(f"{label}: product lockup rendered as {result['brandText']!r}.")
    if result["brandOverflow"]:
        issues.append(f"{label}: product lockup overflowed its home link.")
    if result["brandTarget"]["width"] < 44 or result["brandTarget"]["height"] < 44:
        issues.append(
            f"{label}: home target was {result['brandTarget']['width']}×"
            f"{result['brandTarget']['height']}px, expected at least 44×44px."
        )
    if result["sealVisible"] is not expect_seal:
        expectation = "visible" if expect_seal else "hidden"
        issues.append(f"{label}: civic seal was not intentionally {expectation}.")
    if result["pageOverflow"]:
        issues.append(f"{label}: page-level horizontal overflow was present.")
    if not 60 <= result["headerHeight"] <= 64:
        issues.append(
            f"{label}: utility rail was {result['headerHeight']}px high, expected 60–64px."
        )
    if len(result["controls"]) != 3:
        issues.append(
            f"{label}: found {len(result['controls'])} visible primary controls, expected 3."
        )
    for control in result["controls"]:
        if control["width"] < 44 or control["height"] < 44:
            issues.append(
                f"{label}: {control['name']} target was "
                f"{control['width']}×{control['height']}px, expected at least 44×44px."
            )
        if (
            control["x"] < 0
            or control["y"] < 0
            or control["right"] > width
            or control["bottom"] > result["viewportHeight"]
        ):
            issues.append(f"{label}: {control['name']} target left the viewport.")
    return issues


def _text_spacing_issues(page: Any, width: int, *, expect_seal: bool) -> list[str]:
    """Require the full narrow lockup to survive WCAG text-spacing overrides."""

    result = page.locator(".opi-header__brand").evaluate(
        """
        (brand) => {
          const original = brand.getAttribute("style");
          const product = brand.querySelector(".md-header__product");
          const productOriginal = product?.getAttribute("style");
          brand.style.letterSpacing = "0.12em";
          brand.style.wordSpacing = "0.16em";
          if (product) product.style.lineHeight = "1.5";
          const seal = brand.querySelector(".opi-header__seal");
          const theme = document.querySelector(
            "[data-opi-palette-toggle]:not([hidden])"
          );
          const brandRect = brand.getBoundingClientRect();
          const themeRect = theme.getBoundingClientRect();
          const value = {
            text: product?.textContent.trim(),
            overflow: brand.scrollWidth > brand.clientWidth,
            pageOverflow: document.documentElement.scrollWidth > innerWidth,
            overlapsTheme: brandRect.right > themeRect.left,
            targetWidth: brandRect.width,
            targetHeight: brandRect.height,
            sealVisible: getComputedStyle(seal).display !== "none",
          };
          if (original === null) brand.removeAttribute("style");
          else brand.setAttribute("style", original);
          if (product && productOriginal === null) product.removeAttribute("style");
          else if (product && productOriginal !== undefined) {
            product.setAttribute("style", productOriginal);
          }
          return value;
        }
        """
    )
    if (
        result["text"] == "OPI Foundations"
        and not result["overflow"]
        and not result["pageOverflow"]
        and not result["overlapsTheme"]
        and result["targetWidth"] >= 44
        and result["targetHeight"] >= 44
        and result["sealVisible"] is expect_seal
    ):
        return []
    return [f"Semantic header ({width}px text spacing): invalid lockup state was {result}."]


def _desktop_tab_order_issues(page: Any) -> list[str]:
    """Walk the real desktop header order once from the skip link."""

    page.evaluate("() => document.activeElement?.blur()")
    expected = (
        (".md-skip", "skip link"),
        (".opi-header__brand", "home lockup"),
        ("[data-opi-palette-toggle]:not([hidden])", "theme control"),
        (".md-search__input", "search field"),
    )
    issues: list[str] = []
    for selector, label in expected:
        page.keyboard.press("Tab")
        if not _active_matches(page, selector):
            issues.append(f"Semantic header (desktop): Tab did not reach the {label} in order.")
            return issues

    for _ in range(4):
        page.keyboard.press("Tab")
        if _active_matches(page, ".md-tabs__link"):
            return issues
    issues.append("Semantic header (desktop): top navigation did not follow the header controls.")
    return issues


def _desktop_header_issues(page: Any, base_url: str) -> list[str]:
    """Validate the full civic lockup and nonmodal desktop projection once."""

    requested_url = urljoin(base_url, "about-us/operating-principles-and-culture/")
    issues = navigate_to_ready_page(page, requested_url, "Semantic header", "desktop")
    if issues:
        return issues

    result = page.evaluate(
        """
        () => {
          const rect = (selector) => {
            const value = document.querySelector(selector)?.getBoundingClientRect();
            return value ? { width: value.width, height: value.height } : null;
          };
          const active = document.querySelector(
            ".md-tabs__item--active .md-tabs__link"
          );
          return {
            header: rect(".md-header__inner"),
            seal: rect(".opi-header__seal"),
            search: rect(".md-search__form"),
            tabs: rect(".md-tabs"),
            activeTab: active?.textContent.trim(),
            brandText: document.querySelector(".opi-header__brand")?.innerText,
            wordmarkVisible:
              getComputedStyle(document.querySelector(".md-header__wordmark")).display !== "none",
            menuVisible:
              getComputedStyle(document.querySelector("[data-opi-drawer-open]")).display !== "none",
            searchButtonVisible:
              getComputedStyle(document.querySelector("[data-opi-search-open]")).display !== "none",
            drawerInert: document.querySelector(".md-sidebar--primary")?.inert,
            drawerRole: document.querySelector(".md-sidebar--primary")?.getAttribute("role"),
            searchInert: document.querySelector("#opi-search")?.inert,
            searchRole: document.querySelector("#opi-search")?.getAttribute("role"),
            searchLabel: document.querySelector("#opi-search")?.getAttribute("aria-label"),
            pageOverflow: document.documentElement.scrollWidth > innerWidth,
          };
        }
        """
    )
    expected_scalars = {
        "activeTab": "About Us",
        "brandText": "City of Baltimore\nOPI Foundations",
        "wordmarkVisible": True,
        "menuVisible": False,
        "searchButtonVisible": False,
        "drawerInert": False,
        "drawerRole": None,
        "searchInert": False,
        "searchRole": None,
        "searchLabel": None,
        "pageOverflow": False,
    }
    for key, expected in expected_scalars.items():
        if result[key] != expected:
            issues.append(
                f"Semantic header (desktop): {key} was {result[key]!r}, expected {expected!r}."
            )
    expected_heights = {"header": 72, "seal": 58, "search": 44, "tabs": 48}
    for key, expected in expected_heights.items():
        if result[key] is None or result[key]["height"] != expected:
            issues.append(
                f"Semantic header (desktop): {key} geometry was {result[key]}, "
                f"expected {expected}px high."
            )
    issues.extend(_active_location_marker_issues(page))
    issues.extend(_desktop_tab_order_issues(page))

    active_tab = page.locator(".md-tabs__item--active .md-tabs__link")
    active_tab.focus()
    issues.extend(_focus_indicator_issues(page, ".md-tabs__item--active .md-tabs__link", "Tabs"))
    issues.extend(_breakpoint_issues(page))
    return issues
