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
