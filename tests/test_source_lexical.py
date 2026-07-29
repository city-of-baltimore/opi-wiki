"""Tests for the bounded source-only lexical projection."""

from __future__ import annotations

import pytest
from scripts.repo_tools.source_lexical import source_lexical_projection
from scripts.repo_tools.source_semantics import PARAGRAPH_BOUNDARY


@pytest.mark.parametrize(
    ("source", "expected"),
    (
        ("public **site**", "public site"),
        ("*public* site", "public site"),
        ("internal [documentation](guide.md)", "internal documentation"),
        ("approved <em>version</em>", "approved version"),
        ("public&nbsp;site", "public\u00a0site"),
        ("public<br>site", "public site"),
    ),
)
def test_source_lexical_projection_exposes_bounded_inline_prose(
    source: str,
    expected: str,
) -> None:
    """Supported source-only syntax should retain text and exact offsets."""

    projection = source_lexical_projection(source)

    assert projection.text == expected
    assert len(projection.text) == len(projection.raw_offsets)
    assert source[projection.raw_offsets[0]].casefold() == expected[0].casefold()


@pytest.mark.parametrize(
    "source",
    (
        r"public \*\*site\*\*",
        "[guide](public-site)",
        "Public_Purpose",
        "public_*facing*",
    ),
)
def test_source_lexical_projection_preserves_literal_or_destination_syntax(
    source: str,
) -> None:
    """Escapes, identifiers, and link destinations must not become prose."""

    assert "public site" not in source_lexical_projection(source).text.casefold()


def test_source_lexical_projection_keeps_block_boundaries() -> None:
    """HTML blocks must not form a synthetic cross-block phrase."""

    projection = source_lexical_projection("<h2>Public</h2><p>site</p>")

    assert PARAGRAPH_BOUNDARY in projection.text
    assert "public site" not in projection.text.casefold()


def test_source_lexical_projection_rejects_nontext_input() -> None:
    """The lexical boundary should fail explicitly for an invalid caller value."""

    with pytest.raises(TypeError, match="requires text"):
        source_lexical_projection(None)  # type: ignore[arg-type]
