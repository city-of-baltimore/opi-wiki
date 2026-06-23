# Persona Review Synthesis — OPI Wiki (`ddw/content-reorg`)

Four reviews: **S**taff (CitiStat analyst), **P**artner (peer agency deputy director), **F**under (Council/funder), **B**rand (storyteller). All four returned the **same headline verdict: agree-with-changes** — the *content* is production-ready; *wayfinding and the front door* are not.

## Cross-persona findings (P0 = raised by 2+ personas, or critical single-persona)

| # | Finding | S | P | F | B | Severity | Fix |
|---|---------|---|---|---|---|----------|-----|
| 1 | **The loop is told in 3–5 different wordings** (home, how-we-work/index, how-work-moves, teams-programs-foundations) and will diverge | · | ✅ | · | ✅ | **P0** | Make `how-work-moves-through-opi` the one canonical loop; home/index/services **excerpt-and-link**, don't re-tell |
| 2 | **`how-work-moves-through-opi` should be canonical but is duplicated, not deferred to** | · | ✅ | · | ✅ | **P0** | Same as #1 — quote it verbatim elsewhere |
| 3 | **External readers have no front door / intake path** — CAD and CitiStat (the pages outsiders land on) never say "how do I request this" | · | ✅ | ✅ | · | **P0** | Add "How to request this service" + opi@baltimorecity.gov + who can initiate, to CAD and a partner lane on CitiStat |
| 4 | **No home for the partner/agency reader** (incl. agency Data-Driven Officer quick-start) | ✅ | ✅ | · | · | **P0** | Add an agency-partner / DDO quick-start landing page |
| 5 | **Services missing from top-level nav** — buried under "How We Work" while Teams gets a tab | · | · | ✅ | · | **P0 (sev.)** | Promote `services/` to a top-level tab |
| 6 | **Innovation Lab dual (team + service + product) ambiguity** muddies the taxonomy | · | ✅ | ✅ | · | **P0** | Tighten the "both team and service" explainer at first encounter |
| 7 | **No 30-sec public "what is OPI / why care"** — hero is internally framed; home cards don't reach Services/Products | · | · | ✅ | ✅ | **P0** | Add public-value framing + home cards to Services, Products, outcomes |
| 8 | **No visible governance footer** (owner / last-reviewed) on canonical pages — only in `.metadata.yml` | ✅ | · | · | · | P1 | Render owner/last-reviewed footer from metadata on canonical pages |
| 9 | **Per-service Theory-of-Change parity drift** — 5 TOCs, no enforced template / cross-owner trigger | ✅ | · | ✅ | · | P1 | Shared ToC template + cross-owner review trigger (esp. Performance ↔ CitiStat) |
| 10 | **"Loop" named but drawn as a linear 1→5** — word and picture disagree | · | · | · | ✅ | P1 | Close it back to step 1, or rename "signal-to-solution path" |
| 11 | Naming: "Citywide Performance Management / CitiStat" **slash** collapses service+program (loop table row 1) | ✅ | · | · | · | P2 (quick) | "Citywide Performance Management (via CitiStat)" |
| 12 | `teams-programs-foundations.md` prints the loop blockquote **twice** in 8 lines | · | · | · | ✅ | P2 (quick) | Delete the duplicate |
| 13 | **SRO** appears as a bare acronym (how-work-moves line ~98) | · | · | · | ✅ | P2 (quick) | Spell out on first use |
| 14 | Insider terms "overlay" / "cost center" on the CAD page | · | ✅ | · | · | P2 | Plain-language ("temporary coordination effort, not a permanent office") |
| 15 | No single **budget-to-outcome crosswalk** artifact | · | · | ✅ | · | P2 | Add one scannable crosswalk page |

## Verdicts on the pre-flagged open questions

- **Cross-Agency Delivery clarity (Partner's call): PARTLY.** Excellent cross-cutting *description* ("permitting cuts across DHCD, DOT, Public Works"), but it fails the outsider test — authority is *named* (Authorizer = Deputy Mayor/CA) without being *actionable* (how a deputy director actually triggers convening). → Finding #3.
- **`products/` top-level placement (Funder's call): KEEP IT TOP-LEVEL.** Products are OPI's resident-facing accountability surface; demoting them reduces public visibility. The real gap is the **missing Services tab**, not the presence of Products. → Finding #5.
- **"Our Work" grouping (Funder + Brand both asked): DO NOT ADOPT.** Funder: it pushes Products down and still leaves Services missing up top — the opposite of what oversight needs. Brand: it hides the loop and blurs the home taxonomy table. Both recommend instead **promoting Services to top-level** and keeping the deliverables discoverable.

## Recommended edit backlog (P0 first)
1. Consolidate the loop to one canonical telling; excerpt-and-link everywhere else (#1, #2).
2. Add external front doors: intake/"request this" on CAD + CitiStat, and an agency-partner/DDO landing page (#3, #4).
3. Promote `services/` to top-level nav; keep `products/` top-level; do **not** add an "Our Work" wrapper (#5).
4. Sharpen the Innovation Lab dual-nature explainer (#6) and add a public-value home path (#7).
5. Quick wins, batchable: dedupe the foundations blockquote, fix the CPM/CitiStat slash, spell out SRO (#11–#13).
