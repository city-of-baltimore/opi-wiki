"""Tests for homepage page-tools browser-state validators."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

from scripts.repo_tools.browser_home_tools import (
    _check_home_page_tools_focus_state,
    _check_home_page_tools_layout_state,
)


class _EvaluationPage:
    """Playwright page stand-in returning one scripted DOM result."""

    def __init__(self, result: object) -> None:
        self.result = result
        self.keyboard = MagicMock()

    def evaluate(self, script: str) -> object:
        """Return the configured DOM result."""

        del script
        return self.result


def _home_page_tools_result() -> dict[str, Any]:
    """Return one valid rendered homepage-tools measurement."""

    return {
        "heroFound": True,
        "startFound": True,
        "toolsCount": 1,
        "legacyCount": 0,
        "viewportWidth": 320,
        "viewportHeight": 800,
        "toolsTag": "nav",
        "toolsVisible": True,
        "toolsBackground": "rgb(247, 251, 252)",
        "expectedBackground": "rgb(247, 251, 252)",
        "toolsLeft": 0,
        "toolsRight": 320,
        "toolsTop": 594,
        "toolsBottom": 660,
        "toolsClientWidth": 320,
        "toolsScrollWidth": 320,
        "heroLeft": 0,
        "heroRight": 320,
        "heroBottom": 594,
        "startTop": 708,
        "startBottom": 756,
        "startVisible": True,
        "followsHero": True,
        "labelId": "opi-page-tools-label",
        "labelText": "Page tools",
        "labelVisible": True,
        "labelledBy": "opi-page-tools-label",
        "visibleIconCount": 0,
        "links": [
            {
                "text": "Edit this page",
                "href": "https://github.com/city-of-baltimore/opi-wiki/edit/main/docs/index.md",
                "relEdit": True,
                "tabIndex": 0,
                "visible": True,
                "left": 20,
                "right": 152,
                "top": 610,
                "bottom": 654,
                "width": 132,
                "height": 44,
            },
            {
                "text": "View source",
                "href": "https://github.com/city-of-baltimore/opi-wiki/raw/main/docs/index.md",
                "relEdit": False,
                "tabIndex": 0,
                "visible": True,
                "left": 160,
                "right": 300,
                "top": 610,
                "bottom": 654,
                "width": 140,
                "height": 44,
            },
        ],
    }


def test_home_page_tools_accept_labeled_bounded_links_below_the_hero() -> None:
    """The utility row should preserve clear labels, targets, and source mapping."""

    assert (
        _check_home_page_tools_layout_state(
            _EvaluationPage(_home_page_tools_result()),
            "reflow-light",
            320,
        )
        == []
    )


def test_home_page_tools_reject_missing_and_legacy_actions() -> None:
    """A missing replacement or surviving floating buttons must fail together."""

    page = _EvaluationPage(
        {
            "heroFound": True,
            "startFound": True,
            "toolsCount": 0,
            "legacyCount": 2,
        }
    )

    assert _check_home_page_tools_layout_state(page, "desktop", 1440) == [
        "Home page tools (1440px, desktop): found 0 page-tools rows, expected exactly 1.",
        "Home page tools (1440px, desktop): found 2 legacy floating page actions, expected 0.",
    ]


def test_home_page_tools_report_semantic_geometry_and_target_drift() -> None:
    """One adversarial fixture should exercise every authored row guarantee."""

    result = _home_page_tools_result()
    result.update(
        {
            "viewportWidth": 319,
            "toolsTag": "div",
            "toolsVisible": False,
            "toolsBackground": "rgba(0, 0, 0, 0)",
            "expectedBackground": "rgb(247, 251, 252)",
            "toolsLeft": -2,
            "toolsRight": 330,
            "toolsTop": 580,
            "toolsBottom": 780,
            "toolsClientWidth": 300,
            "toolsScrollWidth": 340,
            "heroLeft": 0,
            "heroRight": 320,
            "heroBottom": 594,
            "startTop": 760,
            "followsHero": False,
            "labelId": "",
            "labelText": "Utilities",
            "labelVisible": False,
            "labelledBy": "missing-label",
            "links": [
                {
                    "text": "Edit",
                    "href": "https://example.test/edit/page",
                    "relEdit": False,
                    "tabIndex": -1,
                    "visible": False,
                    "left": -5,
                    "right": 35,
                    "top": 570,
                    "bottom": 610,
                    "width": 40,
                    "height": 40,
                },
                {
                    "text": "Source",
                    "href": "https://example.test/not-raw/page",
                    "relEdit": False,
                    "tabIndex": -1,
                    "visible": True,
                    "left": 290,
                    "right": 335,
                    "top": 740,
                    "bottom": 780,
                    "width": 45,
                    "height": 40,
                },
            ],
        }
    )

    issues = _check_home_page_tools_layout_state(
        _EvaluationPage(result),
        "reflow-light",
        320,
    )

    assert len(issues) == 23
    assert "browser viewport was 319px" in issues[0]
    assert "tools container was <div>" in issues[1]
    assert "visible tools label was 'Utilities'" in issues[2]
    assert "aria-labelledby was 'missing-label'" in issues[3]
    assert "tools row was not visibly rendered" in issues[4]
    assert "tools background was rgba(0, 0, 0, 0)" in issues[5]
    assert "was not the hero's next rendered element" in issues[6]
    assert "expected to meet the hero edge" in issues[7]
    assert "after Start here began" in issues[8]
    assert "tools bounds were -2–330px" in issues[9]
    assert "did not match hero bounds" in issues[10]
    assert "tools content width was 340px inside 300px" in issues[11]
    assert "link labels were ['Edit', 'Source']" in issues[12]
    assert "did not expose rel='edit'" in issues[13]
    assert "Edit this page destination" in issues[14]
    assert "View source destination" in issues[15]
    assert "'Edit' tabIndex was -1" in issues[16]
    assert "'Edit' was not visibly rendered" in issues[17]
    assert "'Edit' target was 40×40px" in issues[18]
    assert "'Edit' fell outside the tools row" in issues[19]
    assert "'Source' tabIndex was -1" in issues[20]
    assert "'Source' target was 45×40px" in issues[21]
    assert "'Source' fell outside the tools row" in issues[22]


def test_home_page_tools_reject_overlapping_targets() -> None:
    """Individually bounded controls must still occupy distinct hit regions."""

    result = _home_page_tools_result()
    edit_link = result["links"][0]
    result["links"][1].update(
        {
            "left": edit_link["left"],
            "right": edit_link["right"],
            "top": edit_link["top"],
            "bottom": edit_link["bottom"],
        }
    )

    assert _check_home_page_tools_layout_state(
        _EvaluationPage(result),
        "reflow-light",
        320,
    ) == [
        "Home page tools (320px, reflow-light): Edit this page and View source targets overlapped."
    ]


def test_home_page_tools_reject_a_tall_stacked_320px_treatment() -> None:
    """The narrow outcome must keep tools compact and the primary journey visible."""

    result = _home_page_tools_result()
    result["visibleIconCount"] = 2
    result["toolsBottom"] = 712
    result["startTop"] = 812
    result["startBottom"] = 860
    result["links"][1].update(
        {
            "top": 662,
            "bottom": 706,
        }
    )

    assert _check_home_page_tools_layout_state(
        _EvaluationPage(result),
        "reflow-light",
        320,
    ) == [
        "Home page tools (320px, reflow-light): narrow-screen tools did not share one row.",
        "Home page tools (320px, reflow-light): found 2 visible decorative "
        "icons, expected 0 in the compact treatment.",
        "Home page tools (320px, reflow-light): Start here bounds were "
        "812–860px inside a 800px viewport.",
    ]


def test_home_page_tools_focus_uses_the_scheme_token() -> None:
    """Both visible links should receive the intended focus outline."""

    page = _EvaluationPage(
        {
            "expectedOutlineColor": "rgb(95, 77, 134)",
            "links": [
                {
                    "text": "Edit this page",
                    "active": True,
                    "outlineStyle": "solid",
                    "outlineWidth": 3,
                    "outlineColor": "rgb(95, 77, 134)",
                },
                {
                    "text": "View source",
                    "active": True,
                    "outlineStyle": "solid",
                    "outlineWidth": 3,
                    "outlineColor": "rgb(95, 77, 134)",
                },
            ],
        }
    )

    assert _check_home_page_tools_focus_state(page, "light") == []
    page.keyboard.press.assert_called_once_with("Tab")


def test_home_page_tools_focus_rejects_missing_and_weak_outlines() -> None:
    """Missing links, failed focus, and weak or token-drifted outlines must fail."""

    assert _check_home_page_tools_focus_state(
        _EvaluationPage({"expectedOutlineColor": "rgb(1, 2, 3)", "links": []}),
        "dark",
    ) == ["Home page tools focus (dark): found 0 tool links, expected exactly 2."]

    page = _EvaluationPage(
        {
            "expectedOutlineColor": "rgb(214, 196, 255)",
            "links": [
                {
                    "text": "Edit this page",
                    "active": False,
                    "outlineStyle": "solid",
                    "outlineWidth": 1,
                    "outlineColor": "rgb(0, 0, 0)",
                },
                {
                    "text": "View source",
                    "active": True,
                    "outlineStyle": "solid",
                    "outlineWidth": 3,
                    "outlineColor": "rgb(214, 196, 255)",
                },
            ],
        }
    )

    issues = _check_home_page_tools_focus_state(page, "dark")

    assert len(issues) == 3
    assert "could not receive focus" in issues[0]
    assert "outline was 1px, expected at least 2px" in issues[1]
    assert "outline was rgb(0, 0, 0)" in issues[2]
