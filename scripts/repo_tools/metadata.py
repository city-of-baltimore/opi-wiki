"""Validation helpers for page review metadata sidecars."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Mapping

from scripts.repo_tools.data import load_yaml_mapping

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

    raw_data = load_yaml_mapping(path, label="Metadata")

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


# The published staleness policy: pages unreviewed for 6+ months are flagged.
REVIEW_MAX_AGE_DAYS = 183


def _parse_review_date(raw_value: str) -> date | None:
    """Parse an ISO metadata date, returning None when it does not parse."""

    try:
        return date.fromisoformat(raw_value.strip())
    except ValueError:
        return None


def find_review_date_issues(
    metadata: Mapping[str, str],
    relative_file: str,
    *,
    today: date,
) -> list[str]:
    """Validate the freshness contract on one page's resolved metadata."""

    issues: list[str] = []

    last_reviewed = _parse_review_date(metadata.get("last_reviewed", ""))
    next_review = _parse_review_date(metadata.get("next_review", ""))

    if last_reviewed is None:
        issues.append(f"{relative_file}: last_reviewed is not an ISO date (YYYY-MM-DD)")
    elif (today - last_reviewed).days > REVIEW_MAX_AGE_DAYS:
        issues.append(
            f"{relative_file}: last_reviewed {last_reviewed.isoformat()} is older than "
            f"{REVIEW_MAX_AGE_DAYS} days — review the page (or its section) and bump "
            "last_reviewed/next_review in the nearest .metadata.yml"
        )

    if next_review is None:
        issues.append(f"{relative_file}: next_review is not an ISO date (YYYY-MM-DD)")
    elif last_reviewed is not None and next_review < last_reviewed:
        issues.append(
            f"{relative_file}: next_review {next_review.isoformat()} precedes "
            f"last_reviewed {last_reviewed.isoformat()}"
        )

    return issues


def find_metadata_issues(docs_dir: Path, *, today: date | None = None) -> list[str]:
    """Return missing, malformed, or stale metadata issues for Markdown files."""

    issues: list[str] = []
    effective_today = today or date.today()

    for markdown_file in sorted(docs_dir.rglob("*.md")):
        metadata = resolve_page_metadata(docs_dir, markdown_file)
        relative_file = str(markdown_file.relative_to(docs_dir))
        missing = [field for field in REQUIRED_FIELDS if not metadata.get(field)]
        if missing:
            missing_fields = ", ".join(sorted(missing))
            issues.append(f"{relative_file}: missing metadata fields: {missing_fields}")
            continue

        issues.extend(
            find_review_date_issues(metadata, relative_file, today=effective_today)
        )

    return issues
