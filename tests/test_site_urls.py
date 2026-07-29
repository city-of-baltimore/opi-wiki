"""Tests for strict shared site URL identity."""

from __future__ import annotations

import pytest
from scripts.repo_tools.site_urls import (
    normalize_base_url,
    normalize_page_url,
    validate_http_location,
)


def test_http_location_returns_canonical_origin_and_decoded_path() -> None:
    """Validated locations should expose stable origin and path identities."""

    assert validate_http_location(
        "HTTPS://Example.TEST/opi-wiki/%23/",
        "Test URL",
    ) == (("https", "example.test", 443), "/opi-wiki/#/")


@pytest.mark.parametrize(
    "location",
    (
        "relative/",
        "ftp://example.test/opi-wiki/",
        "http://user:secret@example.test/opi-wiki/",
        "http://example.test/opi-\twiki/",
        "http://example.test/opi-wiki/%2Fprivate/",
    ),
)
def test_http_location_rejects_ambiguous_or_unsafe_identity(location: str) -> None:
    """Invalid origins and path mutations must fail rather than normalize silently."""

    with pytest.raises(RuntimeError, match="Test URL"):
        validate_http_location(location, "Test URL")


@pytest.mark.parametrize(
    "location",
    (
        "https://example.test/opi-wiki/%252Fprivate/",
        "https://example.test/opi-wiki/%252e%252e/private/",
    ),
)
def test_http_location_rejects_residual_encoded_path_syntax(location: str) -> None:
    """A second decode must never reveal a separator or dot traversal segment."""

    with pytest.raises(
        RuntimeError,
        match="retains an encoded dot or path separator after decoding",
    ):
        validate_http_location(location, "Test URL")


def test_normalize_base_url_enforces_a_directory_trailing_slash() -> None:
    """A valid base URL should normalize once for stable downstream joins."""

    assert normalize_base_url("http://127.0.0.1:5208/opi-wiki") == (
        "http://127.0.0.1:5208/opi-wiki/"
    )


def test_normalize_base_url_rejects_a_file_target() -> None:
    """A page URL must not masquerade as a browser preview base."""

    with pytest.raises(ValueError, match="must identify a directory path"):
        normalize_base_url("http://127.0.0.1:5208/opi-wiki/index.html")


def test_normalize_page_url_ignores_fragments_but_preserves_queries() -> None:
    """Final-URL checks should ignore fragments without hiding query redirects."""

    assert normalize_page_url("HTTPS://EXAMPLE.ORG/docs#section") == ("https://example.org/docs/")
    assert normalize_page_url("https://example.org/docs/?view=all#top") == (
        "https://example.org/docs/?view=all"
    )


def test_normalize_page_url_rejects_a_malformed_origin() -> None:
    """Malformed URL syntax should fail instead of producing a comparison identity."""

    with pytest.raises(ValueError):
        normalize_page_url("http://[invalid/")
