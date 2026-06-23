"""Tests for maintainable redirect-map structure."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.redirects import ALLOWED_DUPLICATE_DESTINATIONS, find_redirect_issues

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


def test_redirect_allowlist_stays_small_and_explicit() -> None:
    """Intentional many-to-one redirects should remain rare and documented."""

    assert ALLOWED_DUPLICATE_DESTINATIONS == {
        "resources/index.md",
        "resources/reference/position-descriptions/innovation-lab/pd-civic-designer.md",
        "resources/reference/position-descriptions/directors-office/pd-data-storyteller.md",
        "resources/reference/position-descriptions/directors-office/pd-operations-analyst.md",
        "resources/reference/position-descriptions/data-and-analytics/pd-applied-data-scientist.md",
        "resources/reference/position-descriptions/innovation-lab/pd-innovation-program-manager.md",
        "resources/reference/position-descriptions/innovation-lab/pd-product-engineer-full-stack.md",
        "resources/reference/position-descriptions/data-and-analytics/pd-principal-data-engineer.md",
        "resources/reference/position-descriptions/innovation-lab/pd-applied-data-scientist.md",
        "resources/reference/position-descriptions/performance/pd-citistat-analyst.md",
        "resources/reference/position-descriptions/performance/pd-citistat-program-manager.md",
        "resources/reference/position-descriptions/performance/pd-deputy-chief-performance-officer.md",
        "resources/reference/position-descriptions/performance/pd-senior-performance-analyst.md",
        "about-us/our-teams/innovation-lab/cross-agency-delivery-service-definition.md",
        "what-we-do/services/cross-agency-delivery.md",
        "how-we-work/organization/org-structure.md",
        "how-we-work/organization/team-and-roles/index.md",
        "how-we-work/how-work-moves-through-opi.md",
        "about-us/our-teams/performance/index.md",
        "about-us/our-teams/performance/about-performance.md",
        "about-us/our-teams/performance/performance-strategy.md",
        "about-us/our-teams/performance/performance-theory-of-change.md",
    }
