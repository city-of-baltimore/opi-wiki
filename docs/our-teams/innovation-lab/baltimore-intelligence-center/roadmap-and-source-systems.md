# Roadmap and Source Systems

{{ page_header(summary="Twelve vendor months, then six city-led months — and the source-system sequencing that makes the schedule real.") }}

Twelve vendor months, then six city-led months. The vendor-led period is structured around two milestones — Foundation (M1, months 0–6) and Launch (M2, months 7–12). The city-led continuation is the third milestone (M3, months 13–18): an Expansion phase that proves the program runs without daily vendor support.

Source-system sequencing is the single biggest determinant of whether the engagement delivers in 12 months. That is why the roadmap and the source waves are read together on this page.

## M1 — Foundation (months 0–6)

**Platform**

- Stand up the governed Azure platform: medallion architecture, ingest framework, monitoring, security review with BCIT.
- Ingest wave-one priority sources (see [Source-system priorities](#source-system-priorities)).
- Deploy OpenMetadata; populate with wave-one sources; assign data owners and stewards.

**Products**

- Build the city services semantic layer; publish KPI dictionary v1.
- Launch City Services Intelligence in disciplined pilot with named users.
- Launch StatGPT pilot with CitiStat City Services and Public Safety leads.
- Stand up design system v1; adoption playbook for the two flagship products.

**Governance**

- Draft and ratify Data Governance Policy v1 (Sand drafts, Vera owns ratification).
- Establish AI use case intake, risk tiering, and approval process.

## M2 — Launch (months 7–12)

**Platform**

- Ingest wave-two priority sources.
- Stand up the SharePoint Governance Scanner and Project Status Reporting Tool.

**Products**

- Expand semantic layer to public safety and neighborhoods.
- Launch OPI Internal Intelligence in months 7–9.
- Decide BI/GenBI tool selection.

**Governance**

- Run AI evaluation framework on flagship products; publish monthly quality report.
- Begin structured capability transfer in earnest — OPI staff take operational ownership of platform and one flagship product.
- Ratify Data Governance Policy v2 with production lessons folded in.

## M3 — City-led Expansion (months 13–18, post-vendor)

**Platform**

- OPI runs the platform, the catalog, the semantic layer, and the flagship products independently.

**Products**

- Replicate the City Services Intelligence pattern in a second domain (permitting, housing, or vacants).
- Stand up GenBI, Neighborhoods Map, and Neighborhoods Explorer with Chat.

**Governance**

- Sand on call for advisory and architecture review only.
- Publish a public-facing case study and an internal continuation plan for years two and three.

## Phase gate criteria

| **Gate** | **When**        | **Must be true to advance**                                                                                                                                                                                                                               |
|----------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| M1 → M2  | End of month 6  | Platform stable for wave-one sources; Data Governance Policy ratified; KPI dictionary v1 published; City Services Intelligence and StatGPT in disciplined pilot with measured baseline; design system v1 in use; AI use case intake operating.            |
| M2 → M3  | End of month 12 | OPI staff lead daily operations across platform, catalog, semantic layer, and at least one flagship product; AI evaluation framework producing monthly reports; OPI Internal Intelligence in daily use; capability-transfer scorecard at or above target. |
| M3 close | End of month 18 | A second domain has been added without vendor in the chair; continuation plan and budget approved; public case study published; program is sustainable on city staff plus on-call advisory.                                                               |

## Source-system priorities

!!! note "Source-system readiness checklist"

    Before any source goes live, the following must be true:

    - Data owner and steward named in OpenMetadata before any pipeline goes live.
    - Access agreement and security review on file with BCIT.
    - Refresh schedule, monitoring, and alerting defined and tested.
    - Data quality rules in place for any source feeding a production intelligence product.
    - Lineage from source to semantic layer to product visible in the catalog.

The order below is locked. Wave one feeds City Services Intelligence and the StatGPT pilot. Wave two opens up permitting, capital, fleet, and facilities. Axon is explicitly excluded from direct ingestion — BPD will set up its own interfaces, and the engagement integrates through what BPD provides.

### Wave one — months 0–6

| **Source**                                                    | **System / interface**              | **Primary product use**                               |
|---------------------------------------------------------------|-------------------------------------|-------------------------------------------------------|
| 311                                                           | Salesforce SaaS API                 | City Services Intelligence; StatGPT for City Services |
| Cityworks                                                     | Direct (TBD interface confirmation) | City Services Intelligence; StatGPT for City Services |
| Emergency Dispatch (CAD)                                      | Direct database / interface (TBD)   | StatGPT for Public Safety                             |
| Public Safety Incidents                                       | Existing extract / interface        | StatGPT for Public Safety; City Services Intelligence |
| Crash Database                                                | Existing extract / interface        | City Services Intelligence; Public Safety analytics   |
| Vacant Properties                                             | Existing OPI dataset                | Neighborhoods analytics; permitting alignment         |
| Vacant Lots                                                   | Existing OPI dataset                | Neighborhoods analytics                               |
| Neighborhood Layers (CSAs, neighborhoods, planning districts) | GIS reference data                  | Foundation for every product’s geographic context     |
| American Community Survey                                     | Census data                         | Demographic context for every product                 |

### Wave two — months 7–12

| **Source**                     | **System / interface**            | **Primary product use**                   |
|--------------------------------|-----------------------------------|-------------------------------------------|
| Accela                         | SQL Server direct                 | Permitting domain                         |
| ProjectDox (permit documents)  | SQL Server direct                 | Permitting domain                         |
| Capital Projects               | Existing system / interface (TBD) | Capital Stat support; portfolio analytics |
| Citywide Fleet (Faster)        | Direct (TBD)                      | Fleet operations; cross-domain analytics  |
| Citywide Facilities (Archibus) | Direct (TBD)                      | Facilities operations                     |
| AVL (Navman)                   | Vendor API / extract              | Operations and routing analytics          |

### Explicit exclusion — Axon

The engagement will not connect directly to Axon. Baltimore Police Department will set up its own interfaces and provide the data. The engagement’s scope is to integrate through whatever interfaces BPD stands up, not to negotiate or build a direct Axon connection. This is locked in to avoid a recurring source of slippage in prior data initiatives.

### Wave three — city-led, months 13–18

Wave three is determined by city-led work in M3 and reflects the second-domain expansion (permitting, housing, or vacants), plus any additional sources required to support GenBI, the Neighborhoods Map, and the Neighborhoods Explorer with Chat. Sand provides advisory input only; OPI staff lead.

