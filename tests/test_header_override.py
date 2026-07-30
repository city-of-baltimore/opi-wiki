"""Regression tests for the branded Material header override."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from mkdocs.commands.build import build
from mkdocs.config import load_config

REPO_ROOT = Path(__file__).resolve().parents[1]


def _build_header_html(tmp_path: Path, *, search_enabled: bool) -> str:
    """Render one tiny site with the real OPI header overrides."""

    docs_dir = tmp_path / "docs"
    site_dir = tmp_path / "site"
    javascript_dir = docs_dir / "assets" / "javascripts"
    javascript_dir.mkdir(parents=True)
    (docs_dir / "index.md").write_text("# Home\n", encoding="utf-8")
    for script_name in ("header-controls.js", "palette-controls.js"):
        shutil.copyfile(
            REPO_ROOT / "docs" / "assets" / "javascripts" / script_name,
            javascript_dir / script_name,
        )
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
                "  palette:",
                "    - scheme: default",
                "      toggle:",
                "        icon: material/weather-night",
                "        name: Switch to dark mode",
                "    - scheme: slate",
                "      toggle:",
                "        icon: material/weather-sunny",
                "        name: Switch to light mode",
                "plugins:",
                "  - search:",
                f"      enabled: {str(search_enabled).lower()}",
                "extra_javascript:",
                "  - assets/javascripts/header-controls.js",
                "  - assets/javascripts/palette-controls.js",
                "",
            )
        ),
        encoding="utf-8",
    )

    config = load_config(config_file=str(config_file))
    build(config)
    return (site_dir / "index.html").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def enabled_header_html(tmp_path_factory: pytest.TempPathFactory) -> str:
    """Build the search-enabled header contract once."""

    return _build_header_html(tmp_path_factory.mktemp("enabled-header"), search_enabled=True)


@pytest.fixture(scope="module")
def disabled_header_html(tmp_path_factory: pytest.TempPathFactory) -> str:
    """Build the search-disabled header contract once."""

    return _build_header_html(tmp_path_factory.mktemp("disabled-header"), search_enabled=False)


def _button_tag(html: str, marker: str) -> str:
    """Return the rendered button start tag containing one stable marker."""

    marker_index = html.index(marker)
    start = html.rfind("<button", 0, marker_index)
    end = html.index(">", marker_index)
    return html[start : end + 1]


def test_header_renders_one_native_semantic_control_system(enabled_header_html: str) -> None:
    """The branded header must expose native controls over Material-owned state."""

    html = enabled_header_html
    brand_marker = 'class="md-header__title md-header__lockup opi-header__brand"'
    assert html.count(brand_marker) == 1
    brand_index = html.index(brand_marker)
    brand_tag = html[html.rfind("<a", 0, brand_index) : html.index(">", brand_index) + 1]
    assert 'href="' in brand_tag
    assert 'aria-label="OPI Foundations home"' in brand_tag
    assert "City of Baltimore" in html

    controlled_actions = {
        "data-opi-drawer-open": "opi-primary-navigation",
        "data-opi-search-open": "opi-search",
    }
    for marker, target_id in controlled_actions.items():
        tag = _button_tag(html, marker)
        assert 'type="button"' in tag
        assert 'aria-label="' in tag
        assert f'aria-controls="{target_id}"' in tag
        assert 'aria-expanded="false"' in tag
    assert html.count('id="opi-search"') == 1

    for marker in (
        "data-opi-drawer-close",
        "data-opi-search-close",
        "data-opi-palette-toggle",
    ):
        tag = _button_tag(html, marker)
        assert 'type="button"' in tag
        assert 'aria-label="' in tag

    assert html.count("data-opi-palette-toggle") == 2
    assert html.count('class="md-option"') == 2
    assert html.count('tabindex="-1" aria-hidden="true"') == 2
    assert html.count("assets/javascripts/header-controls.js") == 1
    assert html.count("assets/javascripts/palette-controls.js") == 1
    assert 'class="md-header__button md-icon opi-header__fallback-control ' in html
    assert 'class="md-nav__button md-icon opi-drawer__close opi-drawer__fallback-close"' in html
    assert 'class="md-search__icon md-icon opi-search__close ' in html
    assert 'id="opi-primary-navigation-links"' in html


def test_header_omits_search_controls_when_search_is_disabled(
    disabled_header_html: str,
) -> None:
    """The branded override must retain Material's dynamic search guard."""

    html = disabled_header_html
    assert "City of Baltimore" in html
    assert 'for="__search"' not in html
    assert 'class="md-search"' not in html
    assert "data-opi-search-open" not in html
