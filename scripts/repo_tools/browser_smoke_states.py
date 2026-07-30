"""Shared UI state assertions for the browser smoke assurance."""

from __future__ import annotations

from typing import Any

from scripts.repo_tools.browser_smoke_targets import (
    ORG_CHART_NAMES,
    BrowserSmokeTarget,
)


def _resolve_theme_color(page: Any, css_variable: str) -> str:
    """Resolve a CSS custom property to the computed RGB value used by the page."""

    script = """
    ([variableName]) => {
      const probe = document.createElement("div");
      probe.style.color = `var(${variableName})`;
      document.body.appendChild(probe);
      const resolved = getComputedStyle(probe).color;
      probe.remove();
      return resolved;
    }
    """
    return str(page.evaluate(script, [css_variable]))


def _check_mobile_nav_active_state(
    page: Any,
    target: BrowserSmokeTarget,
    scheme: str,
) -> list[str]:
    """Validate the route- and scheme-specific active-link treatment."""

    issues: list[str] = []
    active_link = page.locator(
        ".md-nav--primary .md-nav__link--active",
        has_text=target.active_link_text,
    ).first
    if active_link.count() == 0:
        issues.append(
            f"{target.section} ({scheme}): active nav link "
            f"'{target.active_link_text}' was not found."
        )
    else:
        expected_color = _resolve_theme_color(page, "--opi-nav-accent")
        active_color = active_link.evaluate("element => getComputedStyle(element).color")
        if active_color != expected_color:
            issues.append(
                f"{target.section} ({scheme}): active nav color was {active_color}, "
                f"expected {expected_color}."
            )
    return issues


def _check_table_focus_state(page: Any, scheme: str, navigation: str) -> list[str]:
    """Validate keyboard focusability and focus styling on a generated table wrapper."""

    # Establish keyboard modality before moving focus to the generated region.
    # After an instant-navigation link click, Chromium correctly treats a bare
    # programmatic focus() as pointer-driven and does not match :focus-visible.
    page.keyboard.press("Tab")
    result = page.evaluate(
        """
        () => {
          const region = document.querySelector(".md-typeset__scrollwrap");
          if (!region) return null;
          region.focus();
          const style = getComputedStyle(region);
          return {
            tabIndex: region.tabIndex,
            outlineStyle: style.outlineStyle,
            outlineWidth: style.outlineWidth,
          };
        }
        """
    )
    label = f"Table scroll region ({scheme}, {navigation})"
    if result is None:
        return [f"{label}: generated scroll wrapper was not found."]

    issues: list[str] = []
    if result["tabIndex"] != 0:
        issues.append(f"{label}: tabIndex was {result['tabIndex']}, expected 0.")
    if result["outlineStyle"] == "none" or result["outlineWidth"] == "0px":
        issues.append(f"{label}: keyboard focus outline was not visible.")
    return issues


def _check_org_chart_state(page: Any, scheme: str, navigation: str) -> list[str]:
    """Validate the visible semantic hierarchy and leadership names."""

    result = page.evaluate(
        """
        () => {
          const chart = document.querySelector(".opi-org-chart");
          if (!chart) return null;
          const isVisible = (element) => {
            const style = getComputedStyle(element);
            const rect = element.getBoundingClientRect();
            return style.display !== "none" && style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
          };
          const nodes = [...chart.querySelectorAll(".opi-org-chart__node")];
          const count = (level) =>
            chart.querySelectorAll(`.opi-org-chart__node[data-org-level='${level}']`).length;
          return {
            chartVisible: isVisible(chart),
            chartNames: nodes
              .filter(isVisible)
              .map((node) => node.querySelector(".opi-org-chart__name")?.textContent?.trim())
              .filter(Boolean),
            counts: {
              mayor: count("mayor"),
              city: count("city"),
              executive: count("executive"),
              seniorLead: count("senior-lead"),
              manager: count("manager"),
              team: count("team"),
              staff: count("staff"),
            },
          };
        }
        """
    )
    label = f"Organization chart ({scheme}, {navigation})"
    if result is None:
        return [f"{label}: semantic chart container was not found."]

    issues: list[str] = []
    if not result["chartVisible"]:
        issues.append(f"{label}: chart container had no visible dimensions.")
    missing_chart = [name for name in ORG_CHART_NAMES if name not in result["chartNames"]]
    if missing_chart:
        issues.append(f"{label}: leadership names were not visible: {missing_chart}.")
    expected_counts = {
        "mayor": 1,
        "city": 1,
        "executive": 1,
        "seniorLead": 3,
        "manager": 1,
        "team": 1,
        "staff": 17,
    }
    actual_counts = result["counts"]
    if actual_counts != expected_counts:
        issues.append(
            f"{label}: hierarchy counts were {actual_counts}, expected {expected_counts}."
        )
    return issues
