"""Load and query the public OPI organization directory.

The source file deliberately contains only information published by the org
chart. Payroll identifiers and phone numbers are forbidden at the loader
boundary so those fields cannot silently return to the public build.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts.repo_tools.data import load_docs_yaml_file

_FORBIDDEN_PUBLIC_FIELDS = frozenset({"pin", "phone"})


def _forbidden_field_paths(value: Any, path: str = "root") -> list[str]:
    """Return paths to forbidden publication fields in a nested data value."""

    paths: list[str] = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_text = str(key)
            nested_path = f"{path}.{key_text}"
            if key_text.casefold() in _FORBIDDEN_PUBLIC_FIELDS:
                paths.append(nested_path)
            paths.extend(_forbidden_field_paths(nested_value, nested_path))
    elif isinstance(value, list):
        for index, nested_value in enumerate(value):
            paths.extend(_forbidden_field_paths(nested_value, f"{path}[{index}]"))
    return paths


def load_people(docs_dir: Path, relative_path: str) -> dict[str, Any]:
    """Load the public people mapping and reject private legacy fields."""

    data = load_docs_yaml_file(docs_dir, relative_path, label="People data")
    if not isinstance(data, dict):
        raise ValueError(f"People data file must contain a mapping: {relative_path}")
    if not isinstance(data.get("portfolios"), list) or not data["portfolios"]:
        raise ValueError(f"{relative_path} must define a non-empty 'portfolios' list.")

    forbidden_paths = _forbidden_field_paths(data)
    if forbidden_paths:
        joined_paths = ", ".join(forbidden_paths)
        raise ValueError(
            f"{relative_path} contains fields forbidden from public people data: {joined_paths}"
        )
    return data


def _team_people(portfolio: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a portfolio's lead followed by its staff mappings."""

    people = [portfolio["lead"], *portfolio.get("staff", [])]
    return [person for person in people if isinstance(person, dict)]


def find_role_holder(data: dict[str, Any], title: str) -> str:
    """Return the name of the City staff member holding a working title."""

    wanted = title.strip().casefold()
    for portfolio in data["portfolios"]:
        for person in _team_people(portfolio):
            if str(person.get("title", "")).strip().casefold() == wanted and not str(
                person.get("name", "")
            ).casefold().startswith("open"):
                return str(person["name"]).strip()
    executive_director = data.get("executive_director", {})
    if str(executive_director.get("title", "")).strip().casefold() == wanted:
        return str(executive_director["name"]).strip()
    raise ValueError(f"No filled role holder found for title '{title}'.")
