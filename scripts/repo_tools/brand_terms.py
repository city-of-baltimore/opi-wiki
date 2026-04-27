"""Checks that editorial prose uses OPI and CitiStat consistently."""

from __future__ import annotations

import re
from pathlib import Path

FENCED_CODE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]+`")
HTML_TAG_RE = re.compile(r"<[^>]+>")
URL_RE = re.compile(r"https?://\S+|www\.\S+|\b\S+@[\w.-]+\.\w+\b|\b\S*opi\.baltimorecity\.gov\S*")
PROHIBITED_PATTERNS = (
    (re.compile(r"\bCitistat\b"), "Use 'CitiStat', not 'Citistat'."),
    (re.compile(r"\bOpi\b"), "Use 'OPI', not 'Opi'."),
    (re.compile(r"(?<![/@._-])\bopi\b(?![-./@_])"), "Use 'OPI', not 'opi'."),
)


def _strip_non_editorial_content(text: str) -> str:
    """Remove code, raw HTML tags, and URL-like content before editorial scans."""

    sanitized = FENCED_CODE_RE.sub("", text)
    sanitized = INLINE_CODE_RE.sub("", sanitized)
    sanitized = HTML_TAG_RE.sub("", sanitized)
    return URL_RE.sub("", sanitized)


def find_brand_term_issues(paths: list[Path]) -> list[str]:
    """Return editorial casing issues for OPI and CitiStat in Markdown files."""

    issues: list[str] = []

    for path in sorted(paths):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Unable to read Markdown file: {path}") from error

        sanitized = _strip_non_editorial_content(text)
        for line_number, line in enumerate(sanitized.splitlines(), start=1):
            for pattern, message in PROHIBITED_PATTERNS:
                if pattern.search(line):
                    issues.append(f"{path}:{line_number}: {message}")

    return issues
