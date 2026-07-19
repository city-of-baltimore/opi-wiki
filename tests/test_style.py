"""Tests for the editorial voice guardrail."""

from __future__ import annotations

from pathlib import Path

from main import DOCS_DIR
from scripts.repo_tools.style import find_style_issues


def _write(tmp_path: Path, name: str, text: str) -> Path:
    """Write a Markdown fixture and return its path."""

    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_flags_prose_em_dash(tmp_path: Path) -> None:
    """An em-dash in a prose line is reported."""

    path = _write(tmp_path, "a.md", "We move fast — with intention.\n")
    issues = find_style_issues([path])

    assert len(issues) == 1
    assert "em-dash in prose" in issues[0]


def test_ignores_em_dash_in_table_and_code(tmp_path: Path) -> None:
    """Em-dashes in table rows and fenced code are allowed."""

    text = "| Cell — with dash | Second |\n\n```\ncode — with dash\n```\n"
    path = _write(tmp_path, "b.md", text)

    assert find_style_issues([path]) == []


def test_flags_banned_jargon_case_insensitively(tmp_path: Path) -> None:
    """Banned jargon is reported regardless of case or inflection."""

    path = _write(tmp_path, "c.md", "The Operating Backbone leverages synergies.\n")
    issues = find_style_issues([path])

    joined = "\n".join(issues)
    assert "operating backbone" in joined
    assert "leverage" in joined
    assert "synerg" in joined


def test_clean_prose_passes(tmp_path: Path) -> None:
    """Plain prose with no em-dashes or jargon produces no issues."""

    path = _write(tmp_path, "d.md", "AdminOps keeps the office running, so teams can deliver.\n")

    assert find_style_issues([path]) == []


def test_live_docs_pass_the_guardrail() -> None:
    """Every checked-in wiki page already meets the guardrail."""

    issues = find_style_issues(sorted(DOCS_DIR.rglob("*.md")))

    assert issues == [], "\n".join(issues)
