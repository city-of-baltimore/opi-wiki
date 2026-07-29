"""Strict URL identity helpers shared by previews and browser assurance."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

type HttpOrigin = tuple[str, str, int]

_INVALID_PERCENT_ESCAPE = re.compile(r"%(?![0-9A-Fa-f]{2})")
_RESIDUAL_UNSAFE_ESCAPE = re.compile(
    r"%(?:25)*(?:2e|2f|5c)",
    flags=re.IGNORECASE,
)


def normalize_page_url(url: str) -> str:
    """Normalize a page URL for redirect-sensitive final-URL comparisons."""

    parsed = urlsplit(url)
    path = parsed.path or "/"
    if not Path(path).suffix:
        path = path.rstrip("/") + "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def validate_http_location(
    location: str,
    label: str,
    *,
    allow_empty_path: bool = False,
) -> tuple[HttpOrigin, str]:
    """Return one validated HTTP(S) origin and decoded absolute path."""

    if any(
        character.isspace() or ord(character) < 32 or ord(character) == 127
        for character in location
    ):
        raise RuntimeError(f"{label} contains raw whitespace or a control character: {location!r}")
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

    raw_path = parsed.path or ("/" if allow_empty_path else "")
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
    if _RESIDUAL_UNSAFE_ESCAPE.search(path):
        raise RuntimeError(
            f"{label} retains an encoded dot or path separator after decoding: {location!r}"
        )
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


def normalize_base_url(
    base_url: str,
    *,
    label: str = "Browser preview base URL",
) -> str:
    """Validate and normalize a canonical browser or preview base URL."""

    try:
        _origin, decoded_path = validate_http_location(
            base_url,
            label,
            allow_empty_path=True,
        )
    except RuntimeError as error:
        raise ValueError(str(error)) from error
    if Path(decoded_path.rstrip("/")).suffix:
        raise ValueError(f"{label} must identify a directory path: {base_url!r}")

    parsed = urlsplit(base_url)
    raw_path = parsed.path or "/"
    normalized_path = raw_path if raw_path.endswith("/") else f"{raw_path}/"
    return urlunsplit((parsed.scheme, parsed.netloc, normalized_path, "", ""))
