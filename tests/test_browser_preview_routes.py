"""Tests for canonical route discovery from an already-running preview."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock
from urllib.error import HTTPError

import pytest
import scripts.repo_tools.browser_route_manifest as browser_route_manifest
from scripts.repo_tools.browser_route_manifest import (
    CanonicalRouteManifest,
    _NoRedirectHandler,
    canonical_route_manifest,
    canonical_route_manifest_from_preview,
    canonical_route_paths,
    canonical_route_paths_from_preview,
)


def _write_sitemap(site_dir: Path, route_count: int) -> None:
    """Write one deployment-root location plus the requested unique pages."""

    locations = ["https://example.test/opi-wiki/"]
    locations.extend(
        f"https://example.test/opi-wiki/page-{index}/" for index in range(1, route_count)
    )
    entries = "".join(f"<url><loc>{location}</loc></url>" for location in locations)
    (site_dir / "sitemap.xml").write_text(
        f"<urlset>{entries}</urlset>",
        encoding="utf-8",
    )


def test_preview_routes_come_from_the_served_sitemap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A live audit should crawl the selected preview rather than stale disk output."""

    sitemap_url = "http://127.0.0.1:5208/opi-wiki/sitemap.xml"
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.geturl.return_value = sitemap_url
    response.read.return_value = (
        b"<urlset><url><loc>http://127.0.0.1:5208/opi-wiki/</loc></url>"
        b"<url><loc>http://127.0.0.1:5208/opi-wiki/resources/</loc></url></urlset>"
    )
    opener = MagicMock()
    opener.open.return_value = response
    build_opener = MagicMock(return_value=opener)
    monkeypatch.setattr(browser_route_manifest, "build_opener", build_opener)

    assert canonical_route_paths_from_preview("http://127.0.0.1:5208/opi-wiki") == [
        "/",
        "/resources/",
    ]
    build_opener.assert_called_once()
    opener.open.assert_called_once_with(sitemap_url, timeout=5)
    response.read.assert_called_once_with(5 * 1024 * 1024 + 1)


def test_preview_manifest_wires_the_no_redirect_handler(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Preview discovery must install redirect refusal before opening the sitemap."""

    opener = MagicMock()
    opener.open.side_effect = OSError("connection refused")
    build_opener = MagicMock(return_value=opener)
    monkeypatch.setattr(browser_route_manifest, "build_opener", build_opener)

    with pytest.raises(RuntimeError, match="Unable to read preview sitemap"):
        canonical_route_manifest_from_preview("http://127.0.0.1:5208/opi-wiki/")

    build_opener.assert_called_once()
    handlers = build_opener.call_args.args
    assert len(handlers) == 1
    assert isinstance(handlers[0], _NoRedirectHandler)


def test_preview_routes_reject_an_oversized_sitemap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A served manifest larger than the reviewed byte ceiling must fail closed."""

    sitemap_url = "http://127.0.0.1:5208/opi-wiki/sitemap.xml"
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.geturl.return_value = sitemap_url
    response.read.return_value = b"x" * (5 * 1024 * 1024 + 1)
    opener = MagicMock()
    opener.open.return_value = response
    monkeypatch.setattr(browser_route_manifest, "build_opener", lambda *_args: opener)

    with pytest.raises(RuntimeError, match=r"exceeds 5242880 bytes"):
        canonical_route_paths_from_preview("http://127.0.0.1:5208/opi-wiki/")

    opener.open.assert_called_once_with(sitemap_url, timeout=5)


def test_preview_routes_reject_a_sitemap_that_is_not_valid_utf8(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A served manifest with invalid UTF-8 must not reach XML parsing."""

    sitemap_url = "http://127.0.0.1:5208/opi-wiki/sitemap.xml"
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.geturl.return_value = sitemap_url
    response.read.return_value = b"\xff"
    opener = MagicMock()
    opener.open.return_value = response
    monkeypatch.setattr(browser_route_manifest, "build_opener", lambda *_args: opener)

    with pytest.raises(RuntimeError, match=r"Preview sitemap is not valid UTF-8"):
        canonical_route_paths_from_preview("http://127.0.0.1:5208/opi-wiki/")

    opener.open.assert_called_once_with(sitemap_url, timeout=5)


@pytest.mark.parametrize(
    "base_url",
    (
        "file:///tmp/site/",
        "http://user:secret@example.test/opi-wiki/",
        "http://example.test/opi-wiki/?preview=true",
        "http://example.test:invalid/opi-wiki/",
        "http://example.test/opi-wiki/../other/",
        "http://example.test/opi-wiki/%2Fprivate/",
        "http://example.test/opi-wiki//nested/",
        "http://example.test/opi-wiki/index.html",
        "http://example.test/opi-wiki\\nested/",
        " http://example.test/opi-wiki/",
        "http://example.test/opi-\twiki/",
        "http://example.test/opi-\nwiki/",
        "http://example.test/opi-\rwiki/",
        "http://example.test/opi-\x7fwiki/",
    ),
)
def test_preview_routes_reject_unsafe_or_ambiguous_base_urls(base_url: str) -> None:
    """Only one explicit canonical HTTP(S) preview may supply route authority."""

    with pytest.raises(ValueError, match="(?i)browser preview base URL"):
        canonical_route_paths_from_preview(base_url)


def test_preview_routes_reject_a_redirected_sitemap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A defensive final-URL check must reject a replaced sitemap response."""

    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.geturl.return_value = "http://foreign.test/sitemap.xml"
    response.read.return_value = (
        b"<urlset><url><loc>https://example.test/opi-wiki/</loc></url></urlset>"
    )
    opener = MagicMock()
    opener.open.return_value = response
    monkeypatch.setattr(browser_route_manifest, "build_opener", lambda *_args: opener)

    with pytest.raises(RuntimeError, match="expected canonical URL"):
        canonical_route_paths_from_preview("http://example.test/opi-wiki/")


def test_preview_routes_reject_a_mismatched_deployment_base(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A valid sitemap for another deploy path must not drive this preview."""

    sitemap_url = "http://127.0.0.1:5208/opi-wiki/sitemap.xml"
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.geturl.return_value = sitemap_url
    response.read.return_value = (
        b"<urlset><url><loc>http://127.0.0.1:5208/other/</loc></url>"
        b"<url><loc>http://127.0.0.1:5208/other/resources/</loc></url></urlset>"
    )
    opener = MagicMock()
    opener.open.return_value = response
    monkeypatch.setattr(browser_route_manifest, "build_opener", lambda *_args: opener)

    with pytest.raises(RuntimeError, match=r"base path is '/other/'.*'/opi-wiki/'"):
        canonical_route_paths_from_preview("http://127.0.0.1:5208/opi-wiki/")


def test_preview_routes_report_an_unreachable_sitemap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Transport failure should name the unavailable preview sitemap."""

    opener = MagicMock()
    opener.open.side_effect = OSError("connection refused")
    monkeypatch.setattr(browser_route_manifest, "build_opener", lambda *_args: opener)

    with pytest.raises(RuntimeError, match="Unable to read preview sitemap"):
        canonical_route_paths_from_preview("http://127.0.0.1:5208/opi-wiki/")


def test_preview_routes_reject_a_redirect_before_reading_its_destination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The selected preview must not redirect sitemap discovery elsewhere."""

    sitemap_url = "http://127.0.0.1:5208/opi-wiki/sitemap.xml"
    redirect = HTTPError(
        sitemap_url,
        302,
        "Found",
        {"Location": "http://destination.test/private"},
        None,
    )
    opener = MagicMock()
    opener.open.side_effect = redirect
    monkeypatch.setattr(browser_route_manifest, "build_opener", lambda *_args: opener)

    with pytest.raises(RuntimeError, match=r"redirect HTTP 302.*redirects are not allowed"):
        canonical_route_paths_from_preview("http://127.0.0.1:5208/opi-wiki/")


def test_preview_routes_report_a_non_redirect_http_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A non-success response should retain its exact HTTP status."""

    sitemap_url = "http://127.0.0.1:5208/opi-wiki/sitemap.xml"
    unavailable = HTTPError(sitemap_url, 503, "Unavailable", {}, None)
    opener = MagicMock()
    opener.open.side_effect = unavailable
    monkeypatch.setattr(browser_route_manifest, "build_opener", lambda *_args: opener)

    with pytest.raises(RuntimeError, match=r"returned HTTP 503, expected 200"):
        canonical_route_paths_from_preview("http://127.0.0.1:5208/opi-wiki/")


def test_preview_routes_reject_a_canonical_origin_other_than_the_selected_server(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A preview whose canonical origin drifted cannot prove instant navigation."""

    sitemap_url = "http://127.0.0.1:5208/opi-wiki/sitemap.xml"
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.geturl.return_value = sitemap_url
    response.read.return_value = (
        b"<urlset><url><loc>http://127.0.0.1:8000/opi-wiki/</loc></url>"
        b"<url><loc>http://127.0.0.1:8000/opi-wiki/resources/</loc></url></urlset>"
    )
    opener = MagicMock()
    opener.open.return_value = response
    monkeypatch.setattr(browser_route_manifest, "build_opener", lambda *_args: opener)

    with pytest.raises(RuntimeError, match="canonical origin.*selected preview origin"):
        canonical_route_paths_from_preview("http://127.0.0.1:5208/opi-wiki/")


def test_canonical_manifest_preserves_the_exact_root_location_from_one_parse(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Static routing must use the sitemap's exact root URL, regardless of order."""

    load_locations = MagicMock(
        return_value=[
            "https://example.test/opi-wiki/resources/",
            "https://example.test:443/opi-wiki/",
            "https://example.test/opi-wiki/about-us/",
        ]
    )
    monkeypatch.setattr(browser_route_manifest, "load_sitemap_locations", load_locations)

    assert canonical_route_manifest(tmp_path) == CanonicalRouteManifest(
        canonical_base_url="https://example.test:443/opi-wiki/",
        routes=("/", "/about-us/", "/resources/"),
    )
    load_locations.assert_called_once_with(tmp_path)


def test_canonical_route_limit_accepts_the_reviewed_boundary(tmp_path: Path) -> None:
    """The browser matrix may cover up to its explicit bounded route ceiling."""

    _write_sitemap(tmp_path, 500)

    assert len(canonical_route_paths(tmp_path)) == 500


def test_canonical_route_limit_rejects_an_unbounded_browser_matrix(
    tmp_path: Path,
) -> None:
    """One small manifest must not expand into an hours-long browser run."""

    _write_sitemap(tmp_path, 501)

    with pytest.raises(RuntimeError, match=r"501 URL locations.*500-route"):
        canonical_route_paths(tmp_path)
