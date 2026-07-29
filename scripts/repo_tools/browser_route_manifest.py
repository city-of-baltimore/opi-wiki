"""Canonical route manifests for built sites and live browser previews."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from posixpath import commonpath
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import HTTPRedirectHandler, build_opener

from scripts.repo_tools.built_links import load_sitemap_locations, parse_sitemap_locations
from scripts.repo_tools.site_urls import (
    HttpOrigin,
    normalize_base_url,
    normalize_page_url,
    validate_http_location,
)

_MAX_SITEMAP_BYTES = 5 * 1024 * 1024
_MAX_CANONICAL_ROUTES = 500


@dataclass(frozen=True)
class CanonicalRouteManifest:
    """One canonical deployment identity and its immutable browser routes."""

    canonical_base_url: str
    routes: tuple[str, ...]


class _NoRedirectHandler(HTTPRedirectHandler):
    """Reject redirects before a preview sitemap request can follow them."""

    def redirect_request(
        self,
        req: Any,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        """Refuse every redirect from the explicitly selected sitemap URL."""

        del req, fp, code, msg, headers, newurl
        return None


def _validated_sitemap_location(location: str, index: int) -> tuple[HttpOrigin, str]:
    """Return one validated sitemap origin and decoded absolute path."""

    return validate_http_location(location, f"Built sitemap <loc> entry {index}")


def _canonical_route_manifest(
    locations: list[str],
    *,
    source: str,
    expected_origin: HttpOrigin | None = None,
    expected_base_path: str | None = None,
) -> CanonicalRouteManifest | None:
    """Return one validated canonical deployment manifest."""

    if not locations:
        return None
    if len(locations) > _MAX_CANONICAL_ROUTES:
        raise RuntimeError(
            f"Sitemap contains {len(locations)} URL locations, exceeding the "
            f"{_MAX_CANONICAL_ROUTES}-route browser assurance limit: {source}"
        )
    validated_locations = tuple(
        _validated_sitemap_location(location, index)
        for index, location in enumerate(locations, start=1)
    )
    sitemap_origin = validated_locations[0][0]
    for index, ((origin, _path), location) in enumerate(
        zip(validated_locations, locations, strict=True),
        start=1,
    ):
        if origin != sitemap_origin:
            raise RuntimeError(
                f"Built sitemap <loc> entry {index} origin does not match entry 1: {location!r}"
            )
    if expected_origin is not None and sitemap_origin != expected_origin:
        raise RuntimeError(
            f"Sitemap canonical origin does not match the selected preview origin: {source}"
        )

    shared_path = commonpath(path for _origin, path in validated_locations)
    base_path = "/" if shared_path == "/" else "/" + shared_path.strip("/") + "/"
    if base_path not in {path for _origin, path in validated_locations}:
        raise RuntimeError(
            "Built sitemap does not contain a deployment-root <loc> for common "
            f"base path {base_path!r}"
        )
    if expected_base_path is not None and base_path != expected_base_path:
        raise RuntimeError(
            f"Sitemap deployment base path is {base_path!r}, expected selected "
            f"preview base path {expected_base_path!r}: {source}"
        )

    root_location = next(
        location
        for (_origin, path), location in zip(
            validated_locations,
            locations,
            strict=True,
        )
        if path == base_path
    )
    routes: set[str] = set()
    for index, ((_origin, path), location) in enumerate(
        zip(validated_locations, locations, strict=True),
        start=1,
    ):
        if not path.startswith(base_path):
            raise RuntimeError(
                f"Built sitemap <loc> entry {index} is outside deployment base path "
                f"{base_path!r}: {location!r}"
            )

        route = "/" + path.removeprefix(base_path)
        if not route.endswith("/"):
            if not Path(route).suffix:
                route = route.rstrip("/") + "/"
            elif Path(route).suffix.casefold() != ".html":
                raise RuntimeError(
                    f"Built sitemap <loc> entry {index} is not a scannable HTML route: {location!r}"
                )
        if route in routes:
            raise RuntimeError(
                f"Built sitemap <loc> entry {index} duplicates canonical route {route!r}: "
                f"{location!r}"
            )
        routes.add(route)
    return CanonicalRouteManifest(
        canonical_base_url=root_location,
        routes=tuple(sorted(routes, key=lambda route: (route != "/", route))),
    )


def canonical_route_manifest(site_dir: Path) -> CanonicalRouteManifest:
    """Load one canonical deployment manifest from the built artifact."""

    sitemap = site_dir / "sitemap.xml"
    manifest = _canonical_route_manifest(
        load_sitemap_locations(site_dir),
        source=str(sitemap),
    )
    if manifest is None:
        raise RuntimeError(f"Sitemap contains no canonical routes: {sitemap}")
    return manifest


def canonical_route_paths(site_dir: Path) -> list[str]:
    """Return every validated deployment-relative route from the built sitemap."""

    sitemap = site_dir / "sitemap.xml"
    manifest = _canonical_route_manifest(
        load_sitemap_locations(site_dir),
        source=str(sitemap),
    )
    return [] if manifest is None else list(manifest.routes)


def canonical_route_manifest_from_preview(base_url: str) -> CanonicalRouteManifest:
    """Load one canonical deployment manifest from the selected live preview."""

    normalized_base_url = normalize_base_url(base_url)
    expected_origin, decoded_base_path = validate_http_location(
        normalized_base_url,
        "Browser preview base URL",
    )
    expected_base_path = "/" if decoded_base_path == "/" else decoded_base_path.rstrip("/") + "/"

    sitemap_url = urljoin(normalized_base_url, "sitemap.xml")
    opener = build_opener(_NoRedirectHandler())
    try:
        with opener.open(sitemap_url, timeout=5) as response:
            status = response.status
            final_url = response.geturl()
            sitemap_bytes = response.read(_MAX_SITEMAP_BYTES + 1)
    except HTTPError as error:
        status = error.code
        location = error.headers.get("Location")
        error.close()
        if 300 <= status < 400:
            destination = f" to {location}" if location else ""
            raise RuntimeError(
                f"Preview sitemap returned redirect HTTP {status}{destination}; "
                f"redirects are not allowed: {sitemap_url}"
            ) from error
        raise RuntimeError(
            f"Preview sitemap returned HTTP {status}, expected 200: {sitemap_url}"
        ) from error
    except OSError as error:
        raise RuntimeError(f"Unable to read preview sitemap: {sitemap_url}") from error

    if status != 200:
        raise RuntimeError(f"Preview sitemap returned HTTP {status}, expected 200: {sitemap_url}")
    if normalize_page_url(final_url) != normalize_page_url(sitemap_url):
        raise RuntimeError(
            f"Preview sitemap ended at {final_url}, expected canonical URL {sitemap_url}"
        )
    if len(sitemap_bytes) > _MAX_SITEMAP_BYTES:
        raise RuntimeError(f"Preview sitemap exceeds {_MAX_SITEMAP_BYTES} bytes: {sitemap_url}")
    try:
        sitemap_text = sitemap_bytes.decode("utf-8", errors="strict")
    except UnicodeError as error:
        raise RuntimeError(f"Preview sitemap is not valid UTF-8: {sitemap_url}") from error

    locations = parse_sitemap_locations(sitemap_text, source=sitemap_url)
    manifest = _canonical_route_manifest(
        locations,
        source=sitemap_url,
        expected_origin=expected_origin,
        expected_base_path=expected_base_path,
    )
    if manifest is None:
        raise RuntimeError(f"Sitemap contains no canonical routes: {sitemap_url}")
    return manifest


def canonical_route_paths_from_preview(base_url: str) -> list[str]:
    """Return canonical routes from the selected preview's own sitemap."""

    return list(canonical_route_manifest_from_preview(base_url).routes)
