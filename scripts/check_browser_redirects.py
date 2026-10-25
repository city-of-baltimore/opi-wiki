#!/usr/bin/env python3
"""Follow every old wiki address in Chromium, offline, to its new page."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

try:
    from check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, ensure_repo_root_on_path, run_issue_check

ensure_repo_root_on_path()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the browser redirect check."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=Path("site"),
        help="The built site to serve at the wiki's address. Defaults to ./site.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Report every old address a real browser does not land as built."""

    from scripts.repo_tools import browser_redirects

    args = parse_args(argv)
    result: int = run_issue_check(
        check_name="Browser redirect check",
        success_message=(
            "Every old wiki address lands on its OPI Foundations page in Chromium, "
            "with and without JavaScript, and the 404 page passes axe."
        ),
        issue_finder=lambda: browser_redirects.find_browser_redirect_issues(
            REPO_ROOT, args.site_dir
        ),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
