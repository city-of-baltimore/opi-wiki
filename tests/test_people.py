"""Tests for the public people directory and role lookups."""

from __future__ import annotations

from pathlib import Path

import pytest
from main import DOCS_DIR, PEOPLE_DATA_PATH
from scripts.repo_tools.people import find_role_holder, load_people
from tests.helpers import register_macros


def _data() -> dict:
    return load_people(DOCS_DIR, PEOPLE_DATA_PATH)


def test_public_people_data_loads_cleanly() -> None:
    """The checked-in public organization directory should parse cleanly."""

    data = _data()

    assert data["executive_director"]["name"] == "Dartanion Swift-Williams"
    assert len(data["portfolios"]) == 4
    assert data["portfolios"][0]["key"] == "directors-office"


def test_people_data_rejects_legacy_pin_or_phone_fields(tmp_path: Path) -> None:
    """Private legacy fields must fail even when nested inside a staff record."""

    people_file = tmp_path / "people.yml"
    people_file.write_text(
        "portfolios:\n"
        "  - key: example\n"
        "    lead:\n"
        "      name: Example Person\n"
        "      title: Example Lead\n"
        "      phone: 410-555-0100\n"
        "    staff:\n"
        "      - name: Open\n"
        "        title: Example Role\n"
        "        PIN: '12345'\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match=r"fields forbidden from public people data: .*phone.*PIN",
    ):
        load_people(tmp_path, "people.yml")


def test_find_role_holder_returns_the_filled_incumbent() -> None:
    """Inline role lookups resolve to current public org-chart data."""

    data = _data()

    assert find_role_holder(data, "Innovation Program Manager") == "Gabriel Watson"
    assert find_role_holder(data, "Deputy Chief Data Officer") == "Jason Howard, PhD"
    assert (
        find_role_holder(data, "Executive Director and Chief Data Officer")
        == "Dartanion Swift-Williams"
    )


def test_find_role_holder_rejects_open_or_unknown_titles() -> None:
    """Unknown and unfilled titles should fail instead of exposing a placeholder."""

    with pytest.raises(ValueError, match="No filled role holder"):
        find_role_holder(_data(), "Senior Performance Analyst")
    with pytest.raises(ValueError, match="No filled role holder"):
        find_role_holder(_data(), "Chief Nonexistent Officer")


def test_role_holder_macro_is_registered() -> None:
    """The MkDocs macros module should expose only the needed role lookup."""

    env = register_macros("how-we-work/organization/org-structure.md")

    assert "people" not in env.macros
    assert "role_holder" in env.macros
    assert env.macros["role_holder"]("Chief of Staff") == "Rakeim Young"
