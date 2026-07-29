"""Report possibly undefined acronyms in eligible authored Markdown."""

from __future__ import annotations

import re
from collections.abc import Collection
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS = REPO_ROOT / "docs"
HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
ACRONYM_RE = re.compile(r"\b[A-Z]{2,5}\b")

# Common acronyms that are fine unexpanded. The glossary's acronyms are merged
# in at runtime so the allowlist grows with the site terminology reference.
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
    PLAN DONE MORE LESS GUIDE HACK NOTE OWNER STYLE TODO WARN
    I II III IV V VI VII VIII IX X YYYY MM DD HH SS
    """.split()
)


def load_acronym_allowlist(
    docs_dir: Path = DOCS,
    *,
    authored_paths: Collection[Path] | None = None,
) -> set[str]:
    """Load curated acronyms plus terms from an eligible authored glossary."""

    allow = set(BASE_ALLOW)
    glossary = docs_dir / "resources" / "reference" / "glossary.md"
    if authored_paths is not None and glossary not in authored_paths:
        return allow
    if glossary.exists():
        try:
            glossary_text = glossary.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
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
    display_path = str(path.relative_to(repo_root))
    return [(display_path, token) for token in sorted(found)]
