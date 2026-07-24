"""Guardrail checks that keep the wiki's plain, human voice from regressing.

The copy-edit pass removed two AI-tells: em-dashes used as prose punctuation and
a small set of jargon terms. This module flags either if they return, so the
verification suite can hold the line on every PR and deploy. See STYLE.md for the
standard these checks enforce.
"""

from __future__ import annotations

import re
from pathlib import Path

# Terms the wiki does not use. Kept deliberately small and unambiguous so the
# check never fights legitimate prose; borderline words (for example
# "decision-ready") are intentionally absent. Matched case-insensitively as
# substrings, so inflections like "leverages" or "synergies" are covered.
BANNED_JARGON: tuple[str, ...] = (
    "operating backbone",
    "operational backbone",
    "executive performance rhythm",
    "executive performance routine",
    "executive performance cadence",
    "signal-to-solution loop",
    "seamless",
    "world-class",
    "best-in-class",
    "cutting-edge",
    "turnkey",
    "frictionless",
    "synerg",
    "leverage",
)

EM_DASH = "—"
_FENCE_RE = re.compile(r"^\s*(?:```|~~~)")


def _is_table_row(line: str) -> bool:
    """Return whether a line is a Markdown table row (starts with a pipe)."""

    return line.lstrip().startswith("|")


def find_style_issues(paths: list[Path]) -> list[str]:
    """Return voice-guardrail issues: prose em-dashes and banned jargon.

    Em-dashes are flagged only in prose, not in table rows (where they are used
    as a legitimate cell separator) or fenced code. Banned jargon is flagged
    anywhere outside fenced code.
    """

    issues: list[str] = []

    for path in sorted(paths):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Unable to read Markdown file: {path}") from error

        in_fence = False
        for line_number, line in enumerate(text.splitlines(), start=1):
            if _FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            if EM_DASH in line and not _is_table_row(line):
                issues.append(
                    f"{path}:{line_number}: em-dash in prose; use a period, comma, "
                    "colon, or parentheses (see STYLE.md)."
                )

            lowered = line.lower()
            for term in BANNED_JARGON:
                if term in lowered:
                    issues.append(f'{path}:{line_number}: banned jargon "{term}" (see STYLE.md).')

    return issues
