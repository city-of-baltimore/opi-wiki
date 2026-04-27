#!/usr/bin/env python3
"""CLI entry point for page metadata validation."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

DOCS_DIR = REPO_ROOT / "docs"


def main() -> int:
    """Validate the review metadata coverage for Markdown pages."""

    from scripts.repo_tools.metadata import find_metadata_issues

    return run_issue_check(
        check_name="Page metadata validation",
        success_message="Page metadata validated.",
        issue_finder=lambda: find_metadata_issues(DOCS_DIR),
    )


if __name__ == "__main__":
    raise SystemExit(main())
