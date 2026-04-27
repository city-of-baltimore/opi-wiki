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

- GitHub Pages is the canonical production deployment path.
- Fly.io is preview/test infrastructure only unless the repo's deployment
  posture changes intentionally and the docs are updated with it.
- The checked-in `Dockerfile` should remain a real preview artifact, not an
  abandoned convenience file.
- Do not edit generated `site/` output.

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
