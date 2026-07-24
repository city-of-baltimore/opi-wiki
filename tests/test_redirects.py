"""Tests for maintainable redirect-map structure."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.redirects import (
    ALLOWED_DUPLICATE_DESTINATIONS,
    find_redirect_issues,
    load_redirect_map,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MKDOCS_CONFIG = REPO_ROOT / "mkdocs.yml"
DOCS_DIR = REPO_ROOT / "docs"


def test_redirect_map_has_no_maintainability_issues() -> None:
    """Checked-in redirect maps should stay valid and intentionally aggregated."""

    assert find_redirect_issues(MKDOCS_CONFIG, DOCS_DIR) == []


def test_redirect_duplicate_destinations_require_allowlist(tmp_path: Path) -> None:
    """Many-to-one redirects should be explicit so they do not accumulate silently."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "current.md").write_text("# Current\n", encoding="utf-8")

    config_path = tmp_path / "mkdocs.yml"
    config_path.write_text(
        "plugins:\n"
        "  - redirects:\n"
        "      redirect_maps:\n"
        "        old-a.md: current.md\n"
        "        old-b.md: current.md\n",
        encoding="utf-8",
    )

    issues = find_redirect_issues(config_path, docs_dir)

    assert issues == [
        "Redirect destination is shared by 2 legacy paths without an explicit allowlist: current.md"
    ]


def test_redirect_loader_rejects_duplicate_yaml_keys(tmp_path: Path) -> None:
    """A repeated redirect source must not be silently overwritten by YAML."""

    config_path = tmp_path / "mkdocs.yml"
    config_path.write_text(
        "plugins:\n"
        "  - redirects:\n"
        "      redirect_maps:\n"
        "        retired.md: current-a.md\n"
        "        retired.md: current-b.md\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate YAML key 'retired.md'"):
        load_redirect_map(config_path)


def test_redirect_allowlist_stays_small_and_explicit() -> None:
    """Intentional many-to-one redirects should remain rare and documented."""

    assert ALLOWED_DUPLICATE_DESTINATIONS == {
        "resources/index.md",
        "resources/reference/index.md",
        "about-us/our-teams/team-and-roles.md",
        "what-we-do/services/cross-agency-delivery/service-definition.md",
        "what-we-do/services/cross-agency-delivery/index.md",
        "how-we-work/organization/org-structure.md",
        "how-we-work/index.md",
        "how-we-work/how-work-moves-through-opi.md",
        "about-us/our-teams/performance/index.md",
        "about-us/our-teams/performance/about-performance.md",
        "about-us/our-teams/data-and-analytics/about-data-analytics.md",
        "about-us/our-teams/innovation-lab/about-innovation-lab.md",
        "about-us/our-teams/directors-office/about-admin-ops.md",
        "what-we-do/products/baltimore-intelligence-center/index.md",
        "what-we-do/products/baltimore-intelligence-center/architecture-and-roadmap.md",
        "what-we-do/products/baltimore-intelligence-center/products-and-capabilities.md",
        "what-we-do/programs/citistat/method-playbook.md",
        "what-we-do/programs/data-governance/index.md",
    }
