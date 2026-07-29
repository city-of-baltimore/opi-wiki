"""Route and local-server helpers for browser smoke checks."""

from __future__ import annotations

import re
from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from posixpath import commonpath
from threading import Thread
from typing import Any
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit

from scripts.repo_tools.built_links import load_sitemap_locations

type _Origin = tuple[str, str, int]

_INVALID_PERCENT_ESCAPE = re.compile(r"%(?![0-9A-Fa-f]{2})")


class _QuietStaticSiteHandler(SimpleHTTPRequestHandler):
    """Static-site request handler without per-request console logging."""

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default request logging for local smoke-test servers."""


def normalize_base_url(base_url: str) -> str:
    """Normalize a base URL so downstream joins are stable."""

    return base_url.rstrip("/") + "/"


def normalize_page_url(url: str) -> str:
    """Normalize a page URL for redirect-sensitive final-URL comparisons."""

    parsed = urlsplit(url)
    path = parsed.path or "/"
    if not Path(path).suffix:
        path = path.rstrip("/") + "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def browser_route_url(base_url: str, route: str) -> str:
    """Join one decoded absolute route without changing its URL identity."""

    if not route.startswith("/") or route.startswith("//") or "\\" in route:
        raise ValueError(
            "browser route must be an absolute path with one leading slash and no backslashes"
        )
    return urljoin(base_url, quote(route[1:], safe="/"))


def _validated_sitemap_location(location: str, index: int) -> tuple[_Origin, str]:
    """Return one validated origin and decoded absolute path."""

    label = f"Built sitemap <loc> entry {index}"
    try:
        parsed = urlsplit(location)
    except ValueError as error:
        raise RuntimeError(f"{label} is malformed: {location!r}: {error}") from error

    scheme = parsed.scheme.casefold()
    if scheme not in {"http", "https"} or not parsed.netloc:
        raise RuntimeError(f"{label} must be an absolute HTTP(S) URL: {location!r}")
    if parsed.username is not None or parsed.password is not None:
        raise RuntimeError(f"{label} must not contain credentials: {location!r}")
    try:
        hostname = parsed.hostname
        explicit_port = parsed.port
    except ValueError as error:
        raise RuntimeError(f"{label} has an invalid origin: {location!r}: {error}") from error
    if hostname is None:
        raise RuntimeError(f"{label} has no hostname: {location!r}")
    if parsed.query or parsed.fragment or "?" in location or "#" in location:
        raise RuntimeError(f"{label} must not contain a query or fragment: {location!r}")

    raw_path = parsed.path
    if not raw_path.startswith("/") or raw_path.startswith("//"):
        raise RuntimeError(f"{label} must contain one absolute URL path: {location!r}")
    if (
        "\\" in raw_path
        or any(character.isspace() for character in raw_path)
        or _INVALID_PERCENT_ESCAPE.search(raw_path)
    ):
        raise RuntimeError(f"{label} contains an invalid URL path: {location!r}")
    try:
        path = unquote(raw_path, encoding="utf-8", errors="strict")
    except UnicodeError as error:
        raise RuntimeError(f"{label} contains an invalid encoded path: {location!r}") from error
    if path.count("/") != raw_path.count("/") or "\\" in path:
        raise RuntimeError(f"{label} must not encode path separators: {location!r}")
    if any(ord(character) < 32 or ord(character) == 127 for character in path):
        raise RuntimeError(f"{label} contains a control character in its path: {location!r}")

    if "//" in path[1:]:
        raise RuntimeError(f"{label} contains an empty path segment: {location!r}")
    path_parts = path.strip("/").split("/") if path != "/" else []
    if any(part in {".", ".."} for part in path_parts):
        raise RuntimeError(f"{label} contains an unsafe dot segment: {location!r}")

    default_port = 443 if scheme == "https" else 80
    effective_port = explicit_port if explicit_port is not None else default_port
    return (scheme, hostname.casefold(), effective_port), path


def canonical_route_paths(site_dir: Path) -> list[str]:
    """Return every validated deployment-relative route from the built sitemap."""

    locations = load_sitemap_locations(site_dir)
    if not locations:
        return []
    validated_locations = tuple(
        _validated_sitemap_location(location, index)
        for index, location in enumerate(locations, start=1)
    )
    expected_origin = validated_locations[0][0]
    for index, ((origin, _path), location) in enumerate(
        zip(validated_locations, locations, strict=True),
        start=1,
    ):
        if origin != expected_origin:
            raise RuntimeError(
                f"Built sitemap <loc> entry {index} origin does not match entry 1: {location!r}"
            )

    shared_path = commonpath(path for _origin, path in validated_locations)
    base_path = "/" if shared_path == "/" else "/" + shared_path.strip("/") + "/"
    if base_path not in {path for _origin, path in validated_locations}:
        raise RuntimeError(
            "Built sitemap does not contain a deployment-root <loc> for common "
            f"base path {base_path!r}"
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
    return sorted(routes, key=lambda route: (route != "/", route))


@contextmanager
def local_site_server(site_dir: Path) -> Iterator[str]:
    """Serve a built static site from a temporary local HTTP server."""

    handler = partial(_QuietStaticSiteHandler, directory=str(site_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    try:
        thread.start()
        host_raw, port = server.server_address[0], server.server_address[1]
        host = host_raw.decode() if isinstance(host_raw, bytes) else host_raw
        yield f"http://{host}:{port}/"
    finally:
        if thread.is_alive():
            server.shutdown()
            thread.join(timeout=5)
        server.server_close()


def check_page_load(
    page: Any,
    response: Any,
    requested_url: str,
    label: str,
    scheme: str,
) -> list[str]:
    """Validate the HTTP status and final URL for one canonical page load."""

    if response is None:
        return [f"{label} ({scheme}): navigation returned no HTTP response."]

    issues: list[str] = []
    if response.status != 200:
        issues.append(f"{label} ({scheme}): returned HTTP {response.status}, expected 200.")

    final_url = str(page.url)
    if normalize_page_url(final_url) != normalize_page_url(requested_url):
        issues.append(
            f"{label} ({scheme}): ended at {final_url}, expected canonical URL {requested_url}."
        )
    return issues
