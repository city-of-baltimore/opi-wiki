# Maintainer's Operating Manual

This document is for the OPI Foundations docs maintainer. It describes the role, the weekly cadence, the editorial voice, and the systems involved.

## Contents

**The job** — [The role](#the-role) ·
[Weekly cadence](#weekly-cadence-suggested) ·
[The intake funnel](#the-intake-funnel) ·
[Tools the maintainer uses](#tools-the-maintainer-uses) ·
[Onboarding a new maintainer](#onboarding-a-new-maintainer) ·
[Bus factor mitigation](#bus-factor-mitigation)

**Writing and reviewing** — [Editorial voice](#editorial-voice) ·
[Repository source contract](#repository-source-contract) ·
[Cross-link discipline](#cross-link-discipline) ·
[Method and playbook maintenance check](#method-and-playbook-maintenance-check)

**Structure and navigation** — [Navigation ownership](#navigation-ownership) ·
[Section map: folder ↔ navigation label](#section-map-folder--navigation-label) ·
[Content taxonomy guardrails](#content-taxonomy-guardrails)

**Building a page** — [Landing-page cards](#landing-page-cards) ·
[Page headers](#page-headers) ·
[Headings](#headings) ·
[Page metadata blocks](#page-metadata-blocks) ·
[Structured page data](#structured-page-data) ·
[Page data model](#page-data-model)

**Keeping it current** — [Review-date enforcement](#review-date-enforcement) ·
[Staleness audit (quarterly)](#staleness-audit-quarterly)

**Build and verification** — [Build platform posture](#build-platform-posture) ·
[Verification and browser assurance](#verification-and-browser-assurance) ·
[Which gate runs what](#which-gate-runs-what) ·
[Advisory security scan](#advisory-security-scan)

**Recorded decisions** are kept next to the rule they explain rather than in one
log, in five groups —
[content labels and validation](#recorded-decisions--content-labels-and-validation) ·
[organization data](#recorded-decisions--organization-data) ·
[build platform](#recorded-decisions--build-platform) ·
[preview, browser assurance, accessibility](#recorded-decisions--preview-browser-assurance-accessibility) ·
[the platform gate](#recorded-decisions--the-platform-gate)

## The role

**Title:** OPI Foundations Docs Maintainer
**Effort:** 0.4–0.6 FTE (16–24 hours/week)
**Reports to:** Executive Director

**Primary responsibilities:**

1. Translate suggestions and source documents into Markdown that renders cleanly on the site.
2. Maintain editorial voice consistency across every page.
3. Run the contribution intake process: triage issues and email requests, draft changes, route for review, publish.
4. Keep the navigation (`docs/**/.pages`), glossary, and cross-links in sync as content evolves.
5. Quarterly: audit each page for staleness and route stale pages to their owners for review.

## Weekly cadence (suggested)

| Day | Work |
|---|---|
| Monday | Triage new issues and email requests; acknowledge each within 2 business days |
| Tuesday–Thursday | Draft changes in Markdown; open PRs; route to section owners |
| Friday | Merge reviewed PRs; review freshness and broken-link findings; plan next week. Review usage measures only after product Decision 7 defines them. |

## The intake funnel

```
Issue / Pull request / Email
         │
         ▼
  Maintainer triage
         │
         ├── Typo or small fix     → commit directly to main → auto-deploy
         ├── Substantive change    → branch → PR → section owner review → merge
         └── New section or major  → ED/CDO sign-off before merge
```

## Editorial voice

OPI Foundations is written for **city peers, partner agencies, council members, peer cities, and residents**. The voice is:

- **Plain.** No jargon without a glossary entry.
- **Concrete.** Specific examples beat abstract framings.
- **Active.** "OPI runs CitiStat sessions" not "CitiStat sessions are run by OPI."
- **Sourced.** Every factual claim about city operations should link to a source — a council document, an annual report, a stat brief, or a published City dataset.
- **Calm.** This is reference material, not marketing copy. No hype, no exclamation points.

When in doubt, model the voice on the [Letters from the Director](docs/about-us/letters-from-the-director/index.md). They're the canonical tone reference.

## Repository source contract

**Site source (this repo):**

- Methodology, strategy, operating model
- Briefs and website material
- Methods, service definitions, and the Glossary
- Letters from the Director
- Staff Guide material on onboarding, working norms, performance expectations,
  and leadership commitments
- Staff roster and role-summary index (names, working titles, team
  assignments, reporting relationships, and short role summaries)

**Long-term City-system homes (SharePoint and other owning systems):**

- Full Position Descriptions (with compensation or classification details)
- Performance records and signed evaluations
- MAPS Benefits guides
- Controlled HR forms, case-specific guidance, and staff intake records
- Telework Policy (formal HR doc)

The Staff Guide under `docs/how-we-work/handbook/` is part of the rendered Wiki.
The named section owner must review each page before it is published. The guide
may explain shared expectations and routines. Personnel records, contact lists,
controlled forms, and case-specific HR material stay in their owning City
systems.

When placement is unclear, **ask the section owner before adding the material**.
Every tracked file participates in repository review even when it sits outside
`docs/`.

When the source-language ratchet reports a line, replace generic
repository-state wording with the named reader, reviewer, owner, City system, or
concrete data rule; do not work around the matcher.

When the rendered-language ratchet reports a canonical route, start with the
named Markdown page and generated-HTML context. The text may come from a macro
or structured source, so artifact evidence remains authoritative even when one
Markdown line is not the origin. Do not invent a source location to silence the
finding.

### Recorded decisions — content labels and validation

- 2026-07-27 — **[CONTENT LABELS] keep generic repository-state labels and the
  former pill UI retired** — review belongs to the office release process, so
  source names the actual reader, reviewer, owner, City system, or data rule
  instead — owner: Executive Director/CDO — reversible only through a recorded
  product decision that defines a needed user-facing status model and its
  review, accessibility, and data semantics.

- 2026-07-27 — **[CONTENT VALIDATION] use source and rendered-artifact
  enforcement rather than a parallel Markdown parser** — the fast source
  ratchet gives pull-request feedback, while the existing strict build supplies
  the exact semantic artifact checked by the pre-push and deploy gate; neither
  layer silently substitutes for the other — owner: OPI wiki maintainers —
  reversible only when one layer is proven to subsume the other without adding
  a build, browser, or network step to hosted CI.

- 2026-07-30 — **[PRODUCT DOCUMENTATION] keep OPI Foundations requirements,
  user stories, and technical specification in root `product/`** — these are
  repository governance documents, not reader-facing Wiki content, and keeping
  them outside `docs/` prevents them from entering the MkDocs artifact or
  appearing as a fifth OPI product — owner: Executive Director (scope, pending
  Product Decision 12) and maintainers (maintenance) — reversible through an
  explicit product decision that defines a reader need and moves links,
  ownership, and navigation together.

## Cross-link discipline

The Reference section (`docs/resources/reference/`) is cross-cutting. Every section page should link to:

- The [Glossary](docs/resources/reference/glossary.md) when a term is first used in a section.
- [How Work Moves Through OPI](docs/how-we-work/how-work-moves-through-opi.md)
  when a page is about OPI's structure or describes team and service handoffs.

## Navigation ownership

Navigation is local to each section. Keep `mkdocs.yml` focused on site-wide
runtime settings, and update the nearest `docs/**/.pages` file whenever a page
is added, removed, renamed, or moved.

The Staff Guide contains reviewed onboarding, working norms, performance
expectations, and leadership commitments. Personnel records and contact data
belong in their owning City systems. The staff directory is limited to names,
working titles, team assignments, reporting relationships, and short role
summaries. Do not add payroll identifiers, compensation, classifications,
personnel status, phone numbers, individual email addresses, or controlled
working copies through navigation, redirects, raw data files, or generated
assets.

## Section map: folder ↔ navigation label

Navigation labels are set explicitly in each section's `.pages` `title:` field,
so a few folder names intentionally differ from the label readers see. Keep this
mapping in mind when locating content, and keep the `.pages` title, the
`index.md` H1, and this table in sync if a section is renamed.

| Folder | Navigation label | Notes |
|---|---|---|
| `about-us/our-teams/` | Our Teams | The four team pages live under About Us. |
| `about-us/our-teams/directors-office/` | Director's Office | The team that delivers the **AdminOps** operations and communications service. |
| `about-us/our-teams/performance/` | Performance | The team that delivers **Citywide Performance Management**; the **CitiStat** program itself lives in `what-we-do/programs/citistat/`. |
| `about-us/our-teams/data-and-analytics/` | Data and Analytics | The team that delivers **Citywide Data and Analytics**. |
| `about-us/our-teams/innovation-lab/` | Innovation Lab | Both a team and a service; the products it builds live in `what-we-do/products/`. |
| `how-we-work/organization/` | Organization | Leadership chart and team-purpose overview, generated from the limited organization data in `docs/_data/people.yml`. |
| `what-we-do/` | What We Do | OPI's services, programs, and products. |
| `what-we-do/programs/citistat/` | CitiStat | A **program** supported by all teams — its own section, not a team. |
| `what-we-do/products/` | Products | Tools and platforms OPI builds, including the Baltimore Intelligence Center. |
| `what-we-do/services/` | Services | The five services OPI delivers, including **Cross-Agency Delivery** — a service, not a staffed team. |
| `how-we-work/` | How We Work | Operating model, leadership structure, and the Staff Guide for OPI staff. |

### Check a new folder name against the ignore file first

A `docs/` folder name is two things at once: the public URL readers get, and an
ordinary path that `.gitignore` matches like any other. The managed ignore block
this repository carries from Patapsco holds **unanchored** directory patterns
for Python packaging output, so `build/` and `dist/` match at *any* depth.
`docs/build/` is ignored exactly as a root-level `build/` would be.

That combination fails in the worst direction. The pages are invisible to Git,
so they are never committed and never reach the checks, which read Git's view of
the tree. MkDocs reads the filesystem, so the section renders perfectly in
`task serve`. The author sees it working, the gate reports green, and the
section is simply absent from the published site.

`scripts/check_docs_folder_names.py` fails `task ci` on any such folder, so this
now surfaces while the section is being created rather than after it ships. To
check a candidate name by hand before committing to it:

```bash
git check-ignore -v docs/<candidate-name>/
```

No output means the name is free. Any output names the rule that would swallow
it — pick a different name. Prefer the word a reader should see in the URL;
lifecycle names like `develop/` read well beside the existing sections and
collide with nothing.

Anchoring those patterns locally is not the fix: the block is Patapsco's managed
baseline, and rewriting `build/` as `/build/` here makes `platform-check` report
the block as drifted. That change belongs upstream.

## Content taxonomy guardrails

OPI content sorts into exactly four types. Keep them distinct; do not let a page
silently reclassify one as another.

| Type | What it is | Members | Lives under |
|---|---|---|---|
| **Teams** | Groups with staff and budget (also called portfolios) | Director's Office, Performance, Data and Analytics, Innovation Lab | `about-us/our-teams/` |
| **Services** | What OPI delivers for the City | AdminOps, Citywide Performance Management, Citywide Data and Analytics, Innovation Lab, Cross-Agency Delivery | `what-we-do/services/` |
| **Programs** | Ongoing routines that may span teams | CitiStat, Data Governance, Open Data, Citywide Data Network | `what-we-do/programs/` |
| **Products** | Tools and platforms OPI builds | Baltimore Intelligence Center, Baltimore City Data Platform, Baltimore City Performance Portal, Baltimore 311 Explorer | `what-we-do/products/` |

Rules to enforce on every page:

- **Innovation Lab is deliberately both a team and a service.** That is not a
  duplication error — say so explicitly where it could confuse.
- **CitiStat is a program, not a team.** It is supported by all teams and owned
  by the CitiStat Director.
- **Cross-Agency Delivery is a service, not a staffed team.** There is no
  `about-us/our-teams/cross-agency-delivery/` directory — it activates through Tiger
  Teams and Innovation Lab projects.
- **Never write "CAD."** Spell out Cross-Agency Delivery; "x-agency delivery" is
  the only allowed short form.
- **Every canonical page names an owner and a review cadence** through the
  nearest `.metadata.yml` (`owner`, `last_reviewed`, `next_review`). New
  sections get their own `.metadata.yml`.

## Landing-page cards

Card grids on section landing pages are shared UI, not one-off HTML snippets.
Keep the card content in the nearest `*.cards.yml` file and render it through
the shared `card_grid_from(...)` macro so markup, link affordances, and
accessibility behavior stay consistent across sections.

Keep shared CSS split by responsibility too: design tokens, Material chrome
overrides, reusable components, and page-specific presentation should live in
separate files under `docs/assets/stylesheets/` so one-off tweaks do not drift
into the global theme surface.

## Page headers

Every content page opens with one `{{ page_header(...) }}` call placed directly
under the `# H1`. It renders an optional `category` eyebrow, `summary` lede, and
`tagline` as a single accessible block. Do not hand-build the old stack
(blockquote summary, bold kicker, a bold line restating the title, italic
tagline); that duplicated the title and split header styling three ways across
the corpus. Keep the page title as a single `# H1`. Section `index.md` landing
pages are the exception: they use a plain `>` blockquote summary.

## Headings

Use real Markdown headings (`##`, `###`, `####`) for section breaks — never a
bold-only paragraph. Bold-only "headings" don't appear in the table of contents,
aren't announced as headings by screen readers, and get no anchor link.

- Top-level page sections: `##`. (The old decorative `**■ Section**` style has
  been retired in favor of `## Section`.)
- Sub-sections nest with `###` / `####`.
- Keep **bold** for genuine inline emphasis, for short descriptive *deks* that
  sit directly under a heading, and for memo fields (`**To:**`, `**From:**`).
  A bold sentence or a one-line descriptor is not a heading.

## Page metadata blocks

Visible page front-matter (`VERSION`, `UPDATED`, `OWNER`, `AUDIENCE`,
`EFFECTIVE`, `REVIEW`) uses a Markdown definition list, not ad-hoc bold lines:

```markdown
VERSION
:   v1.0

OWNER
:   Director's Office
```

This renders as a semantic `<dl>`. (This visible block is distinct from the
build-time `.metadata.yml`, which drives ownership and review cadence.)

## Structured page data

When one page needs to repeat the same source-of-truth data across charts and
tables, keep that content in a shared YAML file and render it through a macro.
`docs/_data/people.yml` is deliberately limited to staff names, working titles,
canonical team identifiers, the nested reporting structure, each team's primary
value, and short role summaries. Reader-facing team labels are derived from those
identifiers instead of duplicated in source. One immutable typed record drives
the leadership chart, Team and Roles page, and inline `role_holder(...)`
references.

The organization loader is an exact allowlist, not a blacklist. Unknown fields,
missing or mistyped values, duplicate YAML keys, and drift from the four canonical
teams fail `scripts/check_organization_data.py` in hosted CI. The nested shape
makes reporting cycles unrepresentable; do not add `reports_to` references or
person IDs without an explicit data-model decision. The file must never carry
contractors, payroll identifiers, phone numbers, individual email addresses,
classifications, cost centers, personnel status, compensation, or full position
descriptions.

### Recorded decisions — organization data

- 2026-07-27 — **[ORGANIZATION DATA] defer disposition of `primary_value`** —
  the visible team summary was retired in commit `ee27304`, but its four
  substantive descriptions remain verbatim in source pending an Executive
  Director/CDO decision to restore, move, or retire them — reversible through
  that recorded owner decision.

## Page data model

Use each data shape intentionally:

- `.metadata.yml` for inherited owner, review cadence, and change-log fields.
- `*.cards.yml` for shared landing-page card content rendered through `card_grid_from(...)`.
- `*.data.yml` for page-local structured source data that needs to render into more than one repeated section.

Do not invent new adjacent file conventions casually. If a page needs a new shared data pattern, document it in this manual and `README.md` in the same change.

## Build platform posture

This repo currently runs on MkDocs 1.x and should stay there unless the team
makes a deliberate platform-migration decision.

Keep `mkdocs-redirects` pinned at `1.2.2` unless and until OPI explicitly
records a renderer-migration decision with the OPI Wiki maintainers. Version
1.2.3 adds `properdocs>=1.6.5` alongside `mkdocs>=1.2,<=1.6.1`; do not introduce
a second renderer through a routine dependency update.

If the team chooses another renderer later, treat it as a full platform change:

1. Confirm the target renderer and configuration contract.
2. Update local commands, CI, and preview/deploy scripts together.
3. Re-verify theme, plugins, redirects, and navigation behavior in one slice.

### Recorded decisions — build platform

- 2026-07-29 — **[BUILD PLATFORM] adopt security-patched Material and PyMdown
  while retaining MkDocs 1.x** — `mkdocs-material==9.7.7` fixes a DOM-based XSS
  in search suggestions, and `pymdown-extensions==11.0.1` includes the 11.0
  containment fix for CVE-2026-61632; this site does not enable
  `pymdownx.b64`, but it does not retain a known-vulnerable package. Material
  9.7.2 and later emit an MkDocs 2.0 incompatibility warning; keep that signal
  visible rather than setting `NO_MKDOCS_2_WARNING`. Material 9.7.7 still
  requires `mkdocs>=1.6,<2`, so this slice retains exact-pinned MkDocs 1.6.1
  and defers any renderer migration — owner: OPI Wiki maintainers — review
  before Material's scheduled November 5, 2026 end of life; reversible only to
  another patched, fully verified Material/MkDocs pairing or through a separate
  renderer-migration decision recorded by OPI Wiki maintainers, never by
  restoring the vulnerable pins.

## Review-date enforcement

`scripts/check_page_metadata.py` (run by verify, CI, and the deploy gate)
enforces the freshness contract, not just field presence:

- `last_reviewed` and `next_review` must be ISO dates (`YYYY-MM-DD`).
- `last_reviewed` cannot be in the future.
- `next_review` must not precede `last_reviewed` or be overdue.
- A scheduled review interval cannot exceed **200 days**. The explicit
  `next_review` date is the deadline, so a valid review round does not fail
  before its own scheduled date.

This is deliberate: the quarterly staleness audit below now has teeth. When a
review pass completes, bump the section's `last_reviewed`/`next_review` in one
sidecar edit.

## Staleness audit (quarterly)

Every quarter, run `task prepush` (which includes `mkdocs build --strict`) and audit:

1. Pages whose `next_review` date is approaching or overdue.
2. Pages whose linked source documents have been updated.
3. Pages with low traffic that may not be needed.

Email the relevant section owner with a one-line ask: "Is this still accurate? Any updates?"

## Verification and browser assurance

Every tier delegates to a structured Python verification runner, so maintainers
get per-step timing and failure summaries. If you need a machine-readable report
for CI or triage, call the runner directly:
`./scripts/verify.sh --json-output /path/to/report.json`.

For UI regressions that static checks will miss, maintainers run the pre-deploy
pass with `task validate`. It adds browser interaction checks and an axe-powered
audit of every canonical route at desktop and 320px reflow widths in both color
schemes. That pass expects a one-time local browser install via
`uv run playwright install chromium`. The service promise and required manual
review are documented in
[`docs/resources/accessibility.md`](docs/resources/accessibility.md).

`task validate` is the self-contained release proof; the live diagnostics are
its deliberate opposite, making real requests to a running preview. Both models,
and what each does and does not establish, are in
[`product/technical-spec.md`](product/technical-spec.md#static-and-live-browser-models);
the commands are in [the README](README.md#local-development). Live diagnostics
supplement `task validate` — they never replace its release evidence.

Two rules bind anyone changing the browser automation:

- **One readiness seam.** The hosted static gate scans every
  repository-automation module and fails a direct navigation call, a direct
  browser-context creation, or a `networkidle` wait that returns outside the
  shared seam. Readiness is a canonical load, visible rendered content, and
  settled font loading — never "the network went quiet".
- **Axe CSSOM preloading stays disabled.** Enabling it would synthesize fresh
  XHRs to the font stylesheets after the product page has loaded. Every
  release-critical stylesheet is already a target-owned artifact resource; do
  not hide analyzer traffic by allowing font-provider XHRs into the product
  resource contract.

### Recorded decisions — preview, browser assurance, accessibility

Each entry names the date, the decision, its rationale, its owner, and the
condition under which it can be reversed. Add to this list rather than editing
an entry: a superseded decision is annotated in place, not rewritten.

- 2026-07-28 — **[LOCAL PREVIEW] preserve the reader-visible canonical URL in
  Docker Compose** — MkDocs rewrites `site_url` to its container bind address
  during `serve`; `OPI_SITE_URL` plus `scripts/mkdocs_site_url.py` restores the
  validated `http://127.0.0.1:5208/opi-wiki/` origin so Material instant
  navigation remains same-origin — owner: OPI Wiki maintainers — reversible
  when MkDocs supports separate bind and reader-visible preview URLs natively,
  or when the Compose preview is deliberately retired. The wiring contract
  lives in `tests/test_mkdocs_site_url.py`.

- 2026-07-28 — **[BROWSER ASSURANCE] cap each canonical-route audit at 500
  routes** — the current 79-route site remains within the four-profile browser
  matrix's 600-second validation budget without making an unbounded route count
  look safe — owner: OPI Wiki maintainers — review as the site approaches 400
  canonical routes; reversible only by retiring or replacing the cap with
  measured sharding that keeps the four-profile matrix within a documented
  runtime budget.

- 2026-07-29 — **[BROWSER ASSURANCE] audit the strict build at its sitemap
  canonical origin inside Chromium** — hermetic Playwright request routing
  preserves the exact generated artifact and production same-origin behavior
  without a loopback-origin substitution, DNS, TLS, network access, or an HTML
  rewrite; unknown, unsafe, missing, and out-of-base requests fail locally —
  exact Adobe and Google font origins remain a narrow nonblocking dependency
  for font-related resource types so product workflows can be proven offline,
  while painted typeface and vendor availability remain manual design checks —
  owner: OPI Wiki maintainers — reversible only when a replacement proves the
  same exact-artifact, canonical-origin, isolation, and fail-closed guarantees.

- 2026-07-29 — **[ACCESSIBILITY] carry keyboard-only header controls into the
  render-backed redesign** — the current automated journeys prove the skip link,
  table focus, visible focus treatments, and pointer-opened navigation/search,
  but they do not yet prove keyboard activation of Material's label-based
  header toggles; changing those controls is a visible product decision, so do
  not weaken the service promise or disguise pointer coverage as keyboard
  evidence — owner: OPI Wiki product owner (design sign-off) and maintainers
  (implementation) — retire when navigation and search are traversable,
  operable, and visibly focused by keyboard at desktop and reflow widths, with
  before/after evidence and automated regression proof — **retired 2026-07-29:**
  the semantic civic header slice added native controls, responsive focus
  management, before/after evidence, and the focused browser proof.

- 2026-07-29 — **[HEADER] keep Material's hidden toggles as canonical state
  behind native civic controls** — Material 9.7.7's drawer, search, scroll lock,
  deep links, and presentation consume the existing checkbox and palette-radio
  state; the OPI adapter projects native activation into those controls and
  derives ARIA, inertness, breakpoint roles, route handoff, and focus behavior
  from the same state; this fixes semantics without forking the renderer or
  creating a second open/closed model — owner: OPI Wiki product owner (visible
  design) and maintainers (implementation) — reversible when Material exposes
  equivalent native-control hooks or a replacement proves the same
  controller-ready progressive enhancement, keyboard-native no-JavaScript
  top-level navigation, deliberate search suppression without its runtime,
  instant-navigation, focus, and search behavior.

- 2026-07-29 — **[BROWSER ASSURANCE] prove shared header behavior once at the
  cheapest authoritative layer** — one tiny rendered contract holds structure,
  names, relationships, and the search-disabled guard; one enhanced browser
  journey holds keyboard, geometry, focus, exact breakpoint handoffs, palette,
  search-shortcut, and repeated instant navigation; one JavaScript-disabled
  context holds the visible, keyboard-native top-level navigation fallback,
  rejects hidden drawer focus stops, and proves safe search suppression; the
  existing route-wide axe matrix retains contrast, semantics, and reflow
  coverage, while its route loop checks only the active-link treatment that
  actually varies — owner: OPI Wiki maintainers — reversible only to a
  measured proof with equal risk coverage and no slower duplicated route or
  color-scheme work.

- 2026-07-29 — **[BROWSER ASSURANCE] sample responsive focus after the
  controller's complete frame sequence** — browser rendering evaluates
  media-query changes before animation-frame callbacks, so a two-frame test
  wait registered before the change can resolve immediately before the
  controller's own second frame; issue the breakpoint requests back-to-back,
  drain three frames, and assert only the final user-visible focus outcome
  because the browser may coalesce the intermediate rendering state — owner:
  OPI Wiki maintainers — reversible when the controller no longer uses a
  two-frame focus handoff or exposes a narrower completion signal.

- 2026-07-29 — **[HOME HERO] scale the homepage heading fluidly without changing
  its content hierarchy** — Material's inherited emergency word wrapping split
  “Foundations” inside the word when fixed 48px type met the hero's 240px
  content measure at 320px; a bounded `clamp()` keeps the existing 48px desktop
  direction and gives the word enough room at reflow widths without changing
  the copy, padding, gradient, eyebrow, summary, or global heading system — one
  existing browser-smoke gate measures the rendered word fragments and hero
  bounds at 320px, 390px, and 1440px without adding a context, route crawl, or
  gate — owner: OPI Wiki product owner (visible design) and maintainers
  (implementation) — reversible only to a replacement that preserves intact
  heading words, viewport bounds, and the existing desktop composition.

- 2026-07-29 — **[HOME ACTIONS] retire the hero-overlay placement hold** — the
  product owner selected a labeled neutral utility row beneath the hero, so the
  earlier hold's retirement condition is met in the same slice that proves
  accessible naming, keyboard focus, target size, contrast, and responsive
  placement — owner: OPI Wiki product owner and maintainers — reversible only
  if a later owner decision explicitly reopens placement and preserves those
  guarantees.

- 2026-07-29 — **[HOME TOOLS] place contribution utilities in a labeled
  homepage-only row beneath the hero** — Material inserts its compact icon-only
  actions before page content; the homepage's negative hero offset therefore
  pulled those actions onto a dark gradient, where their placement, contrast,
  target size, and purpose were weak. A per-page Material template now keeps
  ordinary article actions unchanged while presenting native “Edit this page”
  and “View source” links on the neutral surface immediately below the hero.
  The links continue to derive from MkDocs' canonical edit URL; no repository
  URL, duplicate state, global dependency override, or DOM-moving JavaScript
  was introduced — owner: OPI Wiki product owner (visible design) and
  maintainers (implementation) — reversible to another owner-approved
  treatment only when it retains correct destinations, visible naming,
  keyboard order and focus, 44px targets, scheme contrast, and proven
  320px/390px/1440px placement.

- 2026-07-29 — **[BROWSER ASSURANCE] confine fractional-edge tolerance to the
  post-navigation content target** — in Chromium's JavaScript-disabled 320 ×
  800 journey, native focus scrolling placed the new 44px edit target at
  756.203–800.203 CSS pixels after reaching it from the exact top-level header
  sequence. A one-pixel tolerance recognizes subpixel layout without accepting
  a hidden target; every header focus stop retains exact viewport containment
  — owner: OPI Wiki maintainers — reversible when browser focus scrolling
  produces integer edge geometry or the post-navigation target no longer sits
  at the document's scroll boundary.

## Which gate runs what

`Taskfile.yml` exposes the tiers; `scripts/verify.py` defines the suite once and
runs it in three nested tiers. `task ci` is the fast static pass and the only
thing pull-request CI runs; `task prepush` is the pre-push hook; `task validate`
runs before a release and as the Pages deploy gate. Each tier is a strict prefix
of the next, so nothing is lost by moving a check down a tier — it runs later,
not never.
[`product/technical-spec.md`](product/technical-spec.md#verification-architecture)
lists the exact membership of each tier.

Pull-request CI is deliberately lean — **no test suite, no site build, no
browser** — per section 4 of the civic-app consistency standard.
`scripts/check_hosted_ci_policy.py` fails the build if that ever regresses,
including through indirection: it statically resolves both the `Taskfile.yml`
task graph and the `verify.py` plans, so adding a heavy step to any task `ci`
reaches is caught.

The guard also holds the exact ordered shape of `.github/workflows/ci.yml`, the
Taskfile top level, the `ci` task, and the resolved plan in
`scripts/repo_tools/hosted_ci_contract.py`. The workflow action identities,
steps, job properties, and command cardinality are fixed; action revisions may
move only between full commit SHAs. Taskfile-global `env`, `dotenv`, `includes`,
or `vars` are not permitted because they can reinterpret every task before the
task-local contract sees it. An intentional hosted static-check or action change
updates its behavior and the independent contract together; missing, extra,
duplicated, reordered, skipped, ignored, or otherwise modified work is a
failure by design.

The `ci` plan also runs Patapsco's published `platform-check`
(`baltimore-patapsco`, exact-pinned in the dev group), which checks the shared
app marker, task surface, tooling configuration, ignore-file baseline, workflow
shapes, and pre-push hook that apply to this docs site. `task ci:policy` invokes
it directly as well, exactly as it already did the local guard: the estate
proves a hosted gate reaches a policy command by walking `task` edges and cannot
see inside a Python plan module, so the ordinary Taskfile edge is what makes
this gate visible from outside. Keep **both**. `platform-check` 0.9.9 does
not expand `verify.py` plans (it expands `npm` and `.sh` bodies, but not a
Python plan module), has no job-timeout rule, and has no `run:` allowlist, so it
returns "conforms" for all four remaining violations the local guard fails on.
The comparison runs both ways: the 0.4.1 sweep caught two
Taskfile forms the local guard missed — a block-list `deps:` and a `silent: true`
task — which are now fixed and regression-tested here, and the 0.4.3 sweep found
a third — a new `.sh` in the task chain that runs a forbidden command directly —
which is also fixed and regression-tested here. 0.6.17 closed a fourth: the
unpinned `uses:` case was retired from the differential matrix at this bump
because the shared checker now reports it. The measured gaps, and the
condition for deleting the local guard — still unmet at 0.9.9 — are recorded in
the "Two checkers" note in `scripts/repo_tools/hosted_ci_policy.py`.

`scripts/check_platform_guard_evidence.py` runs before `platform-check` in the
hosted tier. It requires one exact Patapsco pin, a dedicated Dependabot update
group, and coordinated current-measurement references. Updating the marker is a
maintainer attestation, not execution proof. The pre-push suite runs
`tests/test_platform_guard_differential.py` against the installed release and
must pass before the change can be pushed or deployed.

### Recorded decisions — the platform gate

- 2026-08-31 — **[PLATFORM GATE] adopt Patapsco 0.9.9 after a tenth
  differential re-measurement** — the estate advanced 0.7.2 -> 0.9.9 (Bromo
  0.54.0). Measured before adopting, exactly as every prior bump: all four
  injected evasion cases are **still MISSED** by the shared checker in their
  ordinary form, and both control cases are still CAUGHT. The local guard
  therefore stays. The root cause is unchanged and is now ten releases old — a
  Python plan module is an opaque leaf to the shared resolver — so this is a
  re-confirmation, not a new finding.

  Recorded separately rather than by editing the 2026-08-14 entry. That entry
  is about 0.7.2 and stays about 0.7.2: a dated decision record answers "what
  did we know, and when", and a version bump applied to it with find-and-replace
  destroys the only thing it was keeping. That is precisely what happened here
  and had to be reverted — in the one repository whose entire local guard exists
  because version claims cannot be taken on trust.

- 2026-08-14 — **[PLATFORM GATE] adopt Patapsco 0.7.2 after differential
  re-measurement** — two releases in one bump. 0.7.1 is a pure BOM advance
  carrying Bromo 0.40.0, which this repo does not consume, and states of itself
  that no rule or contract behaviour changed. 0.7.2 carries Bromo 0.42.0 and is
  the larger of the two: a BOM/release coupling gate, a contracts-provenance
  line on every report, `--pristine` estate scanning, and three fixes (npm
  origin no longer conflated with version, `pages-deploy` trigger, documentation
  held to `contracts/`). Estate hygiene and reporting throughout; no new
  task-resolution capability, and nothing that teaches the shared resolver to
  read a Python aggregate. All four injected cases re-measured against the
  installed 0.7.2: still blocked by the local guard, still missed by
  `platform-check`. Matrix 6/6.
- 2026-08-12 — **[PLATFORM GATE] adopt Patapsco 0.7.0 after differential
  re-measurement** — the 0.6.24 → 0.7.0 delta is the two-compiler TypeScript
  transition (`tooling_typescript` reshaped; `typescript_api` added to the BOM
  schema), compiler governance a MkDocs repo does not consume; no new
  task-resolution capability. All four injected cases re-measured against the
  installed 0.7.0: still blocked by the local guard, still missed by
  `platform-check`. Matrix 6/6.
- 2026-08-10 — **[PLATFORM GATE] adopt Patapsco 0.6.24 after differential
  re-measurement** — seven releases in one bump; 0.6.18 through 0.6.24 are BOM
  advances carrying Bromo 0.37.0 → 0.39.1, which this repo does not consume, plus
  two estate hygiene rules that do apply. `version_claims` (0.6.19) requires
  `README.md` and `AGENTS.md` to each carry one visible `**Platform baseline:**`
  line naming the pin, and absence is a finding — both were missing, which is the
  exact state that let `orf-portal` advertise 0.4.1 across the whole 0.6 line.
  `dependabot_posture` (0.6.19–0.6.21) requires the `uv` ecosystem to fence the
  semver-major *class*; this repo fenced packages by name only. The matrix was
  re-measured after those three fixes, not before: an unconforming control makes
  every case fail for the wrong reason. Result — the control conforms and
  `platform-check` still returns "conforms" on all four cases the local guard
  catches, so both checkers stay and the retirement condition remains unmet —
  owner: OPI wiki maintainers — reversible by repinning the prior release and
  restoring its lock, marker, and evidence claims in one reviewed slice.
- 2026-08-07 — **[PLATFORM GATE] adopt Patapsco 0.6.17 after differential
  re-measurement** — the unmodified control conformed and the matrix still
  proves the local guard catches what the shared checker misses, so both stay.
  Three things changed with the bump: the unpinned-`uses:` case was **retired**
  (0.6.17 catches it, so the matrix is four cases, not five); `platform-check`
  moved out of the `verify.py` plan into the `ci:policy` task, because the
  estate's enforcement rule follows `task` edges and cannot see into a Python
  plan module; and `deploy.yml` is now declared `pages-deploy` and held to that
  shape — workflow-level Pages grants removed, the two write grants scoped to
  the environment-bound deploy job, and the build job's gate raised from
  `task prepush` to `task validate`, the pre-mutation boundary — owner: OPI wiki
  maintainers — reversible by repinning the prior release and restoring its
  lock, workflow, and evidence claims in one reviewed slice.

- 2026-07-27 — **[PLATFORM GATE] isolate and re-measure every Patapsco bump** —
  policy-gate changes must arrive separately from routine tooling and preserve
  the differential evidence, whatever its current case count — owner: OPI wiki
  maintainers — reversible when Patapsco catches the complete matrix and the
  local guard is retired under its documented condition.

- 2026-07-30 — **[PLATFORM GATE] adopt Patapsco 0.4.8 after differential
  re-measurement** — the candidate's unmodified control conformed, and the
  seven-test matrix proved that the local guard still catches all five injected
  violations while the shared checker misses them; retain both checkers while
  accepting 0.4.8's stronger structural pre-push and manifest-aware npm
  resolution — owner: OPI wiki maintainers — reversible by repinning the prior
  release and restoring its lock and evidence claims in one reviewed slice.

- 2026-07-29 — **[DOCS-SITE PORTS] bridge the shared enforcement gap locally**
  — Patapsco 0.4.8 treated `docs-site` as a non-application kind, so neither its
  registry slot nor its compose/loopback rules ran here; the fast
  browser-readiness contract therefore pins the slot-8 MkDocs default and task
  command, exact Compose service, container bind, and Docker startup and health
  behavior — owner: OPI Wiki maintainers (local contract) and Patapsco
  maintainers (shared rule) — retire the local port checks only when the shared
  checker covers port-owning docs sites and this repository re-measures the
  adopting pin.
  **Partly superseded at 0.6.17 (2026-08-07):** the registry slot rule now does
  run for `docs-site` — app name, kind, and the slot-8 frontend port are checked
  against `contracts/ports.toml`. The compose/loopback service, the container
  bind, and Docker startup and health are still uncovered upstream, so the local
  contract stays for those and its port assertions are now a corroborating
  second reading rather than the only one.

**The practical consequence: a broken test or strict build is not caught on the
PR; it surfaces at `git push` (via the hook) or on the deploy run after merge.**

Install the hook once per clone:

```bash
task setup
```

`git push --no-verify` skips it entirely. With tests out of hosted CI, that flag
is the one way a broken suite reaches `main` unnoticed — use it knowingly.

### If a hosted run looks stuck

Every hosted job declares `timeout-minutes`, and every verification step is
bounded by `--step-timeout` (600 seconds by default), so a hang fails with a
named step rather than burning GitHub's six-hour default. Progress lines are
flushed as they happen, so the live log always shows which step is running.
If a run still looks stuck, the last flushed `[n/m] <step>...` line names it.

## Advisory security scan

`./scripts/security_snyk.sh` runs a manual Snyk source-code scan. It is in no
gate by design (Snyk plans cap scan counts), and it does not cover this repo's
uv-managed Python dependencies. Confirm any server-side dependency integration
in Snyk before relying on it; repository configuration alone does not prove
that coverage. See `patapsco/docs/operations/snyk-scanning.md`.

## Bus factor mitigation

This role has a high bus factor by design (it's one person). Mitigations:

1. **Backup maintainer.** A second person trained on the systems but not actively maintaining. Quarterly: run a "could you take over tomorrow?" check-in.
2. **All editorial decisions are written down.** Voice, conventions, structural rules — all in this document. No tribal knowledge.
3. **Vacation coverage.** A two-week vacation should not break the wiki. Section owners with write access can publish urgent fixes in maintainer's absence.

## Tools the maintainer uses

| Tool | Purpose |
|---|---|
| GitHub Enterprise (this repo) | Source of truth, version control, CI/CD |
| uv | Python dependency and environment management |
| MkDocs Material | Site renderer (local preview + production build) |
| `task` ([Taskfile](https://taskfile.dev)) | The command surface: `task prepush` is the standard local pass, `task ci` the PR-CI subset, `task validate` the pre-deploy pass. `task --list` shows the rest |
| `./scripts/security_snyk.sh` | Manual, advisory Snyk source scan (never a gate) |
| Pandoc | Convert .docx → Markdown when migrating Drive content |
| VS Code (or any Markdown editor) | Authoring |
| Google Drive | Read-access to the OPI Foundations folder for source materials |
| SharePoint | Read access to source material maintained in that system |

## Onboarding a new maintainer

Day 1: read [`onboarding.md`](onboarding.md), this document, and
`CONTRIBUTING.md`. Run `task setup` then `task serve` locally. Read every page
on the live site.

Week 1: shadow the previous maintainer through one full intake cycle (issue → PR → merge → deploy).

Week 2: handle the next intake cycle solo, with the previous maintainer reviewing PRs.

Week 3+: independent.

## Method and playbook maintenance check

When reviewing method pages, confirm that each method has a clear source of truth and does not drift across the wiki. In particular:

- Tiger Team language should defer to the Tiger Teams Playbook.
- CitiStat language should defer to the CitiStat Method Playbook and portfolio register.
- Innovation Lab language should defer to About the Innovation Lab and the
  Digital Product Methodology.
- Cross-Agency Delivery language should defer to its service overview and
  service definition.
- Template pages should explain structure without copying system locations,
  contact lists, or controlled working copies.
