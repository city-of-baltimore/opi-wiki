# Products & capabilities

{{ page_header(summary="The intelligence products BIC delivers, and the capabilities behind them.") }}

## The products

BIC's first products turn the governed platform into decisions.

### City Services Intelligence

A view of the city that runs from the citywide level down to district, neighborhood, block, and parcel, including a 3D map. It pairs descriptive analytics and trends with a generative-AI query, so a leader can ask a question in plain language and get an answer grounded in the governed data. The first prototype is a District 6 neighborhood dashboard.

### StatGPT

An assistant that answers performance questions from the record of CitiStat itself, its memos, decks, follow-ups, and KPIs, combined with live agency data through governed tools. Starting with DOT, it answers questions like:

- "Show every DOT Stat commitment about traffic calming in the last year."
- "What did DOT say about signal outages in the last three meetings?"
- "Find all unresolved follow-ups connected to pedestrian safety in Council District 7."

StatGPT makes the record of [CitiStat](../citistat/index.md) searchable, so users can find new hotspots, metrics that are off track, and open follow-ups.

### ML decision support

Machine-learning decision support for concentrated, cross-agency problems, starting with vacant properties and code enforcement. It goes past describing the problem to estimating likely impact, laying out scenario-based options, and showing the trade-offs of each action.

## The capabilities behind them

Every product draws on the same governed capabilities, built once and reused. The semantic layer defines the city's metrics and KPIs once, with conformed dimensions and status crosswalks, so every product answers from the same definitions. The knowledge graph maps the relationships among city entities (resident, service request, street, district, crew), which lets an assistant follow a question across agencies. Machine learning adds feature engineering, a model registry, and predictive models, governed like any other data product. Generative AI gives plain-language answers through governed tools, using retrieval over city documents and the knowledge graph, and every answer is grounded in an approved definition and cites where it came from. A shared design system, compliant with City and Maryland standards, keeps the products feeling like one coherent tool.

## What makes them trustworthy

No product reaches raw data directly. Every AI-facing query passes through a governed tool that enforces the data tiers and refuses anything that has not cleared governance, and every answer is grounded in an approved definition and shows where it came from. The full model is in [Responsible data & AI](responsible-data-and-ai.md).

## Read alongside

- [Architecture](architecture-and-roadmap.md): the layers these products run on.
- [Responsible data & AI](responsible-data-and-ai.md): how products are governed, grounded, and logged.
- [CitiStat](../citistat/index.md): the performance program StatGPT draws on.
