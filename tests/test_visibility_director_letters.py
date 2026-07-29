"""Tests for scoped retired framing in director letters."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.visibility_labels import check_visibility_labels


def test_director_letter_labels_are_scoped_to_the_letter_section(tmp_path: Path) -> None:
    """Former letter framing must not police legitimate governance headings."""

    outside_path = tmp_path / "docs" / "data-governance.md"
    outside_text = "# Framework\n\n## Public Purpose\n\nA public letter may be a record.\n"
    letter_path = tmp_path / "docs" / "about-us" / "letters-from-the-director" / "example.md"

    assert (
        check_visibility_labels(
            outside_path,
            outside_text,
            repo_root=tmp_path,
        )
        == []
    )
    assert (
        check_visibility_labels(
            tmp_path / "docs" / "archive" / "letters-from-the-director-notes.md",
            outside_text,
            repo_root=tmp_path,
        )
        == []
    )
    assert check_visibility_labels(
        letter_path,
        outside_text,
        repo_root=tmp_path,
    ) == [
        "docs/about-us/letters-from-the-director/example.md:3:4: "
        "retired visibility label '## Public Purpose'; "
        "name the reader, review, or concrete data rule instead",
        "docs/about-us/letters-from-the-director/example.md:5:1: "
        "retired visibility label 'A public letter'; "
        "name the reader, review, or concrete data rule instead",
    ]


@pytest.mark.parametrize(
    "heading",
    (
        "# Public Purpose\n",
        " ## Public Purpose\n",
        "### Public Purpose ##\n",
        "###### Public Purpose\n",
        "## Public Purpose {#purpose}\n",
        "## Public Purpose {#purpose} ##\n",
        "## Public Purpose ## {#purpose}\n",
        "## **Public Purpose**\n",
        "## Public *Purpose*\n",
        "## [Public Purpose](#purpose)\n",
        "## Public Purpose:\n",
        "## Public Purpose\r\n",
        "Public Purpose\n===\n",
        "**Public Purpose**\n===\n",
        "Public Purpose {.summary}\n---\n",
        "Public Purpose\r\n===\r\n",
    ),
)
def test_director_letter_heading_syntax_cannot_restore_retired_framing(
    tmp_path: Path,
    heading: str,
) -> None:
    """Equivalent Markdown heading forms must share one semantic outcome."""

    path = tmp_path / "docs" / "about-us" / "letters-from-the-director" / "example.md"

    issues = check_visibility_labels(path, heading, repo_root=tmp_path)

    assert len(issues) == 1
    assert "Public Purpose" in issues[0]


@pytest.mark.parametrize(
    "text",
    (
        "A **public** letter.\n",
        "A _public_ letter.\n",
        "_A public letter_.\n",
    ),
)
def test_director_letter_labels_ignore_markdown_emphasis(
    tmp_path: Path,
    text: str,
) -> None:
    """Inline emphasis must not change the scoped director-letter meaning."""

    path = tmp_path / "docs" / "about-us" / "letters-from-the-director" / "example.md"

    issues = check_visibility_labels(path, text, repo_root=tmp_path)

    assert len(issues) == 1
    assert "A public letter" in issues[0]


def test_director_letter_heading_preserves_literal_identifier_underscores(
    tmp_path: Path,
) -> None:
    """An identifier-like underscore is not Markdown emphasis or retired framing."""

    path = tmp_path / "docs" / "about-us" / "letters-from-the-director" / "example.md"

    assert check_visibility_labels(path, "## Public_Purpose\n", repo_root=tmp_path) == []
