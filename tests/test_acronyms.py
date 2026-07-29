"""Tests for authored Markdown acronym reporting."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.acronyms import acronym_report, load_acronym_allowlist


def test_acronym_report_respects_allowlist_expansion_headings_and_stopwords(
    tmp_path: Path,
) -> None:
    """Known, expanded, heading-only, and stopword tokens should not be reported."""

    page = tmp_path / "docs" / "page.md"
    text = (
        "# ABCD\n"
        "The XYZQ pipeline feeds OPI dashboards.\n"
        "We coordinate with the Department of General Services (DGSX).\n"
    )

    findings = acronym_report(page, text, allow={"OPI"}, repo_root=tmp_path)

    assert findings == [("docs/page.md", "XYZQ")]


def test_acronym_report_returns_no_findings_for_plain_copy(tmp_path: Path) -> None:
    """A page without unknown acronyms should produce no informational findings."""

    page = tmp_path / "docs" / "page.md"

    assert (
        acronym_report(
            page,
            "Plain site copy for everyone.",
            allow=set(),
            repo_root=tmp_path,
        )
        == []
    )


def test_allowlist_combines_curated_and_glossary_terms(tmp_path: Path) -> None:
    """The acronym allowlist should include built-ins and glossary terms."""

    docs_dir = tmp_path / "docs"
    glossary = docs_dir / "resources" / "reference" / "glossary.md"
    glossary.parent.mkdir(parents=True)
    glossary.write_text("# Glossary\n\nABCD is a fixture term.\n", encoding="utf-8")

    allow = load_acronym_allowlist(docs_dir)

    assert {"OPI", "ABCD"} <= allow


def test_allowlist_reports_an_unreadable_glossary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A glossary IO failure should become a contextual runtime error."""

    docs_dir = tmp_path / "docs"
    glossary = docs_dir / "resources" / "reference" / "glossary.md"
    glossary.parent.mkdir(parents=True)
    glossary.touch()
    original_read_text = Path.read_text

    def fail_glossary(path: Path, *, encoding: str) -> str:
        if path == glossary:
            raise OSError("read failed")
        return original_read_text(path, encoding=encoding)

    monkeypatch.setattr(Path, "read_text", fail_glossary)

    with pytest.raises(RuntimeError, match="Unable to read acronym glossary"):
        load_acronym_allowlist(docs_dir)
