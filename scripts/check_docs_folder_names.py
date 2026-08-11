#!/usr/bin/env python3
"""CLI entry point for the docs folder-name ignore-collision check."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()


def main() -> int:
    """Reject a docs/ folder name that an ignore rule would silently swallow."""

    from scripts.repo_tools import docs_folder_names

    result: int = run_issue_check(
        check_name="Docs folder-name check",
        success_message="Every docs/ folder name is visible to Git.",
        issue_finder=lambda: docs_folder_names.find_docs_folder_name_issues(REPO_ROOT),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
