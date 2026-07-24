"""Validation helpers for internal links in a built MkDocs site."""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from posixpath import commonpath
from urllib.parse import unquote, urlsplit


@dataclass(frozen=True)
class BuiltReference:
    """A parsed built-site href or src attribute and its source line."""

    target: str
    line_number: int


class _ReferenceParser(HTMLParser):
    """Collect link and asset references using HTML parsing rules."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[BuiltReference] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record every non-empty href and src on a start tag."""

        del tag
        for name, value in attrs:
            if name.lower() in {"href", "src"} and value is not None:
                self.references.append(BuiltReference(value, self.getpos()[0]))


class _SitemapLocationParser(HTMLParser):
    """Collect URL locations from MkDocs' generated sitemap XML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.locations: list[str] = []
        self._location_parts: list[str] | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Start collecting text inside a loc element."""

        del attrs
        if tag.lower() == "loc":
            self._location_parts = []

    def handle_data(self, data: str) -> None:
        """Collect text belonging to the current loc element."""

        if self._location_parts is not None:
            self._location_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        """Finish one loc element and retain its non-empty URL."""

        if tag.lower() != "loc" or self._location_parts is None:
            return
        location = "".join(self._location_parts).strip()
        if location:
            self.locations.append(location)
        self._location_parts = None


def extract_built_references(text: str) -> list[BuiltReference]:
    """Return parsed href and src references from one built HTML document."""

    parser = _ReferenceParser()
    parser.feed(text)
    parser.close()
    return parser.references


def _is_external_or_document_local(target: str) -> bool:
    """Return whether a reference needs no built-file resolution."""

    stripped = target.strip()
    parsed = urlsplit(stripped)
    return bool(parsed.scheme or parsed.netloc or stripped.startswith(("//", "#")))


def _is_within(path: Path, root: Path) -> bool:
    """Return whether a resolved candidate stays inside the built-site root."""

    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def discover_site_base_path(site_dir: Path) -> str:
    """Return the deployment base shared by URLs in the generated sitemap."""

    locations = load_sitemap_locations(site_dir)
    if not locations:
        return "/"

    paths = [
        urlsplit(location).path for location in locations if urlsplit(location).path.startswith("/")
    ]
    if not paths:
        return "/"

    shared_path = commonpath(paths)
    if shared_path == "/":
        return shared_path
    return "/" + shared_path.strip("/") + "/"


def load_sitemap_locations(site_dir: Path) -> list[str]:
    """Return canonical URL locations from a generated sitemap, if present."""

    sitemap = site_dir / "sitemap.xml"
    if not sitemap.exists():
        return []
    try:
        sitemap_text = sitemap.read_text(encoding="utf-8")
    except OSError as error:
        raise RuntimeError(f"Unable to read built sitemap: {sitemap}") from error

    parser = _SitemapLocationParser()
    parser.feed(sitemap_text)
    parser.close()
    if not parser.locations:
        raise RuntimeError(f"Built sitemap contains no URL locations: {sitemap}")
    return parser.locations


def _candidate_paths(
    html_file: Path,
    site_dir: Path,
    target_path: str,
    base_path: str,
) -> list[Path]:
    """Resolve the built-file candidates represented by one internal URL path."""

    if target_path.startswith("/"):
        relative = target_path.lstrip("/")
        candidates = [(site_dir / relative).resolve()]
        target_parts = [part for part in relative.split("/") if part]
        base_parts = [part for part in base_path.strip("/").split("/") if part]
        if base_parts and target_parts[: len(base_parts)] == base_parts:
            # The built directory is already the configured deployment base,
            # so a matching site_url prefix is the only segment we may strip.
            candidates.append((site_dir / Path(*target_parts[len(base_parts) :])).resolve())
        return candidates
    return [(html_file.parent / target_path).resolve()]


def _candidate_exists(candidate: Path) -> bool:
    """Return whether a candidate names a built file or pretty-URL directory."""

    return candidate.exists() or (not candidate.suffix and (candidate / "index.html").exists())


def find_broken_links(site_dir: Path, *, base_path: str | None = None) -> list[str]:
    """Return broken or root-escaping references across a built site."""

    resolved_site_dir = site_dir.resolve()
    resolved_base_path = base_path or discover_site_base_path(site_dir)
    broken: set[str] = set()
    for html_file in sorted(site_dir.rglob("*.html")):
        try:
            text = html_file.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            raise RuntimeError(f"Unable to read built HTML file: {html_file}") from error

        for reference in extract_built_references(text):
            raw = reference.target.strip()
            if _is_external_or_document_local(raw):
                continue

            path = unquote(urlsplit(raw).path)
            if not path or not any(character.isalnum() for character in path):
                continue

            candidates = _candidate_paths(
                html_file,
                resolved_site_dir,
                path,
                resolved_base_path,
            )
            source = html_file.relative_to(site_dir)
            if any(not _is_within(candidate, resolved_site_dir) for candidate in candidates):
                broken.add(f"{source}:{reference.line_number} -> {raw} [target escapes built site]")
                continue
            if any(_candidate_exists(candidate) for candidate in candidates):
                continue
            broken.add(f"{source}:{reference.line_number} -> {raw}")

    return sorted(broken)
