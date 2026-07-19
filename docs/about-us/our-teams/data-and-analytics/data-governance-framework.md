# Data Governance Framework

{{ page_header(summary="The framework OPI uses to govern city data assets.", category="STRATEGY FRAMEWORK", tagline="A framework for trustworthy data, responsible use, open data, privacy, sharing, and AI readiness.") }}

## Executive Summary

**Clear governance enables responsible speed**

Baltimore City needs a comprehensive data governance framework that treats data as civic infrastructure. The framework should make data easier to use, easier to share responsibly, easier to publish, easier to protect, and easier to trust. It should support internal decision-making, performance management, open data, inter-agency collaboration, external partnerships, and responsible AI adoption.

This document is written as a strategy framework that could evolve into legislation, executive order, administrative policy, or agency guidance. It does not begin from the assumption that governance should slow the City down. It begins from the opposite premise: clear governance enables responsible speed.

Good stewardship is the foundation for every modern data and AI capability. Without shared definitions, quality standards, access rules, privacy protections, data inventories, and ownership models, the City cannot responsibly scale analytics, open data, dashboards, AI pilots, or cross-agency decision support.

## Purpose and Scope

**A citywide approach across the data lifecycle**

The purpose of the framework is to establish a citywide approach for managing data across its lifecycle: creation, collection, access, sharing, use, publication, retention, and disposal. It applies to data created or maintained by City agencies, data created by contractors on behalf of the City, data shared between agencies, data published to the public, and data used in analytics or AI-enabled tools.

The framework should strengthen transparency without compromising privacy, improve data sharing without weakening security, support innovation without enabling shadow systems, and ensure AI readiness without allowing ungoverned automation.

## Guiding Principles

**How the framework should behave**

**1. Data is a City asset.**

Data created or maintained by City agencies should be managed as a shared public asset, not as isolated departmental property.

**2. Open where possible, protected where necessary.**

The City should proactively publish and share data unless privacy, security, legal, or safety considerations require limits.

**3. Stewardship enables use.**

Governance exists to make data reliable and usable at scale, not to create unnecessary gatekeeping.

**4. Residents deserve privacy and transparency.**

The City must clearly protect sensitive information while explaining how data is used to make decisions.

**5. One definition per metric.**

Priority KPIs and shared data elements should have a single official definition, an owner, and documented methodology.

**6. Human judgment remains accountable.**

AI and advanced analytics should support public servants, not obscure responsibility for decisions.

**7. Reuse over rebuild.**

Shared datasets, reusable pipelines, and common standards should reduce duplicate work across agencies.

**8. Be readable from the outside.**

Data sources, owners, definitions, caveats, and approved uses should be understandable to oversight bodies and the public where appropriate.

## Governance Structure and Roles

**Authority that already matters in practice**

The framework should formalize roles that already matter in practice and give them consistent authority. The Chief Data Officer should own citywide data strategy, open data stewardship, governance standards, and major data-sharing decisions. The Deputy Chief Data Officer and Data and Analytics leadership should operate the governance practice day to day.

| **Role**                                    | **Core responsibility**                                                                                               |
|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| Chief Data Officer                          | Owns citywide data strategy; resolves major questions of data sharing, publication, risk, and governance scope.       |
| Data Governance Council                     | Cross-agency forum for standards, shared definitions, data quality, access issues, and stewardship decisions.         |
| Open Data Council                           | Prioritizes open data publication, public feedback, dataset quality, and Open Baltimore roadmap decisions.            |
| Agency Data-Driven Officers / Data Stewards | Own agency-side data quality, definitions, refresh cadence, and coordination with OPI.                                |
| BCIT                                        | Owns enterprise infrastructure, security, identity, production environments, and technology architecture partnership. |
| Law / Privacy / Security partners           | Advise on legal risk, privacy, sensitive data, records retention, security, and public release.                       |
| Executive Sponsors                          | Resolve cross-agency barriers and authorize major policy or operational shifts.                                       |

## Enterprise Data Inventory and Classification

**Knowing what we have and how it can be used**

The City should maintain an enterprise data inventory that identifies major datasets held by agencies and contractors. Each inventory entry should include dataset name, description, owning agency, data steward, system of record, refresh cadence, sensitivity level, publication status, known quality issues, and related KPIs or public products.

Every dataset carries one of four sensitivity tiers, aligned to the State of Maryland's four-tier scheme. The tier governs how the data may be accessed, shared, published, or used in AI:

| Tier | What it covers |
| --- | --- |
| **Public** | Approved for publication and reuse; no harm from disclosure. |
| **Protected** | City operational use; controlled access; not for automatic public release. |
| **Confidential** | Could harm individuals or the City if disclosed — most PII and precise geolocation; access is named and justified. |
| **Restricted** | Governed by law, contract, or investigation; disclosure carries regulatory or criminal exposure; individually authorized. |

Using any tier's data in AI — for model training or AI-enabled output — requires additional review first, regardless of tier. Classification is not permanent: data may become publishable after aggregation, redaction, or de-identification, or need tighter controls as risks become clearer, so the inventory is reviewed regularly.

## Data Quality, Metadata, and Methodology

**Quality is a governance requirement**

Data quality is not a technical nicety. It is a governance requirement. Every priority dataset should have a documented owner, refresh cadence, quality checks, and known caveats. Every public or executive-facing metric should have a methodology card that explains the definition, formula, source, exclusions, limitations, and update schedule.

For priority KPIs, the City should maintain a KPI dictionary. The dictionary should prevent competing definitions and ensure the same metric means the same thing in CitiStat, budget documents, dashboards, open data, and public reports. Where data is incomplete or unreliable, products should name the limitation rather than hide it.

The City should also identify authoritative sources for commonly used reference data such as addresses, neighborhoods, agency names, service request types, permit statuses, facilities, fleet assets, and employee or position identifiers where appropriate. This reduces confusion across systems and supports better integration.

## Inter-agency Data Sharing

**A presumption of responsible sharing**

Baltimore should adopt a presumption of responsible internal sharing. Agencies should be able to share data with one another for legitimate City operations, policymaking, service delivery, performance management, and public accountability unless a legal, privacy, security, or contractual restriction prevents it.

This does not mean unmanaged access. It means a clear path. The City should maintain standard data-sharing agreements, access request processes, and escalation routes for disputes. The Data Governance Council should help resolve definition conflicts, access questions, and quality disputes. Sensitive data should be shared only with documented purpose, approved users, retention expectations, and security controls.

## Open Data and Public Transparency

**Public accountability infrastructure**

Open Baltimore should be treated as public accountability infrastructure. The City should proactively publish high-value datasets that are current, documented, machine-readable, and usable. High-value datasets should be prioritized based on public interest, service impact, Council oversight needs, research value, and alignment to mayoral and agency priorities.

Every high-value open dataset should include metadata, a data dictionary or methodology card where appropriate, update frequency, responsible steward, caveats, and a feedback path. Publication should not be treated as the end of the work. Open data requires maintenance, user support, and continuous improvement.

The City should also publish a public open data roadmap that identifies planned dataset releases, improvements, and refresh priorities. This helps residents, journalists, researchers, and civic technologists understand what is coming and hold the City accountable for follow-through.

## Privacy, Security, and Responsible Access

**Transparency balanced with protection**

Transparency must be balanced with privacy and security. The City should clearly define sensitive and protected information, require privacy review for high-risk projects, and ensure that access to sensitive data is role-based, logged, and limited to a legitimate public purpose.

Privacy impact assessments should be required for new systems, data-sharing arrangements, public releases, or analytics projects that involve sensitive personal information or could materially affect residents. The review should ask what data is collected, why it is needed, who can access it, how long it is retained, whether it can be minimized, and how residents are protected from misuse.

Contracts with vendors should require data protection terms, breach notification, limits on secondary use, return or deletion of City data at the end of the engagement, and compliance with City governance standards. Data created by contractors on behalf of the City should be treated as City data unless a specific legal agreement says otherwise.

## AI and Algorithmic Accountability

**Governance scales to algorithms**

AI readiness should be governed through the same stewardship principles that govern data. The City should maintain an intake and review process for AI and algorithmic use cases. Each proposed use case should identify the problem, users, data sources, risk tier, decision impact, human oversight, evaluation method, logging approach, and sunset criteria.

No production AI use case should operate without:

- A named business owner and technical owner.

- Approved data sources and sensitivity review.

- A clear statement of where human judgment remains responsible.

- Testing for accuracy, usefulness, bias, and failure modes.

- Documentation of limitations and appropriate use.

- Monitoring, incident response, and a decision point for scale, redesign, or retirement.

For higher-risk algorithmic systems, the City should consider a public registry or plain-language disclosure describing the purpose of the system, the data used, the decision supported, and the oversight mechanism. The goal is not to freeze innovation. The goal is to ensure innovation remains explainable, fair, and accountable.

## External Data Partnerships

**Capacity expansion through clear agreements**

The City should support responsible partnerships with universities, nonprofits, philanthropy, civic technologists, other governments, and private vendors. These partnerships can expand capacity and insight, but they must operate through clear data-use agreements.

Any external sharing of non-public data should document the purpose, dataset, permitted use, security requirements, retention period, publication restrictions, and responsibilities of the receiving party. When external partners produce data products, analyses, or models on behalf of the City, the City should retain sufficient rights, documentation, and access to sustain the work.

## Implementation Roadmap

**Phased adoption over 18+ months**

| **Phase**                 | **Timeframe** | **Priority actions**                                                                                                                                                     |
|---------------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Phase 1: Organize         | 0–6 months    | Confirm governance roles; launch Data Governance Council; define classification model; inventory priority datasets; publish standard templates.                          |
| Phase 2: Standardize      | 6–12 months   | Build KPI dictionary; publish methodology card template; stand up open data roadmap; adopt data-sharing agreement templates; begin AI use case review process.           |
| Phase 3: Operationalize   | 12–18 months  | Apply quality rules to priority datasets; resolve definition conflicts; expand open data publication; implement privacy review for high-risk projects; track compliance. |
| Phase 4: Institutionalize | 18+ months    | Convert framework into executive order, legislation, or administrative rules where appropriate; publish annual governance report; continue annual policy refresh.        |

## Pathway to Legislation or Executive Order

**A staged approach**

This strategy can evolve into formal authority through a staged approach. First, OPI can issue administrative standards and templates under the Chief Data Officer’s role. Second, the City Administrator or Mayor can issue an executive directive establishing governance routines, agency responsibilities, and AI review expectations. Third, City Council can codify core responsibilities such as the data inventory, open data roadmap, annual report, agency data stewards, and governance councils.

The framework should survive leadership transitions. Strong data governance should not depend on one person, one platform, or one initiative. It should become part of how Baltimore City operates.

## Closing

Comprehensive data governance is the operating foundation for trustworthy data, better decisions, public transparency, responsible AI, and durable service improvement. Baltimore can build a governance model that is practical, enabling, readable from the outside, and worthy of public trust.
