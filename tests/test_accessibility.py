"""Tests for lightweight accessibility smoke checks."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.accessibility import find_accessibility_issues


def test_accessibility_checker_ignores_non_clickable_cards(tmp_path: Path) -> None:
    """Cards without links should not fail the smoke check."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        '<div class="opi-card-grid"><div class="opi-card"><h3>Info</h3></div></div>',
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert issues == []


def test_accessibility_checker_flags_empty_card_link_text(tmp_path: Path) -> None:
    """Linked cards must expose visible link text."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        (
            '<div class="opi-card-grid"><div class="opi-card">'
            '<a class="opi-card-link" href="/test/"></a>'
            "</div></div>"
        ),
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert len(issues) == 1
    assert "missing visible link text" in issues[0]
