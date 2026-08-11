# OPI Foundations — Repository Overview

OPI Foundations explains how Baltimore City's Mayor's Office of Performance and
Innovation works. It brings the office's purpose, teams, services, programs,
products, methods, and shared vocabulary into one maintained website.

This guide is for a product manager, content owner, or maintainer who is new to
the repository. It explains what the site is, how its information is organized,
how a change reaches the website, and how to run the same checks locally.
It is product and repository onboarding, not an employee-orientation checklist.

The live website is
[city-of-baltimore.github.io/opi-wiki](https://city-of-baltimore.github.io/opi-wiki/).

## The product at a glance

OPI Foundations is a documentation product. There is no application backend,
database, sign-in flow, or production container. Markdown and small YAML data
files are the source; MkDocs turns them into a static website; GitHub Pages
hosts the result.

```text
Content owner or contributor
          |
          v
Markdown, navigation, and shared data in this repository
          |
          v
Automated editorial, structural, link, and accessibility checks
          |
          v
Review and merge to main
          |
          v
MkDocs build -> GitHub Pages
```

The repository is also the change record. A reader can use the edit link on a
page to propose a correction, and a reviewer can see the exact words,
navigation, ownership metadata, and test evidence that changed together.

## Who it serves

The site is written for people who need to understand or work with OPI:

- City leaders and agency partners who need to know what OPI does and how to
  engage it;
- OPI staff who need a shared description of the office's operating model;
- residents, Council staff, researchers, and peer governments looking for a
  clear account of Baltimore's performance and innovation practices; and
- maintainers and content owners responsible for keeping that account current.

It is a reference, not an intake or case-management system. Requests for OPI
support follow the path described in
[How to Engage OPI](docs/what-we-do/how-to-engage-opi.md).

## How the information is organized

The website has four main sections:

| Section | What a reader finds there |
| --- | --- |
| [About Us](docs/about-us/index.md) | OPI's mission, identity, culture, letters, teams, and roles |
| [How We Work](docs/how-we-work/index.md) | The operating model, work cycle, organization, and Staff Guide |
| [What We Do](docs/what-we-do/index.md) | Services, programs, and products |
| [Resources](docs/resources/index.md) | Shared definitions, playbooks, contribution guidance, and supporting references |

Within that structure, four content types must remain distinct:

| Type | Plain-language meaning | Examples |
| --- | --- | --- |
| Team | A group with staff and budget | Director's Office; Performance; Data and Analytics; Innovation Lab |
| Service | What OPI delivers | AdminOps; Citywide Performance Management; Citywide Data and Analytics; Innovation Lab; Cross-Agency Delivery |
| Program | An ongoing routine that may span teams | CitiStat; Data Governance; Open Data; Citywide Data Network |
| Product | A tool or platform OPI builds or supports | Baltimore Intelligence Center; Baltimore City Data Platform; Baltimore City Performance Portal; Baltimore 311 Explorer |

Two distinctions prevent recurring confusion:

- Innovation Lab is both a team and a service.
- CitiStat is a program supported by all four teams, not a fifth team. In the
  current structure, OPI's Executive Director also serves as CitiStat Director.

The [Glossary of OPI Terms](docs/resources/reference/glossary.md) is the
canonical vocabulary reference. Prefer linking to a canonical definition or
method page over restating it in several places.

## How a page is assembled

Most pages are ordinary Markdown under `docs/`. A few neighboring files add
structure without pushing repeated markup into the content: `.pages` orders and
labels a section's navigation, `.metadata.yml` records the owner and review
dates for nearby pages, `*.cards.yml` supplies landing-page cards, and
`_data/people.yml` supplies the shared staff and organization views.

`mkdocs.yml` owns site-wide configuration. Shared rendering helpers live in
`main.py` and `scripts/repo_tools/`. Styling is split by responsibility under
`docs/assets/stylesheets/`. The generated `site/` directory is build output —
never edit it directly.

The [page data model](README.md#page-data-model) in the README is the rule for
choosing among these: reach for the smallest pattern that fits, and leave a page
as plain Markdown when it can be.

## How a change reaches the website

1. Find the canonical page and confirm that the proposed change belongs there.
2. Update the page and any companion navigation, cards, metadata, or references
   in the same change.
3. Preview the result and run the appropriate verification gate.
4. Open a pull request for substantive or structural work and request the
   content owner's review. How much review a change needs depends on its kind —
   [`MAINTAINERS.md`](MAINTAINERS.md) is the operating manual that decides.
5. Merge to `main` after the required review. The deploy workflow rebuilds the
   site and publishes the generated artifact to GitHub Pages.

The repository uses three nested gates: `task ci` is the fast static pass,
`task prepush` adds the tests and a strict site build, and `task validate` adds
real-browser and accessibility checks before a release. Each is a strict superset
of the one before it, and all three are defined once in `scripts/verify.py`,
which keeps local, pull-request, and deployment behavior from drifting apart.
The [Technical Specification](product/technical-spec.md#verification-architecture)
lists exactly what each tier adds.

## Running it locally

Editing the wiki does not require running anything. Content changes can go
through the GitHub web editor, and the checks run for you.

To preview locally you need Python 3.13 or 3.14, `uv`, and
[Task](https://taskfile.dev/):

```bash
task setup
task serve
```

Open <http://127.0.0.1:5208>. The server reloads when a source file changes.
Before handing off a substantial change, run `task validate` — the pre-deploy
proof. It needs Chromium once per machine
(`uv run playwright install chromium`).

[Local development](README.md#local-development) in the README is the full
account: what `task validate` does and does not prove, the Docker Compose
alternative for a host without Python, and how to point the browser checks at a
running preview.

## A product manager's change checklist

Before proposing a content or structure change, ask:

1. Who is the reader, and what should they be able to understand or do?
2. Is this the canonical page, or would the change create a second source of
   truth?
3. Is the item a team, service, program, or product?
4. Does the nearest `.metadata.yml` name the right owner and review dates?
5. If a page moved, did its navigation, cards, links, and redirects move with
   it?
6. Does the language match [STYLE.md](STYLE.md) and the
   [Glossary](docs/resources/reference/glossary.md)?
7. What command proves the change is ready?

Visible changes are product decisions. Capture before-and-after evidence for a
layout, navigation, or shared-component change and name the pages and viewports
reviewed in the pull request.

## Where to go deeper

- [Product requirements](product/product-requirements.md) — the
  product boundary, audiences, complete capability contract, and open decisions
- [User stories](product/user-stories.md) — the reader,
  contributor, owner, and maintainer journeys the website must support
- [Technical specification](product/technical-spec.md) — how the current
  repository, rendering, verification, preview, and publishing boundaries work
- [README](README.md) — setup, architecture, commands, and repository layout
- [Contributing](CONTRIBUTING.md) — how to propose and review a change
- [Maintainer manual](MAINTAINERS.md) — ownership, editorial workflow, and
  structural conventions
- [Engineering and content rules](AGENTS.md) — enforced gates, boundaries, and
  the excellence bar
- [Editorial style](STYLE.md) — voice, plain language, and formatting

For a first tour, read the
[home page](docs/index.md),
[How Work Moves Through OPI](docs/how-we-work/how-work-moves-through-opi.md),
[What We Do](docs/what-we-do/index.md), and the
[Glossary](docs/resources/reference/glossary.md). Together they explain the
product's information model and the office model it represents.
