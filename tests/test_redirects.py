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
        "resources/reference/position-descriptions/innovation-lab/pd-civic-design-and-ux-lead.md",
        "resources/reference/position-descriptions/innovation-lab/pd-civic-technology-lead.md",
        "resources/reference/position-descriptions/innovation-lab/pd-communications-and-partnerships-lead.md",
        "resources/reference/position-descriptions/innovation-lab/pd-innovation-program-manager.md",
        "resources/reference/position-descriptions/innovation-lab/pd-product-engineer-full-stack.md",
        "resources/reference/position-descriptions/innovation-lab/pd-senior-product-engineer.md",
    }
