# Baltimore Intelligence Center Engagement Guide

{{ page_badge() }}

> How the Innovation Lab engages with the Baltimore Intelligence Center.

**BALTIMORE INTELLIGENCE CENTER**

**The citywide data, intelligence, and AI program  
Engagement Guide**

**Mayor’s Office of Performance and Innovation**

Baltimore City

| *A 12-month vendor-led build, followed by a 6-month city-led continuation. By the end of month 12, Baltimore should have a trusted data platform, a working semantic layer, two live decision-support products, and the operating discipline to keep building responsibly without the vendor in the room.* |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

**FRONT MATTER**

# **How to read this document**

This is the single guiding document for the Baltimore Intelligence Center engagement — the citywide data, intelligence, and AI program that the Mayor’s Office of Performance and Innovation is standing up in partnership with Sand Technologies. It consolidates the four scoping artifacts (the policymaker brief, the long-form scope, the pre-kickoff briefing, and the AI readiness materials) into one operating reference for everyone working on, partnering with, or funding the engagement.

It is organized to be read three ways. Executives can read sections one through four to understand vision, structure, and sequencing. Delivery teams can use sections five through ten as a working playbook. Partners and funders can read sections eleven and twelve plus the appendices for governance, risks, and open issues.

### **What this document is**

- A single source of truth for engagement scope, sequencing, decision rights, and target state.

- A working playbook for the Baltimore Intelligence Center squad and Sand delivery teams.

- A governance anchor that defines how use cases are reviewed, approved, measured, and retired.

- A briefing artifact for executives, agency partners, philanthropy, and audit/oversight audiences.

### **What this document is not**

- It is not a contract. The Sand statement of work governs commercial terms.

- It is not a substitute for individual workstream plans. Each workstream produces its own detailed plan during month one.

- It is not an awards nomination. The discipline modeled here positions Baltimore for awards, philanthropy, and replication — but the goal is operating maturity, not prizes.

### **How decisions get made in this document**

Where the source documents had open placeholders, this guide locks them down. Any further changes to the engagement scope, sequencing, or decision rights are tracked in the open issues section (Section 12) and resolved by the Executive Sponsor in consultation with the Project Lead and Sand TPM.

**SECTION 1**

# **Executive context and engagement vision**

### **The problem we are solving**

Baltimore City has the demand and the talent for data-driven government, but not the infrastructure. Every time an agency asks OPI for help — on 311 backlogs, permit performance, public safety, vacants, capital projects — the team first has to orient to the data, clean it, and reconcile it before any analysis can begin. Three things follow. Cycle times are long. Insights are inconsistent. And AI cannot be adopted responsibly because the underlying data is neither governed nor trusted.

OPI is also being asked to lead the city’s response to artificial intelligence. That work cannot succeed on top of fragmented data, undefined KPIs, and informal governance. A trusted data foundation, a semantic layer that encodes how the city actually thinks, and a small set of grounded intelligence products are the prerequisites for everything else.

### **What the engagement does about it**

This engagement establishes the Baltimore Intelligence Center — a citywide data and AI capability that lives operationally inside OPI and serves the whole city. Sand Technologies is the implementation partner for the first 12 months. OPI staff carry the program forward in months 13 to 18 and beyond.

The work is organized around five workstreams that build on each other. A governed data platform comes first, because nothing else works without it. A semantic layer encodes city KPIs and domain logic. Two flagship intelligence products — City Services Intelligence and a CitiStat-aligned StatGPT pilot — prove the platform in real workflows. A small set of internal operating tools makes OPI itself more disciplined. And a design system, adoption practice, and capability-transfer plan ensure the work survives and scales after the vendor leaves.

### **Engagement vision**

| *By end of month 12, Baltimore should have: a governed data platform with an initial set of canonical sources; a semantic layer covering at least two priority domains; City Services Intelligence in disciplined pilot with named users; a StatGPT pilot running with the CitiStat team; an OPI Internal Intelligence assistant in daily use; lightweight but real AI governance covering intake, risk tiering, human-in-the-loop, logging, and post-launch monitoring; and an OPI team that can sustain and extend the work without daily vendor support.* |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

### **Three things that have to be true at month 12**

- The platform is real. Canonical sources are ingested on a schedule, data quality rules are running, lineage is visible, and the catalog is populated.

- The products are used. At least two grounded intelligence products are in regular use by named OPI staff and at least one agency partner; usage, quality, and decision-impact are measured monthly.

- The capability is ours. OPI staff can ship a new ingest, a new semantic-layer change, or a new use case end-to-end — with Sand on call rather than in the chair.

### **Why now**

Three windows are open at the same time, and they will not stay open indefinitely. First, the city has a Mayor and City Administrator who will use disciplined intelligence if the team can produce it. Second, the philanthropic environment for data and AI in cities is at a high-water mark. Third, the AI procurement landscape is still soft enough that a city-owned, governed approach can win against off-the-shelf vendor products before lock-in occurs. Doing this in 2026 is materially easier than doing it in 2028.

**SECTION 2**

# **The Baltimore Intelligence Center**

### **Why a named squad**

The work cuts across OPI’s Innovation Lab, Data and Analytics team, and Performance and CitiStat team — plus Sand and agency partners. A named squad with a clear roster, a single backlog, and a defined operating cadence is the only way to keep delivery coherent across that many seams. The Baltimore Intelligence Center (BIC) is that squad.

### **Where the BIC sits**

Operationally, the BIC runs out of OPI’s Innovation Lab — the home for product delivery and applied technology inside the office. Technically, its center of gravity is the Data and Analytics team, which provides the platform, governance, and engineering muscle. CitiStat is the lead agency-partner anchor for the first wave of intelligence products. The Executive Director and CDO holds executive sponsorship and, in the interim, project lead until the Innovation Program Manager seat is funded and filled.

### **Squad roster**

| **Role on the BIC**                        | **Name**                  | **Position**                                   | **Home team**                  |
|--------------------------------------------|---------------------------|------------------------------------------------|--------------------------------|
| Executive Sponsor and interim Project Lead | Dartanion Swift-Williams  | Executive Director and Chief Data Officer, OPI | OPI — Director’s Office        |
| Product Manager                            | Chiemeka Okeoma           | Senior Product Engineer                        | OPI — Innovation Lab           |
| Project Manager                            | Mallory Screws            | Project Manager                                | OPI                            |
| Data Engineering Lead                      | Alejandro Zuniga Sosa     | Principal Data Engineer                        | OPI — Data and Analytics       |
| Platform Engineering Lead                  | Koby Samuel               | Principal Platform Engineer                    | OPI — Data and Analytics       |
| Data Science and Analytics                 | Selenea Gibson            | Applied Data Scientist                         | OPI — Data and Analytics       |
| Data Engineering                           | Briya Bhakta              | Senior Data Engineer                           | OPI — Data and Analytics       |
| Technical Program Management               | Roberto Herbruger         | Technical Program Manager                      | OPI — Data and Analytics       |
| Data Governance and Analytics              | Vera Choo                 | Data Governance and Analytics Manager          | OPI — Data and Analytics       |
| Deputy CDO and platform partnership        | Jason Howard, PhD         | Deputy Chief Data Officer                      | OPI — Data and Analytics       |
| Product Engineering                        | Xander Jake de los Santos | Product Engineer                               | OPI — Innovation Lab           |
| CitiStat — City Services lead              | Nelson Gomes Boronat      | CitiStat Analyst                               | OPI — Performance and CitiStat |
| CitiStat — City Services lead              | Ross Hackett              | CitiStat Analyst                               | OPI — Performance and CitiStat |
| CitiStat — Public Safety lead              | Derek Thomas              | CitiStat Analyst                               | OPI — Performance and CitiStat |

Sand Technologies provides the Technical Program Manager (TBD), engagement manager, principal architect, semantic-layer lead, product engineering, design lead, and capability-transfer lead across the 12 vendor months. The Sand TPM and OPI Project Manager partner daily; the Sand engagement manager and OPI Project Lead partner weekly.

### **Operating cadence**

- Daily — standup for active workstreams (15 minutes, async-first).

- Weekly — BIC leadership review (Project Lead + Sand engagement manager + workstream leads). Backlog grooming and risk review.

- Bi-weekly — product showcase and user feedback (open to OPI, agency partners, BCIT).

- Monthly — executive steering (Executive Sponsor, Sand engagement leadership, Deputy CDO, Innovation Lab lead, CitiStat lead). Decision log review and milestone reporting.

- Quarterly — portfolio review with BCIT, Law, Procurement, Finance, and agency sponsors. Risks, governance posture, use case approvals.

### **Decision rights at a glance**

| **Decision**                                 | **Owner**                                            | **Consulted / required to inform**                |
|----------------------------------------------|------------------------------------------------------|---------------------------------------------------|
| Engagement scope and sequencing changes      | Executive Sponsor                                    | Project Lead, Sand engagement manager, Deputy CDO |
| Use case approval and risk tiering           | Project Lead + Data Governance Manager               | Executive Sponsor, Law, BCIT security             |
| Architecture and platform decisions          | Platform Engineering Lead + Sand principal architect | Deputy CDO, BCIT                                  |
| Catalog, semantic-layer, and KPI definitions | Data Governance and Analytics Manager                | Sand semantic-layer lead, agency owners           |
| Product roadmap for an intelligence product  | Product Manager                                      | Project Lead, agency sponsor, design lead         |
| Procurement and vendor changes               | Executive Sponsor                                    | Procurement, Finance, Law                         |
| Public release of any data product           | Executive Sponsor + Data Governance Manager          | Communications, Law, agency sponsor               |

### **Capacity and the unfunded ask**

The funded Innovation Lab today is two engineers (Senior Product Engineer and Product Engineer). That is enough to start — with Sand carrying the heavy lift in months 0–6 — but it is not enough to absorb capability transfer in months 7–12 and run the program independently from month 13 onward. Closing at least the Innovation Program Manager seat by month 9 is the most material risk mitigation in this engagement.

**SECTION 3**

# **The five workstreams**

The engagement is organized into five workstreams. They build on each other: the platform comes first because nothing else works without it; the semantic layer translates the platform into city language; the products prove the platform in real workflows; the internal tools tighten OPI’s own operating discipline; and the design system, adoption practice, and capability-transfer plan make sure what gets built survives the vendor handoff.

### **Workstream 1 — Citywide Data Platform and Governance**

Stand up the governed Azure data environment that everything else runs on. Medallion architecture, ingest pipelines for the priority sources, data quality rules, lineage, an open-source data catalog, and an actual data governance policy.

### **Goals**

- Establish a medallion architecture (bronze/silver/gold) on Azure with PostgreSQL warehouse and Azure Blob Storage.

- Stand up containerized Python ingest jobs orchestrated through Azure DevOps or GitHub Actions.

- Ingest the wave-one priority sources (see Section 6) on a documented schedule with monitoring.

- Deploy OpenMetadata as the open-source, self-hosted catalog inside the City’s Azure tenant.

- Author and ratify a formal Data Governance Policy covering ownership, access, sensitivity, retention, and stewardship.

- Stand up a runbook library and operational support model for the platform.

### **Vendor month deliverables**

- Reference architecture and security review approved with BCIT.

- Wave-one ingest live for at least four priority sources by month 6.

- Data quality rules running on at least 311, Cityworks, and the Public Safety Incidents source.

- OpenMetadata deployed, populated, and integrated with at least two source systems.

- Data Governance Policy v1 drafted by month 3, ratified by month 5; v2 incorporating production lessons by month 11.

- Platform runbooks and operational handbook published; on-call rotation established.

| **OPI lead**                                                                                                                       | **Sand role**                                                                                                                                                                | **Key dependencies**                                                                                        |
|------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Koby Samuel (Platform Engineering Lead) and Alejandro Zuniga Sosa (Data Engineering Lead). Vera Choo owns governance ratification. | Principal Architect (lead), Data Engineering team, DevOps engineer, Governance Advisor. Sand drafts the Data Governance Policy as an M1 deliverable; Vera owns ratification. | BCIT security and network approvals; agency data-sharing agreements where required; Azure tenant readiness. |

### **Exit criteria — what “done” looks like at month 12**

- Wave-one priority sources are ingested on schedule with monitoring and quality rules.

- Data Governance Policy is ratified and in use; at least 10 datasets have named owners and stewards in the catalog.

- OPI staff can build, deploy, and monitor a new ingest pipeline without Sand in the chair.

### **Workstream 2 — Semantic Intelligence Layer**

Translate raw city data into the city’s actual decision-making language. Domain semantic layers, a KPI dictionary, an MCP-style server and tool layer, and an evaluation framework for AI outputs.

### **Goals**

- Build domain semantic layers covering, at minimum: city services, public safety, neighborhoods, and (later) permitting and housing.

- Maintain a citywide KPI dictionary that is the canonical definition for every metric used by an intelligence product.

- Stand up an MCP server / tool layer that exposes governed query patterns, KPI logic, and source mappings to the intelligence products.

- Establish an AI evaluation framework with grounded-answer rate, exception rate, and human-review thresholds.

### **Vendor month deliverables**

- KPI dictionary v1 covering city services and public safety domains by month 6.

- Semantic layer for city services live and powering City Services Intelligence by month 6.

- MCP server and tool layer in production for the city services domain by month 6; expanded to public safety and neighborhoods by month 12.

- AI evaluation framework documented and running on the lead intelligence product by month 9.

| **OPI lead**                                                                                                                                                                       | **Sand role**                                                                                                                       | **Key dependencies**                                                                                                                             |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Vera Choo (Data Governance and Analytics Manager) for KPI dictionary and definitions; Alejandro Zuniga Sosa for technical implementation; Selenea Gibson for evaluation framework. | Semantic Layer Lead (lead), AI/ML Engineer, Domain Modeling support. Sand drives implementation; OPI owns the meaning of every KPI. | Workstream 1 platform readiness; agency partner availability to validate KPI definitions; CitiStat’s existing measure library as starting input. |

### **Exit criteria — what “done” looks like at month 12**

- Every metric used by an intelligence product is defined once in the KPI dictionary; no parallel definitions.

- Every AI response in production is grounded through the MCP/tool layer — no freeform model-only answers.

- Evaluation framework produces a monthly quality report reviewed by the BIC leadership and Executive Sponsor.

### **Workstream 3 — Intelligence Products**

Two flagship intelligence products in months 0–6 — City Services Intelligence (lead pilot) and a CitiStat StatGPT pilot in parallel. OPI Internal Intelligence and additional products (GenBI, Neighborhoods Map, Neighborhoods Explorer with Chat) follow in months 7–12.

### **Goals**

- Launch City Services Intelligence as the lead pilot — grounded decision-support for 311, Cityworks, public safety incidents, crash, vacants, and neighborhood data.

- Launch a StatGPT pilot in parallel with CitiStat (City Services and Public Safety leads) using the same semantic layer and governance.

- Launch OPI Internal Intelligence in months 7–9 to support the team’s own knowledge management and operating discipline.

- Plan and scope GenBI, Neighborhoods Map, and Neighborhoods Explorer with Chat for months 10–18.

### **Vendor month deliverables**

- City Services Intelligence in disciplined pilot by month 6 with named users and weekly usage measurement.

- StatGPT pilot running for City Services and Public Safety Stat preparation by month 6, with measured time-to-prep reduction.

- OPI Internal Intelligence live for OPI staff by month 9.

- Use case briefs, baseline metrics, and monthly scorecards published for each product.

| **OPI lead**                                                                                                                                                                                                                   | **Sand role**                                                                                                                 | **Key dependencies**                                                                                                                             |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Chiemeka Okeoma (Product Manager) for City Services Intelligence and OPI Internal Intelligence. Nelson Gomes Boronat and Ross Hackett (CitiStat) for StatGPT City Services. Derek Thomas (CitiStat) for StatGPT Public Safety. | Product Engineering (lead), AI/ML Engineer, Design Lead, UX Researcher. Sand co-builds; OPI Product Manager owns the roadmap. | Workstream 2 semantic layer readiness; agency partner availability for user research; AI governance approval (use case intake and risk tiering). |

### **Exit criteria — what “done” looks like at month 12**

- City Services Intelligence and StatGPT pilot have at least 10 weekly active users each by month 12, with measured decision-impact.

- Each product has a monthly scorecard reviewed by BIC leadership: usage, grounded-answer rate, exception rate, user-reported usefulness, decisions supported.

- OPI Product Manager and Product Engineering team can ship a new feature or new use case without Sand in the chair.

### **Workstream 4 — OPI Internal Operating Tools**

A small set of internal tools that make OPI itself more disciplined: a SharePoint Governance Scanner, a Project Status Reporting Tool, and a Portfolio Reporting Pack.

### **Goals**

- Build the SharePoint Governance Scanner to surface document hygiene, access risk, and information-architecture drift.

- Build the Project Status Reporting Tool to standardize status, risks, and decisions across OPI projects.

- Build the Portfolio Reporting Pack to roll up OPI delivery for the Executive Director, the Mayor, and philanthropic funders.

### **Vendor month deliverables**

- SharePoint Governance Scanner deployed for OPI by month 9.

- Project Status Reporting Tool in use across OPI by month 10.

- Portfolio Reporting Pack producing a monthly executive view by month 12.

| **OPI lead**                                                     | **Sand role**                                                                                                    | **Key dependencies**                                                                                            |
|------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Chiemeka Okeoma (Product Manager) and Mallory (Project Manager). | Product Engineering supports; Sand provides templates and reference implementations from prior city engagements. | OPI SharePoint operating system strategy already in place; existing OPI charter and intake templates as inputs. |

### **Exit criteria — what “done” looks like at month 12**

- OPI runs its weekly portfolio review off the Status Tool, not off email and slides.

- SharePoint Scanner has identified and remediated at least three meaningful governance issues.

- Portfolio Pack is the executive’s default monthly read.

### **Workstream 5 — Design System, Adoption, and Capability Transfer**

The work that decides whether the platform and products survive after Sand leaves. A shared design system, an adoption playbook, and a structured capability-transfer plan from Sand to OPI staff.

### **Goals**

- Build a shared design system for OPI intelligence products with brand-aligned components and accessibility built in.

- Stand up an adoption playbook covering training, office hours, documentation, and feedback loops for each product.

- Run a structured capability-transfer program from Sand to OPI staff across all four other workstreams.

### **Vendor month deliverables**

- Design system v1 in use across both flagship products by month 6; v2 by month 12.

- Adoption playbook live for City Services Intelligence and StatGPT pilot by month 7.

- Capability-transfer scorecard tracked monthly; OPI staff own at least 70% of operational tasks by month 12.

| **OPI lead**                                                                                                                              | **Sand role**                                                                                                              | **Key dependencies**                                                                                                                            |
|-------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| Chiemeka Okeoma (PM) and a designated Civic Design and UX Lead (currently unfunded — see capacity note). Adoption: Vera Choo and Mallory. | Design Lead, Capability Transfer Lead, Adoption Lead. Sand pairs and trains; OPI staff own day-to-day delivery by month 9. | Innovation Program Manager and Civic Design and UX Lead funding decisions; OPI Performance Standards and onboarding artifacts already in place. |

### **Exit criteria — what “done” looks like at month 12**

- OPI staff are the daily operators for the platform, the catalog, the semantic layer, and the two flagship products.

- Sand transitions to an advisory and on-call posture by month 12.

- A documented continuation plan exists for months 13–18 (city-led) and beyond.

**SECTION 4**

# **Operating model**

### **Two homes, one squad**

The Baltimore Intelligence Center has two organizational homes that have to work as one. The Innovation Lab is the home for product delivery, design, and applied technology. The Data and Analytics team is the home for the platform, the catalog, the semantic layer, and engineering. Performance and CitiStat is the lead agency-partner anchor for intelligence products in their first year. The BIC squad model resolves the seams.

### **How work flows**

- Demand intake — every new use case enters through a single intake process owned by the Project Lead and the Data Governance and Analytics Manager. No side channels.

- Risk and governance review — each use case is risk-tiered (low/medium/high) and routed through the appropriate review path. Law, BCIT security, and Procurement are involved as needed.

- Discovery — the Product Manager and lead workstream owners scope the use case, identify required data, and confirm semantic-layer needs.

- Build — the BIC squad delivers in two-week iterations with a defined backlog and demo cadence.

- Pilot — each product runs a structured pilot with named users, baseline metrics, and weekly feedback loops.

- Operate — once a product graduates from pilot, it is governed by a monthly scorecard, an incident path, and a retirement clause if it stops earning its keep.

### **How OPI and Sand actually share the work**

The vendor-led / city-led split is real, not ceremonial. Sand carries the heavy lift in months 0–6. OPI staff pair, learn, and gradually take operational ownership. By month 9, OPI staff are leading day-to-day delivery with Sand on call. By month 12, Sand is in an advisory posture and the city carries the program.

### **Tooling baseline**

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
| Identity, access, and audit |                                                                                |

**SECTION 5**

# **12-month roadmap, plus city-led continuation**

Twelve vendor months, then six city-led months. The vendor-led period is structured around two milestones — Foundation (M1, months 0–6) and Launch (M2, months 7–12). The city-led continuation is the third milestone (M3, months 13–18): an Expansion phase that proves the program runs without daily vendor support.

### **M1 — Foundation (months 0–6)**

- Stand up the governed Azure platform: medallion architecture, ingest framework, monitoring, security review with BCIT.

- Ingest wave-one priority sources (see Section 6).

- Deploy OpenMetadata; populate with wave-one sources; assign data owners and stewards.

- Draft and ratify Data Governance Policy v1 (Sand drafts, Vera owns ratification).

- Build the city services semantic layer; publish KPI dictionary v1.

- Launch City Services Intelligence in disciplined pilot with named users.

- Launch StatGPT pilot with CitiStat City Services and Public Safety leads.

- Stand up design system v1; adoption playbook for the two flagship products.

- Establish AI use case intake, risk tiering, and approval process.

### **M2 — Launch (months 7–12)**

- Ingest wave-two priority sources.

- Expand semantic layer to public safety and neighborhoods.

- Launch OPI Internal Intelligence in months 7–9.

- Stand up the SharePoint Governance Scanner and Project Status Reporting Tool.

- Run AI evaluation framework on flagship products; publish monthly quality report.

- Begin structured capability transfer in earnest — OPI staff take operational ownership of platform and one flagship product.

- Decide BI/GenBI tool selection.

- Ratify Data Governance Policy v2 with production lessons folded in.

### **M3 — City-led Expansion (months 13–18, post-vendor)**

- OPI runs the platform, the catalog, the semantic layer, and the flagship products independently.

- Replicate the City Services Intelligence pattern in a second domain (permitting, housing, or vacants).

- Stand up GenBI, Neighborhoods Map, and Neighborhoods Explorer with Chat.

- Sand on call for advisory and architecture review only.

- Publish a public-facing case study and an internal continuation plan for years two and three.

### **Phase gate criteria**

| **Gate** | **When**        | **Must be true to advance**                                                                                                                                                                                                                               |
|----------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| M1 → M2  | End of month 6  | Platform stable for wave-one sources; Data Governance Policy ratified; KPI dictionary v1 published; City Services Intelligence and StatGPT in disciplined pilot with measured baseline; design system v1 in use; AI use case intake operating.            |
| M2 → M3  | End of month 12 | OPI staff lead daily operations across platform, catalog, semantic layer, and at least one flagship product; AI evaluation framework producing monthly reports; OPI Internal Intelligence in daily use; capability-transfer scorecard at or above target. |
| M3 close | End of month 18 | A second domain has been added without vendor in the chair; continuation plan and budget approved; public case study published; program is sustainable on city staff plus on-call advisory.                                                               |

**SECTION 6**

# **Source-system priorities**

Source-system sequencing is the single biggest determinant of whether the engagement delivers in 12 months. The order below is locked. Wave one feeds City Services Intelligence and the StatGPT pilot. Wave two opens up permitting, capital, fleet, and facilities. Axon is explicitly excluded from direct ingestion — BPD will set up its own interfaces, and the engagement integrates through what BPD provides.

### **Wave one — months 0–6**

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

### **Wave two — months 7–12**

| **Source**                     | **System / interface**            | **Primary product use**                   |
|--------------------------------|-----------------------------------|-------------------------------------------|
| Accela                         | SQL Server direct                 | Permitting domain                         |
| ProjectDox (permit documents)  | SQL Server direct                 | Permitting domain                         |
| Capital Projects               | Existing system / interface (TBD) | Capital Stat support; portfolio analytics |
| Citywide Fleet (Faster)        | Direct (TBD)                      | Fleet operations; cross-domain analytics  |
| Citywide Facilities (Archibus) | Direct (TBD)                      | Facilities operations                     |
| AVL (Navman)                   | Vendor API / extract              | Operations and routing analytics          |

### **Explicit exclusion — Axon**

The engagement will not connect directly to Axon. Baltimore Police Department will set up its own interfaces and provide the data. The engagement’s scope is to integrate through whatever interfaces BPD stands up, not to negotiate or build a direct Axon connection. This is locked in to avoid a recurring source of slippage in prior data initiatives.

### **Wave three — city-led, months 13–18**

Wave three is determined by city-led work in M3 and reflects the second-domain expansion (permitting, housing, or vacants), plus any additional sources required to support GenBI, the Neighborhoods Map, and the Neighborhoods Explorer with Chat. Sand provides advisory input only; OPI staff lead.

### **Source-system readiness checklist**

- Data owner and steward named in OpenMetadata before any pipeline goes live.

- Access agreement and security review on file with BCIT.

- Refresh schedule, monitoring, and alerting defined and tested.

- Data quality rules in place for any source feeding a production intelligence product.

- Lineage from source to semantic layer to product visible in the catalog.

**SECTION 7**

# **Governance — data, AI, and operating discipline**

Governance is the discipline that decides whether the platform earns trust and the products earn use. It is also the difference between a city that adopts AI responsibly and one that gets surprised by it. This section defines three governance instruments: a Data Governance Policy, an AI Governance and use case intake process, and the operating rituals that keep both honest.

### **Data Governance Policy — ownership and timeline**

Sand drafts the formal Data Governance Policy as an M1 deliverable, due in month 3. Vera Choo (Data Governance and Analytics Manager) owns ratification and adoption, with executive approval from the CDO. The policy covers: ownership and stewardship, sensitivity and access tiers, retention, sharing and external release, lineage and quality standards, and a steward onboarding process. v2 of the policy in month 11 incorporates production lessons.

### **AI governance — the lightweight but real version**

AI governance is a six-step operating process, not a 60-page document. It runs through every use case the city builds, including ones that are not part of this engagement.

- 1\. Intake — single form, single owner, no side channels.

- 2\. Risk tier — low / medium / high based on data sensitivity, decision impact, and resident-facing surface.

- 3\. Privacy and security review — routed by tier; high-risk use cases require Law and BCIT security signoff.

- 4\. Human-in-the-loop rules — explicit per use case; no use case ships without them.

- 5\. Logging and grounding — every model output is grounded through the MCP/tool layer and logged for audit.

- 6\. Post-launch monitoring — monthly scorecard, incident path, and a defined retirement clause if the use case stops earning its keep.

### **What the operating rituals enforce**

- No production AI feature runs without an approved use case brief on file.

- No KPI is used in production until it appears in the KPI dictionary.

- No public release of any data product happens without Executive Sponsor and Data Governance Manager signoff.

- No use case proceeds past pilot without baseline metrics and a published scorecard.

### **Audit and oversight readiness**

The platform, the semantic layer, and the AI governance process are designed to be readable from the outside. At any point, an external reviewer should be able to see: every data source, its owner, and its lineage; every KPI definition; every approved use case and its risk tier; every production output’s grounding and logging trail. This is what “responsible AI” looks like in operation.

**SECTION 8**

# **Responsibility split — city vs Sand**

The pre-kickoff briefing left this as a placeholder. This section locks it in. The split is read with two questions in mind: who decides, and who delivers.

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

### **Boundary cases**

- BPD interfaces — BPD owns Axon and any direct connection to it. The engagement integrates through whatever interfaces BPD stands up.

- BCIT-managed systems — OPI partners with BCIT as the system of record owner; the engagement does not duplicate or replace BCIT operational responsibilities.

- Open Data — the Open Data program transfers from BCIT to OPI in FY27. Sand supports the data side of the transition; the program management transition is OPI’s.

**SECTION 9**

# **Risks and mitigations**

Six risks are material enough to manage explicitly. Each has a named owner, a mitigation, and a leading indicator the BIC reviews monthly.

| **Risk**                           | **Why it matters**                                                                                                  | **Mitigation**                                                                                                                     | **Owner**                                |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| Innovation Lab capacity gap        | Two funded engineers cannot absorb capability transfer in months 7–12 and run the program from month 13 onward.     | Close Innovation Program Manager seat by month 9; close Civic Technology Lead and Civic Design and UX Lead by month 12.            | Executive Sponsor                        |
| Source-system access slippage      | Wave-one ingest depends on agency partner availability and BCIT approvals; any one slipping delays the lead pilot.  | Lock wave-one access in month 1; named agency owners; weekly status with BCIT.                                                     | Project Lead + Platform Engineering Lead |
| Data governance ratification delay | Without a ratified policy, the catalog is decoration and the AI governance process is on shaky ground.              | Sand drafts in M1; Vera ratifies by end of month 5; executive approval at the May steering.                                        | Vera Choo + Executive Sponsor            |
| Use case sprawl                    | Demand will exceed capacity. Without intake discipline, the program becomes reactive and quality drops.             | Single intake; risk tier; no production work without an approved brief; quarterly portfolio review prunes use cases.               | Project Lead                             |
| Vendor handoff friction            | A capability-transfer plan that exists on paper but does not run will leave OPI dependent on Sand at month 12.      | Capability-transfer scorecard tracked monthly from month 1; OPI staff own at least 70% of operational tasks by month 12.           | Project Lead + Sand engagement manager   |
| Public exposure before maturity    | A public-facing AI product released before the platform and governance are mature is the fastest way to lose trust. | No public release without Executive Sponsor and Data Governance Manager signoff; internal-first product strategy through month 12. | Executive Sponsor                        |

**SECTION 10**

# **Target state and guiding principles**

This section answers the question every funder, agency partner, and executive will eventually ask: how will we know whether this worked? It defines the target state Baltimore is building toward and the principles that govern how the work is done. Both are operating instruments — the BIC reviews them quarterly to keep the program honest.

### **Target state — the five pillars**

| **Pillar**                           | **What success looks like**                                                                                                                                                                                                                                        | **Evidence the city should be able to show**                                                                           |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| Leadership and operating model       | OPI leads citywide data and AI strategy and portfolio management with executive sponsorship and active partnership from BCIT, Law, Procurement, Finance, and agency sponsors. Each use case has a business owner, a technical lead, and a decision-making cadence. | BIC charter, org map, working group roster, decision rights, named sponsors, monthly steering minutes.                 |
| Trusted data and semantic foundation | Baltimore has a governed data environment, standard KPI definitions, and a working semantic layer for at least two priority domains.                                                                                                                               | Architecture diagram, KPI dictionary, source map, data quality rules, catalog populated, semantic layer documentation. |
| Responsible AI governance            | A lightweight but real governance process is in operation — intake, risk tiering, privacy and security review, human-in-the-loop rules, logging, and post-launch monitoring.                                                                                       | Data Governance Policy v2, intake form, risk matrix, review checklist, approval log, incident path.                    |
| Operational use cases                | Two to three bounded use cases are live or in disciplined pilot — City Services Intelligence, StatGPT, and OPI Internal Intelligence.                                                                                                                              | Use case briefs, demo screens, named pilot users, baseline metrics, monthly scorecards.                                |
| Evidence and readiness               | The city can show training records, baseline metrics, usage and quality dashboards, review decisions, case studies, and a realistic continuation roadmap.                                                                                                          | Training materials, attendance log, usage dashboard, case study, continuation plan for months 13–18 and beyond.        |

### **Guiding principles**

Twelve principles, written so they can be read by anyone working on the program and used as a yes/no test for design and delivery decisions.

- Govern first, build second. Every dataset and KPI has a named owner before it powers a product.

- Ground every output. AI responses are grounded through the MCP/tool layer; freeform model-only answers do not ship.

- One definition per metric. The KPI dictionary is the canonical source; no parallel definitions in product code.

- Intake is single-channel. No side projects, no shadow data products.

- Pilot before scale. Every product earns its way out of pilot through measured use and decision-impact.

- Internal-first. Resident-facing products come after the platform and governance are mature.

- Human-in-the-loop. Every production use case names where a human decides; no autonomous-action use cases without explicit executive approval.

- Measure what matters. Usage, grounded-answer rate, exception rate, and decision-impact — monthly, every product.

- Retire what does not earn its keep. Products with no measured impact at the six-month review are sunset.

- Reuse over rebuild. Every new domain reuses the platform, semantic layer, governance process, and design system.

- Capability transfer is real. The vendor leaves on schedule; the city carries the program.

- Be readable from the outside. Sources, owners, KPIs, use cases, and grounding logs should be inspectable by an external reviewer at any time.

**SECTION 11**

# **Capability transfer and the city-led continuation**

### **What capability transfer means here**

Capability transfer is not documentation handoff. It is the structured process by which OPI staff move from observers, to pairs, to leads, to operators — across every layer of the program. It runs from month one of the engagement, not month nine.

### **The four-stage transfer model**

| **Stage** | **OPI role**                                   | **Sand role**                    | **Target months** |
|-----------|------------------------------------------------|----------------------------------|-------------------|
| Observe   | Watches Sand build and explain.                | Builds and explains.             | Months 0–2        |
| Pair      | Builds with Sand; pull-request review by Sand. | Pairs and reviews.               | Months 2–6        |
| Lead      | Owns delivery; Sand reviews architecture only. | Architecture review and on-call. | Months 6–9        |
| Operate   | Runs day-to-day end-to-end.                    | Advisory and on-call only.       | Months 9–12       |

### **What the city has to be able to do alone by month 12**

- Build, deploy, and monitor a new ingest pipeline.

- Add a new dataset to the catalog with owner, steward, sensitivity, and lineage.

- Add a new KPI to the dictionary and the semantic layer.

- Stand up a new use case end-to-end — intake, risk-tier, build, pilot, scorecard.

- Run the AI evaluation framework and produce the monthly quality report.

- Publish a new product release to internal users.

### **City-led months 13–18 — what gets built without the vendor**

- A second-domain replication of the City Services Intelligence pattern (permitting, housing, or vacants).

- GenBI, the Neighborhoods Map, and the Neighborhoods Explorer with Chat.

- Data Governance Policy v3 with year-one production lessons.

- A continuation plan and budget for years two and three.

- A public case study, written for peer cities and philanthropic audiences.

**SECTION 12**

# **Open issues to resolve at kickoff**

The pre-kickoff briefing flagged a number of placeholders. Most are resolved in this guide. The ones below are still open and need to be closed in the first two weeks of the engagement. Each has an owner, a target close date, and a path.

| **Open issue**                                                                   | **Why it matters**                                                                                                                                 | **Owner**                                  | **Close by** |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|--------------|
| Sand TPM and engagement-manager assignment                                       | Daily and weekly cadence depends on knowing who, on the Sand side, holds the seat.                                                                 | Sand engagement leadership                 | Week 2       |
| Operations Analyst, Data Governance Analyst, and Data Engineer (Python) staffing | Listed as TBD in pre-kickoff. Affects M1 capacity for ingest and governance.                                                                       | Project Lead + Sand TPM                    | Week 2       |
| Cityworks interface (direct vs API) and CAD interface                            | Wave-one ingest depends on confirmed interface. Slippage delays City Services Intelligence and StatGPT.                                            | Platform Engineering Lead + agency owners  | Week 3       |
| Innovation Program Manager funding decision                                      | Material risk to capability transfer. Without it, OPI cannot absorb the program at month 12.                                                       | Executive Sponsor + philanthropic partners | Month 6      |
| BI / GenBI tool selection                                                        | Workstream 3 product roadmap for months 10–18 depends on it.                                                                                       | Project Lead + Deputy CDO + Sand           | Month 9      |
| Public communications posture                                                    | When and how to talk about the BIC publicly — internal-first through month 12, but a published case study at month 18.                             | Executive Sponsor + OPI Communications     | Month 6      |
| City code or charter alignment                                                   | Article 1, Subtitle 61 already requires OPI to run CitiStat and operate an Innovation Lab. Confirm whether the BIC needs any further codification. | Executive Sponsor + Law                    | Month 9      |

**APPENDIX A**

# **Baltimore Intelligence Center — full squad roster**

OPI staff who are part of the BIC, with full positions and home teams. Sand roles are listed by function rather than name and are confirmed in week one.

| **Role on the BIC**                        | **Name**                  | **Position**                                   | **Home team**                  |
|--------------------------------------------|---------------------------|------------------------------------------------|--------------------------------|
| Executive Sponsor and interim Project Lead | Dartanion Swift-Williams  | Executive Director and Chief Data Officer, OPI | OPI — Director’s Office        |
| Product Manager                            | Chiemeka Okeoma           | Senior Product Engineer                        | OPI — Innovation Lab           |
| Project Manager                            | Mallory Screws            | Project Manager                                | OPI                            |
| Data Engineering Lead                      | Alejandro Zuniga Sosa     | Principal Data Engineer                        | OPI — Data and Analytics       |
| Platform Engineering Lead                  | Koby Samuel               | Principal Platform Engineer                    | OPI — Data and Analytics       |
| Data Science and Analytics                 | Selenea Gibson            | Applied Data Scientist                         | OPI — Data and Analytics       |
| Data Engineering                           | Briya Bhakta              | Senior Data Engineer                           | OPI — Data and Analytics       |
| Technical Program Management               | Roberto Herbruger         | Technical Program Manager                      | OPI — Data and Analytics       |
| Data Governance and Analytics              | Vera Choo                 | Data Governance and Analytics Manager          | OPI — Data and Analytics       |
| Deputy CDO and platform partnership        | Jason Howard, PhD         | Deputy Chief Data Officer                      | OPI — Data and Analytics       |
| Product Engineering                        | Xander Jake de los Santos | Product Engineer                               | OPI — Innovation Lab           |
| CitiStat — City Services lead              | Nelson Gomes Boronat      | CitiStat Analyst                               | OPI — Performance and CitiStat |
| CitiStat — City Services lead              | Ross Hackett              | CitiStat Analyst                               | OPI — Performance and CitiStat |
| CitiStat — Public Safety lead              | Derek Thomas              | CitiStat Analyst                               | OPI — Performance and CitiStat |

### **Sand Technologies — expected roles**

- Engagement Manager — weekly partnership with the Project Lead.

- Technical Program Manager — daily partnership with the OPI Project Manager.

- Principal Architect — platform and semantic-layer architecture lead.

- Semantic Layer Lead — KPI dictionary and MCP/tool layer implementation.

- Data Engineering team — ingest, transformations, quality.

- AI/ML Engineer — model integration, grounding, evaluation framework.

- Product Engineering — intelligence products and internal operating tools.

- Design Lead — design system and product UX.

- UX Researcher — user research and adoption support.

- Capability Transfer Lead — structured handoff across all workstreams.

- Governance Advisor — Data Governance Policy authorship and review templates.

**APPENDIX B**

# **Glossary**

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
