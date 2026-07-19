# AGENTS.md

Derived from [`patapsco/docs/agents-master.md`](https://github.com/city-of-baltimore/patapsco/blob/main/docs/agents-master.md).
This file **adapts** the baseline; it never re-litigates it. Anything a machine
can check lives in `platform-check`, not in prose here.

This repository is the public MkDocs site for **OPI Foundations**. Docs are the
product: they must be easy to find, easy to update, easy to review, and hard to
break quietly.

Before any structural change, read `README.md`, `CONTRIBUTING.md`,
`MAINTAINERS.md`, and
`docs/resources/reference/wiki-knowledge-base-structure.md`. Those are standing
guidance for editorial, structural, and governance decisions.

---

## 1 · What is enforced, and where

`platform-check` (shipped in `baltimore-patapsco`) is the authority on the
lean-CI rule, the task surface, naming, ports, and pins. It runs against this
repo; read
[`docs/app-consistency-standard.md`](https://github.com/city-of-baltimore/patapsco/blob/main/docs/app-consistency-standard.md)
for the contract and
[`contracts/`](https://github.com/city-of-baltimore/patapsco/tree/main/contracts)
for the machine-readable truth.

If you believe a rule is wrong, **change the rule in Patapsco**. A local
exception needs a dated, owned waiver in `.baltimore-lab-app.toml`; an expired
waiver fails the build by design.

**What does not apply here.** This repo is `kind = "docs-site"` (registry slot
8), not an application. The baseline sections on compose shape, service names,
postgres/redis, the nginx TLS edge and certs, Django/backend runtime, and
Node/npm/bromo are all **out of scope** — there is no backend, no container in
the deploy path, and no frontend package. `platform-check` already gates those
rules on `kind`; do not adopt them here to "be consistent."

What this repo *does* take from the baseline, and must keep: uv for all Python
dependency management, the Python floor from the platform BOM, the slot-8
loopback port, `.baltimore-lab-app.toml`, `Taskfile.yml` and the shared task
names, the three-tier gate, and Snyk as a manual non-gated scan
(`./scripts/security_snyk.sh` — never wire it into a gate; plans cap scan
counts).

## 2 · The three gates

| Tier       | Command         | Where                         |
| ---------- | --------------- | ----------------------------- |
| `ci`       | `task ci`       | GitHub Actions, on every PR   |
| `prepush`  | `task prepush`  | local pre-push hook; also the Pages deploy gate |
| `validate` | `task validate` | before a deploy; adds the browser suite (`uv run playwright install chromium` first) |

`scripts/verify.py` defines the suite once, in three nested plans, so the lanes
cannot drift. Add a check to `build_steps()` in the right tier — never as an
ad-hoc workflow step.

**Never add a test, build, or browser step to the hosted lane**, directly or by
adding one to a task `ci` reaches. Two checks in the `ci` plan enforce this:

- `scripts/check_hosted_ci_policy.py` (repo-local) walks **both** indirection
  layers — the `Taskfile.yml` graph and the `verify.py` plans — and additionally
  holds the `run:`/`uses:` allowlists and the job-timeout rule.
- `platform-check` (from the pinned `baltimore-patapsco` dev dependency) resolves
  the task graph independently and owns the shared estate baseline.

Resolution is static on purpose in both: `task --dry` writes its plan to stderr,
so a guard that shells out and reads stdout passes vacuously.

**Do not delete the local guard as "duplicated by `platform-check`".** That has
been attempted and measured twice, against 0.4.0 and again against 0.4.1. 0.4.1
expands `npm` script and `.sh` bodies, but a **Python plan module** is still an
opaque leaf, so a `pytest` step added to the `ci` tier of `build_steps()` passes
it while the hosted lane really runs the suite — the same green-but-vacuous
failure mode as the `task --dry` bug. Routing `ci` through `scripts/verify.sh`
is missed for the same reason: the `.sh` body is read, then lands on the same
Python wall. It also misses a missing `timeout-minutes`, an unallowlisted `run:`
command, and an unpinned `uses:` ref. The retirement condition is in the "Two
checkers" note in that module's docstring — and the injection matrix that
produced these numbers is reproducible; re-run it on every pin bump.

Because tests live pre-push, **the hook is the only backstop**. Run
`./scripts/install-hooks.sh` after cloning. A broken test surfaces at
`git push`, not on the pull request.

## 3 · The excellence bar

Aim for work a senior reviewer would call excellent without qualification.

**Correctness**

- Every public function in `scripts/` and `main.py` has a happy-path _and_ a
  failure-path test in `tests/`.
- You fixed the cause, not the symptom. If you silenced a check — a `noqa`, a
  `nosec`, a per-file-ignore — the line above it says why, specifically.
- You never weakened, skipped, or deleted a test to make a gate pass. Moving a
  suite between tiers is fine; reducing coverage is not.

**Design**

- One responsibility per module. Soft-flag at 400 lines, split-review at 500.
- The local layering is: `scripts/check_*.py` are thin argv-driven CLIs;
  the logic they check lives in `scripts/repo_tools/`; `scripts/verify.py` only
  sequences subprocesses and reports. Keep validation logic out of the CLIs and
  out of the runner.
- Python over shell whenever logic branches, parses, validates, or is reused.
  Shell scripts stay thin wrappers around verified commands.
- Prefer official MkDocs and Material features before adding custom template,
  CSS, or JavaScript.

**Interface**

- Python automation carries type hints, docstrings, and explicit exception
  handling at every IO or CLI boundary. mypy runs strict.
- A check that is not wired into a `verify.py` plan does not exist. Either wire
  it into the right tier or document it as an optional maintenance tool.

**Evidence**

- The PR body states the root cause, the seam you fixed, the regression proof,
  and the exact commands you ran. "Tests pass" is not evidence; naming the
  command and its result is.
- Docs move in the _same_ commit as the behavior they describe.

**Judgment (the part no checker can hold)**

- Prefer deleting to adding. The best change is often a smaller one.
- When two designs are close, pick the one a newcomer would understand faster.
- Fix drift when you find it: stale links, outdated paths, and mismatched docs
  are bugs.
- Keep good engineering practice in place even though this is "just docs."

## 4 · Foundations and boundaries

Camden owns data mechanics. Patapsco owns runtime, wire behavior, and this
baseline. Bromo owns presentation. This repo owns its content and its own
publishing automation, and imports no foundation package.

## 5 · Changing the baseline

Change `contracts/` and/or the rule in `platform-check` in Patapsco, run
`platform-check --estate` to see the blast radius, land it there, then open the
follow-up PR here. A baseline change that lands in only one repo has already
drifted.

---

# App-specific

Everything below is local to this repository. It is not in the baseline and no
checker holds it — it is hard-won domain knowledge about OPI's content.

## Content taxonomy

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

## Structure and navigation

- `mkdocs.yml` owns global site/runtime configuration only. `docs/**/.pages`
  owns section-local navigation and ordering. Do not reintroduce a giant
  hand-maintained `nav:` block.
- Every major docs section owns its own `.pages` file. When adding, renaming,
  moving, or deleting pages, update the nearest `.pages` file in the same
  change.
- Keep ordering intentional; the filesystem alone should not decide the public
  information architecture. Use section index pages as each area's landing
  surface.
- Directory boundaries: `docs/` published content and assets, `overrides/`
  Material template overrides, `scripts/` maintenance and verification helpers,
  `.github/workflows/` deploy and CI automation. No mystery top-level scripts.

## Content and linking

- Prefer Markdown-native links to source pages, using `.md` paths in source.
- Raw HTML links are allowed for card-grid layouts but must pass
  `scripts/check_html_links.py`. Use raw HTML only when Markdown cannot produce
  the layout cleanly.
- Keep cross-links current when slugs or folders move.
- Prefer plain language and skimmable structure over ornamental formatting.
- **Public/private boundaries must stay explicit.** Do not expose internal-only
  content through a navigation or linking mistake.
- **Do not delete substantive published content without explicit approval.**
  Safe cleanup is duplicate boilerplate, stale scaffolding, or superseded copies
  where one canonical source of truth remains.

### Memo conversion

Before converting a memo-style source document, ask the clarifying questions
needed to resolve ambiguous dates, named contacts, publication posture, or
sensitive details. Do not silently choose among conflicting memo variants.

## Runtime and deploy

- GitHub Pages is the canonical production path
  (`.github/workflows/deploy.yml`, on push to `main`). There is no container in
  the deploy path.
- Preview locally with `task serve`, or `docker compose up` — both run the same
  uv-based `mkdocs serve` with live reload, both are developer conveniences
  only.
- Both serve on <http://127.0.0.1:5208>: this repo's slot-8 pin in
  `patapsco/contracts/ports.toml`, recorded in `.baltimore-lab-app.toml`. Keep
  the binding on loopback, never `0.0.0.0`, and change the registry before
  changing the port.
- Do not edit generated `site/` output.

## Docs that move with structure

If you change repo structure, navigation, or maintainer workflow, update
`README.md`, `MAINTAINERS.md`, the relevant `docs/**/.pages`, and any reference
doc that explains the structure — in the same change.
