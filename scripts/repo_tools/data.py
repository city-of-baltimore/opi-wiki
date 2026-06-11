"""Shared file-loading helpers for docs-adjacent structured data."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def resolve_docs_path(docs_dir: Path, relative_path: str, *, label: str) -> Path:
    """Resolve a docs-relative path and reject paths that escape the docs tree."""

    docs_root = docs_dir.resolve()
    data_path = (docs_root / relative_path).resolve()

    if data_path != docs_root and docs_root not in data_path.parents:
        raise ValueError(f"{label} file must stay inside the docs directory: {relative_path}")

    return data_path


def read_utf8(path: Path, *, label: str) -> str:
    """Read a UTF-8 text file with normalized IO error messages."""

    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise FileNotFoundError(f"{label} file not found: {path}") from error
    except OSError as error:
        raise RuntimeError(f"Unable to read {label.lower()} file: {path}") from error


def load_yaml_file(path: Path, *, label: str) -> Any:
    """Load YAML data from a path with normalized parsing errors."""

    try:
        return yaml.safe_load(read_utf8(path, label=label))
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML in {label.lower()} file: {path}") from error


def load_docs_yaml_file(docs_dir: Path, relative_path: str, *, label: str) -> Any:
    """Resolve and load a docs-relative YAML file."""

    data_path = resolve_docs_path(docs_dir, relative_path, label=label)
    return load_yaml_file(data_path, label=label)


def load_yaml_mapping(path: Path, *, label: str) -> dict[str, Any]:
    """Load a YAML mapping from disk, defaulting empty files to an empty mapping."""

    raw_data = load_yaml_file(path, label=label) or {}
    if not isinstance(raw_data, dict):
        raise ValueError(f"{label} file must contain a mapping: {path}")
    return raw_data
