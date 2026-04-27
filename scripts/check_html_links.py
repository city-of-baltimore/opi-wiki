#!/usr/bin/env python3
"""CLI entry point for raw HTML link validation."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DOCS_DIR = REPO_ROOT / "docs"


def main() -> int:
    """Run the raw HTML link validator and emit human-readable failures."""

    try:
        from scripts.repo_tools.html_links import find_unresolved_html_links

        errors = find_unresolved_html_links(DOCS_DIR)
    except Exception as error:  # noqa: BLE001
        print(f"Raw HTML link validation failed unexpectedly: {error}", file=sys.stderr)
        return 1

    if errors:
        print("Raw HTML link validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("Raw HTML links validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
