#!/usr/bin/env python3
"""Run browser smoke checks against the built documentation site."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
else:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()

from scripts.repo_tools.browser_smoke import find_browser_smoke_issues  # noqa: E402

SITE_DIR = REPO_ROOT / "site"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for browser smoke checks."""

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
    """Run browser smoke checks from the command line."""

    args = parse_args(argv)
    return run_issue_check(
        check_name="Browser smoke check",
        success_message="Browser smoke check passed.",
        issue_finder=lambda: find_browser_smoke_issues(args.site_dir, base_url=args.base_url),
    )


if __name__ == "__main__":
    raise SystemExit(main())
