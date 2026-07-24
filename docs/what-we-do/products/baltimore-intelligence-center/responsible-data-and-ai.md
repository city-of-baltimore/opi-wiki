# Responsible data & AI

{{ page_header(summary="How BIC keeps city data governed and AI accountable by design, not after the fact.") }}

Because BIC makes city data easier to use, it has to make city data harder to misuse. Governance is built into every use case at intake, not patched on after a product ships. The full policy lives in the [Data Governance Framework](../../../about-us/our-teams/data-and-analytics/data-governance-framework.md), and this page is the BIC-specific summary.

## OPI owns meaning; the platform enforces it

The single most important rule is that OPI decides what a metric, a sensitivity tier, or an access rule means, and the platform enforces it. Definitions and access rules are a governance decision, not an engineering one.

BIC data work is reviewed by the appropriate data owners and City legal, privacy, and security authorities. The review covers whether a use is appropriate, which information it needs, and what controls must apply.

## Four data tiers, enforced at the gate

Every data element carries one of four sensitivity tiers, aligned to the State of Maryland's four-tier scheme. The tier drives who may see the data, how it is protected, and whether an AI product may surface it.

| Tier | What it covers | Default access |
| --- | --- | --- |
| **Public** | Approved for release; no harm from disclosure | Anyone |
| **Protected** | City operational use; controlled access; not for public release | Authenticated analyst |
| **Confidential** | Could harm individuals or the City; most PII and precise geolocation | Named, justified |
| **Restricted** | Legally restricted; disclosure carries regulatory or criminal exposure | Individually authorized |

Access defaults to deny. A governance gate refuses to serve any field or metric that has not cleared governance, regardless of what sits in the warehouse. It is enforced at two points: role-based access on the warehouse for direct queries, and the governed tool layer for AI queries. Access control and AI governance share one control surface.

## Responsible AI, in practice

AI uses follow a governed lifecycle. Each use states the decision it supports, the approved data it needs, its risks, the role of human review, and how results will be evaluated. Models work from governed outputs rather than raw source data. Access is limited by role, answers remain grounded in approved definitions and sources, and activity is logged for monitoring and review. Uses can be changed, paused, or retired when evidence or risk changes.

## Read alongside

- [Data Governance Framework](../../../about-us/our-teams/data-and-analytics/data-governance-framework.md): the full classification, stewardship, privacy, and AI-accountability policy.
- [Architecture](architecture-and-roadmap.md): where the gate sits in the stack.
- [Capabilities](products-and-capabilities.md): how grounding and review apply to product experiences.
