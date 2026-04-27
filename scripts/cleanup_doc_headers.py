#!/usr/bin/env python3
"""Scan or clean repeated document-cover header noise from Markdown pages."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

try:
    from check_cli import REPO_ROOT, build_logger, ensure_repo_root_on_path
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT, build_logger, ensure_repo_root_on_path

ensure_repo_root_on_path()

DOCS_DIR = REPO_ROOT / "docs"


def _target_files(docs_dir: Path) -> list[Path]:
    """Return Markdown files that should be scanned for header boilerplate."""

    return sorted(docs_dir.rglob("*.md"))


def scan_headers(docs_dir: Path = DOCS_DIR, logger: logging.Logger | None = None) -> int:
    """Report boilerplate findings without modifying files."""

    from scripts.repo_tools.header_cleanup import find_header_changes

    logger = logger or build_logger()
    had_changes = False
    for markdown_file in _target_files(docs_dir):
        try:
            text = markdown_file.read_text(encoding="utf-8")
        except OSError as error:
            logger.error("Unable to read %s: %s", markdown_file, error)
            return 1

        changes = find_header_changes(text, markdown_file)
        if not changes:
            continue

        had_changes = True
        for change in changes:
            relative_file = (
                markdown_file.relative_to(REPO_ROOT)
                if markdown_file.is_relative_to(REPO_ROOT)
                else markdown_file
            )
            logger.warning(
                "%s:%s: %s: %s",
                relative_file,
                change.line_number,
                change.reason,
                change.content.strip(),
            )

    return 1 if had_changes else 0


def write_headers(docs_dir: Path = DOCS_DIR, logger: logging.Logger | None = None) -> int:
    """Apply header cleanup changes in place."""

    from scripts.repo_tools.header_cleanup import apply_header_cleanup

    logger = logger or build_logger()
    updated_files = 0
    for markdown_file in _target_files(docs_dir):
        try:
            text = markdown_file.read_text(encoding="utf-8")
        except OSError as error:
            logger.error("Unable to read %s: %s", markdown_file, error)
            return 1

        cleaned_text, changes = apply_header_cleanup(text, markdown_file)
        if not changes:
            continue

        try:
            markdown_file.write_text(cleaned_text, encoding="utf-8")
        except OSError as error:
            logger.error("Unable to write %s: %s", markdown_file, error)
            return 1

        updated_files += 1

    logger.info("Updated %s Markdown files.", updated_files)
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
    logger = build_logger()

    try:
        return write_headers(logger=logger) if args.write else scan_headers(logger=logger)
    except Exception as error:  # noqa: BLE001
        logger.error("Header cleanup failed unexpectedly: %s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
