# Round-2 Review Synthesis (post-reorg)

Six agents, same forced-output rubric as round 1: 4 personas (staff, partner,
funder, storyteller) + Consistency/Parity + Editor/Streamlining. Source reviews:
`review2_*.md`.

## Verdict: 6 of 6 "agree-with-changes"

Unanimous. The reorg landed the **structure** (six clean sections, a real
teams/services/programs/products taxonomy, a canonical loop page). What's left is
a **content pass** — the pages weren't cut and normalized to match the new spine.

## Round-1 → Round-2 delta (what the reorg fixed)

- ✅ **CitiStat reads as a program** — "the biggest reorg win" (staff).
- ✅ **Services no longer buried** — front-and-center under What We Do (funder: "resolved").
- ✅ **One-sentence story exists** and the loop is a strong front-door metaphor (storyteller).
- ✅ **Partner front door works** — an outsider self-serves in ~5 min (partner).
- ✅ **Innovation Lab dual-nature callout removal validated** — "not missed" (partner).
- ✅ **"CAD" ban holds** — every literal CAD is legitimate (all reviewers).
- ✅ **Glossary acronym table** is a real upgrade (storyteller).
- ✅ **Roster merge works** (staff); **PDs have excellent parity, no role-name drift** (consistency).
- ✅ **Taxonomy is now stateable by an outsider** (partner).

## Deduped P0 backlog (ranked by reviewer consensus)

### P0-1 — Make How Work Moves the ONE loop page; retire/fold the two omnibus pages
Flagged by storyteller, editor, consistency (staff/partner adjacent). The loop is
hand-typed in 6+ files with a mutating tail ("sustains" / "documented and sustained"
/ "documented and accountable"; Data's verb "explains" / "helps explain"). Three
pages compete to be the operating model.
- **Retire `operating-frame.md`** — move its only unique bit (the "About vs Theory
  of Change" explainer) to `our-teams/index.md`.
- **Merge-then-retire `teams-programs-foundations.md`** — move its unique
  "Function Boundaries and Handoffs" table into `how-work-moves-through-opi.md`.
- Replace every other full loop restatement with a one-line teaser + link.
- ⚠️ Reverses the earlier "keep + group" decision for these two pages — needs sign-off.

### P0-2 — Settle the naming layer (one term per concept)
Flagged by staff, storyteller, partner, editor, consistency.
- The model: pick ONE of operating model / operating frame / improvement cycle /
  signal-to-solution loop. ("Operating Frame" as a page title competes with "How
  Work Moves.")
- "portfolio" vs "team" — use **team** publicly.
- Performance (team) / Citywide Performance Management (service) / CitiStat
  (program), and the Innovation Lab team-vs-service name collision — add scope
  cues so the labels are distinguishable.

### P0-3 — Enforce ONE Theory-of-Change skeleton
Flagged by consistency (S1), staff, editor. IL + AdminOps carry SERVICE DEFINITION
+ PURPOSE blocks Performance + Data lack; section-2 and section-5 headings are named
2–3 ways; CAD's ToC is a different format in another folder; the Performance team
ToC is titled "Performance Management" and badged as a *service* ToC "OF 05" (only 4
exist; CAD's "04" missing).
- Lock the NORTH STAR → logic-model skeleton, strip PURPOSE/SERVICE-DEFINITION,
  normalize section names (find/replace), fix the "OF 05" counts.

## P1 — High-severity content fixes

- **P1-1 CitiStat two sources of truth** (editor blocker): `strategic-framework.md`
  embeds the full 19-Stat portfolio as cards, duplicating `portfolio/`. Cut to a link.
- **P1-2 Two CAD pages in Services** (editor, consistency): `cross-agency-delivery.md`
  + `cross-agency-delivery-service-definition.md`. Host the deep version once
  (it's CAD's ToC equivalent), link from the service page.
- **P1-3 Collapse "Priority outcomes" + "What this means for people"** on all 5
  service pages — they restate the same four outcomes twice (editor, consistency).
  ⚠️ Deviates from the budget-office template — needs sign-off.
- **P1-4 Team index pages not parallel** (consistency S1): 8 lines (Data) → 32
  lines (Performance) with different section sets. Normalize to a shared skeleton.
- **P1-5 Budget dollars on the Service Crosswalk** (funder): mandate→goal→outcomes
  lands, but no $/FTE. Add a cost-center/FTE column. ⚠️ Needs per-service budget
  data not in hand (deck had only top-line $2.03M FY26).

## P2 — Front-door + polish

- **How to Engage OPI** needs a stronger homepage anchor and a "a CitiStat request
  landed on my desk → what to expect" framing, not just "request a service"
  (partner, editor).
- **De-dup the front door**: Home carries the loop + full taxonomy table (verbatim
  on `what-we-do/index.md`); `what-we-do/index` and `services/index` teach the same
  service-vs-team lesson; `org-structure` explains the distinction 3×. One teacher
  per lesson (editor).
- **Insider terms** on the CAD page (coordination overlay, commitment ledger, SRO)
  before they're defined; pin the approved "x-agency delivery" short form in the
  glossary (partner).
- **Label nits**: lying "OF 05" counts, `AUDIENCE: PUBLIC` only on Performance,
  casing, `pd-product-engineer-full-stack` filename vs "Full Stack Engineer"
  (consistency S2/S3).

## Decisions needed before executing
1. **Retire/fold the two omnibus pages?** (reverses "keep + group") — reviewers unanimous to fold.
2. **Cut "Priority outcomes" from the 5 service pages?** (deviates from budget template).
3. **Per-service budget figures** for the crosswalk — do they exist to add?
