"""Tests for maintainable redirect-map structure."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
MKDOCS_CONFIG = REPO_ROOT / "mkdocs.yml"
DOCS_DIR = REPO_ROOT / "docs"


class _MkDocsConfigLoader(yaml.SafeLoader):
    """Safe loader that tolerates MkDocs Python-name tags."""


def _construct_python_name(
    loader: _MkDocsConfigLoader,
    node: yaml.Node,
) -> str:
    """Treat Python-name tags as plain scalar strings for config inspection."""

    return loader.construct_scalar(node)


_MkDocsConfigLoader.add_constructor(
    "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format",
    _construct_python_name,
)


def _load_redirect_map() -> dict[str, str]:
    """Return the configured MkDocs redirect map."""

    config = yaml.load(
        MKDOCS_CONFIG.read_text(encoding="utf-8"),
        Loader=_MkDocsConfigLoader,
    )
    plugins = config.get("plugins", [])

    for plugin in plugins:
        if isinstance(plugin, dict) and "redirects" in plugin:
            return plugin["redirects"].get("redirect_maps", {})

    raise AssertionError("mkdocs.yml is missing the redirects plugin configuration.")


def test_redirect_map_uses_docs_relative_markdown_paths() -> None:
    """Redirect entries should stay docs-relative and point to Markdown sources."""

    redirect_map = _load_redirect_map()

    assert redirect_map
    for source, destination in redirect_map.items():
        assert not source.startswith("/"), f"Redirect source must be docs-relative: {source}"
        assert not destination.startswith("/"), (
            f"Redirect destination must be docs-relative: {destination}"
        )
        assert source.endswith(".md"), f"Redirect source must target a Markdown page: {source}"
        assert destination.endswith(".md"), (
            f"Redirect destination must target a Markdown page: {destination}"
        )


def test_redirect_destinations_point_to_existing_docs_pages() -> None:
    """Redirect destinations should resolve to checked-in Markdown pages."""

    redirect_map = _load_redirect_map()

    for destination in redirect_map.values():
        destination_path = DOCS_DIR / destination
        assert destination_path.exists(), f"Redirect destination does not exist: {destination}"
