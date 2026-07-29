#!/usr/bin/env python3
"""CLI entry point for Patapsco platform-gate evidence validation."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()


def main() -> int:
    """Validate the exact pin, measurement marker, docs, and update isolation."""

    from scripts.repo_tools.platform_guard_evidence import (
        find_platform_guard_evidence_issues,
    )

    result: int = run_issue_check(
        check_name="Platform guard evidence validation",
        success_message="Platform guard evidence validated.",
        issue_finder=lambda: find_platform_guard_evidence_issues(REPO_ROOT),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
