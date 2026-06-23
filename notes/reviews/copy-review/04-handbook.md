# Copy Review — Handbook (`docs/how-we-work/handbook/`)

Senior-editor pass against a Bloomberg + Harvard Kennedy School target: crisp, factual, active, concrete, human. Scope: all 33 `.md` files under `handbook/` (onboarding, administrative-memos, how-to, operations, plus section/group index pages). Every page read in full.

Tags: **[safe]** = low-risk wording fix preserving meaning · **[judgment]** = changes meaning/tone/structure; owner decides.

Constraints honored: no proposed changes to links, `{{ macros }}`, heading anchors, taxonomy words, "Cross-Agency Delivery," names, titles, or legal citations.

---

## Headline findings

1. **The handbook is, on the whole, strong.** The "OPI Foundations" series (onboarding, leadership norms, intake, QA, performance standards, playbook, templates) is consistently crisp, active, and policy-literate — it already hits the target. Most recommendations below are small polish, not rescue.
2. **Two voices coexist, and one is off-brand.** The polished series pages read like one careful editor wrote them. The unstructured how-tos (`book-the-idea-lab-fayette`, `order-food-catering`, `edit-a-past-reporting-period`, `submit-your-weekly-update`) and especially **`git-guide`** read like raw source pasted in. `git-guide` is the single largest outlier: chatty, jokey ("hit by a bus," "Menacingly."), second-person rambling, and far too long for a reference page.
3. **A few factual / structural defects, not just style.** The telework memo contradicts its own dates and title. `leadership-norms` has a broken ordered-list (items numbered 6–12). Two performance pages use bold paragraphs where sibling sections use `###` headings. These hurt credibility more than any adjective does.

---

# Section-level consistency

- **Onboarding** is the most uniform sub-section: each long page carries the `page_header` + `AUDIENCE / OWNER / VERSION` definition block, a Purpose/Principles opener, then tables. Voice is clean and active. `new-hire-announcement-template` is the exception — it mixes `#` and `##` as visual styling (multiple H1s in body) rather than document structure.
- **Administrative memos** correctly preserve memo format (To/From/Cc/Date/Subject). Voice is appropriately formal. The weak spot is `telework-and-in-office-schedule`, which is both the wordiest and the only one with internal factual contradictions.
- **How-to guides** are deliberately two-tier: clean step-based pages (`silence-teams-notifications`, `change-your-city-password`, `add-a-printer`, `create-planner-groups`) vs. lightly-edited source dumps (`book-the-idea-lab-fayette`, `order-food-catering`, `edit-a-past-reporting-period`, `git-guide`). The index promises "step-based, tool-specific, easy to revise" — the dumps don't yet meet that bar. `git-guide` is formatted as an essay, not a guide.
- **Operations** is the strongest and most internally consistent group. Templates, SOPs, norms, and standards share the same definition-block header, the same recurring epigraph (*"Respond when necessary. Build so we do not have to respond again."*), and the same "Owner and review" footer. Minor heading-level inconsistencies are the only blemishes.

---

# Index / section pages

### `handbook/index.md`
Assessment: Tight and scannable. The `Term — definition` bullets are house style and read fine. No changes needed.

### `onboarding/index.md`, `operations/index.md`
Assessment: One-line blockquote summary + card grid. Clean. No changes.

### `administrative-memos/index.md` and `how-to/index.md`
Assessment: Both carry meta-commentary about the *editorial process* ("Draft pages converted from memo-style source documents," "strip out email-style boilerplate") that reads as internal scaffolding rather than reader-facing guidance.

- `administrative-memos/index.md`: "Draft pages converted from memo-style source documents that still need policy review." → "Office memos turned into maintainable, durable guidance." **[judgment]** (the "still need policy review" status may be intentional; owner decides whether to surface it to readers)
- "This subsection turns office memos into maintainable pages. The goal is to keep durable guidance while stripping out email-style boilerplate, unstable routing details, and one-off distribution headers." → "These pages keep the durable guidance from office memos and drop the email boilerplate, routing details, and one-off headers." **[safe]**
- `how-to/index.md`: "Draft pages converted from short procedural source documents." → "Short, durable procedures you can follow and revise as tools change." **[judgment]**

---

# Onboarding

### `onboarding/onboarding-process-and-checklist.md`
Assessment: Excellent. Active, concrete, well-tabled. Hits the target. Only nits.

- L22 epigraph: "Great onboarding is a retention and performance lever. Treat it as critical infrastructure." — fine, but it is repeated near-verbatim in `managers-onboarding-playbook` L18. Consider varying one. **[judgment]**
- L18: "is productive, connected, and clear on expectations within the first 30 days, owns a defined slice of work by day 60, and is delivering meaningful outputs by day 90." — long but parallel and clear; keep. No change.
- L171: "Office mission, four teams, five services, and the cycle." — "the cycle" is undefined this early for a brand-new hire scanning a meeting list. → "Office mission, four teams, five services, and how the work cycle fits together." **[judgment]**

### `onboarding/offboarding-process-and-checklist.md`
Assessment: Strong, humane, and concrete. The principle bullets and tables are exactly right. Almost nothing to do.

- L45: "Anything that lives in your head must be written down." — good line, keep.
- L5: "Protecting continuity, security, and OPI's credibility through humane, predictable transitions." — sentence fragment as a standfirst; acceptable house style here. No change.

### `onboarding/managers-onboarding-playbook.md`
Assessment: Sharp and usable. Active voice, real specifics. A couple of intensifier/filler trims.

- L42: "They are easy to skip and expensive to skip." — the doubled "to skip" is a deliberate rhetorical echo and works; keep. **[judgment]** (only flag if the owner finds it cute)
- L18: "Staff who land poorly cost the team energy in ways that compound for months." → "Staff who land poorly drain the team for months." **[safe]**
- L94: "\"Do good work\" is not a target." — crisp, keep.

### `onboarding/maps-benefits-quick-guide.md`
Assessment: Genuinely plain-language and well-structured for a benefits reference. The leave table is the highlight. Voice is fine; this is reference material and reads cleanly.

- L16 disclaimer and L138 document-status note say the same "confirm with HR / draft pending review" thing twice. Acceptable for a benefits doc (redundancy is safer here), but the owner could trim one. **[judgment]**
- No prose-level rewrites needed.

### `onboarding/new-hire-announcement-template.md`
Assessment: Warm and on-voice for its purpose. The problem is structural: it uses `#` (H1) repeatedly inside the body as decorative section titles ("A small, warm welcome," "For any new hire," "Who does what, in order"), which breaks heading hierarchy and accessibility — and the QA standard on this very site (`qa-standards.md` Gate 1) requires proper H1/H2/H3 nesting.

- Multiple in-body `#` headings (L7, L36, L61, L87) → demote to `##`/`###` so there is one H1. **[safe]** (structure only; does not touch anchors of the section pages)
- L13: "Editorial guardrails" — good. Content is strong.
- L55 / L98: "Required fields the manager must provide the day before" and "If the new hire opts out" are bold-or-plain pseudo-headings inconsistent with the `##` headings around them. Make them `###`. **[safe]**

### `onboarding/new-hire-orientation-guide.md`
Assessment: One of the best pages in the handbook. Welcoming without being mushy, concrete, active. The tool table and "what good looks like by Day 30" are model sections. Very little to change.

- L186: "Your work will matter quickly." — good, keep.
- L22: "It tells you what to expect, who you'll meet, what you need to do to get set up, and how to find your footing." — slightly listy; fine. No change.
- L152: "The principle is simple: reduce tool sprawl and make it easy to find the truth." — "find the truth" is a touch grand but it is a recurring house phrase across the playbook and strategy pages, so keep for consistency. No change.

---

# Administrative memos

### `administrative-memos/essential-and-emergency-essential-designations.md`
Assessment: Appropriately formal, well-organized, legally careful. Active enough for a continuity memo. Minor redundancy.

- L41–43 vs. L26–32: the "(for example: severe weather, public safety incidents, critical systems outages...)" list appears twice within a few lines. Cut the second instance. **[safe]**
- L47–48 (table) uses passive "Required to report" / "May be required to report" — acceptable and standard for designations language. No change.

### `administrative-memos/media-and-press-engagement.md`
Assessment: Clear and correctly cautious. Reads as a real, well-written directive. Light passive/wordiness trims only.

- L48: "This guidance is not intended to discourage thought leadership or professional engagement, but rather to ensure that all official communications are coordinated, accurate, and consistent." → "This guidance is not meant to discourage thought leadership or professional engagement. It exists to keep official communications coordinated, accurate, and consistent." **[safe]**
- L55: "Thank you for your attention to this standard." → "Thank you." or cut. Mild corporate filler. **[judgment]**

### `administrative-memos/responding-to-city-council-requests.md`
Assessment: Accurate and complete, but the two opening paragraphs are dense, passive, and run-on — the weakest readability in the memo group. Procedure would read better as numbered steps.

- L31–35: "any request for information, documents, data, applications, or other materials that originates from a member of the Baltimore City Council or Baltimore City Council support staff that is received by the Mayor's Office Of Performance and Innovation (OPI), must first be reviewed and approved by the Mayor's Office of Government Relations (MOGR) prior to being shared or released." → "Any request from a Baltimore City Council member or their support staff — for information, documents, data, applications, or other materials — must be reviewed and approved by the Mayor's Office of Government Relations (MOGR) before OPI shares or releases anything." **[safe]**
- L44–54 (the "Process" paragraph): convert to numbered steps (receive → gather the request + the requester's name → email MOGR via City email → wait for authorization → release only after sign-off). Currently one passive block. **[judgment]** (restructure)
- L50: "Mayor's Office of Government relations" — lowercase "relations" is a typo vs. the proper noun used elsewhere. **[safe]**
- L33–41: passive throughout ("must first be reviewed," "should not be released or shared"). Where possible, name the actor ("OPI staff must not release..."). **[judgment]**

### `administrative-memos/telework-and-in-office-schedule.md`
Assessment: The content is sound but the lead paragraph is the most confused prose in the entire handbook — it contradicts the title and itself on dates and cadence, and is one long run-on. This is a credibility/accuracy issue, not just style. Flag to owner before any copy edit.

- **Factual conflict (must resolve):** Title and L18 say the transition begins **Monday, February 23, 2026**. But L20–21 say "Starting the week of **February 1**" and "When this adjustment begins (**Monday, February 1st**), staff will be required to be onsite that week 4x." The example table (L32–34) then starts at **February 16**. Three different start dates. **[judgment]** — owner must pick the correct date(s); an editor cannot guess.
- L18–26 is a single dense paragraph with nested parentheticals, stray apostrophes ("Tuesday's, Wednesday's, and Thursdays"), and "4x per" (missing "week"). Rebuild as: one sentence stating the new rotating 3x/4x policy and start date, then a short clarifier, then the example table. **[safe]** once dates are fixed.
- L36: "This adjustment supports collaboration, culture, and delivery as our team takes on more ambitious goals in FY26." — fine.
- L43–51: three paragraphs ("Being in the office during core days strengthens...," "In-person time also ensures...," "Just as importantly...") are rationale that drifts toward inspirational filler. Tighten to one paragraph or a short bullet list of why core days matter. **[judgment]**
- L46: "those small moments, impromptu discussions, brainstorming sessions, or celebrating wins, are what build OPI's culture." — comma-spliced and a touch breathless. → "the impromptu conversations, brainstorming, and shared wins that build OPI's culture." **[safe]**
- L112: "I am grateful for your flexibility, commitment, and enthusiasm as we enter this next chapter together." — standard sign-off; acceptable. No change.
- Section headings `## In-Office Days`, `## Remote Days`, `## Core Hours`, `## Full-Day Presence` are all `##` but are sub-points of "Core Expectations" (also `##`). Demote them to `###` under Core Expectations. **[safe]**

---

# How-to guides

### `how-to/add-a-printer.md` and `how-to/change-your-city-password.md`
Assessment: Two-line pointer pages to City support articles. Crisp and correct. No changes.

### `how-to/silence-teams-notifications-while-sharing-your-screen.md`
Assessment: Model how-to. Numbered steps, "Before you start," "What success looks like." Exactly the target. No changes.

### `how-to/create-planner-groups-without-automatic-member-alerts.md`
Assessment: Clean and step-based. The "Source note" at the end is internal editorial scaffolding that reads oddly on a reader-facing page.

- L44–47 "Source note": "The source document is brief and assumes a Microsoft 365 environment already in place. Confirm the current Planner and Outlook labels before approving this as a final support page." — this is a note to editors, not users. Move to a comment or cut once verified. **[judgment]**

### `how-to/submit-your-weekly-update.md`
Assessment: Useful and mostly clear, but inconsistent capitalization/voice and a few awkward headings betray its source-doc origin. The structure table is excellent.

- L46 heading: "How to Update Your Initiatives open full item panel (better for full edits)" — ungrammatical run-on heading. → "How to Update Your Initiatives (Full Item Panel)". **[safe]**
- L17: "Link: Book of Business - Weekly Updates" — reads as a placeholder; if this should be a hyperlink, make it one (don't break it if it already resolves via the site). **[judgment]**
- L20: "Mallory is your primary point of contact" — first name only, no role; inconsistent with the named+titled style elsewhere. Add role. **[judgment]**
- L41: "You can also save each entry by hitting the check in each text box" → "Save each entry by clicking the check mark in the text box." **[safe]**
- L77: "Avoid vague updates (e.g., `working on...`), be specific about what changed" — comma splice. → "Avoid vague updates like `working on...`; say specifically what changed." **[safe]**

### `how-to/edit-a-past-reporting-period-in-book-of-business.md`
Assessment: Functional steps, but opens with a broken-looking line and mixes sentence fragments. Reads as lightly-touched source.

- L8: "Below is a video embedded to have visual instructions" — ungrammatical, and there is no visible embed in the markdown. → "A video walkthrough is embedded below." (or remove if no embed exists). **[safe]**
- L13: "On the left navigation select Book of Business and then select weekly update." → "In the left navigation, select **Book of Business**, then **Weekly Update**." **[safe]**
- L34: "Double-click the cell or hit edit in grid view if you want to edit OR click directly into a field." → "Double-click the cell, switch to **Edit in grid view**, or click directly into a field." **[safe]**

### `how-to/book-the-idea-lab-fayette.md`
Assessment: This is a pasted policy/sign-off form, not a wiki how-to. ALL-CAPS shouting, a trailing signature block ("Signed: / Ph. #:"), and inconsistent punctuation. The information is valuable; the presentation is off-brand.

- L49: "GROUP FACILITATOR HAS READ THE INFORMATION AND AGREES TO IDEA LAB POLICIES:" and L51–54 signature block — this is a paper form. Either move it behind a clearly labeled "Reservation form (sign and return)" section or link to the form. As-is it makes a wiki page look like a fax. **[judgment]**
- L28–31: "Spillage of beverages/food, breakage of tables or AV equipment must be reported..." and L41 "Whiteboards MUST be erased" — random ALL-CAPS and "w/" abbreviations. Normalize to sentence case and spell out. **[safe]**
- L8: "Break Room (#2) food to be served - only." → "Break Room (#2): food service only." **[safe]**
- Consider a short lead sentence stating what this page is and the one action a reader takes (email Jeanine Murphy to reserve). Right now it opens mid-policy. **[judgment]**

### `how-to/order-food-catering-from-city-vendors.md`
Assessment: Practical and friendly but riddled with source-doc artifacts: "72Hr's aways," "777?", "bill you(r) Cost Center," shouting bold. Information is good; polish is needed.

- L5: "if you know your date of need is at least 72Hr's aways." → "if your event is at least 72 hours away." **[safe]**
- L24: "These restaurants have agreements with the Baltimore City and will bill Natasha" → "These restaurants have agreements with the City and will bill Natasha." **[safe]**
- L32: "410-727-777?" — incomplete phone number; verify and fix. **[judgment]** (data accuracy)
- L40: "**If asked, tell the caterer that Desi or Natasha will ensure payment**" — bold is fine for emphasis; "ensure payment" is good. No change.
- L18: "Natasha will take care of the order and chargeback to OPI." → "Natasha places the order and charges it back to OPI." **[safe]**

### `how-to/git-guide.md`
Assessment: The biggest voice outlier in the handbook. It is a conversational essay — rhetorical questions as headings, jokes ("hit by a bus," "Menacingly.", "Code... rotting on the vine"), heavy second person, and long meandering paragraphs. The technical content is accurate and the Conventional Commits / Conventional Branch guidance is genuinely useful, but the register is wrong for a reference page and the length triples what's needed. This is the page most in need of a structural rewrite toward crisp, scannable how-to. Recommend a dedicated rewrite pass rather than line edits alone.

Representative line-level fixes (illustrative; the whole page needs tightening):
- L11–16: "Git is a version control system (VCS) that is popularly used in many development teams in tracking changes done to code in a decentralized manner. With Git, one can build an entire history of their application/code from start and easily refer to those prior versions..." → "Git is a version control system. It tracks every change to your code and lets you revisit any earlier version." **[safe]**
- Rhetorical-question headings: "### Now it's installed, what do I do?", "### Is that really all there is to tracking my code with Git?" → declarative headings: "### Set up your first repository", "### Beyond the basics: Git etiquette." **[judgment]** (tone/structure)
- L142–143: "lest you be hit by a bus or leave the team (and we all know which is the worse scenario of the two)." → cut the parenthetical joke; keep "so the work survives if you leave the team." **[judgment]**
- L184–188: "the almighty merge. Without a merge, you'll have branches just... sitting there. Menacingly. Code of varying qualities rotting on the vine..." → "Branches only have value once they merge. A pull request gets your work reviewed and into `main` safely." **[judgment]**
- L48–52, L74–84, L176–181: the long second-person "let's talk about..." connective tissue between sections can be cut entirely; each `###` should open with the instruction. **[judgment]**
- L223: "(The above uses markdown, which is why there are so many asterisks.)" — meta-aside; cut. **[safe]**
- Procedures buried in prose (install, first push, open a PR) should become numbered steps. The install section already has the right idea; the "How do I push my code?" section (L48–71) is one dense paragraph that should be 4–5 numbered steps. **[judgment]**

---

# Operations

### `operations/leadership-norms.md`
Assessment: Authoritative and well-structured — Boundaries / Rules / Standards / Expectations is a clean spine, and the short imperative sub-heads are exactly on target ("No triangulation," "We escalate early"). One real defect: a broken ordered list.

- **Ordered-list bug:** "Manager accountability" (L274–282) renders items as **6, 7, 8, 9** and "Closing" (L298–302) as **10, 11, 12**, continuing the numbering from the L24–32 list. Reset these to `1.`-start lists (or make them bullets). Markdown is continuing the count. **[safe]** (rendering correctness)
- L57: "This is vital for consistent direction and staff morale." — mild filler appended to an otherwise crisp rule. → cut, or "It keeps direction consistent and protects morale." **[safe]**
- L256: "Disagree in the room. Align outside it." — excellent, keep.
- L18: "Our effectiveness depends not only on analytical and technical skill, but on how we work together, how we make decisions, and how we protect trust..." — slightly long but parallel and clear. No change.

### `operations/intake-sop.md`
Assessment: Exemplary. "One front door. Clear vetting. No surprise commitments." sets the tone and the page delivers on it. Active, decision-oriented, concrete. No substantive changes.

- L18: "whether it comes from the Mayor's Office, an agency partner, or an internal team, enters through a single intake process" — clean. No change.
- Numbered vetting checklist and decision-outcome table are model structure. No change.

### `operations/performance-standards-staff.md`
Assessment: Long but disciplined. The rating scale, eight dimensions, and evidence requirements are precise and fair. Plain-language throughout. Two heading-level inconsistencies to fix.

- **Heading inconsistency:** L99 "**When proposing a 1 or after a trust breach**" (bold paragraph) sits between L91 `### When proposing a 2` and L107 `### When a staff member disagrees`. It should be `###`. Same issue at L204 "**When performance is a 1 or a trust breach occurs**" vs. the `###` sibling at L196. **[safe]**
- L51 epigraph "A 3 is the bar..." and L66 "A 3 is strong performance..." restate the same point a few lines apart. Keep the epigraph; trim the L66 repeat. **[judgment]**
- L184: "The goal is clarity and fairness, not debate." — sharp, keep.
- Voice is otherwise active and concrete. No prose rewrites needed.

### `operations/performance-standards-manager-companion.md`
Assessment: Tight, evidence-first, well-scoped. The calibration packet table and bias check are excellent. Same one heading defect as its companion.

- **Heading inconsistency:** L99 "**When proposing a 1 or after a trust breach**" is a bold paragraph between `### When proposing a 2` (L91) and `### When a staff member disagrees` (L107). Promote to `###`. **[safe]**
- L24 epigraph and L65–69 "Calibration principles" restate the "not stack ranking / not politics / not penalizing escalation" trio. Intentional reinforcement; acceptable. **[judgment]**
- No prose-level changes needed.

### `operations/productivity-and-collaboration-playbook.md`
Assessment: Long but genuinely useful and consistently on-voice. The "10 working norms," tool matrix, and templates are model reference material. Active, specific, scannable. Essentially nothing to fix.

- L244: "Ad hoc work is the number-one cause of missed deadlines." — strong, keep.
- L70: "*Practical rule: drafts can live in OneDrive; anything you expect others to use or reference must be moved to the appropriate SharePoint space.*" — clear. No change.
- The `Term — definition` bullet pattern is used heavily and correctly (house style). No flags.

### `operations/qa-standards.md`
Assessment: Excellent and, fittingly, the most plain-language-disciplined page (it sets the plain-language bar and meets it). Active voice, concrete gates, copy/paste checklist. One heading defect.

- **Heading inconsistency:** Gate 3 (L97) opens with "**Minimum standard**" and "**When to consult the Deputy Chief Data Officer designee**" as **bold paragraphs**, while Gates 1, 2, and 4 use `### Minimum standard` / `### Quick checks`. Make Gate 3 match (`###`). **[safe]**
- L20: "*No public artifact ships without QA. No surprise launches.*" — keep.
- L231: "Repeat failures are coached, not punished privately." — good. No change.

### `operations/charter-template.md`
Assessment: Clean, decision-grade, well-structured. The fillable tables and "no charter, no work" framing are exactly right. No substantive changes.

- L21: "*A charter is not a plan. It is the agreement that makes a plan possible.*" — keep.
- Minor: L178 "Required operating model fields" appears after "Maintenance" (L174), so a reader hits Maintenance, then more required content. Consider ordering the operating-model table before Maintenance. **[judgment]** (sequence)

### `operations/problem-statement-template.md`
Assessment: One of the best-written pages on the site. Concrete, witty without being jokey, and the weak→stronger rewrite table is a teaching artifact in itself. Hits the target cleanly. No changes.

- L18: "A good problem statement is the cheapest piece of work in the entire project." — excellent opener, keep.
- L94–98 stress tests are crisp. No change.

### `operations/sharepoint-operating-system-strategy.md`
Assessment: Dense but well-organized strategy/reference. Active, specific (SLAs, owners, cadences), and the schema tables are thorough. Voice is on-target; the only risk is length, but it is reference material and the structure carries it.

- L20: "This is not a file dump. It is a living operating manual..." — strong, keep.
- L21: "The design should feel disciplined and polished: simple at the top, deep underneath, with explicit decision rights and measurable expectations." → "It should be simple at the top, deep underneath, with explicit decision rights and measurable expectations." (trim "should feel disciplined and polished" — telling-not-showing). **[judgment]**
- L351: "*If you only remember one thing: tag the work so someone new can find it and understand who owns it.*" — great closer, keep.
- No other prose changes needed; `Term — definition` bullets are house style.

---

# Recommendation counts

- **[safe]:** 27
- **[judgment]:** 23

(Counts include the structural/heading-level and ordered-list fixes, which are low-risk but worth owner awareness.)

# Priority actions for the owner (beyond copy polish)

1. **Resolve the telework memo date contradiction** (Feb 23 vs. Feb 1 vs. Feb 16). This is an accuracy defect on a policy page. **[judgment]**
2. **Fix the `leadership-norms` ordered-list numbering** (6–12 bug). **[safe]**
3. **Normalize bold-paragraph pseudo-headings to `###`** in `performance-standards-staff`, `performance-standards-manager-companion`, `qa-standards` (Gate 3), and the in-body H1s in `new-hire-announcement-template`. **[safe]**
4. **Schedule a dedicated rewrite of `git-guide`** toward a crisp, scannable, declarative reference — it is the largest voice outlier. **[judgment]**
5. **Clean the four source-dump how-tos** (`book-the-idea-lab-fayette`, `order-food-catering`, `edit-a-past-reporting-period`, `submit-your-weekly-update`) to match the step-based standard the section index promises, and verify the incomplete phone number in the catering page. **[safe]/[judgment]**
