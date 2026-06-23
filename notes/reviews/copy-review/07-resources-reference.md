# Copy Review — Resources & Reference

Senior-editor copy review. Target voice: Bloomberg + Harvard Kennedy School — crisp, factual, active, concrete, plain, authoritative, human. Recommendations only; no files edited.

Pages reviewed (8):
- `docs/resources/contributing.md`
- `docs/resources/index.md`
- `docs/resources/reference/index.md`
- `docs/resources/reference/glossary.md`
- `docs/resources/reference/tiger-teams-playbook.md`
- `docs/resources/reference/service-crosswalk.md`
- `docs/resources/reference/theory-of-change-summaries.md`
- `docs/resources/reference/strategic-priorities-one-pager.md`
- `docs/resources/reference/operating-model-staff-version.md`
- `docs/resources/reference/wiki-knowledge-base-structure.md`

(`position-descriptions/` excluded per scope — owned by another reviewer.)

Tags: **[safe]** = wording fix, meaning preserved. **[judgment]** = changes meaning/tone/structure; owner decides.

---

## 1. `docs/resources/contributing.md`

**Assessment.** Strong page. Tight, concrete, active, and the "thoughtful friend who doesn't work in city government" line lands well — it shows the voice rather than asserting it. The closing checklist is the only drag: it's a wall of yes/no questions that reads more like an internal QA form than guidance, and a couple of items are phrased awkwardly.

**Line-level recommendations**

- "When in doubt, write the way you'd explain something to a thoughtful friend who doesn't work in city government." → keep as-is. **[safe]** (No change — flagged as a model sentence for the rest of the wiki.)

- "This is the public reference. If you're looking for an internal SOP, a personnel record, or a vendor contract, that lives elsewhere: in SharePoint, in HR systems, or in procurement records, not in this wiki."
  → "This is the public reference. Internal SOPs, personnel records, and vendor contracts live elsewhere — in SharePoint, HR systems, and procurement records." **[safe]** (Singular "that lives" disagrees with the plural list; the rewrite fixes agreement and tightens.)

- "Does it use Innovation Lab for the craft of solving and Cross-Agency Delivery for the cross-agency coordination?"
  → "Does it use Innovation Lab for the craft of solving problems and Cross-Agency Delivery for cross-agency coordination?" **[safe]** ("the craft of solving" is missing an object; drops one redundant "the.")

- "Does it describe CitiStat as an executive performance rhythm rather than a meeting calendar?"
  → "Does it describe CitiStat as an executive performance routine rather than a meeting calendar?" **[judgment]** ("rhythm" is softer/more jargony than "routine," which the glossary and other pages favor; owner may prefer "rhythm" deliberately.)

- "Does it avoid retired or use-carefully terms unless the historical context requires them?"
  → "Does it avoid retired or use-with-care terms unless the historical context requires them?" **[safe]** ("use-carefully terms" is ungrammatical as an adjective phrase.)

---

## 2. `docs/resources/index.md`

**Assessment.** Two lines, both fine. Plain, scannable, does its job as a section landing page.

**Line-level recommendations**

- "Reference material and how to contribute." → keep as-is. **[safe]** (No change needed.)

---

## 3. `docs/resources/reference/index.md`

**Assessment.** Clean. The "Start with these references" pointer is genuinely useful onboarding guidance and reads in plain, active voice.

**Line-level recommendations**

- "Those pages define the operating language used across the rest of the wiki."
  → "Those pages define the operating language used across the wiki." **[safe]** ("across the rest of the wiki" — "the rest of" is filler.)

---

## 4. `docs/resources/reference/glossary.md`

**Assessment.** The strongest reference asset in scope: definitions are largely parallel, plain, and policy-literate, and the "**Term.** definition" pattern (accepted house style) is applied consistently. The risk here is not voice but length drift — a handful of entries run to paragraph length while their neighbors are one crisp sentence, which breaks the scannability a glossary lives on. A few definitions also lean on internal shorthand a public reader won't decode.

### Glossary-specific consistency findings (definition prose only; headwords untouched)

- **Parallelism is mostly good.** Most entries open with a noun phrase ("The city's service-request system…", "The platform that powers…"). A few break the pattern by opening differently or burying the definition — see line items below.
- **Length is the main inconsistency.** Outliers that run long relative to peers: **Cross-Agency Delivery** (the longest, ~7 sentences), **Innovation Lab**, **Tiger Team**, **CitiStat Director**, **Data-Driven Officer**, **Debrief**, **Follow-up memo**. None is wrong, but trimming the longest two toward 3–4 sentences would restore scan rhythm. (Many of these are load-bearing operating-model terms, so trims are **[judgment]**.)
- **Plainness is high.** Watch a few terms that assume the reader already knows OPI jargon ("air cover," "pre-memo," "ground-truth") and define-in-place or soften.

**Line-level recommendations**

- "**Authorizer.** The executive who authorizes a Stat, a Tiger Team, or a Cross-Agency Delivery activation and provides the air cover the work needs."
  → "…and provides the executive cover the work needs." **[judgment]** ("air cover" is insider idiom; "executive cover" or "the authority the work needs" is plainer for a public audience. Tone call — owner may want the idiom.)

- "**CitiStat Inspector.** The OPI role responsible for ground-truth checks that keep Stat conversations honest: ride-alongs, site visits, and field validation."
  → "**CitiStat Inspector.** The OPI role responsible for field checks that keep Stat conversations honest: ride-alongs, site visits, and on-the-ground validation." **[safe]** ("ground-truth" is technical jargon; "field checks" / "on-the-ground" is plainer and keeps the meaning.)

- "**Closure.** The end of a commitment, project, or Tiger Team, evidenced by a link, a metric, or a changed process, not just declared."
  → "**Closure.** The end of a commitment, project, or Tiger Team — proven by a link, a metric, or a changed process, not just declared." **[safe]** ("evidenced by" is passive-leaning bureaucratese; "proven by" is plainer and active.)

- "**Cross-Agency Delivery.** … It owns the coordination authority: named Authorizers, Senior Responsible Owners, decision rights, sustainment commitments, and the weekly delivery cadence. The Innovation Lab provides the team and the method; Performance provides the standing performance routine; the Director's Office provides the authorizing relationships at the Deputy Mayor and City Administrator level. Activates as a Tiger Team, a standing delivery review, or an embedded delivery engagement, depending on the problem. Always written in full; do not abbreviate as CAD, which collides with Computer-Aided Dispatch."
  → Consider trimming the middle "provides…provides…provides" triad, which repeats content carried in full on the operating-model and crosswalk pages. The entry could end after "…depending on the problem." and keep the CAD note. **[judgment]** (Longest entry in the glossary; the detail is accurate but a glossary should point, not re-explain the whole model. Owner decides whether the redundancy is intentional.)

- "**Decision-grade.** A standard for analytics work: data and analysis credible enough to anchor a real decision. Sourced, current, defined, and tested."
  → keep as-is. **[safe]** (Model entry: parallel, plain, crisp. No change.)

- "**Front door.** … Freelance project starts are out of bounds."
  → "… Projects do not start on their own; everything comes through here." **[judgment]** ("Freelance project starts are out of bounds" is OPI shorthand; plainer for a public glossary, but the punchy original may be intended. Owner call.)

- "**North star.** "Respond when necessary. Build so we do not have to respond again." OPI's shorthand for the bias toward systemic, durable improvement."
  → "…OPI's shorthand for choosing systemic, durable fixes over one-off responses." **[judgment]** ("the bias toward systemic, durable improvement" is abstract; the rewrite is more concrete. Tone call.)

- "**Walk-up music.** The short piece of music played as panelists and attendees enter the Stat room. A small, deliberate cue that the meeting is starting and that the routine takes itself seriously without taking itself too seriously."
  → Trim the second sentence to "A small, deliberate cue that the meeting is starting." **[judgment]** ("takes itself seriously without taking itself too seriously" is a cute flourish that breaks the glossary's even register; some will love it. Owner call.)

- "**Tiger Team.** A time-boxed, cross-functional delivery sprint focused on one service problem, typically three to six months, scoped to the problem. … what determines the path is whether the work needs Cross-Agency Delivery's coordination authority: named Authorizers at the Deputy Mayor or City Administrator level, decision rights across agencies, and a closure plan with sustainment commitments from each agency."
  → Tighten the tail: this entry restates the Cross-Agency Delivery test verbatim from three other pages. Consider ending after "…or several" and linking to the Playbook for the test. **[judgment]** (Accuracy is fine; this is length/redundancy. Owner decides.)

- "**Operational metrics.** The standing operating measures that appear on every Stat deck — the day-to-day performance signals an agency or service runs by, distinct from the strategic KPIs and the priority deep-dive topics."
  → keep; one prose em-dash here is within tolerance. **[safe]** (No change.)

- Naming-norms bullet: "Avoid "scrape" and "crawl" in resident-facing copy; prefer "collect," "gather," or "extract.""
  → keep as-is. **[safe]** (Clear, useful, plain.)

---

## 5. `docs/resources/reference/tiger-teams-playbook.md`

**Assessment.** Substantive and well-structured, but the longest page in scope and noticeably repetitive: the Tiger Team definition, the "when to use / when not to use" criteria, the three-to-six-month time-box, and the Cross-Agency Delivery charter test each appear two or three times. The phase descriptions (AIM/DESIGN/ACTIVATE/SUSTAIN) are crisp and concrete — the best part of the page. The voice is active and plain throughout; the issue is volume, not tone.

**Line-level recommendations**

- Structural: "### When to use a Tiger Team" appears near the top (lines 25–33) and again as "## When to use a Tiger Team" (lines 86–96) with near-identical criteria; "### When not to use a Tiger Team" and the "Plain-language test" (lines 70–72) cover the same ground a third time.
  → Collapse to one "When to use / When not to use" section. **[judgment]** (Significant restructure; the repetition is the page's biggest readability cost, but consolidation is the owner's call.)

- "Baltimore City has lived with persistent gaps in basic service delivery: parking enforcement, traffic calming, sweeping, waste, code enforcement, forestry. These gaps are not surprises; they are systemic."
  → keep as-is. **[safe]** (Strong, concrete, Bloomberg-register opening. Model paragraph.)

- "A Tiger Team is a focused delivery sprint, time-boxed to the problem, that brings a cross-functional team to one service problem."
  → "A Tiger Team is a focused, time-boxed delivery sprint that brings a cross-functional team to one service problem." **[safe]** ("delivery sprint, time-boxed to the problem, that brings… to one service problem" — "to the problem"/"one service problem" doubles up; tightened.)

- "It moves from analysis to action through fast diagnosis and rapid prototypes that test solutions in real conditions, and it ends with a plan to scale: ownership, operating procedures, and data products."
  → "It moves from analysis to action through fast diagnosis and prototypes tested in real conditions, then ends with a plan to scale: ownership, operating procedures, and data products." **[safe]** ("fast…rapid" is redundant intensifier-stacking; trimmed.)

- "**Purpose.** Prototype, pilot, and scale initiatives in real conditions, not in slides."
  → keep as-is. **[safe]** ("not in slides" is exactly the concrete, plain contrast the target wants.)

- "Mid-cycle review (≋ week 13): is the diagnosis right; are the right pilots running."
  → "Mid-cycle review (around week 13): is the diagnosis right; are the right pilots running." **[safe]** (The "≋" glyph is a rendering accident / approximation symbol misuse; "around" or "≈" is intended. Use a word for a public page.)

- "Produces tangible pilots — people, process, technology — not just recommendations."
  → keep. **[safe]** (One prose em-dash pair, within tolerance, and it's doing real work.)

- "No sustain plan. The pilot lives, the team disbands, and the gain quietly goes away."
  → keep as-is. **[safe]** (Concrete failure mode, well said.)

- "Cross-Agency Delivery's question is *how do we get multiple agencies to actually ship this together?*"
  → "Cross-Agency Delivery's question is *how do we get multiple agencies to ship this together?*" **[safe]** ("actually" is an empty intensifier.)

- OWNER field: "Innovation Lab — with Performance at sustain, and Cross-Agency Delivery when the work needs cross-agency coordination authority"
  → keep (def-list field; em-dash is structural, not prose). **[safe]** (No change.)

---

## 6. `docs/resources/reference/service-crosswalk.md`

**Assessment.** Excellent — does exactly what an accountability crosswalk should: one scannable table, mandate-to-outcome, no padding. Voice is factual and crisp. The "Outcomes it is accountable for" cells use telegraphic fragments, which is right for a dense table.

**Line-level recommendations**

- "This page maps each budgeted service to the City Code mandate behind it, the goal it pursues, and the outcomes it is accountable for, so oversight can see how OPI's structure maps to public value."
  → "This page maps each budgeted service to its City Code mandate, the goal it pursues, and the outcomes it is accountable for, so oversight can see how OPI's structure delivers public value." **[safe]** ("maps… maps to" repeats the verb in one sentence; "the mandate behind it" → "its mandate"; "delivers public value" is more concrete than "maps to public value.")

- "performance visible without spreadsheets" (Performance Management outcomes cell)
  → keep as-is. **[safe]** (Concrete, memorable, on-voice.)

- "public data that's clear and current; one official record per dataset; AI readiness"
  → keep. **[safe]** (Telegraphic table style is appropriate here.)

- "Counts are drawn from the [org structure] and exclude the Executive Director, who leads across all cost centers."
  → keep as-is. **[safe]** (Clear footnote.)

---

## 7. `docs/resources/reference/theory-of-change-summaries.md`

**Assessment.** Clean index page that resists the temptation to duplicate the summaries it points to — and says so explicitly, which is good governance writing. The "How to read a theory of change" table is genuinely plain-language. "The point of a theory of change is not to be right. It is to be honest…" is a strong, human line.

**Line-level recommendations**

- "It carries no independent summaries of its own, so there is one place, and only one place, to maintain each service's logic."
  → "It carries no summaries of its own, so each service's logic lives in exactly one place." **[safe]** ("independent summaries of its own" is redundant ("of its own" already implies independent); "one place, and only one place" is wordy emphasis.)

- "A theory of change is a step-by-step explanation of how the work we do leads to the change we want to see."
  → "A theory of change explains, step by step, how the work we do leads to the change we want to see." **[safe]** (Tighter; "is a step-by-step explanation of how" → active verb.)

- "Each service's assumptions become things we look at in our quarterly review."
  → "Each service's assumptions become items we test in our quarterly review." **[safe]** ("things we look at" is vague filler; "items we test" is concrete and matches the section heading "How we test the theories.")

- "The point of a theory of change is not to be right. It is to be honest about why we believe what we are doing will work, and to find out quickly when it does not."
  → keep as-is. **[safe]** (Best paragraph on the page; do not touch.)

---

## 8. `docs/resources/reference/strategic-priorities-one-pager.md`

**Assessment.** Mostly strong, concrete, and refreshingly specific (dollar figures, dated commitments, named owners and signals). Two recurring drags: a casing inconsistency ("tiger teams" / "tiger team" lowercase in body text vs. "Tiger Team" proper-noun style on the playbook and glossary), and a couple of breathless section headers ("The next-level moves") that clash with the otherwise sober register.

**Line-level recommendations**

- Casing: "tiger teams cohort: six FY26 focus areas…", "Continue the tiger team model…", "tiger team gains stay gained…", "Are tiger teams ending with sustained gains?"
  → Use "Tiger Team(s)" to match the glossary and playbook headword. **[safe]** (Consistency with the canonical term; not a taxonomy change, just casing.)

- "## FY27 — The next-level moves"
  → "## FY27 — The next moves" or "## FY27 — Building on the foundation." **[judgment]** ("next-level" is hype register out of step with the page's sober tone; owner decides.)

- "With the foundation in place, FY27 shifts focus to bigger, more visible outcomes."
  → "With the foundation in place, FY27 turns to bigger, more visible outcomes." **[safe]** ("shifts focus to" → "turns to"; tighter.)

- "Push from "put out the fire" to "find the spark": root-cause work that prevents the fire next year."
  → keep as-is. **[safe]** (Vivid, concrete, earns its metaphor.)

- "Use the city's investment in Workday to its full potential: proper reporting, better HR processes and reporting, capital budget management, grants, and internal workflows that work."
  → "Use the city's Workday investment fully: better reporting, HR processes, capital budget management, grants, and internal workflows that work." **[safe]** ("to its full potential" is filler; "reporting… and reporting" lists reporting twice; trimmed.)

- "We measure ourselves on whether the city's services are getting more reliable, not on the volume of activity in our office."
  → keep as-is. **[safe]** (On-voice; clear contrast.)

- "add the FY27 target of 50% of agencies achieving 90% of their commitment targets"
  → keep as-is. **[safe]** (Specific and measurable — exactly the register the target wants.)

- "Prepare Baltimore for AI with intention and integrity"
  → "Prepare Baltimore for AI, carefully and openly." **[judgment]** ("with intention and integrity" is alliterative mission-speak; the bullets below ("Publish what we are doing and what we are not") already deliver the substance plainly. Owner may want the alliteration as a header hook.)

---

## 9. `docs/resources/reference/operating-model-staff-version.md`

**Assessment.** Clear, well-organized, and genuinely useful to its staff audience. The intake path, decision rights, and escalation sections are crisp and active. "Metadata is part of the work." is a great short directive. Casing on "tiger teams" drifts here too. A few sentences carry mild filler but nothing breathless.

**Line-level recommendations**

- Casing: "…AI pilots, partnerships, and tiger teams." (portfolio table) and "…prototyping, tiger teams, and digital service work."
  → "Tiger Teams" to match the canonical headword. **[safe]** (Consistency.)

- "OPI combines performance, data, design, and delivery to help Baltimore City improve services in ways residents and staff can see and feel."
  → keep as-is. **[safe]** (Strong one-sentence definition.)

- "Our job is to make sure that when residents call 311, apply for a permit, or rely on trash collection, those services actually work…"
  → "Our job: when residents call 311, apply for a permit, or rely on trash collection, those services work — and city staff have the routines, data, and tools to keep them working." **[judgment]** (Drops "make sure that… actually," tightening the sentence and removing the empty "actually"; restructures into a cleaner contrast. Owner decides on the colon construction.)

- "One service, Cross-Agency Delivery, is not a stand-alone team: it is a way of running work that several agencies have to ship together, drawing staff from the other portfolios."
  → keep as-is. **[safe]** (Accurate and plain; defines the term cleanly.)

- "Tag your work in SharePoint with portfolio, service, and sensitivity. Metadata is part of the work."
  → keep as-is. **[safe]** (Punchy, memorable directive.)

- "Each team lead decides scope and pace inside their portfolio."
  → keep. **[safe]** (Active, clear.)

- "Through human-centered design, prototyping, tiger teams, and digital service work." (and the parallel "Through…" fragments in "How the services interlock")
  → keep the bold-lead + "Through…" fragment structure as-is; it's a deliberate parallel device. (Casing fix above still applies.) **[safe]**

---

## 10. `docs/resources/reference/wiki-knowledge-base-structure.md`

**Assessment.** Long but well-governed: the opening "Two different systems" admonition is exactly the disambiguation a reader needs, and the Find/Trust/Survive framing is clean. The page is dense with tables and bullet lists, which suits a structure spec. Voice is plain and active. "It is not a file dump." earns its bluntness. Casing on "tiger teams" drifts again. A couple of sentences over-explain.

**Line-level recommendations**

- Casing: "…CitiStat, Innovation Lab methods, tiger teams, data governance, responsible AI." and "Service playbooks and methods (CitiStat, data governance, Innovation Lab methods, tiger teams)." and "CitiStat, Innovation Lab methods, tiger teams, data governance, responsible AI." (pillar table)
  → "Tiger Teams" to match the canonical headword. **[safe]** (Consistency.)

- "The goal is simple: anyone joining OPI should be able to find the official document, the right template, the active project list, and the person who owns each thing, in under five minutes."
  → "The goal: anyone joining OPI can find the official document, the right template, the active project list, and the owner of each — in under five minutes." **[safe]** ("The goal is simple:" pre-announces simplicity instead of being simple; "should be able to find" → "can find"; "the person who owns each thing" → "the owner of each.")

- "It is not a file dump. It is a maintained operating manual with named owners, review cadences, and a quality bar."
  → keep as-is. **[safe]** (Blunt, concrete, on-voice.)

- "Other tools (Teams chats, OneDrive, personal folders) are not the system of record — by policy."
  → keep; the trailing em-dash "— by policy" is doing emphatic work and is within tolerance. **[safe]** (No change.)

- "Depth comes from consistent subpages, not from adding more tabs."
  → keep as-is. **[safe]** (Clear design principle.)

- "Mismatch is the leading cause of drift."
  → keep as-is. **[safe]** (Concrete, earns its place.)

- "The Wiki is built in three releases so it is useful on day one and improves with use."
  → keep as-is. **[safe]** (Plain and active.)

- "Method pages should define how OPI works, not simply describe past work."
  → "Method pages should define how OPI works, not just describe past work." **[safe]** ("simply" → "just"; minor, both fine, "just" is plainer.)

---

## Section-level / cross-page consistency findings

1. **"tiger team(s)" casing drift.** The glossary and the Tiger Teams Playbook treat **Tiger Team** as a proper-noun headword (title case). Three other pages — strategic-priorities-one-pager, operating-model-staff-version, and wiki-knowledge-base-structure — write it lowercase ("tiger teams") in body text. Standardize to **Tiger Team(s)** everywhere. This is the single most frequent consistency issue in scope. (All **[safe]** casing fixes; not a taxonomy change.)

2. **"Cross-Agency Delivery" spelled in full, never CAD — clean.** Every page honors this. The CAD/Computer-Aided Dispatch collision note in the glossary is the canonical source. No issues.

3. **The Cross-Agency Delivery "coordination authority" test is restated nearly verbatim across four pages** (glossary Tiger Team + Cross-Agency Delivery entries, the playbook in two places, and the strategic-priorities note). It's accurate everywhere, but the repetition adds length. Consider designating one canonical statement (the playbook) and having the others point to it. **[judgment]** — owner's call on whether the redundancy is deliberate reinforcement.

4. **North star line is consistent and verbatim** ("Respond when necessary. Build so we do not have to respond again.") across glossary, theory-of-change, strategic-priorities, operating-model, and wiki-structure. Good. No change.

5. **Def-list fields (VERSION / UPDATED / OWNER / AUDIENCE) are consistent** across the four pages that carry them. The "UPDATED: April 2026" matches the v1.x stamps. No issues — not touched per scope.

6. **Em-dash usage is disciplined.** Prose-flow em-dash overuse is not a problem on these pages; the "**Term** — definition" pattern (house style) and a handful of single emphatic dashes are all within tolerance. No systemic flags.

7. **Glossary definition length is the one structural inconsistency worth a pass** (see Section 4): a cluster of operating-model terms run to paragraph length while peers are one sentence. Trimming the two longest (Cross-Agency Delivery, Tiger Team) toward 3–4 sentences would restore scan rhythm without losing accuracy. **[judgment]**

---

## Tally

- **[safe]** recommendations: **27**
- **[judgment]** recommendations: **13**
- Pages where the dominant note is "keep as-is / already on target": index.md, reference/index.md, service-crosswalk.md, theory-of-change-summaries.md (light touch only).
- Highest-effort opportunities (all [judgment]): de-duplicating the Tiger Teams Playbook's repeated "when to use" criteria, and trimming the glossary's longest entries.
