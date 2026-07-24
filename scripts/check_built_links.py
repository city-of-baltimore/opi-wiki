#!/usr/bin/env python3
"""Check the built MkDocs site for broken internal links.

`mkdocs build --strict` validates Markdown links but NOT macro-generated card
hrefs or raw-HTML hrefs. This crawls the built HTML and flags internal links or
assets that do not resolve to a file, catching card-grid depth bugs that strict
and the Markdown-only checks miss.

Usage: python scripts/check_built_links.py [site_dir]   (default: site)
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    from check_cli import ensure_repo_root_on_path
else:
    from scripts.check_cli import ensure_repo_root_on_path

ensure_repo_root_on_path()

from scripts.repo_tools.built_links import find_broken_links  # noqa: E402


def main(argv: list[str]) -> int:
    """Validate a built site and return a shell-compatible exit code."""

    site_dir = Path(argv[1] if len(argv) > 1 else "site")
    if not site_dir.is_dir():
        print(f"[check_built_links] site directory not found: {site_dir}")
        return 1
    try:
        broken = find_broken_links(site_dir)
    except RuntimeError as error:
        print(f"[check_built_links] {error}")
        return 1
    if broken:
        print(f"[check_built_links] {len(broken)} broken internal link(s):")
        for line in broken:
            print(f"  {line}")
        return 1
    print("[check_built_links] Built-site internal links OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
