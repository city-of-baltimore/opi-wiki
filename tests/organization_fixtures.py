"""Shared fixture builders for organization-data tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from main import DOCS_DIR
from scripts.repo_tools.organization import (
    ORGANIZATION_DATA_PATH,
    OrgStructure,
    load_organization,
)


def raw_organization_data() -> dict[str, Any]:
    """Return a mutable copy of the checked-in organization source."""

    raw_data = yaml.safe_load((DOCS_DIR / ORGANIZATION_DATA_PATH).read_text(encoding="utf-8"))
    assert isinstance(raw_data, dict)
    return raw_data


def write_organization_data(tmp_path: Path, data: Any) -> Path:
    """Write one organization fixture beneath a docs-shaped temporary tree."""

    data_path = tmp_path / ORGANIZATION_DATA_PATH
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(
        yaml.safe_dump(data, sort_keys=False),
        encoding="utf-8",
    )
    return data_path


def load_organization_fixture(tmp_path: Path, data: Any) -> OrgStructure:
    """Write and load one temporary organization fixture."""

    write_organization_data(tmp_path, data)
    return load_organization(tmp_path, ORGANIZATION_DATA_PATH)


def replace_organization_node(
    data: dict[str, Any],
    location: str,
    value: Any,
) -> Any:
    """Replace one schema node and return the possibly replaced root."""

    if location == "root":
        return value
    if location == "mayor":
        data["mayor"] = value
    elif location == "portfolio":
        data["portfolios"][0] = value
    elif location == "lead":
        data["portfolios"][0]["lead"] = value
    elif location == "staff":
        data["portfolios"][0]["staff"][0] = value
    else:
        raise AssertionError(f"Unknown test location: {location}")
    return data


def organization_mapping_at(
    data: dict[str, Any],
    location: str,
) -> dict[str, Any]:
    """Return one mutable schema mapping for parameterized tests."""

    if location == "root":
        return data
    if location == "mayor":
        return data["mayor"]
    if location == "executive_director":
        return data["executive_director"]
    if location == "portfolio":
        return data["portfolios"][0]
    if location == "lead":
        return data["portfolios"][0]["lead"]
    if location == "staff":
        return data["portfolios"][0]["staff"][0]
    raise AssertionError(f"Unknown test location: {location}")
