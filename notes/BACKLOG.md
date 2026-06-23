# OPI Wiki — Running Change Backlog

Tracks production-readiness work on `ddw/content-reorg`. Updated as items land.
Source inputs: persona reviews + synthesis (`notes/reviews/SYNTHESIS.md`), two wiki
audits (`notes/reviews/audit_content.md`, `notes/reviews/audit_reference.md`).

## ✅ Done (committed)
- Restructure into teams / services / programs / products; **What We Do** grouping
- Org chart reflection (Gabriel Watson IPM, Roberto TPM, Mallory → DO, PINs)
- PD consolidations + Full Stack Engineer retitle; full role↔PD parity
- Repo → city-of-baltimore/opi-wiki (edit/PR flow)
- IA consolidation: About Us = identity; How We Work = operating model + machinery
- Team & Roles render fix + roster slim; **merged roster** (one people list, Staff Directory retired)
- Service pages standardized; **Innovation Lab dual-nature language removed** (parity)
- CAD "ToC" → Service Definition; **team-page parity** (added about-innovation-lab, admin-ops-strategy)
- Public section eliminated; staff-directory + roster merge
- External front doors: How to Engage OPI + intake on CAD/CitiStat
- **Acronyms → glossary** reference + sharper linter allowlist
- **Service Crosswalk** (mandate → goal → outcomes) for funders
- Audit fixes: stale PD names, PD compensation parity, strategic-priorities, empty headings, name bug
- Consistency linter (`check_consistency.py`) wired into verify.py
- **Test suite green** (55); ToC category labels normalized

## 🔜 Pending — before / during the big review
- **ToC structural standardization** (focused follow-up) — slim the Innovation Lab + AdminOps theory-of-change pages (they carry SERVICE DEFINITION / PURPOSE sections the Performance + Data ToCs don't, overlapping the about/strategy pages) to the lean NORTH-STAR→logic-model skeleton
- **Minor polish batch** — service "outcomes vs what-this-means" overlap; `strategic-framework` duplicate portfolio cards (2nd source of truth vs `portfolio/`); memo date-format consistency; cosmetic glyph/title nits
- **Products placeholders** — Data Platform + Performance Portal are stubs; decide acceptable-with-note vs fill

## Big agent review (designed, ready to launch)
Re-run the 4 personas (staff, partner, funder, storyteller) on the updated site +
a **Consistency/Parity** reviewer + an **Editor/Streamlining** reviewer, same forced-
output rubric as round 1, then a synthesis comparing to the round-1 baseline.

## Decisions captured
- One roster on Team & Roles (done); fill team parity (done); pre-review cleanup (done)
- IL "both a team and a service" language eliminated (done)
