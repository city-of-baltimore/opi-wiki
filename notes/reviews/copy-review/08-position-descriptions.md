# Copy Review — Position Descriptions

**Scope:** All 19 position descriptions plus the index, under
`docs/resources/reference/position-descriptions/` (directors-office, performance,
data-and-analytics, innovation-lab). Deep read, every page in full.

**Style target:** Bloomberg + Harvard Kennedy School — crisp, factual, active voice,
concrete nouns and verbs; plain, policy-literate, human. PDs should be parallel in
structure, consistent in voice, and free of HR boilerplate clichés.

**Constraint honored:** No role titles, classifications, PINs, salary/grade, reporting
lines, legal citations, names, links, `{{ macro }}`, or heading anchors were proposed
for change. Prose only. Recommendations only — no files edited.

**Tag key:** `[safe]` = low-risk wording fix preserving meaning. `[judgment]` =
changes meaning, tone, or structure; owner decides.

---

## Section-level consistency findings (apply across the set)

The corpus is, on the whole, strong and notably consistent — a shared 7-section
skeleton (At a Glance → Position Summary → Key Responsibilities → Knowledge, Skills,
and Abilities → Minimum Qualifications → Working Conditions → Supervision), a shared
closing EEO paragraph, and a shared "Supervision given / received" convention. Drift is
mostly at the edges. The findings below recur and are worth fixing globally rather than
page-by-page.

1. **`tiger team` mid-sentence capitalization bug (mechanical, fix everywhere).** Two
   `### Key Responsibilities` subheadings render the literal string "tiger team" with a
   lowercase "t" at the start of a Title Case heading:
   - Project Manager: `### tiger team Coordination and Delivery Support`
   - Innovation Program Manager: `### tiger team and Cross-Agency Delivery`
   These read as typos. **[safe]** Recommend "Tiger-Team Coordination and Delivery
   Support" and "Tiger Teams and Cross-Agency Delivery" (or whatever the house style for
   the term is — but capitalized to match sibling headings). Note: the term is hyphenated
   as "tiger-team" when adjectival elsewhere in the same files, so style is already
   inconsistent within a single page.

2. **"Working Conditions" boilerplate is correctly shared but the 24-hour-callback clause
   drops inconsistently.** Most PDs carry "This position may be required to work evening
   and weekend hours and 24-hour callback in an emergency." Five omit it: Data
   Storyteller, Project Manager, CitiStat Analyst, Senior Performance Analyst, Civic
   Designer, Full Stack Engineer. This may be deliberate (these are the lower-intensity
   roles), but it is worth a deliberate owner decision rather than drift. **[judgment]**
   Confirm the omission is intentional and consistent by role tier.

3. **Curly vs. straight apostrophes split the corpus.** Most files use typographic
   apostrophes (OPI's, Director's). The two `data-and-analytics`/`innovation-lab` Applied
   Data Scientist files and a few clauses use straight ASCII apostrophes ("OPI's",
   "Mayor's", "candidate's"). **[safe]** Normalize to the house standard (the rest of the
   set uses curly). Purely mechanical; no meaning change.

4. **Position Summary length and voice vary by tier — mostly fine, two outliers.** The
   director and deputy summaries are tight and parallel. Two summaries break voice:
   - **Operations Analyst** opens with HR-brochure framing ("high-impact, trusted
     partner… goes well beyond traditional administrative support… show up strong"). It is
     the least Bloomberg/HKS summary in the set.
   - **Data-and-Analytics Applied Data Scientist** is the longest and most résumé-flavored
     ("designed for someone who can move comfortably between…", "A successful candidate
     should be equally comfortable…", closing KSA "Self-starter"). It reads like a job-ad
     rather than a PD.
   See per-page notes.

5. **Heading wording is consistent** across `## Key Responsibilities`, `## Knowledge,
   Skills, and Abilities`, `## Minimum Qualifications`. No structural drift found there.
   The KSA sub-buckets vary in name by role, which is appropriate.

6. **Em-dash use in prose is generally controlled.** The "Supervision given/received"
   table cells and Supervision section use em-dashes structurally to set off the list of
   reports — that is correct and flagged only where prose flow is affected. A few summary
   sentences stack em-dashes; noted per page.

---

## Director's Office

### index.md
**Assessment:** Clear, well-structured directory; reads in-voice and needs little. Not a
PD, so the skeleton checks do not apply.

- "translate the Mayor's priorities into measurable service improvements" — fine as is.
- **[safe]** "the connective tissue between" appears in the Chief of Staff PD, not here;
  index prose is clean. No line-level changes required beyond confirming the curly-quote
  normalization in finding 3.

### pd-executive-director-and-cdo.md
**Assessment:** The strongest summary in the set — authoritative, active, concrete.
Parallel to siblings and on-target. Minimal changes.

- **[safe]** "turns analysis into commitments and commitments into delivered work" →
  fine, but the chained repetition is slightly ornate; acceptable for the top role.
  Optional tighten: "turns analysis into commitments and commitments into delivery."
- **[safe]** "ensure OPI communications are accurate, accessible, and on-message with the
  Mayor's Office of Communications" → "on-message" is mild jargon; "aligned with the
  Mayor's Office of Communications" is plainer. Low priority.

### pd-chief-of-staff.md
**Assessment:** Solid, parallel, in-voice. One filler metaphor and one overstuffed
sentence.

- **[safe]** "The role is the connective tissue between the Executive Director and the
  four service portfolios." → cliché. **before → after:** "The role connects the
  Executive Director to the four service portfolios." (or cut entirely — the prior
  sentence already establishes this).
- **[judgment]** Position Summary paragraph 2 is a single ~70-word sentence chaining
  "manages… directly oversees… oversees… and maintains continuity practices including
  OSHA, COOP, and incident response." Recommend splitting into two sentences for
  readability. **before:** "The Chief of Staff manages the Director's Office staff (…),
  directly oversees the Innovation Program Manager role on behalf of the Innovation Lab,
  oversees personnel, purchasing, and facilities coordination, and maintains continuity
  practices including OSHA, COOP, and incident response." **after:** "The Chief of Staff
  manages the Director's Office staff (…) and directly oversees the Innovation Program
  Manager on behalf of the Innovation Lab. The role also oversees personnel, purchasing,
  and facilities coordination, and maintains continuity practices including OSHA, COOP,
  and incident response."

### pd-data-storyteller.md
**Assessment:** Reads parallel and clean; one self-referential brand claim and a long
opening sentence.

- **[safe]** "uphold the Bloomberg/HKS-grade quality bar across deliverables" →
  referencing the house style target inside a public PD is awkward and inside-baseball.
  **before → after:** "uphold OPI's publication quality bar across deliverables." Keeps
  meaning, drops the self-referential brand name.
- **[judgment]** Position Summary is one ~95-word sentence ("The position prepares…,
  supports…, and works with the four teams to translate…"). Recommend a sentence break
  after "OPI's reach." for readability. The content is good; the packaging is dense.

### pd-operations-analyst.md
**Assessment:** Weakest summary in the set against the target — it leans on HR-brochure
hype where the sibling PDs state work plainly. Body and KSAs are fine. Recommend a summary
rewrite for voice parity.

- **[judgment]** "The Operations Analyst is a high-impact, trusted partner to the
  Executive Director and the Director's Office. The role goes well beyond traditional
  administrative support:" → hype + defensiveness. **before → after:** "The Operations
  Analyst is a trusted partner to the Executive Director and the Director's Office,
  protecting and amplifying the Executive Director's capacity through a disciplined
  calendar and briefing system." Drops "high-impact," "goes well beyond traditional
  administrative support."
- **[safe]** "ensure the Executive Director has the prep time needed to show up strong."
  → "show up strong" is colloquial filler. **before → after:** "ensure the Executive
  Director has the prep time needed for each engagement."
- **[safe]** "recommend 'yes,' 'not now,' or 'delegate.'" → fine and concrete; keep.
- **[safe]** "anticipate and resolve conflicts before they escalate" → mild filler;
  "anticipate and resolve scheduling conflicts" is tighter. Low priority.
- **[judgment]** KSA "ability to produce briefing packets and decision memos at speed and
  at a high quality bar" → "at speed and at a high quality bar" is loose. **before →
  after:** "ability to produce briefing packets and decision memos quickly and to a high
  standard."

### pd-project-manager.md
**Assessment:** Parallel and in-voice apart from the `tiger team` heading bug (finding 1).
Summary is good.

- **[safe]** `### tiger team Coordination and Delivery Support` → `### Tiger-Team
  Coordination and Delivery Support` (capitalization; see finding 1).
- **[safe]** "ensure that priorities are tracked, risks are surfaced early, and
  commitments translate into timely delivery." → light passive stack. **before → after:**
  "track priorities, surface risks early, and turn commitments into timely delivery."
  Active and parallel to the verbs around it.
- **[safe]** "decision-ready" / "RAG definitions" — RAG (red/amber/green) is unexplained
  jargon. **[judgment]** Consider "status-color (RAG) definitions" on first use, or spell
  it out, for the non-PM reader.

### pd-citistat-inspector.md
**Assessment:** Concrete, operational, well-matched to the role; one of the cleaner
field-role PDs. No hype.

- **[safe]** "to keep the office running smoothly." → mild filler tail. **before →
  after:** "to keep the office running." or cut "smoothly." Low priority.
- No HR clichés or AI-tells found. Heading set and Supervision block are correct.

---

## Performance

### pd-deputy-chief-performance-officer.md
**Assessment:** Strong, parallel to the other deputy PDs, active voice. Minor wordiness.

- **[safe]** "The DCPO leads a team of civic-minded analysts who gather and analyze data
  from city agencies to assess performance, identify operational challenges, and
  collaborate on solutions." → "civic-minded" is soft editorializing inside a duties
  statement. **before → after:** "The DCPO leads a team of analysts who gather and analyze
  agency data to assess performance, identify operational challenges, and develop
  solutions." ("collaborate on solutions" → "develop solutions" is firmer.)
- **[safe]** "Optimize the CitiStat program for consistent stakeholder engagement…" →
  "optimize" is vague consultant-speak. **before → after:** "Run the CitiStat program for
  consistent stakeholder engagement, planning, deliverables, data use, and program
  evaluation." (Same verb fix applies to the CitiStat Program Manager PD below.)
- **[safe]** KSA "Ability to run high-signal CitiStat sessions" → "high-signal" is jargon.
  **before → after:** "Ability to run focused CitiStat sessions that convert analysis into
  commitments…"

### pd-citistat-program-manager.md
**Assessment:** Parallel and capable; carries the corpus's one true HR cliché
("fast-paced") and a vague "optimize."

- **[safe]** KSA "Ability to coach, support, and collaborate with a team of analysts in a
  fast-paced, public-sector environment." → "fast-paced … environment" is the exact
  boilerplate the target bans. **before → after:** "Ability to coach, support, and
  collaborate with a team of analysts in a demanding public-sector environment." (or drop
  the qualifier entirely: "…with a team of CitiStat analysts.")
- **[safe]** "Optimize the CitiStat operating process: intake, topic calendar…" → as
  above, **before → after:** "Run and improve the CitiStat operating process: intake,
  topic calendar, planning, deliverables, data use, and follow-through."
- **[safe]** "The Program Manager is a champion of data-driven decision-making, process
  improvement, and transparency." → "champion of" is hype filler. **before → after:** "The
  Program Manager advances data-driven decision-making, process improvement, and
  transparency." Low priority; acceptable as is.
- **[safe]** "ensuring sessions are structured, impactful, and aligned with city
  priorities." → "impactful" is hollow. **before → after:** "ensuring sessions are
  structured, decision-focused, and aligned with city priorities."

### pd-citistat-analyst.md
**Assessment:** Among the best-written individual-contributor PDs — opens with a crisp
definition of CitiStat, states the work plainly. Parallel. Minimal changes.

- **[safe]** Position Summary closes "The position reports to the Deputy Chief Performance
  Officer." — this duplicates the At-a-Glance and Supervision blocks and reads as a
  tacked-on fragment. **before → after:** delete the sentence (reporting line is stated
  twice already). **[judgment]** if owner prefers the in-summary cue for parity with the
  deputy PDs, keep but it is redundant.
- No hype or AI-tells. The four-tenet CitiStat phrasing is consistent with the Senior
  Performance Analyst PD — good.

### pd-senior-performance-analyst.md
**Assessment:** Clear, parallel, product-owner framing is concrete. On-target.

- **[safe]** "leads one or more CitiStat topics in the same way a CitiStat Analyst does:
  framing the problem, building the analytic baseline, preparing the session, and
  following through on commitments." → good, keep. Parallel to the Analyst PD.
- No clichés or hype found. Only the shared curly-quote / callback-clause items
  (findings 2–3) apply.

---

## Data and Analytics

### pd-deputy-chief-data-officer.md
**Assessment:** Strong and parallel to the other deputy PDs; one hype word in the KSAs.

- **[safe]** KSA "Visionary leadership in data governance, AI, analytics, and digital
  platforms." → "Visionary" is hype and unmeasurable. **before → after:** "Proven
  leadership in data governance, AI, analytics, and digital platforms." (the next bullet
  already says "Deep expertise," so "Proven" avoids repetition).
- **[safe]** "building toward trusted, transparent, and responsible data infrastructure."
  → fine; "building toward" is slightly soft. Optional: "to build trusted, transparent,
  and responsible data infrastructure."
- **[judgment]** "integrate information from all sources to communicate a well-informed,
  diverse perspective." → this last bullet of "Stewardship and Operations" is abstract and
  off-voice next to the concrete bullets above it. Consider cutting or grounding it; it
  reads like inherited classification boilerplate.

### pd-applied-data-scientist.md (Data and Analytics)
**Assessment:** The richest content in the set, but the **longest and most job-ad-flavored
summary** — it breaks PD voice with second-person-ish candidate framing and closes the
KSAs on a banned cliché. Recommend tightening the summary and the final KSA for parity.
Body responsibilities are excellent and concrete.

- **[judgment]** Summary ¶2: "This role is designed for someone who can move comfortably
  between messy city datasets, operational field realities, and executive
  decision-making. A successful candidate should be equally comfortable sitting with
  program staff…, writing SQL or Python…, developing models…, and translating findings…"
  → this is recruiting-brochure voice, not a PD. **before → after:** "The role moves
  between messy city datasets, operational field realities, and executive
  decision-making: sitting with program staff to learn how a service works, writing SQL or
  Python to investigate the data, building models or geospatial analyses where
  appropriate, and translating findings into clear guidance, reusable tools, and
  follow-through." Removes "designed for someone who," "A successful candidate should be
  equally comfortable."
- **[safe]** Final KSA bullet: "Self-starter with a commitment to continuous learning,
  stakeholder partnership, documentation, follow-through, and delivering tangible impact
  through data." → "Self-starter" and "delivering tangible impact" are the exact banned
  clichés. **before → after:** "Commitment to continuous learning, stakeholder
  partnership, documentation, follow-through, and measurable results." Drops "self-starter"
  and "tangible impact."
- **[safe]** "prioritizing practical impact over methodological formality" appears twice
  in spirit (responsibilities + KSAs). Fine once; watch the duplication.
- **[safe]** Straight apostrophes throughout ("OPI's", "Mayor's") — normalize per finding
  3.
- **[safe]** "Apply iterative, Agile-style approaches to analytical and product work:
  moving quickly, learning from stakeholder feedback, refining continuously, and
  prioritizing practical impact over methodological formality." → wordy. **before →
  after:** "Work iteratively: move quickly, learn from stakeholder feedback, and prioritize
  practical impact over methodological formality."

### pd-principal-data-engineer.md
**Assessment:** Concrete, senior, in-voice. One inherited-boilerplate sentence and a small
redundancy.

- **[safe]** "These platform responsibilities are consolidated into this role." → reads as
  an internal org note dropped into prose. **before → after:** fold into the prior clause
  or cut; the sentence before already says the role "owns the cloud platform, security
  baselines, and CI/CD." **[judgment]** if the "consolidated" signal matters for HR/comp,
  keep but move to a footnote-style aside.
- **[safe]** "Develop data models, lakehouse-style tiered layers, and orchestration
  frameworks that work for efficient computation, fellow engineers, and data consumers."
  → "that work for" is vague. **before → after:** "…that serve efficient computation,
  fellow engineers, and data consumers." (The Senior Data Engineer PD uses "that make
  sense for" for the same line — pick one phrasing across the two engineer PDs for
  parallelism.)

### pd-senior-data-engineer.md
**Assessment:** Clean, appropriately scoped down from the Principal PD, parallel. Minimal.

- **[safe]** "orchestration frameworks that make sense for efficient computation, fellow
  engineers, and data consumers." → align verb with the Principal PD (see above); "make
  sense for" → "serve."
- No hype or clichés. Good parity with its sibling.

### pd-technical-program-manager.md
**Assessment:** Crisp, concrete, well-structured; arguably the cleanest TPM/PM-style PD.
On-target. Very minor.

- **[safe]** "The TPM makes sure the team ships reliable increments on a predictable
  cadence with acceptance evidence and stable operations, and measures impact
  post-release, including data quality, adoption, and resident value." → one long
  sentence; readable but dense. Optional split after "stable operations."
- No clichés or AI-tells found.

---

## Innovation Lab

### pd-innovation-program-manager.md
**Assessment:** Strong and parallel; carries the second `tiger team` heading bug and one
clunky "consolidated into this role" aside (mirrors the Principal Data Engineer pattern).

- **[safe]** `### tiger team and Cross-Agency Delivery` → `### Tiger Teams and
  Cross-Agency Delivery` (capitalization; finding 1).
- **[judgment]** "Direct the work of the Civic Designer and carry the Lab's
  civic-technology leadership directly, a scope consolidated into this role, aligning
  design and technology approach with service-delivery realities." → the mid-sentence "a
  scope consolidated into this role" is an org-design aside that interrupts the duty.
  **before → after:** "Direct the Civic Designer's work and lead the Lab's civic-technology
  agenda, aligning design and technology with service-delivery realities." (Same
  consolidation note recurs in the Supervision-given cell; that one is structural and can
  stay.)
- **[safe]** Summary "turns them into tested, adopted solutions" / "framed for adoption
  from day one, evaluated honestly, and either scaled, sustained… or sunset" → good,
  concrete, keep.

### pd-civic-designer.md
**Assessment:** Clean, plain, parallel; one aspirational sentence verging on mission-speak.

- **[safe]** "Embed human-centered design principles in city operations to keep resident
  needs and equity at the heart of all service delivery." → "at the heart of all" is
  hype. **before → after:** "Embed human-centered design in city operations so resident
  needs and equity shape service delivery." Drops "at the heart of all," tightens.
- **[safe]** "helps embed practical, human-centered approaches across city government." →
  "practical, human-centered approaches" partly duplicates the prior sentence. Optional
  trim.
- No banned clichés. Good IC-level voice.

### pd-applied-data-scientist.md (Innovation Lab)
**Assessment:** Notably well-written — the "sits inside service problems" framing is vivid
and the contrast with the Data-and-Analytics Applied Data Scientist is handled cleanly.
Parallel, in-voice, active. Among the best ICs. Minor.

- **[safe]** "It sits inside service problems: understanding how a service actually works,
  investigating the data behind it, prototyping a solution, and helping prove whether the
  solution moves the metric that matters." → strong; keep. "the metric that matters" is a
  touch colloquial but earns its place.
- **[safe]** Straight apostrophes ("team's", "Lab's") — normalize per finding 3.
- **[safe]** "with honest evaluation of accuracy, bias, and fitness for use" → good,
  concrete, keep. No "passionate"/"dynamic"/"self-starter" tells here — cleaner than its
  Data-and-Analytics twin.

### pd-product-engineer-full-stack.md
**Assessment:** Solid and concrete; opens with a redundant self-referential phrase and one
soft value statement.

- **[safe]** "The Full Stack Engineer is a mission-driven full-stack engineer on the
  Innovation Lab, building modern, scalable data products…" → "is a mission-driven
  full-stack engineer" restates the title and adds an unmeasurable adjective. **before →
  after:** "The Full Stack Engineer builds modern, scalable data products on the
  Innovation Lab that power internal decision-making, public engagement, and transparency
  in Baltimore City government." Removes the tautology and "mission-driven."
- **[safe]** KSA "Commitment to public service, equity, and improving government through
  better tools." → acceptable values statement; "improving government through better
  tools" is slightly slogan-like. Optional: "Commitment to public service, equity, and
  better tools for government." Low priority.
- No "fast-paced"/"wear many hats" tells. Heading set correct.

---

## Summary of counts

- **Pages reviewed:** 20 (19 PDs + index).
- **`[safe]` recommendations:** ~30 (incl. 2 global mechanical fixes: `tiger team`
  heading capitalization ×2 pages, curly/straight apostrophe normalization).
- **`[judgment]` recommendations:** ~11 (summary rewrites for Operations Analyst and the
  Data-and-Analytics Applied Data Scientist; sentence splits; "consolidated into this
  role" asides; callback-clause consistency decision; redundant reporting-line line in the
  CitiStat Analyst summary).

## Top themes

1. **The corpus is strong and remarkably parallel.** Most fixes are polish, not repair.
   The director/deputy summaries and the CitiStat Analyst, Innovation-Lab Applied Data
   Scientist, and Technical Program Manager PDs are already on-target.
2. **Two summaries break voice** with recruiting-brochure language: the **Operations
   Analyst** ("high-impact… goes well beyond… show up strong") and the **Data-and-Analytics
   Applied Data Scientist** ("designed for someone who," "A successful candidate should be
   equally comfortable," closing "Self-starter… tangible impact"). These are the priority
   rewrites.
3. **A small set of recurring tells** to sweep: the `tiger team` heading-capitalization bug
   (2 pages), "optimize" as vague verb (2 Performance PDs), "fast-paced environment" (1),
   "champion/visionary/mission-driven/high-signal/impactful" hype words (scattered), the
   "consolidated into this role" org-aside dropped into prose (2 pages), and curly/straight
   apostrophe drift.
