"""Utilities for detecting and removing document-cover boilerplate."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

HEADER_SCAN_LIMIT = 30
OFFICE_LINES = {
    "Mayor’s Office of Performance and Innovation",
    "Mayor's Office of Performance and Innovation",
    "Mayor’s Office of Performance and Innovation · City of Baltimore",
    "Mayor's Office of Performance and Innovation · City of Baltimore",
}
SIGNER_LINE = "Dartanion Swift-Williams, Executive Director and Chief Data Officer"
STAT_NUMBER_RE = re.compile(r"^\*\*STAT \d+\*\*$")
POSITION_DESCRIPTION_RE = re.compile(r"^\*\*.+POSITION DESCRIPTION\*\*$")
ISSUED_LINE_RE = re.compile(r"^Issued .+")
DOUBLE_BLANK_RE = re.compile(r"\n{3,}")


@dataclass(frozen=True)
class HeaderChange:
    """A single header-boilerplate removal decision."""

    line_number: int
    content: str
    reason: str


def _markdown_title(text: str) -> str | None:
    """Return the first Markdown H1 title from a page."""

    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _normalize_title(value: str) -> str:
    """Normalize a title for lightweight duplicate detection."""

    normalized = value.strip().strip("*").strip()
    normalized = normalized.removeprefix("PD — ").removeprefix("PD - ").strip()
    normalized = normalized.replace("&", "and")
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.casefold()


def _is_letter_page(path: Path) -> bool:
    """Return whether the page is a director letter detail page."""

    return "letters-from-the-director" in path.parts and path.name != "index.md"


def _is_styled_header_line(value: str) -> bool:
    """Return whether a line is a short styled heading-like fragment."""

    return (
        (value.startswith("**") and value.endswith("**"))
        or (value.startswith("*") and value.endswith("*"))
    )


def _should_drop_line(line: str, path: Path, page_title: str | None) -> str | None:
    """Return a removal reason when a header line is known boilerplate."""

    stripped = line.strip()
    if not stripped:
        return None

    if stripped in OFFICE_LINES:
        return "office-line"
    if stripped == SIGNER_LINE or stripped == f"**{SIGNER_LINE}**":
        return "signer-line"
    if ISSUED_LINE_RE.match(stripped):
        return "issued-line"

    if path.name.startswith("pd-"):
        if POSITION_DESCRIPTION_RE.match(stripped):
            return "pd-banner"
        if stripped.startswith("**") and stripped.endswith("**") and page_title:
            if _normalize_title(stripped) == _normalize_title(page_title):
                return "duplicate-title"

    if "citistat-portfolio" in path.parts:
        if stripped == "CitiStat":
            return "stat-label"
        if STAT_NUMBER_RE.match(stripped):
            return "stat-number"
        if stripped.startswith("# **") and stripped.endswith("**") and page_title:
            inner = stripped.removeprefix("# ").strip()
            if _normalize_title(inner) == _normalize_title(page_title):
                return "duplicate-heading"
        if stripped.startswith("**") and stripped.endswith("**") and page_title:
            if _normalize_title(stripped) == _normalize_title(page_title):
                return "duplicate-title"

    return None


def find_header_changes(text: str, path: Path) -> list[HeaderChange]:
    """Return boilerplate header lines that can be safely removed."""

    page_title = _markdown_title(text)
    changes: list[HeaderChange] = []
    seen_header_lines: set[str] = set()

    for index, line in enumerate(text.splitlines(), start=1):
        if index > HEADER_SCAN_LIMIT:
            break
        reason = _should_drop_line(line, path, page_title)
        stripped = line.strip()
        if reason is None and _is_letter_page(path):
            if stripped == "**LETTER FROM THE DIRECTOR**":
                reason = "letter-banner"
            elif stripped == "**Dartanion Swift-Williams**":
                reason = "letter-signer"
            elif stripped == "Executive Director & Chief Data Officer":
                reason = "letter-title-line"
        if (
            reason is None
            and stripped
            and _is_styled_header_line(stripped)
            and stripped in seen_header_lines
        ):
            reason = "duplicate-header-line"
        if reason is None:
            if stripped and _is_styled_header_line(stripped):
                seen_header_lines.add(stripped)
            continue
        changes.append(HeaderChange(line_number=index, content=line, reason=reason))
        if stripped and _is_styled_header_line(stripped):
            seen_header_lines.add(stripped)

    return changes


def apply_header_cleanup(text: str, path: Path) -> tuple[str, list[HeaderChange]]:
    """Remove boilerplate header lines while preserving substantive content."""

    changes = find_header_changes(text, path)
    if not changes:
        return text, []

    remove_lines = {change.line_number for change in changes}
    cleaned_lines = [
        line
        for index, line in enumerate(text.splitlines(), start=1)
        if index not in remove_lines
    ]
    cleaned_text = "\n".join(cleaned_lines).rstrip() + "\n"
    cleaned_text = DOUBLE_BLANK_RE.sub("\n\n", cleaned_text)
    return cleaned_text, changes
