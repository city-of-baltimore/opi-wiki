"""Context-wide browser resource assurance for smoke and accessibility checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin, urlsplit, urlunsplit

from scripts.repo_tools.browser_routes import (
    BrowserTarget,
    browser_target_owns_live_reload_url,
    browser_target_owns_url,
)
from scripts.repo_tools.site_urls import validate_http_location

_BROWSER_CANCELLATION_FAILURE = "net::ERR_ABORTED"
_ALLOWED_EXTERNAL_FONT_ORIGINS = frozenset(
    {
        ("https", "fonts.googleapis.com", 443),
        ("https", "fonts.gstatic.com", 443),
        ("https", "p.typekit.net", 443),
        ("https", "use.typekit.net", 443),
    }
)
_ALLOWED_EXTERNAL_FONT_RESOURCE_TYPES = frozenset({"font", "image", "stylesheet"})


def _is_allowed_external_font_request(request: Any) -> bool:
    """Return whether one request is an explicitly allowed font dependency."""

    if request.resource_type not in _ALLOWED_EXTERNAL_FONT_RESOURCE_TYPES:
        return False
    try:
        parsed = urlsplit(request.url)
        queryless_url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
        origin, _path = validate_http_location(
            queryless_url,
            "External font request URL",
            allow_empty_path=True,
        )
    except (RuntimeError, ValueError):
        return False
    return origin in _ALLOWED_EXTERNAL_FONT_ORIGINS


def _blocking_resource_scope(target: BrowserTarget, request: Any) -> str | None:
    """Return the blocking ownership label for one browser request."""

    if browser_target_owns_url(target, request.url):
        return "target"
    if _is_allowed_external_font_request(request):
        return None
    return "unexpected external"


def _is_expected_search_index_cancellation(
    target: BrowserTarget,
    request: Any,
    failure: str,
) -> bool:
    """Return whether navigation cancelled the exact target search-index fetch."""

    expected_url = urljoin(target.base_url, "search/search_index.json")
    return (
        failure == _BROWSER_CANCELLATION_FAILURE
        and request.resource_type == "fetch"
        and request.url == expected_url
        and browser_target_owns_url(target, request.url)
    )


def _is_expected_live_reload_cancellation(
    target: BrowserTarget,
    request: Any,
    failure: str,
) -> bool:
    """Return whether the audit cancelled its exact live-preview reload XHR."""

    return (
        target.artifact_dir is None
        and failure == _BROWSER_CANCELLATION_FAILURE
        and request.resource_type == "xhr"
        and browser_target_owns_live_reload_url(target, request.url)
    )


@dataclass
class BrowserResourceObserver:
    """Collect blocking resource responses and transport failures for one context."""

    target: BrowserTarget
    issues: list[str]
    scope: str

    def attach(self, context: Any) -> None:
        """Attach response and failure listeners to an entire browser context."""

        context.on("response", self._record_response)
        context.on("requestfailed", self._record_failed_request)

    def set_scope(self, scope: str) -> None:
        """Set the reader-facing operation label for subsequent resource events."""

        self.scope = scope

    def _record_response(self, response: Any) -> None:
        """Record target HTTP failures and every unexpected external response."""

        request_scope = _blocking_resource_scope(self.target, response.request)
        if request_scope is None:
            return
        if request_scope == "target" and response.status < 400:
            return
        self.issues.append(
            f"{self.scope}: {request_scope} resource "
            f"{response.url} returned HTTP {response.status}."
        )

    def _record_failed_request(self, request: Any) -> None:
        """Record blocking request failures except two exact browser cancellations."""

        request_scope = _blocking_resource_scope(self.target, request)
        if request_scope is None:
            return
        failure = request.failure or "unknown transport failure"
        if _is_expected_search_index_cancellation(
            self.target,
            request,
            failure,
        ) or _is_expected_live_reload_cancellation(self.target, request, failure):
            return
        self.issues.append(
            f"{self.scope}: {request_scope} resource {request.url} failed: {failure}."
        )
