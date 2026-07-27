#!/usr/bin/env python3
"""CLI entry point for organization-data validation."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

DOCS_DIR = REPO_ROOT / "docs"


def main() -> int:
    """Validate the canonical organization source against its exact schema."""

    from scripts.repo_tools.organization import find_organization_data_issues

    result: int = run_issue_check(
        check_name="Organization data validation",
        success_message="Organization data validated.",
        issue_finder=lambda: find_organization_data_issues(DOCS_DIR),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
