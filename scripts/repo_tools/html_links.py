"""Validation helpers for raw HTML links embedded in Markdown content."""

from __future__ import annotations

import re
from pathlib import Path

HREF_RE = re.compile(r'href="([^"]+)"')


def is_external_link(href: str) -> bool:
    """Return whether an href should be excluded from local resolution checks."""

    return href.startswith(("http://", "https://", "mailto:", "tel:", "#"))


def candidate_paths(source_file: Path, href: str) -> list[Path]:
    """Resolve candidate local files for a raw HTML href."""

    clean_href = href.split("#", 1)[0].split("?", 1)[0].strip()
    if not clean_href:
        return []

    target = (source_file.parent / clean_href).resolve()

    if Path(clean_href).suffix:
        return [target]

    trimmed = clean_href.rstrip("/")
    target_no_slash = (source_file.parent / trimmed).resolve()
    return [
        target / "index.md",
        target_no_slash.with_suffix(".md"),
        target_no_slash / "index.md",
    ]


def find_unresolved_html_links(docs_dir: Path) -> list[str]:
    """Return unresolved raw HTML links across all Markdown files."""

    errors: list[str] = []

    for markdown_file in sorted(docs_dir.rglob("*.md")):
        try:
            text = markdown_file.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Unable to read Markdown file: {markdown_file}") from error

        for line_number, line in enumerate(text.splitlines(), start=1):
            for href in HREF_RE.findall(line):
                if is_external_link(href):
                    continue
                if any(path.exists() for path in candidate_paths(markdown_file, href)):
                    continue

                relative_file = markdown_file.relative_to(docs_dir.parent)
                errors.append(
                    f"{relative_file}:{line_number}: unresolved raw HTML link '{href}'"
                )

    return errors
