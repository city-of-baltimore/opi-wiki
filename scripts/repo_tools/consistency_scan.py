"""Discover authored sources, coordinate consistency rules, and format evidence."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from scripts.repo_tools.acronyms import acronym_report, load_acronym_allowlist
from scripts.repo_tools.authored_sources import authored_source_paths
from scripts.repo_tools.consistency import (
    DOCS,
    REPO_ROOT,
    check_citistat_narrative,
    check_duplicate_blockquotes,
    check_empty_headings,
    check_glossary_taxonomy,
    check_service_sections,
    check_toc_sections,
)
from scripts.repo_tools.visibility_labels import (
    check_visibility_label_sources,
    check_visibility_labels,
)


@dataclass(frozen=True)
class ConsistencyScan:
    """Collected structural issues and informational acronym findings."""

    structural_issues: tuple[str, ...]
    acronyms: tuple[tuple[str, str], ...]


def _relative_path(path: Path, repo_root: Path) -> str:
    """Return a repository-relative display path."""

    return str(path.relative_to(repo_root))


def scan_consistency(
    docs_dir: Path = DOCS,
    *,
    repo_root: Path = REPO_ROOT,
) -> ConsistencyScan:
    """Read authored repository sources and collect all consistency findings."""

    try:
        source_paths = authored_source_paths(
            repo_root,
            docs_dir,
            include_docs=True,
        )
    except RuntimeError as error:
        return ConsistencyScan(
            (f"repository: unable to discover authored sources: {error}",),
            (),
        )
    effective_docs_dir = docs_dir if docs_dir.is_absolute() else repo_root / docs_dir
    docs_source_paths = tuple(
        path for path in source_paths if path.is_relative_to(effective_docs_dir)
    )
    structural_issues = check_visibility_label_sources(
        (path for path in source_paths if not path.is_relative_to(effective_docs_dir)),
        repo_root=repo_root,
    )
    acronyms: list[tuple[str, str]] = []
    unreadable_glossary: Path | None = None
    try:
        allow = load_acronym_allowlist(
            effective_docs_dir,
            authored_paths=docs_source_paths,
        )
    except RuntimeError as error:
        unreadable_glossary = effective_docs_dir / "resources" / "reference" / "glossary.md"
        cause = error.__cause__ or error
        structural_issues.append(
            f"{_relative_path(unreadable_glossary, repo_root)}: "
            f"unable to read acronym glossary: {cause}"
        )
        allow = load_acronym_allowlist(
            effective_docs_dir,
            authored_paths=(),
        )
    services_dir = effective_docs_dir / "what-we-do" / "services"

    markdown_paths = (path for path in docs_source_paths if path.suffix.casefold() == ".md")
    for path in markdown_paths:
        if path == unreadable_glossary:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            structural_issues.append(
                f"{_relative_path(path, repo_root)}: unable to read Markdown source: {error}"
            )
            continue
        lines = text.split("\n")
        structural_issues.extend(check_empty_headings(path, lines, repo_root=repo_root))
        structural_issues.extend(check_duplicate_blockquotes(path, lines, repo_root=repo_root))
        structural_issues.extend(
            check_service_sections(
                path,
                text,
                services_dir=services_dir,
                repo_root=repo_root,
            )
        )
        structural_issues.extend(check_toc_sections(path, text, repo_root=repo_root))
        structural_issues.extend(check_glossary_taxonomy(path, text, repo_root=repo_root))
        structural_issues.extend(check_citistat_narrative(path, text, repo_root=repo_root))
        structural_issues.extend(check_visibility_labels(path, text, repo_root=repo_root))
        acronyms.extend(acronym_report(path, text, allow, repo_root=repo_root))

    yaml_paths = (path for path in docs_source_paths if path.suffix.casefold() in {".yaml", ".yml"})
    for path in yaml_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            source_label = "card source" if path.name.endswith(".cards.yml") else "YAML source"
            structural_issues.append(
                f"{_relative_path(path, repo_root)}: unable to read {source_label}: {error}"
            )
            continue
        structural_issues.extend(check_visibility_labels(path, text, repo_root=repo_root))
        if path.name.endswith(".cards.yml"):
            structural_issues.extend(check_citistat_narrative(path, text, repo_root=repo_root))

    primary_source_suffixes = frozenset({".md", ".yaml", ".yml"})
    auxiliary_paths = (
        path for path in docs_source_paths if path.suffix.casefold() not in primary_source_suffixes
    )
    for path in auxiliary_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            structural_issues.append(
                f"{_relative_path(path, repo_root)}: unable to read authored source: {error}"
            )
            continue
        structural_issues.extend(check_visibility_labels(path, text, repo_root=repo_root))

    return ConsistencyScan(tuple(structural_issues), tuple(acronyms))


def format_consistency_report(
    scan: ConsistencyScan,
    *,
    show_acronyms: bool,
) -> tuple[str, int]:
    """Format a consistency result and return its shell-compatible exit code."""

    lines: list[str] = []
    if scan.acronyms:
        counts = Counter(token for _path, token in scan.acronyms)
        if show_acronyms:
            lines.append(
                f"[consistency] {len(counts)} distinct possibly-undefined acronym(s) "
                "(informational — add to the glossary or expand on first use):"
            )
            for token in sorted(counts, key=lambda item: (-counts[item], item)):
                lines.append(f"  {token} ({counts[token]} use(s))")
        else:
            lines.append(
                f"[consistency] {len(counts)} distinct possibly-undefined acronyms — "
                "run with --acronyms to list them."
            )

    if scan.structural_issues:
        lines.append("")
        lines.append(f"[consistency] {len(scan.structural_issues)} structural issue(s):")
        lines.extend(f"  {issue}" for issue in scan.structural_issues)
        return "\n".join(lines), 1

    lines.append("Consistency checks passed.")
    return "\n".join(lines), 0
