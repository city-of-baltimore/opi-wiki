"""Tests that every browser-audit context installs resource assurance."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock

import pytest
import scripts.repo_tools.browser_accessibility as browser_accessibility
import scripts.repo_tools.browser_header as browser_header
import scripts.repo_tools.browser_smoke as browser_smoke
from scripts.repo_tools.browser_routes import BrowserTarget


class _ObserverSpy:
    """Capture observer construction and attachment without browser events."""

    instances: list[_ObserverSpy] = []

    def __init__(
        self,
        target: BrowserTarget,
        issues: list[str],
        scope: str,
    ) -> None:
        self.target = target
        self.issues = issues
        self.scope = scope
        self.context: Any | None = None
        self.__class__.instances.append(self)

    def attach(self, context: Any) -> None:
        """Record the context covered by this observer."""

        self.context = context

    def set_scope(self, scope: str) -> None:
        """Record the latest operation label."""

        self.scope = scope


def _browser_manager(browser: Any) -> MagicMock:
    """Return a Playwright context-manager stand-in for one browser."""

    playwright = SimpleNamespace(chromium=SimpleNamespace(launch=lambda: browser))
    manager = MagicMock()
    manager.__enter__.return_value = playwright
    return manager


def test_axe_disables_only_its_analyzer_generated_stylesheet_preload() -> None:
    """Synthetic axe XHRs must not be confused with product resource traffic."""

    axe = MagicMock()
    axe.run.return_value.response = {"violations": []}
    page = MagicMock()

    assert browser_accessibility._run_axe(axe, page) == {"violations": []}
    axe.run.assert_called_once_with(
        page,
        options={
            "resultTypes": ["violations"],
            "preload": False,
        },
    )


def test_smoke_attaches_resource_monitoring_to_canonical_and_interaction_contexts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The canonical crawler and both color schemes must share the resource gate."""

    _ObserverSpy.instances = []
    monkeypatch.setattr(browser_smoke, "BrowserResourceObserver", _ObserverSpy)
    monkeypatch.setattr(browser_smoke, "_check_semantic_header", lambda *_args: [])
    monkeypatch.setattr(browser_smoke, "_check_mobile_nav_active_state", lambda *_args: [])
    monkeypatch.setattr(browser_smoke, "_check_table_focus_state", lambda *_args: [])
    monkeypatch.setattr(
        browser_smoke,
        "_check_table_focus_after_instant_navigation",
        lambda *_args: [],
    )
    monkeypatch.setattr(browser_smoke, "_check_card_focus_state", lambda *_args: [])
    monkeypatch.setattr(browser_smoke, "_check_org_chart_state", lambda *_args: [])
    monkeypatch.setattr(
        browser_smoke,
        "_check_org_chart_after_instant_navigation",
        lambda *_args: [],
    )
    monkeypatch.setattr(
        browser_smoke,
        "navigate_to_ready_page",
        lambda *_args, **_kwargs: [],
    )
    page = MagicMock()
    context = MagicMock()
    context.new_page.return_value = page
    browser = MagicMock()
    browser.new_context.return_value = context
    manager = _browser_manager(browser)
    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))

    assert browser_smoke._collect_browser_smoke_issues(lambda: manager, target) == []

    assert len(_ObserverSpy.instances) == 3
    assert all(observer.target == target for observer in _ObserverSpy.instances)
    assert all(observer.context is context for observer in _ObserverSpy.instances)


def test_semantic_header_attaches_resource_monitoring_to_each_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mobile, desktop, and fallback header proofs must all fail on resource drift."""

    _ObserverSpy.instances = []
    contexts = [MagicMock(name=name) for name in ("mobile", "desktop", "fallback")]
    for context in contexts:
        context.new_page.return_value = MagicMock()

    monkeypatch.setattr(
        browser_header,
        "create_browser_context",
        MagicMock(side_effect=contexts),
    )
    monkeypatch.setattr(browser_header, "BrowserResourceObserver", _ObserverSpy)
    monkeypatch.setattr(browser_header, "_mobile_header_journey", lambda *_args: [])
    monkeypatch.setattr(browser_header, "_desktop_header_issues", lambda *_args: [])
    monkeypatch.setattr(
        browser_header,
        "_no_javascript_fallback_issues",
        lambda *_args: [],
    )
    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))

    assert browser_header._check_semantic_header(MagicMock(), target) == []
    assert [(observer.scope, observer.context) for observer in _ObserverSpy.instances] == [
        ("Semantic header (mobile)", contexts[0]),
        ("Semantic header (desktop)", contexts[1]),
        ("Semantic header (no JavaScript)", contexts[2]),
    ]
    assert all(observer.target == target for observer in _ObserverSpy.instances)
    assert all(context.close.call_count == 1 for context in contexts)


def test_accessibility_attaches_resource_monitoring_to_every_profile_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every viewport and color-scheme audit must enforce the same resource gate."""

    _ObserverSpy.instances = []
    monkeypatch.setattr(
        browser_accessibility,
        "BrowserResourceObserver",
        _ObserverSpy,
    )
    monkeypatch.setattr(
        browser_accessibility,
        "navigate_to_ready_page",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setattr(
        browser_accessibility,
        "_format_axe_violations",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setattr(
        browser_accessibility,
        "_check_document_reflow",
        lambda *_args: [],
    )
    monkeypatch.setattr(
        browser_accessibility,
        "_check_skip_link",
        lambda *_args: [],
    )
    monkeypatch.setattr(
        browser_accessibility,
        "_check_mobile_interactive_states",
        lambda *_args: [],
    )
    page = MagicMock()
    context = MagicMock()
    context.new_page.return_value = page
    browser = MagicMock()
    browser.new_context.return_value = context
    manager = _browser_manager(browser)
    axe_factory = MagicMock()
    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))

    assert (
        browser_accessibility._collect_browser_accessibility_issues(
            lambda: manager,
            axe_factory,
            target,
        )
        == []
    )

    assert len(_ObserverSpy.instances) == len(browser_accessibility.AUDIT_PROFILES)
    assert all(observer.target == target for observer in _ObserverSpy.instances)
    assert all(observer.context is context for observer in _ObserverSpy.instances)
