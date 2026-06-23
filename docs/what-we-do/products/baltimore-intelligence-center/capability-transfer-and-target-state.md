# Capability Transfer and Target State

{{ page_header(summary="What “capability transfer” actually means here, what Baltimore should be able to do alone by month 12, and the target state every funder, agency partner, and executive will eventually ask about.") }}

## What capability transfer means here

Capability transfer is not documentation handoff. It is the structured process by which OPI staff move from observers, to pairs, to leads, to operators — across every layer of the program. It runs from month one of the engagement, not month nine.

## The four-stage transfer model

| **Stage** | **OPI role**                                   | **Sand role**                    | **Target months** |
|-----------|------------------------------------------------|----------------------------------|-------------------|
| Observe   | Watches Sand build and explain.                | Builds and explains.             | Months 0–2        |
| Pair      | Builds with Sand; pull-request review by Sand. | Pairs and reviews.               | Months 2–6        |
| Lead      | Owns delivery; Sand reviews architecture only. | Architecture review and on-call. | Months 6–9        |
| Operate   | Runs day-to-day end-to-end.                    | Advisory and on-call only.       | Months 9–12       |

## What the city has to be able to do alone by month 12

- Build, deploy, and monitor a new ingest pipeline.

- Add a new dataset to the catalog with owner, steward, sensitivity, and lineage.

- Add a new KPI to the dictionary and the semantic layer.

- Stand up a new use case end-to-end — intake, risk-tier, build, pilot, scorecard.

- Run the AI evaluation framework and produce the monthly quality report.

- Publish a new product release to internal users.

## City-led months 13–18 — what gets built without the vendor

- A second-domain replication of the City Services Intelligence pattern (permitting, housing, or vacants).

- GenBI, the Neighborhoods Map, and the Neighborhoods Explorer with Chat.

- Data Governance Policy v3 with year-one production lessons.

- A continuation plan and budget for years two and three.

- A public case study, written for peer cities and philanthropic audiences.

## Target state — the five pillars

This section answers the question every funder, agency partner, and executive will eventually ask: how will we know whether this worked? Both the pillars and the principles that follow are operating instruments — the BIC reviews them quarterly to keep the program honest.

| **Pillar**                           | **What success looks like**                                                                                                                                                                                                                                        | **Evidence the city should be able to show**                                                                           |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| Leadership and operating model       | OPI leads citywide data and AI strategy and portfolio management with executive sponsorship and active partnership from BCIT, Law, Procurement, Finance, and agency sponsors. Each use case has a business owner, a technical lead, and a decision-making cadence. | BIC charter, org map, working group roster, decision rights, named sponsors, monthly steering minutes.                 |
| Trusted data and semantic foundation | Baltimore has a governed data environment, standard KPI definitions, and a working semantic layer for at least two priority domains.                                                                                                                               | Architecture diagram, KPI dictionary, source map, data quality rules, catalog populated, semantic layer documentation. |
| Responsible AI governance            | A lightweight but real governance process is in operation — intake, risk tiering, privacy and security review, human-in-the-loop rules, logging, and post-launch monitoring.                                                                                       | Data Governance Policy v2, intake form, risk matrix, review checklist, approval log, incident path.                    |
| Operational use cases                | Two to three bounded use cases are live or in disciplined pilot — City Services Intelligence, StatGPT, and OPI Internal Intelligence.                                                                                                                              | Use case briefs, demo screens, named pilot users, baseline metrics, monthly scorecards.                                |
| Evidence and readiness               | The city can show training records, baseline metrics, usage and quality dashboards, review decisions, case studies, and a realistic continuation roadmap.                                                                                                          | Training materials, attendance log, usage dashboard, case study, continuation plan for months 13–18 and beyond.        |

## Guiding principles

Twelve principles, written so they can be read by anyone working on the program and used as a yes/no test for design and delivery decisions. They cluster into three groups: governance, delivery discipline, and sustainability.

### Governance

- **Govern first, build second.** Every dataset and KPI has a named owner before it powers a product.
- **Ground every output.** AI responses are grounded through the MCP/tool layer; freeform model-only answers do not ship.
- **One definition per metric.** The KPI dictionary is the canonical source; no parallel definitions in product code.
- **Intake is single-channel.** No side projects, no shadow data products.

### Delivery discipline

- **Pilot before scale.** Every product earns its way out of pilot through measured use and decision-impact.
- **Internal-first.** Resident-facing products come after the platform and governance are mature.
- **Human-in-the-loop.** Every production use case names where a human decides; no autonomous-action use cases without explicit executive approval.
- **Measure what matters.** Usage, grounded-answer rate, exception rate, and decision-impact — monthly, every product.

### Sustainability

- **Retire what does not earn its keep.** Products with no measured impact at the six-month review are sunset.
- **Reuse over rebuild.** Every new domain reuses the platform, semantic layer, governance process, and design system.
- **Capability transfer is real.** The vendor leaves on schedule; the city carries the program.
- **Be readable from the outside.** Sources, owners, KPIs, use cases, and grounding logs should be inspectable by an external reviewer at any time.
