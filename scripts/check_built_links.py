#!/usr/bin/env python3
"""Check the built MkDocs site for broken internal links.

`mkdocs build --strict` validates Markdown links but NOT macro-generated card
hrefs or raw-HTML hrefs. This crawls the built HTML and flags internal links or
assets that do not resolve to a file, catching card-grid depth bugs that strict
and the Markdown-only checks miss.

Usage: python scripts/check_built_links.py [site_dir]   (default: site)
"""

from __future__ import annotations

import pathlib
import re
import sys

_HREF = re.compile(r'(?:href|src)="([^"]+)"')
_SKIP_PREFIXES = (
    "http://", "https://", "mailto:", "tel:", "//", "data:", "javascript:", "#",
)


def find_broken_links(site_dir: pathlib.Path) -> list[str]:
    broken: set[str] = set()
    for html in site_dir.rglob("*.html"):
        for raw in _HREF.findall(html.read_text(encoding="utf-8", errors="ignore")):
            if raw.startswith(_SKIP_PREFIXES):
                continue
            path = raw.split("#", 1)[0].split("?", 1)[0]
            if not path or not re.search(r"[A-Za-z0-9]", path):
                continue  # bare "&", empty, etc.
            if path.startswith("/"):
                # Absolute links (e.g. Material's 404 page) are emitted from
                # site_url and carry the deploy base path (/opi-wiki/...). Accept
                # the link if it resolves with or without that leading base segment.
                rel = path.lstrip("/")
                parts = rel.split("/")
                candidates = [site_dir / rel]
                if len(parts) > 1:
                    candidates.append(site_dir / "/".join(parts[1:]))
            else:
                candidates = [(html.parent / path).resolve()]
            if any(
                c.exists() or (c.suffix == "" and (c / "index.html").exists())
                for c in candidates
            ):
                continue
            broken.add(f"{html.relative_to(site_dir)}  ->  {raw}")
    return sorted(broken)


def main(argv: list[str]) -> int:
    site_dir = pathlib.Path(argv[1] if len(argv) > 1 else "site")
    if not site_dir.is_dir():
        print(f"[check_built_links] site directory not found: {site_dir}")
        return 1
    broken = find_broken_links(site_dir)
    if broken:
        print(f"[check_built_links] {len(broken)} broken internal link(s):")
        for line in broken:
            print(f"  {line}")
        return 1
    print("[check_built_links] Built-site internal links OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
