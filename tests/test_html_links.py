"""Tests for raw HTML link validation in Markdown sources."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.html_links import (
    candidate_paths,
    find_unresolved_html_links,
    is_external_link,
)


def test_external_schemes_and_anchors_are_excluded() -> None:
    """Only local hrefs should be resolved against the docs tree."""

    assert is_external_link("https://example.org")
    assert is_external_link("mailto:opi@baltimorecity.gov")
    assert is_external_link("#section")
    assert not is_external_link("../glossary.md")
    assert not is_external_link("team/")


def test_candidate_paths_cover_pretty_url_forms(tmp_path: Path) -> None:
    """Extension-less hrefs should try index.md and sibling .md forms."""

    source = tmp_path / "docs" / "section" / "page.md"

    candidates = candidate_paths(source, "../team/")

    names = {str(path.relative_to(tmp_path)) for path in candidates}
    assert "docs/team/index.md" in names
    assert "docs/team.md" in names


def test_unresolved_and_resolved_links_are_separated(tmp_path: Path) -> None:
    """Broken raw hrefs are reported with file and line; working ones are not."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "target.md").write_text("# Target\n", encoding="utf-8")
    (docs_dir / "page.md").write_text(
        '<a href="target.md">ok</a>\n<a href="missing.md">broken</a>\n',
        encoding="utf-8",
    )

    errors = find_unresolved_html_links(docs_dir)

    assert len(errors) == 1
    assert "page.md:2" in errors[0]
    assert "missing.md" in errors[0]
