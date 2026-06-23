# The Five Workstreams

{{ page_header(summary="Five workstreams that build on each other. The platform comes first, because nothing else works without it.") }}

The engagement is organized into five workstreams. They build on each other: the platform comes first because nothing else works without it; the semantic layer translates the platform into city language; the products prove the platform in real workflows; the internal tools tighten OPI’s own operating discipline; and the design system, adoption practice, and capability-transfer plan make sure what gets built survives the vendor handoff.

| **Workstream**                                       | **What it does**                                                                                  |
|------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [1 — Citywide Data Platform and Governance](#workstream-1-citywide-data-platform-and-governance) | Stand up the governed Azure data environment that everything else runs on.                        |
| [2 — Semantic Intelligence Layer](#workstream-2-semantic-intelligence-layer)                     | Translate raw city data into the city’s actual decision-making language.                          |
| [3 — Intelligence Products](#workstream-3-intelligence-products)                                 | Two flagship products in months 0–6, then OPI Internal Intelligence and additional products.     |
| [4 — OPI Internal Operating Tools](#workstream-4-opi-internal-operating-tools)                   | A small set of internal tools that make OPI itself more disciplined.                              |
| [5 — Design System, Adoption, and Capability Transfer](#workstream-5-design-system-adoption-and-capability-transfer) | The work that decides whether the platform and products survive after Sand leaves.                |

---

## Workstream 1 — Citywide Data Platform and Governance

Stand up the governed Azure data environment that everything else runs on. Medallion architecture, ingest pipelines for the priority sources, data quality rules, lineage, an open-source data catalog, and an actual data governance policy.

### What gets done by month 12

- **M3** — Reference architecture and security review approved with BCIT.
- **M3** — Data Governance Policy v1 drafted.
- **M5** — Data Governance Policy v1 ratified.
- **M6** — Wave-one ingest live for at least four priority sources (see [Roadmap and Source Systems](roadmap-and-source-systems.md#wave-one-months-06)).
- **M6** — Containerized Python ingest jobs orchestrated through Azure DevOps or GitHub Actions.
- **M6** — Data quality rules running on at least 311, Cityworks, and the Public Safety Incidents source.
- **M9** — OpenMetadata deployed inside the City’s Azure tenant, populated, and integrated with at least two source systems.
- **M11** — Data Governance Policy v2 incorporating production lessons.
- **M12** — Platform runbooks and operational handbook published; on-call rotation established.

### Roles and dependencies

**OPI lead.** Alejandro Zuniga Sosa (Data Engineering Lead). Vera Choo owns governance ratification.

**Sand role.** Principal Architect (lead), Data Engineering team, DevOps engineer, Governance Advisor. Sand drafts the Data Governance Policy as an M1 deliverable; Vera owns ratification.

**Key dependencies.** BCIT security and network approvals; agency data-sharing agreements where required; Azure tenant readiness.

### Exit criteria — what “done” looks like at month 12

- Wave-one priority sources are ingested on schedule with monitoring and quality rules.

- Data Governance Policy is ratified and in use; at least 10 datasets have named owners and stewards in the catalog.

- OPI staff can build, deploy, and monitor a new ingest pipeline without Sand in the chair.

---

## Workstream 2 — Semantic Intelligence Layer

Translate raw city data into the city’s actual decision-making language. Domain semantic layers, a KPI dictionary, an MCP-style server and tool layer, and an evaluation framework for AI outputs.

### What gets done by month 12

- **M6** — KPI dictionary v1 covering city services and public safety domains.
- **M6** — Semantic layer for city services live and powering City Services Intelligence.
- **M6** — MCP server and tool layer in production for the city services domain.
- **M9** — AI evaluation framework documented and running on the lead intelligence product, with grounded-answer rate, exception rate, and human-review thresholds.
- **M12** — MCP server and tool layer expanded to public safety and neighborhoods.
- **M12** — Domain semantic layers live for city services, public safety, and neighborhoods; permitting and housing scoped for follow-on.

### Roles and dependencies

**OPI lead.** Vera Choo (Data Governance and Analytics Manager) for KPI dictionary and definitions; Alejandro Zuniga Sosa for technical implementation; Selenea Gibson for evaluation framework.

**Sand role.** Semantic Layer Lead (lead), AI/ML Engineer, Domain Modeling support. Sand drives implementation; OPI owns the meaning of every KPI.

**Key dependencies.** Workstream 1 platform readiness; agency partner availability to validate KPI definitions; CitiStat’s existing measure library as starting input.

### Exit criteria — what “done” looks like at month 12

- Every metric used by an intelligence product is defined once in the KPI dictionary; no parallel definitions.

- Every AI response in production is grounded through the MCP/tool layer — no freeform model-only answers.

- Evaluation framework produces a monthly quality report reviewed by the BIC leadership and Executive Sponsor.

---

## Workstream 3 — Intelligence Products

Two flagship intelligence products in months 0–6 — City Services Intelligence (lead pilot) and a CitiStat StatGPT pilot in parallel. OPI Internal Intelligence and additional products (GenBI, Neighborhoods Map, Neighborhoods Explorer with Chat) follow in months 7–12.

### What gets done by month 12

- **M6** — City Services Intelligence in disciplined pilot with named users and weekly usage measurement (lead pilot covering 311, Cityworks, public safety incidents, crash, vacants, and neighborhood data).
- **M6** — StatGPT pilot running for City Services and Public Safety Stat preparation, with measured time-to-prep reduction.
- **M9** — OPI Internal Intelligence live for OPI staff to support knowledge management and operating discipline.
- **M12** — Use case briefs, baseline metrics, and monthly scorecards published for each product.
- **M12** — GenBI, Neighborhoods Map, and Neighborhoods Explorer with Chat scoped and planned for months 10–18.

### Roles and dependencies

**OPI lead.** Chiemeka Okeoma (Product Manager) for City Services Intelligence and OPI Internal Intelligence. Nelson Gomes Boronat and Ross Hackett (CitiStat) for StatGPT City Services. Derek Thomas (CitiStat) for StatGPT Public Safety.

**Sand role.** Product Engineering (lead), AI/ML Engineer, Design Lead, UX Researcher. Sand co-builds; OPI Product Manager owns the roadmap.

**Key dependencies.** Workstream 2 semantic layer readiness; agency partner availability for user research; AI governance approval (use case intake and risk tiering).

### Exit criteria — what “done” looks like at month 12

- City Services Intelligence and StatGPT pilot have at least 10 weekly active users each by month 12, with measured decision-impact.

- Each product has a monthly scorecard reviewed by BIC leadership: usage, grounded-answer rate, exception rate, user-reported usefulness, decisions supported.

- OPI Product Manager and Product Engineering team can ship a new feature or new use case without Sand in the chair.

---

## Workstream 4 — OPI Internal Operating Tools

A small set of internal tools that strengthen OPI's own operating discipline: a SharePoint Governance Scanner, a Project Status Reporting Tool, and a Portfolio Reporting Pack.

### What gets done by month 12

- **M9** — SharePoint Governance Scanner deployed for OPI to surface document hygiene, access risk, and information-architecture drift.
- **M10** — Project Status Reporting Tool in use across OPI to standardize status, risks, and decisions.
- **M12** — Portfolio Reporting Pack producing a monthly executive view for the Executive Director, the Mayor, and philanthropic funders.

### Roles and dependencies

**OPI lead.** Chiemeka Okeoma (Product Manager) and Mallory (Project Manager).

**Sand role.** Product Engineering supports; Sand provides templates and reference implementations from prior city engagements.

**Key dependencies.** OPI SharePoint operating system strategy already in place; existing OPI charter and intake templates as inputs.

### Exit criteria — what “done” looks like at month 12

- OPI runs its weekly portfolio review off the Status Tool, not off email and slides.

- SharePoint Scanner has identified and remediated at least three meaningful governance issues.

- Portfolio Pack is the executive’s default monthly read.

---

## Workstream 5 — Design System, Adoption, and Capability Transfer

The work that decides whether the platform and products survive after Sand leaves. A shared design system, an adoption playbook, and a structured capability-transfer plan from Sand to OPI staff.

### What gets done by month 12

- **M6** — Design system v1 in use across both flagship products, with brand-aligned components and accessibility built in.
- **M7** — Adoption playbook live for City Services Intelligence and StatGPT pilot, covering training, office hours, documentation, and feedback loops.
- **M9** — OPI staff own day-to-day delivery across the four other workstreams as the structured capability-transfer program progresses.
- **M12** — Capability-transfer scorecard tracked monthly; OPI staff own at least 70% of operational tasks.
- **M12** — Design system v2 published.

### Roles and dependencies

**OPI lead.** Chiemeka Okeoma (PM) with designated design support as needed. Adoption: Vera Choo and Mallory.

**Sand role.** Design Lead, Capability Transfer Lead, Adoption Lead. Sand pairs and trains; OPI staff own day-to-day delivery by month 9.

**Key dependencies.** Named design coverage for the workstream; OPI Performance Standards and onboarding artifacts already in place.

### Exit criteria — what “done” looks like at month 12

- OPI staff are the daily operators for the platform, the catalog, the semantic layer, and the two flagship products.

- Sand transitions to an advisory and on-call posture by month 12.

- A documented continuation plan exists for months 13–18 (city-led) and beyond.

For the structured handoff model that runs through every workstream, see [Capability Transfer and Target State](capability-transfer-and-target-state.md#the-four-stage-transfer-model).
