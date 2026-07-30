# User Stories

**Status:** Proposed for owner review. Repository evidence was verified on
2026-07-30. Current-state labels describe implemented paths and checks; they do
not claim measured comprehension or task completion.

These stories turn the
[Product Requirements](product-requirements.md) into tasks a person can
complete. They cover understanding OPI, finding content, choosing a next step,
proposing and reviewing a change, and publishing the website.

The stories describe OPI Foundations. They do not define the detailed workflows
of the Baltimore Intelligence Center, Baltimore City Data Platform, Baltimore
City Performance Portal, or Baltimore 311 Explorer. This website owns the
explanation and handoff to those products. Their application behavior belongs
in their own product contracts.

## How to read the stories

Each story names a person, a need, and why that need matters. Acceptance
criteria describe observable outcomes without prescribing a layout unless the
layout itself carries meaning or an accessibility guarantee.

Current-state labels have three meanings:

- **Available now** means a maintained path exists and the repository checks
  the parts it can check. It does not mean a human outcome has been measured.
- **Partially available** means a useful path exists, but a verified gap keeps
  the full acceptance criteria from being claimed.
- **Decision-dependent** means OPI must make a business or product decision
  before the story can be completed safely.

A decision-dependent story is not permission to invent the missing answer. Its
question remains in
[Open decisions](product-requirements.md#open-decisions) until the named owner
resolves it.

## Coverage by audience

| Audience | Primary needs covered here |
| --- | --- |
| Residents and first-time readers | Understand OPI; find programs, products, measures, methods, and a useful next step |
| Agency partners and City staff | Choose a service or routine; prepare for CitiStat; understand roles and handoffs |
| Executive leaders and the City Council | Review mandate, ownership, intended outcomes, and accountability |
| Researchers, journalists, civic technologists, universities, nonprofits, and peer governments | Find definitions and source context; understand data practices; reuse methods with their limits intact |
| OPI staff | Learn the shared operating model and find the maintained explanation |
| Contributors and people reporting barriers | Correct a page, propose content, or report an inaccessible experience |
| Content owners and reviewers | Confirm a bounded business claim and provide traceable review |
| Maintainers and product managers | Preserve the information model, verify proportionately, and publish a reproducible artifact |
| People using keyboard navigation, assistive technology, zoom, narrow screens, or reduced browser capability | Complete the same core reading and contribution journeys |

## Traceability

This matrix connects each story group to the requirement it implements, the
current evidence, and the limit of that evidence. It is intentionally compact;
numbering every sentence would add maintenance without improving review.

| Story group | Requirement | Current evidence | Known limit |
| --- | --- | --- | --- |
| Orientation and shared understanding | [Orientation and progressive disclosure](product-requirements.md#orientation-and-progressive-disclosure) | [Home](../docs/index.md), [About Us](../docs/about-us/index.md), and [How Work Moves Through OPI](../docs/how-we-work/how-work-moves-through-opi.md) | No measured first-time-reader comprehension |
| Finding information | [Navigation and findability](product-requirements.md#navigation-and-findability) and [Ownership and freshness](product-requirements.md#ownership-and-freshness) | Intentional `.pages` navigation, search, breadcrumbs, strict build, built-link checks, and required review metadata | No ordinary-language task baseline, deliberate not-found recovery, or visible ownership treatment |
| Choosing a service or routine | [Service and engagement routing](product-requirements.md#service-and-engagement-routing) | [How to Engage OPI](../docs/what-we-do/how-to-engage-opi.md) and the operating-model decision rules | AdminOps routing remains undecided |
| Programs, products, data, and methods | [Content model and canonical pages](product-requirements.md#content-model-and-canonical-pages) and [Product discovery and outbound journeys](product-requirements.md#product-discovery-and-outbound-journeys) | Canonical What We Do and Reference sections | Four taxonomy, audience, and roadmap questions remain open |
| Correcting and contributing | [Contribution and correction](product-requirements.md#contribution-and-correction) | Page edit links, repository issue forms, email, and [Contributing](../docs/resources/contributing.md) | The general issue card is inert, and response outcomes are not instrumented |
| Inclusive use | [Accessible use](product-requirements.md#accessible-use) and [Responsive presentation and appearance](product-requirements.md#responsive-presentation-and-appearance) | [Accessibility](../docs/resources/accessibility.md), static checks, and focused browser checks | No dated manual screen-reader, zoom, or text-spacing pass is recorded |
| Governing and publishing | [Ownership and freshness](product-requirements.md#ownership-and-freshness), [Organization data and source placement](product-requirements.md#organization-data-and-source-placement), [Local authoring](product-requirements.md#local-authoring), and [Publishing and release integrity](product-requirements.md#publishing-and-release-integrity) | Validated source boundaries, nested task gates, strict build, and artifact checks | Product ownership and some human release evidence remain unresolved |

## Orientation and shared understanding

### Story: Understand OPI's purpose and authority

*As a resident, Council reader, City leader, or first-time partner, I want a
direct explanation of OPI and its mandate so that I can decide whether I am in
the right place and interpret its work in context.*

Current state: **Available now.**

Acceptance criteria:

1. The opening names the Mayor's Office of Performance and Innovation, explains
   what OPI Foundations contains, and does not assume knowledge of City
   reporting lines.
2. About Us explains OPI's mission, values, and authority without turning an
   aspiration into a legal claim.
3. The reader can choose About Us, How We Work, What We Do, or Resources and can
   reach [How to Engage OPI](../docs/what-we-do/how-to-engage-opi.md) when they
   need help.
4. The website remains clearly an explanation layer, not a service-request or
   case-tracking system.

### Story: Learn the four-part office model

*As someone learning about OPI, I want to distinguish a team, service, program,
and product so that I can interpret the rest of the website correctly.*

Current state: **Available now.**

Acceptance criteria:

1. The model defines each type and lists the same current members across
   onboarding, landing pages, navigation, and canonical pages.
2. Innovation Lab appears as both a team and a service with an explanation that
   this is intentional.
3. CitiStat appears as a program supported by all teams, not as a team.
4. Cross-Agency Delivery appears as a service and never as a staffed team.

### Story: Find the team behind the work

*As a City colleague, I want to understand OPI's teams and reporting structure
so that I can place a responsibility without treating the org chart as the
whole operating model.*

Current state: **Available now.**

Acceptance criteria:

1. About Us reaches all four team pages, and each team links to related
   services, programs, or products.
2. The organization and team views use the same limited staff-data model and
   distinguish reporting relationships from service handoffs.
3. The views expose only the documented fields for names, working titles, team
   assignments, reporting relationships, and short role summaries.
4. Personnel records, phone numbers, individual email addresses, compensation,
   and classifications remain in their owning City systems.

### Story: Learn how work moves through OPI

*As a new OPI staff member or agency partner, I want one clear account of how a
problem moves from evidence to a tested fix and sustainment so that I can use
the same operating language as the office.*

Current state: **Available now.**

Acceptance criteria:

1. The reader can follow the roles of CitiStat, Data and Analytics, Innovation
   Lab, Cross-Agency Delivery, and AdminOps while seeing that not every problem
   uses every service.
2. Decision rules distinguish a Stat, data-quality work, product discovery,
   Tiger Team, delivery activation, and one-time decision.
3. Handoffs name the information and ownership expected at each boundary.
4. Shared summaries link to
   [How Work Moves Through OPI](../docs/how-we-work/how-work-moves-through-opi.md)
   instead of creating a competing office-wide model.

## Finding and navigating information

### Story: Find content through navigation or search

*As a reader who does not know the exact page name, I want predictable
navigation and plain-language search so that I can discover the relevant
material without guessing OPI's structure.*

Current state: **Partially available.** Navigation and exact-term search work,
but ordinary-language discovery and result-type disambiguation have no measured
task evidence.

Acceptance criteria:

1. Every canonical page is reachable through intentional global and section
   navigation, and the page title, active state, and breadcrumbs agree.
2. Search indexes meaningful page content and presents enough context to
   distinguish a team, service, program, product, and reference.
3. Full names appear for important terms even when a recognized short form is
   also used.
4. A narrow-screen or JavaScript-disabled reader retains complete navigation
   even when enhanced search is unavailable.

### Story: Follow or recover from a link

*As a reader moving between related pages or returning from a bookmark, I want
clear destinations and a recovery path so that a renamed or missing page does
not become a dead end.*

Current state: **Partially available.** Link integrity is checked, but a
deliberate stale-bookmark and not-found recovery experience has not been
specified.

Acceptance criteria:

1. Link text names the destination or outcome without depending on nearby
   visual context.
2. A link to an OPI product or another City system explains what the reader
   will find there.
3. Moving a page updates navigation, cards, cross-links, and any needed
   redirect in the same change.
4. A missing or retired route offers a useful way back to search, the homepage,
   or the relevant section.

### Story: Know who maintains a page

*As a reader or reviewer, I want to know who maintains a page and when it was
reviewed so that I can direct a correction and judge whether the content may be
stale.*

Current state: **Partially available.** Ownership and review dates are required
and checked in source, but they are not shown on the rendered page. The visible
experience requires
[Decision 9](product-requirements.md#decision-9-should-pages-show-their-owner-and-review-date).

Acceptance criteria:

1. Every canonical page has an owner, last-reviewed date, next-review date, and
   concise change note in the nearest metadata file.
2. A reader-facing treatment, if adopted, distinguishes page maintenance from
   program, service, product, or decision ownership.
3. A new section cannot publish without its ownership fields.
4. An overdue date stops the source gate and gives the maintainer an actionable
   review instruction.

## Choosing an OPI service or routine

### Story: Find the right service

*As an agency partner, I want to compare my need with OPI's services so that I
can contact the right part of the office with useful context.*

Current state: **Partially available.** The engagement page covers four of the
five services; AdminOps requires
[Decision 2](product-requirements.md#decision-2-is-adminops-directly-requestable).

Acceptance criteria:

1. The reader can compare a recurring performance problem, data or analytics
   need, service or product design work, and stalled multi-agency problem.
2. Each path reaches the canonical service explanation before or alongside the
   contact route.
3. Cross-Agency Delivery retains its authorizer and multi-agency entry
   conditions.
4. The page does not promise acceptance, timing, capacity, or a tracked case
   unless OPI establishes that commitment.

### Story: Choose the right operating routine

*As an agency lead with a difficult problem, I want to distinguish a Stat,
data-quality sprint, product discovery, Tiger Team, delivery activation, and
decision memo so that I do not create the wrong meeting or workgroup.*

Current state: **Available now.**

Acceptance criteria:

1. The choice begins with the management problem or decision, not a preferred
   team name.
2. Each routine has a distinct trigger, purpose, and owner or decision-right
   requirement.
3. Performance review is not confused with diagnosis, product work, or
   implementation coordination.
4. The path includes sustainment and handoff, not only kickoff or launch.

### Story: Prepare for a CitiStat session

*As a Stat participant, I want the roles, preparation, artifacts, session
method, and follow-up expectations so that I can contribute to a useful
performance review.*

Current state: **Available now.**

Acceptance criteria:

1. The CitiStat section explains what qualifies as a Stat and reaches the
   strategic framework, method playbook, templates, portfolio, and quality
   standard.
2. Roles name program ownership, day-to-day leadership, quality review, session
   leadership, agency ownership, and analyst work.
3. Preparation covers the problem, measures, source context, prior commitments,
   and decisions needed.
4. Follow-up covers owners, due dates, evidence, escalation, and closure.

### Story: Understand a Cross-Agency Delivery activation

*As a City leader or agency owner, I want to know when Cross-Agency Delivery is
appropriate and what authority it requires so that a multi-agency problem has
real decision rights and a finish condition.*

Current state: **Available now.**

Acceptance criteria:

1. The service is a coordinating service supported by OPI, not a standalone
   team.
2. Entry criteria distinguish an activation from an ordinary workgroup,
   Innovation Lab engagement, or CitiStat follow-up.
3. The reader can identify the Authorizer, Senior Responsible Owner, agency
   owners, escalation path, and sustainment owner.
4. Expected artifacts cover chartering, commitments, decisions, closure
   evidence, and sustainment.

### Story: Review OPI accountability

*As an executive leader or Council reader, I want to compare OPI's services,
mandates, ownership, goals, and intended outcomes so that I can understand what
the office is accountable for.*

Current state: **Available now.**

Acceptance criteria:

1. A cross-service reference presents all five services in comparable form and
   distinguishes each service from its delivering team.
2. Legal authority, goal, outputs, intended outcomes, and measured results are
   not collapsed into one claim.
3. A summary reaches the full service or method when the reader needs detail.
4. The website does not present an intended outcome as an achieved result.

## Understanding programs, products, data, and methods

### Story: Understand how Baltimore publishes and governs data

*As a resident, analyst, researcher, or journalist, I want to understand OPI's
open-data and data-governance work so that I can find usable data and interpret
its limits.*

Current state: **Partially available.** The program explanation exists, but it
does not link to Open Baltimore; the portal's canonical type also requires
[Decision 3](product-requirements.md#decision-3-is-open-baltimore-a-product-a-program-component-or-both).

Acceptance criteria:

1. The reader can distinguish the Citywide Data and Analytics service, Data
   Governance program, Open Data program, and Baltimore City Data Platform.
2. The Open Data path reaches Open Baltimore and explains licensing,
   classification, metadata, and refresh expectations.
3. Data Governance explains stewardship, quality, classification, shared
   definitions, and responsible artificial-intelligence controls.
4. The website does not imply that all City data can be released or that a
   classification decision can be bypassed.

### Story: Understand the Citywide Data Network

*As an agency data lead, civic technologist, university partner, or resident, I
want to understand the Citywide Data Network's purpose and membership so that I
can tell whether and how I participate.*

Current state: **Decision-dependent.** The canonical page and glossary need
[Decision 4](product-requirements.md#decision-4-what-does-the-citywide-data-network-include).

Acceptance criteria:

1. The program has one consistent definition across its page and the glossary.
2. The definition says whether the network is an interagency forum, a broader
   partnership network, or a program with both components.
3. Intended participants, value, and relationship to Open Data are explicit.
4. A participation route appears only if the owner establishes one.

### Story: Reach the live 311 and performance products

*As a resident, reporter, Council reader, researcher, partner, or City staff
member, I want to reach the 311 Explorer or Performance Portal with enough
context to choose the right product and interpret what it shows.*

Current state: **Partially available.** Both product paths work, but the 311
page does not yet give a source link or warn that request volume alone is not a
complete measure of service quality.

Acceptance criteria:

1. Each product page names its audiences, purpose, maintained destination, and
   primary tasks.
2. The 311 page distinguishes exploring requests from submitting or updating a
   request and supplies source, freshness, and interpretation context.
3. The performance page distinguishes its plans and measures from this
   website's descriptive content.
4. Detailed product behavior remains in the product's own requirements and
   tests rather than being duplicated here.

### Story: Understand the Baltimore Intelligence Center

*As a City leader, analyst, or other intended reader, I want a clear explanation
of the Baltimore Intelligence Center's purpose, capabilities, and safeguards so
that I do not assume I have access or that every described capability is
available.*

Current state: **Partially available.** Audience and access language requires
[Decision 5](product-requirements.md#decision-5-who-can-use-the-baltimore-intelligence-center).

Acceptance criteria:

1. The page explains governed City intelligence, responsible
   artificial-intelligence use, architecture, source grounding, human
   oversight, access control, and monitoring in plain language.
2. Current, planned, and conceptual capabilities are distinguishable.
3. The page does not promise access or universal availability before the owner
   decides those facts.
4. The architecture page title matches its content, or a maintained roadmap is
   added after
   [Decision 8](product-requirements.md#decision-8-what-must-every-opi-product-page-say-about-ownership-and-roadmaps).

### Story: Understand the Baltimore City Data Platform

*As a data steward, analyst, product team member, or executive reader, I want
to understand the Data Platform so that I can place it correctly in the City's
data work.*

Current state: **Partially available.** Direct users and tasks require
[Decision 6](product-requirements.md#decision-6-who-directly-uses-the-baltimore-city-data-platform).

Acceptance criteria:

1. The page explains the governed data foundation, shared definitions,
   ownership, quality, and relationship to analytics and artificial
   intelligence.
2. It distinguishes the platform from the Citywide Data and Analytics service
   and Data Governance program.
3. Direct user groups and tasks appear only after the owner confirms them.
4. Operational procedures stay in the platform's owning documentation.

### Story: Learn and reuse an OPI method or term

*As a City colleague, nonprofit partner, university, or peer government, I want
the maintained method and plain-language definitions so that I can adapt the
work without losing the conditions that make it useful.*

Current state: **Available now.**

Acceptance criteria:

1. Reference and program sections expose the current playbooks, frameworks,
   templates, quality standards, and glossary.
2. A method states its purpose, roles, inputs, outputs, decision rights, and
   finish condition where relevant.
3. A summary or unfamiliar term links to the maintained method or definition
   instead of becoming a competing explanation.
4. The page distinguishes an example from a required standard and does not
   imply implementation support without an engagement path.
5. Reuse guidance reaches the
   [CC BY 4.0 content license](../LICENSE-CONTENT.md) and explains that City
   names, seals, and marks are not included in that license.

## Correcting and contributing content

### Story: Correct a page through the appropriate route

*As a reader who finds an error, I want to edit the source, open an issue, or
send an email so that I can propose a precise correction without needing a
particular authoring tool.*

Current state: **Partially available.** The edit and email routes work, but the
general issue card has no destination and the general issue forms do not yet
warn against sensitive personal information.

Acceptance criteria:

1. Every canonical page has a labeled, keyboard-accessible edit link to its
   source rather than generated output.
2. A contributor can use GitHub's web editor to preview Markdown, create a
   branch, and open a pull request without local tools.
3. [Contributing](../docs/resources/contributing.md) offers working issue and
   email routes and asks for the page, problem, evidence, and suggested
   correction.
4. Every issue route warns against sensitive personal information.
5. Hosted pull-request checks remain source-only; a maintainer or the deployment
   gate supplies the strict build and artifact proof for a web-authored change.

### Story: Propose a new page or section

*As an OPI staff member or partner with missing content, I want to propose a
page with a clear reader and owner so that the website grows intentionally.*

Current state: **Partially available.** The proposal and review contract exists,
but the general issue card has no destination and no issue form collects all
required fields.

Acceptance criteria:

1. The proposal names the reader, task, content type, canonical section, and why
   an existing page cannot answer the need.
2. It names a content owner and review cadence before publication.
3. A new section includes its landing page, navigation, card data, metadata,
   and relevant cross-links in one change.
4. New sections, navigation or taxonomy changes, and other structural or
   operating-model changes receive Executive Director sign-off.

### Story: Report an accessibility barrier

*As a reader who cannot complete a task because of an accessibility barrier, I
want a clear reporting route so that OPI can understand and correct the
specific experience.*

Current state: **Available now.**

Acceptance criteria:

1. [Accessibility](../docs/resources/accessibility.md) offers email and issue routes.
2. Guidance asks for the page, intended task, observed behavior, browser, and
   assistive technology when the reporter is comfortable sharing them.
3. Guidance says not to include sensitive personal information.
4. The correction is reviewed at the layer that owns the failure and across the
   affected journey.

## Inclusive reading and interaction

### Story: Read and navigate with a keyboard

*As a reader who does not use a mouse, I want to reach content, navigation,
search, appearance controls, page tools, and scrollable tables in a logical
order so that I can complete the same tasks as a pointer user.*

Current state: **Available now.**

Acceptance criteria:

1. A working skip link reaches main content, and focus order follows the
   semantic reading order.
2. Controls have visible focus and expected Enter, Space, Escape, and Tab
   behavior.
3. Drawers and dialogs contain focus while open, close predictably, and return
   focus to their trigger.
4. Core actions remain keyboard-reachable at desktop and narrow widths.

### Story: Understand the website with a screen reader

*As a screen-reader user, I want meaningful landmarks, headings, names, links,
and reading order so that I can understand the page and each available action.*

Current state: **Partially available.** Static semantics and automated browser
checks pass, but no dated human screen-reader review is recorded.

Acceptance criteria:

1. Each page has one main heading, a logical hierarchy, and meaningful
   landmarks.
2. Links and control names make sense without nearby visual context.
3. Current navigation, expanded state, and dialog purpose are exposed to
   assistive technology.
4. A human screen-reader review confirms the changed journey's announcements,
   reading order, and clarity.

### Story: Read with zoom, text spacing, or a narrow viewport

*As a reader who enlarges or reflows content, I want meaning and controls to
remain intact without page-level horizontal scrolling so that I can read
without repeated panning.*

Current state: **Partially available.** Automated 320-pixel reflow and focused
geometry checks pass; no dated manual 200% and 400% zoom or custom text-spacing
review is recorded.

Acceptance criteria:

1. Canonical pages reflow at 320 CSS pixels without page-level horizontal
   overflow.
2. Text remains usable at 200% and 400% zoom and with increased text spacing.
3. Headings and controls do not fragment, overlap, or leave their region. The
   measured header controls and homepage page tools meet the current
   44-by-44 CSS-pixel rule.
4. A table that needs two-dimensional comparison scrolls inside a labeled
   region rather than forcing the whole page sideways.

### Story: Read across appearance and browser capabilities

*As a reader using either color scheme, JavaScript-disabled navigation, or
fallback fonts, I want the core content and actions to remain available so that
an appearance choice or optional dependency does not block me.*

Current state: **Available now.**

Acceptance criteria:

1. Text, controls, states, and focus remain perceivable in both color schemes,
   and changing schemes does not change content or location.
2. JavaScript-disabled pages retain readable content and keyboard-native
   navigation; unavailable search is hidden rather than left broken.
3. Outside font failure falls back to readable typography.
4. No core journey depends on an outside analytics, script, or font service.

## Governing and publishing the product

### Story: Scope and review a proposed change

*As a product manager, content owner, or maintainer, I want a proposal tied to a
reader, journey, claim, and evidence so that the right owner can review it
without unnecessary process.*

Current state: **Available now.**

Acceptance criteria:

1. The proposal names the reader problem, canonical page, changed contract, and
   evidence.
2. A typo or unambiguous correction may use the direct maintainer path; a
   change to business meaning, ownership, access, metrics, or structure receives
   the required owner review.
3. A visible change includes a design decision and before-and-after evidence.
4. An unresolved business question goes to a named owner instead of being
   answered through implementation.

### Story: Keep structure and review dates aligned

*As a maintainer or content owner, I want structural companions and freshness
metadata to move with a page so that readers do not encounter stale navigation
or conflicting explanations.*

Current state: **Available now.**

Acceptance criteria:

1. Adding, moving, renaming, or deleting a page updates local navigation,
   cards, metadata, links, and redirects in the same change.
2. README, onboarding, maintainer guidance, requirements, and stories change
   when their described workflow changes.
3. An owner review checks business meaning, related definitions, links, and
   next steps before updating review dates.
4. Substantive content is not deleted without the owner's recorded review, and
   generated `site/` output is never edited.

### Story: Preserve the source-placement boundary

*As a maintainer, I want one limited organization model and enforced artifact
boundary so that the website explains OPI without becoming a personnel,
contact, or staff-working-material system.*

Current state: **Available now.**

Acceptance criteria:

1. Organization views consume the same validated `docs/_data/people.yml`
   model, and unknown fields or malformed relationships fail the source gate.
2. Renderers use the permitted staff fields; the non-rendered team
   `primary_value` remains in source until its named owner resolves its
   disposition.
3. Staff operating material and personnel records remain in their owning City
   systems, and the bounded Handbook stays excluded from generated output.
4. The artifact check enforces its named patterns, with owner review covering
   contextual placement that automation cannot infer.

### Story: Preview and verify a change proportionately

*As a contributor, I want one canonical preview and one proportionate
verification path so that I can review my change without repeating suites that
prove the same claim.*

Current state: **Partially available.** The preview paths and nested gates
exist, but one recorded verification exception prevents a complete prove-once
claim.

Acceptance criteria:

1. `task setup` installs the locked environment and hook; `task serve` starts
   the registered loopback preview.
2. Docker Compose serves the same source and reader-visible preview address as
   a development convenience.
3. `task ci` checks fast source contracts; `task prepush` adds tests,
   navigation contracts, one strict build, and artifact checks; `task validate`
   adds browser-only claims.
4. A shared behavior runs once unless another route, viewport, scheme, or state
   represents a distinct risk. Recorded exceptions link to the
   [technical specification](technical-spec.md#verification-architecture), and
   new checks enter the shared plan.

### Story: Publish the reviewed artifact

*As a maintainer, I want reviewed source to produce the GitHub Pages artifact
so that publication cannot drift from the change the team accepted.*

Current state: **Available now.**

Acceptance criteria:

1. The pull request presents source, ownership, navigation, and review evidence
   together.
2. A local branch runs the pre-push hook before push. A web-authored change
   receives the same strict build and artifact proof from a maintainer or the
   Pages deployment gate before publication.
3. Generated output is built from reviewed source rather than edited by hand.
4. A failed strict build, content contract, broken link, unsafe artifact, or
   accessibility check stops publication.

## Story acceptance for a release

A release does not need to exercise every story through the most expensive
gate. It needs complete risk coverage for the stories the change can affect.

A content-only change should prove source rules and the strict built artifact.
A navigation or shared presentation change also needs focused browser and human
review. A business-meaning change needs its content owner even when every
automated check passes. A change that depends on an unresolved decision stops
at the decision rather than shipping a technically valid guess.

When a story changes, update its prose, state, and acceptance criteria with the
behavior. When a new kind of reader task appears, add the story in the same
slice and link it to its product requirement.
