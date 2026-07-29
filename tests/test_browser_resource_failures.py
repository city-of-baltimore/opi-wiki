"""Tests for context-wide browser resource assurance."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock

import pytest
from scripts.repo_tools.browser_resources import (
    BrowserResourceObserver,
    _is_expected_live_reload_cancellation,
    _is_expected_search_index_cancellation,
)
from scripts.repo_tools.browser_routes import BrowserTarget


def _request(
    url: str,
    resource_type: str,
    failure: str | None = None,
) -> SimpleNamespace:
    """Build one resource-request stand-in."""

    return SimpleNamespace(
        url=url,
        resource_type=resource_type,
        failure=failure,
    )


def _attached_handlers(
    target: BrowserTarget,
    issues: list[str],
) -> tuple[BrowserResourceObserver, dict[str, Any]]:
    """Attach one observer and return its context-wide event handlers."""

    context = MagicMock()
    observer = BrowserResourceObserver(target, issues, "Initial scope")
    observer.attach(context)
    handlers = {call.args[0]: call.args[1] for call in context.on.call_args_list}
    return observer, handlers


def test_observer_attaches_context_wide_and_uses_the_current_scope() -> None:
    """One observer should cover every page created by its browser context."""

    issues: list[str] = []
    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))
    observer, handlers = _attached_handlers(target, issues)

    assert set(handlers) == {"response", "requestfailed"}
    observer.set_scope("Search (dark)")
    request = _request("https://cdn.example/runtime.js", "script")
    handlers["response"](SimpleNamespace(status=200, url=request.url, request=request))

    assert issues == [
        "Search (dark): unexpected external resource "
        "https://cdn.example/runtime.js returned HTTP 200."
    ]


def test_observer_rejects_target_errors_and_every_unexpected_external_response() -> None:
    """External HTTP success must not bypass the hermetic resource boundary."""

    issues: list[str] = []
    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))
    _observer, handlers = _attached_handlers(target, issues)
    responses = (
        (
            _request(
                "https://city.example/opi-wiki/assets/stylesheets/main.css",
                "stylesheet",
            ),
            200,
        ),
        (
            _request(
                "https://city.example/opi-wiki/assets/stylesheets/missing.css",
                "stylesheet",
            ),
            404,
        ),
        (
            _request(
                "https://fonts.googleapis.com/css?family=Nunito+Sans",
                "stylesheet",
            ),
            404,
        ),
        (
            _request("https://cdn.example/runtime.js", "script"),
            200,
        ),
        (
            _request("https://cdn.example/missing.js", "script"),
            404,
        ),
        (
            _request("https://fonts.googleapis.com/runtime.js", "script"),
            200,
        ),
        (
            _request("https://fonts.googleapis.com.evil.test/font.woff2", "font"),
            200,
        ),
        (
            _request("http://fonts.googleapis.com/css?family=Nunito+Sans", "stylesheet"),
            200,
        ),
    )

    for request, status in responses:
        handlers["response"](SimpleNamespace(status=status, url=request.url, request=request))

    assert issues == [
        "Initial scope: target resource "
        "https://city.example/opi-wiki/assets/stylesheets/missing.css returned HTTP 404.",
        "Initial scope: unexpected external resource "
        "https://cdn.example/runtime.js returned HTTP 200.",
        "Initial scope: unexpected external resource "
        "https://cdn.example/missing.js returned HTTP 404.",
        "Initial scope: unexpected external resource "
        "https://fonts.googleapis.com/runtime.js returned HTTP 200.",
        "Initial scope: unexpected external resource "
        "https://fonts.googleapis.com.evil.test/font.woff2 returned HTTP 200.",
        "Initial scope: unexpected external resource "
        "http://fonts.googleapis.com/css?family=Nunito+Sans returned HTTP 200.",
    ]


def test_observer_rejects_blocking_transport_failures_and_allows_font_delivery() -> None:
    """Only exact typography origins and resource types may fail nonblockingly."""

    issues: list[str] = []
    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))
    _observer, handlers = _attached_handlers(target, issues)
    requests = (
        _request(
            "https://fonts.gstatic.com/s/nunitosans/v1/font.woff2",
            "font",
            "net::ERR_FAILED",
        ),
        _request(
            "https://city.example/opi-wiki/assets/missing.js",
            "script",
            "connection reset",
        ),
        _request(
            "https://cdn.example/cancelled.js",
            "script",
            "net::ERR_ABORTED",
        ),
        _request(
            "https://city.example/opi-wiki/assets/unknown.js",
            "script",
        ),
    )

    for request in requests:
        handlers["requestfailed"](request)

    assert issues == [
        "Initial scope: target resource "
        "https://city.example/opi-wiki/assets/missing.js failed: connection reset.",
        "Initial scope: unexpected external resource "
        "https://cdn.example/cancelled.js failed: net::ERR_ABORTED.",
        "Initial scope: target resource "
        "https://city.example/opi-wiki/assets/unknown.js failed: "
        "unknown transport failure.",
    ]


@pytest.mark.parametrize(
    ("url", "resource_type", "failure", "expected"),
    [
        (
            "https://city.example/opi-wiki/search/search_index.json",
            "fetch",
            "net::ERR_ABORTED",
            True,
        ),
        (
            "https://city.example/opi-wiki/search/search_index.json",
            "script",
            "net::ERR_ABORTED",
            False,
        ),
        (
            "https://city.example/opi-wiki/search/search_index.json",
            "fetch",
            "connection reset",
            False,
        ),
        (
            "https://city.example/opi-wiki/nested/search/search_index.json",
            "fetch",
            "net::ERR_ABORTED",
            False,
        ),
        (
            "https://external.example/opi-wiki/search/search_index.json",
            "fetch",
            "net::ERR_ABORTED",
            False,
        ),
        (
            "https://city.example/opi-wiki/search/search_index.json?cache=1",
            "fetch",
            "net::ERR_ABORTED",
            False,
        ),
    ],
)
def test_search_index_cancellation_requires_exact_url_type_and_failure(
    url: str,
    resource_type: str,
    failure: str,
    expected: bool,
) -> None:
    """Misleading suffixes and non-fetch failures must remain blocking."""

    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))
    request = _request(url, resource_type, failure)

    assert (
        _is_expected_search_index_cancellation(
            target,
            request,
            failure,
        )
        is expected
    )


def test_live_reload_cancellation_is_live_same_origin_xhr_only() -> None:
    """The preview exception must not weaken static or external transport failures."""

    request = _request(
        "https://city.example/livereload/123/456",
        "xhr",
        "net::ERR_ABORTED",
    )
    live_target = BrowserTarget("https://city.example/opi-wiki/", ("/",))
    static_target = BrowserTarget(
        "https://city.example/opi-wiki/",
        ("/",),
        Path("/artifact"),
    )

    assert _is_expected_live_reload_cancellation(
        live_target,
        request,
        "net::ERR_ABORTED",
    )
    assert not _is_expected_live_reload_cancellation(
        static_target,
        request,
        "net::ERR_ABORTED",
    )
    assert not _is_expected_live_reload_cancellation(
        live_target,
        _request(
            "https://external.example/livereload/123/456",
            "xhr",
            "net::ERR_ABORTED",
        ),
        "net::ERR_ABORTED",
    )
    assert not _is_expected_live_reload_cancellation(
        live_target,
        _request(
            "https://city.example/livereload/123/456",
            "script",
            "net::ERR_ABORTED",
        ),
        "net::ERR_ABORTED",
    )
    assert not _is_expected_live_reload_cancellation(
        live_target,
        request,
        "connection reset",
    )


def test_observer_allows_only_the_two_exact_expected_cancellations() -> None:
    """Cancellation exceptions should be exercised through the installed handler."""

    issues: list[str] = []
    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))
    _observer, handlers = _attached_handlers(target, issues)
    requests = (
        _request(
            "https://city.example/opi-wiki/search/search_index.json",
            "fetch",
            "net::ERR_ABORTED",
        ),
        _request(
            "https://city.example/livereload/123/456",
            "xhr",
            "net::ERR_ABORTED",
        ),
        _request(
            "https://city.example/opi-wiki/search/search_index.json",
            "script",
            "net::ERR_ABORTED",
        ),
    )

    for request in requests:
        handlers["requestfailed"](request)

    assert issues == [
        "Initial scope: target resource "
        "https://city.example/opi-wiki/search/search_index.json "
        "failed: net::ERR_ABORTED."
    ]
