#!/usr/bin/env python3
"""Scan or clean repeated document-cover header noise from Markdown pages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DOCS_DIR = REPO_ROOT / "docs"


def _target_files() -> list[Path]:
    """Return Markdown files that should be scanned for header boilerplate."""

    return sorted(DOCS_DIR.rglob("*.md"))


def _scan() -> int:
    """Report boilerplate findings without modifying files."""

    from scripts.repo_tools.header_cleanup import find_header_changes

    had_changes = False
    for markdown_file in _target_files():
        try:
            text = markdown_file.read_text(encoding="utf-8")
        except OSError as error:
            print(f"Unable to read {markdown_file}: {error}", file=sys.stderr)
            return 1

        changes = find_header_changes(text, markdown_file)
        if not changes:
            continue

        had_changes = True
        for change in changes:
            relative_file = markdown_file.relative_to(REPO_ROOT)
            print(
                f"{relative_file}:{change.line_number}: "
                f"{change.reason}: {change.content.strip()}"
            )

    return 1 if had_changes else 0


def _write() -> int:
    """Apply header cleanup changes in place."""

    from scripts.repo_tools.header_cleanup import apply_header_cleanup

    updated_files = 0
    for markdown_file in _target_files():
        try:
            text = markdown_file.read_text(encoding="utf-8")
        except OSError as error:
            print(f"Unable to read {markdown_file}: {error}", file=sys.stderr)
            return 1

        cleaned_text, changes = apply_header_cleanup(text, markdown_file)
        if not changes:
            continue

        try:
            markdown_file.write_text(cleaned_text, encoding="utf-8")
        except OSError as error:
            print(f"Unable to write {markdown_file}: {error}", file=sys.stderr)
            return 1

        updated_files += 1

    print(f"Updated {updated_files} Markdown files.")
    return 0


def main() -> int:
    """Parse CLI arguments and run the header cleanup workflow."""

    parser = argparse.ArgumentParser(
        description="Remove repeated document-cover boilerplate from docs pages."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply changes in place instead of reporting findings.",
    )
    args = parser.parse_args()

    try:
        return _write() if args.write else _scan()
    except Exception as error:  # noqa: BLE001
        print(f"Header cleanup failed unexpectedly: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
