"""Tests for format-aware authored-source normalization."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.source_semantics import (
    SemanticProjection,
    is_yaml_source,
    logical_line_break_count,
    normalize_source_text,
)


def test_logical_line_break_count_treats_crlf_as_one_break() -> None:
    """Every supported break should count once without doubling CRLF."""

    assert logical_line_break_count("a\r\nb\u2028c") == 2


def test_is_yaml_source_recognizes_suffixes_and_pages_files() -> None:
    """YAML-backed source types should share record semantics."""

    assert is_yaml_source(Path("config.yml"))
    assert is_yaml_source(Path("section/.pages"))
    assert not is_yaml_source(Path("guide.md"))


def test_normalize_source_text_joins_prose_but_separates_records() -> None:
    """Soft Markdown wrapping and structural YAML records need different outputs."""

    markdown, markdown_offsets = normalize_source_text(
        "public\nsite",
        path=Path("guide.md"),
    )
    yaml_text, yaml_offsets = normalize_source_text(
        "tier: public\nsite: opi",
        path=Path("config.yml"),
    )

    assert markdown == "public site"
    assert markdown_offsets[6] == 6
    assert "\N{SYMBOL FOR NULL}" in yaml_text
    assert len(yaml_text) == len(yaml_offsets)


def test_semantic_projection_rejects_mismatched_offsets() -> None:
    """A projection without exact evidence must fail at its construction seam."""

    try:
        SemanticProjection("text", (0,))
    except ValueError as error:
        assert str(error) == "semantic projection text and offset lengths differ"
    else:
        raise AssertionError("mismatched semantic projection was accepted")


def test_normalize_source_text_separates_either_side_of_a_heading() -> None:
    """A heading must not join semantically with preceding or following prose."""

    before, _before_offsets = normalize_source_text(
        "public\n# site\n",
        path=Path("guide.md"),
    )
    after, _after_offsets = normalize_source_text(
        "# public\nsite\n",
        path=Path("guide.md"),
    )

    assert "public site" not in before
    assert "public site" not in after
