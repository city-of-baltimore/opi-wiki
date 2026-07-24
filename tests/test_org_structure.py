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
    assert len(structure.portfolios) == 4
    assert structure.portfolios[3].lead.name == "Gabriel Watson"


def test_org_structure_renderer_covers_public_chart_and_team_table() -> None:
    """The renderer should emit only the public leadership and team views."""

    structure = load_org_structure(DOCS_DIR, "_data/people.yml")

    leadership_chart = render_org_structure(structure, "leadership_chart")
    portfolio_table = render_org_structure(structure, "portfolio_table")

    assert leadership_chart.startswith('<figure class="opi-org-chart"')
    assert 'data-org-level="city"' in leadership_chart
    assert 'data-org-level="executive"' in leadership_chart
    assert leadership_chart.count('data-org-level="team"') == 4
    assert 'data-org-key="innovation-lab"' in leadership_chart
    assert "Director&#x27;s Office" in leadership_chart
    assert "Gabriel Watson" in leadership_chart
    assert "Innovation Program Manager" in leadership_chart
    assert "```mermaid" not in leadership_chart
    assert "| Director's Office | Rakeim Young, Chief of Staff |" in portfolio_table
    assert "Cost Center" not in portfolio_table
    assert "Ifeanyi Akila" not in leadership_chart


def test_define_env_registers_org_structure_macro() -> None:
    """The MkDocs macros module should expose the shared org-structure helper."""

    env = register_macros()

    rendered = env.macros["org_structure_from"](
        "_data/people.yml",
        "portfolio_table",
    )

    assert "| Director's Office | Rakeim Young, Chief of Staff |" in str(rendered)


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
