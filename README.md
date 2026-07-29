# OPI Foundations

The documentation site for Baltimore City's Mayor's Office of Performance and Innovation.

Live site: <https://city-of-baltimore.github.io/opi-wiki/>
Repo: this repository
Maintainer: see [`MAINTAINERS.md`](MAINTAINERS.md)

New to the product or repository? Start with
[`onboarding.md`](onboarding.md).

## What this is

A docs-as-code site, written in Markdown, rendered with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), version-controlled on GitHub, and auto-deployed via GitHub Actions.

This repository contains the source for the OPI Foundations website. Its staff
directory is deliberately limited to City staff names, working titles, team
assignments, reporting relationships, and short role summaries. Full position
descriptions, detailed performance records, contact records, payroll data, and
personnel-status fields belong in Baltimore City's SharePoint and other systems
of record. The existing Handbook sources are a bounded holding area while OPI
decides their long-term City-system destination; MkDocs excludes them from the
generated site.

One strict organization loader accepts only the documented fields and feeds the
org chart, Team and Roles tables, and inline role lookups from the same immutable
record. Hosted CI rejects unknown fields, missing or mistyped values, duplicate
YAML keys, and drift from the canonical four-team structure. The built-artifact
check separately rejects structured YAML, Handbook paths, phone-number patterns,
and PIN labels in generated output. Section-owner review remains responsible for
contextual placement that automation cannot infer.

## Local development

Requires Python 3.13 or 3.14 (3.14 is the default across the Baltimore civic
platform) and [uv](https://docs.astral.sh/uv/). Editing the wiki does not
require running anything locally — content contributions can go through the
GitHub web editor and the checks run in CI.

`Taskfile.yml` is the command surface, the same task names every repo in the
family exposes. It needs [Task](https://taskfile.dev) and `uv`.

```bash
# one-time: install dependencies and the pre-push hook
task setup

# preview the site locally, with live reload
task serve

# build a static site
task build

# the pre-push pass: static checks + tests + strict build + built-site checks
task prepush

# the hosted-CI subset — static checks only. No tests, no site build.
# Fast inner loop, and exactly what pull-request CI runs.
task ci

# the pre-deploy pass: browser interaction + full-route accessibility assurance
task validate

# `task --list` shows the rest (fmt, lint, typecheck, test, security:snyk)
```

`scripts/verify.py` is the runner the Taskfile calls. The thin
`scripts/verify.sh` compatibility wrapper exposes the same flags if needed—for
example `./scripts/verify.sh --json-output /tmp/opi-verify.json` writes a
machine-readable report.

`task serve` runs at <http://127.0.0.1:5208> with live reload.

That port is not arbitrary: this repo holds slot 8 in the Baltimore
civic-platform port registry (`patapsco/contracts/ports.toml`), so its local
preview never collides with a sibling app's stack. `mkdocs.yml` pins
`dev_addr` to `127.0.0.1:5208` — loopback only, never `0.0.0.0`. See
[`.baltimore-lab-app.toml`](.baltimore-lab-app.toml).

Every tier delegates to `scripts/verify.py`, a structured runner that emits step
timings and can optionally write a JSON report for CI or debugging.

To use the optional browser checks locally, install Chromium once per machine:

```bash
uv run playwright install chromium
```

`task validate` is the canonical, self-contained pre-deploy proof. It builds the
site strictly, reads the production canonical origin from that build's
`sitemap.xml`, and mounts the exact generated files at that origin inside
Chromium through hermetic Playwright request routing. It starts no local server,
makes no DNS, TLS, or network request, and does not rewrite the generated HTML.
Requests outside the exact canonical origin and deployment base, unsafe paths,
and files absent from the artifact fail locally. Both browser suites exercise
the production-shaped artifact; the smoke suite additionally proves same-origin
Material instant navigation. `task serve` does not need to be running first.

The static proof also treats the Adobe and Google font services as unavailable,
so product workflows cannot depend on a vendor or internet connection. Only
the exact HTTPS font-provider origins and font-related resource types are
nonblocking; every other external dependency fails. This does not prove which
typeface Chromium painted or whether a vendor is available. Check those
typography details manually in a live browser when they matter.

To diagnose the live-reload preview itself, use two terminals:

```bash
# Terminal A
task serve

# Terminal B, after the initial build completes
uv run python scripts/check_browser_smoke.py \
  --base-url http://127.0.0.1:5208/opi-wiki/
uv run python scripts/check_browser_accessibility.py \
  --base-url http://127.0.0.1:5208/opi-wiki/
```

The live checks take their canonical route manifest from the selected
preview's own `sitemap.xml`, so they cannot silently use stale disk output.
Unlike the self-contained static audit, they make real requests to the running
`task serve` or Docker Compose preview named by `--base-url`.
Do not edit source files until both live checks finish; each run audits the
fixed route list represented by the manifest it loaded at startup, while page
content remains live.
MkDocs keeps a live-reload request open by design; browser readiness therefore
means the canonical URL, rendered page content, and settled font loading—not
that every network request has stopped. The smoke workflows additionally
require a target-specific marker after Material instant navigation.
The audit browser aborts only its own numeric, same-origin live-reload poll so a
full crawl cannot accumulate 60-second server requests. This does not change
live reload for a normal preview browser.

### Run with Docker

No local Python or uv install required — preview the site in a container:

```bash
docker compose up
```

This serves the wiki at <http://127.0.0.1:5208> with live reload; edits to
`docs/` on the host refresh the browser. Production still deploys to GitHub
Pages, not this image.

Compose keeps the container-only bind address separate from the URL a reader
opens. `OPI_SITE_URL` and the registered MkDocs hook preserve
`http://127.0.0.1:5208/opi-wiki/` as the preview's canonical origin, so the
container exercises the same Material instant-navigation behavior as
`task serve`.

The same live browser commands above can audit the Compose preview at
`http://127.0.0.1:5208/opi-wiki/` from a host that has the development
dependencies and Chromium installed. Stop `task serve` first because the two
preview providers intentionally share the registered port.

## How CI is split

Three tiers, defined once in `scripts/verify.py` and shared by every gate.
This is section 4 of the civic-app consistency standard, applied here:

| Tier | Command | Where it runs | What it covers |
| --- | --- | --- | --- |
| `ci` | `task ci` | pull-request CI, fast local loop | workflow policy, formatting, lint, mypy, bandit, and validators over authored repository sources |
| `prepush` | `task prepush` | the pre-push hook and the Pages deploy gate | everything in `ci`, plus pytest, `mkdocs build --strict`, rendered-language assurance, built-artifact safety and link checks, and accessibility checks |
| `validate` | `task validate` | before a deploy, locally | everything in `prepush`, plus browser interaction and full-route WCAG assurance |

`task ci` enforces the source-language and retired-component ratchet across
Git-tracked and non-ignored untracked authored Markdown, YAML, `.pages`, HTML,
CSS, `CODEOWNERS`, and `.gitignore` sources. Repository-root generated and
dependency directories, plus Git-ignored working paths, stay outside that source
set; a same-named directory under `docs/` remains covered. Any non-excluded
symbolic link fails validation instead of being followed, so the reviewed
repository file remains the source of truth. Discovery requires a Git worktree
and fails closed when Git metadata is unavailable, rather than substituting
different ignore semantics. The matcher treats ordinary prose wrapping,
non-breaking spaces, and Unicode dash punctuation alike while preserving source
record boundaries. Decoded YAML scalar values retain exact source
line-and-column evidence, and malformed YAML fails closed rather than weakening
the check. This hosted check deliberately does not emulate the Markdown
renderer.

After the existing strict build, `task prepush` checks the HTML for every
canonical route. The generated artifact from the configured MkDocs, macros,
Python-Markdown, PyMdown, and Material stack is the authority on rendered
meaning: inline elements compose as readers encounter them, block boundaries
stay separate, and macro-generated text cannot bypass the rule. Findings name
the route, its unique Markdown page source, and the exact generated-HTML
line, column, and element context. Missing, malformed, or ambiguously mapped
artifacts fail closed. This check reuses the one build already owned by
`prepush`; it adds no build, browser, network call, or dependency to hosted CI.

Both layers use the same narrow policy. Generic repository-state phrasing and
removed UI hooks are rejected; civic/service terminology and formal
data-classification and access language remain allowed.

Each tier is a strict superset of the one above it, so a check that moves down
a tier is never a check that was dropped.

The validate tier runs axe against every canonical route at desktop and 320px
reflow widths in both color schemes. It also checks the open mobile navigation
and search states, skip-link behavior, focus treatments, and instant
navigation. The reader-facing promise and the manual checks automation cannot
replace are documented in
[`docs/resources/accessibility.md`](docs/resources/accessibility.md).

**Hosted CI runs `task ci` verbatim — no test suite, no site build, no
browser.** That is deliberate, and it has a cost worth stating plainly: a broken
test is caught at `git push`, not on the pull request. `task setup` installs the
pre-push hook that is now the backstop.

`scripts/check_hosted_ci_policy.py` enforces the boundary mechanically. It fails
the build if a hosted workflow reaches a test suite, a site build, an image
build, or a browser suite — including transitively, through *both* indirection
layers: it statically resolves the `Taskfile.yml` task graph and the `verify.py`
plan the workflow asks for, and the two compose. It also fails a job that
forgets `timeout-minutes`. The pull-request workflow is itself an exact contract:
the action identities, job and step order, properties, and command cardinality
must match, every action revision must be a full commit SHA, and execution
modifiers such as `if`, `continue-on-error`, `shell`, or `working-directory`
cannot silently skip or reinterpret the gate. A task it cannot resolve is a
violation, not a pass.

The Taskfile top level, the `ci` task, and its resolved plan are exact ordered
contracts in
`scripts/repo_tools/hosted_ci_contract.py`; subtraction, addition, duplication,
reordering, global `env`/`dotenv`/`includes`/`vars`, and conditional command
modifiers all fail closed. When a new hosted static check or workflow action is
intentional, update the behavior and that independent contract in the same
change. Do not derive one from the other, because doing so would auto-approve
the drift the contract exists to catch.

Alongside it, the `ci` plan runs **`platform-check`** from Patapsco's published
`baltimore-patapsco` package (exact-pinned in the dev group). For this docs
site, it checks the shared app marker, task surface, tooling configuration, and
pre-push hook, and it remains the authority on rules that span sibling repos.

One boundary is explicit: Patapsco 0.4.5 classifies `docs-site` outside its
port-owning application kinds, so its slot and compose/loopback rules do not run
here. The fast repository browser-readiness contract fills that measured gap:
it pins the slot-8 MkDocs default and task command, the exact loopback Compose
service, the container bind, and Docker's startup and health behavior. Extending
the estate-wide rule still belongs in Patapsco, followed by a re-measured pin
bump here; until then, both checks are required.

The two are complementary, not redundant, and the split is measured rather than
assumed — re-measured against `platform-check` 0.4.5, which expands `npm` and
`.sh` bodies but still treats a **Python plan module** as an opaque leaf. It
therefore does not see this repo's second indirection layer
(`verify.py --plan ci`), including when that layer is reached through
`scripts/verify.sh`; it also has no job-timeout rule, and its `run:` coverage is
a denylist rather than an allowlist. 0.4.5 still misses all five injected cases
in their ordinary form; a piped `curl … | sh` is caught only when the URL
happens to end in `.sh`, via the unresolvable-delegation rule rather than any
`curl` denylist entry. Those five, and the forms this repo's own guard misses in the
other direction, are documented in the "Two checkers" note in
`scripts/check_hosted_ci_policy.py`, with the condition for retiring the local
guard — which 0.4.5 does not meet.

`scripts/check_platform_guard_evidence.py` runs immediately before the shared
gate. It keeps Patapsco exact-pinned, isolates its Dependabot pull requests from
routine tooling updates, and requires every current-measurement claim to name
the release actually tested. A pin bump fails CI until a maintainer updates the
measurement marker and living claims; that update is an explicit attestation,
not proof of execution. The pre-push suite runs the five-case differential
matrix against the installed release and must pass before push or deploy.

Do not add a test, build, or browser step to the pull-request workflow, and do
not add one to a task `ci` reaches. Add checks to `build_steps()` in
`scripts/verify.py`, in the right tier, so every gate stays in sync.

## Security scanning

`./scripts/security_snyk.sh` runs an advisory Snyk source-code scan. It is
manual and deliberately wired into no gate — Snyk plans cap scan counts. See
`patapsco/docs/operations/snyk-scanning.md`.

## Build platform note

The exact rendering stack is `mkdocs==1.6.1`, `mkdocs-material==9.7.7`,
`pymdown-extensions==11.0.1`, and `mkdocs-redirects==1.2.2`.

Material 9.7.2 and later print an MkDocs 2.0 incompatibility warning during a
build. This repository intentionally leaves that planning signal visible. It is
not a ProperDocs warning, and it does not require changing renderers in the
security-patch slice that adopted this stack.

Separately, `mkdocs-redirects==1.2.3` adds `properdocs>=1.6.5` alongside MkDocs.
That upgrade remains deferred to a separate renderer-migration decision
recorded by OPI Wiki maintainers, not a routine dependency batch. Such a
migration must update local commands and CI and re-verify every plugin and theme
behavior together.

## Repository conventions

- Keep global site config in `mkdocs.yml`.
- Keep navigation local to the content in `docs/**/.pages`.
- Treat `docs/how-we-work/handbook/` as a bounded holding area pending an
  owner decision on its long-term City-system destination. Do not add new staff
  working material there. Keep personnel records and contact data in their
  owning City systems.
- Open each content page with one `{{ page_header(...) }}` call directly under the `# H1`, not a hand-built stack of blockquote, bold kicker, restated bold title, and italic tagline. The macro renders an optional `category`, `summary`, and `tagline`. Keep the title as a single `# H1` — never restate it as a bold paragraph. Section `index.md` landing pages stay on a plain `>` blockquote summary.
- Keep landing-page card content in neighboring `*.cards.yml` files and render it through the shared `card_grid_from(...)` macro.
- Keep repeated structured page data in neighboring `*.data.yml` files when one source needs to drive multiple rendered sections.
- Keep shared brand CSS split by responsibility under `docs/assets/stylesheets/` so tokens, Material chrome, reusable components, and page-specific presentation do not drift together.
- Run `task prepush` before merging structural or config changes.
- Treat `site/` as generated output, not source.

## Page data model

Use the smallest shared pattern that matches the page need:

- `{{ page_header(...) }}` renders the canonical page intro (optional `category`, `summary`, and `tagline`) once from explicit page arguments. It is the only supported way to render the header chrome.
- `.metadata.yml` carries inherited page metadata: owner, review cadence, and change log.
- `*.cards.yml` carries repeated landing-page card content and should render only through `card_grid_from(...)`.
- `*.data.yml` carries structured page-specific source data when one file needs to drive multiple rendered sections, tables, charts, or lists.

MkDocs excludes `_data/`, the Handbook source folder, `*.cards.yml`, and
`*.data.yml` from the generated site. These files are build inputs, not
downloadable pages; the pre-push built-artifact safety check enforces that
separation and rejects visible PIN or phone-number fields in the built artifact.

If a page can stay plain Markdown, keep it plain Markdown. Only introduce structured data when it removes repeated source-of-truth content or repeated shared UI markup.

## Repository layout

```
opi-foundations/
├── AGENTS.md               # standing repo rules
├── onboarding.md           # plain-language product and repository overview
├── mkdocs.yml              # site-wide MkDocs config
├── pyproject.toml          # project metadata + deps (uv / PEP 621)
├── uv.lock                 # locked Python dependencies
├── docs/                   # all content (Markdown)
│   ├── .pages              # top-level nav ownership
│   ├── index.md            # home
│   ├── index.cards.yml     # shared card-grid data for home
│   ├── about-us/           # mission, letters, our-teams/
│   ├── how-we-work/        # operating model and leadership org chart
│   ├── what-we-do/         # services, programs, and products
│   ├── resources/          # reference, glossary, role summaries
│   ├── */index.cards.yml   # section-local landing-page card data
│   └── assets/
│       ├── stylesheets/tokens.css          # shared design tokens + Material bridges
│       ├── stylesheets/base.css            # typography and content primitives
│       ├── stylesheets/material-chrome.css # header, nav, tabs, footer
│       ├── stylesheets/components.css      # cards, page headers, reusable shared UI
│       ├── stylesheets/org-chart.css       # responsive leadership chart
│       ├── stylesheets/breadcrumbs.css     # breadcrumb presentation
│       ├── stylesheets/home.css            # homepage-only presentation
│       └── images/               # logos and page images
├── overrides/              # breadcrumbs + table keyboard-accessibility hook
├── Taskfile.yml            # the shared task surface (ci/prepush/validate + helpers)
├── scripts/
│   ├── verify.py           # runner + three-tier check plan (ci/prepush/validate)
│   ├── verify.sh           # thin compatibility wrapper for the Python runner
│   ├── check_hosted_ci_policy.py # keeps hosted CI static-only (repo-local guard)
│   ├── check_platform_guard_evidence.py # holds Patapsco pin-bump evidence
│   ├── install-hooks.sh    # installs the pre-push gate
│   ├── hooks/pre-push      # runs the prepush plan before every push
│   ├── check_html_links.py # raw HTML href validation
│   ├── check_built_visibility.py # rendered-language assurance over canonical pages
│   ├── check_built_artifact.py # rejects excluded source/sensitive data in site/
│   ├── check_organization_data.py # exact organization source contract
│   ├── check_page_metadata.py
│   ├── check_brand_terms.py
├── .github/
│   ├── workflows/ci.yml          # PR/push verification
│   ├── workflows/deploy.yml      # GitHub Actions auto-deploy
│   └── ISSUE_TEMPLATE/           # suggestion + error report forms
├── CONTRIBUTING.md
├── MAINTAINERS.md
└── README.md
```

## Editorial workflow

Three-tier review:

1. **Typo / small correction:** maintainer commits directly to `main`. Auto-deploys in ~2 minutes.
2. **Substantive content edit:** maintainer opens a pull request. The section owner reviews it before merge.
3. **New section / structural change:** ED/CDO sign-off is recorded before merge.

See [`MAINTAINERS.md`](MAINTAINERS.md) for the full operating manual.

## Deployment

`main` deploys automatically to the canonical GitHub Pages URL through
`.github/workflows/deploy.yml`. No custom-domain `CNAME` is committed.


## License

Content: [CC BY 4.0](LICENSE-CONTENT.md) — peer cities may adapt it with
attribution. City names, logos, seals, and official marks are excluded.

Code, theme customizations, and build automation: [MIT](LICENSE).

## Documentation method consistency

This wiki treats method pages and playbooks as sources of truth. When adding or editing documentation, prefer linking to the canonical method page instead of redefining a term in a slightly different way. Update the glossary when a term is introduced, retired, or narrowed.
