"""Tests for shared org-structure data and rendering."""

from __future__ import annotations

from pathlib import Path

import pytest
from main import DOCS_DIR, define_env
from scripts.repo_tools.org_structure import load_org_structure, render_org_structure

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


def test_org_structure_data_loads_cleanly() -> None:
    """The checked-in org-structure data file should parse as valid structured data."""

    structure = load_org_structure(DOCS_DIR, "about-us/about-opi/org-structure.data.yml")

    assert structure.city_administrator.name == "Faith P. Leach"
    assert len(structure.portfolios) == 4
    assert structure.portfolios[-1].leadership_edge_style == "dotted"


def test_org_structure_renderer_covers_chart_table_and_roster_sections() -> None:
    """The renderer should emit the major repeated org-structure sections."""

    structure = load_org_structure(DOCS_DIR, "about-us/about-opi/org-structure.data.yml")

    leadership_chart = render_org_structure(structure, "leadership_chart")
    portfolio_table = render_org_structure(structure, "portfolio_table")
    staff_alignment = render_org_structure(structure, "staff_alignment")

    assert "ED -. interim oversight .-> IL" in leadership_chart
    assert "| Director's Office | Rakeim Young, Chief of Staff | AdminOps |" in portfolio_table
    assert "- Mallory Screws — Project Manager" in staff_alignment
    assert (
        "Innovation work is currently supported through a cross-portfolio model"
        in staff_alignment
    )


def test_define_env_registers_org_structure_macro() -> None:
    """The MkDocs macros module should expose the shared org-structure helper."""

    env = FakeMacroEnvironment()

    define_env(env)

    rendered = env.macros["org_structure_from"](
        "about-us/about-opi/org-structure.data.yml",
        "portfolio_tabs",
    )

    assert '=== "Director\'s Office"' in str(rendered)
    assert "Rakeim Young&lt;br/&gt;Chief of Staff" not in str(rendered)
    assert 'Rakeim Young<br/>Chief of Staff' in str(rendered)


def test_org_structure_renderer_rejects_unknown_sections() -> None:
    """Invalid render-section requests should fail clearly."""

    structure = load_org_structure(DOCS_DIR, "about-us/about-opi/org-structure.data.yml")

    with pytest.raises(ValueError, match="Unknown org-structure section"):
        render_org_structure(structure, "unknown")


def test_org_structure_page_uses_shared_data_macros() -> None:
    """The org-structure page should not hand-maintain repeated chart blocks."""

    org_page = REPO_ROOT / "docs/about-us/about-opi/org-structure.md"
    text = org_page.read_text(encoding="utf-8")

    assert 'org_structure_from("about-us/about-opi/org-structure.data.yml"' in text
    assert "```mermaid" not in text
