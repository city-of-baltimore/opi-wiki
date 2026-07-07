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
    assert (
        render_badge("position-description")
        == '<span class="opi-pill internal">Position Description</span>'
    )


def test_render_badge_rejects_unknown_badge_tokens() -> None:
    """Unknown badge tokens should fail clearly for maintainers."""

    with pytest.raises(ValueError, match="Unknown display badge"):
        render_badge("retired")


def test_approved_badge_token_is_retired() -> None:
    """The blanket 'approved' badge was removed; the token must stay invalid."""

    with pytest.raises(ValueError, match="Unknown display badge"):
        render_badge("approved")


def test_define_env_registers_badge_macros() -> None:
    """The macros module should expose both explicit and page-derived badges."""

    env = register_macros("how-we-work/handbook/operations/charter-template.md")

    assert str(env.macros["badge"]("reference")) == (
        '<span class="opi-pill internal">Reference</span>'
    )
    assert str(env.macros["page_badge"]()) == (
        '<span class="opi-pill internal">Template</span>'
    )


def test_markdown_pages_do_not_inline_raw_pill_markup() -> None:
    """Display badges should come from shared macros, not repeated raw HTML."""

    for markdown_file in sorted((REPO_ROOT / "docs").rglob("*.md")):
        text = markdown_file.read_text(encoding="utf-8")
        assert '<span class="opi-pill ' not in text, (
            f"{markdown_file} still inlines raw badge HTML."
        )


def test_badge_pages_retain_metadata_backing() -> None:
    """Checked-in docs should keep badge-bearing pages wired to metadata-driven badges."""

    badge_pages = [
        DOCS_DIR / "resources/reference/wiki-knowledge-base-structure.md",
        DOCS_DIR / "how-we-work/handbook/onboarding/maps-benefits-quick-guide.md",
        DOCS_DIR
        / "resources/reference/position-descriptions/directors-office/"
        "pd-project-manager.md",
    ]

    for markdown_file in badge_pages:
        text = markdown_file.read_text(encoding="utf-8")
        assert "{{ page_header(" in text
