"""Reusable structural and editorial consistency checks for the OPI wiki."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS = REPO_ROOT / "docs"
SERVICES_DIR = DOCS / "what-we-do" / "services"

HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
ACRONYM_RE = re.compile(r"\b[A-Z]{2,5}\b")

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

# Common acronyms that are fine unexpanded. The glossary's acronyms are merged
# in at runtime so the allowlist grows with the public terminology reference.
BASE_ALLOW = frozenset(
    """
    OPI MOPI AI IT HR QA KPI SOP SLA US OK ED CA DM CDO DCDO DCPO DCA SRO PMO ORF
    RAG COOP OSHA WCAG ETL ELT GIS API APIs CSV PDF URL MVP UX UI FAQ FY MOU RFP BIC
    BCDP CCA EOY TBD SQL CI CD ICYMI BCIT BBMR BCPSS BCRP DGS DOT DPW BPD EMS DHR
    DHCD HCD MOED MONSE MOGR BCFD MOIT DPOB LIGHT MAPS RISE DDO PD BI AV ID MCP OOO
    PTO GenBI BCHD DJS ECB HKS BDC DCPBL MWBOO WBE BMORE UMBC WIP PR QC ML UAT PPE JD
    AM PM FMLA ADA AVL CIO COB FYI GPS HVAC IDE IRS ISO JIRA JSON KB MD RBAC SMS SSPR
    AA GRIT AIM ORM VPN SSO MFA WFH SBAR NNN SMBA
    """.split()
)

# Words that are not acronyms but match [A-Z]{2,5}, including common ALL-CAPS
# heading words, Roman numerals, and date/time placeholders.
STOPWORDS = frozenset(
    """
    THE AND OF FOR HOW ABOUT READ STAFF NORTH STAR WHAT WHEN WHO WHY WITH FROM THIS
    THAT OWN WE OUR USE ALL NOT ARE WAS HAS HER HIS ITS OUT NEW NOW ONE TWO WORK TEAM
    PLAN DONE MORE LESS I II III IV V VI VII VIII IX X YYYY MM DD HH SS
    """.split()
)


@dataclass(frozen=True)
class ConsistencyScan:
    """Collected structural issues and informational acronym findings."""

    structural_issues: tuple[str, ...]
    acronyms: tuple[tuple[str, str], ...]


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


def load_acronym_allowlist(docs_dir: Path = DOCS) -> set[str]:
    """Load the curated and glossary-derived acronym allowlist."""

    allow = set(BASE_ALLOW)
    glossary = docs_dir / "resources" / "reference" / "glossary.md"
    if glossary.exists():
        try:
            glossary_text = glossary.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Unable to read acronym glossary: {glossary}") from error
        allow.update(ACRONYM_RE.findall(glossary_text))
    return allow


def acronym_report(
    path: Path,
    text: str,
    allow: set[str],
    *,
    repo_root: Path = REPO_ROOT,
) -> list[tuple[str, str]]:
    """Return possibly undefined acronyms on one page."""

    found: set[str] = set()
    # Skip headings because the wiki uses ALL-CAPS titles that are not acronyms.
    body = "\n".join(line for line in text.split("\n") if not HEADING_RE.match(line))
    for token in ACRONYM_RE.findall(body):
        if token in allow or token in STOPWORDS:
            continue
        if f"({token})" in text:
            continue
        found.add(token)
    display_path = _relative_path(path, repo_root)
    return [(display_path, token) for token in sorted(found)]


def scan_consistency(
    docs_dir: Path = DOCS,
    *,
    repo_root: Path = REPO_ROOT,
) -> ConsistencyScan:
    """Read published Markdown and collect all consistency findings."""

    structural_issues: list[str] = []
    acronyms: list[tuple[str, str]] = []
    allow = load_acronym_allowlist(docs_dir)
    services_dir = docs_dir / "what-we-do" / "services"

    for path in sorted(docs_dir.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
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
        acronyms.extend(acronym_report(path, text, allow, repo_root=repo_root))

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
