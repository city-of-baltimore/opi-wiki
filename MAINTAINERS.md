# Maintainer's Operating Manual

This document is for the OPI Foundations docs maintainer. It describes the role, the weekly cadence, the editorial voice, and the systems involved.

## The role

**Title:** OPI Foundations Docs Maintainer
**Effort:** 0.4–0.6 FTE (16–24 hours/week)
**Reports to:** Executive Director

**Primary responsibilities:**

1. Translate suggestions and source documents into Markdown that renders cleanly on the site.
2. Maintain editorial voice consistency across every page.
3. Run the contribution intake process: triage issues and Google Form submissions, draft changes, route for review, publish.
4. Keep the navigation (`docs/**/.pages`), glossary, and cross-links in sync as content evolves.
5. Quarterly: audit each page for staleness and route stale pages to their owners for review.

## Weekly cadence (suggested)

| Day | Work |
|---|---|
| Monday | Triage new issues + Google Form submissions; respond to acknowledge each within 2 business days |
| Tuesday–Thursday | Draft changes in Markdown; open PRs; route to section owners |
| Friday | Merge reviewed PRs; review metrics (page views, search queries, broken links); plan next week |

## The intake funnel

```
Issue / Google Form / Comment / Email
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
- Staff roster and role-summary index (names, working titles, team
  assignments, reporting relationships, and short role summaries)

**Long-term City-system homes (SharePoint and other owning systems):**

- Onboarding working materials
- Full Position Descriptions (with compensation or classification details)
- Performance records and signed evaluations
- MAPS Benefits guides
- Staff SOPs and intake queues
- Telework Policy (formal HR doc)

The existing `docs/how-we-work/handbook/` files are a bounded holding area while
their owners decide the long-term City-system destination. They remain tracked
source, and MkDocs excludes them from the generated site. Do not add new staff
working material to that folder.

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

## Cross-link discipline

The Reference section (`docs/resources/reference/`) is cross-cutting. Every section page should link to:

- The [Glossary](docs/resources/reference/glossary.md) when a term is first used in a section.
- [How Work Moves Through OPI](docs/how-we-work/how-work-moves-through-opi.md)
  when a page is about OPI's structure or describes team and service handoffs.

## Navigation ownership

Navigation is local to each section. Keep `mkdocs.yml` focused on site-wide
runtime settings, and update the nearest `docs/**/.pages` file whenever a page
is added, removed, renamed, or moved.

The existing Handbook folder is the only bounded holding area for onboarding and
staff operating material pending owner placement; do not expand it. Personnel
records and contact data belong in their owning City systems. The staff
directory is limited to names, working titles, team assignments, reporting
relationships, and short role summaries. Do not add payroll identifiers,
compensation, classifications, personnel status, phone numbers, individual
email addresses, or controlled working copies through navigation, redirects,
raw data files, or generated assets.

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
| `how-we-work/` | How We Work | Operating model and leadership structure. The source-only Handbook holding area is excluded from the generated site pending an owner placement decision. |

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

`task validate` is self-contained: it performs the strict build, reads the
production canonical origin from the built `sitemap.xml`, and mounts the exact
artifact at that origin inside Chromium through hermetic Playwright request
routing. The static audit starts no server, makes no DNS, TLS, or network
request, and does not rewrite generated HTML. Requests outside the exact
canonical origin and deployment base, unsafe paths, unsupported methods, and
files absent from the artifact receive a local failure. For a diagnostic
against an already-running `task serve` or Docker Compose preview, run:

```bash
uv run python scripts/check_browser_smoke.py \
  --base-url http://127.0.0.1:5208/opi-wiki/
uv run python scripts/check_browser_accessibility.py \
  --base-url http://127.0.0.1:5208/opi-wiki/
```

Each live command reads the route manifest from that preview's own
`sitemap.xml`; a missing, malformed, redirected, empty, or oversized manifest
fails closed. Do not edit source files until both live checks finish; each run
uses the fixed route list represented by the manifest it loaded at startup.
MkDocs live reload intentionally keeps network activity open, so the suites use one
shared readiness seam: canonical HTTP load, visible rendered content, settled
font loading; smoke workflows add a target-specific marker for Material instant
navigation. Unlike the hermetic static audit, these commands make real requests
to the running preview named by `--base-url`. The audit context aborts only its
own same-origin numeric `/livereload/` XHR so a canonical crawl cannot
accumulate MkDocs' 60-second polling threads; ordinary preview browsers keep
live reload.
The hosted static gate scans every repository-automation module and prevents
direct navigation calls, direct browser-context creation, or a `networkidle`
wait from returning outside that seam. The hermetic pass treats Adobe and Google
font endpoints as unavailable. Exact HTTPS font-provider origins are
nonblocking only for font, stylesheet, or image requests; every other external
dependency, product-owned HTTP error, and non-cancellation transport failure
remains blocking. Only an aborted target-owned search index and the live
preview's same-origin, numeric `/livereload/` XHR are recognized browser
cancellations.
Axe CSSOM preloading stays disabled because it would synthesize its own XHRs to
those font stylesheets after the product page has loaded. Every release-critical
stylesheet is already a target-owned artifact resource; do not hide analyzer
traffic by allowing font-provider XHRs in the product resource contract.
The automation does not assert which typeface Chromium painted or whether a
vendor delivered it; that remains a manual design check. Live diagnostics
supplement `task validate`; they do not replace its release evidence.

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

### Which gate runs what

`Taskfile.yml` exposes the tiers; `scripts/verify.py` defines the suite once and
runs it in three nested tiers:

| Tier | Where | Covers |
|---|---|---|
| `task ci` | pull-request CI, fast local loop | hosted-CI policy guard, browser-readiness contract, platform-gate evidence, format, lint, mypy, bandit, metadata, organization data, brand terms, style, consistency, raw HTML links |
| `task prepush` | the pre-push hook and the Pages deploy gate | everything above, plus pytest, `mkdocs build --strict`, rendered-language assurance, built-artifact safety and built-link checks, and accessibility checks |
| `task validate` | locally, before a deploy | everything above, plus browser interaction and full-route WCAG assurance |

Each tier is a strict prefix of the next, so nothing is lost by moving a check
down a tier — it runs later, not never.

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
app marker, task surface, tooling configuration, and pre-push hook that apply
to this docs site. Keep **both**. `platform-check` 0.4.5 does
not expand `verify.py` plans (it expands `npm` and `.sh` bodies, but not a
Python plan module), has no job-timeout rule, and has no `run:`/`uses:`
allowlist, so it returns "conforms" for all five violations the local
guard fails on. The comparison runs both ways: the 0.4.1 sweep caught two
Taskfile forms the local guard missed — a block-list `deps:` and a `silent: true`
task — which are now fixed and regression-tested here, and the 0.4.3 sweep found
a third — a new `.sh` in the task chain that runs a forbidden command directly —
which is also fixed and regression-tested here. The measured gaps, and the
condition for deleting the local guard — still unmet at 0.4.5 — are recorded in
the "Two checkers" note in that module's docstring.

`scripts/check_platform_guard_evidence.py` runs before `platform-check` in the
hosted tier. It requires one exact Patapsco pin, a dedicated Dependabot update
group, and coordinated current-measurement references. Updating the marker is a
maintainer attestation, not execution proof. The pre-push suite runs
`tests/test_platform_guard_differential.py` against the installed release and
must pass before the change can be pushed or deployed.

- 2026-07-27 — **[PLATFORM GATE] isolate and re-measure every Patapsco bump** —
  policy-gate changes must arrive separately from routine tooling and preserve
  the five-case differential evidence — owner: OPI wiki maintainers —
  reversible when Patapsco catches the complete matrix and the local guard is
  retired under its documented condition.

- 2026-07-29 — **[DOCS-SITE PORTS] bridge the shared enforcement gap locally**
  — Patapsco 0.4.5 treats `docs-site` as a non-application kind, so its registry
  slot and compose/loopback rules do not run here; the fast browser-readiness
  contract therefore pins the slot-8 MkDocs default and task command, exact
  Compose service, container bind, and Docker startup and health behavior —
  owner: OPI Wiki maintainers (local contract) and Patapsco maintainers (shared
  rule) — retire the local port checks only when the shared checker covers
  port-owning docs sites and this repository re-measures the adopting pin.

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

### Advisory security scan

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
