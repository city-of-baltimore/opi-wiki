# AGENTS.md

## Purpose

This repository is the public MkDocs site for **OPI Foundations**.

It is not a loose content dump or a one-off publishing folder. It should remain
the canonical, maintainable source for how OPI publishes durable public-facing
reference material.

Docs are the product here. The repo should make them:

- easy to find
- easy to update
- easy to review
- hard to break quietly

## Read This First

Before making major structural changes, read:

- `README.md`
- `CONTRIBUTING.md`
- `MAINTAINERS.md`
- `docs/resources/reference/wiki-knowledge-base-structure.md`

Treat those files as standing implementation guidance for editorial,
structural, and governance decisions.

## Core Rules

### Docs are architecture

- Site structure, navigation, and editorial workflow are part of the product.
- When architecture changes, update docs in the same slice as config changes.
- Do not leave repo conventions in chat history only.

### Keep ownership local

- `mkdocs.yml` owns global site/runtime configuration only.
- `docs/**/.pages` owns section-local navigation and ordering.
- Do not reintroduce a giant hand-maintained `nav:` block in `mkdocs.yml`.

### Prefer explicit boundaries

Keep the repo legible:

- `docs/` for published content and assets
- `overrides/` for MkDocs Material template overrides
- `scripts/` for repeatable maintenance and verification helpers
- `.github/workflows/` for deploy and CI automation

Avoid mystery top-level scripts or repo behavior that only one maintainer
understands.

### Content taxonomy guardrails

OPI content sorts into four distinct types. Do not blur them when adding or
moving pages.

- **Teams** (staff + budget, also called portfolios): Director's Office,
  Performance, Data and Analytics, Innovation Lab → `our-teams/`.
- **Services** (what OPI delivers): AdminOps, Citywide Performance Management,
  Citywide Data and Analytics, Innovation Lab, Cross-Agency Delivery →
  `how-we-work/services/`.
- **Programs** (ongoing routines spanning teams): CitiStat → `programs/`.
- **Products** (tools OPI builds): Baltimore Intelligence Center and others →
  `products/`.

Hold these lines:

- Innovation Lab is intentionally both a team and a service — state it, don't
  "fix" it.
- CitiStat is a program supported by all teams, owned by the CitiStat Director —
  never a team.
- Cross-Agency Delivery is a service, not a staffed team. There is no
  `our-teams/cross-agency-delivery/`.
- Never write "CAD." Spell out Cross-Agency Delivery; "x-agency delivery" is the
  only allowed short form.
- Every canonical page carries an owner and review cadence via the nearest
  `.metadata.yml`; new sections add their own.

## Navigation Rules

- Every major docs section should own its own `.pages` file.
- When adding, renaming, moving, or deleting pages, update the nearest
  `.pages` file in the same change.
- Keep ordering intentional. The filesystem alone should not decide the public
  information architecture.
- Use section index pages as the landing surface for each major area.

## Content And Linking Rules

- Prefer Markdown-native links to source pages, using `.md` paths in source.
- Raw HTML links are allowed for card-grid layouts, but they must pass
  `scripts/check_html_links.py` through `./scripts/verify.sh`.
- Keep cross-links up to date when page slugs or folders move.
- Prefer plain language and skimmable structure over ornamental formatting.
- Use raw HTML only when Markdown cannot produce the needed layout cleanly.
- Public/private boundaries must remain explicit. Do not accidentally expose
  internal-only content through a navigation or linking mistake.
- Do not delete substantive published content without explicit approval. Safe
  cleanup includes duplicate boilerplate, stale scaffolding, or superseded
  copies that still have one canonical source of truth left in place.

### Memo conversion rule

- Before converting a memo-style source document, ask the clarifying questions
  needed to resolve ambiguous dates, named contacts, publication posture, or
  sensitive details. Do not silently choose among conflicting memo variants when
  those points are unclear.

## Engineering Rules

- Repo automation should prefer Python over complex shell when logic needs
  branching, parsing, validation, or reuse.
- Python code in this repo must include type hints, docstrings, and explicit
  exception handling at IO or CLI boundaries.
- New or changed Python automation must ship with tests in `tests/`.
- Shell scripts should stay thin wrappers around verified commands.
- Prefer official MkDocs and Material features before adding custom template,
  CSS, or JavaScript behavior.
- Validation logic is not done until it is wired into `./scripts/verify.sh`
  or intentionally documented as an optional maintenance tool.

## Runtime And Deployment Rules

- GitHub Pages is the canonical production deployment path
  (`.github/workflows/deploy.yml` on push to `main`).
- Preview changes locally with `uv run mkdocs serve`, or with
  `docker compose up` (the `Dockerfile` / `docker-compose.yml` run the same
  uv-based `mkdocs serve` in a container with live reload). Both are local
  developer conveniences only; the production deploy path stays GitHub Pages.
- Both preview paths serve on <http://127.0.0.1:5208>. That is this repo's slot
  in the Baltimore civic-platform port registry
  (`patapsco/contracts/ports.toml`, slot 8), recorded in
  `.baltimore-lab-app.toml`. Keep the host binding on loopback, never
  `0.0.0.0`, and do not change the port without changing the registry first.
- Do not edit generated `site/` output.

## Civic-platform Baseline

This repo is a **docs site**, not an application, so most of the civic-app
consistency standard does not apply: no compose backend stack, no postgres, no
nginx/TLS, no Django, no Node/bromo frontend. What it does adopt, and must
keep:

- uv for all Python dependency management (never Poetry).
- The registry port pin above.
- `.baltimore-lab-app.toml` as the machine-readable marker.
- The three-tier check split (`ci` / `prepush` / `validate`) described under
  Verification Rules, and the Python floor from the platform bill of
  materials (`>=3.13,<3.15`; 3.14 is the default).
- Snyk as a manual, non-gated scan (`./scripts/security_snyk.sh`).

## Verification Rules

Run this before shipping structural or config changes:

```bash
./scripts/verify.sh
```

That verification path should stay fast, obvious, and trusted.

At minimum, verification should cover:

- formatting and linting for repo automation
- tests for repo automation
- metadata and naming validation
- strict MkDocs build validation
- raw HTML link validation
- lightweight accessibility smoke checks on generated output

### The three tiers

`scripts/verify.py` defines the suite once and exposes three nested plans, the
same three every repo in the family uses:

- `--plan ci` — static checks only: the workflow-policy guard, lint, mypy, and
  the validators that read `docs/` source. **No test suite, no site build,
  nothing that reads `site/`, no browser.**
- `--plan prepush` (the default) — everything in `ci`, plus pytest,
  `mkdocs build --strict`, the built-site link crawl, and the accessibility
  checks.
- `--plan validate` — everything in `prepush`, plus the Playwright browser
  smoke checks, which need `uv run playwright install chromium`.

Each plan is a strict prefix of the next, and `tests/test_verify.py` asserts it,
so moving a check to a lower tier can never quietly drop it.

Hosted pull-request CI runs **`ci`**. The Pages deploy workflow runs
**`prepush`** and gates production. This follows section 4 of the civic-app
consistency standard: the hosted lane is static checks, contracts, and security
only — tests, builds, and browser suites are forbidden there, directly or
through an aggregate runner.

Three rules follow from that:

- **Never add a test, build, or browser step to `.github/workflows/ci.yml`.**
  Add checks to `build_steps()` in `scripts/verify.py` instead, in the right
  tier. `scripts/check_hosted_ci_policy.py` fails the build if you do — it
  resolves which plan the workflow asks for and scans the commands that plan
  expands to, so an allowlisted-looking string cannot smuggle the heavy chain
  in.
- **Every hosted job declares `timeout-minutes`,** and every verification step
  is bounded by `--step-timeout` (600s default). A hung step must fail fast
  with a named step, not sit on GitHub's six-hour default. The policy guard
  fails a job that has no timeout.
- **Install the hooks (`./scripts/install-hooks.sh`) and let the pre-push gate
  run.** With tests out of the hosted lane, that hook is the only backstop; a
  broken test now surfaces at `git push`, not on the pull request.

Snyk is advisory and manual: `./scripts/security_snyk.sh`. Do not wire it into
`verify.py` or any workflow — Snyk plans cap scan counts.

If you change repo structure, navigation, or maintainer workflow, update:

- `README.md`
- `MAINTAINERS.md`
- relevant `docs/**/.pages` files
- any affected reference doc that explains the structure

## Maintainer Posture

- Optimize for long-term maintainability, not one-time authoring speed.
- Fix drift when you find it: stale links, outdated paths, and mismatched docs
  are bugs.
- Prefer small, boring, explicit patterns over cleverness.
- Keep good engineering practices in place even though this is “just docs”.
