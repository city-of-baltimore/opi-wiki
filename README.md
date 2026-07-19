# OPI Foundations

The public docs site for Baltimore City's Mayor's Office of Performance and Innovation.

Live site: https://city-of-baltimore.github.io/opi-wiki/ (custom domain https://opi.baltimorecity.gov pending DNS)
Repo: this repository
Maintainer: see [`MAINTAINERS.md`](MAINTAINERS.md)

## What this is

A docs-as-code site, written in Markdown, rendered with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), version-controlled on GitHub, and auto-deployed via GitHub Actions.

The site is **public-facing**. Internal companion documents (PDs, performance standards, onboarding checklists) live on Baltimore City's SharePoint intranet and are linked from this site with a 🔒 marker.

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

# the pre-deploy pass: everything above plus the Playwright browser smoke checks
task validate

# `task --list` shows the rest (fmt, lint, typecheck, test, security:snyk)
```

`scripts/verify.sh` is still the underlying runner if you need its flags
directly — for example `./scripts/verify.sh --json-output /tmp/opi-verify.json`
to write a machine-readable report.

`task serve` runs at <http://127.0.0.1:5208> with live reload.

That port is not arbitrary: this repo holds slot 8 in the Baltimore
civic-platform port registry (`patapsco/contracts/ports.toml`), so its local
preview never collides with a sibling app's stack. `mkdocs.yml` pins
`dev_addr` to `127.0.0.1:5208` — loopback only, never `0.0.0.0`. See
[`.baltimore-lab-app.toml`](.baltimore-lab-app.toml).

Every tier delegates to `scripts/verify.py`, a structured runner that emits step
timings and can optionally write a JSON report for CI or debugging.

To use the optional browser smoke checks locally, install the Chromium browser
once per machine:

```bash
uv run playwright install chromium
```

### Run with Docker

No local Python or uv install required — preview the site in a container:

```bash
docker compose up
```

This serves the wiki at <http://127.0.0.1:5208> with live reload; edits to
`docs/` on the host refresh the browser. Production still deploys to GitHub
Pages, not this image.

## How CI is split

Three tiers, defined once in `scripts/verify.py` and shared by every gate.
This is section 4 of the civic-app consistency standard, applied here:

| Tier | Command | Where it runs | What it covers |
| --- | --- | --- | --- |
| `ci` | `task ci` | pull-request CI, fast local loop | workflow policy, lint, mypy, bandit, and the validators that read `docs/` source |
| `prepush` | `task prepush` | the pre-push hook and the Pages deploy gate | everything in `ci`, plus pytest, `mkdocs build --strict`, the built-site link crawl, and the accessibility checks |
| `validate` | `task validate` | before a deploy, locally | everything in `prepush`, plus the Playwright browser smoke checks |

Each tier is a strict superset of the one above it, so a check that moves down
a tier is never a check that was dropped.

**Hosted CI runs `task ci` verbatim — no test suite, no site build, no
browser.** That is deliberate, and it has a cost worth stating plainly: a broken
test is caught at `git push`, not on the pull request. `task setup` installs the
pre-push hook that is now the backstop.

`scripts/check_hosted_ci_policy.py` enforces the boundary mechanically. It fails
the build if a hosted workflow reaches a test suite, a site build, an image
build, or a browser suite — including transitively, through *both* indirection
layers: it statically resolves the `Taskfile.yml` task graph and the `verify.py`
plan the workflow asks for, and the two compose. It also fails a job that
forgets `timeout-minutes`, and holds a strict allowlist for every `run:` command
and every pinned `uses:` action. A task it cannot resolve is a violation, not a
pass.

Alongside it, the `ci` plan runs **`platform-check`** from Patapsco's published
`baltimore-patapsco` package (exact-pinned in the dev group). That is the shared
estate baseline — the app marker, the reserved port slot, the task surface,
ruff/mypy/bandit configuration, and the pre-push hook — and it is the authority
on rules that span every sibling repo.

The two are complementary, not redundant, and the split was measured rather than
assumed. `platform-check` 0.4.0 resolves the `Taskfile.yml` graph but treats
`verify.py --plan ci` as an opaque leaf, so it does not see this repo's second
indirection layer; it also has no job-timeout rule and no workflow allowlist.
The four cases it misses are documented in the "Two checkers" note in
`scripts/check_hosted_ci_policy.py`, with the condition for retiring the local
guard.

Do not add a test, build, or browser step to the pull-request workflow, and do
not add one to a task `ci` reaches. Add checks to `build_steps()` in
`scripts/verify.py`, in the right tier, so every gate stays in sync.

## Security scanning

`./scripts/security_snyk.sh` runs an advisory Snyk source-code scan. It is
manual and deliberately wired into no gate — Snyk plans cap scan counts. See
`patapsco/docs/operations/snyk-scanning.md`.

## Build platform note

This repo intentionally stays on `mkdocs==1.6.1` and pins
`mkdocs-redirects==1.2.2`.

`mkdocs-redirects==1.2.3` introduces a transitive `properdocs` dependency and a
build-time warning encouraging migration away from MkDocs. That migration may be
worth evaluating later, but it should happen as an explicit repo decision, not
as a side effect of a plugin upgrade.

If OPI chooses to adopt ProperDocs in the future, do it as a single migration
slice: rename `mkdocs.yml`, update local commands and CI, and re-verify all
plugins and theme behavior together.

## Repository conventions

- Keep global site config in `mkdocs.yml`.
- Keep navigation local to the content in `docs/**/.pages`.
- Keep recurring operational source material grouped in dedicated local collections such as `docs/how-we-work/administrative-memos/` and `docs/how-we-work/how-to/`, and expose those collections intentionally in the nearest section navigation.
- Open each content page with one `{{ page_header(...) }}` call directly under the `# H1`, not a hand-built stack of badge, blockquote, bold kicker, restated bold title, and italic tagline. The macro renders the status badge (from `.metadata.yml`) plus an optional `category`, `summary`, and `tagline`. Keep the title as a single `# H1` — never restate it as a bold paragraph. Section `index.md` landing pages stay on a plain `>` blockquote summary and carry no badge.
- Keep landing-page card content in neighboring `*.cards.yml` files and render it through the shared `card_grid_from(...)` macro.
- Keep repeated structured page data in neighboring `*.data.yml` files when one source needs to drive multiple rendered sections.
- Page badges are opt-in: set `display_badge` (`draft`, `template`, `reference`, `position-description`) in the nearest `.metadata.yml` only when a page needs a pill; `page_header()` renders it. Never inline raw HTML pill spans.
- Keep shared brand CSS split by responsibility under `docs/assets/stylesheets/` so tokens, Material chrome, reusable components, and page-specific presentation do not drift together.
- Run `task prepush` before merging structural or config changes.
- Treat `site/` as generated output, not source.

## Page data model

Use the smallest shared pattern that matches the page need:

- `{{ page_header(...) }}` renders the canonical page intro (optional opt-in badge + optional `category`, `summary`, `tagline`) once, from the page and its `.metadata.yml`. It is the only supported way to render the header chrome.
- `.metadata.yml` carries inherited page metadata such as owner, review cadence, change log, and optional `display_badge` state.
- `*.cards.yml` carries repeated landing-page card content and should render only through `card_grid_from(...)`.
- `*.data.yml` carries structured page-specific source data when one file needs to drive multiple rendered sections, tables, charts, or lists.

If a page can stay plain Markdown, keep it plain Markdown. Only introduce structured data when it removes repeated source-of-truth content or repeated shared UI markup.

## Repository layout

```
opi-foundations/
├── AGENTS.md               # standing repo rules
├── mkdocs.yml              # site-wide MkDocs config
├── pyproject.toml          # project metadata + deps (uv / PEP 621)
├── uv.lock                 # locked Python dependencies
├── docs/                   # all content (Markdown)
│   ├── .pages              # top-level nav ownership
│   ├── index.md            # home
│   ├── index.cards.yml     # shared card-grid data for home
│   ├── about-us/           # mission, letters, our-teams/
│   ├── how-we-work/        # organization/ (org chart, team & roles), handbook/
│   ├── what-we-do/         # services, programs (CitiStat), products (BIC)
│   ├── resources/          # reference, glossary, position descriptions
│   ├── */index.cards.yml   # section-local landing-page card data
│   └── assets/
│       ├── stylesheets/tokens.css          # shared design tokens + Material bridges
│       ├── stylesheets/base.css            # typography and content primitives
│       ├── stylesheets/material-chrome.css # header, nav, tabs, footer
│       ├── stylesheets/components.css      # cards, pills, reusable shared UI
│       ├── stylesheets/home.css            # homepage-only presentation
│       ├── images/               # logos, page images
│       └── docs/                 # downloadable .docx/.pdf assets
├── overrides/              # MkDocs Material theme overrides (empty for now)
├── Taskfile.yml            # the shared task surface (ci/prepush/validate + helpers)
├── scripts/
│   ├── verify.sh           # underlying runner entrypoint (Taskfile calls it)
│   ├── verify.py           # the three-tier check plan (ci/prepush/validate)
│   ├── check_hosted_ci_policy.py # keeps hosted CI static-only (repo-local guard)
│   ├── install-hooks.sh    # installs the pre-push gate
│   ├── hooks/pre-push      # runs the prepush plan before every push
│   ├── check_html_links.py # raw HTML href validation
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
2. **Substantive content edit:** maintainer opens a pull request. Owner of that section (Performance, Innovation Lab, Data, Director's Office) approves. Then merge.
3. **New section / structural change:** ED/CDO approves before merge.

See [`MAINTAINERS.md`](MAINTAINERS.md) for the full operating manual.

## Deployment

`main` branch deploys automatically to GitHub Pages via the workflow in `.github/workflows/deploy.yml`. To deploy to a custom domain (`opi.baltimorecity.gov`), the city DNS team needs to add a `CNAME` record pointing to GitHub Pages, and a `CNAME` file should be added to `docs/`.


## License

Content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — peer cities welcome to adapt with attribution.
Code (theme, build): MIT.

## Documentation method consistency

This wiki treats method pages and playbooks as sources of truth. When adding or editing documentation, prefer linking to the canonical method page instead of redefining a term in a slightly different way. Update the glossary when a term is introduced, retired, or narrowed.
