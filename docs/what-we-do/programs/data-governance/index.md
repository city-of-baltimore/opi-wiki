# Data Governance

Data Governance is OPI's standing program for making city data trustworthy by design. It sets how data is classified, who stewards it, how quality is checked, how it may be shared, and how AI use is held accountable, so every downstream dashboard, open dataset, and AI product inherits the same discipline.

The guiding principle is that OPI owns what the data means, and the platform enforces it. Definitions, sensitivity tiers, and access rules are governance decisions, not engineering ones.

## What the program covers

The program starts with classification: every data element carries a sensitivity tier (Public, Protected, Confidential, or Restricted), aligned to the State of Maryland's four-tier scheme. Stewardship names owners for priority datasets and sets up the councils and cadences that keep them accountable. Quality means baseline data-quality checks and standardized PII tagging across the platform's governed data. The KPI dictionary gives each priority metric one official definition. And responsible AI adds use-case intake, risk tiering, human oversight, grounding, and logging before anything scales.

The full policy covers classification tiers, stewardship roles, privacy, security, inter-agency sharing, and AI accountability. It lives in the [Data Governance Framework](../../../about-us/our-teams/data-and-analytics/data-governance-framework.md).

## Responsible AI

The same governance that classifies and protects data also governs how the City uses AI on it. Access defaults to deny: a governance gate refuses to serve any field or metric that has not cleared governance, and that gate applies both to direct queries and to AI products, so access control and AI governance share one control surface.

Each AI use follows a governed lifecycle. It states the decision it supports, the approved data it needs, its risks, the role of human review, and how results will be evaluated. Models work from governed outputs rather than raw source data, answers stay grounded in approved definitions and sources, activity is logged for monitoring, and a use can be changed, paused, or retired when the evidence or the risk changes.

## Read alongside

- [Data Governance Framework](../../../about-us/our-teams/data-and-analytics/data-governance-framework.md): the full policy, including the four sensitivity tiers and AI-accountability rules.
- [Data and Analytics](../../../about-us/our-teams/data-and-analytics/index.md): the team that runs the program.
- [Baltimore Intelligence Center](../../products/baltimore-intelligence-center/index.md): the city's governed intelligence and AI product.
