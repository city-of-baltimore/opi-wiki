#!/usr/bin/env python3
"""CLI entry point for lightweight accessibility smoke checks."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


SITE_DIR = REPO_ROOT / "site"


def main() -> int:
    """Validate a few high-signal accessibility invariants in built HTML."""

    try:
        from scripts.repo_tools.accessibility import find_accessibility_issues

        issues = find_accessibility_issues(SITE_DIR)
    except Exception as error:  # noqa: BLE001
        print(f"Accessibility smoke check failed unexpectedly: {error}", file=sys.stderr)
        return 1

    if issues:
        print("Accessibility smoke check failed:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print("Accessibility smoke check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
