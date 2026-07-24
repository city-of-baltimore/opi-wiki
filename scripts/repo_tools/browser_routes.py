"""Route and local-server helpers for browser smoke checks."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from scripts.repo_tools.built_links import discover_site_base_path, load_sitemap_locations


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


def canonical_route_paths(site_dir: Path) -> list[str]:
    """Return deployment-relative canonical routes from the built sitemap."""

    base_path = discover_site_base_path(site_dir)
    routes: set[str] = set()
    for location in load_sitemap_locations(site_dir):
        path = urlsplit(location).path
        if base_path != "/":
            if not path.startswith(base_path):
                continue
            path = path[len(base_path) :]
        route = "/" + path.lstrip("/")
        if not Path(route).suffix:
            route = route.rstrip("/") + "/"
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
