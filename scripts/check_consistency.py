#!/usr/bin/env python3
"""Consistency linter for the OPI wiki.

Catches the classes of structural/editorial defect that page-by-page review
tends to miss:

- Empty headings (a heading with no content before the next heading / EOF)
- Duplicate blockquotes repeated within a single page
- Service pages missing a required section (template parity)
- Undefined acronyms (informational report; allowlist seeded from the glossary)

Hard checks fail the run (exit 1). The acronym report is informational only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"

HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
ACRONYM_RE = re.compile(r"\b[A-Z]{2,5}\b")

SERVICE_REQUIRED = [
    "## What this service does",
    "## The goal",
    "## Mandate",
    "## Priority outcomes",
    "## What this means for people",
]

# Every team service-theory-of-change page shares one skeleton (NORTH STAR + the
# numbered logic model). Enforcing it keeps the ToCs from drifting apart again.
TOC_REQUIRED = [
    "## NORTH STAR",
    "### 1. Service overview",
    "### 2. Operating scope (boundary lines)",
    "### 3. Engagement model",
    "### 4. Theory of Change",
    "### 5. Governance and decision rights",
    "### 6. Core offerings and target service levels",
    "### 7. Metrics, targets, and learning",
    "### 8. Operational handoffs across OPI services",
]

# Common acronyms that are fine unexpanded (curated). The glossary's acronyms
# are merged in at runtime so the allowlist grows with the glossary.
BASE_ALLOW = {
    "OPI", "MOPI", "AI", "IT", "HR", "QA", "KPI", "SOP", "SLA", "US", "OK",
    "ED", "CA", "DM", "CDO", "DCDO", "DCPO", "DCA", "SRO", "PMO", "ORF", "PIN",
    "RAG", "COOP", "OSHA", "WCAG", "ETL", "ELT", "GIS", "API", "APIs", "CSV",
    "PDF", "URL", "MVP", "UX", "UI", "FAQ", "FY", "MOU", "RFP", "BIC", "BCDP",
    "CCA", "EOY", "TBD", "FAQ", "SQL", "CI", "CD", "ICYMI",
    # Baltimore agencies / offices
    "BCIT", "BBMR", "BCPSS", "BCRP", "DGS", "DOT", "DPW", "BPD", "EMS", "DHR",
    "DHCD", "HCD", "MOED", "MONSE", "MOGR", "BCFD", "MOIT", "DPOB", "LIGHT",
    "MAPS", "RISE", "DDO", "PD", "BI", "AV", "ID", "MCP", "OOO", "PTO", "GenBI",
    "BCHD", "DJS", "ECB", "HKS", "BDC", "DCPBL", "MWBOO", "WBE", "BMORE", "UMBC",
    # standard technical / HR acronyms used in how-to guides and memos
    "WIP", "PR", "QC", "ML", "UAT", "PPE", "JD", "AM", "PM", "FMLA", "ADA",
    "AVL", "CIO", "COB", "FYI", "GPS", "HVAC", "IDE", "IRS", "ISO", "JIRA",
    "JSON", "KB", "MD", "RBAC", "SMS", "SSPR", "AA", "GRIT", "AIM", "ORM",
    "VPN", "SSO", "MFA", "WFH", "SBAR", "NNN", "SMBA",
}

# Words that are not acronyms but match [A-Z]{2,5} (common in ALL-CAPS headings),
# Roman numerals, and date/time placeholders.
STOPWORDS = {
    "THE", "AND", "OF", "FOR", "HOW", "ABOUT", "READ", "STAFF", "NORTH", "STAR",
    "WHAT", "WHEN", "WHO", "WHY", "WITH", "FROM", "THIS", "THAT", "OWN", "WE",
    "OUR", "USE", "ALL", "NOT", "ARE", "WAS", "HAS", "HER", "HIS", "ITS", "OUT",
    "NEW", "NOW", "ONE", "TWO", "WORK", "TEAM", "PLAN", "DONE", "MORE", "LESS",
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "YYYY", "MM", "DD", "HH", "SS",
}


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def md_files() -> list[Path]:
    return sorted(DOCS.rglob("*.md"))


def _heading_level(line: str) -> int:
    m = re.match(r"^(#+)\s+\S", line)
    return len(m.group(1)) if m else 0


def check_empty_headings(path: Path, lines: list[str]) -> list[str]:
    """Flag a heading with no body before the next sibling/parent heading.

    A heading followed by a deeper heading (its own subsection) is NOT empty.
    """
    issues: list[str] = []
    for i, line in enumerate(lines):
        level = _heading_level(line)
        if level == 0:
            continue
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j >= len(lines):
            issues.append(f"{rel(path)}:{i + 1}: empty heading '{line.strip()}' (end of file)")
            continue
        next_level = _heading_level(lines[j])
        # Same-level next heading with nothing between = empty section.
        # (A deeper next heading is a subsection; a higher one is often a
        # styled level-1 subtitle — neither is treated as empty.)
        if next_level == level:
            issues.append(f"{rel(path)}:{i + 1}: empty heading '{line.strip()}'")
    return issues


def check_duplicate_blockquotes(path: Path, lines: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    for line in lines:
        s = line.strip()
        if s.startswith("> ") and len(s) > 60:
            counts[s] = counts.get(s, 0) + 1
    return [
        f"{rel(path)}: blockquote repeated {c}x: '{q[:55]}...'"
        for q, c in counts.items()
        if c >= 2
    ]


def check_service_sections(path: Path, text: str) -> list[str]:
    if path.parent.name != "services":
        return []
    if path.name == "index.md":
        return []
    return [
        f"{rel(path)}: service page missing required section '{sec}'"
        for sec in SERVICE_REQUIRED
        if sec not in text
    ]


def check_toc_sections(path: Path, text: str) -> list[str]:
    if not path.name.endswith("-theory-of-change.md"):
        return []
    return [
        f"{rel(path)}: theory-of-change page missing required section '{sec}'"
        for sec in TOC_REQUIRED
        if sec not in text
    ]


def load_acronym_allowlist() -> set[str]:
    allow = set(BASE_ALLOW)
    glossary = DOCS / "resources" / "reference" / "glossary.md"
    if glossary.exists():
        allow |= set(ACRONYM_RE.findall(glossary.read_text(encoding="utf-8")))
    return allow


def acronym_report(path: Path, text: str, allow: set[str]) -> list[tuple[str, str]]:
    found = set()
    # Skip headings — the wiki uses ALL-CAPS section titles that aren't acronyms.
    body = "\n".join(l for l in text.split("\n") if not HEADING_RE.match(l))
    for token in ACRONYM_RE.findall(body):
        if token in allow or token in STOPWORDS:
            continue
        if f"({token})" in text:  # expanded somewhere on the page
            continue
        found.add(token)
    return [(rel(path), token) for token in sorted(found)]


def main() -> int:
    hard: list[str] = []
    acronyms: list[tuple[str, str]] = []
    allow = load_acronym_allowlist()

    for path in md_files():
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        hard += check_empty_headings(path, lines)
        hard += check_duplicate_blockquotes(path, lines)
        hard += check_service_sections(path, text)
        hard += check_toc_sections(path, text)
        acronyms += acronym_report(path, text, allow)

    if acronyms and ("--acronyms" in sys.argv or "-a" in sys.argv):
        by_token: dict[str, int] = {}
        for _fname, token in acronyms:
            by_token[token] = by_token.get(token, 0) + 1
        print(f"[consistency] {len(by_token)} distinct possibly-undefined acronym(s) "
              "(informational — add to the glossary or expand on first use):")
        for token in sorted(by_token, key=lambda t: (-by_token[t], t)):
            print(f"  {token} ({by_token[token]} use(s))")
    elif acronyms:
        print(f"[consistency] {len(set(t for _f, t in acronyms))} distinct "
              "possibly-undefined acronyms — run with --acronyms to list them.")

    if hard:
        print(f"\n[consistency] {len(hard)} structural issue(s):")
        for issue in hard:
            print(f"  {issue}")
        return 1

    print("Consistency checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
