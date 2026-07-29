"""Validation helpers for internal links in a built MkDocs site."""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from posixpath import commonpath
from urllib.parse import unquote, urlsplit

# B405: only the locally generated MkDocs sitemap is parsed, with strict shape checks below.
from xml.etree import ElementTree  # nosec B405


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
    """Return every location from one structurally valid generated sitemap."""

    sitemap = site_dir / "sitemap.xml"
    if not sitemap.exists():
        return []
    try:
        sitemap_text = sitemap.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise RuntimeError(f"Unable to read built sitemap: {sitemap}") from error

    try:
        # S314/B314: this is a locally generated MkDocs artifact; strict parsing
        # is required here, and ElementTree does not retrieve external resources.
        root = ElementTree.fromstring(sitemap_text)  # noqa: S314  # nosec B314
    except ElementTree.ParseError as error:
        raise RuntimeError(f"Built sitemap XML is malformed: {sitemap}: {error}") from error

    def local_name(tag: str) -> str:
        """Return an XML element name without its optional namespace."""

        return tag.rsplit("}", maxsplit=1)[-1]

    if local_name(root.tag) != "urlset":
        raise RuntimeError(f"Built sitemap root must be <urlset>: {sitemap}")

    url_elements = list(root)
    if any(local_name(element.tag) != "url" for element in url_elements):
        raise RuntimeError(f"Built sitemap <urlset> may contain only <url> entries: {sitemap}")

    locations: list[str] = []
    direct_locations: set[int] = set()
    for index, url_element in enumerate(url_elements, start=1):
        location_elements = [element for element in url_element if local_name(element.tag) == "loc"]
        if len(location_elements) != 1:
            raise RuntimeError(
                f"Built sitemap <url> entry {index} must contain exactly one <loc>: {sitemap}"
            )
        location_element = location_elements[0]
        direct_locations.add(id(location_element))
        if list(location_element):
            raise RuntimeError(
                f"Built sitemap <loc> entry {index} must contain URL text only: {sitemap}"
            )
        location = (location_element.text or "").strip()
        if not location:
            raise RuntimeError(f"Built sitemap <loc> entry {index} is empty: {sitemap}")
        locations.append(location)

    nested_locations = {id(element) for element in root.iter() if local_name(element.tag) == "loc"}
    if nested_locations != direct_locations:
        raise RuntimeError(
            f"Built sitemap contains a <loc> outside a direct <url> entry: {sitemap}"
        )

    if not locations:
        raise RuntimeError(f"Built sitemap contains no URL locations: {sitemap}")
    return locations


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
