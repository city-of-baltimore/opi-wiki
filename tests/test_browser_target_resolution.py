"""Tests for authoritative live and static browser-target resolution."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import scripts.repo_tools.browser_routes as browser_routes
from scripts.repo_tools.browser_route_manifest import CanonicalRouteManifest
from scripts.repo_tools.browser_routes import (
    BrowserTarget,
    create_browser_context,
    resolved_browser_target,
)


def test_live_browser_target_normalizes_url_and_uses_preview_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A live preview should own its sitemap without requiring a built site."""

    preview_urls: list[str] = []

    def preview_manifest(base_url: str) -> CanonicalRouteManifest:
        preview_urls.append(base_url)
        return CanonicalRouteManifest(
            canonical_base_url=base_url,
            routes=("/", "/resources/"),
        )

    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest_from_preview",
        preview_manifest,
    )
    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest",
        lambda _site_dir: pytest.fail("A live preview must not inspect a static build."),
    )

    with resolved_browser_target(
        tmp_path / "not-built",
        "http://example.test/opi-wiki",
    ) as target:
        assert target == BrowserTarget(
            base_url="http://example.test/opi-wiki/",
            routes=("/", "/resources/"),
            artifact_dir=None,
        )
        field_name = "base_url"
        with pytest.raises(FrozenInstanceError):
            setattr(target, field_name, "http://mutated.example/")

    assert preview_urls == ["http://example.test/opi-wiki/"]


def test_live_browser_target_rejects_an_empty_preview_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty live sitemap must fail with the normalized source URL."""

    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest_from_preview",
        lambda base_url: CanonicalRouteManifest(base_url, ()),
    )

    with pytest.raises(RuntimeError) as captured:
        with resolved_browser_target(
            tmp_path / "not-built",
            "http://example.test/opi-wiki",
        ):
            pytest.fail("An empty route manifest must not yield a browser target.")

    assert str(captured.value) == (
        "Sitemap contains no canonical routes: http://example.test/opi-wiki/sitemap.xml"
    )


def test_static_browser_target_uses_one_canonical_artifact_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A static audit should retain exact sitemap identity and artifact location."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    load_manifest = MagicMock(
        return_value=CanonicalRouteManifest(
            canonical_base_url="https://city.example/opi-wiki/",
            routes=("/", "/about-us/"),
        )
    )
    monkeypatch.setattr(browser_routes, "canonical_route_manifest", load_manifest)
    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest_from_preview",
        lambda _base_url: pytest.fail("A static target must not read a live preview."),
    )

    with resolved_browser_target(site_dir) as target:
        assert target == BrowserTarget(
            base_url="https://city.example/opi-wiki/",
            routes=("/", "/about-us/"),
            artifact_dir=site_dir.resolve(),
        )

    load_manifest.assert_called_once_with(site_dir)


def test_static_browser_target_rejects_an_empty_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty artifact manifest must not become a vacuous browser pass."""

    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest",
        lambda _site_dir: CanonicalRouteManifest("https://city.example/opi-wiki/", ()),
    )

    with pytest.raises(RuntimeError) as captured:
        with resolved_browser_target(tmp_path):
            pytest.fail("An empty route manifest must not yield a browser target.")

    assert str(captured.value) == (
        f"Sitemap contains no canonical routes: {tmp_path / 'sitemap.xml'}"
    )


def test_static_browser_target_rejects_a_missing_build_before_manifest_loading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Static resolution should report the absent artifact before parsing it."""

    missing_site = tmp_path / "missing"
    load_manifest = MagicMock()
    monkeypatch.setattr(browser_routes, "canonical_route_manifest", load_manifest)

    with pytest.raises(FileNotFoundError) as captured:
        with resolved_browser_target(missing_site):
            pytest.fail("A missing built site must not yield a browser target.")

    assert str(captured.value) == f"Built site directory was not found: {missing_site}"
    load_manifest.assert_not_called()


def test_create_browser_context_mounts_static_and_bounds_live_reload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The shared seam should mount artifacts and abort only MkDocs' audit poll."""

    install_route = MagicMock()
    monkeypatch.setattr(browser_routes, "install_canonical_artifact_route", install_route)
    browser = MagicMock()
    static_context = MagicMock()
    live_context = MagicMock()
    browser.new_context.side_effect = (static_context, live_context)
    static_target = BrowserTarget(
        "https://city.example/opi-wiki/",
        ("/",),
        tmp_path,
    )
    live_target = BrowserTarget("http://127.0.0.1:5208/opi-wiki/", ("/",))

    assert (
        create_browser_context(
            browser,
            static_target,
            color_scheme="dark",
            service_workers="allow",
        )
        is static_context
    )
    assert create_browser_context(browser, live_target) is live_context

    assert browser.new_context.call_args_list[0].kwargs == {
        "color_scheme": "dark",
        "service_workers": "block",
        "offline": True,
    }
    assert browser.new_context.call_args_list[1].kwargs == {
        "service_workers": "block",
        "offline": False,
    }
    install_route.assert_called_once_with(
        static_context,
        canonical_base_url=static_target.base_url,
        site_dir=tmp_path,
    )
    static_context.route.assert_not_called()
    live_context.route.assert_called_once()
    route_pattern, live_reload_handler = live_context.route.call_args.args
    assert route_pattern == "**/livereload/**"

    live_reload_route = MagicMock()
    live_reload_route.request.url = "http://127.0.0.1:5208/livereload/123/456"
    live_reload_handler(live_reload_route)
    live_reload_route.abort.assert_called_once_with(error_code="aborted")
    live_reload_route.continue_.assert_not_called()

    foreign_route = MagicMock()
    foreign_route.request.url = "http://foreign.test/livereload/123/456"
    live_reload_handler(foreign_route)
    foreign_route.continue_.assert_called_once_with()
    foreign_route.abort.assert_not_called()
    static_context.set_default_timeout.assert_called_once_with(5000)
    live_context.set_default_timeout.assert_called_once_with(5000)


def test_create_browser_context_closes_a_context_when_routing_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A partial static mount must not leak an unrouted browser context."""

    context = MagicMock()
    browser = MagicMock()
    browser.new_context.return_value = context
    monkeypatch.setattr(
        browser_routes,
        "install_canonical_artifact_route",
        MagicMock(side_effect=RuntimeError("route installation failed")),
    )
    target = BrowserTarget("https://city.example/opi-wiki/", ("/",), tmp_path)

    with pytest.raises(RuntimeError, match="route installation failed"):
        create_browser_context(browser, target)

    context.close.assert_called_once_with()
