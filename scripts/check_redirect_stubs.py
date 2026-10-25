#!/usr/bin/env python3
"""CLI entry point for the redirect-stub check: one stub per old address."""

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
    """Parse CLI arguments for the redirect-stub check."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=None,
        help=(
            "The site to check, relative to the repository root. Defaults to the "
            "committed source, redirects/stubs; the pre-push tier passes the built site/."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Reject a site that differs from the old address list or the builder's template."""

    from scripts.repo_tools import redirect_stubs

    args = parse_args(argv)
    result: int = run_issue_check(
        check_name="Redirect-stub check",
        success_message="Every old wiki address has one clean stub to OPI Foundations.",
        issue_finder=lambda: redirect_stubs.find_redirect_stub_issues(
            REPO_ROOT, site_dir=args.site_dir
        ),
    )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
