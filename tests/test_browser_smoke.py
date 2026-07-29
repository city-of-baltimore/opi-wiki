"""Tests for browser smoke configuration helpers."""

from __future__ import annotations

import builtins
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock

import pytest
import scripts.check_browser_smoke as browser_cli
import scripts.repo_tools.browser_routes as browser_routes
import scripts.repo_tools.browser_smoke as browser_smoke
from scripts.check_browser_smoke import parse_args
from scripts.repo_tools.browser_route_manifest import CanonicalRouteManifest
from scripts.repo_tools.browser_routes import BrowserTarget
from scripts.repo_tools.browser_smoke import (
    _crawl_canonical_routes,
    find_browser_smoke_issues,
)


def test_canonical_smoke_crawl_encodes_decoded_route_delimiters() -> None:
    """The smoke consumer must never reinterpret decoded route identity."""

    page = MagicMock()

    def navigate(url: str, *, wait_until: str) -> SimpleNamespace:
        """Expose the encoded destination as the fake page's final URL."""

        assert wait_until == "load"
        page.url = url
        return SimpleNamespace(status=200)

    page.goto.side_effect = navigate
    context = MagicMock()
    context.new_page.return_value = page
    browser = MagicMock()
    browser.new_context.return_value = context

    assert (
        _crawl_canonical_routes(
            browser,
            BrowserTarget(
                base_url="http://example.test/opi-wiki/",
                routes=("/#/?/%/",),
            ),
        )
        == []
    )
    assert page.goto.call_args.args[0] == "http://example.test/opi-wiki/%23/%3F/%25/"
    browser.new_context.assert_called_once_with(
        viewport={"width": 1440, "height": 900},
        service_workers="block",
        offline=False,
    )


def test_source_override_keeps_static_repo_link_without_stats_hook() -> None:
    """Repository navigation should not activate Material's optional API fetches."""

    source_override = Path("overrides/partials/source.html").read_text(encoding="utf-8")

    assert 'href="{{ config.repo_url }}"' in source_override
    assert "{{ config.repo_name }}" in source_override
    assert 'data-md-component="source" hook' in source_override
    anchor_markup = source_override.split("<a", maxsplit=1)[1].split(">", maxsplit=1)[0]
    assert "data-md-component" not in anchor_markup


def test_search_toggle_does_not_wait_for_a_navigation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Opening the in-document search control must remain safe in offline Chromium."""

    page = MagicMock()
    page.url = "https://city.example/opi-wiki/"
    search_toggle = MagicMock()
    search_toggle.count.return_value = 1
    search_input = MagicMock()
    result_link = MagicMock()
    result_link.inner_text.return_value = "CitiStat"
    result_link.get_attribute.return_value = "what-we-do/programs/citistat/"
    for locator in (search_toggle, search_input, result_link):
        locator.first = locator
    page.locator.side_effect = (search_toggle, search_input, result_link)
    monkeypatch.setattr(browser_smoke, "navigate_to_ready_page", lambda *_args: [])
    instant_navigation = MagicMock(return_value=[])
    monkeypatch.setattr(browser_smoke, "navigate_to_instant_page", instant_navigation)

    assert browser_smoke._check_search_workflow(page, str(page.url), "light") == []
    search_toggle.click.assert_called_once_with(no_wait_after=True)
    instant_navigation.assert_called_once()


def test_browser_smoke_rejects_a_missing_built_site(tmp_path: Path) -> None:
    """A missing build must fail before a static browser target is created."""

    missing_site = tmp_path / "missing-site"

    with pytest.raises(FileNotFoundError, match="Built site directory was not found"):
        find_browser_smoke_issues(missing_site)


def test_browser_smoke_rejects_a_file_in_place_of_the_built_site(tmp_path: Path) -> None:
    """Static artifact routing requires a directory, not merely an existing path."""

    not_a_site = tmp_path / "site.html"
    not_a_site.write_text("<h1>Not a directory</h1>", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="Built site directory was not found"):
        find_browser_smoke_issues(not_a_site)


def test_browser_smoke_reports_missing_dependency_before_resolving_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A missing browser runtime should not trigger preview network work."""

    original_import = builtins.__import__

    def import_without_playwright(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "playwright.sync_api":
            raise ModuleNotFoundError(name)
        return original_import(name, *args, **kwargs)

    def reject_target_resolution(*_args: object, **_kwargs: object) -> object:
        pytest.fail("Browser target resolution ran before dependency validation.")

    monkeypatch.setattr(builtins, "__import__", import_without_playwright)
    monkeypatch.setattr(browser_smoke, "resolved_browser_target", reject_target_resolution)

    with pytest.raises(RuntimeError) as captured:
        find_browser_smoke_issues(
            tmp_path / "not-built",
            base_url="http://example.test/preview",
        )

    assert str(captured.value) == (
        "Playwright is not installed. Run 'uv sync' and 'uv run playwright install chromium' first."
    )


def test_browser_smoke_uses_a_normalized_explicit_base_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A live preview URL should bypass artifact routing and normalize once."""

    seen: list[BrowserTarget] = []

    def collect(
        _sync_playwright: object,
        target: BrowserTarget,
    ) -> list[str]:
        seen.append(target)
        return ["example finding"]

    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest_from_preview",
        lambda base_url: CanonicalRouteManifest(
            canonical_base_url=base_url,
            routes=("/", "/resources/"),
        ),
    )
    monkeypatch.setattr(browser_smoke, "_collect_browser_smoke_issues", collect)

    issues = find_browser_smoke_issues(tmp_path / "not-built", base_url="http://example.test/docs")

    assert issues == ["example finding"]
    assert seen == [
        BrowserTarget(
            base_url="http://example.test/docs/",
            routes=("/", "/resources/"),
        )
    ]


def test_browser_smoke_rejects_an_empty_preview_route_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An explicit preview must never turn an empty live sitemap into a pass."""

    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest_from_preview",
        lambda base_url: CanonicalRouteManifest(
            canonical_base_url=base_url,
            routes=(),
        ),
    )

    with pytest.raises(RuntimeError, match="Sitemap contains no canonical routes"):
        find_browser_smoke_issues(
            tmp_path / "not-built",
            base_url="http://example.test/docs",
        )


def test_browser_smoke_mounts_a_built_site_at_its_canonical_origin(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A static audit should pass the exact artifact and sitemap origin downstream."""

    (tmp_path / "index.html").write_text("<h1>Home</h1>", encoding="utf-8")
    (tmp_path / "sitemap.xml").write_text(
        (
            "<urlset>"
            "<url><loc>https://example.test/opi-wiki/</loc></url>"
            "<url><loc>https://example.test/opi-wiki/resources/</loc></url>"
            "</urlset>"
        ),
        encoding="utf-8",
    )
    seen: list[BrowserTarget] = []

    def collect(
        _sync_playwright: object,
        target: BrowserTarget,
    ) -> list[str]:
        seen.append(target)
        return []

    monkeypatch.setattr(browser_smoke, "_collect_browser_smoke_issues", collect)

    assert find_browser_smoke_issues(tmp_path) == []
    assert seen == [
        BrowserTarget(
            base_url="https://example.test/opi-wiki/",
            routes=("/", "/resources/"),
            artifact_dir=tmp_path.resolve(),
        )
    ]


def test_browser_cli_parses_site_and_base_url_options(tmp_path: Path) -> None:
    """The CLI should preserve an explicit preview target and built-site path."""

    args = parse_args(["--site-dir", str(tmp_path), "--base-url", "http://example.test"])

    assert args.site_dir == tmp_path
    assert args.base_url == "http://example.test"


def test_browser_cli_rejects_unknown_arguments(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A misspelled browser option must fail instead of being ignored."""

    with pytest.raises(SystemExit) as captured:
        parse_args(["--not-a-browser-option"])

    assert captured.value.code == 2
    assert "unrecognized arguments: --not-a-browser-option" in capsys.readouterr().err


def test_browser_cli_reports_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The browser CLI should return zero when the collector finds no issues."""

    monkeypatch.setattr(browser_cli, "find_browser_smoke_issues", lambda *_args, **_kwargs: [])

    assert browser_cli.main(["--site-dir", str(tmp_path)]) == 0
    assert capsys.readouterr().out == "Browser smoke check passed.\n"


def test_browser_cli_reports_findings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Browser findings should become a nonzero CLI result with evidence."""

    monkeypatch.setattr(
        browser_cli,
        "find_browser_smoke_issues",
        lambda *_args, **_kwargs: ["drawer did not open"],
    )

    assert browser_cli.main(["--site-dir", str(tmp_path)]) == 1
    assert "drawer did not open" in capsys.readouterr().err


def test_browser_collector_runs_both_color_schemes_and_closes_resources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every crawl should use the shared fail-closed context lifecycle."""

    page = MagicMock()

    def navigate(url: str, *, wait_until: str) -> SimpleNamespace:
        """Record a fake successful navigation and expose its final URL."""

        assert wait_until == "load"
        page.url = url
        return SimpleNamespace(status=200)

    page.goto.side_effect = navigate
    context = MagicMock()
    context.new_page.return_value = page
    browser = MagicMock()
    browser.new_context.return_value = context
    playwright = SimpleNamespace(chromium=SimpleNamespace(launch=lambda: browser))
    manager = MagicMock()
    manager.__enter__.return_value = playwright

    monkeypatch.setattr(browser_smoke, "_check_mobile_nav_state", lambda *_args: [])
    monkeypatch.setattr(browser_smoke, "_check_table_focus_state", lambda *_args: [])
    monkeypatch.setattr(
        browser_smoke,
        "_check_table_focus_after_instant_navigation",
        lambda *_args: [],
    )
    monkeypatch.setattr(browser_smoke, "_check_card_focus_state", lambda *_args: [])
    monkeypatch.setattr(browser_smoke, "_check_org_chart_state", lambda *_args: [])
    monkeypatch.setattr(
        browser_smoke,
        "_check_org_chart_after_instant_navigation",
        lambda *_args: [],
    )
    monkeypatch.setattr(browser_smoke, "_check_search_workflow", lambda *_args: [])
    create_context = MagicMock(side_effect=browser_smoke.create_browser_context)
    monkeypatch.setattr(browser_smoke, "create_browser_context", create_context)
    target = BrowserTarget("http://example.test/", ("/",))

    issues = browser_smoke._collect_browser_smoke_issues(lambda: manager, target)

    assert issues == []
    assert [call.kwargs.get("color_scheme") for call in browser.new_context.call_args_list] == [
        None,
        "light",
        "dark",
    ]
    assert all(
        call.kwargs["service_workers"] == "block" for call in browser.new_context.call_args_list
    )
    assert all(call.kwargs["offline"] is False for call in browser.new_context.call_args_list)
    assert create_context.call_count == 3
    assert all(call.args[1] == target for call in create_context.call_args_list)
    assert page.goto.call_count == 15
    assert context.set_default_timeout.call_count == 3
    assert context.close.call_count == 3
    browser.close.assert_called_once_with()
