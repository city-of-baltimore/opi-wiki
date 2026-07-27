"""Tests for the full-browser accessibility assurance harness."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import scripts.check_browser_accessibility as browser_accessibility_cli
import scripts.repo_tools.browser_accessibility as browser_accessibility
from scripts.check_browser_accessibility import parse_args
from scripts.repo_tools.browser_accessibility import (
    AUDIT_PROFILES,
    _AuditProfile,
    _check_document_reflow,
    _check_skip_link,
    _format_axe_violations,
    find_browser_accessibility_issues,
)


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


def test_browser_accessibility_rejects_an_empty_route_manifest(
    tmp_path: Path,
) -> None:
    """A missing sitemap must not turn the canonical-route audit into a vacuous pass."""

    with pytest.raises(RuntimeError, match="Built sitemap contains no canonical routes"):
        find_browser_accessibility_issues(tmp_path, base_url="http://example.test")


def test_browser_accessibility_normalizes_an_explicit_base_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An explicit preview URL should normalize once and bypass the local server."""

    seen: list[str] = []
    monkeypatch.setattr(
        browser_accessibility,
        "canonical_route_paths",
        lambda _site: ["/", "/resources/"],
    )

    def collect(
        _sync_playwright: object,
        _axe_factory: object,
        base_url: str,
        _routes: tuple[str, ...],
    ) -> list[str]:
        seen.append(base_url)
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
    assert seen == ["http://example.test/docs/"]


def test_browser_accessibility_serves_a_built_site(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without an external URL the audit should serve the freshly built artifact."""

    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")
    seen: list[str] = []
    monkeypatch.setattr(
        browser_accessibility,
        "canonical_route_paths",
        lambda _site: ["/"],
    )

    def collect(
        _sync_playwright: object,
        _axe_factory: object,
        base_url: str,
        _routes: tuple[str, ...],
    ) -> list[str]:
        seen.append(base_url)
        return []

    monkeypatch.setattr(
        browser_accessibility,
        "_collect_browser_accessibility_issues",
        collect,
    )

    assert find_browser_accessibility_issues(tmp_path) == []
    assert len(seen) == 1
    assert seen[0].startswith("http://127.0.0.1:")


def test_browser_accessibility_cli_parses_site_and_base_url(tmp_path: Path) -> None:
    """The CLI should preserve an explicit preview target and site directory."""

    args = parse_args(["--site-dir", str(tmp_path), "--base-url", "http://example.test"])

    assert args.site_dir == tmp_path
    assert args.base_url == "http://example.test"


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
