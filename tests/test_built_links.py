"""Tests for the built-site internal link crawl."""

from __future__ import annotations

from pathlib import Path

from scripts.check_built_links import find_broken_links


def _write(site_dir: Path, relative: str, html: str) -> None:
    """Write one built HTML page under the fake site directory."""

    target = site_dir / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def test_resolving_relative_and_directory_links_pass(tmp_path: Path) -> None:
    """Relative links to files and pretty-URL directories should resolve."""

    _write(tmp_path, "index.html", '<a href="team/">Team</a> <img src="logo.png">')
    _write(tmp_path, "team/index.html", "<p>team</p>")
    (tmp_path / "logo.png").write_bytes(b"png")

    assert find_broken_links(tmp_path) == []


def test_broken_relative_link_is_reported(tmp_path: Path) -> None:
    """A link to a missing page should be reported with source and target."""

    _write(tmp_path, "index.html", '<a href="missing/">Gone</a>')

    broken = find_broken_links(tmp_path)

    assert len(broken) == 1
    assert "index.html" in broken[0]
    assert "missing/" in broken[0]


def test_external_anchor_and_query_links_are_skipped(tmp_path: Path) -> None:
    """External schemes, anchors, and query strings should not be flagged."""

    _write(
        tmp_path,
        "index.html",
        '<a href="https://example.org/x">x</a>'
        '<a href="mailto:opi@baltimorecity.gov">mail</a>'
        '<a href="#section">anchor</a>'
        '<a href="page.html?tab=2">query</a>',
    )
    _write(tmp_path, "page.html", "<p>page</p>")

    assert find_broken_links(tmp_path) == []


def test_absolute_links_accept_the_pages_base_segment(tmp_path: Path) -> None:
    """site_url-absolute links may carry the deploy base path (/opi-wiki/...)."""

    _write(tmp_path, "404.html", '<a href="/opi-wiki/resources/">Resources</a>')
    _write(tmp_path, "resources/index.html", "<p>resources</p>")

    assert find_broken_links(tmp_path) == []
