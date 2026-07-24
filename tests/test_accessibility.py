"""Tests for lightweight accessibility smoke checks."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.accessibility import find_accessibility_issues


def _write_built_org_page(site_dir: Path, html: str) -> None:
    """Write a generated org-structure page at its canonical built path."""

    org_dir = site_dir / "how-we-work/organization/org-structure"
    org_dir.mkdir(parents=True)
    (org_dir / "index.html").write_text(html, encoding="utf-8")


def test_accessibility_checker_ignores_non_clickable_cards(tmp_path: Path) -> None:
    """Cards without links should not fail the smoke check."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        ('<div class="opi-card-grid"><article class="opi-card"><h3>Info</h3></article></div>'),
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert issues == []


def test_accessibility_checker_flags_empty_card_link_text(tmp_path: Path) -> None:
    """Linked cards must expose visible link text."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        (
            '<div class="opi-card-grid"><article class="opi-card">'
            '<a class="opi-card-link" href="/test/"></a>'
            "</article></div>"
        ),
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert len(issues) == 1
    assert "missing visible link text" in issues[0]


def test_accessibility_checker_inspects_each_semantic_card(tmp_path: Path) -> None:
    """A later article card must not be hidden by surrounding grid markup."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        (
            "<div class='opi-card-grid'>"
            "<article class='opi-card'>"
            "<a class='opi-card-link' href='/one/'><span>First card</span></a>"
            "</article>"
            "<article class='featured opi-card'>"
            "<a href='/two/' class='opi-card-link'><span> </span></a>"
            "</article>"
            "</div>"
        ),
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert issues == ["index.html: card #2 is missing visible link text"]


def test_accessibility_checker_flags_details_without_summary(tmp_path: Path) -> None:
    """Disclosure widgets must provide a visible summary label."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        "<details><p>Hidden guidance</p></details>",
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert issues == ["index.html: details block #1 is missing a summary label"]


def test_accessibility_checker_flags_empty_nested_summary(tmp_path: Path) -> None:
    """Markup inside summary does not count without visible text."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        "<details><summary><span> </span></summary><p>Guidance</p></details>",
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert issues == ["index.html: details block #1 is missing a summary label"]


def test_accessibility_checker_accepts_labeled_details(tmp_path: Path) -> None:
    """Nested visible summary text satisfies the disclosure label check."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        "<details><summary><strong>More guidance</strong></summary></details>",
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert issues == []


def test_accessibility_checker_flags_multiple_visible_h1s(tmp_path: Path) -> None:
    """A page must expose only one meaningful first-level heading."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        "<h1>Home</h1><div><h1>OPI Foundations</h1></div>",
        encoding="utf-8",
    )

    issues = find_accessibility_issues(site_dir)

    assert issues == ["index.html: page has 2 visible h1 headings; expected at most one"]


def test_accessibility_checker_requires_built_semantic_org_chart(tmp_path: Path) -> None:
    """The built org page must retain its deliberate accessible chart fallback."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    _write_built_org_page(site_dir, "<h1>Org Structure</h1><p>Leadership</p>")

    issues = find_accessibility_issues(site_dir)

    assert issues == [
        "how-we-work/organization/org-structure/index.html: expected one semantic "
        "public leadership chart, found 0"
    ]


def test_accessibility_checker_accepts_complete_built_org_chart(tmp_path: Path) -> None:
    """A captioned hierarchy with all public leadership levels should pass."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    nodes = [
        ("city", "Faith P. Leach"),
        ("executive", "Dartanion Swift-Williams"),
        ("team", "Rakeim Young"),
        ("team", "Danny Heller"),
        ("team", "Jason Howard, PhD"),
        ("team", "Gabriel Watson"),
    ]
    node_markup = "".join(
        f'<div class="opi-org-chart__node" data-org-level="{level}">'
        f'<strong class="opi-org-chart__name">{name}</strong></div>'
        for level, name in nodes
    )
    _write_built_org_page(
        site_dir,
        '<h1>Org Structure</h1><figure class="opi-org-chart">'
        '<figcaption class="opi-org-chart__caption">Public reporting hierarchy</figcaption>'
        f"{node_markup}</figure>",
    )

    assert find_accessibility_issues(site_dir) == []


def test_accessibility_checker_flags_incomplete_built_org_chart(tmp_path: Path) -> None:
    """An empty chart shell must not pass the built-page regression."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    _write_built_org_page(
        site_dir,
        '<figure class="opi-org-chart"><figcaption class="opi-org-chart__caption"> '
        '</figcaption><div class="opi-org-chart__node" data-org-level="city">'
        '<strong class="opi-org-chart__name"> </strong></div></figure>',
    )

    issues = find_accessibility_issues(site_dir)

    assert any("missing its caption" in issue for issue in issues)
    assert any("'executive' nodes; expected 1" in issue for issue in issues)
    assert any("'team' nodes; expected 4" in issue for issue in issues)
    assert any("node #1 is missing a visible name" in issue for issue in issues)


def test_accessibility_checker_reports_built_html_read_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unreadable build output should fail with the affected path."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    html_file = site_dir / "index.html"
    html_file.write_text("<h1>OPI Foundations</h1>", encoding="utf-8")

    def fail_read(path: Path, *, encoding: str) -> str:
        assert path == html_file
        assert encoding == "utf-8"
        raise OSError("read failed")

    monkeypatch.setattr(Path, "read_text", fail_read)

    with pytest.raises(RuntimeError, match=r"Unable to read built HTML file: .*index\.html"):
        find_accessibility_issues(site_dir)
