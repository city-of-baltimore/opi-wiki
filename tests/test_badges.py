"""Tests for shared display badge helpers and macros."""

from __future__ import annotations

from pathlib import Path

import pytest
from main import DOCS_DIR, define_env
from scripts.repo_tools.badges import render_badge

REPO_ROOT = Path(__file__).resolve().parents[1]


class _FakePageFile:
    """Minimal file object for a fake MkDocs page."""

    def __init__(self, src_path: str) -> None:
        """Store the source path used by the macros plugin."""

        self.src_path = src_path


class _FakePage:
    """Minimal page object for a fake MkDocs page."""

    def __init__(self, src_path: str) -> None:
        """Create a fake page with the given source path."""

        self.file = _FakePageFile(src_path)


class FakeMacroEnvironment:
    """Minimal stand-in for the MkDocs macros environment."""

    def __init__(self, page_src_path: str) -> None:
        """Initialize the fake macro registry and current page."""

        self.macros: dict[str, object] = {}
        self.page = _FakePage(page_src_path)

    def macro(self, function: object) -> object:
        """Register a macro function and return it unchanged."""

        self.macros[getattr(function, "__name__", "unknown")] = function
        return function


def test_render_badge_uses_shared_label_and_variant_mapping() -> None:
    """Badge tokens should render through the shared mapping table."""

    assert render_badge("approved") == '<span class="opi-pill approved">Approved</span>'
    assert (
        render_badge("position-description")
        == '<span class="opi-pill internal">Position Description</span>'
    )


def test_render_badge_rejects_unknown_badge_tokens() -> None:
    """Unknown badge tokens should fail clearly for maintainers."""

    with pytest.raises(ValueError, match="Unknown display badge"):
        render_badge("retired")


def test_define_env_registers_badge_macros() -> None:
    """The macros module should expose both explicit and page-derived badges."""

    env = FakeMacroEnvironment("how-we-work/operations/charter-template.md")

    define_env(env)

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
        DOCS_DIR / "how-we-work/onboarding/maps-benefits-quick-guide.md",
        DOCS_DIR
        / "resources/reference/position-descriptions/directors-office/"
        "pd-project-manager.md",
    ]

    for markdown_file in badge_pages:
        text = markdown_file.read_text(encoding="utf-8")
        assert "{{ page_badge() }}" in text
