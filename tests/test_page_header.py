"""Tests for the shared page header helper and macro."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.page_header import render_page_header
from tests.helpers import register_macros

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_render_page_header_renders_eyebrow_summary_and_tagline() -> None:
    """A full header should render category, badge, summary, and tagline."""

    html = render_page_header(
        "draft",
        summary="What this page covers.",
        category="SERIES · OPI FOUNDATIONS",
        tagline="A supporting line.",
    )

    assert '<div class="opi-page-header">' in html
    assert '<span class="opi-page-header__category">SERIES · OPI FOUNDATIONS</span>' in html
    assert '<span class="opi-pill draft">Draft</span>' in html
    assert '<p class="opi-page-header__summary">What this page covers.</p>' in html
    assert '<p class="opi-page-header__tagline">A supporting line.</p>' in html


def test_render_page_header_omits_empty_optional_parts() -> None:
    """Empty optional fields should not emit category, summary, or tagline."""

    html = render_page_header("reference")

    assert "opi-page-header__category" not in html
    assert "opi-page-header__summary" not in html
    assert "opi-page-header__tagline" not in html
    assert '<span class="opi-pill neutral">Reference</span>' in html


def test_render_page_header_without_badge_omits_the_eyebrow() -> None:
    """Badges are opt-in: no badge and no category means no eyebrow row at all."""

    html = render_page_header(None, summary="Just a summary.")

    assert "opi-page-header__eyebrow" not in html
    assert "opi-pill" not in html
    assert '<p class="opi-page-header__summary">Just a summary.</p>' in html


def test_render_page_header_escapes_text() -> None:
    """Author-supplied text should be HTML-escaped."""

    html = render_page_header("draft", summary="A & B <c>")

    assert "A &amp; B &lt;c&gt;" in html
    assert "<c>" not in html


def test_page_header_macro_resolves_badge_from_metadata() -> None:
    """The macro should pull the badge token from inherited page metadata."""

    env = register_macros("resources/reference/position-descriptions/index.md")

    rendered = str(env.macros["page_header"](summary="How charters work."))

    assert '<span class="opi-pill neutral">Reference</span>' in rendered
    assert '<p class="opi-page-header__summary">How charters work.</p>' in rendered


def test_pages_do_not_duplicate_title_as_bold_paragraph() -> None:
    """Migrated pages should not restate their H1 as a bold paragraph."""

    for markdown_file in sorted((REPO_ROOT / "docs").rglob("*.md")):
        lines = markdown_file.read_text(encoding="utf-8").splitlines()
        title = next((line[2:].strip() for line in lines if line.startswith("# ")), None)
        if not title:
            continue
        assert f"**{title}**" not in lines, (
            f"{markdown_file} restates its title as a bold paragraph."
        )
