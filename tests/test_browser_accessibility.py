"""Tests for the full-browser accessibility assurance harness."""

from __future__ import annotations

import builtins
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock

import pytest
import scripts.check_browser_accessibility as browser_accessibility_cli
import scripts.repo_tools.browser_accessibility as browser_accessibility
import scripts.repo_tools.browser_routes as browser_routes
from scripts.check_browser_accessibility import parse_args
from scripts.repo_tools.browser_accessibility import (
    AUDIT_PROFILES,
    _AuditProfile,
    _check_document_reflow,
    _check_skip_link,
    _format_axe_violations,
    find_browser_accessibility_issues,
)
from scripts.repo_tools.browser_route_manifest import CanonicalRouteManifest
from scripts.repo_tools.browser_routes import BrowserTarget


def test_audit_profiles_cover_desktop_reflow_and_both_color_schemes() -> None:
    """The matrix must retain every responsive and contrast-sensitive state."""

    assert [(profile.name, profile.width) for profile in AUDIT_PROFILES] == [
        ("desktop-light", 1440),
        ("desktop-dark", 1440),
        ("reflow-light", 320),
        ("reflow-dark", 320),
    ]


def test_axe_violations_preserve_route_target_and_help_evidence() -> None:
    """Axe failures should identify the exact route, state, rule, and element."""

    profile = _AuditProfile("desktop-light", 1440, 900, "light", False)
    response = {
        "violations": [
            {
                "id": "color-contrast",
                "impact": "serious",
                "help": "Elements must meet minimum color contrast ratio thresholds",
                "helpUrl": "https://example.test/color-contrast",
                "nodes": [
                    {
                        "target": [".example"],
                        "failureSummary": "Fix the foreground and background colors.",
                    }
                ],
            }
        ]
    }

    issues = _format_axe_violations("/example/", profile, response, state="search open")

    assert len(issues) == 1
    assert "/example/ (desktop-light, search open)" in issues[0]
    assert "axe color-contrast [serious] at .example" in issues[0]
    assert "Fix the foreground and background colors." in issues[0]
    assert "https://example.test/color-contrast" in issues[0]


def test_axe_formatter_accepts_a_clean_result() -> None:
    """A clean axe response should remain a clean gate result."""

    profile = _AuditProfile("reflow-dark", 320, 800, "dark", True)

    assert _format_axe_violations("/", profile, {"violations": []}) == []


def test_reflow_check_accepts_content_that_fits_320_css_pixels() -> None:
    """A 320px page without document-level overflow satisfies the reflow ratchet."""

    page = MagicMock()
    page.evaluate.return_value = {"viewportWidth": 320, "documentWidth": 320}
    profile = _AuditProfile("reflow-light", 320, 800, "light", True)

    assert _check_document_reflow(page, "/example/", profile) == []


def test_reflow_check_reports_document_level_horizontal_scrolling() -> None:
    """A page wider than the 320px viewport must fail with measured evidence."""

    page = MagicMock()
    page.evaluate.return_value = {"viewportWidth": 320, "documentWidth": 481}
    profile = _AuditProfile("reflow-dark", 320, 800, "dark", True)

    issues = _check_document_reflow(page, "/example/", profile)

    assert issues == [
        "/example/ (reflow-dark): document width was 481px inside a 320px viewport; "
        "WCAG 2.2 AA reflow requires page-level horizontal scrolling to remain absent."
    ]


def test_skip_link_check_accepts_visible_main_content_target() -> None:
    """The first desktop Tab should reveal the canonical content bypass link."""

    page = MagicMock()
    page.goto.return_value = SimpleNamespace(status=200)
    page.url = "http://example.test/"
    page.evaluate.return_value = {
        "className": "md-skip",
        "href": "http://example.test/#start-here",
        "sameDocument": True,
        "targetExists": True,
        "visible": True,
    }
    profile = _AuditProfile("desktop-light", 1440, 900, "light", False)

    assert _check_skip_link(page, "http://example.test/", profile) == []
    page.keyboard.press.assert_called_once_with("Tab")
    page.wait_for_timeout.assert_called_once_with(300)


def test_skip_link_check_reports_missing_focus_target() -> None:
    """A first Tab that misses the bypass link should fail explicitly."""

    page = MagicMock()
    page.goto.return_value = SimpleNamespace(status=200)
    page.url = "http://example.test/"
    page.evaluate.return_value = None
    profile = _AuditProfile("desktop-dark", 1440, 900, "dark", False)

    issues = _check_skip_link(page, "http://example.test/", profile)

    assert issues[-1] == "Skip link (desktop-dark): first Tab did not focus the skip link."


def test_browser_accessibility_rejects_a_missing_built_site(tmp_path: Path) -> None:
    """The audit must fail before browser startup when the build is absent."""

    with pytest.raises(FileNotFoundError, match="Built site directory was not found"):
        find_browser_accessibility_issues(tmp_path / "missing")


def test_browser_accessibility_reports_missing_dependency_before_resolving_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A missing axe runtime should fail before any preview network work."""

    original_import = builtins.__import__

    def import_without_axe(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "axe_playwright_python.sync_playwright":
            raise ModuleNotFoundError(name)
        return original_import(name, *args, **kwargs)

    def reject_target_resolution(*_args: object, **_kwargs: object) -> object:
        pytest.fail("Browser target resolution ran before dependency validation.")

    monkeypatch.setattr(builtins, "__import__", import_without_axe)
    monkeypatch.setattr(
        browser_accessibility,
        "resolved_browser_target",
        reject_target_resolution,
    )

    with pytest.raises(RuntimeError) as captured:
        find_browser_accessibility_issues(
            tmp_path / "not-built",
            base_url="http://example.test/preview",
        )

    assert str(captured.value) == (
        "Browser accessibility dependencies are missing. Run 'uv sync' and "
        "'uv run playwright install chromium' first."
    )


def test_browser_accessibility_rejects_an_empty_route_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A missing sitemap must not turn the canonical-route audit into a vacuous pass."""

    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest_from_preview",
        lambda _base_url: CanonicalRouteManifest(
            canonical_base_url="http://example.test/",
            routes=(),
        ),
    )

    with pytest.raises(RuntimeError, match="Sitemap contains no canonical routes"):
        find_browser_accessibility_issues(tmp_path, base_url="http://example.test")


def test_browser_accessibility_normalizes_an_explicit_base_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An explicit preview URL should normalize once without artifact routing."""

    seen: list[BrowserTarget] = []
    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest_from_preview",
        lambda _base_url: CanonicalRouteManifest(
            canonical_base_url="http://example.test/docs/",
            routes=("/", "/resources/"),
        ),
    )

    def collect(
        _sync_playwright: object,
        _axe_factory: object,
        target: BrowserTarget,
    ) -> list[str]:
        seen.append(target)
        return ["fixture finding"]

    monkeypatch.setattr(
        browser_accessibility,
        "_collect_browser_accessibility_issues",
        collect,
    )

    issues = find_browser_accessibility_issues(
        tmp_path,
        base_url="http://example.test/docs",
    )

    assert issues == ["fixture finding"]
    assert seen == [
        BrowserTarget(
            base_url="http://example.test/docs/",
            routes=("/", "/resources/"),
            artifact_dir=None,
        )
    ]


def test_accessibility_crawl_encodes_decoded_route_delimiters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The accessibility consumer must navigate the encoded canonical identity."""

    profile = _AuditProfile("desktop-light", 1440, 900, "light", False)
    monkeypatch.setattr(browser_accessibility, "AUDIT_PROFILES", (profile,))
    monkeypatch.setattr(browser_accessibility, "_format_axe_violations", lambda *_args: [])
    monkeypatch.setattr(browser_accessibility, "_check_document_reflow", lambda *_args: [])
    monkeypatch.setattr(browser_accessibility, "_check_skip_link", lambda *_args: [])
    monkeypatch.setattr(
        browser_accessibility,
        "_check_mobile_interactive_states",
        lambda *_args: [],
    )

    page = MagicMock()

    def navigate(url: str, *, wait_until: str) -> SimpleNamespace:
        """Expose the encoded URL as a successful canonical navigation."""

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
    axe_factory = MagicMock()
    target = BrowserTarget(
        base_url="http://example.test/opi-wiki/",
        routes=("/#/?/%/",),
    )

    assert (
        browser_accessibility._collect_browser_accessibility_issues(
            lambda: manager,
            axe_factory,
            target,
        )
        == []
    )
    assert page.goto.call_args.args[0] == "http://example.test/opi-wiki/%23/%3F/%25/"
    browser.new_context.assert_called_once_with(
        color_scheme="light",
        viewport={"width": 1440, "height": 900},
        is_mobile=False,
        service_workers="block",
        offline=False,
    )
    context.set_default_timeout.assert_called_once_with(5000)


def test_browser_accessibility_mounts_a_built_site_at_its_canonical_origin(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A static audit should preserve the artifact's production URL identity."""

    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")
    canonical_base_url = "https://city-of-baltimore.github.io/opi-wiki/"
    seen: list[BrowserTarget] = []
    monkeypatch.setattr(
        browser_routes,
        "canonical_route_manifest",
        lambda _site: CanonicalRouteManifest(
            canonical_base_url=canonical_base_url,
            routes=("/",),
        ),
    )

    def collect(
        _sync_playwright: object,
        _axe_factory: object,
        target: BrowserTarget,
    ) -> list[str]:
        seen.append(target)
        return []

    monkeypatch.setattr(
        browser_accessibility,
        "_collect_browser_accessibility_issues",
        collect,
    )

    assert find_browser_accessibility_issues(tmp_path) == []
    assert seen == [
        BrowserTarget(
            base_url=canonical_base_url,
            routes=("/",),
            artifact_dir=tmp_path.resolve(),
        )
    ]


def test_browser_accessibility_cli_parses_site_and_base_url(tmp_path: Path) -> None:
    """The CLI should preserve an explicit preview target and site directory."""

    args = parse_args(["--site-dir", str(tmp_path), "--base-url", "http://example.test"])

    assert args.site_dir == tmp_path
    assert args.base_url == "http://example.test"


def test_browser_accessibility_cli_rejects_unknown_arguments(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A misspelled accessibility option must fail instead of being ignored."""

    with pytest.raises(SystemExit) as captured:
        parse_args(["--not-an-accessibility-option"])

    assert captured.value.code == 2
    assert "unrecognized arguments: --not-an-accessibility-option" in capsys.readouterr().err


def test_browser_accessibility_cli_reports_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI should report a clean audit with a zero exit code."""

    monkeypatch.setattr(
        browser_accessibility_cli,
        "find_browser_accessibility_issues",
        lambda *_args, **_kwargs: [],
    )

    assert browser_accessibility_cli.main(["--site-dir", str(tmp_path)]) == 0
    assert (
        capsys.readouterr().out
        == "Browser accessibility audit passed across all canonical routes.\n"
    )


def test_browser_accessibility_cli_reports_findings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI should surface actionable browser findings and fail."""

    monkeypatch.setattr(
        browser_accessibility_cli,
        "find_browser_accessibility_issues",
        lambda *_args, **_kwargs: ["fixture issue"],
    )

    assert browser_accessibility_cli.main(["--site-dir", str(tmp_path)]) == 1
    assert "fixture issue" in capsys.readouterr().err
