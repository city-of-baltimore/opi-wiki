"""Tests for organization role lookup, CI adaptation, and MkDocs macros."""

from __future__ import annotations

from pathlib import Path

import pytest
from main import DOCS_DIR
from scripts.repo_tools.organization import (
    ORGANIZATION_DATA_PATH,
    find_organization_data_issues,
    find_role_holder,
    load_organization,
)
from tests.helpers import register_macros
from tests.organization_fixtures import (
    raw_organization_data,
    write_organization_data,
)


def test_find_role_holder_returns_the_filled_incumbent() -> None:
    """Inline role lookups resolve unique titles from the shared typed model."""

    structure = load_organization(DOCS_DIR, ORGANIZATION_DATA_PATH)

    assert find_role_holder(structure, "Innovation Program Manager") == "Gabriel Watson"
    assert find_role_holder(structure, "Deputy Chief Data Officer") == "Jason Howard, PhD"
    assert (
        find_role_holder(structure, "Executive Director and Chief Data Officer")
        == "Dartanion Swift-Williams"
    )


def test_find_role_holder_distinguishes_vacant_unknown_and_blank_titles() -> None:
    """Each lookup failure should tell an author which correction is needed."""

    structure = load_organization(DOCS_DIR, ORGANIZATION_DATA_PATH)

    with pytest.raises(ValueError, match="is vacant"):
        find_role_holder(structure, "Senior Performance Analyst")
    with pytest.raises(ValueError, match="Unknown organization role"):
        find_role_holder(structure, "Chief Nonexistent Officer")
    with pytest.raises(ValueError, match="must be a non-empty string"):
        find_role_holder(structure, " ")


def test_find_role_holder_rejects_ambiguous_filled_titles() -> None:
    """Repeated legitimate titles must never resolve by accidental source order."""

    structure = load_organization(DOCS_DIR, ORGANIZATION_DATA_PATH)

    with pytest.raises(ValueError, match="Multiple filled role holders") as error:
        find_role_holder(structure, "CitiStat Analyst")

    message = str(error.value)
    assert "Ethan Buckborough" in message
    assert "Griffin Riddler, PhD" in message


def test_organization_data_finder_reports_clean_and_invalid_sources(
    tmp_path: Path,
) -> None:
    """The CI adapter should report expected schema failures as findings."""

    assert find_organization_data_issues(DOCS_DIR) == []

    data = raw_organization_data()
    data["portfolios"][0]["staff"][0]["work_email"] = "example@baltimorecity.gov"
    write_organization_data(tmp_path, data)

    issues = find_organization_data_issues(tmp_path)

    assert len(issues) == 1
    assert "_data/people.yml.portfolios[0].staff[0]" in issues[0]
    assert "unsupported fields: work_email" in issues[0]


def test_organization_data_finder_surfaces_duplicate_key_and_line_numbers(
    tmp_path: Path,
) -> None:
    """Hosted CI should tell an author exactly which repeated field to repair."""

    data_path = tmp_path / ORGANIZATION_DATA_PATH
    data_path.parent.mkdir(parents=True)
    source = (DOCS_DIR / ORGANIZATION_DATA_PATH).read_text(encoding="utf-8")
    data_path.write_text(
        source.replace(
            "  title: Mayor\n",
            "  title: Mayor\n  title: Duplicate Mayor\n",
            1,
        ),
        encoding="utf-8",
    )

    issues = find_organization_data_issues(tmp_path)

    assert len(issues) == 1
    assert "Duplicate YAML key 'title' on lines" in issues[0]


def test_organization_data_finder_rejects_control_whitespace_before_build(
    tmp_path: Path,
) -> None:
    """Hosted CI must catch values the Markdown output boundary would reject."""

    data = raw_organization_data()
    data["portfolios"][0]["lead"]["summary"] = "Safe-looking\tindented text"
    write_organization_data(tmp_path, data)

    issues = find_organization_data_issues(tmp_path)

    assert len(issues) == 1
    assert "without control whitespace" in issues[0]


def test_both_macros_propagate_the_same_contract_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Org rendering and role lookup must fail through the same schema parser."""

    data = raw_organization_data()
    data["executive_director"]["employee_id"] = "12345"
    write_organization_data(tmp_path, data)
    monkeypatch.setattr("main.DOCS_DIR", tmp_path)
    env = register_macros()

    with pytest.raises(ValueError) as org_error:
        env.macros["org_structure"]("team_roles")
    with pytest.raises(ValueError) as role_error:
        env.macros["role_holder"]("Chief of Staff")

    assert str(org_error.value) == str(role_error.value)
    assert "unsupported fields: employee_id" in str(org_error.value)


def test_role_holder_macro_escapes_active_markdown_and_html(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A valid name remains inert text when the macro inserts it into Markdown."""

    data = raw_organization_data()
    data["portfolios"][0]["lead"]["name"] = (
        "<img src=x onerror=alert(1)> **Director** [link](javascript:alert(1))"
    )
    write_organization_data(tmp_path, data)
    monkeypatch.setattr("main.DOCS_DIR", tmp_path)
    env = register_macros()

    rendered = env.macros["role_holder"]("Chief of Staff")

    assert "<img" not in rendered
    assert "**Director**" not in rendered
    assert "[link](" not in rendered
    assert "&#60;img src&#61;x onerror&#61;alert&#40;1&#41;&#62;" in rendered
    assert "&#42;&#42;Director&#42;&#42;" in rendered
    assert "&#91;link&#93;&#40;javascript&#58;alert&#40;1&#41;&#41;" in rendered


def test_role_holder_macro_is_registered() -> None:
    """The macros module should expose only the typed role lookup, not raw data."""

    env = register_macros("how-we-work/organization/org-structure.md")

    assert "people" not in env.macros
    assert "role_holder" in env.macros
    assert env.macros["role_holder"]("Chief of Staff") == "Rakeim Young"
