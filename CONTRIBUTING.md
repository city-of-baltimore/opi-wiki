# Contributing

**Content contributions:** see the published
[Contributing](docs/resources/contributing.md) page — it is the source of
truth for suggesting edits, reporting errors, and how review works. No
GitHub or Markdown knowledge required there.

**For maintainers:** [`MAINTAINERS.md`](MAINTAINERS.md) is the operating
manual (editorial voice, review tiers, conventions).

## Working in this repo

```bash
poetry install                  # one-time setup
poetry run mkdocs serve         # live preview at http://127.0.0.1:8000
./scripts/verify.sh             # the full check suite (same gate CI runs)
```

Ground rules, enforced by `./scripts/verify.sh` (and by CI on every PR and
deploy — the suite is defined once, in `scripts/verify.py`):

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
