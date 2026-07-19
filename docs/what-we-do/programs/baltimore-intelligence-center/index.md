# Baltimore Intelligence Center

{{ page_header(summary="Baltimore's program to make city data unified, trusted, and usable — the foundation for responsible AI in city government.") }}

The Baltimore Intelligence Center (BIC) is the City's program for turning fragmented data into trusted intelligence — and for using AI responsibly to make city services faster, more coordinated, and more accountable. The Mayor's Office of Performance and Innovation leads it, in partnership with Sand Technologies, and is building it to run on city-owned operations rather than a permanent vendor.

BIC gives leadership, agencies, and residents a trustworthy, shared view of how the city is performing, and the responsible-AI capability to ask questions of that view in plain language.

## The problem it solves

- **Fragmented, untrusted data.** City data is scattered across source systems with no shared governance, stewardship, lineage, or KPI definitions, so the same question gets different answers.
- **No AI operating model.** AI capabilities lack standard intake, approval, oversight, and monitoring, so they cannot safely scale into real workflows.
- **Limited institutional capability.** If the capability lives with a vendor, the products and governance degrade after launch. BIC is built to transfer to OPI.

## How it fits together

BIC is layered, and each layer has one job:

- The **[Baltimore City Data Platform](../../products/baltimore-city-data-platform.md)** is the governed foundation — it ingests city data and turns it into trustworthy governed marts.
- **BIC** adds the intelligence layers on top: a semantic layer that defines the city's metrics once, a knowledge graph of how city entities relate, and the machine-learning and generative-AI capabilities that turn governed data into answers.
- The **products** — City Services Intelligence, StatGPT, and others — sit on top of that, reading only governed outputs.

The seam between them is a firm rule: the intelligence layer reads the platform's governed marts and never re-ingests raw data. **OPI owns what the data means; the platform enforces it.**

## What it delivers

- A **[governed data platform and semantic layer](architecture-and-roadmap.md)** covering priority city-services and public-safety domains, with one citywide KPI dictionary.
- **[Intelligence products](products-and-capabilities.md)** — situational awareness across the city, ML decision support for problems like vacants and code enforcement, and **StatGPT**, an assistant that answers performance questions from CitiStat memos, decks, follow-ups, and agency data.
- A working model for **[responsible data and AI](responsible-data-and-ai.md)** — classification, access control, human oversight, grounding, and logging that operate in practice, not on paper.

## Where it's headed

BIC is built in stages: stand up the governed foundation, prove value with the first products in disciplined pilots, then scale to more use cases under city-led operations. Data is ingested in two waves — the first by December 2026, the second by June 2027 — and the program starts deliberately small, on low-sensitivity city-services data, to earn trust before it expands.

## In this section

- **[Architecture](architecture-and-roadmap.md)** — how the platform and intelligence layers fit together.
- **[Products & capabilities](products-and-capabilities.md)** — the intelligence products and the semantic, graph, ML, and generative-AI capabilities behind them.
- **[Responsible data & AI](responsible-data-and-ai.md)** — the governance model, the four data tiers, and what is deliberately out of scope.
