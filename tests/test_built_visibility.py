"""Tests for canonical built-content visibility enforcement."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.check_built_visibility as built_visibility_cli
import scripts.repo_tools.built_visibility as built_visibility
from scripts.repo_tools.built_visibility import find_built_visibility_issues


def _page_html(content: str, *, outside: str = "") -> str:
    """Return a minimal built page with one canonical content article."""

    return (
        "<html>\n"
        f"{outside}"
        '<article class="md-content__inner md-typeset">\n'
        f"{content}"
        "</article>\n"
        "</html>\n"
    )


def _write_sitemap(site_dir: Path, routes: tuple[str, ...]) -> None:
    """Write canonical URLs under a non-root deployment base."""

    locations = "\n".join(
        f"<url><loc>https://example.test/wiki{route}</loc></url>" for route in routes
    )
    (site_dir / "sitemap.xml").write_text(
        f"<urlset>\n{locations}\n</urlset>\n",
        encoding="utf-8",
    )


def _write_built_page(site_dir: Path, route: str, html: str) -> Path:
    """Write one pretty-URL HTML page and return its path."""

    built_file = (
        site_dir / "index.html" if route == "/" else site_dir / route.strip("/") / "index.html"
    )
    built_file.parent.mkdir(parents=True, exist_ok=True)
    built_file.write_text(html, encoding="utf-8")
    return built_file


def _root_fixture(tmp_path: Path, html: str) -> tuple[Path, Path]:
    """Create a one-route site and its canonical Markdown source."""

    site_dir = tmp_path / "site"
    docs_dir = tmp_path / "docs"
    site_dir.mkdir()
    docs_dir.mkdir()
    _write_sitemap(site_dir, ("/",))
    _write_built_page(site_dir, "/", html)
    (docs_dir / "index.md").write_text("# Home\n", encoding="utf-8")
    return site_dir, docs_dir


def _add_route(
    site_dir: Path,
    docs_dir: Path,
    route: str,
    html: str,
    source: str,
) -> None:
    """Add one canonical subroute and its selected source form."""

    _write_sitemap(site_dir, ("/", route))
    _write_built_page(site_dir, route, html)
    source_file = docs_dir / source
    source_file.parent.mkdir(parents=True, exist_ok=True)
    source_file.write_text("# Page\n", encoding="utf-8")


def test_built_visibility_accepts_current_canonical_content(tmp_path: Path) -> None:
    """Ordinary civic language in one canonical page should pass."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html("<p>Approved users publish governed public data.</p>\n"),
    )

    assert find_built_visibility_issues(site_dir, docs_dir) == []


def test_built_visibility_reports_rendered_phrase_with_complete_evidence(
    tmp_path: Path,
) -> None:
    """Markup cannot hide a retired label or weaken its built-file evidence."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html("<p>Use the public <strong>site</strong>.</p>\n"),
    )

    assert find_built_visibility_issues(site_dir, docs_dir) == [
        "index.html:3:12: route /; page source docs/index.md; "
        "context 'article.md-content__inner > p:nth-of-type(1)'; "
        "retired visibility label 'public site'"
    ]


@pytest.mark.parametrize(
    "attribute",
    ('srcdoc="public site"', 'src="/embedded-guide/"'),
)
def test_built_visibility_fails_closed_on_macro_generated_iframe_document(
    tmp_path: Path,
    attribute: str,
) -> None:
    """Embedded built output must not evade checks when source fragments were clean."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html(f"<iframe {attribute}></iframe>\n"),
    )

    with pytest.raises(RuntimeError, match="iframe embedded document"):
        find_built_visibility_issues(site_dir, docs_dir)


def test_built_visibility_scans_hooks_in_raw_html_but_only_page_content_for_labels(
    tmp_path: Path,
) -> None:
    """Theme text is not page prose, while a retired built hook still fails."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html(
            "<p>Current page content.</p>\n",
            outside=(
                '<nav>public <strong>site</strong></nav>\n<span class="opi-pill">Legacy</span>\n'
            ),
        ),
    )

    assert find_built_visibility_issues(site_dir, docs_dir) == [
        "index.html:3:14: route /; page source docs/index.md; "
        "context 'raw built HTML'; retired presentation hook 'opi-pill'"
    ]


@pytest.mark.parametrize("source", ("guide.md", "guide/index.md"))
def test_built_visibility_maps_pretty_routes_to_the_one_real_source(
    tmp_path: Path,
    source: str,
) -> None:
    """Both supported MkDocs source shapes should map without theme metadata."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html("<p>Current home content.</p>\n"),
    )
    _add_route(
        site_dir,
        docs_dir,
        "/guide/",
        _page_html("<p>A public <em>site</em>.</p>\n"),
        source,
    )

    issues = find_built_visibility_issues(site_dir, docs_dir)

    assert len(issues) == 1
    assert "route /guide/" in issues[0]
    assert f"page source docs/{source}" in issues[0]


def test_built_visibility_scopes_director_letter_headings_to_heading_content(
    tmp_path: Path,
) -> None:
    """Rendered heading policy must not turn ordinary body prose into a label."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html("<p>Current home content.</p>\n"),
    )
    _add_route(
        site_dir,
        docs_dir,
        "/about-us/letters-from-the-director/example/",
        _page_html(
            "<h2>Public <em>Purpose</em></h2>\n"
            "<p>Public Purpose is also an ordinary governance phrase.</p>\n"
        ),
        "about-us/letters-from-the-director/example.md",
    )

    issues = find_built_visibility_issues(site_dir, docs_dir)

    assert len(issues) == 1
    assert "context 'article.md-content__inner > h2:nth-of-type(1)'" in issues[0]
    assert "retired visibility label 'Public Purpose'" in issues[0]


def test_built_visibility_allows_public_purpose_heading_outside_director_letters(
    tmp_path: Path,
) -> None:
    """The scoped historical heading remains valid elsewhere in the site."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html("<h2>Public <em>Purpose</em></h2>\n"),
    )

    assert find_built_visibility_issues(site_dir, docs_dir) == []


def test_built_visibility_requires_site_and_docs_directories(tmp_path: Path) -> None:
    """Neither missing input root may produce a vacuous pass."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    with pytest.raises(FileNotFoundError, match="Built site directory was not found"):
        find_built_visibility_issues(tmp_path / "missing-site", docs_dir)

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    with pytest.raises(FileNotFoundError, match="Documentation source directory was not found"):
        find_built_visibility_issues(site_dir, tmp_path / "missing-docs")


def test_built_visibility_requires_sitemap_routes(tmp_path: Path) -> None:
    """A missing sitemap cannot silently remove every canonical page."""

    site_dir = tmp_path / "site"
    docs_dir = tmp_path / "docs"
    site_dir.mkdir()
    docs_dir.mkdir()

    with pytest.raises(RuntimeError, match="Built sitemap contains no canonical routes"):
        find_built_visibility_issues(site_dir, docs_dir)


def test_built_visibility_requires_each_canonical_html_file(tmp_path: Path) -> None:
    """A sitemap route without its built page should fail closed."""

    site_dir = tmp_path / "site"
    docs_dir = tmp_path / "docs"
    site_dir.mkdir()
    docs_dir.mkdir()
    _write_sitemap(site_dir, ("/",))
    (docs_dir / "index.md").write_text("# Home\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="Canonical built HTML file was not found"):
        find_built_visibility_issues(site_dir, docs_dir)


def test_built_visibility_rejects_unresolved_and_ambiguous_page_sources(
    tmp_path: Path,
) -> None:
    """Every canonical route must have exactly one deterministic source."""

    site_dir = tmp_path / "site"
    docs_dir = tmp_path / "docs"
    site_dir.mkdir()
    docs_dir.mkdir()
    _write_sitemap(site_dir, ("/",))
    _write_built_page(site_dir, "/", _page_html("<p>Current.</p>\n"))

    with pytest.raises(FileNotFoundError, match="has no Markdown source"):
        find_built_visibility_issues(site_dir, docs_dir)

    (docs_dir / "index.md").write_text("# Home\n", encoding="utf-8")
    guide = docs_dir / "guide"
    guide.mkdir()
    (docs_dir / "guide.md").write_text("# Guide\n", encoding="utf-8")
    (guide / "index.md").write_text("# Guide\n", encoding="utf-8")
    _write_sitemap(site_dir, ("/", "/guide/"))
    _write_built_page(site_dir, "/guide/", _page_html("<p>Current.</p>\n"))

    with pytest.raises(RuntimeError, match="has ambiguous Markdown sources"):
        find_built_visibility_issues(site_dir, docs_dir)


def test_built_visibility_requires_strict_utf8_html(tmp_path: Path) -> None:
    """Malformed output bytes must name the canonical route and built file."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html("<p>Current.</p>\n"),
    )
    (site_dir / "index.html").write_bytes(b"\xff")

    with pytest.raises(RuntimeError, match=r"not valid UTF-8 for route /: .*index\.html"):
        find_built_visibility_issues(site_dir, docs_dir)


@pytest.mark.parametrize(
    "html",
    (
        "<html><p>No content article.</p></html>",
        _page_html("<p>One.</p>\n") + _page_html("<p>Two.</p>\n"),
        '<article class="md-content__inner md-typeset"><p>Unclosed.</p>',
    ),
)
def test_built_visibility_requires_exactly_one_closed_content_projection(
    tmp_path: Path,
    html: str,
) -> None:
    """Malformed or ambiguous content roots must fail with route evidence."""

    site_dir, docs_dir = _root_fixture(tmp_path, html)

    with pytest.raises(RuntimeError, match=r"Unable to project canonical content.*route /"):
        find_built_visibility_issues(site_dir, docs_dir)


def test_built_visibility_rejects_unsafe_canonical_routes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A malformed sitemap route must never escape either input root."""

    site_dir, docs_dir = _root_fixture(
        tmp_path,
        _page_html("<p>Current.</p>\n"),
    )
    monkeypatch.setattr(
        built_visibility,
        "canonical_route_paths",
        lambda _site_dir: ["/../outside/"],
    )

    with pytest.raises(RuntimeError, match="escapes the site root"):
        find_built_visibility_issues(site_dir, docs_dir)


def test_built_visibility_cli_reports_success_and_findings(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The thin CLI should expose both outcomes from the library checker."""

    monkeypatch.setattr(
        built_visibility,
        "find_built_visibility_issues",
        lambda _site, _docs: [],
    )
    assert built_visibility_cli.main() == 0
    captured = capsys.readouterr()
    assert captured.out == "Canonical built content uses current visibility language.\n"
    assert captured.err == ""

    monkeypatch.setattr(
        built_visibility,
        "find_built_visibility_issues",
        lambda _site, _docs: ["fixture built-content issue"],
    )
    assert built_visibility_cli.main() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "fixture built-content issue" in captured.err
