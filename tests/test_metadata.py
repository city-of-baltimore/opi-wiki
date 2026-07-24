"""Tests for metadata sidecar resolution."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from scripts.repo_tools.metadata import (
    find_metadata_issues,
    find_review_date_issues,
    resolve_page_metadata,
)


def _fresh_metadata(**overrides: str) -> dict[str, str]:
    """Return complete page metadata that passes the freshness contract."""

    metadata = {
        "owner": "OPI Director's Office",
        "status": "approved",
        "last_reviewed": "2026-06-01",
        "next_review": "2026-09-01",
        "change_log": "Test fixture.",
    }
    metadata.update(overrides)
    return metadata


def test_metadata_resolution_inherits_defaults_and_page_overrides(tmp_path: Path) -> None:
    """A page should inherit metadata from ancestor sidecars."""

    docs_dir = tmp_path / "docs"
    section_dir = docs_dir / "section"
    section_dir.mkdir(parents=True)

    (docs_dir / ".metadata.yml").write_text(
        "defaults:\n"
        "  owner: OPI Director's Office\n"
        "  status: approved\n"
        "  last_reviewed: 2026-04-15\n"
        "  next_review: 2026-07-15\n"
        "  change_log: Root default.\n",
        encoding="utf-8",
    )
    (section_dir / ".metadata.yml").write_text(
        "pages:\n  page.md:\n    owner: Chief of Staff\n",
        encoding="utf-8",
    )
    page = section_dir / "page.md"
    page.write_text("# Page\n", encoding="utf-8")

    metadata = resolve_page_metadata(docs_dir, page)

    assert metadata["owner"] == "Chief of Staff"
    assert metadata["status"] == "approved"
    assert metadata["change_log"] == "Root default."


def test_metadata_validator_reports_missing_fields(tmp_path: Path) -> None:
    """Pages missing required metadata should be reported."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "page.md").write_text("# Page\n", encoding="utf-8")

    issues = find_metadata_issues(docs_dir)

    assert len(issues) == 1
    assert "missing metadata fields" in issues[0]


def test_review_dates_pass_when_fresh() -> None:
    """A recently reviewed page with a future next_review raises no issues."""

    issues = find_review_date_issues(_fresh_metadata(), "page.md", today=date(2026, 7, 7))

    assert issues == []


def test_review_dates_flag_an_excessive_review_interval() -> None:
    """A distant deadline must not disable the review-cadence guardrail."""

    issues = find_review_date_issues(
        _fresh_metadata(last_reviewed="2025-12-01"),
        "page.md",
        today=date(2026, 7, 7),
    )

    assert len(issues) == 1
    assert "review interval" in issues[0]
    assert "exceeds 200 days" in issues[0]


def test_requested_review_round_passes_until_its_deadline() -> None:
    """The approved July-to-January review round must not fail prematurely."""

    issues = find_review_date_issues(
        _fresh_metadata(
            last_reviewed="2026-07-19",
            next_review="2027-01-31",
        ),
        "page.md",
        today=date(2027, 1, 30),
    )

    assert issues == []


def test_review_dates_flag_future_last_reviewed() -> None:
    """Review dates cannot claim work that has not happened yet."""

    issues = find_review_date_issues(
        _fresh_metadata(
            last_reviewed="2026-07-08",
            next_review="2026-09-01",
        ),
        "page.md",
        today=date(2026, 7, 7),
    )

    assert issues == ["page.md: last_reviewed 2026-07-08 is in the future"]


def test_review_dates_flag_unparseable_dates() -> None:
    """Non-ISO review dates should fail loudly instead of passing silently."""

    issues = find_review_date_issues(
        _fresh_metadata(last_reviewed="April 2026", next_review="soon"),
        "page.md",
        today=date(2026, 7, 7),
    )

    assert len(issues) == 2
    assert all("not an ISO date" in issue for issue in issues)


def test_review_dates_flag_next_review_before_last_reviewed() -> None:
    """next_review must not precede last_reviewed."""

    issues = find_review_date_issues(
        _fresh_metadata(next_review="2026-05-01"),
        "page.md",
        today=date(2026, 7, 7),
    )

    assert len(issues) == 1
    assert "precedes" in issues[0]


def test_review_dates_flag_overdue_next_review() -> None:
    """A passed review deadline should fail even when last_reviewed is recent."""

    issues = find_review_date_issues(
        _fresh_metadata(next_review="2026-07-01"),
        "page.md",
        today=date(2026, 7, 7),
    )

    assert len(issues) == 1
    assert "is overdue" in issues[0]


def test_metadata_validator_rejects_nonpublic_status(tmp_path: Path) -> None:
    """Internal or restricted pages must never build in this public repository."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / ".metadata.yml").write_text(
        "defaults:\n"
        "  owner: Chief of Staff\n"
        "  status: internal\n"
        "  last_reviewed: 2026-07-01\n"
        "  next_review: 2026-12-31\n"
        "  change_log: Test fixture.\n",
        encoding="utf-8",
    )
    (docs_dir / "page.md").write_text("# Internal page\n", encoding="utf-8")

    issues = find_metadata_issues(docs_dir, today=date(2026, 7, 7))

    assert issues == ["page.md: status 'internal' is not publishable in this public repository"]
