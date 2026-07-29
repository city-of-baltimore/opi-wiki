"""Tests for direct and Material instant browser navigation readiness."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from scripts.repo_tools.browser_routes import (
    check_page_load,
    navigate_to_instant_page,
    navigate_to_ready_page,
)


class _Response:
    """Minimal Playwright response stand-in for page-load tests."""

    def __init__(self, status: int) -> None:
        self.status = status


class _Page:
    """Minimal Playwright page stand-in for final-URL tests."""

    def __init__(self, url: str) -> None:
        self.url = url


def test_page_load_accepts_a_200_at_the_canonical_url() -> None:
    """A canonical page returning HTTP 200 should pass the load check."""

    requested = "http://127.0.0.1:5208/resources/"

    assert check_page_load(_Page(requested), _Response(200), requested, "Resources", "light") == []


def test_page_load_reports_status_and_unexpected_redirect() -> None:
    """HTTP errors and redirect-only smoke targets must fail with useful evidence."""

    issues = check_page_load(
        _Page("http://127.0.0.1:5208/retired/"),
        _Response(404),
        "http://127.0.0.1:5208/resources/",
        "Resources",
        "dark",
    )

    assert len(issues) == 2
    assert "returned HTTP 404" in issues[0]
    assert "expected canonical URL" in issues[1]


def test_page_load_reports_a_missing_navigation_response() -> None:
    """Non-HTTP navigation results should fail instead of passing vacuously."""

    issues = check_page_load(
        _Page("about:blank"),
        None,
        "http://127.0.0.1:5208/resources/",
        "Resources",
        "light",
    )

    assert issues == ["Resources (light): navigation returned no HTTP response."]


def test_ready_page_navigation_uses_bounded_rendered_document_readiness() -> None:
    """A canonical load should not wait for unrelated live-reload network traffic."""

    requested = "http://127.0.0.1:5208/resources/"
    response = _Response(200)
    page = MagicMock()
    page.url = requested
    page.goto.return_value = response

    assert navigate_to_ready_page(page, requested, "Resources", "light") == []
    page.goto.assert_called_once_with(requested, wait_until="load")
    page.locator.assert_called_once_with("article.md-content__inner")
    page.locator.return_value.first.wait_for.assert_called_once_with(state="visible")
    page.wait_for_function.assert_called_once_with("() => document.fonts.status === 'loaded'")


@pytest.mark.parametrize(
    ("response", "final_url"),
    (
        (None, "about:blank"),
        (_Response(503), "http://127.0.0.1:5208/resources/"),
        (_Response(200), "http://127.0.0.1:5208/retired/"),
    ),
)
def test_ready_page_navigation_preserves_load_failures_without_masking_them(
    response: _Response | None,
    final_url: str,
) -> None:
    """HTTP and canonical-URL failures should surface before a selector timeout."""

    requested = "http://127.0.0.1:5208/resources/"
    page = MagicMock()
    page.url = final_url
    page.goto.return_value = response

    issues = navigate_to_ready_page(page, requested, "Resources", "dark")

    assert issues
    page.locator.assert_not_called()
    page.wait_for_function.assert_not_called()


def test_instant_navigation_requires_the_expected_url_and_unique_target() -> None:
    """Instant navigation should prove route identity and same-document replacement."""

    requested = "http://127.0.0.1:5208/programs/citistat/"
    page = MagicMock()
    page.url = requested
    page.evaluate.side_effect = [
        {
            "token": "transition-token",
            "sourceUrl": "http://127.0.0.1:5208/",
            "timeOrigin": 1234.5,
        },
        True,
    ]
    link = MagicMock()

    assert (
        navigate_to_instant_page(
            page,
            link,
            requested,
            "Search result",
            "light",
            ready_selector="h1#citistat",
        )
        == []
    )
    link.click.assert_called_once_with()
    assert page.wait_for_function.call_count == 3
    assert page.wait_for_function.call_args_list[0].kwargs == {"arg": "http://127.0.0.1:5208/"}
    assert page.wait_for_function.call_args_list[1].kwargs == {"arg": "transition-token"}
    page.locator.assert_called_once_with("h1#citistat")
    page.locator.return_value.first.wait_for.assert_called_once_with(state="visible")
    assert (
        page.wait_for_function.call_args_list[2].args[0]
        == "() => document.fonts.status === 'loaded'"
    )


def test_instant_navigation_reports_final_url_drift_before_target_wait() -> None:
    """A redirect must report the observed route instead of timing out on the target."""

    requested = "http://127.0.0.1:5208/programs/citistat/"
    page = MagicMock()
    page.url = "http://127.0.0.1:5208/retired/"
    page.evaluate.return_value = {
        "token": "transition-token",
        "sourceUrl": "http://127.0.0.1:5208/",
        "timeOrigin": 1234.5,
    }

    issues = navigate_to_instant_page(
        page,
        MagicMock(),
        requested,
        "Search result",
        "dark",
        ready_selector="h1#citistat",
    )

    assert len(issues) == 1
    assert "expected canonical URL" in issues[0]
    page.locator.assert_not_called()


def test_instant_navigation_rejects_a_full_document_reload() -> None:
    """A target loaded by full navigation must not satisfy the instant-navigation gate."""

    requested = "http://127.0.0.1:5208/programs/citistat/"
    page = MagicMock()
    page.url = requested
    page.evaluate.side_effect = [
        {
            "token": "transition-token",
            "sourceUrl": "http://127.0.0.1:5208/",
            "timeOrigin": 1234.5,
        },
        False,
    ]

    issues = navigate_to_instant_page(
        page,
        MagicMock(),
        requested,
        "Search result",
        "light",
        ready_selector="h1#citistat",
    )

    assert issues == [
        "Search result (light): loaded a new document instead of using Material instant navigation."
    ]
    page.locator.assert_not_called()


def test_instant_navigation_requires_old_content_replacement() -> None:
    """An already-visible target marker in the source DOM must not pass vacuously."""

    requested = "http://127.0.0.1:5208/programs/citistat/"
    page = MagicMock()
    page.url = requested
    page.evaluate.side_effect = [
        {
            "token": "transition-token",
            "sourceUrl": "http://127.0.0.1:5208/",
            "timeOrigin": 1234.5,
        },
        True,
    ]
    page.wait_for_function.side_effect = [
        None,
        RuntimeError("old article remained attached"),
    ]

    with pytest.raises(RuntimeError, match="old article remained attached"):
        navigate_to_instant_page(
            page,
            MagicMock(),
            requested,
            "Search result",
            "light",
            ready_selector="h1#citistat",
        )

    page.locator.assert_not_called()


def test_instant_navigation_propagates_a_missing_target_failure() -> None:
    """A stalled content swap must fail hard instead of accepting the old document."""

    page = MagicMock()
    page.url = "http://127.0.0.1:5208/programs/citistat/"
    page.evaluate.side_effect = [
        {
            "token": "transition-token",
            "sourceUrl": "http://127.0.0.1:5208/",
            "timeOrigin": 1234.5,
        },
        True,
    ]
    page.locator.return_value.first.wait_for.side_effect = RuntimeError(
        "target never became visible"
    )

    with pytest.raises(RuntimeError, match="target never became visible"):
        navigate_to_instant_page(
            page,
            MagicMock(),
            "http://127.0.0.1:5208/programs/citistat/",
            "Search result",
            "light",
            ready_selector="h1#citistat",
        )
