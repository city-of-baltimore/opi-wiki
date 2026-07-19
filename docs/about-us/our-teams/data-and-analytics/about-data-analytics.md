# About Data and Analytics

{{ page_header(summary="How OPI makes Baltimore's data trustworthy, governed, and useful — and builds the platform the city's intelligence runs on.", category="ABOUT · SERVICE") }}

The Data and Analytics team is Baltimore's civic data infrastructure team. It turns fragmented administrative data into shared, governed assets: reliable measures, reusable datasets, dashboards, maps, open data, and the platform the city's analytics and AI products run on. It sits at the seam between agency operations, executive priorities, public transparency, and BCIT's infrastructure.

The team owns the **meaning** of the city's data: what a metric is, who owns it, how sensitive it is, and how it may be used. That principle runs through everything below.

## What the team does

- Build and operate the **[Baltimore City Data Platform](../../../what-we-do/products/baltimore-city-data-platform.md)** — the governed data foundation: ingestion pipelines, a medallion warehouse, shared datasets, and APIs.
- Develop dashboards, maps, spatial analysis, and reusable insight products.
- Steward **Open Baltimore** and high-quality open data publication.
- Maintain the citywide **KPI dictionary** — one official definition per priority metric, with owner, formula, source, cadence, and caveats.
- Set data governance, classification, quality, and methodology standards (see the [Data Governance Framework](data-governance-framework.md)).
- Prepare Baltimore for **responsible AI** — use-case intake, risk tiering, human oversight, grounding, logging, and evaluation before anything scales.
- Supply the trustworthy data behind CitiStat, delivery activations, and public reporting.

## How the work fits together

The team builds in layers, and keeps them distinct:

- The **Baltimore City Data Platform** is the governed foundation — raw sources land, get cleaned, and become governed marts (the single source of truth).
- The **[Baltimore Intelligence Center](../../../what-we-do/programs/baltimore-intelligence-center/index.md)** is the program that builds the semantic layer, knowledge graph, and AI products *on top of* those governed marts. The integration contract is firm: the intelligence layer reads the governed marts and never re-ingests raw data.
- Products and portals, including StatGPT, City Services Intelligence, and the Performance Portal, consume that governed output, not the raw systems.

This is why the team insists on definitions, lineage, and ownership up front: everything downstream inherits them.

## What the team owns

- The Baltimore City Data Platform and shared data infrastructure — pipelines, reusable datasets, and APIs.
- Analytics and insight products, executive and Stat dashboards, and GIS.
- Open Data and Open Baltimore.
- Data governance, classification, quality standards, and the KPI dictionary.
- Responsible-AI readiness standards (with the Innovation Lab on applied pilots).

## What the team does not own

- Agency systems of record, and agency day-to-day operations.
- Enterprise infrastructure, identity, security, and production environments — **BCIT** owns those.
- Performance routines themselves — the **Performance** team.
- Service redesign and product builds where the primary need is workflow or user experience — the **Innovation Lab** (with Data as a partner).

The team partners closely on all of these; it does not replace the agency, BCIT, Performance, or Innovation roles.

## Governance: OPI owns meaning, and enforces it at the gate

Every data element carries a sensitivity tier (**Public, Protected, Confidential, or Restricted**) aligned to the State of Maryland's four-tier scheme. The tier drives who can see the data, how it is encrypted, and whether an AI product may surface it. Access defaults to deny; a governance gate refuses to serve any field or metric that has not cleared governance, regardless of what sits in the warehouse. The full model — classification, stewardship, quality, privacy, and AI accountability — is in the [Data Governance Framework](data-governance-framework.md).

## How the team partners across OPI

Data and Analytics is the evidence layer for the whole office. It gives **Performance** the KPI definitions, dashboards, and data-quality notes behind every Stat; gives the **Innovation Lab** the data, APIs, and AI-evaluation support behind its products; gives **Cross-Agency Delivery** the shared data models and milestone instrumentation that show whether implementation is working; and gives **AdminOps** the publishing cadence and QA behind public-facing data products.

## What success looks like

- Priority datasets have owners, definitions, refresh schedules, and quality standards.
- Stat decks and executive briefings use the same numbers.
- Open Baltimore is current, complete, and useful.
- Agencies reuse shared data products instead of rebuilding the same extract.
- AI use cases carry evaluation, human oversight, and sunset criteria before they scale.
- Residents, Council, researchers, and journalists can verify what the City reports.

## See also

- [Baltimore City Data Platform](../../../what-we-do/products/baltimore-city-data-platform.md) — the governed data foundation this team builds.
- [Baltimore Intelligence Center](../../../what-we-do/programs/baltimore-intelligence-center/index.md) — the program building the semantic layer and AI products on top.
- [Data Governance Framework](data-governance-framework.md) — classification, stewardship, quality, privacy, and AI accountability.
