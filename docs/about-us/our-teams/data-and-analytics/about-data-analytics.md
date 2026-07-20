# About Data and Analytics

{{ page_header(summary="How OPI makes Baltimore's data trustworthy, governed, and useful, and builds the platform the city's analytics run on.", category="ABOUT · SERVICE") }}

The Data and Analytics team builds and runs Baltimore's civic data infrastructure. It takes the scattered administrative data that agencies collect and turns it into shared, governed assets: reliable measures, reusable datasets, dashboards, maps, open data, and the platform the city's analytics and AI products run on. The work sits where agency operations, executive priorities, public transparency, and BCIT's infrastructure meet.

The team owns the meaning of the city's data: what a metric is, who owns it, how sensitive it is, and how it may be used. That idea runs through everything below.

## What the team does

The team builds and runs the [Baltimore City Data Platform](../../../what-we-do/products/baltimore-city-data-platform.md), the governed foundation that holds the city's ingestion pipelines, a medallion warehouse, shared datasets, and APIs. On top of that platform it develops dashboards, maps, spatial analysis, and reusable insight products, and it stewards Open Baltimore and the rest of the city's open data.

It maintains the citywide KPI dictionary, which gives each priority metric one official definition with an owner, formula, source, refresh cadence, and caveats. It sets the standards for data governance, classification, quality, and methodology (see the [Data Governance Framework](data-governance-framework.md)). And it prepares Baltimore for responsible AI, running use-case intake, risk tiering, human oversight, grounding, logging, and evaluation before anything scales. All of this supplies the reliable data behind CitiStat, delivery work, and public reporting.

## How the work fits together

The team builds in layers and keeps them distinct. The [Baltimore City Data Platform](../../../what-we-do/products/baltimore-city-data-platform.md) is the governed foundation, where raw sources land, get cleaned, and become governed marts that serve as the official record. The [Baltimore Intelligence Center](../../../what-we-do/programs/baltimore-intelligence-center/index.md) is the program that builds the semantic layer, knowledge graph, and AI products on top of those governed marts; by firm agreement, the intelligence layer reads the governed marts and never re-ingests raw data. Products and portals, including StatGPT, City Services Intelligence, and the Performance Portal, draw on that governed output rather than the raw systems.

The team insists on definitions, lineage, and ownership up front because everything downstream inherits them.

## What the team owns

The team owns the Baltimore City Data Platform and the shared data infrastructure around it: pipelines, reusable datasets, and APIs. It owns the analytics and insight products, the executive and Stat dashboards, and GIS. It owns Open Data and Open Baltimore, along with the data governance, classification, quality standards, and KPI dictionary that keep all of it reliable. And it owns the city's responsible-AI readiness standards, working with the Innovation Lab on applied pilots.

## What the team does not own

The team does not own agency systems of record or agencies' day-to-day operations. Enterprise infrastructure, identity, security, and production environments belong to BCIT. The performance routines themselves belong to the Performance team. Service redesign and product builds, where the main need is workflow or user experience, belong to the Innovation Lab, with Data as a partner.

The team works closely on all of these. It does not replace the agency, BCIT, Performance, or Innovation roles.

## Governance: OPI owns meaning and enforces it at the gate

Every data element carries a sensitivity tier (Public, Protected, Confidential, or Restricted) aligned to the State of Maryland's four-tier scheme. The tier drives who can see the data, how it is encrypted, and whether an AI product may show it. Access defaults to deny. A governance gate refuses to serve any field or metric that has not cleared governance, no matter what sits in the warehouse. The full model covers classification, stewardship, quality, privacy, and AI accountability, and it lives in the [Data Governance Framework](data-governance-framework.md).

## How the team partners across OPI

Data and Analytics is the evidence layer for the whole office. It gives Performance the KPI definitions, dashboards, and data-quality notes behind every Stat. It gives the Innovation Lab the data, APIs, and AI-evaluation support behind its products. It gives Cross-Agency Delivery the shared data models and milestone instrumentation that show whether implementation is working. And it gives AdminOps the publishing cadence and QA behind public-facing data products.

## What success looks like

- Priority datasets have owners, definitions, refresh schedules, and quality standards.
- Stat decks and executive briefings use the same numbers.
- Open Baltimore is current, complete, and useful.
- Agencies reuse shared data products instead of rebuilding the same extract.
- AI use cases carry evaluation, human oversight, and sunset criteria before they scale.
- Residents, Council, researchers, and journalists can verify what the City reports.

## Read alongside

- [Baltimore City Data Platform](../../../what-we-do/products/baltimore-city-data-platform.md): the governed data foundation this team builds.
- [Baltimore Intelligence Center](../../../what-we-do/programs/baltimore-intelligence-center/index.md): the program building the semantic layer and AI products on top.
- [Data Governance Framework](data-governance-framework.md): classification, stewardship, quality, privacy, and AI accountability.
- [On Trustworthy Data](../../letters-from-the-director/on-trustworthy-data.md): the Director's letter on why this work matters.
