"""Tests for raw HTML link validation in Markdown sources."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.repo_tools.html_links as html_links
from scripts.check_html_links import main
from scripts.repo_tools.html_links import (
    candidate_paths,
    extract_html_links,
    find_unresolved_html_links,
    is_external_link,
)


def test_external_schemes_and_anchors_are_excluded() -> None:
    """Only local hrefs should be resolved against the docs tree."""

    assert is_external_link("https://example.org")
    assert is_external_link("mailto:opi@baltimorecity.gov")
    assert is_external_link("//cdn.example.org/logo.svg")
    assert is_external_link("#section")
    assert is_external_link("?view=compact")
    assert is_external_link("")
    assert not is_external_link("../glossary.md")
    assert not is_external_link("team/")


def test_candidate_paths_cover_pretty_url_forms(tmp_path: Path) -> None:
    """Extension-less hrefs should try index.md and sibling .md forms."""

    source = tmp_path / "docs" / "section" / "page.md"

    candidates = candidate_paths(source, "../team/")

    names = {str(path.relative_to(tmp_path)) for path in candidates}
    assert "docs/team/index.md" in names
    assert "docs/team.md" in names

    file_candidate = candidate_paths(source, "../target.pdf")
    assert file_candidate == [(tmp_path / "docs" / "target.pdf").resolve()]


def test_html_parser_supports_single_quotes_unquoted_values_and_multiline_tags() -> None:
    """HTML-valid attribute syntax must not bypass raw-link validation."""

    links = extract_html_links(
        "<a href='single.md'>one</a>\n"
        "<a href=unquoted.md>two</a>\n"
        "<a\n  class='card'\n  href=\"multiline.md\">three</a>\n"
    )

    assert [(link.href, link.line_number) for link in links] == [
        ("single.md", 1),
        ("unquoted.md", 2),
        ("multiline.md", 3),
    ]


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


def test_single_quoted_broken_link_is_reported(tmp_path: Path) -> None:
    """A single-quoted href should receive the same validation as double quotes."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "page.md").write_text("<a href='missing.md'>broken</a>\n", encoding="utf-8")

    errors = find_unresolved_html_links(docs_dir)

    assert len(errors) == 1
    assert "missing.md" in errors[0]


def test_link_escaping_docs_is_rejected_even_when_target_exists(tmp_path: Path) -> None:
    """Raw links may not publish or validate files outside docs/."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (tmp_path / "private.md").write_text("private\n", encoding="utf-8")
    (docs_dir / "page.md").write_text(
        '<a href="../private.md">private</a>\n',
        encoding="utf-8",
    )

    errors = find_unresolved_html_links(docs_dir)

    assert len(errors) == 1
    assert "escapes docs/" in errors[0]


def test_root_relative_link_resolves_from_docs_root(tmp_path: Path) -> None:
    """A leading slash denotes the publish root, not the host filesystem root."""

    docs_dir = tmp_path / "docs"
    section_dir = docs_dir / "section"
    section_dir.mkdir(parents=True)
    (docs_dir / "target.md").write_text("# Target\n", encoding="utf-8")
    (section_dir / "page.md").write_text('<a href="/target.md">target</a>\n', encoding="utf-8")

    assert find_unresolved_html_links(docs_dir) == []


def test_unreadable_markdown_source_raises_a_contextual_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A source IO failure should name the affected Markdown file."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    markdown_file = docs_dir / "page.md"
    markdown_file.write_text("# Page\n", encoding="utf-8")

    def fail_read(path: Path, *, encoding: str) -> str:
        assert path == markdown_file
        assert encoding == "utf-8"
        raise OSError("read failed")

    monkeypatch.setattr(Path, "read_text", fail_read)

    with pytest.raises(RuntimeError, match=r"Unable to read Markdown file: .*page\.md"):
        find_unresolved_html_links(docs_dir)


def test_html_link_cli_reports_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The raw-link CLI should return success for a clean scan."""

    monkeypatch.setattr(html_links, "find_unresolved_html_links", lambda _docs: [])

    assert main() == 0
    assert capsys.readouterr().out == "Raw HTML links validated.\n"


def test_html_link_cli_reports_validator_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Unexpected validator errors should become a concise CLI failure."""

    def fail_validation(_docs: Path) -> list[str]:
        raise RuntimeError("read failed")

    monkeypatch.setattr(html_links, "find_unresolved_html_links", fail_validation)

    assert main() == 1
    assert capsys.readouterr().err == (
        "Raw HTML link validation failed unexpectedly: read failed\n"
    )
