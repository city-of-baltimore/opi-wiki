"""Tests for browser smoke targets and page-state validators."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from scripts.repo_tools.browser_smoke_states import (
    _check_home_hero_reflow_state,
    _check_mobile_nav_active_state,
    _check_org_chart_state,
    _check_table_focus_state,
)
from scripts.repo_tools.browser_smoke_targets import ORG_CHART_NAMES, SMOKE_TARGETS


class _EvaluationPage:
    """Playwright page stand-in returning one scripted DOM result."""

    def __init__(self, result: object) -> None:
        self.result = result
        self.keyboard = MagicMock()

    def evaluate(self, script: str) -> object:
        """Return the configured DOM result."""

        del script
        return self.result


def test_smoke_targets_cover_each_major_section() -> None:
    """Browser smoke coverage should keep one representative page per major section."""

    assert [target.section for target in SMOKE_TARGETS] == [
        "About Us",
        "How We Work",
        "What We Do",
        "Resources",
    ]
    assert [target.path for target in SMOKE_TARGETS] == [
        "/about-us/operating-principles-and-culture/",
        "/how-we-work/how-work-moves-through-opi/",
        "/what-we-do/services/cross-agency-delivery/",
        "/resources/reference/glossary/",
    ]


def test_mobile_navigation_checks_only_route_specific_active_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Shared drawer behavior must not be repeated through the route matrix."""

    page = MagicMock()
    active_link = MagicMock()
    active_link.count.return_value = 1
    active_link.evaluate.return_value = "rgb(1, 2, 3)"
    active_link.first = active_link
    page.locator.return_value = active_link
    monkeypatch.setattr(
        "scripts.repo_tools.browser_smoke_states._resolve_theme_color",
        lambda *_args: "rgb(1, 2, 3)",
    )

    assert _check_mobile_nav_active_state(page, SMOKE_TARGETS[0], "light") == []
    page.locator.assert_called_once_with(
        ".md-nav--primary .md-nav__link--active",
        has_text=SMOKE_TARGETS[0].active_link_text,
    )


def test_table_scroll_wrapper_has_keyboard_focus_treatment() -> None:
    """Generated table wrappers should be tabbable and visibly focused."""

    page = _EvaluationPage({"tabIndex": 0, "outlineStyle": "solid", "outlineWidth": "2px"})

    assert _check_table_focus_state(page, "light", "direct load") == []
    page.keyboard.press.assert_called_once_with("Tab")


def test_home_hero_reflow_accepts_intact_words_inside_the_viewport() -> None:
    """Whole heading words and bounded hero geometry should satisfy the ratchet."""

    page = _EvaluationPage(
        {
            "viewportWidth": 320,
            "documentWidth": 320,
            "heroLeft": 0,
            "heroRight": 320,
            "heroTop": 84,
            "heroBottom": 594,
            "heroClientWidth": 320,
            "heroScrollWidth": 320,
            "heroVisible": True,
            "headingLeft": 40,
            "headingRight": 280,
            "headingTop": 234,
            "headingBottom": 326,
            "headingClientWidth": 280,
            "headingScrollWidth": 280,
            "headingVisible": True,
            "words": [
                {"text": "OPI", "lineCount": 1, "fragmentWidths": [59.55]},
                {"text": "Foundations", "lineCount": 1, "fragmentWidths": [201.81]},
            ],
        }
    )

    assert _check_home_hero_reflow_state(page, "reflow-light", 320) == []


def test_home_hero_reflow_reports_missing_broken_and_overflowing_layouts() -> None:
    """A missing hero or mid-word/viewport overflow must fail with measurements."""

    assert _check_home_hero_reflow_state(
        _EvaluationPage(None),
        "reflow-light",
        320,
    ) == ["Home hero (320px, reflow-light): rendered hero and heading were not found."]

    page = _EvaluationPage(
        {
            "viewportWidth": 319,
            "documentWidth": 360,
            "heroLeft": -2,
            "heroRight": 330,
            "heroTop": 84,
            "heroBottom": 594,
            "heroClientWidth": 280,
            "heroScrollWidth": 310,
            "heroVisible": True,
            "headingLeft": 40,
            "headingRight": 280,
            "headingTop": 234,
            "headingBottom": 326,
            "headingClientWidth": 100,
            "headingScrollWidth": 240,
            "headingVisible": True,
            "words": [
                {
                    "text": "Foundations",
                    "lineCount": 2,
                    "fragmentWidths": [224.98, 51.7],
                }
            ],
        }
    )

    issues = _check_home_hero_reflow_state(page, "reflow-light", 320)

    assert len(issues) == 6
    assert "browser viewport was 319px" in issues[0]
    assert "document width was 360px" in issues[1]
    assert "hero bounds were -2–330px" in issues[2]
    assert "hero content width was 310px inside 280px" in issues[3]
    assert "heading content width was 240px inside 100px" in issues[4]
    assert "'Foundations' split across 2 rendered lines" in issues[5]


def test_home_hero_reflow_rejects_vacuous_hidden_or_empty_headings() -> None:
    """Hidden, empty, and zero-fragment headings must not satisfy the visual guard."""

    hidden_page = _EvaluationPage(
        {
            "viewportWidth": 320,
            "documentWidth": 320,
            "heroLeft": 0,
            "heroRight": 320,
            "heroTop": 84,
            "heroBottom": 594,
            "heroClientWidth": 320,
            "heroScrollWidth": 320,
            "heroVisible": False,
            "headingLeft": 40,
            "headingRight": 40,
            "headingTop": 234,
            "headingBottom": 234,
            "headingClientWidth": 0,
            "headingScrollWidth": 0,
            "headingVisible": False,
            "words": [{"text": "OPI", "lineCount": 0, "fragmentWidths": []}],
        }
    )

    issues = _check_home_hero_reflow_state(hidden_page, "reflow-light", 320)

    assert issues == [
        "Home hero (320px, reflow-light): hero and heading were not both visibly rendered.",
        "Home hero (320px, reflow-light): 'OPI' had no visible rendered line.",
    ]

    empty_page = _EvaluationPage(
        {
            "viewportWidth": 320,
            "documentWidth": 320,
            "heroLeft": 0,
            "heroRight": 320,
            "heroTop": 84,
            "heroBottom": 594,
            "heroClientWidth": 320,
            "heroScrollWidth": 320,
            "heroVisible": True,
            "headingLeft": 40,
            "headingRight": 280,
            "headingTop": 234,
            "headingBottom": 286,
            "headingClientWidth": 280,
            "headingScrollWidth": 280,
            "headingVisible": True,
            "words": [],
        }
    )

    assert _check_home_hero_reflow_state(empty_page, "reflow-light", 320) == [
        "Home hero (320px, reflow-light): heading contained no rendered words."
    ]

    off_canvas_page = _EvaluationPage(
        {
            "viewportWidth": 320,
            "documentWidth": 320,
            "heroLeft": 0,
            "heroRight": 320,
            "heroTop": 84,
            "heroBottom": 594,
            "heroClientWidth": 320,
            "heroScrollWidth": 320,
            "heroVisible": True,
            "headingLeft": -9999,
            "headingRight": -9719,
            "headingTop": 234,
            "headingBottom": 286,
            "headingClientWidth": 280,
            "headingScrollWidth": 280,
            "headingVisible": True,
            "words": [{"text": "OPI", "lineCount": 1, "fragmentWidths": [59.55]}],
        }
    )

    issues = _check_home_hero_reflow_state(off_canvas_page, "reflow-light", 320)

    assert len(issues) == 1
    assert "heading bounds -9999–-9719px" in issues[0]
    assert "fell outside hero bounds" in issues[0]


def test_table_scroll_wrapper_reports_missing_or_inaccessible_state() -> None:
    """Missing wrappers, tabindex drift, and invisible focus must be actionable."""

    assert _check_table_focus_state(_EvaluationPage(None), "dark", "direct load") == [
        "Table scroll region (dark, direct load): generated scroll wrapper was not found."
    ]

    issues = _check_table_focus_state(
        _EvaluationPage({"tabIndex": -1, "outlineStyle": "none", "outlineWidth": "0px"}),
        "dark",
        "instant navigation",
    )

    assert len(issues) == 2
    assert "tabIndex was -1" in issues[0]
    assert "focus outline was not visible" in issues[1]


def test_org_chart_exposes_the_expected_visible_hierarchy() -> None:
    """The rendered chart should expose all leaders at the intended levels."""

    page = _EvaluationPage(
        {
            "chartVisible": True,
            "chartNames": list(ORG_CHART_NAMES),
            "counts": {
                "mayor": 1,
                "city": 1,
                "executive": 1,
                "seniorLead": 3,
                "manager": 1,
                "team": 1,
                "staff": 17,
            },
        }
    )

    assert _check_org_chart_state(page, "light", "direct load") == []


def test_org_chart_reports_missing_names_and_hierarchy_drift() -> None:
    """Chart regressions should name both the missing leaders and structural mismatch."""

    page = _EvaluationPage(
        {
            "chartVisible": False,
            "chartNames": [],
            "counts": {
                "mayor": 0,
                "city": 0,
                "executive": 0,
                "seniorLead": 0,
                "manager": 0,
                "team": 0,
                "staff": 0,
            },
        }
    )

    issues = _check_org_chart_state(page, "dark", "instant navigation")

    assert len(issues) == 3
    assert "no visible dimensions" in issues[0]
    assert "leadership names were not visible" in issues[1]
    assert "hierarchy counts" in issues[2]
