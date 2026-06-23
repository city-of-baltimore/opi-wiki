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
- **About Us flattened** (Mission/Vision + Principles promoted; about-opi layer removed)
- **How We Work regrouped** into Organization + Handbook sub-sections

## Big agent review — DONE (6/6 agree-with-changes)
Ran 4 personas + Consistency/Parity + Editor/Streamlining on the live reorg.
Synthesis: `notes/reviews/SYNTHESIS2.md`. Structure is production-ready; remaining
work is a streamlining + consistency pass, not re-architecture.

## 🔜 Pending — round-2 P0/P1 (ranked by reviewer consensus)
- **P0-1 One loop page** — make `how-work-moves` canonical; retire `operating-frame`
  + merge-then-retire `teams-programs-foundations` (move Function Boundaries table in);
  replace loop restatements with teaser+link. ⚠️ reverses "keep + group"
- **P0-2 Naming layer** — one term per concept (model name; team≠portfolio; disambiguate
  Performance/CPM/CitiStat + Innovation Lab team-vs-service)
- **P0-3 One ToC skeleton** — strip PURPOSE/SERVICE-DEFINITION from IL+AdminOps, normalize
  section-2/section-5 headings, fix lying "OF 05" counts, retitle Performance team ToC
- **P1-1 CitiStat two sources of truth** — cut `strategic-framework` 19-Stat cards → link to `portfolio/`
- **P1-2 Two CAD pages** in Services — host deep version once, link from service page
- **P1-3 Service pages** — collapse "Priority outcomes" + "What this means for people". ⚠️ deviates from budget template
- **P1-4 Team index pages** not parallel (8→32 lines) — shared skeleton
- **P1-5 Crosswalk dollars** — add cost-center/FTE column. ⚠️ needs per-service budget data
- **P2 polish** — How-to-Engage homepage anchor + "request landed on my desk" framing;
  front-door taxonomy de-dup; CAD insider terms/short-form glossary; label nits (AUDIENCE:PUBLIC, casing, full-stack filename)
- **Products placeholders** — Data Platform + Performance Portal stubs; acceptable-with-note vs fill

## Decisions captured
- One roster on Team & Roles (done); fill team parity (done); pre-review cleanup (done)
- IL "both a team and a service" language eliminated (done)
