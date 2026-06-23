# Persona Review — CitiStat Analyst

Reviewer persona: existing CitiStat analyst, occasional Innovation Lab Tiger Team member. Lens: onboarding new hires, prepping Stat meetings, finding operating references fast.

## Scenario findings

1. **What is CitiStat / program vs team.** `programs/citistat/index.md` opens with "CitiStat is a **program**, not a team" and sits under **Programs** in the nav, not **Our Teams**. The Performance team index reinforces it ("**CitiStat is a program**... the Performance team is its operational home"). Glossary entry cites Baltimore City Code Art. 1, Subtitle 61. This reads correctly and consistently. No confusion.

2. **My team's canonical Theory of Change in 1–2 clicks.** The playbook "See also" links **Performance Management Theory of Change** directly (`our-teams/performance/performance-theory-of-change.md`), and `theory-of-change-summaries.md` lists it as service #1 with the same single-source-of-truth target. Good: CitiStat does NOT fabricate its own ToC — it inherits Performance's. One click from the playbook. Clean.

3. **Loop page owner + last reviewed.** The canonical loop is `how-we-work/how-work-moves-through-opi.md`. Owner/review data is NOT on the page — it lives only in `how-we-work/.metadata.yml`: owner **Chief of Staff**, last_reviewed **2026-04-15**, next_review **2026-07-15**. As a daily user I can't see this without going into the repo. The page itself gives me no governance footer. That's a gap.

4. **Prep a pre-memo from the Method Playbook ALONE.** Largely works. The playbook carries the 12-step analyst cycle (pre-memo at T-2, step 8), the no-ambushes/data-with-context principles, the cabinet attendance rules, data standards, and the four-color follow-up convention. It correctly hands the actual pre-memo *template* to `templates.md` and the QA bar to `quality-standards.md` — both linked in "See also." I was NOT forced back into the Strategic Framework to prep; the only Framework reference is the optional crosswalk for mapping 12 steps to 7 phases, which I'd never need mid-prep. This is the strongest part of the site for my job.

5. **Performance / CPM / CitiStat language.** Mostly disciplined, one nit. The service page (`citywide-performance-management.md`) keeps service vs program clean. The one spot that blurs is the loop table row 1: **"Citywide Performance Management / CitiStat"** with a slash. The slash treats the service and the program as interchangeable in the exact place the site is teaching the distinction. Everywhere else they're carefully separated; here they're mashed.

## FORCED OUTPUTS

1. **Reaction:** agree-with-changes — usable today for Stat prep; a few governance/visibility gaps to close first.

2. **Top 3 blockers:**
   - No on-page governance footer (owner/last-reviewed) on the canonical loop page — invisible unless you open `.metadata.yml`.
   - Loop table row 1 "Citywide Performance Management / CitiStat" slash collapses service and program in the teaching artifact.
   - Loop page (last_reviewed 2026-04-15) is the oldest-reviewed canonical page and its next_review (2026-07-15) is < 1 month out — stale-risk on the most-linked page.

3. **Top 3 low-risk/high-impact fixes:**
   - Add a visible "Owner / Last reviewed" footer macro to the loop page (and other canonical pages).
   - Replace the slash in loop row 1 with "Citywide Performance Management (via CitiStat)".
   - Add a one-line "To prep a pre-memo, start here" callout at the top of the Method Playbook linking templates.md#pre-memo.

4. **Naming issue:** "Citywide Performance Management / CitiStat" slash — service vs program should never be slashed together.

5. **Drift risk:** the Performance ToC is the single source for CitiStat's logic. If Performance edits it without telling the CitiStat program owner, the playbook's "See also" silently misrepresents the program. Needs a cross-owner review trigger.

6. **Audience need missed:** a one-page **agency Data-Driven Officer** quick-start. DDOs are named all over the playbook but there's no landing page aimed at them; I onboard them verbally every time.

7. **Should be canonical (but isn't treated as such):** `programs/citistat/method-playbook.md` is the operational source of truth for running a Stat, yet it carries no governance footer and defers its review cadence to the directory default. Treat it as a named canonical page with its own visible owner/review stamp.
