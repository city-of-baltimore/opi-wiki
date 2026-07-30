"""Rendered current-location marker proof for the semantic civic header."""

from __future__ import annotations

from typing import Any


def _active_location_marker_issues(page: Any) -> list[str]:
    """Require active location markers in normal and forced-color rendering."""

    normal = page.evaluate(
        """
        () => {
          const active = document.querySelector(
            ".md-tabs__item--active .md-tabs__link"
          );
          const inactive = document.querySelector(
            ".md-tabs__item:not(.md-tabs__item--active) .md-tabs__link"
          );
          const drawerActive = document.querySelector(
            ".md-nav--primary .md-nav__link--active"
          );
          const drawerInactive = document.querySelector(
            ".md-nav--primary .md-nav__link:not(.md-nav__link--active)"
          );
          const probe = document.createElement("span");
          probe.style.color = "var(--opi-gold)";
          document.body.appendChild(probe);
          const gold = getComputedStyle(probe).color;
          probe.remove();
          return {
            active: active ? getComputedStyle(active).boxShadow : "none",
            inactive: inactive ? getComputedStyle(inactive).boxShadow : "none",
            drawerActive: drawerActive
              ? getComputedStyle(drawerActive).boxShadow
              : "none",
            drawerInactive: drawerInactive
              ? getComputedStyle(drawerInactive).boxShadow
              : "none",
            gold,
          };
        }
        """
    )
    page.emulate_media(forced_colors="active")
    try:
        forced = page.evaluate(
            """
            () => {
              const tab = document.querySelector(
                ".md-tabs__item--active .md-tabs__link"
              );
              const drawer = document.querySelector(
                ".md-nav--primary .md-nav__link--active"
              );
              const tabStyle = tab ? getComputedStyle(tab) : null;
              const drawerStyle = drawer ? getComputedStyle(drawer) : null;
              return {
                tab: tabStyle
                  ? [tabStyle.borderBottomStyle, parseFloat(tabStyle.borderBottomWidth)]
                  : null,
                drawer: drawerStyle
                  ? [
                      drawerStyle.borderInlineStartStyle,
                      parseFloat(drawerStyle.borderInlineStartWidth),
                    ]
                  : null,
              };
            }
            """
        )
    finally:
        page.emulate_media(forced_colors="none")

    active = normal["active"]
    normal_valid = (
        normal["gold"] in active
        and "0px -3px" in active
        and "inset" in active
        and "0px -3px" not in normal["inactive"]
        and normal["gold"] in normal["drawerActive"]
        and ("3px 0px" in normal["drawerActive"] or "-3px 0px" in normal["drawerActive"])
        and "inset" in normal["drawerActive"]
        and "3px 0px" not in normal["drawerInactive"]
        and "-3px 0px" not in normal["drawerInactive"]
    )
    forced_valid = forced == {
        "tab": ["solid", 3],
        "drawer": ["solid", 3],
    }
    if normal_valid and forced_valid:
        return []
    return [
        "Semantic header (desktop): active marker was "
        f"{active!r} with inactive {normal['inactive']!r}, gold "
        f"{normal['gold']!r}; drawer marker was {normal['drawerActive']!r} "
        f"with inactive {normal['drawerInactive']!r}; forced-color markers "
        f"were {forced!r}."
    ]
