# Products & capabilities

{{ page_header(summary="The intelligence products BIC delivers, and the capabilities behind them.") }}

## The products

BIC's first products turn the governed platform into decisions.

### City Services Intelligence

A situational-awareness view of the city, from the citywide level down to district, neighborhood, block, and parcel — including a 3D map. It pairs descriptive analytics and trends with a generative-AI query, so a leader can ask a question in plain language and get a grounded answer. The first prototype is a District 6 neighborhood dashboard.

### StatGPT

An assistant that answers performance questions from the record of CitiStat itself — its memos, decks, follow-ups, and KPIs — combined with live agency data through governed tools. Starting with DOT, it answers questions like:

- "Show every DOT Stat commitment about traffic calming in the last year."
- "What did DOT say about signal outages in the last three meetings?"
- "Find all unresolved follow-ups connected to pedestrian safety in Council District 7."

StatGPT makes the discipline of [CitiStat](../citistat/index.md) searchable — surfacing new hotspots, metrics that are off track, and open follow-ups.

### ML decision support

Machine-learning decision intelligence for concentrated, cross-agency problems — starting with vacant properties and code enforcement. It moves past description to insight, likely impact, scenario-based recommendations, and the trade-offs of each action.

## The capabilities behind them

Every product draws on the same governed capabilities, built once and reused:

- **Semantic layer** — the city's metrics and KPIs defined once, with conformed dimensions and status crosswalks, so every product answers from the same definitions.
- **Knowledge graph** — the relationships among city entities (resident, service request, street, district, crew), which lets an assistant follow a question across agencies.
- **Machine learning** — feature engineering, a model registry, and predictive models, governed like any other data product.
- **Generative AI** — plain-language answers through governed tools, using retrieval over city documents and the knowledge graph. Every answer is grounded in an approved definition and cites where it came from.
- **A shared design system** — a City- and Maryland-compliant interface standard so the products feel like one coherent tool.

## What makes them trustworthy

No product reaches raw data directly. Every AI-facing query passes through a governed tool that enforces the data tiers and refuses anything that has not cleared governance, and every answer is grounded in an approved definition with its provenance. The full model is in [Responsible data & AI](responsible-data-and-ai.md).

## Read alongside

- [Architecture](architecture-and-roadmap.md) — the layers these products run on.
- [Responsible data & AI](responsible-data-and-ai.md) — how products are governed, grounded, and logged.
- [CitiStat](../citistat/index.md) — the performance program StatGPT draws on.
