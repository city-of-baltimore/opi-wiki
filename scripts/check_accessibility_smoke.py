#!/usr/bin/env python3
"""CLI entry point for lightweight accessibility smoke checks."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

SITE_DIR = REPO_ROOT / "site"


def main() -> int:
    """Validate a few high-signal accessibility invariants in built HTML."""

    from scripts.repo_tools.accessibility import find_accessibility_issues

    result: int = run_issue_check(
        check_name="Accessibility smoke check",
        success_message="Accessibility smoke check passed.",
        issue_finder=lambda: find_accessibility_issues(SITE_DIR),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
