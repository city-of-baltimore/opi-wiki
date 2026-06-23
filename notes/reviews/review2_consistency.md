# Review 2 — Consistency & Parity (post-reorg)

Reviewer pass over the OPI wiki (`/Users/dartanion/opi-wiki/docs`), comparing sibling pages
directly for parallel structure, uniform labels, and non-redundancy. Lens: what the Director
cares about — clear, crisp, consistent.

Severity key: **S1** blocker (breaks the parity promise / will read as sloppy to leadership) ·
**S2** should-fix (visible inconsistency) · **S3** polish.

---

## 1. The 5 service pages — MOSTLY GOOD, two outliers

The five `docs/what-we-do/services/*.md` pages share the intended skeleton: summary header →
What this service does → The goal → Mandate → Priority outcomes → What this means for people →
Delivered by → Read alongside. Performance, Data, Innovation Lab, AdminOps are clean and parallel.
Two deviations:

| File | Issue | Sev | Fix |
|---|---|---|---|
| `services/admin-ops.md` | Only service page with an **"Also called"** line (L5: "OPI Administration & Operations"). No sibling has an alias line. | S3 | Either give every service its formal-name line or drop this one for parity. |
| `services/cross-agency-delivery.md` | Carries an **extra "How to request this service"** section (L41-43) that the other four lack; and an extra preamble sentence about naming (L5). Its "Delivered by" is a paragraph, not the one-line pattern the others use. | S2 | Accept the asymmetry as intentional (overlay service) but add a parallel "How to request" or "How to engage" line to the other four, OR move CAD's request path into "Read alongside" so the body skeleton matches. |
| `services/cross-agency-delivery-service-definition.md` | A **6th file in the services folder** that is not one of "the 5." It is CAD's theory-of-change/method, parked under services. Breaks the "5 standardized pages + crosswalk" mental model of the folder. | S2 | Fine to keep, but it should be visibly labeled as the CAD appendix (it is, via category "SERVICE DEFINITION") — confirm nav groups it under CAD, not as a peer service. |

**Redundancy inside the service set:** the "Priority outcomes" bullets and the "What this means
for people" bullets are the *same four outcomes twice*, once as system statements and once as
first-person voice (verified on all 5 pages — e.g. `citywide-performance-management.md` L21-31).
This is deliberate (audience framing) but it is the single biggest "say-it-twice" pattern on the
service pages. **S2** — keep if intentional, but the Director should sign off that every service
restates its outcomes in two registers.

---

## 2. The 4 team pages — INDEX PAGES ARE NOT PARALLEL (S1)

All four teams have the intended trio (`about-*`, `*-strategy`, `*-theory-of-change`). But:

| File | Issue | Sev | Fix |
|---|---|---|---|
| `our-teams/data-and-analytics/index.md` | **8 lines, 2 sections** (just a card grid + PD pointer). | S1 | Bring to parity with Performance/Innovation: add the 2-3 paragraph "what this team owns / works closely with" intro. |
| `our-teams/directors-office/index.md` | Has a "What this team does" prose block + card grid. | — | Reasonable baseline. |
| `our-teams/performance/index.md` | **6 prose sections** (CitiStat program, Works closely with, PD, A note on language…). Much heavier than the others. | S2 | Trim or push parity up — pick a target index template (intro + card grid + PD pointer + 1 "works closely with") and apply to all four. |
| `our-teams/innovation-lab/index.md` | Intro + card grid + PD pointer, names current incumbents inline. | — | Closest to a good template. |
| Extra sub-pages | Data has `data-governance-framework.md`; Innovation has `digital-product-methodology.md`. Performance and Director's Office have **no equivalent "method/framework" page**. | S3 | Acceptable (teams differ), but note Performance's method lives in the CitiStat program section and Director's has none — call this out so it doesn't read as a gap. |

**The four index pages range from 8 lines to ~32 lines with wholly different section sets.** This
is the most visible non-parallelism in "Our Teams" and the first thing a reader clicking team to
team will notice.

---

## 3. The 5 theory-of-change pages — SKELETON DRIFT, worse than the known issue (S1)

The known issue is real and confirmed, plus more:

| File | Sections 1-8 present? | Extra/missing | Sev |
|---|---|---|---|
| `performance/performance-theory-of-change.md` | Yes (NORTH STAR + 1-8) | clean | baseline |
| `data-and-analytics/data-analytics-theory-of-change.md` | Yes (NORTH STAR + 1-8) | clean | baseline |
| `innovation-lab/innovation-lab-theory-of-change.md` | Yes | **+ SERVICE DEFINITION + PURPOSE AND PHILOSOPHIES** (incl. "How we partner" sub-block) before §1 | S1 |
| `directors-office/admin-ops-theory-of-change.md` | Yes | **+ SERVICE DEFINITION + PURPOSE AND PHILOSOPHIES + an extra "Operating principles for the team"** sub-block | S1 |
| `services/cross-agency-delivery-service-definition.md` | Yes (§4 = ToC) | **structurally different** — it is a full SERVICE DEFINITION doc with the ToC embedded as section 4; lives in a different folder; carries its own NORTH STAR/PURPOSE blocks | S1 |

Two compounding label inconsistencies in the same set:
- **Section 2 is named two ways:** "**Operating scope (boundary lines)**" (Performance, Data) vs
  "**Scope and service boundaries**" (Innovation, AdminOps). Pick one.
- **Section 5 is named three ways:** "Governance, decision rights, and operating cadence"
  (Performance), "Governance and decision rights" (Data, Innovation, AdminOps, CAD).

**Fix (S1):** Define one ToC skeleton. Either (a) strip SERVICE DEFINITION / PURPOSE from
Innovation + AdminOps so all five match Performance/Data, or (b) add those sections to
Performance/Data. Recommended: (a) — the About pages already carry PURPOSE; the ToC should be the
operational backbone only (the `operating-frame.md` L49-55 explicitly says "About answers spirit;
Theory of Change answers how it's staffed/governed/measured"). The extra PURPOSE blocks on two ToC
pages directly violate the office's own stated division of labor.

---

## 4. Position descriptions — EXCELLENT PARITY (S3 only)

All 19 PDs share an identical skeleton: At a Glance → Position Summary → Key Responsibilities →
Knowledge, Skills, and Abilities → Minimum Qualifications → Working Conditions → Supervision.
At-a-Glance rows are uniform across all 19 (Working title / Classification / Portfolio / Reports to
/ Supervision given / Supervision received). This is the strongest section of the wiki.

Minor:

| File | Issue | Sev | Fix |
|---|---|---|---|
| `position-descriptions/innovation-lab/pd-product-engineer-full-stack.md` | **Filename says `product-engineer-full-stack`; working title is "Full Stack Engineer."** Filename/title drift (redirects cover it, but the file is the odd one out). | S3 | Rename to `pd-full-stack-engineer.md` and update the redirect map, or accept and document. |
| PD index `position-descriptions/index.md` | Lists "Full Stack Engineer" — matches roster and PD title (good). Two "Applied Data Scientist" PDs exist (Data + Innovation portfolios) — correct per roster (Vera Choo / Chiemeka Okeoma) but worth a one-line note so readers don't think it's a dup. | S3 | Add parenthetical portfolio after duplicate titles in the index. |

**No title/role-name drift vs roster.** Cross-checked `team-and-roles/index.md` roster against the
19 PDs and the PD index: working titles, classifications, and reporting lines all reconcile
(Executive Director and CDO, Chief of Staff, two Deputy Chiefs, Innovation Program Manager,
Civic Designer, Full Stack Engineer, Senior Performance Analyst = the one open PIN 115657, etc.).
This was clearly reconciled in the recent commits.

---

## 5. Products — CONSISTENT (S3)

`products/index.md` correctly lists BIC (Active), Data Platform (Placeholder), Performance Portal
(Placeholder). The two placeholders are **structurally identical**: same `!!! note "Placeholder
page"` admonition → "What it is" → "Read alongside." BIC is the only multi-page product. No parity
problem. Only nit: `index.md` status column uses "Active / Placeholder," while the BIC sub-pages
have their own internal structure — fine, BIC is intentionally the built-out one.

---

## 6. Redundancy — THE LOOP IS RESTATED IN ~4 CANONICAL PLACES (S1)

The "signal-to-solution loop" sentence — *"CitiStat identifies the problem. Data helps explain it.
The Innovation Lab designs and tests the solution. Cross-Agency Delivery coordinates implementation…
AdminOps keeps the work visible…"* — or a near-verbatim variant appears in:

1. `how-we-work/index.md` (L5-13, numbered list form)
2. `how-we-work/how-work-moves-through-opi.md` (L9 blockquote **and** L13-21 loop table)
3. `how-we-work/operating-frame.md` (L41-47 "How the cycle moves" table)
4. `how-we-work/teams-programs-foundations.md` (L13 blockquote **and again** L225-227)

That is four pages (five+ instances) carrying the same model. **S1 for the Director's "no
redundancy" bar.** `how-work-moves-through-opi.md` is the obvious canonical home (it has the
fullest treatment: loop table, ownership, Tiger Teams, decision rules, handoffs). The other three
should link to it and keep at most a one-line teaser, not a full restatement.

Three overlapping "operating model" pages compound this:
- `operating-frame.md` ("How OPI is structured… five services as one cycle")
- `teams-programs-foundations.md` ("four portfolios in operating detail… signal-to-solution loop")
- `how-work-moves-through-opi.md` ("how OPI moves from signal to sustained improvement")

All three explain teams/services/the loop with heavy overlap. **S2** — they have *nominally*
distinct jobs (frame = services-as-cycle; TPF = portfolio ownership detail; how-work-moves =
routing/decision rules) but a reader cannot tell from the titles which to read, and all three
re-teach the loop. Recommend an explicit "Read X for the loop, Y for portfolio ownership, Z for
routing" disambiguation block, and demote two of the three loop restatements to links.

The five-service one-liners are also restated in `operating-frame.md` (L19-37), `services/index.md`
(L7-13 table), and `service-crosswalk.md` (L7-13 table). The crosswalk and services-index tables
serve different cuts (mandate-to-outcomes vs delivered-by) so that pair is defensible; the
operating-frame prose version is the third copy. **S3.**

---

## 7. Naming / labels — NUMBERING SERIES IS INCONSISTENT (S2)

The `page_header` `category=` field is used as a series label, and the numbering is uneven:

- **About series:** `ABOUT · SERVICE 01 OF 05` (Performance), `02 OF 05` (Data), `03 OF 05`
  (Innovation), **`05 OF 05`** (AdminOps) — **"04 OF 05" (Cross-Agency Delivery) is missing** from
  the About series because CAD has no About page. The series claims "OF 05" but only 4 exist.
- **Strategy series:** only Performance carries the numbered+audience label
  (`STRATEGY · SERVICE 01 OF 05 · AUDIENCE: PUBLIC`); Data, Innovation, AdminOps just say
  `STRATEGY`. So one of four is numbered, three are not.
- **`AUDIENCE: PUBLIC` only on Performance's About and Strategy** — no sibling carries it. Reads
  like a leftover from an earlier public-brief.
- **Theory-of-change series:** numbered `01/02/03/05 OF 05` (again no 04 in this folder — CAD's is
  the differently-labeled `OPI · SERVICE DEFINITION`).
- Section-5 / section-2 ToC heading drift (see §3).
- `category` casing is otherwise inconsistent across the site: `OPI · SERVICE`, `STRATEGY`,
  `ABOUT OPI`, `TEAMS, PROGRAMS & FOUNDATIONS`, `SERIES · OPI FOUNDATIONS` — no single convention,
  though this is lower-stakes.

**Fix (S2):** Pick one rule for the numbered series. Either number all four team docs `01-04 OF 04`
(treating CAD's service-definition as the 5th, separately), or drop the `OF 05` counts entirely and
just label `ABOUT · SERVICE` / `STRATEGY` / `SERVICE THEORY OF CHANGE`. Remove the stray
`AUDIENCE: PUBLIC` from Performance's two pages unless every sibling gets it.

**Filenames vs titles:** mostly clean. `pd-product-engineer-full-stack.md` is the one drift (§4).
`about-data-analytics.md` titled "# About Data Analytics" while the *service* is "Citywide Data and
Analytics" and the *team* is "Data and Analytics" — three near-but-not-identical names for one
thing. **S3.**

---

# FORCED OUTPUTS

**1. One-line reaction:** **Agree-with-changes** — the spine is sound and PDs/services/products are
in good shape, but the team index pages, the theory-of-change skeleton drift, and the four-way loop
duplication are real parity defects that a "clear, crisp, consistent" Director will see immediately.

**2. Top 3 blockers (S1):**
   1. Theory-of-change skeleton drift — Innovation Lab + AdminOps carry SERVICE DEFINITION +
      PURPOSE blocks (and AdminOps an extra "Operating principles") that Performance + Data don't,
      and CAD's lives in a different folder/format. Plus section-2 and section-5 are named 2-3 ways.
   2. The signal-to-solution loop is fully restated in 4+ canonical pages
      (how-we-work/index, how-work-moves, operating-frame, teams-programs-foundations ×2).
   3. The four team `index.md` pages range from 8 lines to ~32 with different section sets
      (Data and Analytics is a near-stub vs Performance's six sections).

**3. Top 3 low-risk high-impact fixes:**
   1. Normalize section-2 ("Operating scope (boundary lines)") and section-5 ("Governance and
      decision rights") headings across all five ToC pages — pure find/replace, instantly visible.
   2. Drop the `OF 05` counts (or fill the missing 04) and remove the stray `AUDIENCE: PUBLIC` from
      Performance's About/Strategy so the series labels stop lying about their own count.
   3. Replace three of the four loop restatements with a one-line teaser + link to
      `how-work-moves-through-opi.md`.

**4. One naming/nomenclature issue:** The numbered series labels claim "OF 05" but the About and
Theory-of-Change folders only hold 4 numbered docs (Cross-Agency Delivery is missing "04"), and
only Performance carries `AUDIENCE: PUBLIC`. The count and the audience tag are inconsistent with
the rest of the series.

**5. One drift risk:** The ToC skeleton has no enforced template, so as services edit their own
pages the section names ("Operating scope" vs "Scope and service boundaries," three variants of
"Governance…") and the optional PURPOSE blocks will keep diverging. Without a `theory-of-change`
template file or a lint check, parity will erode page-by-page at the next edit.

**6. One audience need the structure misses:** A **new agency partner / Authorizer** has no single
"start here, this is what OPI can do for you and how to ask for it" page. The request path exists
only inside `cross-agency-delivery.md` ("How to request") and `how-to-engage-opi.md`, while "the
loop" pages speak to internal staff. An external partner clicking in cannot tell where to begin.

**7. One page that should be canonical (and isn't):** **`how-work-moves-through-opi.md`** is the
fullest, best treatment of the operating loop (loop table + ownership + Tiger Teams + decision
rules + handoffs) but it is not treated as the single source — `operating-frame.md` and
`teams-programs-foundations.md` re-teach the same model as peers rather than deferring to it. Make
`how-work-moves-through-opi.md` the canonical loop page and have the others link to it.
