"""Tests for shared org-structure data and rendering."""

from __future__ import annotations

from pathlib import Path

import pytest
from main import DOCS_DIR
from scripts.repo_tools.org_structure import load_org_structure, render_org_structure
from tests.helpers import register_macros

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_org_structure_data_loads_cleanly() -> None:
    """The checked-in org-structure data file should parse as valid structured data."""

    structure = load_org_structure(DOCS_DIR, "_data/people.yml")

    assert structure.city_administrator.name == "Faith P. Leach"
    assert len(structure.portfolios) == 5
    assert structure.portfolios[-1].leadership_edge_style == "solid"
    assert structure.portfolios[-1].lead.name == "Ifeanyi Akila"
    assert structure.portfolios[-1].lead.worker_type == "contractor"
    assert structure.portfolios[3].lead.name == "Gabriel Watson"


def test_org_structure_renderer_covers_chart_table_and_roster_sections() -> None:
    """The renderer should emit the major repeated org-structure sections."""

    structure = load_org_structure(DOCS_DIR, "_data/people.yml")

    leadership_chart = render_org_structure(structure, "leadership_chart")
    portfolio_table = render_org_structure(structure, "portfolio_table")
    staff_alignment = render_org_structure(structure, "staff_alignment")

    assert "ED --> IL" in leadership_chart
    assert "Director's Office" in leadership_chart
    assert "Director&#x27;s Office" not in leadership_chart
    assert "Gabriel Watson<br/>Innovation Program Manager" in leadership_chart
    assert "| Director's Office | Rakeim Young, Chief of Staff | AdminOps |" in portfolio_table
    assert "- Audrey Randazzo — Data Storyteller" in staff_alignment
    assert "- Gabriel Watson — Innovation Program Manager" in staff_alignment
    assert "- Ifeanyi Akila — AI Enablement Lead (Contractor)" in staff_alignment
    assert "- Byron Roelofsz — Product Lead (Contractor · offshore)" in staff_alignment
    assert "cross-portfolio model" not in staff_alignment


def test_org_structure_marks_contractors_in_chart_and_roster() -> None:
    """Contractors should be color-coded on the chart and tagged in the roster."""

    structure = load_org_structure(DOCS_DIR, "_data/people.yml")

    leadership_chart = render_org_structure(structure, "leadership_chart")
    cards = render_org_structure(structure, "staff_cards")

    assert "classDef contractor" in leadership_chart
    assert "classDef offshore" in leadership_chart
    # The AI Enablement branch lead is an onshore contractor.
    assert ":::contractor" in leadership_chart
    # Offshore BIC members are color-coded on the roster cards.
    assert "opi-org-card--offshore" in cards
    assert "opi-org-card--contractor" in cards
    # Leads render as the full-width gold card; vacant seats render dashed.
    assert "opi-org-card--lead" in cards
    assert "opi-org-card--open" in cards


def test_define_env_registers_org_structure_macro() -> None:
    """The MkDocs macros module should expose the shared org-structure helper."""

    env = register_macros()

    rendered = env.macros["org_structure_from"](
        "_data/people.yml",
        "staff_cards",
    )

    assert '=== "Director\'s Office"' in str(rendered)
    assert '<span class="opi-org-card__name">Rakeim Young</span>' in str(rendered)


def test_org_structure_renderer_rejects_unknown_sections() -> None:
    """Invalid render-section requests should fail clearly."""

    structure = load_org_structure(DOCS_DIR, "_data/people.yml")

    with pytest.raises(ValueError, match="Unknown org-structure section"):
        render_org_structure(structure, "unknown")


def test_org_structure_page_uses_shared_data_macros() -> None:
    """The org-structure page should not hand-maintain repeated chart blocks."""

    org_page = REPO_ROOT / "docs/how-we-work/organization/org-structure.md"
    text = org_page.read_text(encoding="utf-8")

    assert 'org_structure_from("_data/people.yml"' in text
    assert "```mermaid" not in text
