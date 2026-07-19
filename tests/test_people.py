"""Tests for the canonical people directory and its renderers."""

from __future__ import annotations

from pathlib import Path

import pytest
from main import DOCS_DIR, PEOPLE_DATA_PATH
from scripts.repo_tools.people import find_role_holder, load_people, render_people
from tests.helpers import register_macros

REPO_ROOT = Path(__file__).resolve().parents[1]


def _data() -> dict:
    return load_people(DOCS_DIR, PEOPLE_DATA_PATH)


def test_people_data_loads_cleanly() -> None:
    """The checked-in people directory should parse as a valid mapping."""

    data = _data()

    assert data["executive_director"]["name"] == "Dartanion Swift-Williams"
    assert len(data["portfolios"]) == 5
    assert [pf["key"] for pf in data["portfolios"]][0] == "directors-office"


def test_summary_counts_are_computed_from_the_directory() -> None:
    """The glance stats should be derived, not hard-coded."""

    summary = render_people(_data(), "summary")

    assert "| **Total positions** | 22 |" in summary
    assert "| **Filled** | 20 |" in summary
    assert "| **Open / unfilled** | 2 |" in summary


def test_pd_index_groups_the_inspector_under_performance() -> None:
    """The CitiStat Inspector sits on Performance even though the PD is filed elsewhere."""

    pd_index = render_people(_data(), "pd_index")

    performance = pd_index.split("### Performance", 1)[1].split("### ", 1)[0]
    assert "CitiStat Inspector" in performance
    # The Inspector must not appear under the Director's Office section.
    directors = pd_index.split("### Director's Office", 1)[1].split("### ", 1)[0]
    assert "CitiStat Inspector" not in directors


def test_pd_index_collapses_shared_position_descriptions() -> None:
    """The five CitiStat Analysts share one PD and appear once."""

    pd_index = render_people(_data(), "pd_index")

    assert pd_index.count("performance/pd-citistat-analyst.md") == 1


def test_roster_and_contractors_render_expected_people() -> None:
    """Staff appear in the team rosters and contractors in their own panel."""

    data = _data()
    roster = render_people(data, "roster")
    contractors = render_people(data, "contractors")

    assert "Rashaad Tillery" in roster
    assert "rashaad.tillery@baltimorecity.gov" in roster
    assert "Open — recruiting" in roster
    # Contractors are separated out and carry no PIN.
    assert "Daniel De Freitas" in contractors
    assert "Daniel De Freitas" not in roster
    assert "Byron Roelofsz" in contractors


def test_cost_centers_group_people_by_funding_line() -> None:
    """The cost-center view groups by cost center, not team."""

    cost_centers = render_people(_data(), "cost_centers")

    # The Data Storyteller sits in the Director's Office but is funded by the Lab.
    lab = cost_centers.split("**Innovation Lab**", 1)[1]
    assert "Audrey Randazzo" in lab.split("**", 1)[0]


def test_find_role_holder_returns_the_filled_incumbent() -> None:
    """Inline role lookups resolve to the current staff member."""

    data = _data()

    assert find_role_holder(data, "Innovation Program Manager") == "Gabriel Watson"
    assert find_role_holder(data, "Deputy Chief Data Officer") == "Jason Howard, PhD"
    assert (
        find_role_holder(data, "Executive Director and Chief Data Officer")
        == "Dartanion Swift-Williams"
    )


def test_find_role_holder_rejects_unknown_titles() -> None:
    """An unknown title should fail clearly rather than return an empty string."""

    with pytest.raises(ValueError, match="No filled role holder"):
        find_role_holder(_data(), "Chief Nonexistent Officer")


def test_render_people_rejects_unknown_sections() -> None:
    """Invalid section requests should fail clearly."""

    with pytest.raises(ValueError, match="Unknown people section"):
        render_people(_data(), "nope")


def test_people_macros_are_registered() -> None:
    """The MkDocs macros module should expose the people helpers."""

    env = register_macros("how-we-work/organization/team-and-roles/index.md")

    assert "people" in env.macros
    assert "role_holder" in env.macros
    assert env.macros["role_holder"]("Chief of Staff") == "Rakeim Young"
    assert "Leadership" in str(env.macros["people"]("roster"))


def test_roster_page_uses_shared_people_macros() -> None:
    """The Team & Roles page should not hand-maintain the roster tables."""

    page = REPO_ROOT / "docs/how-we-work/organization/team-and-roles/index.md"
    text = page.read_text(encoding="utf-8")

    assert '{{ people("roster") }}' in text
    assert '{{ people("summary") }}' in text
    assert '{{ people("contractors") }}' in text
    # The old hand-maintained PIN tables should be gone.
    assert "| **PIN** |" not in text
