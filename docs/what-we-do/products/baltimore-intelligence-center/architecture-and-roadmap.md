# Architecture

{{ page_header(summary="How the platform and intelligence layers fit together.") }}

## The layered architecture

BIC extends the [Baltimore City Data Platform](../baltimore-city-data-platform.md) rather than rebuilding it. The platform ingests city data and produces governed data products; BIC adds intelligence capabilities on top and reads only those approved outputs.

| Layer | What it does |
| --- | --- |
| **Data foundation** | Ingests approved sources, applies governance and quality checks, and publishes trusted data products. |
| **Definitions and context** | Keeps shared measures, dimensions, and relationships consistent across use cases. |
| **Analytical services** | Supports reusable analysis and carefully evaluated decision-support methods. |
| **AI interaction layer** | Supports plain-language questions grounded in approved definitions and sources. |
| **User experiences** | Presents approved information for specific city-service and performance workflows. |

The integration contract is one rule: the intelligence layers read governed outputs and never re-ingest raw sources. That preserves one official record and makes the same governance controls apply downstream, even as implementation components evolve.


## Read alongside

- [Baltimore City Data Platform](../../products/baltimore-city-data-platform.md): the data foundation and its pipeline.
- [Capabilities](products-and-capabilities.md): what this architecture can support.
- [Data Governance](../../programs/data-governance/index.md): the governance that runs through every layer.
