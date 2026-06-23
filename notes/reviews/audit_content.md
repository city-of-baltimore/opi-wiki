# OPI Wiki — Content Consistency & Quality Audit

**Scope:** `docs/how-we-work/`, `docs/what-we-do/`, `docs/our-teams/`
**Date:** 2026-06-22
**Method:** Source review against live site (http://127.0.0.1:8092/) plus the site glossary (`docs/resources/reference/glossary.md`, out of scope but used as the authority for acronym/term checks).

> Note on working-tree state: at audit time the four short service pages and several other files had uncommitted edits in progress that added a shared structure (`What this service does / The goal / Mandate / Priority outcomes / What this means for people / Delivered by / Read alongside`). Findings below reflect the **current on-disk content** (what the live site serves), not committed HEAD.

---

## 1. Inconsistent structure within a page type

### 1.1 Service pages — RESOLVED DURING AUDIT (was HIGH)
- **File:** `docs/what-we-do/services/cross-agency-delivery.md`
- **Status:** Was the lone outlier; it has since been rewritten to the shared service spine (*What this service does · The goal · Mandate · Priority outcomes · What this means for people · Delivered by · Read alongside*). All five service pages now match. No action needed — recorded for completeness.

### 1.2 Service `page_header` category label — RESOLVED DURING AUDIT (was MED)
- **File:** `docs/what-we-do/services/cross-agency-delivery.md`
- **Status:** Was `category="OPI · FOUNDATIONS"`; now `category="OPI · SERVICE"`, matching all four siblings. No action needed.

### 1.3 Theory of Change pages — two different page skeletons (HIGH)
- **Files:** `our-teams/data-and-analytics/data-analytics-theory-of-change.md` and `our-teams/performance/performance-theory-of-change.md` use a single `## NORTH STAR` H2 followed by a numbered `### 1–8` structure. `our-teams/directors-office/admin-ops-theory-of-change.md`, `our-teams/innovation-lab/innovation-lab-theory-of-change.md`, and `what-we-do/services/cross-agency-delivery-theory-of-change.md` use top-level H2 sections (`## NORTH STAR`, `## SERVICE DEFINITION`, `## PURPOSE AND PHILOSOPHIES`) *before* the numbered 1–8 block.
- **Fix:** Pick one ToC skeleton and apply it to all five.

### 1.4 ToC pages — extra trailing sections only on some siblings (LOW)
- **Files:** `performance-theory-of-change.md` ends with `## See also`; `data-analytics-theory-of-change.md` has no `See also`. `innovation-lab-theory-of-change.md` adds `## Relationship to Cross-Agency Delivery and Tiger Teams`; `cross-agency-delivery-theory-of-change.md` adds `## Relationship to the Innovation Lab`; the others have neither.
- **Fix:** Standardize the trailing `See also` / relationship sections across all ToC pages.

### 1.5 "About" team pages — Innovation Lab has no About page (MED)
- **Files:** `our-teams/data-and-analytics/about-data-analytics.md`, `directors-office/about-admin-ops.md`, `performance/about-performance.md` exist; `our-teams/innovation-lab/` has **no `about-*.md`**.
- **Fix:** Add `about-innovation-lab.md` for symmetry, or drop the About pattern for all teams.

### 1.6 Team file sets are asymmetric (MED)
- **Files:** `directors-office/` has **no `*-strategy.md`** (the other three teams each have one). `data-and-analytics/` is the only team with a `data-governance-framework.md`. `innovation-lab/` has a `digital-product-methodology.md` no other team has.
- **Fix:** Document the intentional asymmetries, or add the missing strategy page for the Director's Office.

### 1.7 Team index pages have inconsistent section sets (MED)
- **Files:** `our-teams/*/index.md`. `performance/index.md` has *Pages in this section · The CitiStat program · Works closely with · Position descriptions · A note on language*; `directors-office/index.md` has only *What this team does · Position descriptions*; `data-and-analytics/index.md` has *Strategy and methodology · Position descriptions*; `innovation-lab/index.md` has *Pages in this section · Position descriptions*. Heading for the first section also varies ("What this team does" vs "Pages in this section" vs "Strategy and methodology").
- **Fix:** Adopt a common team-index skeleton (e.g., intro · Pages in this section · Position descriptions · Works closely with).

### 1.8 `about-*` team pages: section drift (LOW)
- **Files:** `directors-office/about-admin-ops.md` has extra `### Field evidence rule` and `### Partnership operating rule`; `performance/about-performance.md` has extra `### The four tenets of Stat` and a `## See also`; `about-data-analytics.md` has neither set.
- **Fix:** Accept page-specific sections but align the common backbone and add/remove `See also` consistently.

### 1.9 Strategy pages: heading-case + structure drift (MED)
- **Files:** `data-analytics-strategy.md` and `innovation-lab-strategy.md` use ALL-CAPS H2s (`## EXECUTIVE SUMMARY`, `## WHAT THE LAB OWNS`, …). `performance/performance-strategy.md` uses Title/sentence-case H2s (`## From performance to action`, `## See also`) and an entirely different internal structure (only two H2s for a 260-line page).
- **Fix:** Bring `performance-strategy.md` into the shared strategy skeleton + casing used by its two siblings.

### 1.10 How-to pages have no shared structure or title casing (MED)
- **Files:** `how-we-work/how-to/*.md`. Titles mix Title Case ("Add a Printer", "Change Your City Password") with sentence case ("Order food or catering from preferred vendors", "Reserving the Idea Lab"). Several pages have **no `##` sections at all** (`add-a-printer.md`, `change-your-city-password.md`); others use "Step 1/Step 2", "Option 1/Option 2", or freeform headings.
- **Fix:** Define a how-to template (e.g., *Before you start · Steps · If it doesn't work*) and a single title-casing convention.

---

## 2. Awkward or broken formatting

### 2.1 Stray empty `## CLOSING` heading pollutes ToC (MED)
- **File:** `what-we-do/programs/citistat/portfolio/youth-stat.md` (line 51)
- **Issue:** All 19 portfolio stat pages share an identical H3 spine (Public Purpose / Staff Purpose / Core Management Questions / Starter Focus Areas / Standard Artifacts and Data Products / Tiger Team / Delivery Triggers). `youth-stat.md` alone appends a bare `## CLOSING` H2 with **no body** — a leftover that shows in the table of contents.
- **Fix:** Delete the empty `## CLOSING` heading.

### 2.2 Very wide tables likely to render/scroll poorly (LOW–MED)
- **Files:** widest pipe-table rows exceed 400 chars in `baltimore-intelligence-center/governance-and-risks.md` (426), `baltimore-intelligence-center/capability-transfer-and-target-state.md` (424), `services/cross-agency-delivery-theory-of-change.md` (421), `our-teams/innovation-lab/innovation-lab-strategy.md` (395), `programs/citistat/method-playbook.md` (328), and the four numbered-ToC pages (`data-analytics-theory-of-change.md` 321, `performance-theory-of-change.md` 312, `admin-ops-theory-of-change.md` 295).
- **Issue:** Single-cell paragraphs of 200–400 chars inside tables read as walls of text and overflow on narrow viewports.
- **Fix:** Convert the densest "definition" tables to definition lists or prose; reserve tables for genuinely tabular data.

### 2.3 `order-food-catering-from-city-vendors.md` odd heading formatting (LOW)
- **File:** `how-we-work/how-to/order-food-catering-from-city-vendors.md`
- **Issue:** Section headings render as `## 72Hrs + Away?` and `## 72Hrs or less Away?` — compressed, inconsistent spacing/capitalization.
- **Fix:** Rewrite as readable headings, e.g., "More than 72 hours out" / "72 hours or less".

---

## 3. Undefined acronyms / jargon

(The site glossary defines: AI, BBMR, BCIT, CAD, DHCD, HR, IT, KPI, LIGHT, MVP, OPI, ORF, OWNER, PMO, SOP, SRO. Acronyms below appear in-scope without local expansion and are **not** in the glossary.)

### 3.1 `PIN` used as a table column header, never expanded (MED)
- **File:** `how-we-work/team-and-roles/index.md` (4 roster tables, e.g. lines 48, 61, 84, 103, 128) and `how-we-work/team-and-roles/staff-directory.md` context.
- **Fix:** Expand on first use (Position Identification Number) or add a glossary entry.

### 3.2 `BoB` used before/without definition on a sibling page (LOW)
- **Files:** Defined once in `how-we-work/how-to/submit-your-weekly-update.md` (line 5), but used undefined in the sibling `how-we-work/how-to/edit-a-past-reporting-period-in-book-of-business.md` and again as "the BoB" in the same family. A reader landing on the edit page sees no expansion.
- **Fix:** Expand "Book of Business (BoB)" on first use in each how-to page or add a glossary entry.

### 3.3 Agency acronyms used without expansion (LOW each, MED in aggregate)
- **Files (examples):** `DGS` (`services/cross-agency-delivery.md`, multiple stat pages), `DOT`, `DPW`, `BPD`, `EMS`, `BCRP`, `DHR`, `MOED`, `MONSE`, `MOGR`, `DCDO`/`DCA`/`DCPO`/`CDO` (deputy/chief officer abbreviations across `our-teams/` strategy + ToC pages and `team-and-roles/index.md`).
- **Issue:** None of these are in the glossary; most appear first inside dense tables with no expansion.
- **Fix:** Add the recurring agency + officer abbreviations to the glossary, or expand on first use per page.

### 3.4 BIC technical jargon (mostly defined, two gaps) (LOW)
- **File:** `what-we-do/products/baltimore-intelligence-center/`. `reference.md` glossary covers BIC, MCP/tool layer, semantic layer, medallion architecture, etc. — good. But `GenBI`, `RAG`, and `GIS` appear in `roadmap-and-source-systems.md` / other BIC pages without expansion and are not in the BIC glossary.
- **Fix:** Add `GenBI`, `RAG`, `GIS` to the BIC `reference.md` glossary.

> The Director-flagged "MAC" no longer appears anywhere in scope — already resolved.

---

## 4. Redundancy / duplication

### 4.1 Service pages restate the same points in two adjacent sections (MED)
- **Files:** all four standard service pages — `services/admin-ops.md`, `citywide-data-and-analytics.md`, `citywide-performance-management.md`, `innovation-lab.md`.
- **Issue:** "Priority outcomes" and "What this means for people" cover the same four ideas in two voices. On `admin-ops.md` they are near-verbatim (e.g., "Priority work is driven, tracked, and communicated" ↔ "I want confidence that priority work is being driven, tracked, and communicated").
- **Fix:** Keep one framing (outcomes *or* persona statements), or differentiate them so they don't echo.

### 4.2 The signal-to-solution loop is retold on many pages (LOW–MED)
- **Files:** narrated/listed in `how-we-work/index.md`, `how-we-work/how-work-moves-through-opi.md`, `what-we-do/index.md`, `what-we-do/services/index.md`, `what-we-do/programs/index.md`, `what-we-do/programs/citistat/index.md`, `our-teams/index.md`, and again as the "Why it matters / In the signal-to-solution loop, this is the step that…" sentence in all five service pages.
- **Fix:** Make `how-work-moves-through-opi.md` the canonical description; have other pages link to it rather than re-narrating the five steps.

### 4.3 Team/service/program/product taxonomy defined repeatedly (LOW)
- **Files:** `what-we-do/index.md`, `what-we-do/services/index.md`, `what-we-do/products/index.md`, `what-we-do/programs/index.md`, `our-teams/index.md` each re-define the same four terms ("a service is what OPI delivers… distinct from a team (staff and budget)…"). The glossary also defines all four.
- **Fix:** Define once (glossary or one hub page); have section indexes link to it with a one-line gloss.

### 4.4 Full 20-stat portfolio embedded in the strategic framework (MED)
- **File:** `what-we-do/programs/citistat/strategic-framework.md` lines ~280–439 (`## Current CitiStat portfolio`).
- **Issue:** Reproduces the entire portfolio as HTML cards (name, type, cluster, focus) — the same content the `portfolio/` index and the 19 portfolio stat pages already own. Two sources of truth for the roster.
- **Fix:** Replace the embedded card grid with a link to the portfolio index; keep the roster in one place.

---

## 5. Orphan / asymmetric pages

### 5.1 Standalone deep-dive page exists for only one service (HIGH — still open)
- **File:** `what-we-do/services/cross-agency-delivery-service-definition.md` (renamed during audit from `cross-agency-delivery-theory-of-change.md`)
- **Issue:** Cross-Agency Delivery is the only one of the five **services** with its own standalone deep-dive ("Service Definition") page in `what-we-do/services/`. The other four services have no parallel page (their teams have team-level strategy/ToC pages under `our-teams/`, but that is a different page type and location). The asymmetry remains after the rename.
- **Fix:** Either give the other four services a parallel deep-dive page, or fold this content into the team-level pages so the services section is symmetric.

### 5.2 ToC "series" numbering — RESOLVED DURING AUDIT (was MED)
- **File:** `cross-agency-delivery-service-definition.md`
- **Status:** The page header was `category="SERVICE THEORY OF CHANGE · 04 OF 05"` (implied a nonexistent 5-part series); it is now `category="OPI · SERVICE DEFINITION"`. No action needed.

### 5.3 Placeholder product pages shipped as live product entries (MED)
- **Files:** `what-we-do/products/baltimore-city-data-platform.md`, `what-we-do/products/baltimore-city-performance-portal.md`
- **Issue:** Both carry a "Placeholder page" admonition and the products index lists their **Status = "Placeholder"** — i.e., two of three products are stubs. They sit as siblings to the fully built BIC, creating an uneven section.
- **Fix:** Either flesh them out or mark them clearly as "planned/coming" (Status "Planned" reads better than "Placeholder") and de-emphasize until ready.

---

## 6. Label / column inconsistencies

### 6.1 Performance Standards page titles use two different conventions (LOW)
- **Files:** `how-we-work/operations/performance-standards-manager-companion.md` titled "Performance Standards — Manager Companion" (em-dash) vs `performance-standards-staff.md` titled "Performance Standards (Staff)" (parenthetical).
- **Fix:** Pick one form, e.g., "Performance Standards — Staff" / "Performance Standards — Manager Companion".

### 6.2 How-to filename / title mismatch (LOW)
- **File:** `how-we-work/how-to/book-the-idea-lab-fayette.md` — title is "Reserving the Idea Lab" (filename says "book … fayette", and "@ Fayette" is dropped from the title).
- **Fix:** Align title and filename (e.g., title "Reserve the Idea Lab @ Fayette").

### 6.3 Email casing inconsistency in staff directory (LOW)
- **File:** `how-we-work/team-and-roles/staff-directory.md`
- **Issue:** `XanderJake.DeLosSantos@baltimorecity.gov` is mixed-case while every other email is all-lowercase.
- **Fix:** Lowercase the address for consistency (and to match `team-and-roles/index.md`, which renders it differently).

### 6.4 Executive Director title omits "Chief Performance Officer" (LOW)
- **Files:** `staff-directory.md`, `team-and-roles/index.md`, telework memo — ED rendered as "Executive Director and Chief Data Officer". The glossary states the ED "also serves as the city's Chief Data Officer **and Chief Performance Officer**."
- **Fix:** Decide the canonical title and apply it consistently (the title currently drops the CPO half).

### 6.5 "AdminOps" vs "admin-ops" vs "OPI Administration & Operations" (LOW)
- **Files:** 103 uses of "AdminOps" vs an "Also called OPI Administration & Operations" gloss only on `services/admin-ops.md`. Naming is mostly consistent; flagging the lone alternate label for awareness.
- **Fix:** Fine as-is, but ensure the "Also called" gloss is the single canonical alias.

---

## 7. Stale / placeholder content

### 7.1 Same-person name rendered as "Rock Young" vs "Rakeim Young" (HIGH)
- **Files:** `how-we-work/administrative-memos/telework-and-in-office-schedule.md` (line 10, From line) and `how-we-work/administrative-memos/responding-to-city-council-requests.md` (line 68, body). Everywhere else (staff directory, roster, other memos) the Chief of Staff is "Rakeim Young".
- **Fix:** Replace both "Rock Young" with "Rakeim Young".

### 7.2 Administrative-memo date formats inconsistent (MED)
- **Files:** `responding-to-city-council-requests.md` "3/20/2026", `media-and-press-engagement.md` "3/20/2026", `essential-and-emergency-essential-designations.md` "March 5, 2026", `telework-and-in-office-schedule.md` "02/17/2026".
- **Fix:** Standardize on one date format across all memos (e.g., "March 20, 2026").

### 7.3 Administrative-memo "From"/header fields inconsistent (LOW)
- **Files:** `administrative-memos/*.md`. The ED's From line varies ("Dartanion Swift-Williams, Executive Director" vs "…, Executive Director and Chief Data Officer"). Memo title casing also varies ("Protocol For Responding To City Council Requests" capitalizes For/To; others use normal sentence case).
- **Fix:** Standardize the memo header block (To/From/Cc/Date) and title casing across all four memos.

### 7.4 Placeholder admonitions on two product pages (MED — see 5.3)
- **Files:** `products/baltimore-city-data-platform.md`, `products/baltimore-city-performance-portal.md` — both explicitly "This page is a placeholder… full page content is still being written."
- **Fix:** Complete or reframe as "Planned" (cross-referenced under 5.3).

### 7.5 BIC open `TBD` items (LOW — intentional but worth tracking)
- **Files:** `baltimore-intelligence-center/roadmap-and-source-systems.md` (interface "TBD" rows), `governance-and-risks.md` (staffing "TBD"), `engagement-overview.md` (Sand TPM "TBD"). These are deliberately tracked as "Open issues to resolve at kickoff," so they are legitimate — flagged only so they aren't mistaken for forgotten placeholders and are closed on schedule.
- **Fix:** No change needed; ensure they're cleared at kickoff per the governance page.

---

## Summary by severity

- **HIGH (open):** 1.3 (ToC skeletons differ), 5.1 (orphan service deep-dive page), 7.1 ("Rock Young" name error).
- **MED (open):** 1.5, 1.6, 1.7, 1.9, 1.10, 2.1, 3.1, 4.1, 4.4, 5.3, 7.2, 7.4.
- **LOW (open):** 1.4, 1.8, 2.2, 2.3, 3.2, 3.3, 3.4, 4.2, 4.3, 6.1, 6.2, 6.3, 6.4, 6.5, 7.3, 7.5.
- **Resolved during the audit:** 1.1, 1.2, 5.2 (Cross-Agency Delivery page rewritten to template + recategorized while this review was in progress).
