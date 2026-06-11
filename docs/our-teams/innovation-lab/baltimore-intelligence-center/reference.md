# Reference

{{ page_badge() }}

> Full squad roster, expected Sand roles, and a glossary of the program’s working vocabulary.

## Full squad roster

OPI staff who are part of the BIC, with full positions and home teams. Sand roles are listed by function rather than name and are confirmed in week one.

| **Role on the BIC**                            | **Name**                  | **Position**                                   | **Home team**                  |
|------------------------------------------------|---------------------------|------------------------------------------------|--------------------------------|
| Executive Sponsor and interim BIC Project Lead | Dartanion Swift-Williams  | Executive Director and Chief Data Officer, OPI | OPI — Director’s Office        |
| Product Manager                                | Chiemeka Okeoma           | Senior Product Engineer                        | OPI — Innovation Lab           |
| Project Manager                                | Mallory Screws            | Project Manager                                | OPI                            |
| Data Engineering Lead                          | Alejandro Zuniga Sosa     | Principal Data Engineer                        | OPI — Data and Analytics       |
| Platform Engineering Lead                      | Koby Samuel               | Principal Platform Engineer                    | OPI — Data and Analytics       |
| Civic Design and Evaluation                    | Selenea Gibson            | Civic Designer                                 | OPI — Innovation Lab           |
| Data Engineering                               | Briya Bhakta              | Senior Data Engineer                           | OPI — Data and Analytics       |
| Technical Program Management                   | Roberto Herbruger         | Technical Program Manager                      | OPI — Data and Analytics       |
| Data Governance and Analytics                  | Vera Choo                 | Data Governance and Analytics Manager          | OPI — Data and Analytics       |
| Deputy CDO and platform partnership            | Jason Howard, PhD         | Deputy Chief Data Officer                      | OPI — Data and Analytics       |
| Product Engineering                            | Xander Jake de los Santos | Product Engineer                               | OPI — Innovation Lab           |
| CitiStat — City Services lead                  | Nelson Gomes Boronat      | CitiStat Analyst                               | OPI — Performance |
| CitiStat — City Services lead                  | Ross Hackett              | CitiStat Analyst                               | OPI — Performance |
| CitiStat — Public Safety lead                  | Derek Thomas              | CitiStat Analyst                               | OPI — Performance |

## Sand Technologies — expected roles

- **Engagement Manager** — weekly partnership with the Project Lead.

- **Technical Program Manager** — daily partnership with the OPI Project Manager.

- **Principal Architect** — platform and semantic-layer architecture lead.

- **Semantic Layer Lead** — KPI dictionary and MCP/tool layer implementation.

- **Data Engineering team** — ingest, transformations, quality.

- **AI/ML Engineer** — model integration, grounding, evaluation framework.

- **Product Engineering** — intelligence products and internal operating tools.

- **Design Lead** — design system and product UX.

- **UX Researcher** — user research and adoption support.

- **Capability Transfer Lead** — structured handoff across all workstreams.

- **Governance Advisor** — Data Governance Policy authorship and review templates.

## Glossary

| **Term**                      | **Definition**                                                                                                                                                                                                |
|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BIC                           | Baltimore Intelligence Center — the named squad delivering this engagement. Operationally housed in the Innovation Lab; technically anchored in Data and Analytics.                                           |
| Medallion architecture        | A three-layer data modeling pattern — bronze (raw), silver (cleaned and conformed), gold (curated for analytics) — used to organize the warehouse.                                                            |
| Semantic layer                | A modeled, governed set of definitions that translate raw warehouse data into the business and policy concepts the city actually uses (KPIs, domains, entities). Sits between the warehouse and the products. |
| MCP / tool layer              | A model-context-protocol-style server that exposes governed query patterns, KPI logic, and source mappings to AI products. Every AI response is grounded through this layer.                                  |
| KPI dictionary                | The canonical citywide list of metric definitions — owner, formula, source, refresh, sensitivity, and approved use. The single source of truth for any metric used by an intelligence product.                |
| Catalog (OpenMetadata)        | The open-source, self-hosted data catalog used to register every dataset with owner, steward, lineage, sensitivity, and quality rules.                                                                        |
| Use case intake               | The single-channel process by which any new AI or data product proposal enters the BIC — risk-tiered, reviewed, and approved before any production work begins.                                               |
| Grounded-answer rate          | A quality metric — the share of AI product responses that are produced through the MCP/tool layer with attributable evidence (versus unsupported model-only output).                                          |
| Disciplined pilot             | A bounded product release with named users, baseline metrics, weekly feedback, and a clear graduation or sunset decision at month six.                                                                        |
| Capability transfer scorecard | Monthly tracker measuring the share of operational tasks (ingest, catalog, semantic layer, product release) led by OPI staff versus Sand. Target: at or above 70% by month 12.                                |
| StatGPT                       | A grounded decision-support assistant for CitiStat preparation, scoped initially to City Services and Public Safety leads.                                                                                    |
| City Services Intelligence    | The lead intelligence product — a grounded assistant that combines 311, work orders, location, public safety incidents, and neighborhood data to support service-delivery decisions.                          |
| OPI Internal Intelligence     | A grounded assistant for OPI staff covering the office’s own knowledge management and operating discipline.                                                                                                   |
