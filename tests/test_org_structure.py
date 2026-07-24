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


def test_leadership_chart_is_the_reporting_spine_only() -> None:
    """The chart is City Administrator -> Executive Director; teams live in a table."""

    structure = load_org_structure(DOCS_DIR, "_data/people.yml")
    chart = render_org_structure(structure, "leadership_chart")

    assert chart.startswith('<figure class="opi-org-chart"')
    assert chart.count('data-org-level="city"') == 1
    assert chart.count('data-org-level="executive"') == 1
    assert "Faith P. Leach" in chart
    assert "Dartanion Swift-Williams" in chart
    # Teams, staff, and contractors are not chart nodes here.
    assert 'data-org-level="team"' not in chart
    assert 'data-org-level="report"' not in chart
    assert "Gabriel Watson" not in chart
    assert "```mermaid" not in chart


def test_team_reports_table_lists_each_lead_and_their_reports() -> None:
    """The team_reports table pairs every team lead with their direct reports."""

    structure = load_org_structure(DOCS_DIR, "_data/people.yml")
    table = render_org_structure(structure, "team_reports_table")
    portfolio_table = render_org_structure(structure, "portfolio_table")

    assert table.startswith("| **Team** | **Lead** | **Reports** |")
    assert "| Director's Office | Rakeim Young, Chief of Staff | Roberto Herbruger" in table
    assert "Xander Jake de los Santos" in table
    # Open roles show their title marked open; contractors never appear.
    assert "Senior Performance Analyst (open)" in table
    assert "| Open |" not in table
    assert "Byron Roelofsz" not in table
    assert "Sand Technologies" not in table
    assert "| Director's Office | Rakeim Young, Chief of Staff |" in portfolio_table
    assert "Cost Center" not in portfolio_table


def test_team_roles_table_lists_people_with_role_summaries() -> None:
    """The team_roles view is one table per team: name, title, and what the role does."""

    structure = load_org_structure(DOCS_DIR, "_data/people.yml")
    roles = render_org_structure(structure, "team_roles")

    # The Executive Director leads a group of one, headed by the role title
    # (not "Office of the Executive Director", which reads as an office of one).
    assert roles.startswith("## Executive Director and Chief Data Officer")
    assert "## Office of the Executive Director" not in roles
    assert "| Dartanion Swift-Williams | Executive Director and Chief Data Officer |" in roles
    assert "## Director's Office" in roles
    assert "| Name | Title | What the role does |" in roles
    assert "| Rashaad Tillery | CitiStat Inspector |" in roles
    assert "| Open | Senior Performance Analyst |" in roles
    assert "Byron Roelofsz" not in roles


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
