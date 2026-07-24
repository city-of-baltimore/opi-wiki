"""Tests for shared display badge helpers and macros."""

from __future__ import annotations

from pathlib import Path

import pytest
from main import DOCS_DIR
from scripts.repo_tools.badges import render_badge
from tests.helpers import register_macros

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_render_badge_uses_shared_label_and_variant_mapping() -> None:
    """Badge tokens should render through the shared mapping table."""

    assert render_badge("draft") == '<span class="opi-pill draft">Draft</span>'
    assert render_badge("reference") == ('<span class="opi-pill neutral">Reference</span>')


def test_render_badge_rejects_unknown_badge_tokens() -> None:
    """Unknown badge tokens should fail clearly for maintainers."""

    with pytest.raises(ValueError, match="Unknown display badge"):
        render_badge("retired")


def test_approved_badge_token_is_retired() -> None:
    """The blanket 'approved' badge was removed; the token must stay invalid."""

    with pytest.raises(ValueError, match="Unknown display badge"):
        render_badge("approved")


def test_define_env_registers_explicit_badge_macro() -> None:
    """The macros module should expose the supported inline badge helper."""

    env = register_macros("resources/reference/glossary.md")

    assert str(env.macros["badge"]("reference")) == (
        '<span class="opi-pill neutral">Reference</span>'
    )
    assert "page_badge" not in env.macros


def test_markdown_pages_do_not_inline_raw_pill_markup() -> None:
    """Display badges should come from shared macros, not repeated raw HTML."""

    for markdown_file in sorted((REPO_ROOT / "docs").rglob("*.md")):
        text = markdown_file.read_text(encoding="utf-8")
        assert '<span class="opi-pill ' not in text, (
            f"{markdown_file} still inlines raw badge HTML."
        )


def test_badge_page_retains_metadata_backing() -> None:
    """The checked-in reference pages should stay wired to metadata-driven badges."""

    badge_pages = [
        DOCS_DIR / "resources/reference/glossary.md",
    ]

    for markdown_file in badge_pages:
        text = markdown_file.read_text(encoding="utf-8")
        assert "{{ page_header(" in text
