"""Validation helpers for page review metadata sidecars."""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import yaml

REQUIRED_FIELDS = ("owner", "status", "last_reviewed", "next_review", "change_log")


@dataclass(frozen=True)
class MetadataConfig:
    """Normalized metadata configuration for a directory scope."""

    defaults: dict[str, str]
    patterns: dict[str, dict[str, str]]
    pages: dict[str, dict[str, str]]


def _normalize_mapping(raw: Any, source: Path, label: str) -> dict[str, dict[str, str]]:
    """Validate a nested mapping section from a metadata file."""

    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(f"{source}: '{label}' must be a mapping.")

    normalized: dict[str, dict[str, str]] = {}
    for key, value in raw.items():
        if not isinstance(value, dict):
            raise ValueError(f"{source}: '{label}.{key}' must be a mapping.")
        normalized[str(key)] = {
            str(field): str(field_value) for field, field_value in value.items()
        }
    return normalized


def load_metadata_config(path: Path) -> MetadataConfig:
    """Load a metadata sidecar file."""

    try:
        raw_data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Metadata file not found: {path}") from error
    except OSError as error:
        raise RuntimeError(f"Unable to read metadata file: {path}") from error
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML in metadata file: {path}") from error

    if not isinstance(raw_data, dict):
        raise ValueError(f"Metadata file must contain a mapping: {path}")

    defaults = raw_data.get("defaults", {})
    if defaults is None:
        defaults = {}
    if not isinstance(defaults, dict):
        raise ValueError(f"{path}: 'defaults' must be a mapping.")

    return MetadataConfig(
        defaults={str(key): str(value) for key, value in defaults.items()},
        patterns=_normalize_mapping(raw_data.get("patterns"), path, "patterns"),
        pages=_normalize_mapping(raw_data.get("pages"), path, "pages"),
    )


def resolve_page_metadata(docs_dir: Path, markdown_file: Path) -> dict[str, str]:
    """Resolve effective metadata for a page using inherited sidecar files."""

    relative_parts = markdown_file.relative_to(docs_dir).parts[:-1]
    candidate_dirs = [docs_dir]
    current = docs_dir
    for part in relative_parts:
        current = current / part
        candidate_dirs.append(current)

    effective: dict[str, str] = {}
    relative_to_parent = markdown_file.name

    for directory in candidate_dirs:
        metadata_path = directory / ".metadata.yml"
        if not metadata_path.exists():
            continue

        config = load_metadata_config(metadata_path)
        effective.update(config.defaults)

        for pattern, values in config.patterns.items():
            if fnmatch(relative_to_parent, pattern):
                effective.update(values)

        page_override = config.pages.get(relative_to_parent)
        if page_override:
            effective.update(page_override)

    return effective


def find_metadata_issues(docs_dir: Path) -> list[str]:
    """Return missing or malformed metadata issues for Markdown files."""

    issues: list[str] = []

    for markdown_file in sorted(docs_dir.rglob("*.md")):
        metadata = resolve_page_metadata(docs_dir, markdown_file)
        missing = [field for field in REQUIRED_FIELDS if not metadata.get(field)]
        if missing:
            relative_file = markdown_file.relative_to(docs_dir)
            missing_fields = ", ".join(sorted(missing))
            issues.append(f"{relative_file}: missing metadata fields: {missing_fields}")

    return issues
