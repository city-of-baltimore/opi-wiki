# Governance and Risks

{{ page_badge() }}

> Data governance, AI governance, the risks that are big enough to manage explicitly, and the open issues that have to close in the first weeks.

Governance is the discipline that decides whether the platform earns trust and the products earn use. It is also the difference between a city that adopts AI responsibly and one that gets surprised by it.

## Data Governance Policy — ownership and timeline

Sand drafts the formal Data Governance Policy as an M1 deliverable, due in month 3. Vera Choo (Data Governance and Analytics Manager) owns ratification and adoption, with executive approval from the Chief Data Officer. The policy covers: ownership and stewardship, sensitivity and access tiers, retention, sharing and external release, lineage and quality standards, and a steward onboarding process. v2 of the policy in month 11 incorporates production lessons.

## AI governance — the lightweight but real version

AI governance is a six-step operating process, not a 60-page document. It runs through every use case the city builds, including ones that are not part of this engagement.

1. **Intake** — single form, single owner, no side channels.
2. **Risk tier** — low / medium / high based on data sensitivity, decision impact, and resident-facing surface.
3. **Privacy and security review** — routed by tier; high-risk use cases require Law and BCIT security signoff.
4. **Human-in-the-loop rules** — explicit per use case; no use case ships without them.
5. **Logging and grounding** — every model output is grounded through the MCP/tool layer and logged for audit.
6. **Post-launch monitoring** — monthly scorecard, incident path, and a defined retirement clause if the use case stops earning its keep.

## What the operating rituals enforce

- No production AI feature runs without an approved use case brief on file.

- No KPI is used in production until it appears in the KPI dictionary.

- No public release of any data product happens without Executive Sponsor and Data Governance Manager signoff.

- No use case proceeds past pilot without baseline metrics and a published scorecard.

## Audit and oversight readiness

The platform, the semantic layer, and the AI governance process are designed to be readable from the outside. At any point, an external reviewer should be able to see: every data source, its owner, and its lineage; every KPI definition; every approved use case and its risk tier; every production output’s grounding and logging trail. This is what “responsible AI” looks like in operation.

## Risks and mitigations

Six risks are material enough to manage explicitly. Each has a named owner, a mitigation, and a leading indicator the BIC reviews monthly.

| **Risk**                           | **Why it matters**                                                                                                  | **Mitigation**                                                                                                                     | **Owner**                                |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| Innovation Lab capacity gap        | The current staffed Innovation Lab bench is lean relative to the capability-transfer burden in months 7–12 and ongoing sustainment after the vendor drawdown. | Scope the work to the current staffed roster, pair Sand transfer directly with named OPI owners, and treat aspirational roles as additive capacity rather than baseline assumptions. | Executive Sponsor                        |
| Source-system access slippage      | Wave-one ingest depends on agency partner availability and BCIT approvals; any one slipping delays the lead pilot.  | Lock wave-one access in month 1; named agency owners; weekly status with BCIT.                                                     | Project Lead + Platform Engineering Lead |
| Data governance ratification delay | Without a ratified policy, the catalog is decoration and the AI governance process is on shaky ground.              | Sand drafts in M1; Vera ratifies by end of month 5; executive approval at the May steering.                                        | Vera Choo + Executive Sponsor            |
| Use case sprawl                    | Demand will exceed capacity. Without intake discipline, the program becomes reactive and quality drops.             | Single intake; risk tier; no production work without an approved brief; quarterly portfolio review prunes use cases.               | Project Lead                             |
| Vendor handoff friction            | A capability-transfer plan that exists on paper but does not run will leave OPI dependent on Sand at month 12.      | Capability-transfer scorecard tracked monthly from month 1; OPI staff own at least 70% of operational tasks by month 12.           | Project Lead + Sand engagement manager   |
| Public exposure before maturity    | A public-facing AI product released before the platform and governance are mature is the fastest way to lose trust. | No public release without Executive Sponsor and Data Governance Manager signoff; internal-first product strategy through month 12. | Executive Sponsor                        |

## Open issues to resolve at kickoff

The pre-kickoff briefing flagged a number of placeholders. Most are resolved across this hub. The ones below are still open and need to be closed in the first two weeks of the engagement. Each has an owner, a target close date, and a path.

| **Open issue**                                                                   | **Why it matters**                                                                                                                                 | **Owner**                                  | **Close by** |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|--------------|
| Sand TPM and engagement-manager assignment                                       | Daily and weekly cadence depends on knowing who, on the Sand side, holds the seat.                                                                 | Sand engagement leadership                 | Week 2       |
| Operations Analyst, Data Governance Analyst, and Data Engineer (Python) staffing | Listed as TBD in pre-kickoff. Affects M1 capacity for ingest and governance.                                                                       | Project Lead + Sand TPM                    | Week 2       |
| Cityworks interface (direct vs API) and CAD interface                            | Wave-one ingest depends on confirmed interface. Slippage delays City Services Intelligence and StatGPT.                                            | Platform Engineering Lead + agency owners  | Week 3       |
| Innovation Lab sustainment posture                                               | Material risk to capability transfer. Sustainment planning must assume the current staffed roster and documented handoff coverage at month 12.    | Executive Sponsor + Chief of Staff         | Month 6      |
| BI / GenBI tool selection                                                        | Workstream 3 product roadmap for months 10–18 depends on it.                                                                                       | Project Lead + Deputy CDO + Sand           | Month 9      |
| Public communications posture                                                    | When and how to talk about the BIC publicly — internal-first through month 12, but a published case study at month 18.                             | Executive Sponsor + OPI Communications     | Month 6      |
| City code or charter alignment                                                   | Article 1, Subtitle 61 already requires OPI to run CitiStat and operate an Innovation Lab. Confirm whether the BIC needs any further codification. | Executive Sponsor + Law                    | Month 9      |
