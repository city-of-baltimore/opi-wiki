"""Tests for maintainable team navigation structure."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

TEAM_NAV_FILES = [
    REPO_ROOT / "docs/about-us/our-teams/directors-office/.pages",
    REPO_ROOT / "docs/about-us/our-teams/performance/.pages",
    REPO_ROOT / "docs/about-us/our-teams/data-and-analytics/.pages",
]

TEAM_LANDING_PAGES = [
    REPO_ROOT / "docs/about-us/our-teams/directors-office/index.md",
    REPO_ROOT / "docs/about-us/our-teams/performance/index.md",
    REPO_ROOT / "docs/about-us/our-teams/data-and-analytics/index.md",
    REPO_ROOT / "docs/about-us/our-teams/innovation-lab/index.md",
]

OLD_TEAM_PD_DIRS = [
    REPO_ROOT / "docs/about-us/our-teams/directors-office",
    REPO_ROOT / "docs/about-us/our-teams/performance",
    REPO_ROOT / "docs/about-us/our-teams/data-and-analytics",
]

TEAM_AND_ROLES_PAGE = REPO_ROOT / "docs/about-us/our-teams/team-and-roles.md"

NAV_TITLE_EXPECTATIONS = {
    REPO_ROOT / "docs/about-us/.pages": "About Us",
    REPO_ROOT / "docs/about-us/letters-from-the-director/.pages": "Letters from the Director",
    REPO_ROOT / "docs/how-we-work/.pages": "How We Work",
    REPO_ROOT / "docs/how-we-work/organization/.pages": "Organization",
    REPO_ROOT / "docs/about-us/our-teams/.pages": "Our Teams",
    REPO_ROOT / "docs/about-us/our-teams/directors-office/.pages": "Director's Office",
    REPO_ROOT / "docs/about-us/our-teams/performance/.pages": "Performance",
    REPO_ROOT / "docs/about-us/our-teams/innovation-lab/.pages": "Innovation Lab",
    REPO_ROOT / "docs/about-us/our-teams/data-and-analytics/.pages": "Data and Analytics",
    REPO_ROOT / "docs/what-we-do/.pages": "What We Do",
    REPO_ROOT / "docs/what-we-do/services/.pages": "Services",
    REPO_ROOT / "docs/what-we-do/programs/.pages": "Programs",
    REPO_ROOT / "docs/what-we-do/programs/citistat/.pages": "CitiStat",
    REPO_ROOT / "docs/what-we-do/programs/citistat/portfolio/.pages": "CitiStat Portfolio",
    REPO_ROOT / "docs/what-we-do/products/.pages": "Products",
    REPO_ROOT / "docs/resources/.pages": "Resources",
    REPO_ROOT / "docs/resources/reference/.pages": "Reference",
}


def test_team_nav_files_do_not_list_position_description_pages() -> None:
    """Team navigation should not duplicate position-description page lists."""

    for nav_file in TEAM_NAV_FILES:
        nav_text = nav_file.read_text(encoding="utf-8")
        assert not any(line.strip().startswith("- pd-") for line in nav_text.splitlines()), (
            f"{nav_file} still lists PD pages in nav."
        )


def test_team_landing_pages_point_to_canonical_team_and_roles_page() -> None:
    """Team landing pages should hand off role discovery to the Team and Roles page."""

    for landing_page in TEAM_LANDING_PAGES:
        page_text = landing_page.read_text(encoding="utf-8")
        assert "team-and-roles.md" in page_text
        assert "pd-" not in page_text, (
            f"{landing_page} still links directly to role-specific PD pages."
        )


def test_full_position_descriptions_are_not_published() -> None:
    """Role summaries live on the public Team and Roles page; no full PDs are published."""

    for team_dir in OLD_TEAM_PD_DIRS:
        assert list(team_dir.glob("pd-*.md")) == []

    assert list((REPO_ROOT / "docs").rglob("pd-*.md")) == []
    assert TEAM_AND_ROLES_PAGE.is_file()


def test_major_sections_define_explicit_nav_titles() -> None:
    """Major sections should not rely on auto-derived nav titles."""

    for nav_file, expected_title in NAV_TITLE_EXPECTATIONS.items():
        nav_text = nav_file.read_text(encoding="utf-8")
        assert f"title: {expected_title}" in nav_text
