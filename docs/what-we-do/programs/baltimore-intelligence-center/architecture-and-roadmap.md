# Architecture

{{ page_header(summary="How the platform and intelligence layers fit together.") }}

## The layered architecture

BIC extends the [Baltimore City Data Platform](../../products/baltimore-city-data-platform.md) rather than rebuilding it. The platform ingests city data and turns it into governed marts; BIC adds the intelligence layers on top, as a separate service that reads those marts.

| Layer | What it does |
| --- | --- |
| **Data foundation** (Baltimore City Data Platform) | Ingests sources, cleans and governs them, and publishes governed marts — the single source of truth. |
| **Semantic layer** | Defines the city's metrics and KPIs once, with conformed dimensions (geography, agency, status, date) and status crosswalks across systems. |
| **Knowledge graph** | Maps how city entities relate — resident → service request → street → district → crew — so questions can follow real-world relationships. |
| **ML & data science** | Feature engineering, a model registry, and predictive models for problems like vacants and code enforcement. |
| **Generative AI** | Answers questions in plain language through governed tools, grounded in the semantic layer and city documents. |
| **Consumers** | OPI analysts, agency staff, leadership, and residents — through StatGPT and situational-awareness assistants. |

**The integration contract.** The intelligence layers read the platform's governed marts and never re-ingest raw sources. That single rule keeps one source of truth and keeps governance enforceable everywhere downstream.

A deliberate choice sits underneath: the data platform is open-source (Dagster, dbt, PostgreSQL), while the AI application layer is Microsoft-native (Azure OpenAI, AI Search, an MCP gateway). A hybrid — open-source data, Azure AI — is a reasonable, deliberate design, not an accident.


## Read alongside

- [Baltimore City Data Platform](../../products/baltimore-city-data-platform.md) — the data foundation and its pipeline.
- [Products & capabilities](products-and-capabilities.md) — what gets built on this architecture.
- [Responsible data & AI](responsible-data-and-ai.md) — the governance that runs through every layer.
