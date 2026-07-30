"""Tests for homepage card and hero browser-state validators."""

from __future__ import annotations

from unittest.mock import MagicMock

from scripts.repo_tools.browser_home_states import _check_home_hero_reflow_state


class _EvaluationPage:
    """Playwright page stand-in returning one scripted DOM result."""

    def __init__(self, result: object) -> None:
        self.result = result
        self.keyboard = MagicMock()

    def evaluate(self, script: str) -> object:
        """Return the configured DOM result."""

        del script
        return self.result


def _home_hero_result() -> dict[str, object]:
    """Return one valid rendered homepage-hero measurement."""

    return {
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
        "eyebrowText": "Mayor's Office of Performance and Innovation",
        "eyebrowVisible": True,
        "summaryText": "How a modern performance and innovation office runs.",
        "summaryVisible": True,
        "words": [
            {"text": "OPI", "lineCount": 1, "fragmentWidths": [59.55]},
            {"text": "Foundations", "lineCount": 1, "fragmentWidths": [201.81]},
        ],
    }


def test_home_hero_reflow_accepts_complete_intact_copy_inside_the_viewport() -> None:
    """Whole heading words and visible authored copy should satisfy the ratchet."""

    assert (
        _check_home_hero_reflow_state(
            _EvaluationPage(_home_hero_result()),
            "reflow-light",
            320,
        )
        == []
    )


def test_home_hero_reflow_reports_missing_broken_and_overflowing_layouts() -> None:
    """A missing hero or mid-word/viewport overflow must fail with measurements."""

    assert _check_home_hero_reflow_state(
        _EvaluationPage(None),
        "reflow-light",
        320,
    ) == ["Home hero (320px, reflow-light): rendered hero and heading were not found."]

    result = _home_hero_result()
    result.update(
        {
            "viewportWidth": 319,
            "documentWidth": 360,
            "heroLeft": -2,
            "heroRight": 330,
            "heroClientWidth": 280,
            "heroScrollWidth": 310,
            "headingClientWidth": 100,
            "headingScrollWidth": 240,
            "words": [
                {
                    "text": "Foundations",
                    "lineCount": 2,
                    "fragmentWidths": [224.98, 51.7],
                }
            ],
        }
    )

    issues = _check_home_hero_reflow_state(
        _EvaluationPage(result),
        "reflow-light",
        320,
    )

    assert len(issues) == 6
    assert "browser viewport was 319px" in issues[0]
    assert "document width was 360px" in issues[1]
    assert "hero bounds were -2–330px" in issues[2]
    assert "hero content width was 310px inside 280px" in issues[3]
    assert "heading content width was 240px inside 100px" in issues[4]
    assert "'Foundations' split across 2 rendered lines" in issues[5]


def test_home_hero_reflow_rejects_vacuous_hidden_or_empty_headings() -> None:
    """Hidden, empty, and zero-fragment headings must not satisfy the visual guard."""

    hidden_result = _home_hero_result()
    hidden_result.update(
        {
            "heroVisible": False,
            "headingRight": 40,
            "headingBottom": 234,
            "headingClientWidth": 0,
            "headingScrollWidth": 0,
            "headingVisible": False,
            "words": [{"text": "OPI", "lineCount": 0, "fragmentWidths": []}],
        }
    )

    issues = _check_home_hero_reflow_state(
        _EvaluationPage(hidden_result),
        "reflow-light",
        320,
    )

    assert issues == [
        "Home hero (320px, reflow-light): hero and heading were not both visibly rendered.",
        "Home hero (320px, reflow-light): 'OPI' had no visible rendered line.",
    ]

    empty_result = _home_hero_result()
    empty_result["words"] = []

    assert _check_home_hero_reflow_state(
        _EvaluationPage(empty_result),
        "reflow-light",
        320,
    ) == ["Home hero (320px, reflow-light): heading contained no rendered words."]

    off_canvas_result = _home_hero_result()
    off_canvas_result.update(
        {
            "headingLeft": -9999,
            "headingRight": -9719,
        }
    )

    issues = _check_home_hero_reflow_state(
        _EvaluationPage(off_canvas_result),
        "reflow-light",
        320,
    )

    assert len(issues) == 1
    assert "heading bounds -9999–-9719px" in issues[0]
    assert "fell outside hero bounds" in issues[0]


def test_home_hero_reflow_rejects_missing_or_hidden_authored_copy() -> None:
    """A metadata typo must not silently erase the homepage eyebrow or summary."""

    result = _home_hero_result()
    result.update(
        {
            "eyebrowText": "",
            "eyebrowVisible": False,
            "summaryVisible": False,
        }
    )

    assert _check_home_hero_reflow_state(
        _EvaluationPage(result),
        "desktop",
        320,
    ) == [
        "Home hero (320px, desktop): authored eyebrow was empty or missing.",
        "Home hero (320px, desktop): authored summary was not visibly rendered.",
    ]
