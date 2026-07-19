# Baltimore City Data Platform

> The governed data foundation that Baltimore's analytics and AI products run on.

## What it is

The Baltimore City Data Platform is the shared, governed data foundation the [Data and Analytics team](../../about-us/our-teams/data-and-analytics/index.md) builds and operates. It ingests data from city source systems, cleans and governs it, and turns it into trustworthy data that dashboards, open data, applications, and the [Baltimore Intelligence Center](../programs/baltimore-intelligence-center/index.md)'s AI products all read from.

The design principle is extend, don't rebuild. OPI keeps maturing this platform, and new intelligence and AI layers are built on top of its governed outputs rather than re-ingesting raw data.

## How it works

Data moves through the platform in governed stages:

| Stage | What happens | Tools |
| --- | --- | --- |
| Ingest | Source data is pulled on a schedule and orchestrated | Dagster, dlt |
| Land (bronze) | Raw data lands as Parquet, minimized to the fields a use case needs | Azure Blob |
| Model and govern (silver → gold) | dbt transforms raw data into conformed, tested tables; the gold layer holds the governed marts, the official record for analytics | dbt, PostgreSQL |
| Serve | Dashboards, open data, and the Baltimore Intelligence Center read the governed marts through role-based access | PostgreSQL, APIs |

Supporting this are GitHub and GitHub Actions (source control and CI/CD), Terraform (infrastructure as code), Microsoft Entra ID (identity and role-based access), and Azure Key Vault (secrets). Governance runs through **OpenMetadata** (catalog and lineage), **dbt tests** (data quality), and role-based access on the warehouse.

## Governance built in

Every data element carries a sensitivity tier (Public, Protected, Confidential, or Restricted), and every priority metric maps to one official definition in the citywide KPI dictionary. Personal data is kept only where a use case needs it and is protected by tier and role-based access. Access defaults to deny, and a governance gate refuses to serve data that has not cleared governance. The full model is in the [Data Governance Framework](../../about-us/our-teams/data-and-analytics/data-governance-framework.md).

## Read alongside

- [Data and Analytics team](../../about-us/our-teams/data-and-analytics/index.md): the team that builds and operates the platform.
- [Baltimore Intelligence Center](../programs/baltimore-intelligence-center/index.md): the program building the semantic layer and AI products on top.
- [Data Governance Framework](../../about-us/our-teams/data-and-analytics/data-governance-framework.md): classification, quality, privacy, and AI accountability.
