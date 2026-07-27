"""Tests for shared structured-data loading helpers."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.data import (
    load_docs_yaml_file,
    load_yaml_mapping,
    resolve_docs_path,
)


def test_resolve_docs_path_rejects_paths_outside_docs_dir(tmp_path: Path) -> None:
    """Docs-relative loaders should reject paths that escape the docs tree."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    with pytest.raises(ValueError, match="must stay inside the docs directory"):
        resolve_docs_path(docs_dir, "../outside.yml", label="Test data")


def test_load_docs_yaml_file_loads_valid_yaml(tmp_path: Path) -> None:
    """Docs-relative YAML files should load through the shared helper."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    data_path = docs_dir / "sample.yml"
    data_path.write_text("title: Example\n", encoding="utf-8")

    assert load_docs_yaml_file(docs_dir, "sample.yml", label="Sample") == {"title": "Example"}


def test_load_docs_yaml_file_rejects_nested_duplicate_keys(tmp_path: Path) -> None:
    """Structured sources must never silently keep the last repeated YAML field."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    data_path = docs_dir / "sample.yml"
    data_path.write_text(
        "person:\n  name: First value\n  name: Second value\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid YAML") as error:
        load_docs_yaml_file(docs_dir, "sample.yml", label="Sample")

    assert error.value.__cause__ is not None
    assert "Duplicate YAML key 'name' on lines 2 and 3" in str(error.value.__cause__)


def test_load_docs_yaml_file_preserves_safe_yaml_merge_semantics(tmp_path: Path) -> None:
    """Duplicate rejection must retain SafeLoader's standard merge-key behavior."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    data_path = docs_dir / "sample.yml"
    data_path.write_text(
        "defaults: &defaults\n"
        "  owner: Director's Office\n"
        "  review: quarterly\n"
        "page:\n"
        "  <<: *defaults\n"
        '  "<<": literal merge-looking key\n'
        "  owner: Performance\n",
        encoding="utf-8",
    )

    loaded = load_docs_yaml_file(docs_dir, "sample.yml", label="Sample")

    assert loaded["page"] == {
        "<<": "literal merge-looking key",
        "owner": "Performance",
        "review": "quarterly",
    }


def test_load_yaml_mapping_defaults_empty_files_to_empty_mapping(tmp_path: Path) -> None:
    """Empty mapping files should normalize to an empty mapping."""

    data_path = tmp_path / ".metadata.yml"
    data_path.write_text("", encoding="utf-8")

    assert load_yaml_mapping(data_path, label="Metadata") == {}


def test_load_yaml_mapping_rejects_non_mapping_yaml(tmp_path: Path) -> None:
    """Mapping loaders should fail clearly on sequence-based YAML files."""

    data_path = tmp_path / ".metadata.yml"
    data_path.write_text("- one\n- two\n", encoding="utf-8")

    with pytest.raises(ValueError, match="must contain a mapping"):
        load_yaml_mapping(data_path, label="Metadata")
