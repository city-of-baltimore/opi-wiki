"""Tests for the header-cleanup CLI workflow helpers."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

from scripts.check_cli import build_logger
from scripts.cleanup_doc_headers import scan_headers, write_headers


def test_scan_headers_reports_findings_to_stderr(tmp_path: Path) -> None:
    """Scan mode should report boilerplate findings without editing files."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    markdown_file = docs_dir / "sample.md"
    markdown_file.write_text(
        "# Sample\n\n"
        "Mayor's Office of Performance and Innovation\n"
        "Real content stays here.\n",
        encoding="utf-8",
    )

    stdout = StringIO()
    stderr = StringIO()
    logger = build_logger(stdout=stdout, stderr=stderr)

    exit_code = scan_headers(docs_dir=docs_dir, logger=logger)

    assert exit_code == 1
    assert stdout.getvalue() == ""
    assert "office-line" in stderr.getvalue()
    assert "Mayor's Office of Performance and Innovation" in stderr.getvalue()


def test_write_headers_updates_files_and_reports_count(tmp_path: Path) -> None:
    """Write mode should clean files in place and log the updated-file count."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    markdown_file = docs_dir / "sample.md"
    markdown_file.write_text(
        "# Sample\n\n"
        "Mayor's Office of Performance and Innovation\n"
        "Real content stays here.\n",
        encoding="utf-8",
    )

    stdout = StringIO()
    stderr = StringIO()
    logger = build_logger(stdout=stdout, stderr=stderr)

    exit_code = write_headers(docs_dir=docs_dir, logger=logger)

    assert exit_code == 0
    assert stdout.getvalue() == "Updated 1 Markdown files.\n"
    assert stderr.getvalue() == ""
    assert "Mayor's Office of Performance and Innovation" not in markdown_file.read_text(
        encoding="utf-8"
    )
