"""Tests for the page consistency linter."""

from __future__ import annotations

from scripts.check_consistency import (
    DOCS,
    acronym_report,
    check_duplicate_blockquotes,
    check_empty_headings,
    check_service_sections,
)

# rel() inside the linter resolves against the repo root, so fixture paths just
# need to live under it — the files are never read.
PAGE = DOCS / "example" / "page.md"


def test_empty_heading_before_same_level_sibling_is_flagged() -> None:
    """A heading immediately followed by a same-level heading is empty."""

    lines = ["## First", "", "## Second", "Body text."]

    issues = check_empty_headings(PAGE, lines)

    assert len(issues) == 1
    assert "empty heading '## First'" in issues[0]


def test_heading_with_subsection_is_not_empty() -> None:
    """A deeper next heading is a subsection, not an empty section."""

    lines = ["## Parent", "", "### Child", "Body text."]

    assert check_empty_headings(PAGE, lines) == []


def test_trailing_empty_heading_is_flagged() -> None:
    """A heading at end-of-file with no body should be reported."""

    lines = ["Body.", "", "## Dangling"]

    issues = check_empty_headings(PAGE, lines)

    assert len(issues) == 1
    assert "end of file" in issues[0]


def test_repeated_long_blockquote_is_flagged() -> None:
    """The same long blockquote twice on one page indicates copy drift."""

    quote = "> " + "Respond when necessary. Build so we do not have to respond again. " * 2
    lines = [quote, "Body.", quote]

    issues = check_duplicate_blockquotes(PAGE, lines)

    assert len(issues) == 1
    assert "repeated 2x" in issues[0]


def test_service_pages_require_the_shared_skeleton() -> None:
    """Service pages missing required sections should be reported."""

    service_page = DOCS / "what-we-do" / "services" / "example.md"
    text = "## What this service does\n\ncontent\n"

    issues = check_service_sections(service_page, text)

    assert any("## The goal" in issue for issue in issues)
    assert not any("## What this service does" in issue for issue in issues)


def test_acronym_report_respects_allowlist_and_expansion() -> None:
    """Allowlisted and page-expanded acronyms are fine; unknown ones are not."""

    text = (
        "The XYZQ pipeline feeds OPI dashboards.\n"
        "We coordinate with the Department of General Services (DGSX).\n"
    )

    findings = acronym_report(PAGE, text, allow={"OPI"})

    tokens = {token for _path, token in findings}
    assert "XYZQ" in tokens  # unknown and never expanded
    assert "OPI" not in tokens  # allowlisted
    assert "DGSX" not in tokens  # expanded in parentheses on the page
