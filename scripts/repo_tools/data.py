"""Shared file-loading helpers for docs-adjacent structured data."""

from __future__ import annotations

from collections.abc import Hashable
from pathlib import Path
from typing import Any

import yaml

_YAML_MERGE_KEY = object()


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys at every depth."""

    def construct_mapping(
        self,
        node: yaml.MappingNode,
        deep: bool = False,
    ) -> dict[Any, Any]:
        """Construct a mapping after proving that every explicit key is unique."""

        if not isinstance(node, yaml.MappingNode):
            raise ValueError(f"Expected a YAML mapping node, got {node!r}.")

        first_lines: dict[Hashable, int] = {}
        for key_node, _value_node in node.value:
            # SafeConstructor resolves this special tag only while flattening
            # the mapping. Recognize it here without constructing it so legal
            # YAML merge keys retain their standard override behavior.
            is_merge_key = key_node.tag == "tag:yaml.org,2002:merge"
            key = (
                _YAML_MERGE_KEY
                if key_node.tag == "tag:yaml.org,2002:merge"
                else self.construct_object(key_node, deep=deep)
            )
            if not isinstance(key, Hashable):
                raise ValueError(f"Unhashable YAML mapping key at {key_node.start_mark}.")
            line_number = key_node.start_mark.line + 1
            if key in first_lines:
                display_key = "<<" if is_merge_key else key
                raise ValueError(
                    f"Duplicate YAML key '{display_key}' on lines "
                    f"{first_lines[key]} and {line_number}."
                )
            first_lines[key] = line_number

        return super().construct_mapping(node, deep=deep)


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
        # S506: UniqueKeySafeLoader subclasses yaml.SafeLoader and adds only
        # duplicate-key rejection. It cannot construct arbitrary Python objects.
        return yaml.load(  # nosec B506
            read_utf8(path, label=label),
            Loader=UniqueKeySafeLoader,  # noqa: S506
        )
    except (ValueError, yaml.YAMLError) as error:
        raise ValueError(f"Invalid YAML in {label.lower()} file: {path}. {error}") from error


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
