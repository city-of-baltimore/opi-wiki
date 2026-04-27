# SharePoint Operating System Strategy

<span class="opi-pill approved">Approved</span>

> How OPI uses SharePoint as an internal operating system.

**SERIES · OPI FOUNDATIONS**

**SharePoint Operating**

**System Strategy**

A searchable, governed, and durable knowledge base for OPI. Strategy, metadata taxonomy, and Project Directory schema.

**AUDIENCE** OPI staff, site stewards, service leads

**OWNER** Chief of Staff (Site Steward) · DCDO (Taxonomy)

**VERSION** v1.0 · February 22, 2026

**■ Goal and design intent**

Build a SharePoint-based operating system for OPI that is easy to use on day one, rigorous enough for production work, and durable enough to survive staffing and leadership changes.

This is not a file dump. It is a living operating manual with clear ownership, standards, and searchability. The design should feel disciplined and polished: simple at the top, deep underneath, with explicit decision rights and measurable expectations.

> *Respond when necessary. Build so we do not have to respond again.*

**Design principles**

- Simple top-level navigation. Depth comes from consistent subpages, not more tabs.

- One source of truth for every “what, who, when.” No shadow guidance in chats or personal folders.

- Pages for guidance. Documents for controlled artifacts. Lists for systems of record.

- Plain language. Assume a smart reader who is new to city government.

- Operational specificity wins. Names, cadences, SLAs, owners, and a definition of done.

- Governance is the product. Every page has an owner and a review cadence, or it does not exist.

**What SharePoint does for OPI**

- **Knowledge base:** How OPI works, written down, current, and easy to find.

- **Operating system:** A few systems of record (lists) that answer: what are we doing, who owns it, what decisions are needed, what is the status.

- **Enablement:** Templates, how-tos, and standards that make good work repeatable across teams and agencies.

**■ Information architecture**

Top-level navigation has five pillars. This is the entire navigation surface. Anything else lives one level down.

| **Top-level pillar**      | **What lives here**                                                                                             |
|---------------------------|-----------------------------------------------------------------------------------------------------------------|
| About OPI                 | Mandate, teams, programs, services, and what we are and are not.                                                |
| How We Deliver            | Operating model (intake → charter → deliver → sustain), cadences, decision forums, escalation.                  |
| Playbooks and Methods     | How we do the work: CitiStat, delivery activations, data governance, human-centered design, responsible AI.     |
| Tools and Systems         | City systems 101 plus OPI tooling plus engineering and data platform standards (Git, CI/CD, secrets, runbooks). |
| Operations and Governance | Norms, policies, HR/IT/procurement how-tos, templates, change control, archives.                                |

Persistent utility links sit in the top right corner: Directory, Project Directory, Templates, Change Log, Start Here. Small, consistent, high-value.

**Page types and where content belongs**

| **Content type**   | **Use it for**                                                                        | **Example**                                | **Rules**                                                        |
|--------------------|---------------------------------------------------------------------------------------|--------------------------------------------|------------------------------------------------------------------|
| SharePoint pages   | Living guidance that needs to be read and searched.                                   | How to run a delivery room.                | Owned page; quarterly review; plain language; link to artifacts. |
| Document libraries | Controlled artifacts and templates that require versioning.                           | Charter template; KPI dictionary template. | Versioned; changes logged; avoid duplicates.                     |
| Lists              | Systems of record: structured data that must be sortable, filterable, and reportable. | Project Directory; People Directory.       | Required fields; weekly updates; named owners.                   |
| Folders            | Organizing supporting files inside a project space.                                   | Meeting attachments.                       | Not a system of record. Never store “truth” only in files.       |

**Governance: keep it sharp**

A SharePoint wiki fails when ownership is vague. Governance is non-negotiable.

- **Every page:** Owner, last-reviewed date, next-review date, and a short change log.

- **Every list:** Data owner, update cadence, validation rules, and a single “how to use this list” page.

- **Every template:** Version number, owner, change notes, and an approved usage context.

**Governance roles**

| **Role**                                | **What they own**                                                     |
|-----------------------------------------|-----------------------------------------------------------------------|
| Site Steward (CoS)                      | Structure, navigation, standards, and change control.                 |
| Taxonomy Owner (DCDO + CoS)             | Term sets, data sensitivity labels, and metadata rules.               |
| Service Owners (DCPO, DCDO, Innovation) | Content owners for service playbooks and standards.                   |
| Ops Librarian (PMO / AdminOps)          | Audits broken links, archives snapshots, enforces naming conventions. |

**■ Implementation approach**

Build in three releases so the system is useful immediately and improves with use.

**MVP — first 2 weeks**

- Site structure with the five-pillar navigation.

- Project Directory list with required fields, validation rules, and standard views.

- People and Contacts Directory list.

- Templates and Controlled Artifacts library, seeded with charter, decision memo, KPI definition, and QA templates.

- Start Here page for new hires with the first-week reading path.

- Change Log page with a named site steward.

**V1 — 30 to 45 days**

- Service playbooks and How We Deliver cadence pages (intake, chartering, sustainment).

- Engineering standards under Tools and Systems (Git workflow, CI/CD, secrets, runbooks).

- City Systems 101 pages (311, permitting, Workday, payments, Granicus, Open Baltimore).

- Systems of Record map and named owners for each system or dataset.

- 60-minute staff training: how to use the Project Directory, how to tag, where artifacts live.

- First quarterly audit and archive snapshot.

**V2 — quarterly**

- Expand systems-of-record lists.

- Add dashboards and additional views.

- Harden governance with audits, term updates, and archives.

**■ Metadata taxonomy**

Make OPI’s work findable, governable, and reportable without making people fill out a bureaucracy. The design goal is the minimum effective metadata: a small set of tags that unlocks search, filtering, ownership clarity, and risk management.

**Principles**

- Metadata is a contract. If a field is required, it must be accurate and current.

- Prefer controlled vocabularies (managed metadata) wherever people will filter or search.

- Use people-picker fields for who owns what, and metadata fields for what it is.

- Treat data sensitivity and production readiness as first-class fields, not footnotes.

- Limit required fields to what OPI will actually use in reviews, dashboards, and decisions.

**Core term sets (managed metadata)**

| **Term set**         | **Definition**                                                   | **Example values**                                                                                             | **Owner**           |
|----------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|---------------------|
| Service line         | Which OPI service owns the work.                                 | Citywide Performance Management; Citywide Data and Analytics; Innovation Lab; Cross-Agency Delivery; AdminOps. | CoS + service leads |
| Program              | Named recurring program, run year after year.                    | CitiStat; Tiger Teams; Open Data; Innovation Lab; Data and AI Platform.                                        | CoS + DCPO / DCDO   |
| Agency               | Primary agency partner(s) involved.                              | DPW; DOT; DHCD; BPD; Fire; Finance; BCIT.                                                                      | CoS + AdminOps      |
| Work type            | What kind of artifact or work product this is.                   | Decision memo; Charter; KPI definition; Dashboard; Dataset; Runbook; Training.                                 | CoS + DCDO          |
| Lifecycle phase      | Where work sits in the standard lifecycle.                       | Intake; Charter; Discovery; Build; Pilot; Scale; Sustain; Closed; Parked.                                      | PMO / AdminOps      |
| Priority level       | How urgent or important the work is relative to capacity.        | P0 (Mayoral / CA); P1 (service reliability); P2 (enablement); P3 (nice-to-have).                               | CoS + CA liaison    |
| Sensitivity          | How broadly this can be shared.                                  | Public; Internal; Restricted (PII); Confidential (legal / personnel).                                          | DCDO (policy)       |
| Production readiness | How safe it is to treat this as “real” in production.            | Prototype; Pilot; Production; Deprecated.                                                                      | DCDO (technical)    |
| Service area         | Resident-facing service domain.                                  | 311; Permitting; Trash collection; Street sweeping; Code enforcement; Forestry.                                | Service leads       |
| Equity lens          | Whether and how equity considerations are relevant and included. | Required; Not applicable; In progress.                                                                         | DCPO                |

**Required metadata by content type**

| **Content**                    | **Required fields**                                                                                                       | **Optional fields**                                                   | **Notes**                                                          |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|--------------------------------------------------------------------|
| SharePoint page                | Owner; Service line; Last reviewed; Next review.                                                                          | Program; Audience.                                                    | Pages are guidance. They must be owned and reviewed.               |
| Document (template / artifact) | Work type; Service line; Owner; Version; Sensitivity.                                                                     | Program; Agency; Production readiness.                                | Templates and policy docs must be versioned and logged.            |
| Project Directory item         | Project name; Service line; Agency; OPI Owner; Sponsor; Authorizer; Lifecycle phase; Priority; RAG; Next checkpoint date. | Program; Service area; Decision needed by; Dependencies; Equity lens. | If it can’t be described in these fields, it isn’t ready to start. |
| People Directory item          | Person; Team; Role; What to contact for.                                                                                  | Skills; Programs; Backup coverage.                                    | Directory reduces “who owns this?” churn.                          |

**Naming conventions**

Naming conventions are not cosmetic. They are what makes search work for new hires and partners.

- Verb-led page titles such as “How to,” “Run,” “Publish.” Avoid internal acronyms in titles.

- Memos and decision records use YYYY-MM-DD – Topic – Decision / Brief.

- Templates are named “Template – \[Artifact\] – vX.Y” with owner and last updated date in the page header.

- Projects are named “Service area – Outcome – Agency.”

**Taxonomy governance and change control**

- Single request path: a SharePoint list form for “Request a new tag or term,” reviewed weekly by Ops Librarian.

- Monthly taxonomy review (30 minutes): CoS + DCDO + PMO. Approve new terms, retire unused terms.

- Quarterly audit: missing required fields, inconsistent tags, stale pages past review date.

- Sensitivity labels and production-readiness definitions are policy-controlled by DCDO. Changes require a written note.

**■ Project Directory schema**

A single, trusted portfolio record that answers, at any moment, what are we doing, who owns it, what decisions are needed, and what “done” means. This is the backbone of OPI’s book of business.

**Design principles**

- One list is the portfolio truth. Do not run parallel trackers in decks, DMs, or personal files.

- The list is decision-oriented, not activity-oriented. It surfaces decisions, risks, and next checkpoints.

- Required fields are minimal and enforce clarity at intake. No charter, no work.

- People fields create accountability. Metadata fields enable sorting, filtering, and reporting.

- Every project links to its artifacts (charter, decision memos, KPI pack, runbooks).

**Data model**

- **List:** Project Directory (portfolio record).

- **List:** People and Contacts Directory.

- **Library:** Templates and Controlled Artifacts.

- **Library:** Project Working Files (attachments, working docs).

Optional, add when ready:

- Systems and Platforms (systems of record, ownership, production readiness).

- Decisions / Decision Records.

- Risks and Issues log.

**Project Directory — fields (required at intake in bold)**

| **Field**                | **Type**                  | **Required** | **Definition / standard**                                                                                                     |
|--------------------------|---------------------------|--------------|-------------------------------------------------------------------------------------------------------------------------------|
| **Project ID**           | Single-line text (unique) | Yes (auto)   | Stable identifier (e.g., OPI-2026-001). Auto-generate via Power Automate; never reuse.                                        |
| **Project name**         | Single-line text          | Yes          | Plain-language name: Service area – outcome – agency. Avoid internal acronyms.                                                |
| **Service line**         | Managed metadata          | Yes          | OPI service owner. Used for routing and views.                                                                                |
| Program                  | Managed metadata          | No           | If part of a named program. Examples: CitiStat, Tiger Teams, Innovation Lab.                                                  |
| **Agency (primary)**     | Managed metadata          | Yes          | Primary agency partner. Allow multi-select for cross-agency work.                                                             |
| Service area             | Managed metadata          | No           | Resident-facing domain. Examples: 311, permitting.                                                                            |
| **OPI Owner**            | Person                    | Yes          | Accountable OPI lead. Updates weekly.                                                                                         |
| **Agency sponsor**       | Person                    | Yes          | Accountable agency leader (or designee) who can make decisions. If missing, work is not accepted.                             |
| **Authorizer**           | Person                    | Yes          | Senior responsible owner with authority to resolve cross-agency blockers. Often CA or Deputy. Required for cross-agency work. |
| **Lifecycle phase**      | Choice / managed metadata | Yes          | Intake; Charter; Discovery; Build; Pilot; Scale; Sustain; Closed; Parked.                                                     |
| **Priority level**       | Choice                    | Yes          | P0 (Mayoral / CA); P1 (service reliability); P2 (enablement); P3 (nice-to-have).                                              |
| **RAG status**           | Choice                    | Yes          | Green = on track; Amber = risk; Red = off track / blocked. Must include blocker / ask when Amber or Red.                      |
| **Next checkpoint date** | Date                      | Yes          | Next date the owner will update status or bring the project to review. Default = next weekly ops review.                      |
| Decision needed          | Multi-line text           | No           | Plain-language decision request, if any. Format: “We need X by date Y.”                                                       |
| Decision needed by       | Date                      | No           | Deadline for the decision to avoid delay. If blank, assume no decision needed.                                                |
| **Problem statement**    | Multi-line text           | Yes          | 1–3 sentences: what is failing and who feels it. Not a diagnosis essay.                                                       |
| **Outcome statement**    | Multi-line text           | Yes          | What will be measurably better. Start with “Reduce” / “Increase.”                                                             |
| **Primary KPI(s)**       | Single line + hyperlink   | Yes          | KPI names plus a link to the KPI dictionary or dashboard. If undefined, it is a red flag.                                     |
| Equity lens              | Choice                    | No           | Required; Not applicable; In progress. DCPO standard.                                                                         |
| **Start date**           | Date                      | Yes          | When work formally starts (charter approved).                                                                                 |
| Target end date          | Date                      | No           | Expected completion date. Use for time-boxing and gating.                                                                     |
| Dependencies             | Multi-line text           | No           | Known dependencies (policy, procurement, BCIT, data access). List owners next to dependencies.                                |
| Risks / blockers         | Multi-line text           | No           | What could stop this work. Required when Amber or Red.                                                                        |
| Artifacts (links)        | Hyperlink                 | No           | Charter, decision memo, runbook, etc. Use a project hub page as the landing link.                                             |
| Teams channel link       | Hyperlink                 | No           | Working channel for async collaboration. Prevents email sprawl.                                                               |
| Production readiness     | Choice                    | No           | Prototype; Pilot; Production; Deprecated. Required for tools and data products.                                               |
| Sensitivity              | Choice                    | No           | Public; Internal; Restricted; Confidential. Required for data-related projects.                                               |
| Public narrative status  | Choice                    | No           | Not public; Eligible; Drafting; Published. Feeds the Our Work storytelling pipeline.                                          |
| Last updated             | Date / time               | System       | Auto-populated by SharePoint. Used for reminder automation.                                                                   |

**Validation rules (the quality bar for the list)**

- If Lifecycle phase is not “Closed” or “Parked,” Next checkpoint date is required and must be within 30 days.

- If RAG is Amber or Red, Risks / blockers and Decision needed by (or a stated mitigation) must be filled.

- If Program = CitiStat or Tiger Teams, Service area and Primary KPI(s) are required.

- If Production readiness is Pilot or Production, runbook link and Tech Lead are required.

**Standard views**

- Portfolio — Active (all non-closed, non-parked).

- By Service line (Performance / Data / Innovation / Delivery / AdminOps).

- Decisions needed in the next 14 days.

- At-risk (Amber / Red) with blockers and authorizers.

- Upcoming checkpoints (next 7 days).

- By Agency (useful for agency leader check-ins).

- Public narrative pipeline (Eligible / Drafting / Published).

- Production items (Pilot / Production only) for reliability and incident readiness.

**Cadence and accountability**

- **Weekly:** Project owners update by a set deadline (e.g., Monday 12:00).

- **Weekly:** Ops Review run by CoS / PMO uses “Decisions needed” and “At-risk” views; closes the loop on asks.

- **Monthly:** DCPO and DCDO review service-line views against roadmaps and Stat schedules.

- **Quarterly:** Archive snapshot (PDF export) for institutional memory and audits.

**Automations (high leverage)**

- Reminder: if a project has not been updated in 7 days and is Active, notify Owner and copy PMO.

- Digest: weekly email or Teams post with “Decisions needed in 14 days” and “Red items.”

- Project kickoff: when Lifecycle phase moves to Charter, auto-create a project folder (or document set) and a project hub page from template.

**■ People and Contacts Directory**

A directory list makes tagging practical. It bridges “who owns this?” with “who can help?”

| **Field**           | **Type**         | **Required** | **Definition**                                                                               |
|---------------------|------------------|--------------|----------------------------------------------------------------------------------------------|
| Person              | Person           | Yes          | Primary identifier.                                                                          |
| OPI team            | Choice / managed | Yes          | Director’s Office; Performance and CitiStat; Data and Analytics; Innovation Lab; AdminOps.   |
| Role title          | Single line      | Yes          | Formal role (what HR calls it).                                                              |
| What to contact for | Managed (multi)  | Yes          | Practical routing tags such as “CitiStat memos,” “Data access,” “Open Baltimore publishing.” |
| Focus areas         | Managed (multi)  | No           | Service domains (311, permitting, sanitation, etc.).                                         |
| Backup / coverage   | Person           | No           | Who covers when OOO.                                                                         |
| Preferred channel   | Choice           | No           | Teams / email / phone for urgent matters.                                                    |
| Notes               | Multi-line text  | No           | Short, practical notes. Avoid personal information.                                          |

**■ Site governance — minimum rules**

- No new top-level navigation items without CoS approval.

- Every new page uses the standard page template (owner, review dates, links to artifacts).

- Every new template lives in the Templates library and is versioned.

- Quarterly archive snapshot of key pages and a Project Directory export.

- Delete or archive obsolete guidance. If it is wrong, it cannot remain “for reference.”

**■ Project hub page — standard template**

Every active project has a simple hub page linked from the Project Directory.

- One-paragraph summary (problem + outcome).

- Owners and contacts (OPI Owner, Agency Sponsor, Authorizer, Tech Lead).

- Primary KPI(s) plus baseline / target links.

- Current status (RAG + next checkpoint + decisions needed).

- Artifacts (charter, decision memos, runbooks, dashboards).

- Timeline (start, target end, key milestones).

- Sustain plan (who owns it after OPI; what routine keeps it alive).

**■ Quick reference for staff**

> *If you only remember one thing: tag the work so someone new can find it and understand who owns it.*

- **Pages:** Owner + Service line + Review dates.

- **Projects:** Owner + Agency + Authorizer + Phase + Priority + RAG + Next checkpoint.

- **Tools / data products:** Production readiness + Sensitivity + Runbook link.
