"""Reusable structural and editorial consistency checks for the OPI wiki."""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS = REPO_ROOT / "docs"
SERVICES_DIR = DOCS / "what-we-do" / "services"

SERVICE_REQUIRED = (
    "## What this service does",
    "## The goal",
    "## Mandate",
    "## Priority outcomes",
    "## What this means for people",
)

# Every team service-theory-of-change page shares one skeleton (NORTH STAR + the
# numbered logic model). Enforcing it keeps the ToCs from drifting apart again.
TOC_REQUIRED = (
    "## NORTH STAR",
    "### 1. Service overview",
    "### 2. Operating scope (boundary lines)",
    "### 3. Engagement model",
    "### 4. Theory of Change",
    "### 5. Governance and decision rights",
    "### 6. Core offerings and target service levels",
    "### 7. Metrics, targets, and learning",
    "### 8. Operational handoffs across OPI services",
)

GLOSSARY_DRIFT_PATTERNS = (
    (
        re.compile(r"\*\*Data and Analytics\.\*\*\s+OPI[’']s service\b", re.IGNORECASE),
        "Data and Analytics is a team; name Citywide Data and Analytics as the service.",
    ),
    (
        re.compile(r"\*\*Performance\.\*\*\s+OPI[’']s service\b", re.IGNORECASE),
        "Performance is a team; name Citywide Performance Management as the service.",
    ),
    (
        re.compile(r"\bData Platform program\b", re.IGNORECASE),
        "The Baltimore City Data Platform is a product, not a program.",
    ),
    (
        re.compile(r"\*\*Director[’']s Office\.\*\*[^\n]*\binspections\b", re.IGNORECASE),
        "CitiStat inspection belongs to Performance, not the Director's Office.",
    ),
    (
        re.compile(r"\*\*Innovation Lab\.\*\*[^\n]*\bOwns OPI[’']s methods\b", re.IGNORECASE),
        "Do not imply that OPI owns the externally authored Public Innovation Toolkit.",
    ),
    (
        re.compile(r"\bOPI[’']s strategic priorities\b", re.IGNORECASE),
        "Strategic Priorities guidance is retired; describe the durable concept instead.",
    ),
    (
        re.compile(r"\bFY26 permit reform priority\b", re.IGNORECASE),
        "Remove expired fiscal-year priority language from the durable glossary.",
    ),
    (
        re.compile(r"\bFY26\b[^\n]*\bWorkday\b[^\n]*\bpriority\b", re.IGNORECASE),
        "Remove expired fiscal-year priority language from the durable glossary.",
    ),
    (
        re.compile(
            r"Technical Program Manager \(a Data and Analytics role\)",
            re.IGNORECASE,
        ),
        "The Technical Program Manager is a Director's Office role.",
    ),
)

CITISTAT_DRIFT_PATTERNS = (
    (
        re.compile(r"\bagency briefs?\b", re.IGNORECASE),
        "The portfolio mixes agency and thematic Stats; call these Stat briefs.",
    ),
    (
        re.compile(r"\bagency portfolio\b", re.IGNORECASE),
        "The CitiStat portfolio includes agency and thematic Stats; call it the Stat portfolio.",
    ),
    (
        re.compile(r"\bcurrent schedule of active Stats\b", re.IGNORECASE),
        "The portfolio is a register; calendar details are maintained separately.",
    ),
    (
        re.compile(
            r"\bPerformance team owns how the city reviews performance\b",
            re.IGNORECASE,
        ),
        "Performance owns the method; the Executive Director owns CitiStat as CitiStat Director.",
    ),
    (
        re.compile(r"\bteam owns\b[^\n]*\bCitiStat\b[^\n]*\bprogram\b", re.IGNORECASE),
        "The Executive Director owns CitiStat; Performance operates it day to day.",
    ),
    (
        re.compile(r"\bPerformance routines and CitiStat belong to\b", re.IGNORECASE),
        "Performance owns the method and operates CitiStat; it does not own the program.",
    ),
)


def _relative_path(path: Path, repo_root: Path) -> str:
    """Return a repository-relative display path."""

    return str(path.relative_to(repo_root))


def _heading_level(line: str) -> int:
    """Return a Markdown heading level, or zero for a non-heading line."""

    match = re.match(r"^(#+)\s+\S", line)
    return len(match.group(1)) if match else 0


def check_empty_headings(
    path: Path,
    lines: Sequence[str],
    *,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Flag headings with no body before the next sibling heading or EOF.

    A heading followed by a deeper heading (its own subsection) is not empty.
    """

    issues: list[str] = []
    for index, line in enumerate(lines):
        level = _heading_level(line)
        if level == 0:
            continue
        next_index = index + 1
        while next_index < len(lines) and lines[next_index].strip() == "":
            next_index += 1
        if next_index >= len(lines):
            issues.append(
                f"{_relative_path(path, repo_root)}:{index + 1}: "
                f"empty heading '{line.strip()}' (end of file)"
            )
            continue
        next_level = _heading_level(lines[next_index])
        # A deeper heading is a subsection. A higher one is often a styled
        # level-one subtitle. Only an immediate sibling proves emptiness.
        if next_level == level:
            issues.append(
                f"{_relative_path(path, repo_root)}:{index + 1}: empty heading '{line.strip()}'"
            )
    return issues


def check_duplicate_blockquotes(
    path: Path,
    lines: Sequence[str],
    *,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Return duplicate long blockquotes that suggest copy drift."""

    counts: dict[str, int] = {}
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("> ") and len(stripped) > 60:
            counts[stripped] = counts.get(stripped, 0) + 1
    return [
        f"{_relative_path(path, repo_root)}: blockquote repeated {count}x: '{quote[:55]}...'"
        for quote, count in counts.items()
        if count >= 2
    ]


def check_service_sections(
    path: Path,
    text: str,
    *,
    services_dir: Path = SERVICES_DIR,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Return missing shared sections for canonical service summaries."""

    try:
        relative_path = path.relative_to(services_dir)
    except ValueError:
        return []

    # A service can be a direct file or a nested section landing page. The
    # services landing page and supporting detail pages do not use this shape.
    is_direct_service_page = len(relative_path.parts) == 1 and path.name != "index.md"
    is_nested_service_landing = len(relative_path.parts) == 2 and path.name == "index.md"
    if not (is_direct_service_page or is_nested_service_landing):
        return []
    return [
        f"{_relative_path(path, repo_root)}: service page missing required section '{section}'"
        for section in SERVICE_REQUIRED
        if section not in text
    ]


def check_toc_sections(
    path: Path,
    text: str,
    *,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Return missing sections for team theory-of-change pages."""

    if not path.name.endswith("-theory-of-change.md"):
        return []
    return [
        f"{_relative_path(path, repo_root)}: theory-of-change page missing required section "
        f"'{section}'"
        for section in TOC_REQUIRED
        if section not in text
    ]


def check_glossary_taxonomy(
    path: Path,
    text: str,
    *,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Reject glossary wording that reintroduces verified taxonomy drift."""

    if path.as_posix().split("/")[-3:] != ["resources", "reference", "glossary.md"]:
        return []

    issues: list[str] = []
    for pattern, message in GLOSSARY_DRIFT_PATTERNS:
        for match in pattern.finditer(text):
            line_number = text.count("\n", 0, match.start()) + 1
            issues.append(f"{_relative_path(path, repo_root)}:{line_number}: {message}")
    return issues


def check_citistat_narrative(
    path: Path,
    text: str,
    *,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Reject wording that blurs CitiStat ownership or portfolio composition."""

    if not _is_citistat_narrative_path(path):
        return []

    issues: list[str] = []
    for pattern, message in CITISTAT_DRIFT_PATTERNS:
        for match in pattern.finditer(text):
            line_number = text.count("\n", 0, match.start()) + 1
            issues.append(f"{_relative_path(path, repo_root)}:{line_number}: {message}")
    return issues


def _is_citistat_narrative_path(path: Path) -> bool:
    """Return whether a source participates in the CitiStat ownership narrative."""

    normalized_path = path.as_posix()
    is_citistat_page = "what-we-do/programs/citistat" in normalized_path
    is_performance_page = "about-us/our-teams/performance" in normalized_path
    is_innovation_page = "about-us/our-teams/innovation-lab" in normalized_path
    is_team_index_cards = normalized_path.endswith("about-us/our-teams/index.cards.yml")
    is_glossary = normalized_path.endswith("resources/reference/glossary.md")
    return (
        is_citistat_page
        or is_performance_page
        or is_innovation_page
        or is_team_index_cards
        or is_glossary
    )
