"""Regression tests for the branded Material header override."""

from __future__ import annotations

from pathlib import Path

from mkdocs.commands.build import build
from mkdocs.config import load_config

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_header_omits_search_controls_when_search_is_disabled(tmp_path: Path) -> None:
    """The branded override must retain Material's dynamic search guard."""

    docs_dir = tmp_path / "docs"
    site_dir = tmp_path / "site"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Home\n", encoding="utf-8")
    config_file = tmp_path / "mkdocs.yml"
    config_file.write_text(
        "\n".join(
            (
                "site_name: OPI Foundations",
                f"docs_dir: {docs_dir.as_posix()}",
                f"site_dir: {site_dir.as_posix()}",
                "theme:",
                "  name: material",
                f"  custom_dir: {(REPO_ROOT / 'overrides').as_posix()}",
                "plugins:",
                "  - search:",
                "      enabled: false",
                "",
            )
        ),
        encoding="utf-8",
    )

    config = load_config(config_file=str(config_file))
    build(config)
    html = (site_dir / "index.html").read_text(encoding="utf-8")

    assert "City of Baltimore" in html
    assert 'for="__search"' not in html
    assert 'class="md-search"' not in html
