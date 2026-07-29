"""Tests for interactive states in the full browser accessibility audit."""

from unittest.mock import MagicMock

import pytest
import scripts.repo_tools.browser_accessibility as browser_accessibility
from scripts.repo_tools.browser_accessibility import _AuditProfile


def test_mobile_controls_use_pointer_interaction_without_navigation_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Drawer and search toggles should not wait for a navigation they cannot cause."""

    monkeypatch.setattr(
        browser_accessibility,
        "navigate_to_ready_page",
        lambda *_args: [],
    )
    page = MagicMock()
    drawer_toggle = MagicMock()
    drawer_overlay = MagicMock()
    drawer_overlay.bounding_box.return_value = {
        "x": 0,
        "y": 0,
        "width": 100,
        "height": 100,
    }
    search_toggle = MagicMock()
    for locator in (drawer_toggle, drawer_overlay, search_toggle):
        locator.first = locator
    page.locator.side_effect = (drawer_toggle, drawer_overlay, search_toggle)
    axe = MagicMock()
    axe.run.return_value.response = {"violations": []}
    profile = _AuditProfile("reflow-light", 320, 800, "light", True)

    assert (
        browser_accessibility._check_mobile_interactive_states(
            page,
            axe,
            "https://city.example/opi-wiki/",
            profile,
        )
        == []
    )
    drawer_toggle.click.assert_called_once_with(no_wait_after=True)
    search_toggle.click.assert_called_once_with(no_wait_after=True)
