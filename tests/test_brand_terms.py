"""Tests for editorial brand-term validation."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.brand_terms import find_brand_term_issues


def test_brand_term_checker_flags_editorial_casing_errors(tmp_path: Path) -> None:
    """The checker should catch prose casing mistakes for OPI and CitiStat."""

    markdown_file = tmp_path / "sample.md"
    markdown_file.write_text(
        "# Sample\n\nOpi is wrong here.\nCitistat is also wrong here.\n",
        encoding="utf-8",
    )

    issues = find_brand_term_issues([markdown_file])

    assert len(issues) == 2
    assert "Use 'OPI', not 'Opi'." in issues[0] or "Use 'OPI', not 'Opi'." in issues[1]
    assert (
        "Use 'CitiStat', not 'Citistat'." in issues[0]
        or "Use 'CitiStat', not 'Citistat'." in issues[1]
    )


def test_brand_term_checker_ignores_urls_and_code(tmp_path: Path) -> None:
    """Valid lowercase tokens inside code and URLs should not raise issues."""

    markdown_file = tmp_path / "sample.md"
    markdown_file.write_text(
        "# Sample\n\n"
        "Visit https://opi.baltimorecity.gov for details.\n\n"
        "`opi-foundations` stays lowercase in code.\n",
        encoding="utf-8",
    )

    issues = find_brand_term_issues([markdown_file])

    assert issues == []
