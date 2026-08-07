"""Reject retired visibility labels while preserving real domain language."""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

from scripts.repo_tools.authored_sources import authored_source_paths
from scripts.repo_tools.source_lexical import source_lexical_projection
from scripts.repo_tools.source_semantics import (
    SemanticProjection,
    is_yaml_source,
    logical_line_break_count,
    normalize_source_text,
)
from scripts.repo_tools.visibility_policy import (
    PRESENTATION_HOOK_KIND,
    VisibilityPolicyMatch,
    find_presentation_hook_matches,
    find_visibility_label_matches,
)
from scripts.repo_tools.yaml_semantics import YamlSemanticError, yaml_scalar_projections

REPO_ROOT = Path(__file__).resolve().parents[2]
DIRECTOR_LETTER_ROOT = Path("docs/about-us/letters-from-the-director")
_DIRECTOR_LETTER_SOURCE_HEADING_REGIONS = (
    re.compile(
        r"^[ \t]{0,3}#{1,6}[^\S\r\n]+[^\r\n]+[ \t]*\r?$",
        re.MULTILINE,
    ),
    re.compile(
        r"^[ \t]{0,3}[^\r\n]+?[ \t]*"
        r"(?:\r\n|[\n\r\x85\u2028\u2029])"
        r"[ \t]{0,3}(?:=+|-+)[ \t]*\r?$",
        re.MULTILINE,
    ),
)


def _relative_path(path: Path, repo_root: Path) -> str:
    """Return a repository-relative path when possible."""

    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _is_director_letter_path(path: Path, repo_root: Path) -> bool:
    """Return whether a source is in the canonical director-letter section."""

    try:
        return path.relative_to(repo_root).is_relative_to(DIRECTOR_LETTER_ROOT)
    except ValueError:
        return False


def _needs_source_lexical_projection(path: Path, repo_root: Path) -> bool:
    """Return whether a source lacks canonical rendered-page text coverage."""

    try:
        relative_path = path.relative_to(repo_root)
    except ValueError:
        return False
    is_canonical_docs_markdown = path.suffix.casefold() == ".md" and relative_path.is_relative_to(
        Path("docs")
    )
    return not is_canonical_docs_markdown


def _matched_text(value: str) -> str:
    """Return a compact, readable representation of a matched source phrase."""

    return " ".join(value.split()).strip("_")


def check_visibility_labels(
    path: Path,
    text: str,
    *,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Return line-level findings for retired labels in one authored source."""

    normalized_text, raw_offsets = normalize_source_text(text, path=path)
    findings: list[tuple[int, int, tuple[str, int, str], str]] = []

    def record_match(
        policy_match: VisibilityPolicyMatch,
        *,
        semantic_text: str,
        source_text: str,
        normalized_offsets: tuple[int, ...],
    ) -> None:
        """Record one finding with its original source offset."""

        canonical_match_index = policy_match.start
        matched_source = semantic_text[policy_match.start : policy_match.end]
        for match_offset, character in enumerate(matched_source):
            if character.isalnum():
                canonical_match_index = policy_match.start + match_offset
                break
        source_start = normalized_offsets[canonical_match_index]
        line_number = 1 + logical_line_break_count(source_text[:source_start])
        previous_line_break = max(
            source_text.rfind(line_break, 0, source_start)
            for line_break in ("\n", "\r", "\v", "\f", "\x85", "\u2028", "\u2029")
        )
        column_number = source_start - previous_line_break
        matched_text = _matched_text(policy_match.text)
        if policy_match.kind == PRESENTATION_HOOK_KIND:
            message = (
                f"{_relative_path(path, repo_root)}:{line_number}:{column_number}: "
                f"retired presentation hook '{matched_text}'; "
                "use plain page content and supported shared components instead"
            )
        else:
            message = (
                f"{_relative_path(path, repo_root)}:{line_number}:{column_number}: "
                f"retired visibility label '{matched_text}'; "
                "name the reader, review, or concrete data rule instead"
            )
        occurrence_key = (policy_match.kind, source_start, matched_text.casefold())
        findings.append((line_number, source_start, occurrence_key, message))

    def normalized_projection(
        projection: SemanticProjection,
        *,
        single_line_breaks_are_structural: bool = False,
    ) -> tuple[str, tuple[int, ...]]:
        """Normalize projected text and compose its absolute source offsets."""

        normalized, projected_offsets = normalize_source_text(
            projection.text,
            path=path,
            single_line_breaks_are_structural=single_line_breaks_are_structural,
        )
        absolute_offsets = tuple(
            projection.raw_offsets[projected_offset] for projected_offset in projected_offsets
        )
        return normalized, absolute_offsets

    def scan_policy(
        semantic_text: str,
        semantic_offsets: tuple[int, ...],
        *,
        director_letter: bool = False,
        heading: bool = False,
        include_presentation: bool = True,
    ) -> None:
        """Record policy matches in one source-mapped text projection."""

        policy_matches = list(
            find_visibility_label_matches(
                semantic_text,
                director_letter=director_letter,
                heading=heading,
            )
        )
        if include_presentation:
            policy_matches.extend(find_presentation_hook_matches(semantic_text))
        for policy_match in sorted(
            policy_matches,
            key=lambda item: (item.start, item.end, item.kind, item.text.casefold()),
        ):
            record_match(
                policy_match,
                semantic_text=semantic_text,
                source_text=text,
                normalized_offsets=semantic_offsets,
            )

    is_director_letter = path.suffix.casefold() == ".md" and _is_director_letter_path(
        path, repo_root
    )
    scan_policy(
        normalized_text,
        raw_offsets,
        director_letter=is_director_letter,
    )

    if _needs_source_lexical_projection(path, repo_root):
        lexical_projection = source_lexical_projection(text)
        lexical_text, lexical_offsets = normalized_projection(lexical_projection)
        scan_policy(
            lexical_text,
            lexical_offsets,
            include_presentation=False,
        )

    if is_director_letter:
        for region_pattern in _DIRECTOR_LETTER_SOURCE_HEADING_REGIONS:
            for region in region_pattern.finditer(text):
                region_text = region.group(0)
                region_offsets = tuple(range(region.start(), region.end()))
                scan_policy(
                    region_text,
                    region_offsets,
                    director_letter=True,
                    heading=True,
                    include_presentation=False,
                )

    if is_yaml_source(path):
        try:
            yaml_projections = yaml_scalar_projections(text)
        except YamlSemanticError as error:
            line_start = 0
            for _line in range(1, error.line_number):
                next_break = text.find("\n", line_start)
                if next_break == -1:
                    break
                line_start = next_break + 1
            findings.append(
                (
                    error.line_number,
                    line_start,
                    ("visibility_label", line_start, error.detail),
                    f"{_relative_path(path, repo_root)}:{error.line_number}: "
                    f"unable to validate semantic YAML text: {error.detail}",
                )
            )
        else:
            for projection in yaml_projections:
                semantic_yaml, semantic_offsets = normalized_projection(
                    projection,
                    single_line_breaks_are_structural=True,
                )
                scan_policy(
                    semantic_yaml,
                    semantic_offsets,
                )
    findings.sort(key=lambda finding: (finding[0], finding[1]))
    messages: list[str] = []
    seen: set[tuple[str, int, str]] = set()
    for _line_number, _order, occurrence_key, message in findings:
        if occurrence_key not in seen:
            seen.add(occurrence_key)
            messages.append(message)
    return messages


def find_visibility_label_issues(
    repo_root: Path = REPO_ROOT,
    docs_dir: Path | None = None,
    *,
    include_docs: bool = True,
) -> list[str]:
    """Return file-and-line findings for retired repository visibility labels."""

    effective_docs_dir = docs_dir or repo_root / "docs"
    try:
        source_paths = authored_source_paths(
            repo_root,
            effective_docs_dir,
            include_docs=include_docs,
        )
    except RuntimeError as error:
        return [f"repository: unable to discover authored sources: {error}"]
    return check_visibility_label_sources(source_paths, repo_root=repo_root)


def check_visibility_label_sources(
    source_paths: Iterable[Path],
    *,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Read explicit authored sources and return retired-label findings."""

    issues: list[str] = []
    for path in source_paths:
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            issues.append(
                f"{_relative_path(path, repo_root)}: unable to read source for "
                f"visibility-label validation: {error}"
            )
            continue
        issues.extend(check_visibility_labels(path, text, repo_root=repo_root))
    return issues
