#!/usr/bin/env python3
"""Run full-browser accessibility assurance against the built documentation site."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

if __package__ in {None, ""}:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
else:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

from scripts.repo_tools.browser_accessibility import (  # noqa: E402
    find_browser_accessibility_issues,
)

SITE_DIR = REPO_ROOT / "site"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for browser accessibility assurance."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        help="Use an already-running site at this base URL instead of serving ./site locally.",
    )
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=SITE_DIR,
        help="Path to a built site directory. Defaults to ./site.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run browser accessibility assurance from the command line."""

    args = parse_args(argv)
    result: int = run_issue_check(
        check_name="Browser accessibility audit",
        success_message="Browser accessibility audit passed across all canonical routes.",
        issue_finder=lambda: find_browser_accessibility_issues(
            args.site_dir,
            base_url=args.base_url,
        ),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
