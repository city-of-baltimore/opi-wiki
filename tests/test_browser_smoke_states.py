"""Tests for shared browser smoke targets and page-state validators."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from scripts.repo_tools.browser_smoke_states import (
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
