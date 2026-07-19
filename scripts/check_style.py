#!/usr/bin/env python3
"""CLI entry point for the editorial voice guardrail."""

from __future__ import annotations

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()


SCAN_PATHS = sorted((REPO_ROOT / "docs").rglob("*.md"))


def main() -> int:
    """Check wiki Markdown for prose em-dashes and banned jargon."""

    from scripts.repo_tools.style import find_style_issues

    result: int = run_issue_check(
        check_name="Editorial voice guardrail",
        success_message="Editorial voice guardrail passed.",
        issue_finder=lambda: find_style_issues(SCAN_PATHS),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
