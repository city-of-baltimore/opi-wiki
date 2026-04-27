# OPI Foundations

The public docs site for Baltimore City's Mayor's Office of Performance and Innovation.

Live site: https://opi.baltimorecity.gov *(once deployed)*
Repo: this repository
Maintainer: see [`MAINTAINERS.md`](MAINTAINERS.md)

## What this is

A docs-as-code site, written in Markdown, rendered with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), version-controlled in GitHub Enterprise, and auto-deployed via GitHub Actions.

The site is **public-facing**. Internal companion documents (PDs, performance standards, onboarding checklists) live on Baltimore City's SharePoint intranet and are linked from this site with a 🔒 marker.

## Local development

Requires Python 3.11+ and Poetry 2.x.

```bash
# one-time setup
poetry install

# preview the site locally
poetry run mkdocs serve

# build a static site
poetry run mkdocs build

# run the maintainer verification pass
./scripts/verify.sh
```

`poetry run mkdocs serve` runs at <http://127.0.0.1:8000> with live reload.

## Build platform note

This repo intentionally stays on `mkdocs==1.6.1` and pins
`mkdocs-redirects==1.2.2`.

`mkdocs-redirects==1.2.3` introduces a transitive `properdocs` dependency and a
build-time warning encouraging migration away from MkDocs. That migration may be
worth evaluating later, but it should happen as an explicit repo decision, not
as a side effect of a plugin upgrade.

If OPI chooses to adopt ProperDocs in the future, do it as a single migration
slice: rename `mkdocs.yml`, update local commands, CI, Docker/Fly preview
commands, and re-verify all plugins and theme behavior together.

## Repository conventions

- Keep global site config in `mkdocs.yml`.
- Keep navigation local to the content in `docs/**/.pages`.
- Keep recurring operations material grouped in local subsections such as `docs/how-we-work/operations/administrative-memos/` and `docs/how-we-work/operations/how-to/` when the source documents represent a durable content class.
- Keep landing-page card content in neighboring `*.cards.yml` files and render it through the shared `card_grid_from(...)` macro.
- Keep repeated structured page data in neighboring `*.data.yml` files when one source needs to drive multiple rendered sections.
- Keep visible page badges in `.metadata.yml` via the `display_badge` field and render them through `page_badge()` or `badge(...)`, not raw HTML spans.
- Run `./scripts/verify.sh` before merging structural or config changes.
- Treat `site/` as generated output, not source.

## Repository layout

```
opi-foundations/
├── AGENTS.md               # standing repo rules
├── mkdocs.yml              # site-wide MkDocs config
├── pyproject.toml          # Poetry project metadata + deps
├── poetry.lock             # locked Python dependencies
├── docs/                   # all content (Markdown)
│   ├── .pages              # top-level nav ownership
│   ├── index.md            # home
│   ├── index.cards.yml     # shared card-grid data for home
│   ├── about-us/
│   ├── how-we-work/
│   ├── our-teams/
│   ├── resources/
│   ├── public/
│   ├── contributing.md
│   ├── */index.cards.yml   # section-local landing-page card data
│   └── assets/
│       ├── stylesheets/opi.css   # OPI brand styles
│       ├── images/               # logos, page images
│       └── docs/                 # downloadable .docx/.pdf assets
├── overrides/              # MkDocs Material theme overrides (empty for now)
├── scripts/
│   ├── verify.sh           # local verification entrypoint
│   ├── check_html_links.py # raw HTML href validation
│   ├── check_page_metadata.py
│   ├── check_brand_terms.py
│   └── cleanup_doc_headers.py
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

## Fly.io Test Deploy

For a disposable preview on Fly.io, this repo includes a `Dockerfile` and `fly.toml` that run:

```bash
poetry run mkdocs serve --dev-addr=0.0.0.0:8080 --no-livereload
```

This is a test setup only. `mkdocs serve` is MkDocs' development server, so keep GitHub Pages as the production path.

```bash
# 1) authenticate if needed
fly auth login

# 2) create the Fly app from this repo config
# pick a unique name; this also avoids extra spare machines for a test app
fly launch --copy-config --no-deploy --ha=false --name your-unique-app-name

# 3) deploy a single test machine
fly deploy --ha=false

# 4) open the preview
fly open
```

Useful follow-ups:

```bash
fly status
fly logs
fly scale count 0
```

## License

Content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — peer cities welcome to adapt with attribution.
Code (theme, build): MIT.
