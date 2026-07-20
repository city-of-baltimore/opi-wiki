# Responsible data & AI

{{ page_header(summary="How BIC keeps city data governed and AI accountable by design, not after the fact.") }}

Because BIC makes city data easier to use, it has to make city data harder to misuse. Governance is built into every use case at intake, not patched on after a product ships. The full policy lives in the [Data Governance Framework](../../../about-us/our-teams/data-and-analytics/data-governance-framework.md), and this page is the BIC-specific summary.

## OPI owns meaning; the platform enforces it

The single most important rule is that OPI decides what a metric, a sensitivity tier, or an access rule means, and the platform enforces it. Definitions and access rules are a governance decision, not an engineering one.

Three bodies jointly clear BIC data work: OPI (the programmatic and administrative owner of definitions and fitness), City Legal (privacy and disclosure), and BCIT information security (confidentiality, integrity, and availability).

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

AI use cases follow a governed lifecycle rather than an open door. Every use case is approved before it is built, stating the decision it supports, the data and tiers it needs, and its risks. No model touches raw data; every AI query goes through a governed tool. A tool will not return a PII field, an unverified metric, or equity-unadjusted demand data, and every answer cites an approved definition, with its version, time window, and caveats. Every tool call is logged, so the city can reconstruct exactly what data and definition produced any answer. Review thresholds are set before launch, and definitions and tools are versioned so they can be rolled back.

## Start small, and stay in scope

BIC earns trust before it expands. The first pilots use low-sensitivity city-services data, such as 311 service requests. Two areas are deliberately out of scope for the early work. Police and criminal-justice data is excluded from the pilot: only US citizens may access the underlying data, and police data is individually authorized. Health, education, and payment data stays out unless a specific use case requires it and clears governance.

Peer-city experience drives this discipline. The programs that kept public trust started on low-risk services and treated their data-classification policy as law. The ones that overreached into surveillance lost legitimacy. Baltimore starts with trash pickup and traffic, not policing.

## Read alongside

- [Data Governance Framework](../../../about-us/our-teams/data-and-analytics/data-governance-framework.md): the full classification, stewardship, privacy, and AI-accountability policy.
- [Architecture](architecture-and-roadmap.md): where the gate sits in the stack.
- [Products & capabilities](products-and-capabilities.md): how grounding and logging show up in the products.
