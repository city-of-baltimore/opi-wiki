"""Validation helpers for raw HTML links embedded in Markdown content."""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


@dataclass(frozen=True)
class HtmlLink:
    """A parsed raw-HTML link and its source line."""

    href: str
    line_number: int


class _HrefParser(HTMLParser):
    """Collect href attributes using HTML's actual quoting and spacing rules."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[HtmlLink] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record every non-empty href on a start tag."""

        del tag
        for name, value in attrs:
            if name.lower() == "href" and value is not None:
                self.links.append(HtmlLink(value, self.getpos()[0]))


def extract_html_links(text: str) -> list[HtmlLink]:
    """Return raw-HTML hrefs from Markdown text, including their line numbers."""

    parser = _HrefParser()
    parser.feed(text)
    parser.close()
    return parser.links


def is_external_link(href: str) -> bool:
    """Return whether an href should be excluded from local resolution checks."""

    stripped = href.strip()
    parsed = urlsplit(stripped)
    return bool(
        not parsed.path or parsed.scheme or parsed.netloc or stripped.startswith(("//", "#"))
    )


def candidate_paths(source_file: Path, href: str, *, docs_dir: Path | None = None) -> list[Path]:
    """Resolve candidate local files for a raw HTML href."""

    clean_href = unquote(urlsplit(href.strip()).path)
    if not clean_href:
        return []

    if clean_href.startswith("/"):
        resolution_root = docs_dir if docs_dir is not None else source_file.parent
        target = (resolution_root / clean_href.lstrip("/")).resolve()
    else:
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


def _is_within(path: Path, root: Path) -> bool:
    """Return whether a resolved target stays inside its publication root."""

    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def find_unresolved_html_links(docs_dir: Path) -> list[str]:
    """Return unresolved raw HTML links across all Markdown files."""

    errors: list[str] = []
    resolved_docs_dir = docs_dir.resolve()

    for markdown_file in sorted(docs_dir.rglob("*.md")):
        try:
            text = markdown_file.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Unable to read Markdown file: {markdown_file}") from error

        for link in extract_html_links(text):
            if is_external_link(link.href):
                continue

            candidates = candidate_paths(markdown_file, link.href, docs_dir=resolved_docs_dir)
            relative_file = markdown_file.relative_to(docs_dir.parent)
            if any(not _is_within(path, resolved_docs_dir) for path in candidates):
                errors.append(
                    f"{relative_file}:{link.line_number}: raw HTML link escapes docs/ '{link.href}'"
                )
                continue
            if any(path.exists() for path in candidates):
                continue

            errors.append(
                f"{relative_file}:{link.line_number}: unresolved raw HTML link '{link.href}'"
            )

    return errors
