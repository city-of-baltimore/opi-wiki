#!/usr/bin/env python3
"""CLI entry point for raw HTML link validation."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

DOCS_DIR = REPO_ROOT / "docs"


def main() -> int:
    """Run the raw HTML link validator and emit human-readable failures."""

    from scripts.repo_tools.html_links import find_unresolved_html_links

    result: int = run_issue_check(
        check_name="Raw HTML link validation",
        success_message="Raw HTML links validated.",
        issue_finder=lambda: find_unresolved_html_links(DOCS_DIR),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
