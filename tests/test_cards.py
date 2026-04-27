"""Tests for shared card-grid data and macro rendering."""

from __future__ import annotations

from pathlib import Path

import pytest
from main import DOCS_DIR, define_env
from scripts.repo_tools.cards import load_card_sections, render_card_grid

REPO_ROOT = Path(__file__).resolve().parents[1]


class FakeMacroEnvironment:
    """Minimal stand-in for the MkDocs macros environment."""

    def __init__(self) -> None:
        """Initialize the fake macro registry."""

        self.macros: dict[str, object] = {}

    def macro(self, function: object) -> object:
        """Register a macro function and return it unchanged."""

        self.macros[getattr(function, "__name__", "unknown")] = function
        return function


def test_card_renderer_supports_linked_and_non_linked_cards(tmp_path: Path) -> None:
    """Shared card rendering should cover linked and informational cards."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    data_file = docs_dir / "sample.cards.yml"
    data_file.write_text(
        "- meta: Linked\n"
        "  title: First card\n"
        "  body: Has a destination.\n"
        "  href: /first/\n"
        "- meta: Informational\n"
        "  title: Second card\n"
        "  body: No destination.\n",
        encoding="utf-8",
    )

    sections = load_card_sections(docs_dir, "sample.cards.yml")
    html = render_card_grid(sections["default"])

    assert 'class="opi-card-link"' in html
    assert 'href="/first/"' in html
    assert 'class="opi-card-copy"' in html
    assert "No destination." in html


def test_define_env_registers_card_grid_macro() -> None:
    """The MkDocs macros module should expose the shared card-grid helper."""

    env = FakeMacroEnvironment()

    define_env(env)

    macro = env.macros["card_grid_from"]
    rendered = macro("index.cards.yml")

    assert 'class="opi-card-grid"' in str(rendered)
    assert "What OPI is and why it exists" in str(rendered)


def test_card_loader_rejects_non_mapping_card_entries(tmp_path: Path) -> None:
    """Card data should fail clearly when a list item is not a mapping."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    data_file = docs_dir / "broken.cards.yml"
    data_file.write_text("- just text\n", encoding="utf-8")

    with pytest.raises(ValueError, match="must be a mapping"):
        load_card_sections(docs_dir, "broken.cards.yml")


def test_all_card_data_files_load_cleanly() -> None:
    """All checked-in card data files should parse as valid shared card sections."""

    data_files = sorted(DOCS_DIR.rglob("*.cards.yml"))

    assert data_files
    for data_file in data_files:
        sections = load_card_sections(DOCS_DIR, str(data_file.relative_to(DOCS_DIR)))
        assert sections


def test_markdown_pages_do_not_inline_card_grid_markup() -> None:
    """Landing-page card markup should come from shared data, not repeated HTML."""

    for markdown_file in sorted((REPO_ROOT / "docs").rglob("*.md")):
        text = markdown_file.read_text(encoding="utf-8")
        assert '<div class="opi-card-grid">' not in text, (
            f"{markdown_file} still inlines shared card-grid HTML."
        )
        assert 'class="opi-card-link"' not in text, (
            f"{markdown_file} still inlines shared card-link HTML."
        )
