#!/usr/bin/env python3
"""CLI entry point for canonical built-content visibility checks."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

SITE_DIR = REPO_ROOT / "site"
DOCS_DIR = REPO_ROOT / "docs"


def main() -> int:
    """Reject retired visibility language in canonical built content."""

    from scripts.repo_tools.built_visibility import find_built_visibility_issues

    result: int = run_issue_check(
        check_name="Built-content visibility check",
        success_message="Canonical built content uses current visibility language.",
        issue_finder=lambda: find_built_visibility_issues(SITE_DIR, DOCS_DIR),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
