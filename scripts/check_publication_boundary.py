#!/usr/bin/env python3
"""CLI entry point for built-site publication-boundary checks."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

SITE_DIR = REPO_ROOT / "site"


def main() -> int:
    """Reject private source files and sensitive fields in built output."""

    from scripts.repo_tools.publication import find_publication_boundary_issues

    result: int = run_issue_check(
        check_name="Publication boundary check",
        success_message="Publication boundary check passed.",
        issue_finder=lambda: find_publication_boundary_issues(SITE_DIR),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
