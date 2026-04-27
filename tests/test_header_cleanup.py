"""Tests for document-cover header cleanup helpers."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.header_cleanup import (
    SIGNER_LINE,
    apply_header_cleanup,
    find_header_changes,
)


def test_narrative_header_cleanup_removes_signature_block() -> None:
    """Narrative pages should lose office/signer boilerplate near the top."""

    text = """# Mission, Vision, Identity

<span class="opi-pill approved">Approved</span>

> Why this office exists.
Mayor’s Office of Performance and Innovation
Dartanion Swift-Williams, Executive Director and Chief Data Officer
Issued April 2026 · Effective FY27

**Mission**

Real content stays here.
"""

    cleaned, changes = apply_header_cleanup(
        text, Path("docs/about-us/about-opi/mission-vision-identity.md")
    )

    assert "Mayor’s Office of Performance and Innovation" not in cleaned
    assert SIGNER_LINE not in cleaned
    assert "Issued April 2026" not in cleaned
    assert "Real content stays here." in cleaned
    assert {change.reason for change in changes} == {"office-line", "signer-line", "issued-line"}


def test_pd_header_cleanup_keeps_role_metadata() -> None:
    """PD pages should lose letterhead while preserving classification content."""

    text = """# PD — Project Manager

<span class="opi-pill internal">Position Description</span>

> Position description for the Project Manager.
**DIRECTOR’S OFFICE · POSITION DESCRIPTION**
**Project Manager**
Mayor’s Office of Performance and Innovation · City of Baltimore
**CLASSIFICATION** Operations Officer III
**PORTFOLIO** Director's Office
"""

    cleaned, _ = apply_header_cleanup(
        text,
        Path(
            "docs/resources/reference/position-descriptions/directors-office/"
            "pd-project-manager.md"
        ),
    )

    assert "**DIRECTOR’S OFFICE · POSITION DESCRIPTION**" not in cleaned
    assert "Mayor’s Office of Performance and Innovation · City of Baltimore" not in cleaned
    assert "**CLASSIFICATION** Operations Officer III" in cleaned
    assert "**PORTFOLIO** Director's Office" in cleaned


def test_stat_header_cleanup_removes_cover_boilerplate() -> None:
    """Stat pages should lose duplicate title and cover metadata."""

    text = """# 311 Stat

<span class="opi-pill approved">Approved</span>

> CitiStat brief for 311.
**311 Stat**

CitiStat

**Dartanion Swift-Williams, Executive Director and Chief Data Officer**

Mayor's Office of Performance and Innovation

**STAT 1**

# **311 Stat**

| **Field** | **Value** |
|-----------|-----------|
| Stat Type | Thematic  |
"""

    cleaned, changes = apply_header_cleanup(
        text, Path("docs/our-teams/performance-and-citistat/citistat-portfolio/311-stat.md")
    )

    assert "CitiStat\n" not in cleaned
    assert "**STAT 1**" not in cleaned
    assert "# **311 Stat**" not in cleaned
    assert "| **Field** | **Value** |" in cleaned
    assert {change.reason for change in changes} >= {
        "duplicate-title",
        "stat-label",
        "signer-line",
        "office-line",
        "stat-number",
        "duplicate-heading",
    }


def test_scan_is_limited_to_the_page_header() -> None:
    """Office references later in the page should not be removed."""

    filler = "\n".join(f"Paragraph {index}" for index in range(1, 40))
    text = (
        "# Sample\n\n"
        "<span class=\"opi-pill approved\">Approved</span>\n\n"
        f"{filler}\n\n"
        "Mayor’s Office of Performance and Innovation\n"
    )

    changes = find_header_changes(text, Path("docs/sample.md"))

    assert changes == []


def test_letter_cleanup_keeps_one_title_and_summary() -> None:
    """Letter pages should lose duplicate masthead blocks and signer lines."""

    text = """# On OPI Foundations

<span class="opi-pill approved">Approved</span>

> Why we're publishing this body of work.
**LETTER FROM THE DIRECTOR**
**Better Government Is a Discipline**
*A public letter on what the office does.*
**Dartanion Swift-Williams**
Executive Director & Chief Data Officer
**LETTER FROM THE DIRECTOR**
**Better Government Is a Discipline**
*A public letter on what the office does.*

Every city in America is being asked to do more with less.
"""

    cleaned, changes = apply_header_cleanup(
        text, Path("docs/about-us/letters-from-the-director/on-opi-foundations.md")
    )

    assert cleaned.count("**Better Government Is a Discipline**") == 1
    assert cleaned.count("*A public letter on what the office does.*") == 1
    assert "**Dartanion Swift-Williams**" not in cleaned
    assert "Executive Director & Chief Data Officer" not in cleaned
    assert "Every city in America" in cleaned
    assert {change.reason for change in changes} >= {
        "letter-banner",
        "letter-signer",
        "letter-title-line",
        "duplicate-header-line",
    }
