"""Low-level UI state assertions for the browser smoke assurance."""

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


def _check_card_focus_state(page: Any, scheme: str) -> list[str]:
    """Validate that shared cards still expose a visible keyboard focus treatment."""

    card_link = page.locator(".opi-card-link").first
    if card_link.count() == 0:
        return [f"Home ({scheme}): no shared card links were found."]

    card_link.focus()
    outline_style = card_link.evaluate("element => getComputedStyle(element).outlineStyle")
    card_shadow = card_link.locator("xpath=ancestor::article[1]").evaluate(
        "element => getComputedStyle(element).boxShadow"
    )

    issues: list[str] = []
    if outline_style == "none":
        issues.append(f"Home ({scheme}): focused card link lost its visible outline.")
    if card_shadow == "none":
        issues.append(f"Home ({scheme}): focused card lost its focus-within elevation state.")
    return issues


def _check_home_hero_reflow_state(
    page: Any,
    profile: str,
    expected_width: int,
) -> list[str]:
    """Require the homepage hero to fit and wrap its heading between words."""

    result = page.evaluate(
        """
        () => {
          const hero = document.querySelector(".opi-hero");
          const heading = hero?.querySelector("h1");
          if (!hero || !heading) return null;

          const words = [];
          const walker = document.createTreeWalker(
            heading,
            NodeFilter.SHOW_TEXT
          );
          for (let node = walker.nextNode(); node; node = walker.nextNode()) {
            const text = node.textContent || "";
            for (const match of text.matchAll(/\\S+/g)) {
              const start = match.index;
              const range = document.createRange();
              range.setStart(node, start);
              range.setEnd(node, start + match[0].length);
              const rects = [...range.getClientRects()].filter(
                (rect) => rect.width > 0 && rect.height > 0
              );
              const lineTops = [];
              for (const rect of rects) {
                if (!lineTops.some((top) => Math.abs(top - rect.top) < 1)) {
                  lineTops.push(rect.top);
                }
              }
              words.push({
                text: match[0],
                lineCount: lineTops.length,
                fragmentWidths: rects.map(
                  (rect) => Math.round(rect.width * 100) / 100
                ),
              });
            }
          }

          const heroRect = hero.getBoundingClientRect();
          const headingRect = heading.getBoundingClientRect();
          const visiblyRendered = (element, rect) => {
            const style = getComputedStyle(element);
            return style.display !== "none" &&
              style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 &&
              rect.width > 0 &&
              rect.height > 0;
          };
          return {
            viewportWidth: document.documentElement.clientWidth,
            documentWidth: Math.max(
              document.documentElement.scrollWidth,
              document.body?.scrollWidth || 0
            ),
            heroLeft: heroRect.left,
            heroRight: heroRect.right,
            heroTop: heroRect.top,
            heroBottom: heroRect.bottom,
            heroClientWidth: hero.clientWidth,
            heroScrollWidth: hero.scrollWidth,
            heroVisible: visiblyRendered(hero, heroRect),
            headingLeft: headingRect.left,
            headingRight: headingRect.right,
            headingTop: headingRect.top,
            headingBottom: headingRect.bottom,
            headingClientWidth: heading.clientWidth,
            headingScrollWidth: heading.scrollWidth,
            headingVisible: visiblyRendered(heading, headingRect),
            words,
          };
        }
        """
    )
    label = f"Home hero ({expected_width}px, {profile})"
    if result is None:
        return [f"{label}: rendered hero and heading were not found."]

    issues: list[str] = []
    viewport_width = result["viewportWidth"]
    if viewport_width != expected_width:
        issues.append(
            f"{label}: browser viewport was {viewport_width}px, expected {expected_width}px."
        )
    if result["documentWidth"] > viewport_width + 1:
        issues.append(
            f"{label}: document width was {result['documentWidth']}px "
            f"inside a {viewport_width}px viewport."
        )
    if result["heroLeft"] < -1 or result["heroRight"] > viewport_width + 1:
        issues.append(
            f"{label}: hero bounds were {result['heroLeft']}–"
            f"{result['heroRight']}px inside a {viewport_width}px viewport."
        )
    if (
        result["headingLeft"] < result["heroLeft"] - 1
        or result["headingRight"] > result["heroRight"] + 1
        or result["headingTop"] < result["heroTop"] - 1
        or result["headingBottom"] > result["heroBottom"] + 1
    ):
        issues.append(
            f"{label}: heading bounds "
            f"{result['headingLeft']}–{result['headingRight']}px × "
            f"{result['headingTop']}–{result['headingBottom']}px fell outside "
            f"hero bounds {result['heroLeft']}–{result['heroRight']}px × "
            f"{result['heroTop']}–{result['heroBottom']}px."
        )
    if result["heroScrollWidth"] > result["heroClientWidth"] + 1:
        issues.append(
            f"{label}: hero content width was {result['heroScrollWidth']}px "
            f"inside {result['heroClientWidth']}px."
        )
    if result["headingScrollWidth"] > result["headingClientWidth"] + 1:
        issues.append(
            f"{label}: heading content width was {result['headingScrollWidth']}px "
            f"inside {result['headingClientWidth']}px."
        )
    if not result["heroVisible"] or not result["headingVisible"]:
        issues.append(f"{label}: hero and heading were not both visibly rendered.")
    if not result["words"]:
        issues.append(f"{label}: heading contained no rendered words.")
    for word in result["words"]:
        if word["lineCount"] == 0:
            issues.append(f"{label}: {word['text']!r} had no visible rendered line.")
        elif word["lineCount"] > 1:
            issues.append(
                f"{label}: {word['text']!r} split across "
                f"{word['lineCount']} rendered lines with fragment widths "
                f"{word['fragmentWidths']}; hero copy must wrap only between words."
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
