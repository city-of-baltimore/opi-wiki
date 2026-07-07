#!/usr/bin/env python3
"""Shared CLI helpers for repo verification entry points."""

from __future__ import annotations

import logging
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TextIO

REPO_ROOT = Path(__file__).resolve().parents[1]


class _MaxLevelFilter(logging.Filter):
    """Allow only log records at or below a maximum level."""

    def __init__(self, max_level: int) -> None:
        """Store the highest log level that should pass through."""

        super().__init__()
        self.max_level = max_level

    def filter(self, record: logging.LogRecord) -> bool:
        """Return whether the record is below or equal to the configured level."""

        return record.levelno <= self.max_level


IssueFinder = Callable[[], Sequence[str]]


def ensure_repo_root_on_path() -> Path:
    """Add the repository root to ``sys.path`` for direct script execution."""

    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    return REPO_ROOT


def build_logger(
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> logging.Logger:
    """Create a CLI logger that splits info and error output by stream."""

    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr

    logger = logging.Logger("opi.check_cli", level=logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter("%(message)s")

    info_handler = logging.StreamHandler(stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(_MaxLevelFilter(logging.INFO))
    info_handler.setFormatter(formatter)

    error_handler = logging.StreamHandler(stderr)
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    return logger


def run_issue_check(
    *,
    check_name: str,
    success_message: str,
    issue_finder: IssueFinder,
    logger: logging.Logger | None = None,
) -> int:
    """Run a repo check and report success, findings, or unexpected failure."""

    logger = logger or build_logger()

    try:
        issues = list(issue_finder())
    except Exception as error:  # noqa: BLE001
        logger.error("%s failed unexpectedly: %s", check_name, error)
        return 1

    if issues:
        logger.error("%s failed:", check_name)
        for issue in issues:
            logger.error("  - %s", issue)
        return 1

    logger.info(success_message)
    return 0
