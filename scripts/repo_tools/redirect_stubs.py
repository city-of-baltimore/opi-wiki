"""Check the wiki's final site: one redirect stub per old address.

Ownership: repository tooling for the retired wiki. ``redirects/stubs/`` is the
whole published site. opi-publications' ``build_wiki_redirect_stubs.py`` wrote
its stubs (WIKI-14), and ``404.html`` is written here. ``redirects/
old-addresses.txt`` lists the addresses the wiki served at its import commit,
taken from the wiki's own sitemap and ``redirect_maps`` rather than from
opi-publications' import manifest, so this check compares two independent
sources.

Invariants enforced here:

1. Every old address has exactly one stub, and the tree holds nothing else
   except ``404.html``. A missing stub would 404 a published address; an extra
   file would publish something nobody listed.
2. Every stub is the builder's exact template. Its canonical link, its script,
   its refresh and its body link all name one URL, and that URL is a page under
   the new home. A hand edit that changes one of the four and not the others
   would send readers with and without JavaScript to different places.
3. ``404.html`` links to the new home and redirects nowhere: an unknown address
   has no right destination to guess.

Boundary: this module reads files only. It never requests either site; the
browser check and opi-publications' ``--verify`` do that.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

OLD_BASE = "https://city-of-baltimore.github.io/opi-wiki/"
NEW_ORIGIN = "https://opi-publications.fly.dev"
NEW_HOME = f"{NEW_ORIGIN}/foundations/"
STUBS_DIR = Path("redirects/stubs")
ADDRESSES_FILE = Path("redirects/old-addresses.txt")
NOT_FOUND_PAGE = "404.html"

# The builder's template, character for character, with one group per place
# the target URL appears: canonical, script, refresh and body.
_STUB = re.compile(
    r"<!doctype html>\n"
    r'<html lang="en">\n'
    r"<head>\n"
    r'    <meta charset="utf-8">\n'
    r"    <title>Redirecting\.\.\.</title>\n"
    r'    <link rel="canonical" href="(?P<canonical>[^"<>]+)">\n'
    r"    <script>var anchor=window\.location\.hash\.substr\(1\);"
    r'location\.href="(?P<script>[^"<>\\]+)"\+\(anchor\?"#"\+anchor:""\)</script>\n'
    r'    <meta http-equiv="refresh" content="0; url=(?P<refresh>[^"<>]+)">\n'
    r"</head>\n"
    r"<body>\n"
    r'OPI Foundations has moved to <a href="(?P<body>[^"<>]+)">a new address</a>\.\n'
    r"</body>\n"
    r"</html>\n"
)
_PAGE_PATH = re.compile(r"^/foundations/(?:[a-z0-9]+(?:-[a-z0-9]+)*/)*$")


def read_addresses(path: Path) -> tuple[list[str], list[str]]:
    """Return the old addresses in ``path`` and any problems with the list itself."""

    issues: list[str] = []
    addresses: list[str] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.startswith(OLD_BASE) or not line.endswith("/"):
            issues.append(f"{path}:{number}: {line!r} is not a directory address under {OLD_BASE}")
            continue
        addresses.append(line)
    duplicates = sorted({address for address in addresses if addresses.count(address) > 1})
    issues.extend(f"{path}: {address} is listed more than once" for address in duplicates)
    if addresses != sorted(addresses):
        issues.append(f"{path}: the addresses are not sorted")
    return addresses, issues


def stub_file(address: str) -> str:
    """Return the stub's path inside the site for one old address."""

    return f"{address.removeprefix(OLD_BASE)}index.html"


def stub_target(text: str) -> str | None:
    """Return the one URL a stub sends readers to, or ``None`` if it is not a clean stub."""

    match = _STUB.fullmatch(text)
    if match is None:
        return None
    try:
        script = json.loads(f'"{match["script"]}"')
    except json.JSONDecodeError:
        return None
    urls = {
        html.unescape(match["canonical"]),
        script,
        html.unescape(match["refresh"]),
        html.unescape(match["body"]),
    }
    return urls.pop() if len(urls) == 1 else None


def is_new_home_page(url: str) -> bool:
    """Return whether ``url`` is a directory page under the new home, with nothing else."""

    parts = urlsplit(url)
    return (
        url.startswith(NEW_HOME)
        and parts.scheme == "https"
        and f"{parts.scheme}://{parts.netloc}" == NEW_ORIGIN
        and not parts.query
        and not parts.fragment
        and _PAGE_PATH.fullmatch(parts.path) is not None
    )


def stub_targets(site_dir: Path, addresses: list[str]) -> dict[str, str | None]:
    """Map every old address to the URL its stub sends readers to (``None`` if broken)."""

    targets: dict[str, str | None] = {}
    for address in addresses:
        stub = site_dir / stub_file(address)
        targets[address] = stub_target(stub.read_text(encoding="utf-8")) if stub.is_file() else None
    return targets


def _not_found_page_issues(site_dir: Path) -> list[str]:
    """Check that ``404.html`` points at the new home and goes nowhere by itself."""

    page = site_dir / NOT_FOUND_PAGE
    if not page.is_file():
        return [f"{page} is missing, so unknown addresses get GitHub's bare 404"]
    text = page.read_text(encoding="utf-8")
    issues = []
    if f'<a href="{NEW_HOME}">' not in text:
        issues.append(f"{page} does not link to {NEW_HOME}")
    if "<script" in text or "http-equiv" in text:
        issues.append(f"{page} redirects by itself; an unknown address has no right destination")
    if '<html lang="en">' not in text or "<h1>" not in text or "<title>" not in text:
        issues.append(f"{page} needs its language, a title and a heading")
    return issues


def find_redirect_stub_issues(
    repo_root: Path,
    *,
    site_dir: Path | None = None,
) -> list[str]:
    """Return every way the site at ``site_dir`` differs from the old address list."""

    site = repo_root / (site_dir or STUBS_DIR)
    if not site.is_dir():
        return [f"{site} is not a directory"]
    addresses, issues = read_addresses(repo_root / ADDRESSES_FILE)

    expected = {stub_file(address) for address in addresses} | {NOT_FOUND_PAGE}
    present = {path.relative_to(site).as_posix() for path in site.rglob("*") if path.is_file()}
    issues.extend(
        f"{site}/{name}: no stub for this old address" for name in sorted(expected - present)
    )
    issues.extend(
        f"{site}/{name}: not on the old address list" for name in sorted(present - expected)
    )

    for address, target in stub_targets(site, addresses).items():
        if (site / stub_file(address)).is_file() and target is None:
            issues.append(f"{address}: its stub is not the builder's template with one target URL")
        elif target is not None and not is_new_home_page(target):
            issues.append(f"{address}: its stub sends readers to {target}, outside {NEW_HOME}")

    issues.extend(_not_found_page_issues(site))
    return issues
