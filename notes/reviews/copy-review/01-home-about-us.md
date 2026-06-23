# Copy Review 01 — Home + About Us + Letters from the Director

Reviewer: Senior Editor (Bloomberg + HKS voice target)
Date: 2026-06-23
Scope: `docs/index.md`; every `.md` directly under `docs/about-us/`; every `.md` under `docs/about-us/letters-from-the-director/`.
Out of scope (other reviewer): `docs/about-us/our-teams/`.

Style target: crisp, factual, active voice, concrete nouns/verbs; authoritative, plain, policy-literate, human. Short declarative sentences. Specifics over adjectives.

Note on the em-dash rule: the `**Term** — definition` pattern in bulleted lists and "Read alongside" blocks is accepted house style and is NOT flagged. Only prose-flow em-dash overuse is flagged.

---

## Cross-page consistency findings (read these first)

1. **All-caps section headings only appear in two pages.** `mission-vision-identity.md` and `operating-principles-and-culture.md` use SCREAMING-CAPS H2s ("NORTH STAR", "MISSION JOURNEY", "OPERATING CHEAT CODES", "PAST SELVES, FUTURE SELVES"). No other page in scope does this — the letters and the index files all use sentence-case or title-case headings. The all-caps style reads as deck-slide residue, not web copy, and it is the single biggest tonal outlier in the set. **[judgment]** Recommend converting to title case ("North Star", "Mission Journey", "Operating Cheat Codes") for sibling parity. These are H2 text, not anchors, so changing them does not break links unless something deep-links the slug; verify before changing.

2. **Two competing voices.** The six letters and `on-opi-foundations.md` are genuinely strong long-form prose — first person, plain, human, on target. `mission-vision-identity.md` and `operating-principles-and-culture.md` are internal strategy-deck transcriptions: caps headers, bolded slide titles followed by italic captions, listening-session framing ("From listening sessions and strategy retros..."). They read like they belong in a different document class than their siblings. Worth a deliberate decision about whether these two are public-facing reference or internal artifacts dressed for the public.

3. **The bold-slide-title + italic-caption pattern repeats heavily** in the two strategy pages (e.g. `**The five framework questions we used to write our mission**` then `*Our mission did not arrive whole...*`). It is an AI/deck tell at volume. The letters never do this. Flagged per-page below.

4. **"Discipline" is the signature word and it is load-bearing — keep it, but watch density.** "Better government is a discipline" is clearly the house thesis (mission tagline, on-opi-foundations, and every letter closes on it). That is good, intentional repetition. The risk is within a single page: `on-cross-agency-delivery.md` ends with "A discipline of finishing" after using "discipline" ~8 times; `on-innovation-and-civic-design.md` leans on it hard too. No change to the motif; just avoid stacking it 3x in one paragraph.

5. **Terminology is consistent and correct.** "Cross-Agency Delivery" is spelled out everywhere; "CAD" never appears. Team/service/program/product taxonomy on the index is used cleanly. AdminOps vs. "administration and operations team" — both forms appear (index uses "AdminOps"; the AdminOps letter uses the long form throughout). That's defensible (letter = plain language) but note the inconsistency exists.

6. **"Recently updated" on the home page is a maintenance hazard, not a copy issue** — flagging only so the owner knows it will go stale without a process. Not a wording rec.

7. **Em-dash density is healthy in the letters** (mostly the accepted definition pattern or single rhetorical dashes). The two strategy pages have a few prose-flow stacks; flagged inline.

---

## docs/index.md — Home

**Assessment:** Hits the target well. Crisp, concrete, active. The "signal-to-solution loop" sentence and the taxonomy table are genuinely good public-reference writing. Minor drag: one or two sentences run long and stack clauses, and a couple of phrasings ("see the work plainly," "keeps us honest" appears elsewhere) lean slightly into mission-speak.

- **[safe]** Hero subhead is a four-part list with a colon that runs long.
  Before: "How a modern performance and innovation office runs, in public: the methodology, the operating model, the strategy, and the people behind Baltimore City's performance and innovation work."
  After: "How a modern performance and innovation office runs, in public — its methodology, operating model, strategy, and people."
  (Drops the repeated "performance and innovation work" already named in the eyebrow.)

- **[safe]** Redundant scope statement.
  Before: "It documents the office's methodology, strategy, and operating model so partners, peer cities, and the public can see the work plainly."
  After: "It documents the office's methodology, strategy, and operating model so partners, peer cities, and the public can see how the work is done."
  ("see the work plainly" is vague; "how the work is done" is concrete.)

- **[judgment]** Line 25 packs the whole taxonomy into one sentence with mismatched verbs ("is organized into teams... delivers services... and runs programs").
  Before: "OPI is organized into teams that have staff and budget, delivers services to city government, and runs programs and products that may involve multiple teams."
  After: "OPI is organized into teams with staff and budget. Those teams deliver services to city government and run programs and products, some of which span multiple teams."
  (Splits one overloaded sentence; fixes the subject-verb drift.)

- **[safe]** "How this site works" bullet is wordy.
  Before: "Every page on this site, and every change to every page, has a commit, an author, and a timestamp."
  After: "Every page, and every change to it, has a commit, an author, and a timestamp."

---

## docs/about-us/index.md — About Us landing

**Assessment:** Short, clean, on target. The blockquote intro and the numbered reading order do their job with no filler. One closing sentence is slightly academic.

- **[safe]** Closing line edges toward jargon ("interpret team-specific methods").
  Before: "This path teaches the operating model before asking readers to interpret team-specific methods."
  After: "This path explains the operating model before readers dig into how individual teams work."

- **[safe]** Minor: "New readers should move through OPI in this order" — you move through the material, not through OPI.
  Before: "New readers should move through OPI in this order:"
  After: "New readers should work through these pages in order:"

---

## docs/about-us/mission-vision-identity.md

**Assessment:** The content is substantive and the values/customer/misperceptions tables are useful. But the voice is the strongest outlier in the whole set: all-caps headers, deck-caption pairs, and internal-process framing ("what the OPI team has heard, debated, and aligned on") make it read as an internal strategy artifact published verbatim rather than as public reference. Tighten the framing language and it lands much closer to its siblings.

- **[judgment]** All-caps H2s throughout ("NORTH STAR", "MISSION JOURNEY", "WHO WE ARE (AND ARE NOT)", "MISPERCEPTIONS", "VISION THEMES", "CUSTOMER DEFINITION", "STRATEGIC THEMES", "MISSION FRAMINGS", "HOW WE USE THIS DOCUMENT"). Convert to title case for sibling parity. Verify nothing deep-links the slugs first.

- **[judgment]** "How this document should be used" + "NORTH STAR" framing is inward-facing for a public page.
  Before: "This document captures what the OPI team has heard, debated, and aligned on about our identity. It is the human side of the OPI Foundations deck: not the org chart or the service catalog, but the operating story we use to introduce ourselves, recruit teammates, and stay grounded when the work gets hard."
  After: "This page is the human side of OPI Foundations — not the org chart or the service catalog, but the story the office uses to introduce itself, recruit, and stay grounded when the work gets hard."
  (Drops "captures what the team has heard, debated, and aligned on," which is process narration; "deck" reads as internal.)

- **[safe]** AI-tell / deck caption.
  Before: "**The five framework questions we used to write our mission**" then "*Our mission did not arrive whole. We worked through five questions as a team. Each section below captures the answers we converged on.*"
  After: "**Five questions we worked through to write our mission**" then "*We answered these as a team. Each section below is where we landed.*"
  ("did not arrive whole," "converged on," "captures the answers" are the tells.)

- **[safe]** Empty intensifier / vague.
  Before: "Some of our biggest narrative work is corrective: closing the gap between how OPI is described in the wild and what we actually do."
  After: "Much of our communications work is corrective: closing the gap between how OPI is described and what we actually do."
  ("biggest narrative work," "in the wild" are loose.)

- **[safe]** Deck caption before the strategic themes.
  Before: "*From listening sessions and strategy retros, six themes recur. They are not strategy on their own — they are the conditions strategy has to address.*"
  After: "*Six themes recur across our planning. They are not a strategy on their own; they are the conditions any strategy has to address.*"

- **[judgment]** "MISSION FRAMINGS" section is nearly content-free — it shows one quote, says "we capture both here," but only one framing is shown.
  Before: "*The current mission statement consolidates these framings. We capture both here because our mission language is a living statement, not a tagline written by committee.*"
  After: Either show the two framings it references, or cut the section. As written it promises "two ways" and delivers one. (Owner decides — possible content gap, not just wording.)

- **[safe]** Wordiness in value rows is fine, but the values intro caption is a fragment-y run.
  Before: "*Our six core values guide how we work, both with each other and our partners. They are paired with the operating maxim: we move with urgency, but not chaos.*"
  After: "*Six core values guide how we work with each other and our partners, paired with one operating maxim: move with urgency, not chaos.*"

- **Note:** Smart/curly apostrophes are used throughout this file ("Mayor's", "someone's", "agency's"). The letters and index use straight apostrophes in places and curly in others. Not a copy rec per se, but a consistency item worth a global pass.

---

## docs/about-us/operating-principles-and-culture.md

**Assessment:** The ten operating principles are excellent — punchy, concrete, memorable, exactly on target ("Public-sector heroics are usually a sign of a system failure" is the best line in the set). The drag is structural: the same all-caps headers and deck-caption pairs as the mission page, plus a few headers that fight their siblings ("OPERATING CHEAT CODES" is jaunty in a way nothing else is).

- **[judgment]** All-caps H2s ("NORTH STAR", "OPERATING PRINCIPLES", "RECOGNITION CULTURE", "RESIDENT-FOCUSED OPERATING NORMS", "CIVIC DATA COMMUNITY", "OWNERSHIP MODEL", "OPERATING CHEAT CODES", "PAST SELVES, FUTURE SELVES", "HOW WE PLAN TEAM TIME", "LIVING DOCUMENT"). Convert to title case for parity.

- **[judgment]** "OPERATING CHEAT CODES" is a register mismatch with the rest of the site.
  Before: "## OPERATING CHEAT CODES" / "**Frameworks we use across the team**"
  After: "## Frameworks We Use" (and drop the now-redundant bold subtitle).
  ("Cheat codes" is the only gamer-casual heading in an otherwise policy-literate set.)

- **[safe]** Deck caption / process narration.
  Before: "These principles emerged from team listening sessions, strategy retros, and homework reflections."
  After: "These principles come from our team's listening sessions and strategy reviews."
  ("homework reflections" is internal jargon a public reader won't parse.)

- **[safe]** Wordy opener on Recognition.
  Before: "Recognition is operational. It is how we retain people who could be paid more in the private sector, and how we communicate to the rest of the city what good work looks like."
  After: "Recognition is operational. It helps us keep people who could earn more in the private sector, and it shows the rest of the city what good work looks like."

- **[safe]** Jargon for a public audience.
  Before: "GitHub-style contribution programs: open repositories where partners and residents contribute analyses, data products, and documentation."
  After: "Open contribution programs: public repositories where partners and residents add analyses, data products, and documentation."
  ("GitHub-style" assumes the reader knows GitHub; "repositories" is borderline but defensible given the context.)

- **[safe]** Prose-flow em-dash plus passive.
  Before: "Governance — through the Data Governance Council, Open Data Council, and intake committee — is how we share authority instead of bottlenecking on one leader."
  After: "Governance through the Data Governance Council, Open Data Council, and intake committee is how we share authority instead of bottlenecking on one leader."
  (Removes the parenthetical dashes in running prose; reads cleaner.)

- **[safe]** "table stakes" is business-speak.
  Before: "AI evaluation memos, human oversight, and sunset criteria are the table stakes for responsible use." (in mission page §4 too — same phrase)
  After: "AI evaluation memos, human oversight, and sunset criteria are the minimum for responsible use."

- **[safe]** Weak/abstract opener on the ownership table.
  Before: "*Most of our cross-agency conflict comes from unclear ownership. This is the working model we use to disambiguate.*"
  After: "*Most cross-agency conflict comes from unclear ownership. This is the model we use to sort it out.*"
  ("disambiguate" is jargon.)

- **[safe]** The 70/20/10 intro caption is slightly hedged and wordy.
  Before: "*We protect against burnout and chaos by structuring how we allocate our hours. The model below is the working baseline: a guide, not a constraint, reviewed each fiscal year.*"
  After: "*We structure how we spend our hours to guard against burnout. The model below is a working baseline — a guide, not a rule — reviewed each fiscal year.*"

---

## docs/about-us/letters-from-the-director/index.md

**Assessment:** Does its job in three lines. On target. No issues. The blockquote ("Plain language, no jargon") sets the right promise — and the letters keep it.

- No recommendations.

---

## on-opi-foundations.md

**Assessment:** Excellent. This is the model the two strategy pages should aspire to: first person, plain, concrete, confident without hype. Active voice dominates. The "dashboard without a routine is a screen no one looks at" run is exactly the target register.

- **[safe]** Tiny tighten — triple "discipline of" stack risk is fine here (it's deliberate anaphora), leave it. One filler phrase:
  Before: "We are not perfect at any of this yet. We are working on it openly."
  After: "We are not there yet. We are working on it openly."
  (Optional; "perfect at any of this" is slightly loose. Low priority.)

- **[judgment]** "READ ALONGSIDE" links point to artifacts ("About OPI: Operating Frame", "Strategic Priorities OnePager", "Theory of Change Summaries") that are described but not linked. Confirm these resolve to real pages or are intended as plain references. Not a wording change — surfacing a possible dangling-reference issue. ("OnePager" as one word is also a slight house-style oddity vs. "one-pager.")

---

## on-admin-ops.md

**Assessment:** Strong, warm, and concrete. The opening inventory ("before the meeting, behind the dashboard, in the email that confirms a hire...") is vivid and earns its length. Active voice throughout. Very close to target; only minor tightening.

- **[safe]** One sentence stacks four "fails" — effective, but the last is abstract.
  Before: "A new strategy without a budget that backs it is a press release."
  After: Keep — this is the strongest line in the run. No change.

- **[safe]** Mild wordiness.
  Before: "the practical day-to-day routines that make a small office function like a serious one."
  After: "the day-to-day routines that make a small office run like a serious one."
  ("practical" + "function like" is soft; "run like" is crisper.)

- **[safe]** Slight hedge / abstraction.
  Before: "I take administrative and operational excellence personally."
  After: Keep — clear and human. No change. (Noting it as reviewed, not flagged.)

- **[judgment]** "READ ALONGSIDE" entry "**ToC: AdminOps —**" uses an unexplained abbreviation (Theory of Change) that a public reader won't decode; it appears as "Theory of Change Summaries" on the foundations letter but "ToC:" here. Standardize. (Cross-page consistency: spell out "Theory of Change" or define it once.)

---

## on-cross-agency-delivery.md

**Assessment:** Very good. The "work lives in the seams" thesis is concrete and well-developed; the failure-modes paragraph ("scope creeps, ownership blurs, the working group keeps meeting without deciding anything") is exactly the candid, specific register the style guide wants. The only drag is "discipline" density near the end.

- **[safe]** "Discipline" stacks at the close (heading "A discipline of finishing" + "discipline of finishing" + "discipline to take..."). Keep the motif, vary one instance.
  Before: "What we owe residents is the discipline to take the most important of those problems, name them clearly, organize the right people around them, and finish what we start."
  After: "What we owe residents is the resolve to take the most important of those problems, name them clearly, organize the right people, and finish what we start."

- **[safe]** Minor wordiness.
  Before: "It is a discipline for getting complicated, multi-owner outcomes across the line."
  After: "It is a discipline for getting complicated, multi-owner outcomes done."
  ("across the line" is fine but the letter uses sports/finish metaphors several times; varying helps.)

- **[safe]** The closing "Plain-language operating distinction" block is good and on-target. One tighten:
  Before: "It creates the room, cadence, decision rights, and sustainment commitments that allow agencies to ship together."
  After: "It creates the room, cadence, decision rights, and commitments that let agencies ship together."
  ("sustainment commitments" + "allow" → "commitments" + "let".)

---

## on-innovation-and-civic-design.md

**Assessment:** The longest letter and mostly strong — the "residents do not experience government as an organization chart; they experience it as a journey" opening is the best hook in the set. But it sprawls: several sections make the same point (services fail in the seams; design tells the truth; launch isn't success), and "Leadership is design / Leadership, at its best, is design" is the one place the prose turns a little sermon-y. Tightening length would sharpen it.

- **[judgment]** Length/redundancy. Three sections — "Civic design is how we tell the truth about a service," "We map the system end to end," and parts of "Why the Innovation Lab exists" — circle the same insight (services break in the seams; no one owns the end-to-end experience). Consider merging two of them. This is the only letter where I'd cut for length. (Owner decides — structural.)

- **[safe]** Heading inconsistency within the page: most H2s are sentence case, but "**Civic design is how we tell the truth about a service**" is rendered as bold text, not an H2, while its neighbors are `##` headings. Promote it to `## Civic design is how we tell the truth about a service` for parity, or demote the others. (Structural consistency.)

- **[safe]** Empty intensifier.
  Before: "Innovation is one of the most overused words in our field."
  After: Keep — accurate and earns the paragraph. No change.

- **[safe]** Slight hype near the close.
  Before: "Civic design helps Baltimore move from fragmented to coordinated, from reactive to proactive, from bureaucratic to human."
  After: Keep one pair, cut one: "Civic design helps Baltimore move from fragmented to coordinated, from reactive to proactive." (The triple parallelism tips toward slogan; two beats land harder than three.)  **[judgment]** (tone).

- **[safe]** Closing paragraph stacks short fragments for effect — mostly works, but the final line piles three adverbial fragments.
  Before: "Not as theater, but as civic design in action. Every day. In every system. For every resident."
  After: "Not as theater, but as civic design in action — every day, in every system, for every resident."
  (Consolidates three sentence-fragments into one cadence; less breathless.) **[judgment]** (tone).

---

## on-performance-management.md

**Assessment:** The best-targeted letter in the set. "Most cities do not fail because they lack data. They fail because the data does not change what anyone does on Tuesday morning" is Bloomberg-grade. Tight, factual, active, specific (names the principal agencies, the pre-memo/post-memo cycle). Almost nothing to fix.

- **[safe]** One near-cliché.
  Before: "When that routine is real, government gets better. When it is not, performance becomes performance art."
  After: Keep — the "performance/performance art" turn is earned. No change.

- **[safe]** Minor tighten.
  Before: "It needs to be reliable." (after "It is unglamorous on purpose. Performance management does not need to be theatrical to be powerful.")
  After: Keep — the short sentence is doing real work. No change.

- **[safe]** Slight abstraction in the close.
  Before: "Performance management is one of the ways a city earns that standing."
  After: Keep. No change.

- This letter is essentially clean. Flagging that I reviewed it line by line and found no required edits.

---

## on-trustworthy-data.md

**Assessment:** Strong and policy-literate. Handles AI without hype — "If the underlying data is messy, the model will simply make messy conclusions faster" is exactly right. The "graveyard of stale files" line is vivid. One or two sentences run long, and the opening paragraph is a touch abstract before it gets concrete.

- **[safe]** Abstract opener; the concrete version is one paragraph down. Consider leading with the concrete.
  Before: "Every generation of city government faces a test. For this generation, one of the clearest tests is whether we can use technology, data, and artificial intelligence in ways that make government more effective without losing the public trust that makes government legitimate."
  After: "Every generation of city government faces a test. Ours is whether we can use data and artificial intelligence to make government more effective without losing the public trust that makes government legitimate."
  (Tightens a 38-word sentence; drops "technology, data, and" triple to the two that carry the paragraph.) **[judgment]** (light).

- **[safe]** Long sentence with a clause pile-up.
  Before: "It shows up in 311 service requests, permit applications, fire and EMS calls, water accounts, code inspections, work orders, budgets, grants, parks, streets, and neighborhood conditions."
  After: Keep — the inventory is deliberate and concrete, the same device the AdminOps letter uses well. No change.

- **[safe]** "ripple outward" is mild filler.
  Before: "When that data is incomplete, inconsistent, or hard to access, the consequences ripple outward."
  After: "When that data is incomplete, inconsistent, or hard to access, the costs add up."

- **[safe]** Wordy hedge.
  Before: "So our first responsibility is not to chase the newest tool. Our first responsibility is to build the conditions under which new tools can be used responsibly:"
  After: "So our first responsibility is not to chase the newest tool. It is to build the conditions for using new tools responsibly:"

- **[safe]** "rules of the road" appears here and the same metaphor logic ("guardrails") stacks in one paragraph.
  Before: "Governance should not be a wall that blocks progress. It should be a set of guardrails that lets us move faster because we know the rules of the road."
  After: "Governance should not be a wall that blocks progress. It should be guardrails that let us move faster because we know the rules."
  (Trims the doubled metaphor.)

---

## Summary of recommendation counts

- **[safe]:** 28
- **[judgment]:** 11
- Pages with zero required edits: `letters-from-the-director/index.md`, and `on-performance-management.md` (clean line by line).
- Highest-impact single change: convert the all-caps H2s and deck-caption pairs in `mission-vision-identity.md` and `operating-principles-and-culture.md` to match the sentence/title-case, plain-prose register of the letters. That one move closes most of the tonal gap in the section.
