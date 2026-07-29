"""Strict loading and role lookup for OPI organization data."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from scripts.repo_tools.data import load_docs_yaml_file

ORGANIZATION_DATA_PATH = "_data/people.yml"

_ROOT_FIELDS = frozenset(
    {
        "mayor",
        "city_administrator",
        "executive_director",
        "portfolios",
    }
)
_PERSON_FIELDS = frozenset({"name", "title", "summary"})
_PORTFOLIO_FIELDS = frozenset({"key", "lead", "primary_value", "staff"})
_PORTFOLIO_LABELS = MappingProxyType(
    {
        "directors-office": "Director's Office",
        "performance": "Performance",
        "data-and-analytics": "Data and Analytics",
        "innovation-lab": "Innovation Lab",
    }
)
_PORTFOLIO_KEYS = tuple(_PORTFOLIO_LABELS)


@dataclass(frozen=True, slots=True)
class OrgPerson:
    """One named organization role and its optional plain-language summary."""

    name: str
    title: str
    summary: str = ""

    @property
    def is_vacant(self) -> bool:
        """Return whether this role has no current incumbent."""

        return self.name.casefold() == "open"


@dataclass(frozen=True, slots=True)
class Portfolio:
    """One OPI team, its lead, its staff, and its primary value."""

    key: str
    lead: OrgPerson
    primary_value: str
    staff: tuple[OrgPerson, ...]

    @property
    def label(self) -> str:
        """Derive the display label from the canonical portfolio identifier."""

        return _PORTFOLIO_LABELS[self.key]


@dataclass(frozen=True, slots=True)
class OrgStructure:
    """The complete, immutable OPI organization directory."""

    mayor: OrgPerson
    city_administrator: OrgPerson
    executive_director: OrgPerson
    portfolios: tuple[Portfolio, ...]


def _mapping(value: Any, path: str) -> dict[Any, Any]:
    """Return a mapping value or fail with its source location."""

    if not isinstance(value, dict):
        raise ValueError(f"{path}: must be a mapping.")
    return value


def _validate_fields(
    mapping: dict[Any, Any],
    *,
    allowed: frozenset[str],
    required: frozenset[str],
    path: str,
) -> None:
    """Reject unknown and missing fields at one organization-data level."""

    unknown = sorted(
        (repr(key) if not isinstance(key, str) else key)
        for key in mapping
        if not isinstance(key, str) or key not in allowed
    )
    if unknown:
        unknown_fields = ", ".join(unknown)
        allowed_fields = ", ".join(sorted(allowed))
        raise ValueError(
            f"{path}: unsupported fields: {unknown_fields}. Allowed fields: {allowed_fields}."
        )

    missing = sorted(field for field in required if field not in mapping)
    if missing:
        missing_fields = ", ".join(missing)
        raise ValueError(f"{path}: missing required fields: {missing_fields}.")


def _text(mapping: dict[Any, Any], field: str, path: str) -> str:
    """Return one required, single-line plain-text field."""

    value = mapping[field]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}.{field}: must be a non-empty string.")

    normalized = value.strip()
    if any(character in normalized for character in "\r\n\t\f\v"):
        raise ValueError(
            f"{path}.{field}: must be single-line plain text without control whitespace."
        )
    return normalized


def _optional_text(mapping: dict[Any, Any], field: str, path: str) -> str:
    """Return one optional plain-text field."""

    if field not in mapping:
        return ""
    return _text(mapping, field, path)


def _person(
    raw_person: Any,
    path: str,
    *,
    summary_required: bool,
) -> OrgPerson:
    """Validate and normalize one person mapping."""

    person = _mapping(raw_person, path)
    required = {"name", "title", "summary"} if summary_required else {"name", "title"}
    _validate_fields(
        person,
        allowed=_PERSON_FIELDS,
        required=frozenset(required),
        path=path,
    )
    return OrgPerson(
        name=_text(person, "name", path),
        title=_text(person, "title", path),
        summary=_optional_text(person, "summary", path),
    )


def _portfolio(raw_portfolio: Any, index: int, source: str) -> Portfolio:
    """Validate and normalize one portfolio mapping."""

    portfolio_path = f"{source}.portfolios[{index}]"
    portfolio = _mapping(raw_portfolio, portfolio_path)
    _validate_fields(
        portfolio,
        allowed=_PORTFOLIO_FIELDS,
        required=_PORTFOLIO_FIELDS,
        path=portfolio_path,
    )

    raw_staff = portfolio["staff"]
    if not isinstance(raw_staff, list):
        raise ValueError(f"{portfolio_path}.staff: must be a list.")

    return Portfolio(
        key=_text(portfolio, "key", portfolio_path),
        lead=_person(
            portfolio["lead"],
            f"{portfolio_path}.lead",
            summary_required=True,
        ),
        primary_value=_text(portfolio, "primary_value", portfolio_path),
        staff=tuple(
            _person(
                member,
                f"{portfolio_path}.staff[{member_index}]",
                summary_required=True,
            )
            for member_index, member in enumerate(raw_staff)
        ),
    )


def load_organization(docs_dir: Path, relative_path: str) -> OrgStructure:
    """Load the one allowlisted organization-data shape under the docs tree."""

    raw_data = load_docs_yaml_file(docs_dir, relative_path, label="Organization data")
    source = relative_path
    data = _mapping(raw_data, source)
    _validate_fields(
        data,
        allowed=_ROOT_FIELDS,
        required=_ROOT_FIELDS,
        path=source,
    )

    raw_portfolios = data["portfolios"]
    if not isinstance(raw_portfolios, list):
        raise ValueError(f"{source}.portfolios: must be a list.")
    if not raw_portfolios:
        raise ValueError(f"{source}.portfolios: must be a non-empty list.")

    portfolios = tuple(
        _portfolio(portfolio, index, source) for index, portfolio in enumerate(raw_portfolios)
    )
    key_positions: defaultdict[str, list[int]] = defaultdict(list)
    for index, portfolio in enumerate(portfolios):
        key_positions[portfolio.key].append(index)
    duplicate_keys = {
        key: positions for key, positions in key_positions.items() if len(positions) > 1
    }
    if duplicate_keys:
        details = "; ".join(
            f"'{key}' at indexes {', '.join(str(index) for index in positions)}"
            for key, positions in sorted(duplicate_keys.items())
        )
        raise ValueError(f"{source}.portfolios: duplicate portfolio keys: {details}.")

    portfolio_keys = tuple(portfolio.key for portfolio in portfolios)
    if portfolio_keys != _PORTFOLIO_KEYS:
        raise ValueError(
            f"{source}.portfolios: expected keys in canonical order "
            f"{list(_PORTFOLIO_KEYS)}; found {list(portfolio_keys)}."
        )

    return OrgStructure(
        mayor=_person(data["mayor"], f"{source}.mayor", summary_required=False),
        city_administrator=_person(
            data["city_administrator"],
            f"{source}.city_administrator",
            summary_required=False,
        ),
        executive_director=_person(
            data["executive_director"],
            f"{source}.executive_director",
            summary_required=True,
        ),
        portfolios=portfolios,
    )


def _role_holders(structure: OrgStructure) -> tuple[OrgPerson, ...]:
    """Return organization roles eligible for inline role-holder lookup."""

    portfolio_people = tuple(
        person
        for portfolio in structure.portfolios
        for person in (portfolio.lead, *portfolio.staff)
    )
    return (structure.executive_director, *portfolio_people)


def find_role_holder(structure: OrgStructure, title: str) -> str:
    """Return the sole filled incumbent for one working title."""

    if not isinstance(title, str):
        raise ValueError("Role-holder title must be a non-empty string.")
    wanted = title.strip().casefold()
    if not wanted:
        raise ValueError("Role-holder title must be a non-empty string.")

    title_matches = tuple(
        person for person in _role_holders(structure) if person.title.casefold() == wanted
    )
    if not title_matches:
        raise ValueError(f"Unknown organization role '{title}'.")

    filled_matches = tuple(person for person in title_matches if not person.is_vacant)
    if not filled_matches:
        raise ValueError(f"Organization role '{title}' is vacant.")
    if len(filled_matches) > 1:
        names = ", ".join(person.name for person in filled_matches)
        raise ValueError(f"Multiple filled role holders found for title '{title}': {names}.")
    return filled_matches[0].name


def find_organization_data_issues(
    docs_dir: Path,
    relative_path: str = ORGANIZATION_DATA_PATH,
) -> list[str]:
    """Return an actionable finding when the organization source is invalid."""

    try:
        load_organization(docs_dir, relative_path)
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        return [str(error)]
    return []
