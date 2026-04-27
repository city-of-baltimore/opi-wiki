"""Tests for shared check-script CLI helpers."""

from __future__ import annotations

import pytest
from scripts.check_cli import build_logger, run_issue_check


def test_run_issue_check_reports_success(capsys: pytest.CaptureFixture[str]) -> None:
    """Successful checks should log a single success message to stdout."""

    logger = build_logger()

    exit_code = run_issue_check(
        check_name="Example check",
        success_message="Example check passed.",
        issue_finder=lambda: [],
        logger=logger,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Example check passed.\n"
    assert captured.err == ""


def test_run_issue_check_reports_findings(capsys: pytest.CaptureFixture[str]) -> None:
    """Checks with findings should write the heading and bullets to stderr."""

    logger = build_logger()

    exit_code = run_issue_check(
        check_name="Example check",
        success_message="Example check passed.",
        issue_finder=lambda: ["first issue", "second issue"],
        logger=logger,
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == (
        "Example check failed:\n"
        "  - first issue\n"
        "  - second issue\n"
    )


def test_run_issue_check_reports_unexpected_errors(capsys: pytest.CaptureFixture[str]) -> None:
    """Unexpected exceptions should be surfaced as a single stderr line."""

    logger = build_logger()

    def raise_error() -> list[str]:
        """Raise a predictable exception for the test."""

        raise RuntimeError("boom")

    exit_code = run_issue_check(
        check_name="Example check",
        success_message="Example check passed.",
        issue_finder=raise_error,
        logger=logger,
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "Example check failed unexpectedly: boom\n"
