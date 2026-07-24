"""Checks that private source data does not enter the published site."""

from __future__ import annotations

import re
from pathlib import Path

PHONE_NUMBER_RE = re.compile(r"(?<!\d)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-])\d{3}[ .-]\d{4}(?!\d)")
PIN_LABEL_RE = re.compile(r"\bPINs?\b")
TEXT_OUTPUT_SUFFIXES = frozenset({".html", ".json", ".txt", ".xml"})
YAML_SUFFIXES = frozenset({".yaml", ".yml"})


def find_publication_boundary_issues(site_dir: Path) -> list[str]:
    """Return source-data and sensitive-field findings in a built site."""

    if not site_dir.is_dir():
        raise FileNotFoundError(f"Built site directory was not found: {site_dir}")

    issues: list[str] = []
    for published_file in sorted(path for path in site_dir.rglob("*") if path.is_file()):
        relative_file = published_file.relative_to(site_dir)
        suffix = published_file.suffix.casefold()

        if suffix in YAML_SUFFIXES:
            issues.append(f"{relative_file}: structured YAML source was published")
            continue
        if suffix not in TEXT_OUTPUT_SUFFIXES:
            continue

        try:
            text = published_file.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            raise RuntimeError(f"Unable to read built output: {published_file}") from error

        if PHONE_NUMBER_RE.search(text):
            issues.append(f"{relative_file}: contains a phone-number pattern")
        if PIN_LABEL_RE.search(text):
            issues.append(f"{relative_file}: contains a visible PIN label")

    return issues
