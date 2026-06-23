# Copy Review — `docs/about-us/our-teams/`

**Reviewer:** Senior editor (comprehensive line-by-line read)
**Date:** 2026-06-23
**Style target:** Bloomberg + Harvard Kennedy School — crisp, factual, active voice, concrete nouns and verbs; authoritative, plain, policy-literate, human; short declarative sentences; specifics over adjectives.
**Scope:** 20 files — the four teams (about / strategy / theory-of-change / section index for each), the section index, plus the Cross-Agency Delivery service-definition page.

**Conventions used below**

- **[safe]** = clear, low-risk wording fix that preserves meaning.
- **[judgment]** = changes meaning, tone, or structure; owner decides.
- The `**Term** — definition` em-dash pattern in bulleted lists and "Read alongside" blocks is accepted house style and is **not** flagged. Only prose-flow em-dash overuse is flagged.
- No recommendation breaks links, `{{ macros }}`, heading anchors, taxonomy words, "Cross-Agency Delivery", names, titles, PINs, or legal citations.

---

## Section-level findings (consistency across the four siblings)

These four team pages should read as parallel siblings. They mostly do, but there is real structural and voice drift worth naming before the page-by-page notes.

1. **The About pages are two different documents wearing the same hat.** Performance, AdminOps, and Data and Analytics About pages run long, with a fixed heading spine (`What this service is for` / `Who we are` / `What we do` / `Why it matters` / `How we work` / `What we own` / `What we do not own` / `How we partner across OPI` / `What success looks like` / `Common outputs`). The **Innovation Lab About page is a stub** by comparison: same heading spine but one or two sentences per section, no `Common outputs`, no closing pull-quote, no `Read alongside` block, and no `page_header` sub-title lines (the italic tagline + "Read alongside" + "This About doc explains…" triplet that the other three all carry). A reader moving across the four feels the Lab page as thin and unfinished. **Recommendation [judgment]:** bring the Innovation Lab About page up to sibling depth, or accept it as deliberately lean and trim the other three toward it — but pick one standard.

2. **The strategy pages don't share a skeleton.** Performance and (loosely) Data/Innovation strategies open with framing prose before `EXECUTIVE SUMMARY`; AdminOps strategy jumps straight to `EXECUTIVE SUMMARY` with no tagline triplet. Performance, Data, and Innovation strategies carry `THE CASE FOR CHANGE → NORTH STAR → GUIDING PRINCIPLES → … → FY27 PRIORITIES → CLOSING`. AdminOps strategy is a short 8-section doc with none of those movements. That asymmetry is partly justified (AdminOps is an internal backbone, not a citywide service), but the **AdminOps strategy reads as a different genre** — flag for the owner to decide whether that's intentional.

3. **The Theory-of-Change pages are the most consistent of the three tiers** — the recent normalization shows. All four share `NORTH STAR → 1. Service overview → 2. Operating scope → 3. Engagement model → 4. Theory of Change → 5. Governance → 6. Core offerings → 7. Metrics → 8. Handoffs → Appendix`. Two drifts remain: (a) Performance and Data ToC pages carry the italic `*Full ownership / partnership / referral patterns are detailed in the About doc…*` boundary note; AdminOps and Innovation ToC pages do not. (b) AdminOps and Innovation ToC pages use `In scope / Out of scope (we partner or refer)`; Performance and Data use `In scope for this cost center / Routed elsewhere`. Pick one label pair across all four. **[judgment].**

4. **House terminology drifts between `&` and `and`.** The Performance and Data **strategy** pages use ampersand "Data & Analytics" throughout; every other page (Abouts, ToCs, indexes) uses "Data and Analytics." Same service, two renderings. Standardize on the spelled-out "and" to match the section's dominant style. **[safe]** (does not touch links or anchors — these are body-text mentions).

5. **The "disciplined, humane, learning-oriented" triad is load-bearing across Performance and Innovation** and reads as a shared OPI voice — good. But both then unpack it with the same `Disciplined because… Humane because… Learning-oriented because…` paragraph. Verbatim parallelism across two siblings is fine as house cadence; just confirm it's intentional rather than copy-paste.

6. **"What we heard / what we changed" / "What we heard, what we have aligned on"** appears as a recurring motif (AdminOps ToC, Cross-Agency Delivery). Consistent and good.

---

## `index.md` (Our Teams section index)

**Assessment.** Tight, plain, and well-pitched. The taxonomy explainer in line 11 does real work in few words. Voice hits the target. Only minor drag from one abstract phrase and one slightly mushy sentence.

- Line 3 (blockquote): "The four teams inside OPI and the cross-agency service that runs across all of them." — clean. No change.
- Line 15: "covers what the team is for and how it works **in spirit**" → "covers what the team is for and how it works." **[safe]** — "in spirit" is vague filler against a concrete companion clause about scope/governance.
- Line 13: "It prevents Cross-Agency Delivery from being described like a staffed team, keeps CitiStat from being treated as all of performance management, and keeps the Innovation Lab from becoming a catch-all for any special project." — strong, concrete, keep. (Note: heading anchor `how-to-read-the-team-pages` here vs. the Performance index linking to `#how-to-read-the-portfolio-pages` — see Performance index note 1; not a copy issue but flag for the owner.)

---

## `directors-office/index.md`

**Assessment.** Functional and clear. Slightly list-heavy in the roster sentence but acceptable for an index. Voice is on target.

- Lines 5–9: "The Director's Office sets direction, manages executive coordination, and runs the operational backbone of OPI." — good active opening. Keep.
- Line 3 (blockquote) and line 5 both say "runs the operational backbone of OPI" within four lines. **[safe]** — vary one: e.g., blockquote keep "runs the operational backbone," body → "The Director's Office sets direction, coordinates executive work, and owns the AdminOps function beneath it."

---

## `directors-office/about-admin-ops.md`

**Assessment.** Mostly strong and human, but the longest and most abstract of the About pages. Several sentences lean on metaphor ("operating system," "connective tissue," "operating backbone") stacked close together, and a few intensifier/negation patterns ("is not overhead," "is not bureaucracy," "is not spin") repeat as a tic. Trim the metaphors and the doc gets crisper without losing warmth.

- Line 7: "*The operating backbone that keeps OPI aligned, coordinated, resourced, and credible.*" then line 17: "AdminOps keeps OPI aligned, coordinated, resourced, documented, and understood." then line 21: "It is the operating system that lets a small, multidisciplinary office…" — three near-restatements of the same idea in 15 lines. **[judgment]** — keep the tagline, keep one body statement, cut the redundancy.
- Line 21: "AdminOps is not overhead. It is the operating system that lets a small, multidisciplinary office deliver citywide work with discipline and credibility." → "AdminOps is not overhead. It is the discipline that lets a small, multidisciplinary office deliver citywide work credibly." **[judgment]** — "operating system" is the third backbone metaphor; demoting it tightens the rhythm.
- Line 29: "We keep the office moving without letting it become chaotic." → "We keep the office moving without letting it slide into chaos." **[safe]** — minor; "become chaotic" is flat.
- Line 29: "make sure work does not disappear when a meeting ends or a person changes roles." — concrete and good. Keep.
- Line 63: "AdminOps creates the shared standards that make OPI reliable. **Clarity is not bureaucracy. Clarity protects people, quality, and impact.**" — the "Clarity is not bureaucracy / Clarity protects…" couplet also appears as the pull-quote in the AdminOps ToC (line 15 there). Fine as a deliberate refrain; confirm intentional.
- Line 67: "We make the work **legible**." → "We make the work easy to follow." **[judgment]** — "legible" is mild jargon for a public audience; it recurs (line 61-style "navigating ambiguity" too). If "legible" is house voice, keep; otherwise plain it down.
- Line 71: "We help OPI say yes responsibly and no on purpose." — punchy, on-brand. Keep.
- Line 73: "Communications is not spin. It is how OPI explains what changed, what we learned, what remains hard, and what comes next." — good, keep. (Third "X is not Y" in the doc; see tic note above — consider varying one.)
- Line 61: "every request has a different intake path, every project has a different status format, every briefing starts from scratch, every folder becomes its own filing system, every public artifact carries risk, and staff spend too much time navigating ambiguity." — strong cumulative sentence, but six clauses is long. **[safe]** — cut to four of the strongest (e.g., drop "every folder becomes its own filing system" and "navigating ambiguity") for punch.
- Line 121 / 135 / 147 (italic operating-rule notes): clear, keep.

---

## `directors-office/admin-ops-strategy.md`

**Assessment.** The crispest strategy page in the set — short, declarative, almost no filler. "Documented over heroic" and "ships reliably vs. runs on heroics" land exactly on the Bloomberg target. The main issue is genre drift from its siblings (see section finding 2), not prose quality.

- Line 7: "A team that asks city agencies to operate with discipline must hold itself to the same standard. AdminOps is how OPI does that." — excellent, keep.
- Line 15: "It is the difference between a team that ships reliably and one that runs on heroics." — keep.
- Line 34: "Documented over heroic. Processes that survive leadership transitions. A single front door beats freelance project starts. Investment in OPI's own operations returns time to the citywide services." — strong telegraphic posture lines; keep. Only nit: "freelance project starts" is slightly cute; **[safe]** alt "ad-hoc project starts" if a plainer register is wanted.
- No AI-tells, no passive drift, no hype. Clean page.

---

## `directors-office/admin-ops-theory-of-change.md`

**Assessment.** Consistent with the ToC template and clear. Tables carry most of the load well. Prose is sparse and factual — on target. A couple of stock metaphors and one cliché to flag.

- Line 11 (NORTH STAR): "**A small office that runs like a well-oiled machine.**" → consider "**A small office that runs on routines, not heroics.**" **[judgment]** — "well-oiled machine" is a cliché; the suggested replacement reuses the doc's own (stronger) heroics framing.
- Line 84 (Impact row): "The operating model is the product." — crisp and memorable. Keep.
- Line 15 pull-quote duplicates the About page couplet — see About note; fine as refrain.
- Section 5 governance table is solid. No passive-voice problems. No change.

---

## `performance/index.md`

**Assessment.** Information-dense and accurate, but the longest of the four team indexes and slightly overloaded — it re-explains the team/program distinction three times (intro, "The CitiStat program," "A note on language"). Voice is right; the drag is repetition, not register.

- Line 31: links to `../index.md#how-to-read-the-portfolio-pages`, but the Our Teams index heading is `## How to read the team pages` (anchor `how-to-read-the-team-pages`). **This anchor likely 404s.** Flag for the owner — do **not** silently rewrite, since I was told not to break anchors; the fix is to point at the correct existing anchor `#how-to-read-the-team-pages`. **[judgment / owner verify].**
- Lines 7, 15–17, 29–31: three passes at "Performance is the team; CitiStat is the program." **[judgment]** — keep the crisp line 7 statement; consider folding "The CitiStat program" section and "A note on language" into one shorter block to stop the loop.
- Line 9: "The goal is not more meetings; it is clearer ownership, faster decisions, and measurable improvements." — strong, keep. (This "goal is not more meetings" line recurs across Performance pages — intentional refrain, fine.)
- Line 5: "owns Baltimore's executive performance rhythm: how priorities become measures, how leaders see what is working and what is stuck, and how commitments turn into measurable service improvements." — good concrete opening. Keep.

---

## `performance/about-performance.md`

**Assessment.** The strongest About page for voice — human, candid, concrete ("We are not auditors," "broken promise," "performance theater"). It earns its length. A few intensifiers and one long question-chain are the only drags.

- Line 27: "We help agencies and leadership focus on the right questions: What are we trying to improve? What does the data show? What is causing the problem? Who owns the next step? What decision is needed? How will we know whether anything changed?" — six stacked questions. **[safe]** — effective but long; trim to four for pace, or keep if the cadence is deliberate.
- Line 29: "We are not auditors. We are not here to surprise agencies, embarrass teams, or create performance theater." — excellent, keep.
- Line 53: "City government does not improve because someone reports on a problem. It improves when the problem is defined clearly, the right people are in the room, the right data is trusted, commitments are assigned, and follow-up continues until conditions change." — strong, keep.
- Line 55: "Residents benefit when service issues are identified earlier, bottlenecks are addressed faster, and agencies build routines…" — mild passive cluster ("are identified," "are addressed"). **[safe]** → "Residents benefit when the City spots service issues earlier, clears bottlenecks faster, and agencies build routines…" Tightens to active voice.
- Line 59: "We work through a disciplined but humane performance cycle." — good. Keep.
- Line 155: "priority services show improvements residents can feel, and performance plans become living management tools rather than annual paperwork." — concrete and good. Keep.
- No AI-tells. Em-dash prose flow is controlled. This page is close to finished.

---

## `performance/performance-strategy.md`

**Assessment.** Authoritative and well-structured; the strongest long-form strategy doc. Reads like a real policy strategy, which is the target. Drags: a handful of abstract openers, a couple of triadic-intensifier sentences, and some length in the principle explanations. No AI-tells of note.

- Line 28: "Baltimore City is rebuilding performance management as a citywide operating system, not a reporting exercise." — strong thesis. Keep.
- Line 32: "It helps government see reality clearly, act on the evidence, and keep improving. It is also a trust discipline." — good, keep.
- Line 38: "When these services work, government earns trust. When they fail repeatedly, residents do not experience a single failed metric. They experience a broken promise." — excellent, keep.
- Line 40: "A current performance system has to account for cross-agency work, digital service expectations, data quality, AI readiness, resident experience, equity, and the need to connect performance to budget." → "A modern performance system has to account for…" **[safe]** — "current performance system" is ambiguous (current as in present-day, or the existing one?); "modern" is what's meant and matches line 260's "modern government."
- Line 42: "Too often, goals, measures, meetings, budgets, dashboards, and improvement projects operate in parallel." — good. Keep.
- Line 109: "The purpose is to help agencies manage their work, not create a compliance document that sits on a shelf." — concrete, keep.
- Line 117: "The goal is not more meetings. The goal is clearer ownership, better decisions, and measurable improvements." — recurring refrain; fine.
- Line 174: "The budget is one of Baltimore's most powerful performance tools." — good plain opener. Keep.
- Line 184: "The public story should avoid **triumphalism**. It should build trust through candor, specificity, and evidence of follow-through." **[safe]** — "triumphalism" is slightly elevated for a public audience; alt "The public story should avoid overclaiming." Keep "candor, specificity, evidence of follow-through" — it's strong.
- Line 260: long closing sentence "It honors the City's CitiStat legacy while updating it for a modern government that must manage data, digital services, cross-agency delivery, public trust, and fiscal stewardship at the same time." — five-item tail. **[safe]** — trim to three or break the sentence.

---

## `performance/performance-theory-of-change.md`

**Assessment.** Dense, accurate, and well-aligned to the ToC template; the tables do the work. Prose is minimal and factual — on target. Only nits are one passive construction and one abstract noun phrase.

- Line 17 (NORTH STAR italic): "non-punitive, evidence-driven, and relentless about follow-through. Method, governance, and measurement detail follows." — "detail follows" is a slightly clipped house tag (recurs in Data ToC line 17). Fine; consistent.
- Line 81 (Impact): "An institutionalized culture of continuous improvement that survives leadership changes, retires chronic problems, and earns resident trust through visible, sustained results." — "institutionalized culture of continuous improvement" is the most abstract phrase in the doc. **[judgment]** → "A culture of continuous improvement that outlasts leadership changes, retires chronic problems, and earns resident trust through visible results." Drops the jargon and the redundant "sustained results."
- Line 79 (Outcomes 0–6 mo): "leadership time focused on the bottlenecks that matter most" — good and concrete. Keep.
- Governance and offerings tables: clean, no passive drift. No change.

---

## `data-and-analytics/index.md`

**Assessment.** Clear and concrete. "It turns administrative data into shared, reusable assets that every other OPI service can run on" lands well. On target.

- Line 5: "The Data and Analytics team builds the data foundation that makes OPI's work trustworthy and useful." — good active opener. Keep.
- Line 5: "It owns data governance and quality, analytics and insight products, data engineering and the data platform, open data, and GIS." — fine. Keep.
- No filler, no AI-tells. Minimal changes needed.

---

## `data-and-analytics/about-data-analytics.md`

**Assessment.** Solid and human, with strong civic framing ("We are translators," "civic infrastructure"). Slightly leans on the "we are not just X" / "Data is not Y" negation pattern (same tic as the AdminOps page). One stacked-metaphor passage and a couple of abstractions to tighten.

- Line 21: "The work is both technical and civic. It is about pipelines, dashboards, open data, GIS, data governance, AI readiness, and analytics. It is also about trust, accountability, and making sure the City can explain what it knows and how it knows it." — the closing "what it knows and how it knows it" is sharp; keep. Middle list is long but acceptable.
- Line 29: "We are translators. We translate between agencies and BCIT, between raw data and policy decisions, between technical systems and public meaning, and between what a dashboard shows and what leaders need to do next." — four "between" pairs; effective but long. **[safe]** — trim to three.
- Line 31: "We are not just a dashboard team. We build the conditions that make dashboards trustworthy." — keep, good.
- Line 61: "Data is not a side function. It is civic infrastructure." and line 63 "When this team succeeds…" — keep; concrete payoff follows.
- Line 59: "Performance routines fail when agencies use different numbers. Delivery work stalls when data cannot show whether conditions changed. Innovation work suffers when products are built on unstable datasets. Public trust erodes when residents, Council, researchers, and journalists cannot verify what the City reports." — strong four-beat parallel. Keep.
- Line 72: "Methodology is not paperwork after the work. It is part of the work." — keep, crisp.
- Line 171 closing pull-quote: "trustworthy enough to manage with, transparent enough to share, and useful enough to change decisions." — strong triad, keep.
- Overall: this page's negation pattern ("We are not just…", "Data is not…", "Methodology is not…") echoes AdminOps. **[judgment]** — across the two pages, vary one or two so it doesn't read as a formula.

---

## `data-and-analytics/data-analytics-strategy.md`

**Assessment.** Strong and confident; "Build once, reuse many times" and "A city cannot manage what it cannot trust" are exactly the register. Main issues: the ampersand "Data & Analytics" (section finding 4) and a few hype-adjacent lines. Otherwise on target.

- Throughout: "Data & Analytics" (ampersand) vs. the spelled-out "Data and Analytics" everywhere else in the section. **[safe]** — standardize to "and" in body prose. (Lines 15, 24, 73, 76, 81, 89, 110, 198, etc.)
- Line 33: "A city cannot manage what it cannot trust." — keep, excellent.
- Line 37 (blockquote): "AI without data stewardship is risk without value." — crisp, keep.
- Line 91 (blockquote): "Five intake questions: What decision will this support? Who will use it? Can it be reused? What data quality or governance risk exists? Who will sustain it after the first release?" — good, keep. (Parallel to the Lab's "Five Lab intake questions" — nice cross-page consistency.)
- Line 140: "The standard is not whether the technology is impressive. The standard is whether it improves a real decision or service while protecting residents and public trust." — keep, on-target.
- Line 196: "When the foundation is strong, every agency can move faster with more confidence. When it is weak, every improvement effort starts over." — keep, good.
- Line 19: "Without strong data stewardship, every other OPI service is weaker." — fine, but "weaker" is soft; **[safe]** alt "every other OPI service rests on sand" is too cute — keep as-is, low priority.
- No AI-tells. Em-dash prose flow controlled.

---

## `data-and-analytics/data-analytics-theory-of-change.md`

**Assessment.** Consistent with the ToC template; tables carry it. Factual and clean. Almost nothing to flag — among the most finished pages in the set.

- Line 17 (NORTH STAR italic): mirrors the Performance ToC tag "…detail follows." Consistent, fine.
- Line 79 (Impact): "Baltimore runs on trustworthy, well-governed data. Decisions are evidence-based by default. The public can verify what the City reports. Agencies see data as shared infrastructure, not a one-off favor." — strong four-beat. Keep.
- Section 5 governance, section 6 SLAs: clean, no passive drift. No change.
- Note the `Routed elsewhere` / `In scope for this cost center` labels here vs. Innovation/AdminOps `Out of scope` / `In scope` — see section finding 3.

---

## `innovation-lab/index.md`

**Assessment.** Crisp and well-pitched — the "craft of solving" framing is distinctive and earns its place. On target. One long opening sentence is the only drag.

- Line 5: "It owns the craft of solving: discovery, service design, user research, product management, prototyping, civic technology, applied AI pilots, and MVP-and-handoff methods." — eight-item list in one sentence. **[safe]** — acceptable for an index, but consider a colon-led break or trimming to the strongest six.
- Line 5: "The Lab can work on one-agency or multi-agency problems." — clear, keep.
- "MVP-and-handoff" appears unglossed here and across Lab pages; for a non-technical public audience MVP may need expansion on first use. **[judgment]** — see About note.

---

## `innovation-lab/about-innovation-lab.md`

**Assessment.** Punchy and readable, but **structurally the outlier** — a stub next to the other three full About pages (section finding 1). The prose that exists is good; the problem is depth and missing template furniture (no tagline triplet, no `Read alongside`, no `Common outputs`, no closing pull-quote). Also the most acronym-dense page for a public audience.

- **Missing furniture [judgment]:** add the `page_header` companion lines the other three Abouts carry — the italic tagline, "*Read alongside: OPI Service Theory of Change — Innovation Lab.*", and the "*This About doc explains the service in plain language…*" line — for sibling parity.
- Line 9: "the **craft of solving**, used to make city services easier to access, track, and complete." — strong, keep.
- Line 17: "**MVP-and-handoff**" and line 17 "prototype a fix in real conditions" — "MVP" is unglossed. **[judgment]** — for a public audience, gloss on first use: "a minimum viable product (MVP) and a clean handoff" or rephrase to "ship a working first version and hand it off."
- Line 21: "Service problems usually look like technology, policy, or staffing problems in isolation. They are usually all three." — excellent, keep.
- Line 25: "Time-boxed, evidence-led, and adoption-first. We design for handoff from day one, test before we scale, and reach for emerging methods like AI only when they solve a real operational problem." — strong, keep.
- Line 47: "Residents can access, track, and complete services more easily; agencies own the improvements after the Lab steps back; a small portfolio of credible, visible wins ships each year." — good, keep. Only nit: "credible, visible wins" stacks two adjectives; **[safe]** drop one ("a small portfolio of visible wins ships each year").
- Compared with siblings, this page has no `What we do not own` partner-philosophy depth, no metrics gesture, no outputs list. Decide depth standard (section finding 1).

---

## `innovation-lab/innovation-lab-strategy.md`

**Assessment.** Confident and well-built — "Innovation as delivery, not theater" is exactly the register and the four commitments are crisp. The longest strategy doc; a few sections (Civic Design as Leadership, Responsible AI) drift slightly toward essayistic abstraction, and there are two near-duplicate Tiger-Team explainer passages. Strong overall.

- Line 14: "**Innovation as delivery, not theater**" — keep, excellent framing (and the closing line 231 "Not as theater, but as delivery" bookends it well).
- Line 20: "start with the service, not the screen; design with users, not for them; build only when build is the right answer; and treat sustainment as the test of success." — crisp four commitments. Keep.
- Lines 130 and 149 and 189–191 and 213–215: the **Innovation Lab / Cross-Agency Delivery relationship is explained four times** (Tiger Team table row, "With Cross-Agency Delivery" section, "Tiger Team usage standard" section, FY27 priority 5). Content is correct each time but the repetition is heavy. **[judgment]** — keep the fullest statement (line 149), compress the others to one-line cross-references.
- Line 149: "The Lab is the capability, the craft team that asks *how do we solve this?* Cross-Agency Delivery owns coordination authority across agencies and asks *how do we get multiple agencies to actually ship this together?*" — "actually" is a filler intensifier. **[safe]** → "…how do we get multiple agencies to ship this together?"
- Line 159: "Leadership, at its best, is design: designing systems that are clear and accountable, teams that know how to work together, routines that create follow-through, and processes that do not break under pressure." — good, but the whole "Civic Design as Leadership" section is the most essayistic in the doc. **[judgment]** — fine to keep as a values statement; just confirm it earns its length against the Bloomberg-crisp target.
- Line 167: "It does not use AI as theater or as a substitute for judgment." — keep.
- Line 229: "A learning government does not confuse activity with impact." — keep, sharp.
- Line 130 (table cell): the Tiger Team `Use when` cell is a 3-sentence paragraph inside a table column — heavy for a table. **[judgment]** — move the charter-routing detail to prose and keep the cell to one line.

---

## `innovation-lab/innovation-lab-theory-of-change.md`

**Assessment.** Aligned to the ToC template and clean; tables carry it. Among the more finished pages. One em-dash-in-prose spot and one passive note.

- Line 19 (Why it matters cell): "Many service problems are not about more staff or more money — they are about how services are designed, delivered, and felt." — the em-dash here is prose-flow, but it's a single instance in a table cell and reads fine. Low priority; leave.
- Line 11 (pull-quote): "We are organized by discipline, but we work as one team. The Innovation Lab turns service problems into practical solutions." — keep.
- Line 25: "*The Innovation Lab is the official service name.*" — slightly orphaned standalone italic line; **[safe]** consider folding into the `What it is` cell or the overview, since it currently floats below the table with no surrounding context.
- Lines 139–143 ("Relationship to Cross-Agency Delivery and Tiger Teams"): correct, but this is the **fourth or fifth** restatement of the same relationship across the Lab pages and the CAD page. **[judgment]** — keep one canonical version (likely on the CAD service-definition page) and cross-reference rather than restate.
- Section 6 SLA table, section 7 metrics: clean. No change.

---

## `innovation-lab/cross-agency-delivery-service-definition.md`

**Assessment.** The most complete single service document in the set — it correctly carries both the About-style "purpose and philosophies" prose and the ToC-style tables, which fits its role as the canonical definition. Voice is strong and the "overlay, not a team" guardrail is repeated deliberately and well. Drags: some prose-flow em-dashes, a couple of long table cells, and the recurring metaphor density.

- Line 9: "Cross-Agency Delivery is a service overlay: a coordinating service that runs across the four teams rather than a standalone team with its own staff and budget." — excellent, load-bearing, keep.
- Line 11 (blockquote): "Performance management often fails because the people in the room can analyze the problem but cannot change the conditions that produce it. Delivery is where conditions change." — keep, strong.
- Line 33: "Delivery is where conditions change. Stat surfaces the problem; delivery resolves it." — this "delivery is where conditions change" line appears three times (lines 11, 33, plus "Delivery is what changes the conditions" in the Performance strategy line 166). **[judgment]** — refrain is fine within this page; just confirm intentional.
- Line 35: "Communities feel the failure of coordination. They do not care which agency owns what. They want the service to work." — keep, excellent.
- Line 42: "Without it, every plan is theater." and line 43 "Tiger Teams over standing committees." — good telegraphic posture lines, keep.
- Line 59: "Short-cycle issues route to Stat, not delivery." — clear, keep.
- Line 76: "If it does not, we use a different routine — a Stat, a product council, a charter and an owner, or a one-time decision memo." — prose-flow em-dash introducing a list; acceptable but **[safe]** could be a colon: "…we use a different routine: a Stat, a product council, a charter and an owner, or a one-time decision memo."
- Line 68 (table cell): "Without an owner, a sequence, and an authorizer, they drift. The Cross-Agency Delivery overlay gives them a home until they are resolved." — "are resolved" passive; minor, leave (table register).
- Line 97 (Deliver row cell): "Run weekly delivery reviews with the SRO and agency owners; track commitments; escalate blockers to the Authorizer; QA before any public release." — dense but parallel and clear. Keep.
- Line 126 (Tiger Team activation `When to use` cell): a 3-sentence paragraph inside a table column (same pattern as the Innovation Lab strategy table). **[judgment]** — compress the cell; move the Innovation-Lab-provides / CAD-provides split to prose if it isn't already stated elsewhere on the page (it is, line 173).
- Line 173 ("Relationship to the Innovation Lab"): canonical and well-placed. Keep this as the single source and trim the duplicate explainers on the Lab pages (see Innovation Lab notes).
- Line 49: "City Hall owns the user experience, OPI owns the data and method, agencies own the workflow, BCIT owns the infrastructure." — crisp ownership line, keep.

---

## Summary of recommendation counts

- **Section-level findings:** 6 (mix of [judgment] consistency calls and 1 [safe] terminology standardization).
- **Page-level [safe] recommendations:** ~17.
- **Page-level [judgment] recommendations:** ~16.
- **Owner-verify flag (possible broken anchor, not a copy edit):** 1 — `performance/index.md` line 31 link to `#how-to-read-the-portfolio-pages`.

The four sibling sets are closest to parity at the **Theory-of-Change** tier and most divergent at the **About** tier (Innovation Lab About is a stub). The prose is generally strong and on-target; the dominant cleanups are (1) trimming repeated metaphors and the "X is not Y" negation tic, (2) standardizing "Data and Analytics" vs. "Data & Analytics," and (3) deduplicating the Innovation Lab / Cross-Agency Delivery relationship explainer, which is restated four to five times across pages.
