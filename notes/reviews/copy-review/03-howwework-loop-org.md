# Copy Review 03 — How We Work: the Loop + Organization

Reviewer: senior editor (Bloomberg + HKS voice target)
Date: 2026-06-23
Scope reviewed in full:

- `docs/how-we-work/index.md`
- `docs/how-we-work/how-work-moves-through-opi.md` (load-bearing model page)
- `docs/how-we-work/organization/index.md`
- `docs/how-we-work/organization/org-structure.md`
- `docs/how-we-work/organization/team-and-roles/index.md`

Note on house style: the `**Term** — definition` em-dash pattern in bulleted lists and "Read alongside" blocks is accepted and not flagged. Only prose-flow em-dash overuse is flagged. Macros, links, anchors, taxonomy words, names, titles, PINs, and classifications are left untouched.

---

## 1. `how-we-work/index.md`

**Assessment.** Short, functional landing copy. The voice is mostly on target — concrete and plain — but the opening sentence stacks two ideas into one comma-spliced clause, and "day-to-day mechanics" trails into a soft list. The bolded one-line model summary is strong and earns its place. The parenthetical in the third paragraph is overloaded and reads like an inventory dump rather than a sentence a reader can hold.

### Recommendations

1. **[safe]** Weak/overstuffed opening.
   - Before: "OPI moves work through a simple signal-to-solution loop, and runs the office with a set of internal operating routines."
   - After: "OPI moves work through a simple signal-to-solution loop, and runs the office on a set of internal routines."
   - (Drops "operating" as filler; "runs the office with a set of" → "runs the office on" tightens.)

2. **[judgment]** The third paragraph's parenthetical is a 30-word list inside one sentence and is hard to parse.
   - Before: "For the full model (what each service owns, the handoffs, and when to use a Stat, a data product, an Innovation Lab engagement, a Tiger Team, a Cross-Agency Delivery activation, or a decision memo) read **[How Work Moves Through OPI](how-work-moves-through-opi.md)**."
   - After: "For the full model — what each service owns, how the handoffs work, and when to use a Stat, a data product, an Innovation Lab engagement, a Tiger Team, a Cross-Agency Delivery activation, or a decision memo — read **[How Work Moves Through OPI](how-work-moves-through-opi.md)**."
   - (Converts the parenthetical to em-dash setoff so the main clause "For the full model ... read X" stays continuous. Owner decides; this is the one place an em-dash pair improves flow.)

3. **[safe]** "the day-to-day mechanics: onboarding, memos, how-to guides, and operations" — "operations" is vague and overlaps "mechanics."
   - Before: "the day-to-day mechanics: onboarding, memos, how-to guides, and operations."
   - After: "and the day-to-day mechanics: onboarding, memos, and how-to guides."

---

## 2. `how-we-work/how-work-moves-through-opi.md` (load-bearing — scrutinized hardest)

**Assessment.** This is the strongest-written page in scope and the most important. The voice is largely on target: declarative, concrete, policy-literate, with genuinely useful decision tables. The bolded model line, the decision rules, and the "Common confusion" table are excellent — plain, opinionated, human. The drag comes from a handful of AI-cadence tics ("not just a meeting and not every recurring meeting is a Stat," "not just to produce charts," "not just recommendations" — the "not just X, but Y" frame recurs four-plus times and becomes a verbal habit), a few abstract nouns ("craft of solving," "operating backbone"), and one genuinely jargon-heavy stretch in the "owns the coordination" block. Tighten the repeated "not just" frame and the few abstractions and this page is near-final.

### Recommendations

1. **[safe]** "The short version" opener is a touch soft.
   - Before: "OPI works best when each part of the office is clear about what it owns and how the handoffs work."
   - After: "OPI works best when every part of the office knows what it owns and how the handoffs work."
   - ("is clear about" → "knows"; "each" → "every" for a firmer cadence.)

2. **[judgment]** Repeated "not just" frame — appears in CitiStat ("not just a meeting"), Data and Analytics ("not just to produce charts"), and Tiger Teams ("not just recommendations"). The construction is fine once; four times it reads as an AI tell. Recommend varying at least two. Example for the CitiStat instance:
   - Before: "It is not just a meeting and not every recurring meeting is a Stat."
   - After: "It is more than a meeting, and not every recurring meeting is a Stat."

3. **[safe]** "data quality sprint, product discovery, a Tiger Team, a delivery activation, or a one-time executive decision" — clean; no change. (Noted as a positive.)

4. **[judgment]** "The Innovation Lab owns the craft of solving" — the heading is evocative but abstract for a public audience; "craft of solving" is not a concrete noun.
   - Before: "### The Innovation Lab owns the craft of solving"
   - After: "### The Innovation Lab owns how problems get solved"
   - (Owner decides — "craft" is arguably intentional brand voice. If kept, leave it; flag only.)

5. **[safe]** Over-hedged sentence in Data and Analytics block.
   - Before: "Its role is to make the evidence reliable enough to support action, not just to produce charts."
   - After: "Its job is to make evidence reliable enough to act on, not just to produce charts."
   - ("role is to make the evidence reliable enough to support action" is wordy; "act on" is more concrete than "support action.")

6. **[safe]** Jargon stack in the Cross-Agency Delivery block — this is the densest sentence on the page for a non-technical reader.
   - Before: "Cross-Agency Delivery owns the coordination authority: Authorizer, Senior Responsible Owner, decision rights, commitment tracking, escalation, weekly or bi-weekly delivery cadence, and sustainment commitments across agencies."
   - After: "Cross-Agency Delivery owns the coordination authority: who authorizes the work, who the Senior Responsible Owner is, who holds decision rights, plus commitment tracking, escalation, a weekly or bi-weekly delivery cadence, and sustainment commitments across agencies."
   - (Owner decides — this is longer but readable; alternatively keep the term list as-is since it functions as a glossary line. Flag the parallelism: "Authorizer" is a role, "decision rights" is a thing, "commitment tracking" is an activity — the list mixes categories.)

7. **[judgment]** "Its question is: **How do we get multiple agencies to actually ship this together?**" — "actually" is a filler intensifier and the casual "ship" sits oddly next to "multiple agencies."
   - Before: "How do we get multiple agencies to actually ship this together?"
   - After: "How do we get multiple agencies to deliver this together?"
   - (Drops "actually"; "deliver" reads more authoritative than "ship" for a government audience. Owner may prefer "ship" as deliberate voice — flag only. Note: the same "ship together" phrasing also appears in the loop table row 4, "How do we get multiple agencies to ship this together?" — align both.)

8. **[safe]** "AdminOps owns the operating backbone" + body — "operating backbone" is a metaphor; the body sentence is a long inventory.
   - Before: "AdminOps keeps the work visible, documented, communicated, and sustained. It owns intake discipline, portfolio visibility, knowledge management, executive briefings, Council readiness, communications, QA, and the operating routines that keep a small office from becoming reactive or personality-dependent."
   - After: No change to the inventory (it is reference content), but consider trimming the closing flourish: "personality-dependent" is jargon. Suggest: "...the operating routines that keep a small office from running on individual heroics."
   - (Owner decides — "personality-dependent" is precise management-speak; "individual heroics" is plainer but changes register.)

9. **[safe]** Tiger Team definition — clean and concrete; the "not just recommendations" tail is the one weak spot (see rec 2 pattern).
   - Before: "...and a sustainment plan, not just recommendations."
   - After: "...and a sustainment plan — not a stack of recommendations."
   - (Sharper and more human; or simply delete the tail since the preceding list already proves the point. Owner decides.)

10. **[safe]** Decision rule 5 is strong ("Launch is not success."). No change. (Positive note.)

11. **[safe]** "Common confusion" table — the "less theatrical" rationale for "Delivery room" is good plain writing. No change.

12. **[judgment]** Function boundaries intro: "OPI's teams overlap by intent, not by accident." — strong line, keep. The following sentence is slightly passive.
    - Before: "When more than one team could plausibly own a piece of work, these rules decide who leads."
    - After: "When more than one team could own a piece of work, these rules decide who leads."
    - ("plausibly" is a soft hedge that adds nothing.)

13. **[safe]** Function boundaries table, "Operational digital products" cell ends with an em-dash dependent clause inside a table cell that is itself a long list. Acceptable in a table; no change required, but note the cell runs long for mobile.

---

## 3. `organization/index.md`

**Assessment.** Minimal and clean. The blockquote summary line is concrete and does its job. No meaningful drag. One small parallelism note in the two bullets.

### Recommendations

1. **[safe]** The blockquote uses an em-dash in prose (not the term-definition pattern).
   - Before: "> OPI's structure and its people — the org chart and the staff roster."
   - After: Acceptable as-is (it reads as an appositive summary, not a flow problem). No change needed; flagging only for awareness.

2. **[safe]** Bullet parallelism is fine ("Org Structure — ..." / "Team and Roles — ..."). No change.

---

## 4. `organization/org-structure.md`

**Assessment.** Mostly on target — authoritative, structured, with clear "three lenses" framing. The two italic blockquote aphorisms ("Better government is not a one-time project. It is a discipline." and "We move with urgency, but not chaos.") are punchy and human; they fit the brand voice. The drag is in the parenthetical-heavy definitional sentences (the Cross-Agency Delivery overlay is defined three times across the page with slightly different wording) and a couple of passive/wordy constructions in the "How to Read This Structure" section.

### Recommendations

1. **[safe]** Opening sentence is solid. The second sentence is slightly redundant with the first.
   - Before: "OPI delivers its mission through four teams and five services. The teams are how we organize people, leadership, and cost centers. The services are how we describe what OPI delivers to residents, agencies, and city leadership."
   - After: Keep as-is — this is foundational framing and the repetition aids comprehension. No change. (Positive note: clear and concrete.)

2. **[judgment]** Cross-Agency Delivery is defined parenthetically here, then again in its own section, then again in the cost-center note. The cost-center-line parenthetical is the most cluttered.
   - Before: "Cross-Agency Delivery is tracked as a service overlay (a coordinating function that draws on staff from across OPI rather than a team of its own) unless and until dedicated staff or budget are assigned."
   - After: "Cross-Agency Delivery is tracked as a service overlay — a coordinating function that draws on staff from across OPI rather than a standing team — unless and until dedicated staff or budget are assigned."
   - (Owner decides — same definition appears verbatim-ish in how-work-moves rec; recommend aligning the wording ("standing team" vs "a team of its own") across both pages for consistency. See consistency findings below.)

3. **[safe]** Passive construction in "How to Read This Structure."
   - Before: "When work is intaken, we ask: which team holds the lead?"
   - After: "When we intake work, we ask: which team holds the lead?"
   - ("is intaken" is both passive and an awkward verbed noun; "When we intake work" keeps the house term but goes active.)

4. **[safe]** Wordy hedge in the staff-alignment note.
   - Before: "with aspirational seats labeled as such so the current team and intended structure stay visible in one place."
   - After: "with aspirational seats labeled so the current and intended structure stay visible together."
   - ("labeled as such" → "labeled"; "in one place" → "together.")

5. **[safe]** "Execution model" cell in the overlay table runs long and stacks three clauses.
   - Before: "Assigned lead by activation; time-boxed delivery reviews or working sessions; status tracked through the team leadership council and weekly leadership reporting."
   - After: "Lead assigned at activation; time-boxed delivery reviews or working sessions; status tracked through the leadership council and weekly leadership reporting."
   - ("Assigned lead by activation" is garbled syntax → "Lead assigned at activation"; "team leadership council" vs "leadership council" — see consistency note.)

6. **[safe]** "stewarding delivery discipline and cross-agency coordination" — "stewarding" is soft jargon.
   - Before: "Danny Heller serves as Interim Delivery Manager, stewarding delivery discipline and cross-agency coordination."
   - After: "Danny Heller serves as Interim Delivery Manager, overseeing delivery discipline and cross-agency coordination."
   - (Owner decides — "stewarding" may be deliberate; "overseeing" or "leading" is plainer.)

---

## 5. `organization/team-and-roles/index.md`

**Assessment.** This is primarily a reference roster (tables, PINs, classifications) and reads correctly as such — no rewriting of the data. The narrative connective tissue is clean and plain. The italic aphorism ("Respond when necessary. Build so we do not have to respond again.") is strong. Only minor prose touch-ups in the framing sentences.

### Recommendations

1. **[safe]** "How OPI is organized" sub-lead uses "working groups," which is a fourth term for the same concept the rest of the section calls "teams."
   - Before: "OPI runs as four working groups under the Executive Director:"
   - After: "OPI runs as four teams under the Executive Director:"
   - (Consistency: org-structure.md and how-work-moves both say "four teams." "Working groups" introduces a synonym that muddies the taxonomy. Recommend "teams." Marked [safe] because it aligns with established usage, but confirm it does not collide with the card_grid labels.)

2. **[safe]** "How to read this document" — long sentence with a semicolon-joined example.
   - Before: "Teams and cost centers do not always match one-to-one; the Director's Office, for example, includes positions funded under AdminOps and positions funded under the Innovation Lab cost center."
   - After: "Teams and cost centers do not always match one-to-one. The Director's Office, for example, includes positions funded under AdminOps and others funded under the Innovation Lab cost center."
   - (Split the run-on; "positions funded ... and positions funded" → "positions funded ... and others funded" removes the repetition.)

3. **[safe]** Closing italic note has a minor wordiness.
   - Before: "PIN numbers and budget detail come from Baltimore City's official position file."
   - After: "PINs and budget detail come from Baltimore City's official position file."
   - ("PIN numbers" is redundant — the N already stands for Number. Note: "PIN" is a protected taxonomy term per scope, so this only drops the trailing word "numbers," it does not alter the term.)

---

## Section-level consistency findings

1. **"team(s)" vs "working groups."** `team-and-roles/index.md` says "four working groups"; everywhere else (index, how-work-moves, org-structure) it is "four teams." Standardize on **teams**. (See team-and-roles rec 1.)

2. **Cross-Agency Delivery definition wording drifts.** Three near-identical definitions use different phrasing for the "not a standing team" idea:
   - how-work-moves: "draws on staff from across OPI rather than a standing team, and not a cost center"
   - org-structure intro parenthetical: "draws on staff from across OPI rather than a team of its own"
   - org-structure cost-center note: "a coordinating function that draws on staff from across OPI rather than a team of its own"
   Recommend one canonical phrase — suggest "draws on staff from across OPI rather than a standing team" — used consistently.

3. **"ship" vs "deliver."** how-work-moves uses "ship this together" in both the loop table (row 4) and the Cross-Agency Delivery question. If you accept the move to "deliver" (rec 7), change both instances; if you keep "ship," keep both. Do not split.

4. **"leadership council" naming.** org-structure's overlay table says "team leadership council" in the Execution-model cell. Confirm whether the canonical body is "leadership council" or "team leadership council" and use one form. (Flagged, not auto-changed — may be a defined governance body.)

5. **"AdminOps" cost-center vs "Performance Management" cost-center labels.** org-structure's Cost Centers table lists the center as **Performance**; team-and-roles "OPI at a Glance" lists cost centers as "Performance Management"; the roster tables use "Performance Management" for cost center and "Performance" for team. This is a team-vs-cost-center distinction and is likely correct, but the proximity of "Performance" (team) and "Performance Management" (cost center) is a known reader trip-point. No copy change recommended — flagging for awareness; the existing "teams and cost centers do not always match" note partly covers it.

6. **The "not just X" frame** recurs across how-work-moves (CitiStat, Data and Analytics, Tiger Teams) and once in org-structure tone. Vary it (see how-work-moves rec 2/5/9) so it does not read as a template.

7. **Heading style is consistent** (sentence case for H2/H3, Title Case reserved for proper section names like "The Four Teams," "Five Services," "How to Read This Structure"). Minor: org-structure mixes "The Four Teams" / "Five Services" (Title Case) with "Cost Centers and Budget Services" (Title Case) and "How to Read This Structure" (Title Case), while how-work-moves uses sentence case ("What each service owns," "Decision rules"). Both pages are internally consistent; the two pages differ from each other. If a house standard exists, align — otherwise leave, as each page is self-consistent.

8. **Aphorism blockquotes** ("Better government is not a one-time project. It is a discipline.", "We move with urgency, but not chaos.", "Respond when necessary. Build so we do not have to respond again.") are on-voice and effective. Keep. They are the most distinctly "human" lines in the section and earn their place.

---

## Tally

- Pages reviewed: **5**
- Recommendations: **[safe] 18**, **[judgment] 7** (plus 8 section-level consistency findings, most actionable as [safe] alignment edits).
- Strongest page: `how-work-moves-through-opi.md` — keep its decision tables and aphorisms; tighten the recurring "not just" frame and two abstract headings.
- Weakest drag: parenthetical-heavy definitional sentences and the "working groups"/"teams" terminology split.
