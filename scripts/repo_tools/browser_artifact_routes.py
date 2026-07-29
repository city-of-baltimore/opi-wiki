"""Serve one built MkDocs artifact at its canonical origin inside Playwright."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlsplit, urlunsplit

from scripts.repo_tools.site_urls import (
    HttpOrigin,
    normalize_base_url,
    validate_http_location,
)

if TYPE_CHECKING:
    from playwright.sync_api import BrowserContext, Route

_NOT_FOUND_BODY = b"Not Found\n"
_TEXT_CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".map": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".webmanifest": "application/manifest+json; charset=utf-8",
    ".xml": "application/xml; charset=utf-8",
}


def _content_type(path: Path) -> str:
    """Return a deterministic content type for one artifact."""

    override = _TEXT_CONTENT_TYPES.get(path.suffix.casefold())
    if override is not None:
        return override
    guessed_type, _encoding = mimetypes.guess_type(path.name, strict=False)
    return guessed_type or "application/octet-stream"


def _fulfill_not_found(route: Route, *, empty_body: bool = False) -> None:
    """Fulfill one rejected request without disclosing filesystem details."""

    route.fulfill(
        status=404,
        content_type="text/plain; charset=utf-8",
        body=b"" if empty_body else _NOT_FOUND_BODY,
    )


def _validated_request_path(url: str, expected_origin: HttpOrigin) -> str | None:
    """Return one decoded request path, ignoring only its query string."""

    try:
        parsed = urlsplit(url)
    except ValueError:
        return None
    if "#" in url:
        return None

    queryless_url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    try:
        origin, decoded_path = validate_http_location(
            queryless_url,
            "Browser artifact request URL",
            allow_empty_path=True,
        )
    except RuntimeError:
        return None
    if origin != expected_origin:
        return None

    return decoded_path


def _artifact_path(
    *,
    request_url: str,
    expected_origin: HttpOrigin,
    base_path: str,
    site_root: Path,
) -> Path | None:
    """Resolve one canonical request to a regular file inside the build root."""

    request_path = _validated_request_path(request_url, expected_origin)
    if request_path is None:
        return None

    if base_path == "/":
        relative_path = request_path.removeprefix("/")
    elif request_path.startswith(base_path):
        relative_path = request_path.removeprefix(base_path)
    else:
        return None

    if not relative_path or relative_path.endswith("/"):
        relative_path = f"{relative_path}index.html"

    try:
        candidate = site_root.joinpath(*relative_path.split("/")).resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not candidate.is_relative_to(site_root) or not candidate.is_file():
        return None
    return candidate


def install_canonical_artifact_route(
    context: BrowserContext,
    *,
    canonical_base_url: str,
    site_dir: Path,
) -> None:
    """Route a built site through one canonical HTTP(S) origin in Playwright.

    The installed catch-all never delegates to Chromium's network stack.
    Requests outside the exact canonical origin and deployment base, unsafe
    paths, unsupported methods, and missing artifacts receive a local 404.
    """

    try:
        site_root = site_dir.resolve(strict=True)
    except OSError as error:
        raise FileNotFoundError(f"Built site directory was not found: {site_dir}") from error
    if not site_root.is_dir():
        raise NotADirectoryError(f"Built site path is not a directory: {site_dir}")

    normalized_base_url = normalize_base_url(
        canonical_base_url,
        label="Canonical artifact base URL",
    )
    expected_origin, base_path = validate_http_location(
        normalized_base_url,
        "Canonical artifact base URL",
    )

    def fulfill_from_artifact(route: Route) -> None:
        """Fulfill one intercepted request from the immutable build artifact."""

        method = route.request.method.upper()
        if method not in {"GET", "HEAD"}:
            _fulfill_not_found(route)
            return

        artifact = _artifact_path(
            request_url=route.request.url,
            expected_origin=expected_origin,
            base_path=base_path,
            site_root=site_root,
        )
        if artifact is None:
            _fulfill_not_found(route, empty_body=method == "HEAD")
            return

        try:
            body = artifact.read_bytes()
        except OSError:
            _fulfill_not_found(route, empty_body=method == "HEAD")
            return
        route.fulfill(
            status=200,
            content_type=_content_type(artifact),
            body=b"" if method == "HEAD" else body,
        )

    context.route("**/*", fulfill_from_artifact)
