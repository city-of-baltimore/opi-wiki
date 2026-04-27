#!/usr/bin/env python3
"""CLI entry point for editorial brand-term validation."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


SCAN_PATHS = [
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "README.md",
    REPO_ROOT / "CONTRIBUTING.md",
    REPO_ROOT / "MAINTAINERS.md",
    *sorted((REPO_ROOT / "docs").rglob("*.md")),
]


def main() -> int:
    """Check editorial Markdown for discouraged brand-term casing."""

    try:
        from scripts.repo_tools.brand_terms import find_brand_term_issues

        issues = find_brand_term_issues(SCAN_PATHS)
    except Exception as error:  # noqa: BLE001
        print(f"Brand-term validation failed unexpectedly: {error}", file=sys.stderr)
        return 1

    if issues:
        print("Brand-term validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print("Brand terms validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
