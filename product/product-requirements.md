# Product Requirements

**Status:** Proposed repository contract for owner review. Evidence was verified
against the repository on 2026-07-30. Current-assurance statements describe
implemented source, rendered behavior, and checks; they do not claim measured
reader comprehension or task completion.

OPI Foundations is the maintained website that explains how Baltimore City's
Mayor's Office of Performance and Innovation works. It gives readers one place
to understand the office's purpose, teams, services, programs, products,
methods, and shared vocabulary.

This document describes OPI Foundations itself. It does not define the detailed
behavior of the City products described in
[What We Do](../docs/what-we-do/products/index.md). Each of those products needs
its own product contract in the repository or City system that governs it.

## The product in one page

| Product fact | Current contract |
| --- | --- |
| Product type | A documentation website built from Markdown and small YAML data files |
| Primary job | Help a reader understand OPI, find the relevant part of its work, and know what to do next |
| Product governance | The Executive Director signs off on navigation, taxonomy, new sections, and other structural or operating-model changes |
| Content owners | The owner named in the nearest `.metadata.yml` file |
| Day-to-day maintenance | OPI Foundations Docs Maintainer |
| Delivery | A static MkDocs artifact published through GitHub Pages |
| Authentication | None |
| Runtime data | No database or service records; static build source includes the bounded organization model |
| Canonical change record | The repository history, pull requests, and ownership metadata |
| Release standard | The source, built artifact, and browser gates described in [Accessibility](../docs/resources/accessibility.md) and the repository maintainer guidance |

The website is a reference and an explanation layer. It is not an intake queue,
case-management system, employee system, data warehouse, or authenticated
workspace. When a reader needs OPI's help, the website routes them to
[How to Engage OPI](../docs/what-we-do/how-to-engage-opi.md). When a reader needs
to use an OPI product, the relevant product page should send them to that
product's owning system.

## Why the product exists

OPI's work crosses organizational and technical boundaries. A reader may know
the name of a team but need a service, know the name of a program but need a
method, or encounter a product without knowing who supports it. Without a
maintained explanation, those distinctions blur. People then rely on old
slides, personal explanations, or an organizational chart that cannot explain
how the work moves.

OPI Foundations solves that problem by making the office understandable. It
defines the vocabulary, shows how teams and work relate, explains the methods,
and gives every maintained page an owner and a review date. It also makes the
explanation correctable: a reader can propose a change from the page where they
found the problem.

## Product principles

### Begin with the reader's question

A page should answer why a reader came before it explains how OPI organizes
itself. A resident may want to understand a City performance measure. An agency
partner may need help with a recurring problem. A new OPI staff member may need
to learn the operating model. The page should give that person a useful first
step without requiring knowledge of OPI's org chart.

### Keep the office model exact

Teams, services, programs, and products are different things. The distinction
must stay consistent in navigation, landing pages, definitions, and individual
pages. Innovation Lab is both a team and a service. CitiStat is a program
supported by all teams. Cross-Agency Delivery is a service, not a staffed team.

### Prefer one maintained explanation

When one page owns a definition or method, other pages should link to it. A
second explanation becomes a second place that can become stale. The
[Glossary](../docs/resources/reference/glossary.md) owns shared terms, and
[How Work Moves Through OPI](../docs/how-we-work/how-work-moves-through-opi.md)
owns the office-wide handoff model.

### Show what is known and what is not

The website must not fill a gap with a confident assumption. If the audience,
owner, access rule, outcome measure, or business meaning is unsettled, the
question belongs in [Open decisions](#open-decisions) with a named owner.

### Make correction part of the product

Every page must have a source-side owner and review date, and readers must have
a correction route. Showing ownership metadata on the rendered page remains a
design decision. Maintainers must be able to trace a published statement to its
source change and review.

### Treat accessibility as a release condition

Every reader journey must work with a keyboard, assistive technology, narrow
screens, zoom, and either supported color scheme. Accessibility is part of the
same release decision as content accuracy and working links.

## People the website serves

The repository names the following audiences. This is a known-audience model,
not a ranked list. Which audience should receive first priority in homepage and
navigation decisions remains an open product decision.

### Residents and other first-time readers

Residents may want to understand what OPI does, how the City reviews
performance, what a named program means, or where a measure or service comes
from. They need plain language, enough context to interpret a page, and a clear
next step. They should not need a City title, an OPI acronym, or knowledge of
the office structure.

This group also includes journalists, researchers, students, civic
technologists, nonprofit partners, universities, peer governments, and anyone
trying to understand or reuse Baltimore's methods and open data.

### Agency partners and City staff

Agency directors, operational staff, analysts, data stewards, and Data-Driven
Officers need to understand what OPI offers and which routine fits a problem.
They need service boundaries, engagement paths, inputs, outputs, decision
rights, and links to the full method. They should be able to distinguish a
CitiStat question from a data request, product discovery, or a
Cross-Agency Delivery activation.

### City leadership and the City Council

Executive leaders, Council members, and Council staff need a concise and
credible account of OPI's mandate, work, ownership, and intended outcomes. They
need enough detail to understand accountability without having to inspect
working documents or operational systems.

### OPI staff

New and current OPI staff need a shared explanation of the office. The website
should help them use the same terms, understand handoffs, find the governing
method, and explain the work consistently. It does not replace employee
onboarding records, personnel documents, or staff operating materials held by
their owning City systems.

### Contributors and people reporting problems

A reader who finds an error, missing explanation, broken link, or accessibility
barrier needs a low-friction way to report it. A contributor with a proposed
wording change needs to know where the official page lives and what review the
change will receive.

### Content owners, reviewers, and maintainers

Content owners need a bounded review request, the changed words in context, and
an explicit statement of what they are being asked to confirm. Maintainers need
an information model, local preview, review history, and automated checks that
catch structural or accessibility regressions before publication.

### Access needs apply to every audience

Keyboard use, screen readers, zoom, text spacing, narrow screens, reduced
network availability, dark mode, and JavaScript-disabled reading are not
separate personas. They are ways any member of the audiences above may use the
website. The product must support them across the same core journeys.

## Product scope

### In scope

OPI Foundations owns:

1. The explanation of OPI's mission, identity, culture, structure, and
   operating model.
2. Canonical pages for OPI's teams, services, programs, and products.
3. Cross-cutting methods, service definitions, playbooks, accountability
   references, and the glossary.
4. The reading experience: information architecture, navigation, search,
   breadcrumbs, links, responsive presentation, and color schemes.
5. The correction experience: page edit links, issue and email routes,
   ownership metadata, review, and publication.
6. The limited organization model used by the leadership chart and team views.
7. The repository automation that builds, checks, and publishes the website.
8. Local authoring through `task serve` and the equivalent Docker Compose
   preview.

### Out of scope

OPI Foundations does not own:

1. Service-request intake, status tracking, case management, or a response
   queue.
2. Authentication, authorization, user accounts, or application audit logs.
3. The detailed workflows of the Baltimore Intelligence Center, Baltimore City
   Data Platform, Baltimore City Performance Portal, or Baltimore 311
   Explorer.
4. Operational datasets, dashboards, data pipelines, or the systems that
   calculate City measures.
5. Personnel records, full position descriptions, contact lists, performance
   records, vendor contracts, and controlled staff working materials.
6. Formal policies or records maintained by HR, procurement, legal, SharePoint,
   or another owning City system.
7. Analytics collection or user tracking until the City decides the measures,
   purpose, retention, and privacy rules.

An out-of-scope item may be linked when the link helps a reader finish a
journey. The website must not make a copy and present it as the maintained
record.

## Information architecture

The website has four main sections, each with a different reader question.

| Section | Question it answers |
| --- | --- |
| [About Us](../docs/about-us/index.md) | Who is OPI, what does it believe, and which teams make up the office? |
| [How We Work](../docs/how-we-work/index.md) | How does work move from a problem to a fix, and how is the office organized? |
| [What We Do](../docs/what-we-do/index.md) | Which services, programs, and products does OPI deliver or support? |
| [Resources](../docs/resources/index.md) | Where are the shared definitions, service standards, and contribution paths? |

Within that structure, every canonical page has an explicit role. One named
capability may have separate, intentionally scoped pages in more than one role,
as Innovation Lab does as both a team and a service.

| Type | Meaning | Current members |
| --- | --- | --- |
| Team | A group with staff and budget | Director's Office; Performance; Data and Analytics; Innovation Lab |
| Service | What OPI delivers | AdminOps; Citywide Performance Management; Citywide Data and Analytics; Innovation Lab; Cross-Agency Delivery |
| Program | An ongoing routine that may span teams | CitiStat; Data Governance; Open Data; Citywide Data Network |
| Product | A tool, platform, or resource OPI builds or supports | Baltimore Intelligence Center; Baltimore City Data Platform; Baltimore City Performance Portal; Baltimore 311 Explorer |

Navigation must express these distinctions. Search terms and cross-links may
connect them, but no page should silently reclassify an item to make a local
layout easier.

## Core journeys

The product must support the following end-to-end journeys. Detailed acceptance
criteria live in [User Stories](user-stories.md).

| Journey | Starting need | Successful end state |
| --- | --- | --- |
| Understand OPI | “What is this office?” | The reader can explain OPI's purpose and choose a useful next page. |
| Learn the office model | “How do the teams and work fit together?” | The reader can distinguish teams, services, programs, and products. |
| Find the right service | “Which part of OPI can help?” | An agency partner reaches the relevant service and engagement route. |
| Choose the right routine | “Is this CitiStat, a data issue, product work, or a delivery problem?” | The partner can identify the closest routine and the information needed to begin. |
| Prepare for CitiStat | “What happens before, during, and after a Stat?” | A participant finds the framework, playbook, roles, artifacts, and quality standard. |
| Review accountability | “What is OPI responsible for and what should result?” | A leader or Council reader can compare mandate, service, owner, and intended outcomes. |
| Understand City data work | “How does Baltimore govern, publish, and use data?” | The reader reaches the relevant program, service, product, or open-data destination. |
| Explore 311 or performance | “Where can I inspect service requests or performance measures?” | The reader reaches the correct OPI product and understands its purpose. |
| Understand governed intelligence | “What is the Baltimore Intelligence Center?” | The reader understands the documented purpose and boundaries without being promised undefined access. |
| Learn or reuse a method | “How does Baltimore run this practice?” | The reader finds a canonical playbook, definition, or method and its context. |
| Propose a correction | “This page is wrong or incomplete.” | The reader can submit the page, problem, and proposed correction through a maintained route. |
| Report an accessibility barrier | “I cannot complete this reading task.” | The reader can report the page, task, behavior, and technology without sharing sensitive information. |
| Review and publish content | “Is this change accurate and ready?” | The owner and maintainer can verify scope, review evidence, and release the same artifact that was checked. |
| Run the website locally | “How do I preview or verify a change?” | A contributor can start the canonical local preview and run the proportionate gate. |

## Capability requirements

### Orientation and progressive disclosure

The homepage must state what OPI Foundations is, what the office does, and how
the site is organized. It must offer useful starts for a first-time reader
without turning the homepage into a complete copy of the website.

Section landing pages must explain the section in plain language and present an
intentional reading order. Individual pages must lead with the point, define
unfamiliar terms, and link to deeper material when the reader needs it.

The product must not assume that a reader knows an acronym, City reporting
line, or OPI's four-part content model. When a formal term matters, the page
must define it or link to the glossary at first meaningful use.

### Navigation and findability

Every canonical page must be reachable through intentional navigation, not
only through search or a direct link. Section-local `.pages` files own the
labels and order. The current location must be clear through page title,
navigation state, and breadcrumbs.

Search must find pages by the words readers use, including full names and
necessary aliases. Search results must identify a destination clearly enough
that a reader can choose without opening several near-duplicates.

Links must name their destination or outcome. “Read more” and raw addresses do
not provide enough context when the destination can be named. A moved or
renamed page must update navigation, cards, cross-links, and any required
redirect in the same change.

### Content model and canonical pages

Each canonical team, service, program, and product page must make five facts
understandable:

1. What the item is.
2. Who it serves or affects.
3. What it owns and what it does not own.
4. How it relates to the rest of OPI.
5. What the reader should do or read next.

Where the office has decided them, the page should also name the accountable
owner, engagement route, expected inputs and outputs, intended outcomes, and
review cadence. Where those facts remain unsettled, the page must not imply
that a metadata owner is the business owner or that a descriptive page is a
product roadmap.

Shared terms belong in the glossary. Office-wide handoffs belong in
[How Work Moves Through OPI](../docs/how-we-work/how-work-moves-through-opi.md).
Detailed CitiStat mechanics belong in its strategic framework, method
playbook, templates, and quality standard. A summary may orient the reader, but
it must link back to the maintained explanation.

### Service and engagement routing

[How to Engage OPI](../docs/what-we-do/how-to-engage-opi.md) must help an agency
partner choose among the documented service paths and reach a person or
existing City routine. A service page must not imply that submitting a request
creates a tracked case or guarantees acceptance, timing, or capacity unless
OPI has established that promise.

The routing model must preserve meaningful entry criteria. Cross-Agency
Delivery, for example, requires the documented authorizer and multi-agency
conditions. A simple contact link must not erase those conditions.

The current engagement table does not name an AdminOps request path. That gap
is recorded as an open decision rather than filled in by this contract.

### Product discovery and outbound journeys

The products landing page must explain the difference between a product,
service, and program, and must list the current products consistently with the
rest of the website. Each product page must state its purpose and intended
readers before directing someone to an external application or explaining
technical layers.

OPI Foundations owns the handoff to a product, not the product's in-application
experience. A product link should explain where it goes and what the reader can
do there. If access is restricted or not yet defined, the page should state the
known boundary without inventing an audience or access process.

### Contribution and correction

Every canonical content page must expose a labeled edit route to its source.
The contribution page must also offer an issue route and an email route for
people who do not want to edit Markdown.

The maintainer triages a proposal within five business days. A typo or obvious
correction may be published by a maintainer. Substantive changes require the
page owner's accuracy review. New sections, navigation or taxonomy changes,
and other structural or operating-model changes require Executive Director
sign-off.

A review request must identify the changed claim, the reader affected, the
official page, and the evidence the owner is being asked to confirm. Sensitive
personal information must not be requested through a GitHub issue.

### Ownership and freshness

Every canonical page inherits an owner, last-reviewed date, next-review date,
and concise change note from the nearest `.metadata.yml`. A new section must
establish those fields before publication.

Metadata identifies who maintains the page. It must not be presented as proof
of program ownership, product ownership, decision rights, or endorsement
unless the content explicitly establishes that meaning.

Review dates are operational controls, not decoration. A maintainer must route
stale pages to their owners, record the review even when no wording changes,
and update linked pages when the review reveals a shared contradiction.

### Organization data and source placement

The organization views must use the single, validated model in
`docs/_data/people.yml`. Its rendered fields are limited to names, working
titles, team assignments, reporting relationships, and short role summaries.
The source also retains each team's non-rendered `primary_value` while the
Executive Director decides whether to restore, move, or retire it. A second
parser or parallel staff roster is not permitted.

Personnel records, compensation, classifications, personal or work phone
numbers, individual email addresses, contact-list exports, and controlled
working copies belong in their owning City systems. The website may explain
where a record belongs, but it must not publish a convenience copy.

The Staff Guide under `docs/how-we-work/handbook/` contains reviewed guidance on
onboarding, working norms, performance expectations, and leadership
commitments. Personnel records, contact lists, controlled forms, signed
evaluations, and case-specific HR material remain in their owning City systems.

### Responsive presentation and appearance

Pages must preserve meaning and reading order from a narrow mobile viewport
through a desktop viewport. Content must reflow without page-level horizontal
scrolling. A data table may scroll inside a clearly labeled region when the
table cannot be made meaningfully linear.

Navigation, search, page tools, cards, headings, links, and tables must remain
understandable in both supported color schemes. Appearance controls must not
hide the current page, change the content, or require a pointer device.

The product should use official MkDocs and Material features before adding a
template, stylesheet, or script. A customization must solve a verified reader
need, remain accessible, and be tested at the narrowest shared layer that owns
the behavior.

### Accessible use

OPI Foundations targets WCAG 2.2 Level AA. The complete promise and proof are
in [Accessibility](../docs/resources/accessibility.md).

The core reading journeys must work with keyboard navigation, visible focus,
screen readers, zoom, increased text spacing, narrow screens, and either color
scheme. The site must retain a useful reading and navigation path when
JavaScript is unavailable. Failure of an outside font service must not block
content or navigation.

Automated checks are necessary but not sufficient. A structural navigation,
template, or shared-component change also requires human review of keyboard
use, zoom, spacing, reading order, and screen-reader clarity.

### Publishing and release integrity

The source reviewed in a pull request must be the source used to build the
release. Generated `site/` files are never edited. GitHub Pages is the
canonical deployment path; Docker Compose is a local preview convenience.

The three verification gates must remain nested:

| Gate | Product claim it proves |
| --- | --- |
| `task ci` | Fast source formatting, types, policy, security, metadata, language, and local contracts are valid. |
| `task prepush` | The tests and navigation contracts pass, MkDocs builds strictly, and the generated artifact satisfies source-placement, link, and static accessibility rules. |
| `task validate` | The pre-push proof passes and the exact artifact also completes the browser interaction, reflow, and accessibility checks. |

Hosted pull-request checks remain fast and static. Tests, builds, and browsers
belong in the local pre-push and release gates. A new check must enter the
shared verification plan at the cheapest authoritative tier that proves its
claim. The current duplicate hosted-policy invocation is recorded, with its
retirement condition, in the
[Technical Specification](technical-spec.md#verification-architecture).

### Local authoring

`task setup` must install the project environment, and `task serve` must start
the live-reloading preview at the registered loopback address. Docker Compose
must serve the same source and canonical preview address for contributors who
do not want Python tooling on the host.

Local commands, the pre-push hook, and the deployment workflow must call the
same verification plans. A maintainer should not need a private sequence of
commands to reproduce a release result.

## Whole-product commitments

Each commitment separates current assurance from the human outcome that remains
unmeasured.

| Commitment | Current assurance | What is not yet proven |
| --- | --- | --- |
| The website presents one coherent account of OPI and its four-part model. | Homepage, section pages, cross-links, and consistency checks align the source. | First-time-reader comprehension and audience priority |
| Known journeys have maintained paths. | Navigation, search, breadcrumbs, product links, and engagement guidance exist. | Task success, search success, and not-found recovery |
| Every page has maintenance ownership and a review date. | Source metadata is required; overdue dates stop the source gate. | Metadata is not reader-visible and does not establish business ownership |
| Readers can propose corrections or report barriers. | Page edit links, email, and the accessibility issue route exist. | The general issue card is not linked, and response outcomes are not measured |
| The interface has strong automated accessibility assurance. | Static semantics, browser journeys, axe scans, and reflow checks enforce the documented automated contract. | No dated human screen-reader, zoom, or custom text-spacing pass is recorded |
| Generated output keeps structured source data and named sensitive patterns out. | Checks reject YAML artifacts, phone-number patterns, and PIN labels; owner review governs context. | Automation does not recognize every possible staff record or govern other City systems |
| Releases are reproducible. | Nested gates build and inspect source-derived output before GitHub Pages publication. | Outside font availability remains a manual visual check, not a release dependency |

## Nonfunctional requirements

### Clarity

Content must meet the repository style guide: lead with the point, use active
voice, prefer concrete language, define necessary terms, and avoid ornamental
formatting. A thoughtful reader outside OPI should be able to understand the
first screen of a canonical page without opening the glossary.

### Consistency

The same item must have the same name, type, owner meaning, and relationship
across navigation, landing pages, cards, definitions, and canonical pages.
Generated organization views must consume the same immutable data model.

### Maintainability

Navigation is section-local, repeated cards use structured card data, and page
metadata is inherited from the nearest section. Shared presentation behavior
belongs in shared components. Validation logic belongs in repository-tool
modules, not in thin command wrappers or the verification sequencer.

### Reliability

Strict builds, broken links, missing routes, unsafe artifacts, accessibility
failures, and contract drift must stop publication. External fonts may improve
appearance but must not be required to read or navigate the site.

### Security and privacy

The website has no accounts or application database. Dependencies remain
locked. The bounded manual Snyk command scans source; it does not establish
vulnerability coverage for uv-managed Python dependencies. Source and artifact
checks enforce their named patterns, while owner review governs contextual
source placement. Contribution guidance must tell people not to put sensitive
personal information in an issue.

### Performance

The static website should load without an application server and remain useful
when optional outside resources fail. New scripts, styles, or images must
justify their reader benefit and must not create a network dependency for a
core journey.

## Current assurance

| Area | Implemented evidence | Known gap |
| --- | --- | --- |
| Purpose and office model | Homepage, onboarding, section pages, glossary, and operating-model source align. | Audience priority and measured comprehension |
| Teams, services, and programs | Canonical sections, intentional navigation, metadata, and cross-links exist. | AdminOps routing and Citywide Data Network scope |
| Product catalog | Four OPI products have canonical pages and a shared landing page. | Open Baltimore classification, Data Platform users, BIC audience, and roadmap expectations |
| Findability | Navigation, breadcrumbs, search, cards, strict build, and built-link checks exist. | Ordinary-language search success, stale-bookmark recovery, and a task baseline |
| Contribution and governance | Edit and email paths, metadata, and review rules exist. | Inert general issue card, reader-visible metadata, and response measurement |
| Accessibility | A detailed standard and layered automated proof exist. | Dated human screen-reader, zoom, text-spacing, language-access, and browser-support decisions |
| Publishing and local use | GitHub Pages, Task, Docker Compose, strict builds, and nested gates share source. | One recorded duplicate hosted-policy invocation |
| Outcome measurement | Release quality and content freshness are observable. | Product outcomes, targets, collection purpose, retention, and privacy rules |

## Success measures

Success is a reader completing a meaningful task, not simply a page view. The
product should eventually measure the following outcomes:

1. A first-time reader can explain what OPI does and choose the correct section.
2. An agency partner can select the appropriate service or routine without
   relying on an OPI staff member to translate the website.
3. A reader can distinguish a team, service, program, and product and place a
   named item in the correct type.
4. A CitiStat participant can find the roles, preparation, artifacts, and
   follow-up expectations needed for the session.
5. A reader can reach an OPI product or maintained contact route without a dead
   end.
6. A contributor can report a specific error or barrier and understand what
   happens next.
7. Content owners can review stale pages before the next-review date.
8. A release can be reproduced locally and reaches GitHub Pages only after the
   required gate succeeds.
9. Readers using keyboard navigation, assistive technology, zoom, narrow
   screens, or either color scheme can complete the same core journeys.

The repository currently proves release quality and metadata coverage. It does
not collect product analytics or have owner-approved targets for the other
outcomes. Baselines, targets, collection methods, retention, and privacy rules
must be decided together before instrumentation is added. More tracking is not
a substitute for a clear decision about what OPI will learn and why.

## Product acceptance criteria

OPI Foundations is ready to publish a product change when:

1. The affected reader and journey are named.
2. The change belongs inside the product boundary and on the canonical page.
3. Team, service, program, and product terms remain consistent.
4. Navigation, cards, metadata, cross-links, and redirects move with any
   structural change.
5. The page states a useful next step and does not promise an undefined service,
   access path, owner, or outcome.
6. The content owner has reviewed every substantive business claim.
7. A visible or interactive change has before-and-after evidence and a product
   decision.
8. The proportionate automated gate passes once at the cheapest authoritative
   layer.
9. Structural or shared-interface changes receive the human accessibility
   review named in the accessibility service standard.
10. The pull request records the root cause, changed contract, review evidence,
    exact commands, and what each command proved.
11. Product requirements, user stories, onboarding, and maintainer guidance
    change in the same slice when their behavior or workflow changes.

## Open decisions

The following questions were found by comparing canonical pages. They are
deliberately not resolved in this document.

### Decision 1: Which audience receives first priority?

**Owner:** Executive Director

The homepage describes residents and partners, the mission names City agencies
and residents, onboarding also names OPI staff and maintainers, and maintainer
guidance adds Council and peer governments. All are valid audiences, but they
are not ranked. Priority matters when homepage space, navigation labels, and
content depth force a tradeoff.

The owner should name the primary audience, the next two audiences, and the
journeys that must never be displaced. Until then, product decisions should
serve the known audiences without claiming a priority order.

### Decision 2: Is AdminOps directly requestable?

**Owner:** Chief of Staff

AdminOps is one of OPI's five services, but
[How to Engage OPI](../docs/what-we-do/how-to-engage-opi.md) offers request paths
for the other four. The omission may be intentional because AdminOps serves the
office, or it may be a missing agency-partner route. Adding a contact path
without knowing the service boundary could create demand that OPI does not
intend to accept.

The owner should decide whether AdminOps has an external request path, an
OPI-staff route held elsewhere, or no direct intake.

### Decision 3: Is Open Baltimore a product, a program component, or both?

**Owner:** Deputy Chief Data Officer

The glossary calls Open Baltimore a City open-data portal product. The
[Open Data program](../docs/what-we-do/programs/open-data/index.md) describes it
as the platform through which the program publishes datasets. The products
landing page does not list it. Readers need to know whether this is an
intentional product-within-a-program relationship or a taxonomy contradiction.

The owner should decide the canonical type, accountable owner, and navigation
placement. The Open Data program page remains the maintained route until that
decision is recorded.

### Decision 4: What does the Citywide Data Network include?

**Owner:** Deputy Chief Data Officer

The canonical program page describes a broad partnership among agencies,
residents, civic technologists, universities, and peer governments. The
glossary describes a narrower interagency forum of data leaders, BCIT, and
partners. Those descriptions imply different membership and different reader
journeys.

The owner should decide whether they describe one program, separate parts of a
program, or two different things. The decision should name membership,
purpose, and how someone participates.

### Decision 5: Who can use the Baltimore Intelligence Center?

**Owner:** Deputy Chief Data Officer

The current pages refer to authorized users and governed City data, which is a
sound boundary but not a complete audience definition. The website does not say
which roles can use which capabilities, how access is decided, or which
capabilities are only conceptual.

The owner should define the intended audiences and the level of access detail
that belongs on this website. Detailed authorization rules should remain in the
system that enforces them.

### Decision 6: Who directly uses the Baltimore City Data Platform?

**Owner:** Deputy Chief Data Officer

The product page explains architecture, governance, and why the platform
matters, but the direct users and their core tasks are not explicit. A data
steward, analyst, product team, and executive reader have different needs.
Inventing one audience would distort both the page and any future requirements.

The owner should name the direct user groups, their primary tasks, and which
tasks belong in platform documentation outside OPI Foundations.

### Decision 7: What outcomes should OPI Foundations measure?

**Owner:** Executive Director, with the OPI Foundations Docs Maintainer

The repository can prove build quality, link integrity, accessibility
coverage, and ownership metadata. It does not define task-completion targets or
collect usage analytics. Instrumentation without a clear purpose would add
privacy and maintenance costs without proving that readers understand OPI.

The owner should choose a small set of outcomes, set baselines and targets, and
approve the collection, retention, access, and deletion rules before any
tracking code is added.

### Decision 8: What must every OPI product page say about ownership and roadmaps?

**Owner:** Chief of Staff, with each named product owner

The products landing page says a product has a roadmap, an owner, and users,
but individual pages do not consistently name all three. The Baltimore
Intelligence Center navigation also names an “Architecture and Roadmap” source
file whose rendered page contains architecture but no roadmap. A metadata
owner cannot safely stand in for product ownership.

The owners should decide the minimum product-page contract, whether roadmap
content belongs here or in another City system, and whether the Baltimore
Intelligence Center page should gain roadmap content or use an
architecture-only name.

### Decision 9: Should pages show their owner and review date?

**Owner:** Executive Director

The repository requires and validates ownership and review metadata for every
canonical page, but the rendered website does not show it. A visible treatment
could help readers judge freshness and direct corrections. It could also imply
business ownership or endorsement if the labels are not defined carefully.

The owners should decide whether to show the fields, what each label means, and
where the treatment belongs. Any implementation needs before-and-after design
review and must distinguish page maintenance from program, service, product,
and decision ownership.

### Decision 10: What language access should the website provide?

**Owner:** Executive Director

Residents are a named audience, but the product does not define priority
languages, translated journeys, translation ownership, update parity, or how a
reader requests language help. Adding isolated translated pages without a
maintenance model would create unequal and quickly stale experiences.

The owner should identify the journeys and languages to support, the qualified
translation and review process, and how translated pages remain aligned when
the English source changes.

### Decision 11: Which browsers and devices does OPI support?

**Owner:** Executive Director, with OPI Wiki maintainers

The automated browser proof uses pinned Chromium profiles and several
viewports. That is strong regression evidence for the tested engine, not a
support statement for Safari, Firefox, mobile assistive technology, or older
devices.

The owners should define the supported browser and device policy from reader
needs and City standards. Maintainers can then choose the smallest manual or
automated evidence set that proves that policy without multiplying the suite.

### Decision 12: Who is accountable for OPI Foundations product governance?

**Owner:** Executive Director

Older maintainer decisions refer to an “OPI Wiki product owner,” but no
canonical assignment defines the role holder, decision rights, or delegation.
Page metadata establishes content-review responsibility, and the Docs
Maintainer operates the repository; neither fact establishes accountable
product ownership.

The owner should name the accountable product owner and define which product,
design, and release decisions that person may delegate. Until then, the
Executive Director remains the required sign-off for structural changes, and
the OPI Foundations Docs Maintainer is the operational steward rather than an
inferred product owner.

## Maintaining this contract

Product requirements and user stories are living contracts. Update them in the
same pull request when a change adds or removes an audience, capability,
journey, service promise, or product boundary. A wording correction that does
not change behavior does not need a new requirement.

When an open decision is resolved, record the date, area, decision, rationale,
owner, and reversal condition in the maintainer guidance. Then update the
affected canonical pages and user stories in the same slice. Do not leave a
resolved question here as if it were still open.
