"""Lightweight accessibility smoke checks for generated site HTML."""

from __future__ import annotations

import re
from pathlib import Path

DETAILS_RE = re.compile(r"<details\b.*?>(.*?)</details>", re.S)
SUMMARY_RE = re.compile(r"<summary\b[^>]*>(.*?)</summary>", re.S)
CARD_RE = re.compile(r'<div class="[^"]*\bopi-card\b[^"]*".*?>(.*?)</div>', re.S)
CARD_LINK_RE = re.compile(r'<a class="[^"]*\bopi-card-link\b[^"]*"[^>]*>(.*?)</a>', re.S)
TAG_RE = re.compile(r"<[^>]+>")


def _plain_text(fragment: str) -> str:
    """Collapse HTML markup into plain text for content checks."""

    return TAG_RE.sub("", fragment).strip()


def find_accessibility_issues(site_dir: Path) -> list[str]:
    """Return basic accessibility issues from generated site HTML."""

    issues: list[str] = []

    for html_file in sorted(site_dir.rglob("*.html")):
        try:
            html = html_file.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Unable to read built HTML file: {html_file}") from error

        relative_file = html_file.relative_to(site_dir)

        for index, details_block in enumerate(DETAILS_RE.findall(html), start=1):
            summary_match = SUMMARY_RE.search(details_block)
            if not summary_match or not _plain_text(summary_match.group(1)):
                issues.append(f"{relative_file}: details block #{index} is missing a summary label")

        for index, card_block in enumerate(CARD_RE.findall(html), start=1):
            link_match = CARD_LINK_RE.search(card_block)
            if link_match is None:
                continue
            if not _plain_text(link_match.group(1)):
                issues.append(f"{relative_file}: card #{index} is missing visible link text")

    return issues
