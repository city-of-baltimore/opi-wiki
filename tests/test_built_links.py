"""Tests for the built-site internal link crawl."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.check_built_links as built_links_cli
from scripts.check_built_links import main
from scripts.repo_tools.built_links import (
    discover_site_base_path,
    extract_built_references,
    find_broken_links,
    load_sitemap_locations,
)


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


def test_parser_supports_single_quotes_unquoted_values_and_multiline_tags() -> None:
    """Valid HTML attribute styles must all reach the built-link checker."""

    references = extract_built_references(
        "<a href='single/'>one</a>\n"
        "<img src=unquoted.png>\n"
        "<a\n  class='card'\n  href=\"multiline/\">three</a>\n"
    )

    assert [(reference.target, reference.line_number) for reference in references] == [
        ("single/", 1),
        ("unquoted.png", 2),
        ("multiline/", 3),
    ]


def test_single_quoted_broken_link_is_reported(tmp_path: Path) -> None:
    """Single-quoted attributes cannot bypass built-link validation."""

    _write(tmp_path, "index.html", "<a href='missing/'>Gone</a>")

    broken = find_broken_links(tmp_path)

    assert len(broken) == 1
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
    (tmp_path / "sitemap.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.org/opi-wiki/</loc></url>
  <url><loc>https://example.org/opi-wiki/resources/</loc></url>
</urlset>
""",
        encoding="utf-8",
    )

    assert find_broken_links(tmp_path) == []


def test_absolute_link_cannot_drop_an_arbitrary_first_segment(tmp_path: Path) -> None:
    """A broken root URL must not validate merely because the site root exists."""

    _write(tmp_path, "index.html", '<a href="/missing/">Missing</a>')

    broken = find_broken_links(tmp_path)

    assert len(broken) == 1
    assert "/missing/" in broken[0]


def test_sitemap_base_path_discovery_handles_root_and_missing_sitemaps(tmp_path: Path) -> None:
    """Deployment base discovery should be explicit and safe by default."""

    assert discover_site_base_path(tmp_path) == "/"
    assert load_sitemap_locations(tmp_path) == []

    (tmp_path / "sitemap.xml").write_text(
        "<urlset><url><loc>https://example.org/</loc></url>"
        "<url><loc>https://example.org/resources/</loc></url></urlset>",
        encoding="utf-8",
    )

    assert discover_site_base_path(tmp_path) == "/"


def test_sitemap_base_path_discovery_rejects_an_empty_sitemap(tmp_path: Path) -> None:
    """An existing but unusable sitemap should fail instead of weakening resolution."""

    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text("<urlset></urlset>", encoding="utf-8")

    with pytest.raises(RuntimeError, match=r"Built sitemap contains no URL locations"):
        discover_site_base_path(tmp_path)


def test_relative_link_escaping_site_is_rejected_even_when_target_exists(tmp_path: Path) -> None:
    """A link must never validate against a file outside the publish root."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (tmp_path / "private.html").write_text("private", encoding="utf-8")
    _write(site_dir, "index.html", '<a href="../private.html">Private</a>')

    broken = find_broken_links(site_dir)

    assert len(broken) == 1
    assert "escapes built site" in broken[0]


def test_encoded_path_escape_is_rejected(tmp_path: Path) -> None:
    """Percent encoding must not hide a traversal outside the built site."""

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (tmp_path / "private.html").write_text("private", encoding="utf-8")
    _write(site_dir, "index.html", '<a href="%2e%2e/private.html">Private</a>')

    assert "escapes built site" in find_broken_links(site_dir)[0]


def test_main_reports_a_missing_site_directory(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI should return failure instead of raising for a missing build."""

    missing = tmp_path / "missing"

    assert main(["check_built_links.py", str(missing)]) == 1
    assert "site directory not found" in capsys.readouterr().out


def test_main_reports_success_for_a_valid_site(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI should return success for a fully resolved built site."""

    _write(tmp_path, "index.html", "<p>Home</p>")

    assert main(["check_built_links.py", str(tmp_path)]) == 0
    assert "Built-site internal links OK" in capsys.readouterr().out


def test_unreadable_built_html_raises_a_contextual_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A built-file IO failure should identify the affected HTML page."""

    html_file = tmp_path / "index.html"
    html_file.write_text("<h1>Home</h1>", encoding="utf-8")

    def fail_read(path: Path, *, encoding: str, errors: str) -> str:
        assert path == html_file
        assert encoding == "utf-8"
        assert errors == "replace"
        raise OSError("read failed")

    monkeypatch.setattr(Path, "read_text", fail_read)

    with pytest.raises(RuntimeError, match=r"Unable to read built HTML file: .*index\.html"):
        find_broken_links(tmp_path)


def test_main_reports_broken_links(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI should list broken targets and return failure."""

    _write(tmp_path, "index.html", '<a href="missing/">Missing</a>')

    assert main(["check_built_links.py", str(tmp_path)]) == 1
    output = capsys.readouterr().out
    assert "1 broken internal link(s)" in output
    assert "missing/" in output


def test_main_reports_an_unexpected_crawl_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A crawler IO error should become a concise CLI failure."""

    def fail_crawl(_site_dir: Path) -> list[str]:
        raise RuntimeError("read failed")

    monkeypatch.setattr(built_links_cli, "find_broken_links", fail_crawl)

    assert main(["check_built_links.py", str(tmp_path)]) == 1
    assert capsys.readouterr().out == "[check_built_links] read failed\n"
