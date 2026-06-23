# OPI Wiki — Running Change Backlog

Tracks production-readiness work on `ddw/content-reorg`. Updated as items land.
Source inputs: persona reviews + synthesis (`notes/reviews/SYNTHESIS.md`), two wiki
audits (`notes/reviews/audit_content.md`, `notes/reviews/audit_reference.md`).

## ✅ Done (committed)
- Restructure into teams / services / programs / products
- Reflect org chart: Gabriel Watson IPM; Roberto TPM; Mallory → Director's Office; PINs/classifications
- PD consolidations + Full Stack Engineer retitle; full role↔PD parity
- Repo → city-of-baltimore/opi-wiki (edit/PR flow)
- Group services/programs/products under **What We Do**; Teams stay top-level
- Fix Team & Roles table rendering (code-block bug) + ToC pollution
- **Service pages standardized** to the budget-office template (goal, mandate, outcomes, "what this means for people")
- Innovation Lab dual-nature explainer (P0)
- Reframe "CAD Theory of Change" → **Cross-Agency Delivery Service Definition** (item #2)
- Staff directory: "Email" column + Xander's address (item #4)
- Remove undefined "MAC" (item #5)
- Quick wins: loop blockquote dedupe, SRO spelled out, CPM/CitiStat slash
- Audit bugs: "Rock Young" → Rakeim Young; youth-stat + tiger-teams empty headings

## 🔜 Pending — decided, ready to execute
- **#6 Public elimination** — move website-copy + IA to `notes/`; retire 3 briefs (redirect to canonical); drop `public/` from nav
- **#1 Reporting redesign** — slim roster tables; surface the org chart
- **IA consolidation** — About Us vs How We Work (see proposal below) — *awaiting confirmation*

## 🔜 Pending — P0 / backlog
- **Loop consolidation** — make `how-work-moves` the one canonical telling; others excerpt-and-link (mostly done; tighten)
- **External front doors** — "how to request this" + opi@ on CAD & CitiStat; agency-partner landing page
- **Consistency linter** — new `scripts/check_consistency.py` (required-sections, undefined-acronym, empty-heading, duplicate-block, stale-date)
- **Public-value home cards** + budget-to-outcome crosswalk (funder)

## 🔜 Pending — audit findings (batched)
- Stale PD role names: `pd-chief-of-staff`, `pd-citistat-inspector` ("Comms & Partnerships Lead", "Special Assistant")
- PD parity: lone "Compensation range" row on D&A applied-data-scientist
- ToC-page skeleton parity (2 different structures across 5 service ToCs)
- Team-section asymmetry: Innovation Lab has no `about-*`; Director's Office has no `*-strategy`
- Undefined acronyms → glossary: DCA, RAG, PIN, BoB, agency abbrevs (DGS/DOT/DPW/BPD/EMS/BCRP/DHR/MOED), DCDO/DCPO/CDO
- `strategic-priorities-one-pager`: past dates ("by Jan 2026"), "17 vs 19 Stats", mixed H3/bold headings
- `citistat-public-brief` "three core services" but names five
- Memo date-format inconsistency; memo header/title casing
- Service pages: "Priority outcomes" vs "What this means for people" overlap (tighten)
- `strategic-framework` embeds full portfolio cards (2nd source of truth vs `portfolio/`)
- Minor: `order-food-catering` heading glyphs; book-the-idea-lab title/filename mismatch; "tiger team" casing

## Decisions captured
- Public CMS artifacts (website-copy, website-IA) → move to `notes/` (out of built site)
- Reporting redesign → slim tables + link org chart
