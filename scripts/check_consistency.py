#!/usr/bin/env python3
"""CLI entry point for the OPI wiki consistency checks."""

from __future__ import annotations

import sys
from collections.abc import Sequence

try:
    from check_cli import ensure_repo_root_on_path
except ModuleNotFoundError:
    from scripts.check_cli import ensure_repo_root_on_path

ensure_repo_root_on_path()


def main(argv: Sequence[str] | None = None) -> int:
    """Run consistency checks and return a shell-compatible exit code."""

    from scripts.repo_tools import consistency as consistency_logic

    arguments = sys.argv[1:] if argv is None else argv
    try:
        scan = consistency_logic.scan_consistency()
    except RuntimeError as error:
        print(f"[consistency] {error}")
        return 1

    report, exit_code = consistency_logic.format_consistency_report(
        scan,
        show_acronyms="--acronyms" in arguments or "-a" in arguments,
    )
    print(report)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
