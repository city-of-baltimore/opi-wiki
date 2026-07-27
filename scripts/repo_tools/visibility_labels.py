"""Reject retired visibility labels while preserving real domain language."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTENSIONLESS_GUIDANCE_PATHS = (
    Path(".github/CODEOWNERS"),
    Path(".gitignore"),
)
SOURCE_SUFFIXES = frozenset({".md", ".yaml", ".yml"})

RETIRED_VISIBILITY_LABEL_PATTERNS = (
    re.compile(r"\bpublic[- ]facing\b", re.IGNORECASE),
    re.compile(r"\bpublication posture\b", re.IGNORECASE),
    re.compile(r"\bpublic/private boundar(?:y|ies)\b", re.IGNORECASE),
    re.compile(r"\binternal-only\b", re.IGNORECASE),
    re.compile(
        r"\b(?:public|internal|approved)[- ]"
        r"(?:audience|badge|copy|label|language|version)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bA public letter\b", re.IGNORECASE),
    re.compile(r"^##\s+Public Purpose\s*$", re.IGNORECASE | re.MULTILINE),
    re.compile(
        r"\bpublic (?:"
        r"briefs?|content(?: review)?|docs? site|effect|Foundations site|"
        r"leadership(?: chart| names)?|materials?|MkDocs site|operating model|"
        r"org chart|organization data|pages?|reference|repository|"
        r"role summar(?:y|ies)|roster|site|staff(?: roster)?|summar(?:y|ies)|"
        r"template pages"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\binternal (?:"
        r"companion documents?|guidance|onboarding(?: working)? materials?|"
        r"operating guidance|operations and communications|SOPs?|working materials?"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bapproved (?:engineering stack|PRs?|short form)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:ED/CDO|section owner) approves?\b", re.IGNORECASE),
    re.compile(r"\bED/CDO approval\b", re.IGNORECASE),
)


def _source_paths(
    repo_root: Path,
    docs_dir: Path,
    *,
    include_docs: bool,
) -> tuple[Path, ...]:
    """Return deterministic authored sources covered by the label ratchet."""

    root_guidance = [
        path
        for path in repo_root.iterdir()
        if path.is_file() and path.suffix.casefold() in SOURCE_SUFFIXES
    ]
    github_dir = repo_root / ".github"
    github_guidance = (
        [
            path
            for path in github_dir.rglob("*")
            if path.is_file() and path.suffix.casefold() in SOURCE_SUFFIXES
        ]
        if github_dir.is_dir()
        else []
    )
    extensionless_guidance = [
        repo_root / relative_path for relative_path in EXTENSIONLESS_GUIDANCE_PATHS
    ]
    docs_sources = (
        [
            path
            for path in docs_dir.rglob("*")
            if path.is_file() and path.suffix.casefold() in SOURCE_SUFFIXES
        ]
        if include_docs
        else []
    )
    return tuple(
        sorted(
            {
                *root_guidance,
                *github_guidance,
                *extensionless_guidance,
                *docs_sources,
            }
        )
    )


def _relative_path(path: Path, repo_root: Path) -> str:
    """Return a repository-relative path when possible."""

    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def check_visibility_labels(
    path: Path,
    text: str,
    *,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Return line-level findings for retired labels in one authored source."""

    issues: list[str] = []
    for pattern in RETIRED_VISIBILITY_LABEL_PATTERNS:
        for match in pattern.finditer(text):
            line_number = text.count("\n", 0, match.start()) + 1
            matched_text = " ".join(match.group(0).split())
            issues.append(
                f"{_relative_path(path, repo_root)}:{line_number}: retired visibility label "
                f"'{matched_text}'; name the reader, review, or concrete data rule instead"
            )
    return issues


def find_visibility_label_issues(
    repo_root: Path = REPO_ROOT,
    docs_dir: Path | None = None,
    *,
    include_docs: bool = True,
) -> list[str]:
    """Return file-and-line findings for retired repository visibility labels."""

    effective_docs_dir = docs_dir or repo_root / "docs"
    issues: list[str] = []
    for path in _source_paths(repo_root, effective_docs_dir, include_docs=include_docs):
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            issues.append(
                f"{_relative_path(path, repo_root)}: unable to read source for "
                f"visibility-label validation: {error}"
            )
            continue
        issues.extend(check_visibility_labels(path, text, repo_root=repo_root))
    return issues
