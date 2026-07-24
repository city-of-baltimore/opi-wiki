# Maintainer's Operating Manual

This document is for the OPI Foundations docs maintainer. It describes the role, the weekly cadence, the editorial voice, and the systems involved.

## The role

**Title:** OPI Foundations Docs Maintainer
**Effort:** 0.4–0.6 FTE (16–24 hours/week)
**Reports to:** Executive Director

**Primary responsibilities:**

1. Translate suggestions and source documents into Markdown that renders cleanly on the site.
2. Maintain editorial voice consistency across every page.
3. Run the contribution intake process: triage issues and Google Form submissions, draft changes, route for approval, publish.
4. Keep the navigation (`docs/**/.pages`), glossary, and cross-links in sync as content evolves.
5. Quarterly: audit each page for staleness and route stale pages to their owners for review.

## Weekly cadence (suggested)

| Day | Work |
|---|---|
| Monday | Triage new issues + Google Form submissions; respond to acknowledge each within 2 business days |
| Tuesday–Thursday | Draft changes in Markdown; open PRs; route to section owners |
| Friday | Merge approved PRs; review metrics (page views, search queries, broken links); plan next week |

## The intake funnel

```
Issue / Google Form / Comment / Email
         │
         ▼
  Maintainer triage
         │
         ├── Typo or small fix     → commit directly to main → auto-deploy
         ├── Substantive change    → branch → PR → section owner approves → merge
         └── New section or major  → ED/CDO approves before merge
```

## Editorial voice

OPI Foundations is written for **city peers, partner agencies, council members, peer cities, and the public**. The voice is:

- **Plain.** No jargon without a glossary entry.
- **Concrete.** Specific examples beat abstract framings.
- **Active.** "OPI runs CitiStat sessions" not "CitiStat sessions are run by OPI."
- **Sourced.** Every factual claim about city operations should link to a source — a council document, an annual report, a stat brief, or a public dataset.
- **Calm.** This is reference material, not marketing copy. No hype, no exclamation points.

When in doubt, model the voice on the [Letters from the Director](docs/about-us/letters-from-the-director/index.md). They're the canonical tone reference.

## What goes here vs. SharePoint

**Public Foundations site (this repo):**

- Methodology, strategy, operating model
- Public briefs and website material
- Public methods, service definitions, and the Glossary
- Letters from the Director
- Position Descriptions Index (titles + summaries)

**City of Baltimore intranet (SharePoint):**

- Onboarding checklists (with PII)
- Full Position Descriptions (with compensation)
- Performance Standards (signed)
- MAPS Benefits guides
- Internal SOPs and intake queues
- Telework Policy (formal HR doc)

When publication posture is unclear, **ask the section owner and do not publish
until they confirm**. A public repository is itself a publication surface even
when a file is outside `docs/`.

## Cross-link discipline

The Reference section (`docs/resources/reference/`) is cross-cutting. Every section page should link to:

- The [Glossary](docs/resources/reference/glossary.md) when a term is first used in a section.
- [How Work Moves Through OPI](docs/how-we-work/how-work-moves-through-opi.md)
  when a page is about OPI's structure or describes team and service handoffs.
- The [Strategic Priorities](docs/resources/reference/strategic-priorities-one-pager.md) when a page connects to current FY priorities.

## Navigation ownership

Navigation is local to each section. Keep `mkdocs.yml` focused on site-wide
runtime settings, and update the nearest `docs/**/.pages` file whenever a page
is added, removed, renamed, or moved.

Internal operating guidance, onboarding material, personnel records, and
contact data belong in SharePoint or the appropriate City system. Do not add
those collections under `docs/` or expose them through public navigation,
redirects, raw data files, or generated assets.

## Section map: folder ↔ navigation label

Navigation labels are set explicitly in each section's `.pages` `title:` field,
so a few folder names intentionally differ from the label readers see. Keep this
mapping in mind when locating content, and keep the `.pages` title, the
`index.md` H1, and this table in sync if a section is renamed.

| Folder | Navigation label | Notes |
|---|---|---|
| `about-us/our-teams/` | Our Teams | The four team pages live under About Us. |
| `about-us/our-teams/directors-office/` | Director's Office | The team that delivers the **AdminOps** service (operating backbone). |
| `about-us/our-teams/performance/` | Performance | The team that delivers **Citywide Performance Management**; the **CitiStat** program itself lives in `what-we-do/programs/citistat/`. |
| `about-us/our-teams/data-and-analytics/` | Data and Analytics | The team that delivers **Citywide Data and Analytics**. |
| `about-us/our-teams/innovation-lab/` | Innovation Lab | Both a team and a service; the products it builds live in `what-we-do/products/`. |
| `how-we-work/organization/` | Organization | Public leadership chart and team-purpose overview, generated from the limited public organization data in `docs/_data/people.yml`. |
| `what-we-do/` | What We Do | Services, programs (CitiStat and portfolio), and products (Baltimore Intelligence Center). |
| `what-we-do/programs/citistat/` | CitiStat | A **program** supported by all teams — its own section, not a team. |
| `what-we-do/products/` | Products | Tools and platforms OPI builds, including the Baltimore Intelligence Center. |
| `what-we-do/services/` | Services | The five services OPI delivers, including **Cross-Agency Delivery** — a service, not a staffed team. |
| `how-we-work/` | How We Work | Public operating model and leadership structure. Internal operating guidance remains in SharePoint and is not published here. |

## Content taxonomy guardrails

OPI content sorts into exactly four types. Keep them distinct; do not let a page
silently reclassify one as another.

| Type | What it is | Members | Lives under |
|---|---|---|---|
| **Teams** | Groups with staff and budget (also called portfolios) | Director's Office, Performance, Data and Analytics, Innovation Lab | `about-us/our-teams/` |
| **Services** | What OPI delivers for the City | AdminOps, Citywide Performance Management, Citywide Data and Analytics, Innovation Lab, Cross-Agency Delivery | `what-we-do/services/` |
| **Programs** | Ongoing routines that may span teams | CitiStat | `what-we-do/programs/` |
| **Products** | Tools and platforms OPI builds | Baltimore Intelligence Center, Baltimore City Data Platform, Baltimore City Performance Portal | `what-we-do/products/` |

Rules to enforce on every page:

- **Innovation Lab is deliberately both a team and a service.** That is not a
  duplication error — say so explicitly where it could confuse.
- **CitiStat is a program, not a team.** It is supported by all teams and owned
  by the CitiStat Director.
- **Cross-Agency Delivery is a service, not a staffed team.** There is no
  `about-us/our-teams/cross-agency-delivery/` directory — it activates through Tiger
  Teams and Innovation Lab projects.
- **Never write "CAD."** Spell out Cross-Agency Delivery; "x-agency delivery" is
  the only approved short form.
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
under the `# H1`. It renders the canonical intro — the status badge plus an
optional `category` eyebrow, `summary` lede, and `tagline` — as a single
accessible block. Do not hand-build the old stack (badge macro, blockquote
summary, bold kicker, a bold line restating the title, italic tagline); that
duplicated the title and split header styling three ways across the corpus. Keep
the page title as a single `# H1`. Section `index.md` landing pages are the
exception: they use a plain `>` blockquote summary and no badge.

## Page badges

Visible status/type pills are shared UI too, and they are **opt-in**: a page
renders a pill only when a `.metadata.yml` scope sets `display_badge` to
`draft`, `template`, or `reference`. Most pages set no
badge — the old blanket `approved` badge was retired because labeling the
default state added noise (and the token is now rejected by validation).
`page_header()` renders the page's badge automatically; use the `badge(...)`
macro only for one-off inline badges, and never inline raw HTML pill spans.

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
build-time `.metadata.yml`, which drives review cadence and the status badge.)

## Structured page data

When one public page needs to repeat the same source-of-truth data across
charts and tables, keep that content in a shared YAML file and render it
through a macro. `docs/_data/people.yml` is deliberately limited to public
leadership names, titles, team labels, and team purposes; it drives the public
leadership chart and inline `role_holder(...)` references. It must never carry
staff rosters, contractors, payroll identifiers, phone numbers, email
addresses, classifications, personnel status, or full position descriptions.

## Page data model

Use each data shape intentionally:

- `.metadata.yml` for inherited page metadata, review fields, and optional `display_badge` state.
- `*.cards.yml` for shared landing-page card content rendered through `card_grid_from(...)`.
- `*.data.yml` for page-local structured source data that needs to render into more than one repeated section.

Do not invent new adjacent file conventions casually. If a page needs a new shared data pattern, document it in this manual and `README.md` in the same change.

## Build platform posture

This repo currently runs on MkDocs 1.x and should stay there unless the team
approves a deliberate platform migration.

Keep `mkdocs-redirects` pinned at `1.2.2` unless and until OPI explicitly
decides to migrate to ProperDocs. Newer redirect-plugin releases pull in
ProperDocs transitively and emit migration warnings during normal MkDocs builds.

If the team wants ProperDocs later, treat it as a full platform change:

1. Rename `mkdocs.yml` to `properdocs.yml`.
2. Update local commands, CI, and preview/deploy scripts from `mkdocs` to `properdocs`.
3. Re-verify theme, plugins, redirects, and navigation behavior in one slice.

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
pass with `task validate`, which adds the browser smoke checks. That pass
expects a one-time local browser install via
`uv run playwright install chromium`.

### Which gate runs what

`Taskfile.yml` exposes the tiers; `scripts/verify.py` defines the suite once and
runs it in three nested tiers:

| Tier | Where | Covers |
|---|---|---|
| `task ci` | pull-request CI, fast local loop | hosted-CI policy guard, format, lint, mypy, bandit, metadata, brand terms, style, consistency, raw HTML links |
| `task prepush` | the pre-push hook and the Pages deploy gate | everything above, plus pytest, `mkdocs build --strict`, publication-boundary and built-link checks, and accessibility checks |
| `task validate` | locally, before a deploy | everything above, plus the Playwright browser smoke checks |

Each tier is a strict prefix of the next, so nothing is lost by moving a check
down a tier — it runs later, not never.

Pull-request CI is deliberately lean — **no test suite, no site build, no
browser** — per section 4 of the civic-app consistency standard.
`scripts/check_hosted_ci_policy.py` fails the build if that ever regresses,
including through indirection: it statically resolves both the `Taskfile.yml`
task graph and the `verify.py` plans, so adding a heavy step to any task `ci`
reaches is caught.

The `ci` plan also runs Patapsco's published `platform-check`
(`baltimore-patapsco`, exact-pinned in the dev group), which owns the shared
estate baseline: the app marker, the slot-8 ports, the task surface, tooling
configuration, and the pre-push hook. Keep **both**. `platform-check` 0.4.3 does
not expand `verify.py` plans (it expands `npm` and `.sh` bodies, but not a
Python plan module), has no job-timeout rule, and has no `run:`/`uses:`
allowlist, so it returns "conforms" for four of the five violations the local
guard fails on. The comparison runs both ways: the 0.4.1 sweep caught two
Taskfile forms the local guard missed — a block-list `deps:` and a `silent: true`
task — which are now fixed and regression-tested here, and the 0.4.3 sweep found
a third that is not yet fixed (a new `.sh` in the task chain that runs a
forbidden command directly). The measured gaps, and the condition under which
the local guard can finally be deleted — still unmet at 0.4.3 — are recorded in
the "Two checkers" note in that module's docstring.
If you bump the pin, re-run that comparison before assuming it is now redundant.
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
| SharePoint | Read-access for understanding what stays internal |

## Onboarding a new maintainer

Day 1: read this document and `CONTRIBUTING.md`. Run `task setup` then `task serve` locally. Read every page on the live site.

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
- Public template pages should explain structure without publishing internal
  system locations, contact lists, or controlled working copies.
