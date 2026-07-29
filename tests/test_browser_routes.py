"""Tests for canonical browser routes and local-site serving."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.browser_route_manifest import (
    canonical_route_paths,
)
from scripts.repo_tools.browser_routes import (
    BrowserTarget,
    browser_route_url,
    browser_target_owns_live_reload_url,
    browser_target_owns_url,
)


def _write_sitemap(site_dir: Path, locations: tuple[str, ...]) -> None:
    """Write one structurally valid sitemap with the supplied locations."""

    site_dir.mkdir(parents=True, exist_ok=True)
    entries = "".join(f"<url><loc>{location}</loc></url>" for location in locations)
    (site_dir / "sitemap.xml").write_text(
        f"<urlset>{entries}</urlset>",
        encoding="utf-8",
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
            "https://example.test/opi-wiki/%252Fhidden/",
            "retains an encoded dot or path separator after decoding",
        ),
        (
            "https://example.test/opi-wiki/%252e%252e/hidden/",
            "retains an encoded dot or path separator after decoding",
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
            "https://example.test/opi-\twiki/hidden/",
            "raw whitespace or a control character",
        ),
        (
            "https://example.test/opi-\x7fwiki/hidden/",
            "raw whitespace or a control character",
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
        ("%2523", "%23"),
    ),
)
def test_canonical_routes_preserve_filesystem_identity_but_encode_browser_urls(
    tmp_path: Path,
    encoded_segment: str,
    decoded_segment: str,
) -> None:
    """Safe reserved percent data must round-trip through separate seams."""

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


@pytest.mark.parametrize(
    ("route", "expected_error"),
    (
        ("/../outside/", "unsafe dot segment"),
        ("/section/./page/", "unsafe dot segment"),
        ("/section//page/", "empty path segment"),
        ("/section/\tpage/", "whitespace or control"),
        ("/section/\x00page/", "whitespace or control"),
        ("/%2Foutside/", "encoded dot or path separator"),
        ("/%252e%252e/outside/", "encoded dot or path separator"),
        ("/section/%5Coutside/", "encoded dot or path separator"),
    ),
)
def test_browser_route_url_rejects_unsafe_decoded_path_identity(
    route: str,
    expected_error: str,
) -> None:
    """A decoded route must remain contained after browser URL construction."""

    with pytest.raises(ValueError, match=expected_error):
        browser_route_url("http://127.0.0.1:5208/opi-wiki/", route)


def test_browser_route_url_normalizes_the_base_without_losing_its_deploy_path() -> None:
    """A caller's missing trailing slash must not turn a route into an origin-root path."""

    assert (
        browser_route_url(
            "http://127.0.0.1:5208/opi-wiki",
            "/resources/",
        )
        == "http://127.0.0.1:5208/opi-wiki/resources/"
    )


@pytest.mark.parametrize(
    ("url", "owned"),
    (
        ("https://city.example/opi-wiki/", True),
        ("https://city.example/opi-wiki", True),
        ("https://city.example/opi-wiki/assets/app.js?v=1", True),
        ("https://city.example/opi-wiki-archive/", False),
        ("https://city.example/outside/", False),
        ("https://fonts.example/opi-wiki/", False),
        ("http://city.example/opi-wiki/", False),
        ("malformed", False),
    ),
)
def test_browser_target_owns_only_its_canonical_url_space(
    url: str,
    owned: bool,
) -> None:
    """Runtime failures should be attributed only to the selected product."""

    target = BrowserTarget("https://city.example/opi-wiki/", ("/",))

    assert browser_target_owns_url(target, url) is owned


@pytest.mark.parametrize(
    ("url", "live", "owned"),
    (
        ("http://127.0.0.1:5208/livereload/123/456", True, True),
        ("http://127.0.0.1:5208/livereload/not-numeric/456", True, False),
        ("http://127.0.0.1:5208/livereload/123/456?retry=1", True, False),
        ("http://foreign.test/livereload/123/456", True, False),
        ("https://127.0.0.1:5208/livereload/123/456", True, False),
        ("http://127.0.0.1:5208/livereload/123/456", False, False),
    ),
)
def test_browser_target_owns_only_its_exact_live_reload_poll(
    url: str,
    live: bool,
    owned: bool,
    tmp_path: Path,
) -> None:
    """Only live targets may suppress their exact same-origin numeric poll."""

    target = BrowserTarget(
        "http://127.0.0.1:5208/opi-wiki/",
        ("/",),
        None if live else tmp_path,
    )

    assert browser_target_owns_live_reload_url(target, url) is owned
