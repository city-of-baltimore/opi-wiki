# Contributing

{{ page_header(summary="How to suggest a change, report a problem, or propose new content.") }}

## Three ways to contribute

{{ card_grid_from("resources/contributing.cards.yml") }}

## How proposed changes are reviewed

Every change follows the same path. A proposal comes in as a pull request, an issue, or an email. The wiki maintainer triages it within five business days. The content owner for that page then reviews it for accuracy, so a change to a Data and Analytics page goes to the Deputy CDO. Once it is approved, the change ships to the live site automatically through GitHub Actions.

## Editorial voice

OPI Foundations is written in plain language. We avoid jargon where we can, define it where we can't, and prefer concrete nouns and active verbs. When in doubt, write the way you'd explain something to a thoughtful friend who doesn't work in city government. The full standard, including the words we replace and how we handle bullets, tables, and em-dashes, is in `STYLE.md` at the repository root.

## What lives where

This is the public reference. Internal SOPs, personnel records, and vendor contracts live elsewhere, in SharePoint, HR systems, and procurement records.

## Operating model consistency checklist

Before opening a documentation PR, check whether the page uses OPI's core operating model consistently.

- Does the page distinguish the four content types: team (portfolio), service, program, and product?
- Does it place CitiStat as a program supported by all teams, and Cross-Agency Delivery as a service (not a staffed team)?
- Does it spell out Cross-Agency Delivery in full, never "CAD"?
- Does it use Innovation Lab for the work of solving problems and Cross-Agency Delivery for cross-agency coordination?
- Does the page (or its section `.metadata.yml`) name an owner and a review cadence?
- Does it describe CitiStat as how the city reviews performance and follows through, rather than just a meeting calendar?
- Does it link to the official method page when using terms like Tiger Team, Stat, delivery activation, or product discovery?
- Does it name the audience and public posture?
- Does it avoid retired or use-with-care terms unless the historical context requires them?
