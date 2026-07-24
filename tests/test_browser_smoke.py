"""Tests for browser smoke configuration helpers."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
from urllib.request import urlopen

import pytest
import scripts.check_browser_smoke as browser_cli
import scripts.repo_tools.browser_smoke as browser_smoke
from scripts.check_browser_smoke import parse_args
from scripts.repo_tools.browser_smoke import (
    ORG_EXPECTED_NAMES,
    SMOKE_TARGETS,
    _check_org_chart_state,
    _check_page_load,
    _check_table_focus_state,
    canonical_route_paths,
    find_browser_smoke_issues,
    local_site_server,
    normalize_base_url,
    normalize_page_url,
)


def test_smoke_targets_cover_each_major_section() -> None:
    """Browser smoke coverage should keep one representative page per major section."""

    assert [target.section for target in SMOKE_TARGETS] == [
        "About Us",
        "How We Work",
        "What We Do",
        "Resources",
    ]

    assert all(target.path.endswith("/") for target in SMOKE_TARGETS)
    assert all("/public/" not in target.path for target in SMOKE_TARGETS)
    assert all(not target.path.startswith("/our-teams/") for target in SMOKE_TARGETS)


def test_normalize_base_url_enforces_trailing_slash() -> None:
    """Base URLs should normalize so joined paths stay stable."""

    assert normalize_base_url("http://127.0.0.1:8000") == "http://127.0.0.1:8000/"
    assert normalize_base_url("http://127.0.0.1:8000/") == "http://127.0.0.1:8000/"


def test_normalize_page_url_ignores_fragments_but_preserves_queries() -> None:
    """Final-URL checks should ignore fragments without hiding query redirects."""

    assert normalize_page_url("HTTPS://EXAMPLE.ORG/docs#section") == "https://example.org/docs/"
    assert normalize_page_url("https://example.org/docs/?view=all#top") == (
        "https://example.org/docs/?view=all"
    )


class _Response:
    """Minimal Playwright response stand-in for page-load tests."""

    def __init__(self, status: int) -> None:
        self.status = status


class _Page:
    """Minimal Playwright page stand-in for final-URL tests."""

    def __init__(self, url: str) -> None:
        self.url = url


class _EvaluationPage:
    """Playwright page stand-in returning one scripted DOM result."""

    def __init__(self, result: object) -> None:
        self.result = result

    def evaluate(self, script: str) -> object:
        """Return the configured result after verifying the expected selector."""

        return self.result


def test_canonical_route_paths_are_derived_from_the_sitemap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route crawl should use canonical sitemap URLs and strip the deploy base."""

    monkeypatch.setattr(browser_smoke, "discover_site_base_path", lambda _site: "/opi-wiki/")
    monkeypatch.setattr(
        browser_smoke,
        "load_sitemap_locations",
        lambda _site: [
            "https://example.test/opi-wiki/",
            "https://example.test/opi-wiki/resources/",
            "https://example.test/outside/",
        ],
    )

    assert canonical_route_paths(tmp_path) == ["/", "/resources/"]


def test_page_load_accepts_a_200_at_the_canonical_url() -> None:
    """A canonical page returning HTTP 200 should pass the load check."""

    requested = "http://127.0.0.1:5208/resources/"

    assert _check_page_load(_Page(requested), _Response(200), requested, "Resources", "light") == []


def test_page_load_reports_status_and_unexpected_redirect() -> None:
    """HTTP errors and redirect-only smoke targets must fail with useful evidence."""

    issues = _check_page_load(
        _Page("http://127.0.0.1:5208/retired/"),
        _Response(404),
        "http://127.0.0.1:5208/resources/",
        "Resources",
        "dark",
    )

    assert len(issues) == 2
    assert "returned HTTP 404" in issues[0]
    assert "expected canonical URL" in issues[1]


def test_page_load_reports_a_missing_navigation_response() -> None:
    """Non-HTTP navigation results should fail instead of passing vacuously."""

    issues = _check_page_load(
        _Page("about:blank"),
        None,
        "http://127.0.0.1:5208/resources/",
        "Resources",
        "light",
    )

    assert issues == ["Resources (light): navigation returned no HTTP response."]


def test_table_scroll_wrapper_has_keyboard_focus_treatment() -> None:
    """Generated table wrappers should be tabbable and visibly focused."""

    page = _EvaluationPage({"tabIndex": 0, "outlineStyle": "solid", "outlineWidth": "2px"})

    assert _check_table_focus_state(page, "light", "direct load") == []


def test_table_scroll_wrapper_reports_missing_or_inaccessible_state() -> None:
    """Missing wrappers, tabindex drift, and invisible focus must be actionable."""

    assert _check_table_focus_state(_EvaluationPage(None), "dark", "direct load") == [
        "Table scroll region (dark, direct load): generated scroll wrapper was not found."
    ]

    issues = _check_table_focus_state(
        _EvaluationPage({"tabIndex": -1, "outlineStyle": "none", "outlineWidth": "0px"}),
        "dark",
        "instant navigation",
    )

    assert len(issues) == 2
    assert "tabIndex was -1" in issues[0]
    assert "focus outline was not visible" in issues[1]


def test_org_chart_exposes_the_expected_visible_hierarchy() -> None:
    """The rendered chart should expose all public leaders at the intended levels."""

    page = _EvaluationPage(
        {
            "chartVisible": True,
            "visibleNames": list(ORG_EXPECTED_NAMES),
            "cityCount": 1,
            "executiveCount": 1,
            "teamCount": 4,
        }
    )

    assert _check_org_chart_state(page, "light", "direct load") == []


def test_org_chart_reports_missing_names_and_hierarchy_drift() -> None:
    """Chart regressions should name both the missing leaders and structural mismatch."""

    page = _EvaluationPage(
        {
            "chartVisible": False,
            "visibleNames": [],
            "cityCount": 0,
            "executiveCount": 0,
            "teamCount": 0,
        }
    )

    issues = _check_org_chart_state(page, "dark", "instant navigation")

    assert len(issues) == 3
    assert "no visible dimensions" in issues[0]
    assert "public leadership names were not visible" in issues[1]
    assert "hierarchy counts" in issues[2]


def test_source_override_keeps_static_repo_link_without_stats_hook() -> None:
    """Repository navigation should not activate Material's optional API fetches."""

    source_override = Path("overrides/partials/source.html").read_text(encoding="utf-8")

    assert 'href="{{ config.repo_url }}"' in source_override
    assert "{{ config.repo_name }}" in source_override
    assert 'data-md-component="source" hook' in source_override
    anchor_markup = source_override.split("<a", maxsplit=1)[1].split(">", maxsplit=1)[0]
    assert "data-md-component" not in anchor_markup


def test_local_site_server_serves_the_requested_directory(tmp_path: Path) -> None:
    """The browser orchestrator's local server should expose freshly built files."""

    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")

    with local_site_server(tmp_path) as base_url:
        with urlopen(base_url, timeout=2) as response:  # noqa: S310
            assert response.status == 200
            assert b"<h1>OPI</h1>" in response.read()


def test_browser_smoke_rejects_a_missing_built_site(tmp_path: Path) -> None:
    """A missing build must fail before a local server is started."""

    missing_site = tmp_path / "missing-site"

    with pytest.raises(FileNotFoundError, match="Built site directory was not found"):
        find_browser_smoke_issues(missing_site)


def test_browser_smoke_rejects_a_file_in_place_of_the_built_site(tmp_path: Path) -> None:
    """The local server requires a directory, not merely an existing path."""

    not_a_site = tmp_path / "site.html"
    not_a_site.write_text("<h1>Not a directory</h1>", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="Built site directory was not found"):
        find_browser_smoke_issues(not_a_site)


def test_browser_smoke_uses_a_normalized_explicit_base_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An external preview URL should bypass the local server and normalize once."""

    seen: list[str] = []

    def collect(
        _sync_playwright: object,
        base_url: str,
        _routes: tuple[str, ...],
    ) -> list[str]:
        seen.append(base_url)
        return ["example finding"]

    monkeypatch.setattr(browser_smoke, "_collect_browser_smoke_issues", collect)

    issues = find_browser_smoke_issues(tmp_path / "not-built", base_url="http://example.test/docs")

    assert issues == ["example finding"]
    assert seen == ["http://example.test/docs/"]


def test_browser_smoke_serves_a_built_site_for_the_collector(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without an external URL, orchestration should use a loopback site server."""

    (tmp_path / "index.html").write_text("<h1>Home</h1>", encoding="utf-8")
    seen: list[str] = []

    def collect(
        _sync_playwright: object,
        base_url: str,
        _routes: tuple[str, ...],
    ) -> list[str]:
        seen.append(base_url)
        return []

    monkeypatch.setattr(browser_smoke, "_collect_browser_smoke_issues", collect)

    assert find_browser_smoke_issues(tmp_path) == []
    assert len(seen) == 1
    assert seen[0].startswith("http://127.0.0.1:")
    assert seen[0].endswith("/")


def test_browser_cli_parses_site_and_base_url_options(tmp_path: Path) -> None:
    """The CLI should preserve an explicit preview target and built-site path."""

    args = parse_args(["--site-dir", str(tmp_path), "--base-url", "http://example.test"])

    assert args.site_dir == tmp_path
    assert args.base_url == "http://example.test"


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
    """The browser orchestrator should cover both schemes and always close contexts."""

    page = MagicMock()

    def navigate(url: str, *, wait_until: str) -> SimpleNamespace:
        """Record a fake successful navigation and expose its final URL."""

        assert wait_until == "networkidle"
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

    monkeypatch.setattr(browser_smoke, "_check_page_load", lambda *_args: [])
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

    issues = browser_smoke._collect_browser_smoke_issues(lambda: manager, "http://example.test/")

    assert issues == []
    assert [call.kwargs["color_scheme"] for call in browser.new_context.call_args_list] == [
        "light",
        "dark",
    ]
    assert page.goto.call_count == 14
    assert context.close.call_count == 2
    browser.close.assert_called_once_with()
