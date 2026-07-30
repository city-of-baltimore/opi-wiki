"""Homepage card and hero assertions for the browser smoke assurance."""

from __future__ import annotations

from typing import Any


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
    """Require the complete homepage hero to remain visible and reflow safely."""

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
            if (!element) return false;
            const style = getComputedStyle(element);
            return style.display !== "none" &&
              style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 &&
              rect.width > 0 &&
              rect.height > 0;
          };
          const copyState = (element) => {
            const rect = element?.getBoundingClientRect() || new DOMRect();
            return {
              text: element?.textContent?.trim() || "",
              visible: visiblyRendered(element, rect),
            };
          };
          const eyebrow = copyState(
            hero.querySelector(".opi-hero-eyebrow")
          );
          const summary = copyState(
            hero.querySelector(".opi-hero-summary")
          );
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
            eyebrowText: eyebrow.text,
            eyebrowVisible: eyebrow.visible,
            summaryText: summary.text,
            summaryVisible: summary.visible,
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
    for key, name in (("eyebrow", "eyebrow"), ("summary", "summary")):
        if not result[f"{key}Text"]:
            issues.append(f"{label}: authored {name} was empty or missing.")
        elif not result[f"{key}Visible"]:
            issues.append(f"{label}: authored {name} was not visibly rendered.")
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
