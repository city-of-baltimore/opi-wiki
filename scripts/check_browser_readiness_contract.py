#!/usr/bin/env python3
"""CLI entry point for the browser readiness source contract."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()


def main() -> int:
    """Require all browser navigation to use the live-preview-safe shared seam."""

    from scripts.repo_tools.browser_readiness_contract import (
        find_browser_readiness_contract_issues,
    )

    result: int = run_issue_check(
        check_name="Browser readiness source contract",
        success_message="Browser readiness is centralized and live-preview safe.",
        issue_finder=lambda: find_browser_readiness_contract_issues(REPO_ROOT),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
