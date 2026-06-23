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
- Team & Roles table render fix + **roster slim** (item #1); org chart co-located + linked
- **Service pages standardized** to the budget-office template
- Innovation Lab dual-nature explainer; CAD "ToC" → **Service Definition** (item #2)
- **Public section eliminated** (item #6) — files archived to notes/, redirects added
- Staff directory "Email" + Xander (item #4); "MAC" removed (item #5)
- **External front doors** (P0): How to Engage OPI page + intake on CAD & CitiStat
- Quick wins: loop dedupe, SRO, CPM slash
- Audit bugs: Rock→Rakeim Young; youth-stat/tiger-teams/telework/leadership-norms empty headings
- Audit fixes: stale PD role names; PD compensation parity; strategic-priorities dates/headings
- **Consistency linter** (`scripts/check_consistency.py`, wired into verify.py)
- **Test suite green** (55) — reconciled tests + redirect allowlist with the reorg

## 🔜 Pending — backlog
- **Loop consolidation** — mostly done (verbatim dups removed; home/how-we-work link to canonical); optional further tightening
- **Budget-to-outcome crosswalk** page (funder) — home partner card already added
- **Acronyms → glossary** — linter flags ~99 distinct (DCA, RAG, PIN, WIP, TPM, VPN, etc.); curate the real ones into the glossary
- **Team-section asymmetry** — Innovation Lab has no `about-*`; Director's Office has no `*-strategy`
- **ToC-page skeleton parity** — 2 different structures across the 5 service theory-of-change pages
- **Service pages** — tighten "Priority outcomes" vs "What this means for people" overlap
- **strategic-framework** embeds full portfolio cards (2nd source of truth vs `portfolio/`)
- Memo date-format consistency; memo header/title casing
- Minor: `order-food-catering` heading glyphs; book-the-idea-lab title/filename; "tiger team" casing

## Decisions captured
- Public CMS artifacts → notes/ (done); reporting redesign → slim + link org chart (done)
- IA: About Us = identity, How We Work = operating model + machinery (done)
