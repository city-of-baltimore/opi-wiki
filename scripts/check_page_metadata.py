#!/usr/bin/env python3
"""CLI entry point for page metadata validation."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DOCS_DIR = REPO_ROOT / "docs"


def main() -> int:
    """Validate the review metadata coverage for Markdown pages."""

    try:
        from scripts.repo_tools.metadata import find_metadata_issues

        issues = find_metadata_issues(DOCS_DIR)
    except Exception as error:  # noqa: BLE001
        print(f"Metadata validation failed unexpectedly: {error}", file=sys.stderr)
        return 1

    if issues:
        print("Page metadata validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print("Page metadata validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
