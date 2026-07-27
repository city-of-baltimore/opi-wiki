"""Tests for the canonical organization-data schema."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from main import DOCS_DIR
from scripts.repo_tools.organization import ORGANIZATION_DATA_PATH, load_organization
from tests import organization_fixtures as fixtures


def test_checked_in_organization_data_satisfies_the_contract() -> None:
    """The real source should produce the exact immutable four-team model."""

    structure = load_organization(DOCS_DIR, ORGANIZATION_DATA_PATH)

    assert structure.mayor.name == "Brandon M. Scott"
    assert structure.city_administrator.name == "Faith P. Leach"
    assert structure.executive_director.name == "Dartanion Swift-Williams"
    assert isinstance(structure.portfolios, tuple)
    assert tuple(portfolio.key for portfolio in structure.portfolios) == (
        "directors-office",
        "performance",
        "data-and-analytics",
        "innovation-lab",
    )
    assert isinstance(structure.portfolios[0].staff, tuple)
    assert structure.portfolios[0].label == "Director's Office"
    assert (
        structure.portfolios[0].primary_value
        == "Keeps work prioritized, documented, communicated, and deliverable."
    )
    assert "table_lead" not in fixtures.raw_organization_data()["portfolios"][0]
    assert "label" not in fixtures.raw_organization_data()["portfolios"][0]


@pytest.mark.parametrize(
    ("location", "field", "expected_path"),
    [
        ("root", "work_email", "_data/people.yml"),
        ("mayor", "employee_id", "_data/people.yml.mayor"),
        ("portfolio", "label", r"_data/people.yml.portfolios\[0\]"),
        ("portfolio", "phone", r"_data/people.yml.portfolios\[0\]"),
        ("lead", "email", r"_data/people.yml.portfolios\[0\].lead"),
        ("staff", "reports_to", r"_data/people.yml.portfolios\[0\].staff\[0\]"),
    ],
)
def test_organization_rejects_unknown_fields_at_every_schema_boundary(
    tmp_path: Path,
    location: str,
    field: str,
    expected_path: str,
) -> None:
    """Unknown data must fail at its exact path instead of being ignored."""

    data = fixtures.raw_organization_data()
    fixtures.organization_mapping_at(data, location)[field] = "not allowed"

    with pytest.raises(
        ValueError,
        match=rf"{expected_path}: unsupported fields: {field}",
    ):
        fixtures.load_organization_fixture(tmp_path, data)


@pytest.mark.parametrize("location", ["root", "mayor", "portfolio", "lead", "staff"])
def test_organization_rejects_non_mapping_nodes(
    tmp_path: Path,
    location: str,
) -> None:
    """Every record-shaped node must be a mapping, with no silent coercion."""

    data = fixtures.replace_organization_node(
        fixtures.raw_organization_data(), location, "not a mapping"
    )

    with pytest.raises(ValueError, match="must be a mapping"):
        fixtures.load_organization_fixture(tmp_path, data)


@pytest.mark.parametrize("value", [None, "staff", 0, {"name": "Example"}])
def test_organization_rejects_non_list_staff(
    tmp_path: Path,
    value: Any,
) -> None:
    """An explicitly present staff collection must always be a YAML list."""

    data = fixtures.raw_organization_data()
    data["portfolios"][0]["staff"] = value

    with pytest.raises(
        ValueError,
        match=r"_data/people.yml.portfolios\[0\].staff: must be a list",
    ):
        fixtures.load_organization_fixture(tmp_path, data)


@pytest.mark.parametrize("value", [None, "portfolios", 0, {"key": "performance"}])
def test_organization_rejects_non_list_portfolios(
    tmp_path: Path,
    value: Any,
) -> None:
    """The portfolio collection must be a list, not a falsey stand-in."""

    data = fixtures.raw_organization_data()
    data["portfolios"] = value

    with pytest.raises(
        ValueError,
        match=r"_data/people.yml.portfolios: must be a list",
    ):
        fixtures.load_organization_fixture(tmp_path, data)


def test_organization_rejects_an_empty_portfolio_list(tmp_path: Path) -> None:
    """The source must always define the teams consumed by the fixed renderer."""

    data = fixtures.raw_organization_data()
    data["portfolios"] = []

    with pytest.raises(ValueError, match="must be a non-empty list"):
        fixtures.load_organization_fixture(tmp_path, data)


@pytest.mark.parametrize(
    ("location", "field", "value"),
    [
        ("mayor", "name", 123),
        ("executive_director", "summary", False),
        ("portfolio", "key", ["directors-office"]),
        ("portfolio", "primary_value", {"text": "value"}),
        ("lead", "title", None),
        ("staff", "summary", True),
    ],
)
def test_organization_rejects_non_string_text_fields(
    tmp_path: Path,
    location: str,
    field: str,
    value: Any,
) -> None:
    """YAML-native numbers, booleans, and collections must never become display text."""

    data = fixtures.raw_organization_data()
    fixtures.organization_mapping_at(data, location)[field] = value

    with pytest.raises(ValueError, match=rf"\.{field}: must be a non-empty string"):
        fixtures.load_organization_fixture(tmp_path, data)


@pytest.mark.parametrize("value", ["", "   "])
def test_organization_rejects_blank_required_text(
    tmp_path: Path,
    value: str,
) -> None:
    """Required text cannot collapse to an empty rendered value."""

    data = fixtures.raw_organization_data()
    data["portfolios"][0]["lead"]["summary"] = value

    with pytest.raises(ValueError, match=r"\.lead\.summary: must be a non-empty string"):
        fixtures.load_organization_fixture(tmp_path, data)


@pytest.mark.parametrize(
    "value",
    [
        "First line\nSecond line",
        "Text\tindented",
        "Text\fpage break",
        "Text\vvertical break",
    ],
)
def test_organization_rejects_structural_whitespace(
    tmp_path: Path,
    value: str,
) -> None:
    """Display fields remain one-line records rather than embedded structures."""

    data = fixtures.raw_organization_data()
    data["portfolios"][0]["lead"]["summary"] = value

    with pytest.raises(ValueError, match="must be single-line plain text"):
        fixtures.load_organization_fixture(tmp_path, data)


@pytest.mark.parametrize(
    ("location", "field"),
    [
        ("root", "mayor"),
        ("root", "city_administrator"),
        ("root", "executive_director"),
        ("root", "portfolios"),
        ("portfolio", "key"),
        ("portfolio", "lead"),
        ("portfolio", "primary_value"),
        ("portfolio", "staff"),
        ("mayor", "name"),
        ("mayor", "title"),
        ("executive_director", "summary"),
        ("lead", "summary"),
        ("staff", "summary"),
    ],
)
def test_organization_rejects_missing_required_fields(
    tmp_path: Path,
    location: str,
    field: str,
) -> None:
    """Required fields should fail at the owning mapping with an actionable name."""

    data = fixtures.raw_organization_data()
    del fixtures.organization_mapping_at(data, location)[field]

    with pytest.raises(ValueError, match=rf"missing required fields: {field}"):
        fixtures.load_organization_fixture(tmp_path, data)


def test_organization_requires_canonical_portfolio_order(tmp_path: Path) -> None:
    """The renderer's four-team layout contract must be explicit at load time."""

    data = fixtures.raw_organization_data()
    data["portfolios"][0], data["portfolios"][1] = (
        data["portfolios"][1],
        data["portfolios"][0],
    )

    with pytest.raises(ValueError, match="expected keys in canonical order"):
        fixtures.load_organization_fixture(tmp_path, data)


def test_organization_rejects_duplicate_portfolio_keys(tmp_path: Path) -> None:
    """Duplicate team identifiers should name both conflicting positions."""

    data = fixtures.raw_organization_data()
    data["portfolios"][1]["key"] = data["portfolios"][0]["key"]

    with pytest.raises(
        ValueError,
        match=r"duplicate portfolio keys: 'directors-office' at indexes 0, 1",
    ):
        fixtures.load_organization_fixture(tmp_path, data)


def test_organization_rejects_duplicate_yaml_keys_at_any_depth(tmp_path: Path) -> None:
    """A nested repeated field must fail instead of silently keeping the last value."""

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

    with pytest.raises(ValueError, match="Invalid YAML") as error:
        load_organization(tmp_path, ORGANIZATION_DATA_PATH)

    assert error.value.__cause__ is not None
    assert "Duplicate YAML key 'title' on lines" in str(error.value.__cause__)
