"""Tests for metadata sidecar resolution."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.metadata import find_metadata_issues, resolve_page_metadata


def test_metadata_resolution_inherits_defaults_and_page_overrides(tmp_path: Path) -> None:
    """A page should inherit metadata from ancestor sidecars."""

    docs_dir = tmp_path / "docs"
    section_dir = docs_dir / "section"
    section_dir.mkdir(parents=True)

    (docs_dir / ".metadata.yml").write_text(
        "defaults:\n"
        "  owner: OPI Director's Office\n"
        "  status: approved\n"
        "  last_reviewed: 2026-04-15\n"
        "  next_review: 2026-07-15\n"
        "  change_log: Root default.\n",
        encoding="utf-8",
    )
    (section_dir / ".metadata.yml").write_text(
        "pages:\n"
        "  page.md:\n"
        "    owner: Chief of Staff\n",
        encoding="utf-8",
    )
    page = section_dir / "page.md"
    page.write_text("# Page\n", encoding="utf-8")

    metadata = resolve_page_metadata(docs_dir, page)

    assert metadata["owner"] == "Chief of Staff"
    assert metadata["status"] == "approved"
    assert metadata["change_log"] == "Root default."


def test_metadata_validator_reports_missing_fields(tmp_path: Path) -> None:
    """Pages missing required metadata should be reported."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "page.md").write_text("# Page\n", encoding="utf-8")

    issues = find_metadata_issues(docs_dir)

    assert len(issues) == 1
    assert "missing metadata fields" in issues[0]
