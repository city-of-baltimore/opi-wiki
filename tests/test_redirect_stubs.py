"""Tests for the static redirect-stub check and the site build."""

from __future__ import annotations

import html
import json
from pathlib import Path

import pytest
from scripts import build_redirect_site
from scripts.repo_tools.redirect_stubs import (
    ADDRESSES_FILE,
    NEW_HOME,
    OLD_BASE,
    STUBS_DIR,
    find_redirect_stub_issues,
    is_new_home_page,
    read_addresses,
    stub_file,
    stub_target,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

NOT_FOUND = (
    "<!doctype html>\n"
    '<html lang="en">\n'
    "<head><title>Moved</title></head>\n"
    f'<body><main><h1>Moved</h1><a href="{NEW_HOME}">OPI Foundations</a></main></body>\n'
    "</html>\n"
)


def _stub(url: str) -> str:
    """Return one stub exactly as opi-publications' builder writes it."""

    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '    <meta charset="utf-8">\n'
        "    <title>Redirecting...</title>\n"
        f'    <link rel="canonical" href="{html.escape(url)}">\n'
        "    <script>var anchor=window.location.hash.substr(1);"
        f'location.href="{json.dumps(url)[1:-1]}"+(anchor?"#"+anchor:"")</script>\n'
        f'    <meta http-equiv="refresh" content="0; url={html.escape(url)}">\n'
        "</head>\n"
        "<body>\n"
        f'OPI Foundations has moved to <a href="{html.escape(url)}">a new address</a>.\n'
        "</body>\n"
        "</html>\n"
    )


def _site(tmp_path: Path, stubs: dict[str, str]) -> Path:
    """Write a small repository with an address list, its stubs and a 404 page."""

    (tmp_path / ADDRESSES_FILE).parent.mkdir(parents=True)
    (tmp_path / ADDRESSES_FILE).write_text("".join(f"{a}\n" for a in sorted(stubs)))
    for address, url in stubs.items():
        stub = tmp_path / STUBS_DIR / stub_file(address)
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(_stub(url))
    (tmp_path / STUBS_DIR / "404.html").write_text(NOT_FOUND)
    return tmp_path


SMALL = {OLD_BASE: NEW_HOME, f"{OLD_BASE}about-us/": f"{NEW_HOME}about-us/"}


def test_the_committed_site_passes() -> None:
    """The stubs in this repository match its old address list, one for one."""

    assert find_redirect_stub_issues(REPO_ROOT) == []


def test_the_committed_list_holds_every_old_address() -> None:
    """88 sitemap pages and 161 legacy redirects: 249 addresses, all distinct."""

    addresses, issues = read_addresses(REPO_ROOT / ADDRESSES_FILE)

    assert issues == []
    assert len(addresses) == 249
    assert addresses[0] == OLD_BASE


def test_this_template_is_the_builders() -> None:
    """The test's stub must be byte-identical to a committed one, or the tests prove nothing."""

    committed = (REPO_ROOT / STUBS_DIR / "about-us" / "index.html").read_text()

    assert committed == _stub(f"{NEW_HOME}about-us/")
    assert stub_target(committed) == f"{NEW_HOME}about-us/"


def test_a_small_clean_site_passes(tmp_path: Path) -> None:
    """The check accepts a site that matches its list."""

    assert find_redirect_stub_issues(_site(tmp_path, SMALL)) == []


def test_a_missing_stub_is_reported(tmp_path: Path) -> None:
    """An old address without a stub would 404 on the published site."""

    repo = _site(tmp_path, SMALL)
    (repo / STUBS_DIR / "about-us" / "index.html").unlink()

    issues = find_redirect_stub_issues(repo)

    assert any("about-us/index.html: no stub for this old address" in i for i in issues)


def test_an_extra_file_is_reported(tmp_path: Path) -> None:
    """Nothing is published that the old address list doesn't name."""

    repo = _site(tmp_path, SMALL)
    (repo / STUBS_DIR / "notes.txt").write_text("draft\n")

    issues = find_redirect_stub_issues(repo)

    assert issues == [f"{repo / STUBS_DIR}/notes.txt: not on the old address list"]


def test_a_stub_whose_urls_disagree_is_reported(tmp_path: Path) -> None:
    """A hand edit to the script alone would split readers with and without JavaScript."""

    repo = _site(tmp_path, SMALL)
    stub = repo / STUBS_DIR / "about-us" / "index.html"
    stub.write_text(
        stub.read_text().replace(
            f'location.href="{NEW_HOME}about-us/"', f'location.href="{NEW_HOME}"'
        )
    )

    issues = find_redirect_stub_issues(repo)

    assert issues == [
        f"{OLD_BASE}about-us/: its stub is not the builder's template with one target URL"
    ]


def test_page_text_added_to_a_stub_is_reported(tmp_path: Path) -> None:
    """Stubs hold no page text; anything added breaks the template."""

    repo = _site(tmp_path, SMALL)
    stub = repo / STUBS_DIR / "index.html"
    stub.write_text(stub.read_text().replace("</body>", "<p>Staff contacts</p>\n</body>"))

    assert len(find_redirect_stub_issues(repo)) == 1


def test_a_target_outside_the_new_home_is_reported(tmp_path: Path) -> None:
    """Every stub must send readers to a page under OPI Foundations."""

    repo = _site(tmp_path, {**SMALL, f"{OLD_BASE}about-us/": "https://example.com/about-us/"})

    issues = find_redirect_stub_issues(repo)

    assert issues == [
        f"{OLD_BASE}about-us/: its stub sends readers to https://example.com/about-us/, "
        f"outside {NEW_HOME}"
    ]


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (NEW_HOME, True),
        (f"{NEW_HOME}what-we-do/programs/citistat/portfolio/311-stat/", True),
        (f"{NEW_HOME}about-us", False),
        (f"{NEW_HOME}about-us/?next=/", False),
        (f"{NEW_HOME}about-us/#mission", False),
        ("http://opi-publications.fly.dev/foundations/", False),
        ("https://opi-publications.fly.dev.example.com/foundations/", False),
        ("https://opi-publications.fly.dev/foundationsx/", False),
        (f"{NEW_HOME}About-Us/", False),
    ],
)
def test_only_directory_pages_under_the_new_home_qualify(url: str, expected: bool) -> None:
    """The target must be a plain page address: https, the right host, no query or fragment."""

    assert is_new_home_page(url) is expected


def test_the_404_page_must_link_home_and_stay_put(tmp_path: Path) -> None:
    """An unknown address has no right destination, so the 404 page never redirects."""

    repo = _site(tmp_path, SMALL)
    page = repo / STUBS_DIR / "404.html"
    page.write_text(
        NOT_FOUND.replace(NEW_HOME, "https://example.com/").replace(
            "</head>", '<meta http-equiv="refresh" content="0; url=/"></head>'
        )
    )

    issues = find_redirect_stub_issues(repo)

    assert any("does not link to" in issue for issue in issues)
    assert any("redirects by itself" in issue for issue in issues)


def test_a_missing_404_page_is_reported(tmp_path: Path) -> None:
    """Without it, unknown addresses get GitHub's bare 404."""

    repo = _site(tmp_path, SMALL)
    (repo / STUBS_DIR / "404.html").unlink()

    issues = find_redirect_stub_issues(repo)

    assert any("404.html: no stub" in issue for issue in issues)
    assert any("404.html is missing" in issue for issue in issues)


@pytest.mark.parametrize(
    ("lines", "problem"),
    [
        ([f"{OLD_BASE}b/", f"{OLD_BASE}a/"], "not sorted"),
        ([f"{OLD_BASE}a/", f"{OLD_BASE}a/"], "listed more than once"),
        ([f"{OLD_BASE}a"], "not a directory address"),
        (["https://example.com/opi-wiki/a/"], "not a directory address"),
    ],
)
def test_a_malformed_address_list_is_reported(
    tmp_path: Path, lines: list[str], problem: str
) -> None:
    """The list is the independent half of the check, so it is held to its own shape."""

    path = tmp_path / "old-addresses.txt"
    path.write_text("".join(f"{line}\n" for line in lines))

    _addresses, issues = read_addresses(path)

    assert any(problem in issue for issue in issues)


def test_the_build_copies_the_stubs_exactly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """site/ is a byte-for-byte copy of the stubs, replacing whatever was there."""

    repo = _site(tmp_path, SMALL)
    site = repo / "site"
    (site / "old").mkdir(parents=True)
    (site / "old" / "index.html").write_text("stale MkDocs output\n")
    monkeypatch.setattr(build_redirect_site, "SOURCE", repo / STUBS_DIR)
    monkeypatch.setattr(build_redirect_site, "SITE", site)

    assert build_redirect_site.main() == 0

    copied = {
        p.relative_to(site).as_posix(): p.read_bytes() for p in site.rglob("*") if p.is_file()
    }
    source = {
        p.relative_to(repo / STUBS_DIR).as_posix(): p.read_bytes()
        for p in (repo / STUBS_DIR).rglob("*")
        if p.is_file()
    }
    assert copied == source
    assert find_redirect_stub_issues(repo, site_dir=Path("site")) == []


def test_the_cli_passes_on_the_committed_site(capsys: pytest.CaptureFixture[str]) -> None:
    """The ci step's command line reports success on this repository's stubs."""

    from scripts import check_redirect_stubs

    assert check_redirect_stubs.main([]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Every old wiki address has one clean stub to OPI Foundations.\n"
    assert captured.err == ""


def test_the_cli_reports_a_missing_site(capsys: pytest.CaptureFixture[str]) -> None:
    """The pre-push step fails, by name, when site/ was never built."""

    from scripts import check_redirect_stubs

    assert check_redirect_stubs.main(["--site-dir", "no-such-site"]) == 1
    assert "no-such-site is not a directory" in capsys.readouterr().err
