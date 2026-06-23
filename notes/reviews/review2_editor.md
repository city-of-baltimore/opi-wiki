# Review 2 — Editor / Streamlining Pass

**Reviewer role:** Editor / streamlining. **Date:** 2026-06-23.
**Lens:** Cut words, sections, and whole pages without losing meaning. The Director wants clear, crisp, consistent, no bloat.

---

## Headline

The reorg landed the *structure* well — six clean top sections, a canonical loop page, and a real taxonomy. But the content didn't get cut to match. Three things now say the same thing as `how-work-moves-through-opi.md`, the service pages restate every point twice, and the CitiStat Strategic Framework has become a **second source of truth** for the portfolio. This is a streamlining problem, not a structure problem — and it's fixable in a focused editing pass.

The single biggest issue: **the signal-to-solution loop is written out, in full prose, in at least 6 places** (`index.md`, `how-we-work/index.md`, `how-work-moves-through-opi.md`, `operating-frame.md`, `teams-programs-foundations.md`, `about-admin-ops.md`, plus the orientation guide and CitiStat framework). Every restatement is a future drift point.

---

## Prioritized streamlining list

### P1 — Retire the two legacy omnibus pages in How We Work

**`operating-frame.md` → RETIRE (merge nothing new).**
It restates the loop (the "How the cycle moves" table is the same five steps as `how-work-moves-through-opi.md`), then gives a one-paragraph blurb per service that the `What We Do/Services` pages and the team `about-*` pages already own better. The only content not canonical elsewhere is the "About vs Theory of Change — how to read the package" explainer (lines 49–55). Move those ~4 sentences into `our-teams/index.md` ("How to read the portfolio pages") and delete the page. **Payoff:** kills one full loop restatement and one set of five service mini-definitions; removes a page a reader can't tell apart from `how-work-moves-through-opi`.

**`teams-programs-foundations.md` → MERGE down, then RETIRE.**
This is ~1,450 words. It restates the loop *twice* (lines 13 and 227), re-lists what each portfolio "Owns / Typical Outputs" (already in `org-structure.md` cost-center table + each team page), and re-explains "What Innovation Means / Is Not" (already in `innovation-lab/about-innovation-lab.md`). The genuinely unique content is the **Function Boundaries and Handoffs** table (lines 213–221) — the "who owns it when two portfolios could" rules. That table is valuable and lives nowhere else. Move it into `how-work-moves-through-opi.md` (it belongs right next to "Standard handoffs"), then retire the page. **Payoff:** removes the single most redundant page on the site; consolidates all "who owns the handoff" guidance in one canonical place.

> Net for How We Work: two omnibus pages collapse into the one canonical loop page. The section landing (`how-we-work/index.md`) already restates the loop a third time — once the omnibus pages are gone, trim its loop to a one-line pointer to `how-work-moves-through-opi`.

### P2 — De-duplicate the CitiStat portfolio (two sources of truth)

`strategic-framework.md` (lines 284–437) embeds the **full 19-Stat portfolio as cards** — name, type, cluster, focus for every Stat. That same portfolio is the entire job of `portfolio/index.md` ("The 19 Stats"). Two places now define the portfolio; they *will* diverge the first time a Stat is added, renamed, or re-clustered. **Cut the card grid from the Strategic Framework** and replace it with a 2-sentence summary + link to the portfolio register. **Payoff:** removes ~150 lines, eliminates the most dangerous drift risk on the site, and lets the Framework stay what it claims to be (the strategic case, not a register).

While there: the Framework also carries the **four tenets** and the **right-routine decision table**, both of which appear in `about-performance.md`, `performance-strategy.md`, `method-playbook.md`, and the glossary. Pick one home for the tenets (the Method Playbook) and link to it; the Framework can name them in a sentence.

### P3 — Collapse "Priority outcomes" + "What this means for people" on every service page

All five service pages (`admin-ops`, `citywide-data-and-analytics`, `citywide-performance-management`, `cross-agency-delivery`, `innovation-lab`) carry both sections, and they restate each other. On `citywide-performance-management.md`:
- Priority outcomes: *"Commitments made in a Stat are commitments kept, with evidence of closure."*
- What this means: *"As a Council member, I want confidence that commitments made are commitments kept."*

Same point, twice, in two formats. **Keep one.** The persona "As a resident… / As a City Administrator…" framing is the more distinctive and human, so keep "What this means for people" and delete "Priority outcomes" (or fold the one or two outcomes it adds into the personas). **Payoff:** ~8 lines off each of 5 pages and a crisper read; the service pages currently feel like a filled-in template.

### P4 — Merge the two Cross-Agency Delivery pages

`services/cross-agency-delivery.md` (the standard service page) and `services/cross-agency-delivery-service-definition.md` (a 1,830-word "Service Definition" with North Star, 8 numbered sections, Theory of Change, governance, SLAs) both live in the same folder. A reader expects one CAD page, not two, and the service-definition file duplicates the depth that the *team theory-of-change* pages carry for the other four services. **Decision:** move the service-definition content to where the parallel lives — it's the CAD equivalent of a Theory of Change, and CAD has no team (it's an overlay), so host it once and link from the service page. Do **not** keep two CAD pages side-by-side under Services. **Payoff:** removes a structural inconsistency (CAD is the only service with two pages in the services folder) and a near-duplicate.

### P5 — Tighten the front door

- **Home (`index.md`):** Good but doing too much. It has the loop *and* the full four-row taxonomy table *and* a separate "How this site works"/"How this site is organized" pair that overlap. Cut the loop to its one-line arrow form (already present) and drop the duplicate taxonomy table — it's repeated verbatim on `what-we-do/index.md`. The "Do not use 'CAD'" nomenclature note (line 34) belongs in the glossary, not the home page.
- **`what-we-do/index.md`** and **`services/index.md`** both open with the same "a service is distinct from a team and a program" taxonomy lesson. One of them should teach it; the other should link. Pick `what-we-do/index.md` to teach it.
- **`org-structure.md`** has three different "how to read this" explainers (Cost Centers vs Services vs Portfolios opener at line 5, the "Five Services" recap at 53–65, and "How to Read This Structure" at 82–92) that all explain the portfolio/service/cost-center distinction. Keep one.

### P6 — Tables that should be prose or should be trimmed

- `strategic-framework.md` is 4,000 words with ~8 fixed-width tables. The "Crosswalk: 7 strategic phases and 12 operating steps" (lines 187–201) is a table that exists only to map to *another* table in the Method Playbook — it's coordination overhead between two staff docs sitting on a public strategy page. Move it to the Method Playbook.
- The fixed-width pipe tables with manual column padding (the `| --- |` walls in `operating-frame`, `org-structure`, `strategic-framework`) are hard to edit and encourage staleness. Several are short enough to be bulleted lists.

---

## FORCED OUTPUTS

**1. One-line reaction:** **Agree-with-changes.** The structure is production-ready; the content is over-written and has two live duplicate-source-of-truth problems that should be cut before this is called done.

**2. Top 3 blockers:**
1. **CitiStat portfolio has two sources of truth** — the card grid in `strategic-framework.md` vs the register in `portfolio/index.md`. Will drift. Cut the cards.
2. **Two legacy omnibus pages** (`operating-frame.md`, `teams-programs-foundations.md`) still duplicate the canonical loop, the per-service definitions, and the org table. A reader can't tell which page is canonical. Retire both, rescuing only the Function Boundaries table.
3. **Two Cross-Agency Delivery pages** in the Services folder — a structural inconsistency that reads as unfinished.

**3. Top 3 low-risk high-impact fixes:**
1. Delete "Priority outcomes" on all 5 service pages (keep the persona section). Mechanical, ~40 lines, instantly crisper.
2. Cut the duplicate taxonomy table from `index.md` (it's verbatim on `what-we-do/index.md`).
3. Trim the loop on `how-we-work/index.md` to a single pointer line once the omnibus pages are gone.

**4. One naming/nomenclature issue:** "Operating model" / "operating frame" / "the loop" / "signal-to-solution loop" / "improvement cycle" are used interchangeably for the *same* concept across `index.md`, `how-we-work/index.md`, `operating-frame.md`, and `teams-programs-foundations.md`. Pick **one** name ("the signal-to-solution loop") and use it everywhere; "Operating Frame" as a page title actively competes with "How Work Moves Through OPI."

**5. One drift risk:** The signal-to-solution loop sentence is hand-written in full prose in 6+ files. The next time the loop wording changes (e.g., a service is renamed), someone updates `how-work-moves-through-opi` and misses the other five. Make `how-work-moves-through-opi` the only place the loop is spelled out in full; everywhere else uses the one-line arrow form or a link.

**6. One audience need the structure misses:** The **partner agency who just got a CitiStat request and wants to know what's about to happen to them** — a 5-minute "what to expect" path. `how-to-engage-opi.md` exists and is pointed to, but it's framed as "request a service," not "a request landed on my desk, what now." That reader currently has to read the 4,000-word Strategic Framework. A short, plain-language partner page would carry real load.

**7. One page that should be canonical (and isn't):** **`how-work-moves-through-opi.md`** is *written* as canonical but isn't *treated* as canonical — three other pages (`operating-frame`, `teams-programs-foundations`, the section landing) carry parallel copies of its loop, its service ownership, and its handoffs. Make it the single home for the loop, "what each service owns," handoffs, and the function-boundary rules (pulled in from `teams-programs-foundations`), and reduce the others to links.
