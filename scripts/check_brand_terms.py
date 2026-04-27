#!/usr/bin/env python3
"""CLI entry point for editorial brand-term validation."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()


SCAN_PATHS = [
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "README.md",
    REPO_ROOT / "CONTRIBUTING.md",
    REPO_ROOT / "MAINTAINERS.md",
    *sorted((REPO_ROOT / "docs").rglob("*.md")),
]


def main() -> int:
    """Check editorial Markdown for discouraged brand-term casing."""

    from scripts.repo_tools.brand_terms import find_brand_term_issues

    return run_issue_check(
        check_name="Brand-term validation",
        success_message="Brand terms validated.",
        issue_finder=lambda: find_brand_term_issues(SCAN_PATHS),
    )


if __name__ == "__main__":
    raise SystemExit(main())
