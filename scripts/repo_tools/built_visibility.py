"""Validate retired visibility language in canonical built-site content."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from scripts.repo_tools.browser_routes import canonical_route_paths
from scripts.repo_tools.rendered_text import (
    RenderedProjection,
    RenderedTextError,
    project_rendered_content,
)
from scripts.repo_tools.source_semantics import PARAGRAPH_BOUNDARY
from scripts.repo_tools.visibility_policy import (
    PRESENTATION_HOOK_KIND,
    VisibilityPolicyKind,
    VisibilityPolicyMatch,
    find_presentation_hook_matches,
    find_visibility_label_matches,
)

_DIRECTOR_LETTER_ROOT = Path("about-us/letters-from-the-director")
_HEADING_CONTEXT = re.compile(
    r"(?:^| > )h[1-6](?:[.#:\[].*)?\Z",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class _CanonicalPage:
    """One canonical route and its exact built/source files."""

    route: str
    built_file: Path
    source_file: Path


@dataclass(frozen=True)
class _BuiltFinding:
    """One built-artifact policy finding with complete review evidence."""

    built_path: str
    line: int
    column: int
    route: str
    source_path: str
    context: str
    kind: VisibilityPolicyKind
    phrase: str

    def message(self) -> str:
        """Return the stable human-readable diagnostic."""

        description = (
            "retired presentation hook"
            if self.kind == PRESENTATION_HOOK_KIND
            else "retired visibility label"
        )
        return (
            f"{self.built_path}:{self.line}:{self.column}: route {self.route}; "
            f"page source {self.source_path}; context {self.context!r}; "
            f"{description} {self.phrase!r}"
        )


def _route_parts(route: str) -> tuple[str, ...]:
    """Return safe path components for one deployment-relative route."""

    if not route.startswith("/") or route.startswith("//") or "\\" in route:
        raise RuntimeError(f"Canonical sitemap route is not a safe local path: {route!r}")
    parts = tuple(part for part in route.strip("/").split("/") if part)
    if any(part in {".", ".."} for part in parts):
        raise RuntimeError(f"Canonical sitemap route escapes the site root: {route!r}")
    return parts


def _page_candidates(
    route: str,
    site_dir: Path,
    docs_dir: Path,
) -> tuple[Path, tuple[Path, ...]]:
    """Return the canonical built HTML path and possible Markdown sources."""

    parts = _route_parts(route)
    if not parts:
        return site_dir / "index.html", (docs_dir / "index.md",)

    route_path = Path(*parts)
    if route.endswith("/"):
        built_file = site_dir / route_path / "index.html"
        source_stem = route_path
    else:
        if route_path.suffix.casefold() != ".html":
            raise RuntimeError(f"Canonical sitemap route is not an HTML page: {route!r}")
        built_file = site_dir / route_path
        source_stem = route_path.with_suffix("")

    return built_file, (
        docs_dir / source_stem.with_suffix(".md"),
        docs_dir / source_stem / "index.md",
    )


def _canonical_pages(
    site_dir: Path,
    docs_dir: Path,
) -> tuple[_CanonicalPage, ...]:
    """Resolve every sitemap route to exactly one HTML file and source page."""

    routes = canonical_route_paths(site_dir)
    if not routes:
        raise RuntimeError(
            f"Built sitemap contains no canonical routes: {site_dir / 'sitemap.xml'}"
        )

    pages: list[_CanonicalPage] = []
    for route in routes:
        built_file, source_candidates = _page_candidates(route, site_dir, docs_dir)
        if not built_file.is_file():
            raise FileNotFoundError(
                f"Canonical built HTML file was not found for route {route}: {built_file}"
            )

        sources = tuple(candidate for candidate in source_candidates if candidate.is_file())
        if not sources:
            choices = ", ".join(str(candidate) for candidate in source_candidates)
            raise FileNotFoundError(
                f"Canonical route {route} has no Markdown source; checked: {choices}"
            )
        if len(sources) != 1:
            choices = ", ".join(str(candidate) for candidate in sources)
            raise RuntimeError(f"Canonical route {route} has ambiguous Markdown sources: {choices}")
        pages.append(_CanonicalPage(route, built_file, sources[0]))
    return tuple(pages)


def _read_built_html(page: _CanonicalPage) -> str:
    """Read one canonical built page as strict UTF-8."""

    try:
        return page.built_file.read_text(encoding="utf-8", errors="strict")
    except UnicodeError as error:
        raise RuntimeError(
            f"Canonical built HTML is not valid UTF-8 for route {page.route}: {page.built_file}"
        ) from error
    except OSError as error:
        raise RuntimeError(
            f"Unable to read canonical built HTML for route {page.route}: {page.built_file}"
        ) from error


def _line_column(text: str, offset: int) -> tuple[int, int]:
    """Return a one-based line and column for an exact string offset."""

    if not 0 <= offset < len(text):
        raise RuntimeError(f"Policy match offset {offset} is outside built HTML")
    line = text.count("\n", 0, offset) + 1
    previous_newline = text.rfind("\n", 0, offset)
    return line, offset - previous_newline


def _source_label(source_file: Path, docs_dir: Path) -> str:
    """Return a stable docs-rooted source path for diagnostics."""

    return (Path(docs_dir.name) / source_file.relative_to(docs_dir)).as_posix()


def _is_director_letter(source_file: Path, docs_dir: Path) -> bool:
    """Return whether the source belongs to the canonical director-letter section."""

    return source_file.relative_to(docs_dir).is_relative_to(_DIRECTOR_LETTER_ROOT)


def _heading_segments(projection: RenderedProjection) -> tuple[tuple[int, int], ...]:
    """Return contiguous rendered-text spans owned by one heading context."""

    segments: list[tuple[int, int]] = []
    start: int | None = None
    active_context: str | None = None
    for index, (character, context) in enumerate(
        zip(
            (*projection.text, None),
            (*projection.contexts, None),
            strict=True,
        )
    ):
        is_heading = (
            character != PARAGRAPH_BOUNDARY
            and context is not None
            and _HEADING_CONTEXT.search(context) is not None
        )
        if is_heading and start is None:
            start = index
            active_context = context
        elif start is not None and (not is_heading or context != active_context):
            segments.append((start, index))
            start = index if is_heading else None
            active_context = context if is_heading else None
    return tuple(segments)


def _rendered_matches(
    projection: RenderedProjection,
    *,
    director_letter: bool,
) -> tuple[tuple[VisibilityPolicyMatch, int], ...]:
    """Return unique policy matches and their absolute projection offsets."""

    found: list[tuple[VisibilityPolicyMatch, int]] = [
        (match, 0)
        for match in find_visibility_label_matches(
            projection.text,
            director_letter=director_letter,
            heading=False,
        )
    ]
    if director_letter:
        for start, end in _heading_segments(projection):
            heading_text = projection.text[start:end]
            found.extend(
                (match, start)
                for match in find_visibility_label_matches(
                    heading_text,
                    director_letter=True,
                    heading=True,
                )
            )

    unique: dict[tuple[VisibilityPolicyKind, int, int, str], tuple[VisibilityPolicyMatch, int]] = {}
    for match, base_offset in found:
        absolute_start = base_offset + match.start
        absolute_end = base_offset + match.end
        key = (match.kind, absolute_start, absolute_end, match.text.casefold())
        unique[key] = (match, base_offset)
    return tuple(
        unique[key]
        for key in sorted(
            unique,
            key=lambda item: (item[1], item[2], item[0], item[3]),
        )
    )


def _rendered_findings(
    page: _CanonicalPage,
    html: str,
    site_dir: Path,
    docs_dir: Path,
) -> list[_BuiltFinding]:
    """Return semantic and raw-hook findings for one canonical built page."""

    try:
        projection = project_rendered_content(html)
    except RenderedTextError as error:
        relative = page.built_file.relative_to(site_dir).as_posix()
        raise RuntimeError(
            f"Unable to project canonical content for {relative} (route {page.route}): {error}"
        ) from error

    built_path = page.built_file.relative_to(site_dir).as_posix()
    source_path = _source_label(page.source_file, docs_dir)
    findings: list[_BuiltFinding] = []
    for match, base_offset in _rendered_matches(
        projection,
        director_letter=_is_director_letter(page.source_file, docs_dir),
    ):
        start = base_offset + match.start
        end = base_offset + match.end
        if not (0 <= start < end <= len(projection.text)):
            raise RuntimeError(
                f"Visibility policy returned an invalid rendered range "
                f"{start}:{end} for route {page.route}"
            )
        origin = projection.origins[start]
        findings.append(
            _BuiltFinding(
                built_path=built_path,
                line=origin.line,
                column=origin.column,
                route=page.route,
                source_path=source_path,
                context=projection.contexts[start],
                kind=match.kind,
                phrase=match.text,
            )
        )

    for match in find_presentation_hook_matches(html):
        if not (0 <= match.start < match.end <= len(html)):
            raise RuntimeError(
                f"Visibility policy returned an invalid built-HTML range "
                f"{match.start}:{match.end} for route {page.route}"
            )
        line, column = _line_column(html, match.start)
        findings.append(
            _BuiltFinding(
                built_path=built_path,
                line=line,
                column=column,
                route=page.route,
                source_path=source_path,
                context="raw built HTML",
                kind=match.kind,
                phrase=match.text,
            )
        )
    return findings


def find_built_visibility_issues(site_dir: Path, docs_dir: Path) -> list[str]:
    """Return evidence for retired labels in every canonical built page."""

    if not site_dir.is_dir():
        raise FileNotFoundError(f"Built site directory was not found: {site_dir}")
    if not docs_dir.is_dir():
        raise FileNotFoundError(f"Documentation source directory was not found: {docs_dir}")

    findings: list[_BuiltFinding] = []
    for page in _canonical_pages(site_dir, docs_dir):
        html = _read_built_html(page)
        findings.extend(_rendered_findings(page, html, site_dir, docs_dir))
    return [
        finding.message()
        for finding in sorted(
            findings,
            key=lambda item: (
                item.built_path,
                item.line,
                item.column,
                item.kind,
                item.phrase.casefold(),
                item.phrase,
            ),
        )
    ]
