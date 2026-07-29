"""Tests for canonical browser routes and local-site serving."""

from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen

import pytest
from scripts.repo_tools.browser_routes import (
    browser_route_url,
    canonical_route_paths,
    check_page_load,
    local_site_server,
    normalize_base_url,
    normalize_page_url,
)


class _Response:
    """Minimal Playwright response stand-in for page-load tests."""

    def __init__(self, status: int) -> None:
        self.status = status


class _Page:
    """Minimal Playwright page stand-in for final-URL tests."""

    def __init__(self, url: str) -> None:
        self.url = url


def _write_sitemap(site_dir: Path, locations: tuple[str, ...]) -> None:
    """Write one structurally valid sitemap with the supplied locations."""

    site_dir.mkdir(parents=True, exist_ok=True)
    entries = "".join(f"<url><loc>{location}</loc></url>" for location in locations)
    (site_dir / "sitemap.xml").write_text(
        f"<urlset>{entries}</urlset>",
        encoding="utf-8",
    )


def test_normalize_base_url_enforces_trailing_slash() -> None:
    """Base URLs should normalize so joined paths stay stable."""

    assert normalize_base_url("http://127.0.0.1:8000") == "http://127.0.0.1:8000/"
    assert normalize_base_url("http://127.0.0.1:8000/") == "http://127.0.0.1:8000/"


def test_normalize_page_url_ignores_fragments_but_preserves_queries() -> None:
    """Final-URL checks should ignore fragments without hiding query redirects."""

    assert normalize_page_url("HTTPS://EXAMPLE.ORG/docs#section") == "https://example.org/docs/"
    assert normalize_page_url("https://example.org/docs/?view=all#top") == (
        "https://example.org/docs/?view=all"
    )


def test_canonical_route_paths_are_derived_from_the_sitemap(
    tmp_path: Path,
) -> None:
    """The route crawl should use canonical sitemap URLs and strip the deploy base."""

    _write_sitemap(
        tmp_path,
        (
            "https://example.test/opi-wiki/",
            "https://example.test/opi-wiki/resources/",
            "https://example.test/opi-wiki/reference.html",
        ),
    )

    assert canonical_route_paths(tmp_path) == ["/", "/reference.html", "/resources/"]


def test_canonical_route_paths_accepts_the_deployment_root_in_any_order(
    tmp_path: Path,
) -> None:
    """Sitemap ordering must not become an undocumented coverage contract."""

    _write_sitemap(
        tmp_path,
        (
            "https://example.test/opi-wiki/resources/",
            "https://example.test/opi-wiki/",
            "https://example.test/opi-wiki/about-us/",
        ),
    )

    assert canonical_route_paths(tmp_path) == ["/", "/about-us/", "/resources/"]


@pytest.mark.parametrize(
    ("invalid_location", "expected_error"),
    (
        ("relative-hidden/", r"absolute HTTP\(S\) URL"),
        ("ftp://example.test/opi-wiki/hidden/", r"absolute HTTP\(S\) URL"),
        (
            "https://foreign.test/opi-wiki/hidden/",
            "origin does not match entry 1",
        ),
        (
            "https://example.test/outside/hidden/",
            r"does not contain a deployment-root <loc>",
        ),
        (
            "https://example.test/opi-wiki/hidden/?preview=true",
            "must not contain a query or fragment",
        ),
        (
            "https://example.test/opi-wiki/hidden/#preview",
            "must not contain a query or fragment",
        ),
        (
            "https://example.test/opi-wiki/%2e%2e/hidden/",
            "unsafe dot segment",
        ),
        (
            "https://example.test/opi-wiki/hidden%ZZ/",
            "contains an invalid URL path",
        ),
        (
            "https://example.test/opi-wiki//hidden/",
            "contains an empty path segment",
        ),
        (
            "https://example.test/opi-wiki/hidden.pdf",
            "not a scannable HTML route",
        ),
    ),
)
def test_canonical_route_paths_rejects_any_unscannable_location(
    tmp_path: Path,
    invalid_location: str,
    expected_error: str,
) -> None:
    """A corrupt middle entry must fail rather than silently shrink coverage."""

    _write_sitemap(
        tmp_path,
        (
            "https://example.test/opi-wiki/",
            invalid_location,
            "https://example.test/opi-wiki/resources/",
        ),
    )

    with pytest.raises(RuntimeError, match=expected_error):
        canonical_route_paths(tmp_path)


def test_canonical_route_paths_rejects_duplicate_normalized_routes(
    tmp_path: Path,
) -> None:
    """Two locations that normalize to one route make coverage ambiguous."""

    _write_sitemap(
        tmp_path,
        (
            "https://example.test/opi-wiki/",
            "https://example.test/opi-wiki/resources/",
            "https://example.test/opi-wiki/resources",
        ),
    )

    with pytest.raises(RuntimeError, match=r"duplicates canonical route '/resources/'"):
        canonical_route_paths(tmp_path)


@pytest.mark.parametrize(
    ("encoded_segment", "decoded_segment"),
    (
        ("%23", "#"),
        ("%3F", "?"),
        ("%25", "%"),
        ("%252F", "%2F"),
        ("%252e%252e", "%2e%2e"),
    ),
)
def test_canonical_routes_preserve_filesystem_identity_but_encode_browser_urls(
    tmp_path: Path,
    encoded_segment: str,
    decoded_segment: str,
) -> None:
    """Reserved and residual percent data must round-trip through separate seams."""

    _write_sitemap(
        tmp_path,
        (
            "https://example.test/opi-wiki/",
            f"https://example.test/opi-wiki/{encoded_segment}/",
        ),
    )

    assert canonical_route_paths(tmp_path) == ["/", f"/{decoded_segment}/"]
    assert (
        browser_route_url(
            "http://127.0.0.1:5208/opi-wiki/",
            f"/{decoded_segment}/",
        )
        == f"http://127.0.0.1:5208/opi-wiki/{encoded_segment}/"
    )


@pytest.mark.parametrize(
    "route",
    (
        "",
        "relative/",
        "//foreign.test/authority/",
        r"/mixed\separator/",
    ),
)
def test_browser_route_url_rejects_ambiguous_route_forms(route: str) -> None:
    """Only decoded absolute-path identities may reach browser navigation."""

    with pytest.raises(ValueError, match="absolute path"):
        browser_route_url("http://127.0.0.1:5208/opi-wiki/", route)


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


def test_local_site_server_serves_the_requested_directory(tmp_path: Path) -> None:
    """The browser orchestrator's local server should expose freshly built files."""

    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")

    with local_site_server(tmp_path) as base_url:
        with urlopen(base_url, timeout=2) as response:  # noqa: S310
            assert response.status == 200
            assert b"<h1>OPI</h1>" in response.read()
