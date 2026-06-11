# Operating Model

{{ page_badge() }}

> Two organizational homes, one squad — and the city/Sand split that makes the engagement actually run.

## Two homes, one squad

The Baltimore Intelligence Center has two organizational homes that have to work as one. The Innovation Lab is the home for product delivery, design, and applied technology. The Data and Analytics team is the home for the platform, the catalog, the semantic layer, and engineering. Performance and CitiStat is the lead agency-partner anchor for intelligence products in their first year. The BIC squad model resolves the seams.

## How work flows

1. **Demand intake** — every new use case enters through a single intake process owned by the Project Lead and the Data Governance and Analytics Manager. No side channels.
2. **Risk and governance review** — each use case is risk-tiered (low/medium/high) and routed through the appropriate review path. Law, BCIT security, and Procurement are involved as needed.
3. **Discovery** — the Product Manager and lead workstream owners scope the use case, identify required data, and confirm semantic-layer needs.
4. **Build** — the BIC squad delivers in two-week iterations with a defined backlog and demo cadence.
5. **Pilot** — each product runs a structured pilot with named users, baseline metrics, and weekly feedback loops.
6. **Operate** — once a product graduates from pilot, it is governed by a monthly scorecard, an incident path, and a retirement clause if it stops earning its keep.

For the AI governance steps that intake feeds into, see [Governance and Risks](governance-and-risks.md#ai-governance-the-lightweight-but-real-version).

## How OPI and Sand actually share the work

The vendor-led / city-led split is real, not ceremonial. Sand carries the heavy lift in months 0–6. OPI staff pair, learn, and gradually take operational ownership. By month 9, OPI staff are leading day-to-day delivery with Sand on call. By month 12, Sand is in an advisory posture and the city carries the program.

The four-stage transfer model that drives this transition is described in [Capability Transfer and Target State](capability-transfer-and-target-state.md#the-four-stage-transfer-model).

## Tooling baseline

| **Layer**                   | **Choice**                                                                     |
|-----------------------------|--------------------------------------------------------------------------------|
| Cloud                       | Microsoft Azure (City tenant)                                                  |
| Warehouse                   | PostgreSQL on Azure                                                            |
| Storage                     | Azure Blob Storage                                                             |
| Ingest and orchestration    | Containerized Python jobs via Docker; Azure DevOps or GitHub Actions for CI/CD |
| Modeling pattern            | Medallion architecture (bronze/silver/gold)                                    |
| Catalog                     | OpenMetadata, open-source, self-hosted on Azure                                |
| Semantic layer              | Sand-built on the warehouse; MCP-style server and tool layer                   |
| BI / GenBI                  | In-scope for months 10–18 — tool selection during M2                           |
| Identity, access, and audit | Microsoft Entra ID (Azure AD) for SSO; Azure RBAC for resource access; Azure activity logs and Defender for Cloud for audit |

## Responsibility split — city vs Sand

The split is read with two questions in mind: who decides, and who delivers.

| **Activity**                            | **Decides**           | **Delivers (months 0–6)** | **Delivers (months 7–12)** |
|-----------------------------------------|-----------------------|---------------------------|----------------------------|
| Engagement scope and sequencing         | OPI Executive Sponsor | Sand                      | Sand + OPI                 |
| Architecture and platform design        | OPI + Sand            | Sand                      | OPI lead, Sand advisory    |
| Data governance policy authoring        | OPI                   | Sand drafts               | OPI                        |
| Catalog deployment and operation        | OPI                   | Sand                      | OPI                        |
| Source-system ingest pipelines          | OPI                   | Sand                      | OPI                        |
| KPI dictionary content                  | OPI (Vera Choo)       | OPI + Sand                | OPI                        |
| Semantic layer implementation           | OPI + Sand            | Sand                      | OPI lead, Sand advisory    |
| Use case intake and risk tiering        | OPI                   | OPI + Sand                | OPI                        |
| Intelligence product design and roadmap | OPI Product Manager   | Sand + OPI                | OPI lead, Sand advisory    |
| Intelligence product engineering        | OPI + Sand            | Sand lead                 | OPI lead, Sand advisory    |
| Adoption, training, and user research   | OPI                   | Sand + OPI                | OPI                        |
| Public release of any data product      | OPI Executive Sponsor | OPI                       | OPI                        |
| Operational support and on-call         | OPI                   | Sand                      | OPI primary, Sand on-call  |

## Boundary cases

- **BPD interfaces** — BPD owns Axon and any direct connection to it. The engagement integrates through whatever interfaces BPD stands up.

- **BCIT-managed systems** — OPI partners with BCIT as the system of record owner; the engagement does not duplicate or replace BCIT operational responsibilities.

- **Open Data** — the Open Data program transfers from BCIT to OPI in FY27. Sand supports the data side of the transition; the program management transition is OPI’s.
