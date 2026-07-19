# Baltimore Intelligence Center

{{ page_header(summary="Baltimore's program to make city data unified, trusted, and usable, and the foundation for responsible AI in city government.") }}

The Baltimore Intelligence Center (BIC) turns the city's scattered data into one trusted picture, and lets the city use AI on top of it to make services faster, better coordinated, and easier to hold accountable. The Mayor's Office of Performance and Innovation leads BIC, in partnership with Sand Technologies, and is building it to run on city staff rather than a permanent vendor.

BIC gives leadership, agencies, and residents one reliable view of how the city is performing, and lets them ask questions of that view in plain language.

## The problem it solves

Today the same question gets different answers, because city data sits in separate source systems with no shared governance, stewardship, lineage, or KPI definitions. AI has no operating model either: without standard intake, approval, oversight, and monitoring, it cannot safely move into real workflows. And when this kind of capability lives with a vendor, the products and the governance behind them decay after launch. BIC is built to transfer to OPI so that does not happen.

## How it fits together

BIC is layered, and each layer has one job. The [Baltimore City Data Platform](../../products/baltimore-city-data-platform.md) is the governed foundation: it ingests city data and turns it into trustworthy governed marts. BIC adds the intelligence layers on top, a semantic layer that defines the city's metrics once, a knowledge graph of how city entities relate, and the machine-learning and generative-AI capabilities that turn governed data into answers. The products, including City Services Intelligence and StatGPT, sit above that and read only governed outputs.

One firm rule holds the seam together: the intelligence layer reads the platform's governed marts and never re-ingests raw data. OPI decides what the data means, and the platform enforces it.

## What it delivers

BIC delivers a [governed data platform and semantic layer](architecture-and-roadmap.md) covering priority city-services and public-safety domains, with one citywide KPI dictionary. On top of that come the [intelligence products](products-and-capabilities.md): situational awareness across the city, machine-learning decision support for problems like vacants and code enforcement, and StatGPT, an assistant that answers performance questions from CitiStat memos, decks, follow-ups, and agency data. Running through all of it is a working model for [responsible data and AI](responsible-data-and-ai.md), where classification, access control, human oversight, grounding, and logging operate in practice, not on paper.

## Where it's headed

BIC is built in stages. First it stands up the governed foundation, then it proves value with the first products in disciplined pilots, then it scales to more use cases under city-led operations. Data is ingested in two waves, the first by December 2026 and the second by June 2027. The program starts deliberately small, on low-sensitivity city-services data, to earn trust before it expands.

## In this section

- [Architecture](architecture-and-roadmap.md): how the platform and intelligence layers fit together.
- [Products & capabilities](products-and-capabilities.md): the intelligence products and the semantic, graph, ML, and generative-AI capabilities behind them.
- [Responsible data & AI](responsible-data-and-ai.md): the governance model, the four data tiers, and what is deliberately out of scope.
