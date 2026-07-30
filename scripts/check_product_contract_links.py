#!/usr/bin/env python3
"""CLI entry point for root product-contract link validation."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()


def main() -> int:
    """Validate repository-local links in root product contracts."""

    from scripts.repo_tools.product_contract_links import (
        find_product_contract_link_issues,
    )

    result: int = run_issue_check(
        check_name="Product contract link validation",
        success_message="Product contract links validated.",
        issue_finder=lambda: find_product_contract_link_issues(REPO_ROOT),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
