"""Keep an explicit MkDocs site URL authoritative during local serving."""

from __future__ import annotations

import os
from ipaddress import ip_address

from mkdocs.config.defaults import MkDocsConfig

from scripts.repo_tools.site_urls import normalize_base_url, validate_http_location

_SITE_URL_ENVIRONMENT_VARIABLE = "OPI_SITE_URL"


def _normalized_path(path: str) -> str:
    """Return one decoded absolute directory path with a trailing slash."""

    return "/" if path == "/" else path.rstrip("/") + "/"


def _is_loopback_host(hostname: str) -> bool:
    """Return whether a hostname is explicitly local-only."""

    if hostname == "localhost":
        return True
    try:
        return ip_address(hostname).is_loopback
    except ValueError:
        return False


def on_config(config: MkDocsConfig) -> MkDocsConfig:
    """Restore a validated external site URL after ``mkdocs serve`` rewrites it."""

    requested_url = os.environ.get(_SITE_URL_ENVIRONMENT_VARIABLE)
    if requested_url is None:
        return config

    normalized_url = normalize_base_url(
        requested_url,
        label=_SITE_URL_ENVIRONMENT_VARIABLE,
    )
    requested_origin, requested_path = validate_http_location(
        normalized_url,
        _SITE_URL_ENVIRONMENT_VARIABLE,
    )
    scheme, hostname, _port = requested_origin
    if scheme == "http" and not _is_loopback_host(hostname):
        raise ValueError(
            f"{_SITE_URL_ENVIRONMENT_VARIABLE} may use plain HTTP only for a "
            f"loopback host: {requested_url!r}"
        )

    runtime_site_url = str(config.site_url or "")
    try:
        _runtime_origin, runtime_path = validate_http_location(
            runtime_site_url,
            "MkDocs runtime site_url",
            allow_empty_path=True,
        )
    except RuntimeError as error:
        raise ValueError(str(error)) from error
    if _normalized_path(requested_path) != _normalized_path(runtime_path):
        raise ValueError(
            f"{_SITE_URL_ENVIRONMENT_VARIABLE} path "
            f"{_normalized_path(requested_path)!r} must match the MkDocs serve "
            f"path {_normalized_path(runtime_path)!r}"
        )

    config.site_url = normalized_url
    return config
