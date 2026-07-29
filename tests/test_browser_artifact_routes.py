"""Tests for canonical-origin Playwright artifact routing."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import pytest
from playwright.sync_api import BrowserContext, Route
from scripts.repo_tools.browser_artifact_routes import (
    install_canonical_artifact_route,
)


@dataclass(frozen=True)
class _FakeRequest:
    """One intercepted browser request."""

    url: str
    method: str = "GET"


class _FakeRoute:
    """Capture one Playwright route fulfillment."""

    def __init__(self, request: _FakeRequest) -> None:
        """Initialize one unresolved route."""

        self.request = request
        self.fulfillment: dict[str, Any] | None = None

    def fulfill(self, **kwargs: Any) -> None:
        """Record the only allowed terminal route operation."""

        assert self.fulfillment is None
        self.fulfillment = kwargs


class _FakeContext:
    """Capture and invoke one context-wide Playwright route."""

    def __init__(self) -> None:
        """Initialize an empty route registry."""

        self.pattern: str | None = None
        self.handler: Callable[[Route], Any] | None = None

    def route(self, pattern: str, handler: Callable[[Route], Any]) -> None:
        """Register the canonical artifact handler."""

        self.pattern = pattern
        self.handler = handler

    def request(self, url: str, *, method: str = "GET") -> dict[str, Any]:
        """Send one fake request through the installed handler."""

        assert self.handler is not None
        route = _FakeRoute(_FakeRequest(url=url, method=method))
        self.handler(cast(Route, route))
        assert route.fulfillment is not None
        return route.fulfillment


def _install(site_dir: Path) -> _FakeContext:
    """Install the router against the production-shaped canonical base."""

    context = _FakeContext()
    install_canonical_artifact_route(
        cast(BrowserContext, context),
        canonical_base_url="https://city.example/opi-wiki/",
        site_dir=site_dir,
    )
    assert context.pattern == "**/*"
    return context


def test_canonical_artifact_route_serves_pages_assets_and_query_variants(
    tmp_path: Path,
) -> None:
    """Canonical page and asset requests should use the built artifact only."""

    (tmp_path / "about").mkdir()
    (tmp_path / "assets").mkdir()
    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")
    (tmp_path / "about" / "index.html").write_text("<h1>About</h1>", encoding="utf-8")
    (tmp_path / "assets" / "site.css").write_text("body {}", encoding="utf-8")
    context = _install(tmp_path)

    root = context.request("https://city.example/opi-wiki/")
    page = context.request("https://city.example/opi-wiki/about/?source=browser")
    asset = context.request("https://city.example/opi-wiki/assets/site.css?v=1")

    assert root == {
        "status": 200,
        "content_type": "text/html; charset=utf-8",
        "body": b"<h1>OPI</h1>",
    }
    assert page["status"] == 200
    assert page["body"] == b"<h1>About</h1>"
    assert asset == {
        "status": 200,
        "content_type": "text/css; charset=utf-8",
        "body": b"body {}",
    }


@pytest.mark.parametrize(
    "url",
    (
        "https://foreign.example/opi-wiki/",
        "http://city.example/opi-wiki/",
        "https://city.example:444/opi-wiki/",
        "https://person@city.example/opi-wiki/",
        "https://city.example:invalid/opi-wiki/",
        "https://city.example/outside/",
        "https://city.example/opi-wiki",
        "https://city.example/opi-wiki-archive/",
        "https://city.example/opi-wiki//about/",
        "https://city.example/opi-wiki/../secret.txt",
        "https://city.example/opi-wiki/%2e%2e/secret.txt",
        "https://city.example/opi-wiki/%252e%252e/secret.txt",
        "https://city.example/opi-wiki/%25252e%25252e/secret.txt",
        "https://city.example/opi-wiki/assets%2fsecret.txt",
        "https://city.example/opi-wiki/assets%252Fsecret.txt",
        "https://city.example/opi-wiki/assets%25252fsecret.txt",
        r"https://city.example/opi-wiki/assets%5csecret.txt",
        "https://city.example/opi-wiki/malformed%ZZ.txt",
        "https://city.example/opi-wiki/#fragment",
        "https://city.example/opi-wiki/missing.html",
    ),
)
def test_canonical_artifact_route_fails_closed_with_not_found(
    tmp_path: Path,
    url: str,
) -> None:
    """No rejected request may escape to the external network or filesystem."""

    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")
    context = _install(tmp_path)

    assert context.request(url) == {
        "status": 404,
        "content_type": "text/plain; charset=utf-8",
        "body": b"Not Found\n",
    }


def test_canonical_artifact_route_rejects_a_symlink_escape(tmp_path: Path) -> None:
    """An artifact symlink must not expose a file outside the resolved build root."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    secret = tmp_path / "secret.txt"
    secret.write_text("outside artifact", encoding="utf-8")
    (site_dir / "leak.txt").symlink_to(secret)
    context = _install(site_dir)

    assert context.request("https://city.example/opi-wiki/leak.txt")["status"] == 404


def test_canonical_artifact_route_handles_head_without_a_response_body(
    tmp_path: Path,
) -> None:
    """HEAD should prove artifact availability without returning its bytes."""

    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")
    context = _install(tmp_path)

    assert context.request(
        "https://city.example/opi-wiki/",
        method="HEAD",
    ) == {
        "status": 200,
        "content_type": "text/html; charset=utf-8",
        "body": b"",
    }
    assert (
        context.request(
            "https://city.example/opi-wiki/missing/",
            method="HEAD",
        )["body"]
        == b""
    )


def test_canonical_artifact_route_rejects_unsupported_methods(tmp_path: Path) -> None:
    """The immutable artifact surface must not accept state-changing methods."""

    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")
    context = _install(tmp_path)

    assert (
        context.request(
            "https://city.example/opi-wiki/",
            method="POST",
        )["status"]
        == 404
    )


@pytest.mark.parametrize(
    ("site_path", "error_type", "message"),
    (
        ("missing", FileNotFoundError, "Built site directory was not found"),
        ("index.html", NotADirectoryError, "Built site path is not a directory"),
    ),
)
def test_canonical_artifact_route_rejects_an_invalid_build_root(
    tmp_path: Path,
    site_path: str,
    error_type: type[OSError],
    message: str,
) -> None:
    """Installation must fail before registering a route for an invalid root."""

    context = _FakeContext()
    if Path(site_path).suffix:
        (tmp_path / site_path).write_text("not a directory", encoding="utf-8")

    with pytest.raises(error_type, match=message):
        install_canonical_artifact_route(
            cast(BrowserContext, context),
            canonical_base_url="https://city.example/opi-wiki/",
            site_dir=tmp_path / site_path,
        )

    assert context.handler is None


def test_canonical_artifact_route_rejects_an_invalid_canonical_url(
    tmp_path: Path,
) -> None:
    """Only a validated HTTP(S) directory URL may establish the route boundary."""

    context = _FakeContext()

    with pytest.raises(ValueError, match=r"absolute HTTP\(S\) URL"):
        install_canonical_artifact_route(
            cast(BrowserContext, context),
            canonical_base_url="file:///tmp/site/",
            site_dir=tmp_path,
        )

    assert context.handler is None


@pytest.mark.parametrize(
    "canonical_base_url",
    (
        "https://city.example/opi%252Fwiki/",
        "https://city.example/opi-wiki/%252e%252e/",
    ),
)
def test_canonical_artifact_route_rejects_residual_encoded_path_syntax_in_base(
    tmp_path: Path,
    canonical_base_url: str,
) -> None:
    """The deployment boundary must not reveal unsafe syntax after another decode."""

    context = _FakeContext()

    with pytest.raises(
        ValueError,
        match="retains an encoded dot or path separator after decoding",
    ):
        install_canonical_artifact_route(
            cast(BrowserContext, context),
            canonical_base_url=canonical_base_url,
            site_dir=tmp_path,
        )

    assert context.handler is None


def test_canonical_artifact_route_supports_a_root_deployment(tmp_path: Path) -> None:
    """A site deployed at the origin root should retain the same containment rules."""

    (tmp_path / "index.html").write_text("<h1>Root</h1>", encoding="utf-8")
    context = _FakeContext()
    install_canonical_artifact_route(
        cast(BrowserContext, context),
        canonical_base_url="https://city.example/",
        site_dir=tmp_path,
    )

    assert context.request("https://city.example/")["body"] == b"<h1>Root</h1>"
