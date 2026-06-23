# OPI Wiki Audit — About Us, Resources/Reference, Public

Scope: `docs/about-us/` (about-opi, letters-from-the-director), `docs/resources/`
(reference incl. position-descriptions, glossary, theory-of-change-summaries,
operating-model-staff-version, tiger-teams-playbook, strategic-priorities-one-pager,
wiki-knowledge-base-structure, contributing), and `docs/public/`.

Date: 2026-06-22. Findings grouped by issue class; severity high/med/low.

---

## 1. Undefined acronyms / jargon

| File | Acronym | Description | Sev | Fix |
|---|---|---|---|---|
| about-us/about-opi/operating-principles-and-culture.md:139 | **MAC** | Used bare in the Ownership Model table ("311, MAC"). Expanded once far earlier (line 95, "Mayor's Action Center") but never near use and absent from glossary. (Director-flagged example.) | high | Write "Mayor's Action Center (MAC)" on first use in the table, or add MAC to the glossary. |
| about-us/about-opi/operating-principles-and-culture.md:150,154 | **SBAR / STAR** | Frameworks expanded inline (good) but jargon-dense; not in glossary. | low | Optional: add to glossary. |
| about-us/about-opi/mission-vision-identity.md:62,186 | **DCAs** | "Deputy Mayors and DCAs" — never expanded; glossary tells you to expand "DM" but DCA is undefined everywhere. | med | Expand to "Deputy City Administrators (DCAs)" on first use; add to glossary. |
| resources/reference/operating-model-staff-version.md:108; position-descriptions/directors-office/pd-project-manager.md:32 | **RAG** | "RAG status" / "RAG definitions" undefined (Red/Amber/Green). | med | Expand on first use; add to glossary. |
| resources/reference/operating-model-staff-version.md:38 (and several PDs) | **HCD** | "HCD" used bare in the portfolio table; spelled out elsewhere as human-centered design. | low | Use "human-centered design (HCD)" on first use. |
| resources/reference/wiki-knowledge-base-structure.md:82,200,202 | **CDO / DCDO / DCPO** | "Deputy CDO", "DCDO", "DCPO" used bare in tables/role lists; expanded only inside individual PDs. | med | Expand on first use in this page or add to glossary. |
| position-descriptions/data-and-analytics/pd-senior-data-engineer.md, pd-principal-data-engineer.md | **ETL / ELT** | Used bare. | low | Acceptable for technical PD audience; optionally gloss once. |
| position-descriptions/directors-office/pd-chief-of-staff.md:20,64 | **OSHA / COOP** | "OSHA, COOP" used bare. | low | Expand COOP ("Continuity of Operations") on first use. |
| position-descriptions/directors-office/pd-citistat-inspector.md; pd-chief-of-staff.md | **AV** | "rooms/AV", "AV setup" bare. | low | Spell out "audiovisual (AV)" once. |
| position-descriptions/innovation-lab/pd-product-engineer-full-stack.md:40 | **WCAG** | Bare. | low | Acceptable; optionally gloss. |
| position-descriptions/data-and-analytics/pd-technical-program-manager.md:18 | **TPM / UAT** | TPM expanded; UAT ("user-acceptance testing") spelled out later — fine. | low | None needed. |
| resources/reference/strategic-priorities-one-pager.md; tiger-teams-playbook.md | **DHCD / DPW / DOT / BCRP** | Agency acronyms — expanded in tiger-teams-playbook table (good) but used bare in strategic-priorities-one-pager line 39 before any expansion. | low | Expand on first use in strategic-priorities or rely on the playbook table. |

Note: BCIT, BBMR, ORF, SRO, PMO, KPI, SOP are defined in the glossary — not flagged.

---

## 2. Redundancy / duplication

### Verdict on `public/` (the Director's hypothesis)

The `public/` section is **largely redundant** with canonical wiki content. Detail per page:

| public/ page | Duplicates | Unique content | Verdict |
|---|---|---|---|
| **citistat-public-brief.md** | The public-facing CitiStat explainer in `what-we-do/programs/citistat/*` and `about-us/.../on-performance-management.md`; the four tenets and 19-Stat list also live in the CitiStat method pages and the Stat portfolio (`what-we-do/programs/citistat/portfolio/`, 21 pages). | The compact public 19-Stat one-liner table and "where to see results" framing. | **Mostly redundant.** Merge any unique resident-facing framing into the canonical CitiStat program page; retire as a standalone. |
| **data-analytics-public-brief.md** | `what-we-do/services/citywide-data-and-analytics.md` and `our-teams/data-and-analytics/about-data-analytics.md`. | "How to engage" split by audience (agency / researcher / resident). | **Mostly redundant.** Move the audience-specific engagement copy into the canonical service page; retire. |
| **innovation-lab-public-brief.md** | `what-we-do/services/innovation-lab.md`, `our-teams/innovation-lab/innovation-lab-strategy.md`, and the "what we are not" list duplicated from `teams-programs-foundations.md`. | "Four moves" (Listen/Design/Test/Hand off) framing; funder/philanthropy engagement path. | **Mostly redundant.** Merge the four-moves + funder path into the canonical Lab page; retire. |
| **website-copy-master.md** | Re-states About OPI, every team, every program, every service — overlapping `mission-vision-identity.md`, `teams-programs-foundations.md`, `operating-frame.md`, the three briefs, and the canonical service/team pages. | It is a CMS copy-deck (publication-ready blocks + voice guardrails + site footer). | **Keep, but reposition.** This is a working artifact for the *external* opi.baltimorecity.gov build, not a wiki reference. Its content duplicates the wiki by design; keep it labeled as a web-publishing source, or move it out of the public reference section. |
| **website-information-architecture.md** | Pairs with website-copy-master; describes an external-site nav that is intentionally different from this wiki's nav. | Site map, URL/slug standards, template inventory, accessibility specs, open launch questions. | **Keep, but reposition** alongside website-copy-master as a pre-launch planning artifact (note it carries unresolved "open questions" — see §6). |

Recommendation: the three briefs are safe to **retire after merging** their small unique sections into the canonical service/program pages. The two website-* docs should **stay** but be clearly framed as external-site build artifacts (or relocated out of the public reference) so readers don't mistake them for the canonical public description.

### Other sitewide duplication (within scope)

| Files | Description | Sev | Fix |
|---|---|---|---|
| teams-programs-foundations.md:7 & 15 | The "Signal-to-solution loop" blockquote ("CitiStat identifies the problem...") is printed **twice on the same page**, verbatim, lines 7 and 15. | med | Delete one. |
| The signal-to-solution loop ("CitiStat surfaces what is not working / Data explains why / Innovation Lab redesigns...") appears in operating-frame.md, teams-programs-foundations.md (x3 forms), operating-model-staff-version.md:128-136, all three public briefs, website-copy-master.md, and the letters. | The same loop is paraphrased ~10 times sitewide with small wording drift. | low | Canonicalize one phrasing (glossary or operating-frame) and link to it. |
| tiger-teams-playbook.md:70-99 | The "When to use a Tiger Team" criteria + plain-language test are repeated **three times** (lines 21-37, 70-72, 76-99). See also §4 (broken headings). | high | Collapse to one canonical "When to use / When not to use" block. |

---

## 3. Inconsistent structure within a page type

| Files | Description | Sev | Fix |
|---|---|---|---|
| letters-from-the-director/on-innovation-and-civic-design.md | The only letter with an extra "## How this shows up in Tiger Teams" section — and it sits **after the signature block** (lines 75-83 signoff, then 85 new H2). | med | Move the section above the signoff, or drop it for parity with the other five letters. |
| letters-from-the-director/on-cross-agency-delivery.md:67 | The only letter where a section ("## Plain-language operating distinction") appears **after READ ALONGSIDE** (which is otherwise the last section in every letter). | med | Move above the signoff / READ ALONGSIDE for parity. |
| position-descriptions/data-and-analytics/pd-applied-data-scientist.md:11 | The **only** PD (of 20) with a "Compensation range" row in the At-a-Glance table. All 19 others omit it. | high | Add the row to all PDs or remove it from this one for consistency. |
| position-descriptions/directors-office/pd-chief-of-staff.md:13,20,48,116; pd-citistat-inspector.md:20 | Reference stale Director's-Office role names "Communications and Partnerships Lead" and "Special Assistant" — the index, redirects, and June-2026 roster renamed these to **Data Storyteller** and **Operations Analyst**. | high | Replace stale titles with Data Storyteller / Operations Analyst. |
| public briefs (citistat vs data-analytics vs innovation-lab) | Asymmetric trailers: innovation-lab brief has a "## Plain-language distinction" closing section; the other two do not. Contact-table label is "Director" in the CitiStat brief but "Lead" in the other two for the same role. | med | Standardize a trailer (or none) and a single label across the three briefs. |
| theory-of-change-summaries.md:39 ("## Read alongside") vs the six letters ("## READ ALONGSIDE") | Same cross-reference section rendered in two casings. | low | Pick one casing convention sitewide. |

PD bodies are otherwise consistent (At a Glance → Position Summary → Key Responsibilities → KSA → Minimum Qualifications → Working Conditions → Supervision). Letters are otherwise consistent (page_header summary → body H2s → signoff → READ ALONGSIDE).

---

## 4. Awkward or broken formatting

| File | Description | Sev | Fix |
|---|---|---|---|
| tiger-teams-playbook.md:74 | "## What makes a Tiger Team different" is an **empty heading** — immediately followed by another H2 with no body. Pollutes the ToC and looks broken; the bullet list that belongs to it (lines 91-99) is orphaned under the *next* heading. | high | Fill or remove the empty heading; reattach the orphaned bullets; dedupe the repeated "When to use" content (see §2). |
| tiger-teams-playbook.md:184 | "(≋ week 13)" uses an unusual triple-tilde glyph instead of "~" or "approximately". | low | Replace with "~week 13" or "approx. week 13". |
| website-copy-master.md (throughout) | Dozens of **identical repeated H3s** — "### Why this team exists", "### What we do", "### What it means for agencies/residents", "### When to use this service", "### What you can expect from OPI", "### How we work", "### What success looks like", "### Why it exists", "### How it works", "### Authority" — recur once per team/program/service, flooding the ToC with duplicate anchors. | med | Demote the per-block sub-labels to bold text, or scope them so the ToC isn't polluted. (This is a copy-deck, so partly inherent — see §2 reposition recommendation.) |
| operating-principles-and-culture.md, mission-vision-identity.md, glossary.md, etc. | Heavy use of wide fixed-width markdown tables (Ownership Model, 70/20/10, Customer Definition, Misperceptions). They render fine but are very wide on mobile. | low | Acceptable; consider responsive review for the widest tables. |

---

## 5. Orphan / asymmetric pages

| File | Description | Sev | Fix |
|---|---|---|---|
| position-descriptions: two "PD — Applied Data Scientist" pages (data-and-analytics/ and innovation-lab/) | Same working title in two portfolios. Legitimate (two real seats) but indistinguishable by title in nav and ToC ("PD — Applied Data Scientist" twice). | low | Disambiguate nav/title, e.g. "Applied Data Scientist (Data & Analytics)" vs "(Innovation Lab)". |
| public/index vs the three briefs | Only three of five OPI services have a public brief (CitiStat/Performance, Data & Analytics, Innovation Lab). No public brief for **Cross-Agency Delivery** or **AdminOps**. | low | Either add the two missing briefs for symmetry or (preferred, per §2) retire the brief format entirely. |
| position-descriptions/index.md:64 "Cross-Agency Delivery" | Section exists but intentionally has no PDs (overlay). Handled gracefully — not a defect, noted for completeness. | n/a | None. |

---

## 6. Stale or placeholder content

| File | Description | Sev | Fix |
|---|---|---|---|
| strategic-priorities-one-pager.md:55 | "stand up and stabilize 19 regularly occurring Stats by end of January 2026" and "sustain by June 2026" — both dates are now past/at-deadline (today is 2026-06-22) yet written as future commitments. | med | Refresh to FY27 framing or restate as completed. |
| strategic-priorities-one-pager.md:55 | Internal number mismatch: "19 regularly occurring Stats... 12 of the 17 are new or relaunched" — 17 vs 19 in the same sentence. | med | Reconcile the counts. |
| strategic-priorities-one-pager.md:57,85,89,104; theory-of-change-summaries.md:14 | "tiger teams" / "tiger team" lowercase vs the canonical "Tiger Team" (Title Case) used in the playbook and glossary. | low | Normalize casing to "Tiger Team". |
| position-descriptions/directors-office/pd-project-manager.md:34; innovation-lab/pd-innovation-program-manager.md:34 | Subheadings "### tiger team Coordination..." and "### tiger team and Cross-Agency Delivery" use lowercase "tiger team" inside Title-Case headings. | low | Capitalize to "Tiger Team". |
| website-information-architecture.md:239-249 | "Open questions to resolve before launch" (CMS choice, named publisher, launch date, language scope) — unresolved planning placeholders on a live reference site. | med | Acceptable in a planning doc, but reposition out of the public reference (see §2) so it doesn't read as canonical. |
| operating-model-staff-version.md:158 footer "Reviewed quarterly" vs front matter "v1.0 / UPDATED April 2026" | Claims a quarterly cadence but hasn't been touched since April (2 quarters). Same pattern across most reference pages (all "UPDATED April 2026", all "Reviewed quarterly"). | low | Run the quarterly review or soften the cadence claim. |

---

## 7. Label / column inconsistencies

| File | Description | Sev | Fix |
|---|---|---|---|
| public briefs Contact tables | citistat-public-brief uses **"Director"** as the row label; data-analytics and innovation-lab briefs use **"Lead"** for the equivalent role. | med | Standardize the label. |
| citistat-public-brief.md:85 | "CitiStat is one of **three** core OPI services" — then names five (CitiStat, Data & Analytics, Innovation Lab, Cross-Agency Delivery, AdminOps). | med | Fix to "five services" or rephrase to "three core delivery services plus two supporting." |
| website-information-architecture.md:35 vs 44-47 | Design principles say "The four sections are Teams, Programs, Services, and **About**", but the nav table lists Home, Teams, Programs, Services, **Reports** (About is in the utility bar). The "four sections" claim omits Reports and miscounts. | med | Reconcile the section list with the actual nav. |
| position-descriptions/index.md:29 (Conventions) | Lists a "Status" field as maintained, but no individual PD carries a Status row (Status lives only in the index's own table). | low | Clarify that Status is an index-only column, or add it to PDs. |
| strategic-priorities-one-pager.md:29,45 ("### Priority 1/3") vs :37 ("**Priority 2**") and :67,75,83 ("**Direction 1-3**") vs :91 ("### Direction 4") | Priorities and Directions mix real H3 headings with bold-text pseudo-headings, so only some appear in the ToC and the numbering looks broken. | high | Make all priorities/directions consistent H3 headings. |

---

## Highest-priority fixes (summary)

1. **tiger-teams-playbook.md** — empty heading + triple-duplicated "When to use" content (§2, §4).
2. **strategic-priorities-one-pager.md** — bold-vs-H3 priority/direction headings break the ToC; stale Jan/June 2026 dates; 17-vs-19 count (§6, §7).
3. **pd-applied-data-scientist (D&A)** — lone Compensation-range row; reconcile across all 20 PDs (§3).
4. **pd-chief-of-staff.md / pd-citistat-inspector.md** — stale "Communications and Partnerships Lead" / "Special Assistant" titles (§3).
5. **MAC** undefined in operating-principles-and-culture.md (§1).
6. **public/** — retire the three briefs after merging unique content into canonical pages; reposition the two website-* docs as external-build artifacts (§2).
7. Two **letters** with sections after the signoff (§3); **teams-programs-foundations** duplicated blockquote (§2).
