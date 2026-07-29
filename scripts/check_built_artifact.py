#!/usr/bin/env python3
"""CLI entry point for built-artifact safety checks."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

SITE_DIR = REPO_ROOT / "site"


def main() -> int:
    """Reject excluded source files and sensitive fields in built output."""

    from scripts.repo_tools.built_artifact import find_built_artifact_issues

    result: int = run_issue_check(
        check_name="Built-artifact safety check",
        success_message="Built-artifact safety check passed.",
        issue_finder=lambda: find_built_artifact_issues(SITE_DIR),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
