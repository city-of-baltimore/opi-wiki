"""Homepage page-tools assertions for the browser smoke assurance."""

from __future__ import annotations

from typing import Any


def _check_home_page_tools_layout_state(
    page: Any,
    profile: str,
    expected_width: int,
) -> list[str]:
    """Require the homepage tools to follow the hero as bounded labeled links."""

    result = page.evaluate(
        """
        () => {
          const hero = document.querySelector(".opi-hero");
          const start = document.querySelector("#start-here");
          const toolRows = [...document.querySelectorAll(".opi-page-tools")];
          const legacyCount = document.querySelectorAll(
            "a.md-content__button"
          ).length;
          if (!hero || !start || toolRows.length !== 1) {
            return {
              heroFound: Boolean(hero),
              startFound: Boolean(start),
              toolsCount: toolRows.length,
              legacyCount,
            };
          }

          const tools = toolRows[0];
          const label = tools.querySelector(".opi-page-tools__label");
          const links = [...tools.querySelectorAll("a.opi-page-tools__link")];
          const heroRect = hero.getBoundingClientRect();
          const toolsRect = tools.getBoundingClientRect();
          const startRect = start.getBoundingClientRect();
          const colorProbe = document.createElement("span");
          colorProbe.style.backgroundColor = "var(--opi-bg-soft)";
          document.body.appendChild(colorProbe);
          const expectedBackground = getComputedStyle(colorProbe).backgroundColor;
          colorProbe.remove();
          const visiblyRendered = (element, rect) => {
            if (!element) return false;
            const style = getComputedStyle(element);
            return style.display !== "none" &&
              style.visibility !== "hidden" &&
              Number(style.opacity) !== 0 &&
              rect.width > 0 &&
              rect.height > 0;
          };
          const style = getComputedStyle(tools);
          return {
            heroFound: true,
            startFound: true,
            toolsCount: 1,
            legacyCount,
            viewportWidth: document.documentElement.clientWidth,
            viewportHeight: document.documentElement.clientHeight,
            toolsTag: tools.tagName.toLowerCase(),
            toolsVisible: visiblyRendered(tools, toolsRect),
            toolsBackground: style.backgroundColor,
            expectedBackground,
            toolsLeft: toolsRect.left,
            toolsRight: toolsRect.right,
            toolsTop: toolsRect.top,
            toolsBottom: toolsRect.bottom,
            toolsClientWidth: tools.clientWidth,
            toolsScrollWidth: tools.scrollWidth,
            heroLeft: heroRect.left,
            heroRight: heroRect.right,
            heroBottom: heroRect.bottom,
            startTop: startRect.top,
            startBottom: startRect.bottom,
            startVisible: visiblyRendered(start, startRect),
            followsHero: hero.nextElementSibling === tools,
            labelId: label?.id || "",
            labelText: label?.textContent?.trim() || "",
            labelVisible: visiblyRendered(
              label,
              label?.getBoundingClientRect() || new DOMRect()
            ),
            labelledBy: tools.getAttribute("aria-labelledby") || "",
            visibleIconCount: [
              ...tools.querySelectorAll(".opi-page-tools__icon")
            ].filter((icon) =>
              visiblyRendered(icon, icon.getBoundingClientRect())
            ).length,
            links: links.map((link) => {
              const rect = link.getBoundingClientRect();
              return {
                text: link.textContent?.trim() || "",
                href: link.href,
                relEdit: link.relList.contains("edit"),
                tabIndex: link.tabIndex,
                visible: visiblyRendered(link, rect),
                left: rect.left,
                right: rect.right,
                top: rect.top,
                bottom: rect.bottom,
                width: rect.width,
                height: rect.height,
              };
            }),
          };
        }
        """
    )
    label = f"Home page tools ({expected_width}px, {profile})"
    issues: list[str] = []
    if not result["heroFound"]:
        issues.append(f"{label}: rendered hero was not found.")
    if not result["startFound"]:
        issues.append(f"{label}: rendered Start here heading was not found.")
    if result["toolsCount"] != 1:
        issues.append(f"{label}: found {result['toolsCount']} page-tools rows, expected exactly 1.")
    if result["legacyCount"] != 0:
        issues.append(
            f"{label}: found {result['legacyCount']} legacy floating page actions, expected 0."
        )
    if issues:
        return issues

    viewport_width = result["viewportWidth"]
    if viewport_width != expected_width:
        issues.append(
            f"{label}: browser viewport was {viewport_width}px, expected {expected_width}px."
        )
    if result["toolsTag"] != "nav":
        issues.append(f"{label}: tools container was <{result['toolsTag']}>, expected <nav>.")
    if result["labelText"] != "Page tools" or not result["labelVisible"]:
        issues.append(
            f"{label}: visible tools label was {result['labelText']!r}, expected 'Page tools'."
        )
    if not result["labelId"] or result["labelledBy"] != result["labelId"]:
        issues.append(
            f"{label}: aria-labelledby was {result['labelledBy']!r}, "
            f"expected the visible label id {result['labelId']!r}."
        )
    if not result["toolsVisible"]:
        issues.append(f"{label}: tools row was not visibly rendered.")
    if result["toolsBackground"] != result["expectedBackground"]:
        issues.append(
            f"{label}: tools background was {result['toolsBackground']}, "
            f"expected neutral token {result['expectedBackground']}."
        )
    if not result["followsHero"]:
        issues.append(f"{label}: tools row was not the hero's next rendered element.")
    if abs(result["toolsTop"] - result["heroBottom"]) > 1:
        issues.append(
            f"{label}: tools began at {result['toolsTop']}px, expected to meet "
            f"the hero edge at {result['heroBottom']}px."
        )
    if result["toolsBottom"] > result["startTop"] + 1:
        issues.append(
            f"{label}: tools ended at {result['toolsBottom']}px after Start here began "
            f"at {result['startTop']}px."
        )
    if result["toolsLeft"] < -1 or result["toolsRight"] > viewport_width + 1:
        issues.append(
            f"{label}: tools bounds were {result['toolsLeft']}–"
            f"{result['toolsRight']}px inside a {viewport_width}px viewport."
        )
    if (
        abs(result["toolsLeft"] - result["heroLeft"]) > 1
        or abs(result["toolsRight"] - result["heroRight"]) > 1
    ):
        issues.append(
            f"{label}: tools bounds {result['toolsLeft']}–{result['toolsRight']}px "
            f"did not match hero bounds {result['heroLeft']}–{result['heroRight']}px."
        )
    if result["toolsScrollWidth"] > result["toolsClientWidth"] + 1:
        issues.append(
            f"{label}: tools content width was {result['toolsScrollWidth']}px "
            f"inside {result['toolsClientWidth']}px."
        )

    links = result["links"]
    expected_labels = ["Edit this page", "View source"]
    if [link["text"] for link in links] != expected_labels:
        issues.append(
            f"{label}: link labels were {[link['text'] for link in links]}, "
            f"expected {expected_labels}."
        )
    if len(links) == 2:
        edit_link, view_link = links
        expected_edit_href = "https://github.com/city-of-baltimore/opi-wiki/edit/main/docs/index.md"
        expected_view_href = edit_link["href"]
        for segment in ("/edit/", "/blob/"):
            if segment in expected_view_href:
                expected_view_href = expected_view_href.replace(segment, "/raw/", 1)
                break
        if not edit_link["relEdit"]:
            issues.append(f"{label}: Edit this page link did not expose rel='edit'.")
        if edit_link["href"] != expected_edit_href:
            issues.append(
                f"{label}: Edit this page destination was {edit_link['href']}, "
                f"expected {expected_edit_href}."
            )
        if view_link["href"] != expected_view_href:
            issues.append(
                f"{label}: View source destination was {view_link['href']}, "
                f"expected {expected_view_href}."
            )
        for link in links:
            if link["tabIndex"] != 0:
                issues.append(
                    f"{label}: {link['text']!r} tabIndex was {link['tabIndex']}, expected 0."
                )
            if not link["visible"]:
                issues.append(f"{label}: {link['text']!r} was not visibly rendered.")
            if link["width"] < 44 or link["height"] < 44:
                issues.append(
                    f"{label}: {link['text']!r} target was "
                    f"{link['width']}×{link['height']}px, expected at least 44×44px."
                )
            if (
                link["left"] < result["toolsLeft"] - 1
                or link["right"] > result["toolsRight"] + 1
                or link["top"] < result["toolsTop"] - 1
                or link["bottom"] > result["toolsBottom"] + 1
            ):
                issues.append(f"{label}: {link['text']!r} fell outside the tools row.")
        overlap_width = min(edit_link["right"], view_link["right"]) - max(
            edit_link["left"], view_link["left"]
        )
        overlap_height = min(edit_link["bottom"], view_link["bottom"]) - max(
            edit_link["top"], view_link["top"]
        )
        if overlap_width > 1 and overlap_height > 1:
            issues.append(f"{label}: Edit this page and View source targets overlapped.")
        if result["viewportWidth"] == 320:
            if (
                abs(edit_link["top"] - view_link["top"]) > 1
                or abs(edit_link["bottom"] - view_link["bottom"]) > 1
            ):
                issues.append(f"{label}: narrow-screen tools did not share one row.")
            if result["visibleIconCount"] != 0:
                issues.append(
                    f"{label}: found {result['visibleIconCount']} visible decorative "
                    "icons, expected 0 in the compact treatment."
                )
            if (
                not result["startVisible"]
                or result["startTop"] < -1
                or result["startBottom"] > result["viewportHeight"] + 1
            ):
                issues.append(
                    f"{label}: Start here bounds were {result['startTop']}–"
                    f"{result['startBottom']}px inside a "
                    f"{result['viewportHeight']}px viewport."
                )
        if view_link["top"] < edit_link["top"] - 1 or (
            abs(view_link["top"] - edit_link["top"]) <= 1
            and view_link["left"] < edit_link["left"] - 1
        ):
            issues.append(f"{label}: visual order did not keep Edit before View source.")
    return issues


def _check_home_page_tools_focus_state(page: Any, scheme: str) -> list[str]:
    """Require both homepage tools to expose the scheme-specific focus ring."""

    page.keyboard.press("Tab")
    result = page.evaluate(
        """
        () => {
          const probe = document.createElement("span");
          probe.style.color = "var(--opi-link-color)";
          document.body.appendChild(probe);
          const expectedOutlineColor = getComputedStyle(probe).color;
          probe.remove();
          const links = [
            ...document.querySelectorAll(".opi-page-tools__link")
          ];
          return {
            expectedOutlineColor,
            links: links.map((link) => {
              link.focus();
              const style = getComputedStyle(link);
              return {
                text: link.textContent?.trim() || "",
                active: document.activeElement === link,
                outlineStyle: style.outlineStyle,
                outlineWidth: Number.parseFloat(style.outlineWidth),
                outlineColor: style.outlineColor,
              };
            }),
          };
        }
        """
    )
    label = f"Home page tools focus ({scheme})"
    links = result["links"]
    if len(links) != 2:
        return [f"{label}: found {len(links)} tool links, expected exactly 2."]

    issues: list[str] = []
    for link in links:
        if not link["active"]:
            issues.append(f"{label}: {link['text']!r} could not receive focus.")
        if link["outlineStyle"] == "none" or link["outlineWidth"] < 2:
            issues.append(
                f"{label}: {link['text']!r} outline was "
                f"{link['outlineWidth']}px, expected at least 2px."
            )
        if link["outlineColor"] != result["expectedOutlineColor"]:
            issues.append(
                f"{label}: {link['text']!r} outline was {link['outlineColor']}, "
                f"expected {result['expectedOutlineColor']}."
            )
    return issues
