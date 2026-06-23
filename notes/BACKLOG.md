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

## ✅ Round-2 streamlining (committed)
- **P0-1 One loop page** — `how-work-moves` canonical; `operating-frame` +
  `teams-programs-foundations` retired (Function Boundaries + About-vs-ToC folded in);
  loop sentence locked; restatements → pointer+link; landing cards fixed
- **P0-3 One ToC skeleton** — stripped PURPOSE/SERVICE-DEFINITION from IL+AdminOps,
  normalized section 2/5/8, dropped "OF 05" counts, retitled Performance/Data ToCs;
  `check_consistency` now enforces the ToC skeleton
- **P1-1 CitiStat dedup** — 19-Stat cards cut from `strategic-framework` → link to `portfolio/`
- **P1-2 Two CAD pages** — service-definition dropped from Services nav (kept, linked)
- **P1-3 Service pages** — "Priority outcomes" cut from all 5; AdminOps "Also called" folded in
- **P1-4 Team index parity** — 4 landings normalized to one skeleton
- **P1-5 Crosswalk** — cost-center + budgeted-positions table added (dollars still in budget book)
- **P2 (partial)** — about/ToC badges normalized; commitment-ledger glossary term added

## ✅ Owner round (committed)
- **Priority outcomes restored** to all 5 service pages (+ linter contract)
- **Cross-Agency Delivery → one service page**; Service Definition rehomed with the Innovation Lab
- **portfolio → team** in public surfaces (prose, org-structure, roster, renderer header, glossary); **"Innovation Lab team" → "Innovation Lab"**
- **Work phone column restored** to the roster (11 numbers from git)
- **CitiStat SSOT** — Strategic Framework no longer re-teaches the four tenets / routine table (→ Method Playbook + How Work Moves)
- **How-to-Engage** — added the "a CitiStat request landed on my desk → what to expect" sequence
- **Front-door taxonomy de-dup** — Home is the one taxonomy teacher; what-we-do/index + our-teams/index trimmed to nav + glossary pointers

## 🔜 Still open
- **portfolio → team in internal handbook plumbing** — named bodies ("Portfolio Council"),
  onboarding sub-channels, charter "Portfolio" field, intake-sop; left for a separate operational pass
- **Cosmetic** — `pd-product-engineer-full-stack` filename vs "Full Stack Engineer" title (redirect churn for low gain — recommend skip)
- **Per-service dollars** on the crosswalk — needs budget-book figures
- **Products placeholders** — Data Platform + Performance Portal stubs; acceptable-with-note vs fill

## Decisions captured
- One roster on Team & Roles (done); fill team parity (done); pre-review cleanup (done)
- IL "both a team and a service" language eliminated (done)
