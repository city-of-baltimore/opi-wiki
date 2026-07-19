# Contributing

**Content contributions:** see the published
[Contributing](docs/resources/contributing.md) page — it is the source of
truth for suggesting edits, reporting errors, and how review works. No
GitHub or Markdown knowledge required there.

**For maintainers:** [`MAINTAINERS.md`](MAINTAINERS.md) is the operating
manual (editorial voice, review tiers, conventions).

**Editorial style:** [`STYLE.md`](STYLE.md) is the writing standard — voice,
the jargon we replace, and how we handle bullets, tables, and em-dashes.

## Working in this repo

```bash
uv sync                          # one-time setup
./scripts/install-hooks.sh       # one-time: installs the pre-push gate
uv run mkdocs serve              # live preview at http://127.0.0.1:5208
./scripts/verify.sh              # tests + strict build + built-site checks
./scripts/verify.sh --plan ci    # static checks only (what PR CI runs)
```

Ground rules, enforced by `./scripts/verify.sh` (and by CI — the suite is
defined once, in `scripts/verify.py`). Pull-request CI runs the static `ci`
tier only. The test suite, the strict build, and the checks that read built
HTML run in the pre-push hook and the deploy gate — so install the hooks, and
run `./scripts/verify.sh` before you push:

- Strict MkDocs build: broken links and nav entries fail the build.
- Page metadata sidecars (`.metadata.yml`) must be complete and fresh —
  pages unreviewed for 6+ months fail validation.
- Python automation is linted (ruff), typed (mypy --strict), and tested
  (pytest). New or changed automation ships with tests.
- Repo conventions live in [`AGENTS.md`](AGENTS.md) and the README; follow
  the page data model (`page_header()`, `.cards.yml`, `.data.yml`) instead
  of hand-rolled markup.

Review tiers: typo-level fixes may go straight to `main` by maintainers;
substantive edits go through a PR reviewed by the section owner
(see `.github/CODEOWNERS`); structural changes need ED/CDO approval.
