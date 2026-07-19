# Wiki Knowledge Base Structure

{{ page_header(summary="How OPI organizes its internal SharePoint knowledge base — a separate system from this public site.", category="SERIES · OPI FOUNDATIONS", tagline="Structure, governance, and what each pillar must contain.") }}

!!! note "Two different systems"
    This page documents OPI's **internal SharePoint knowledge base**, the
    staff-only operating home for project records, directories, and controlled
    templates. It does **not** describe this public site.

    **This public site (OPI Foundations)** is a MkDocs site organized into four
    sections (About Us, How We Work, What We Do, and Resources) and
    published openly. The internal SharePoint KB described below is where the
    non-public, day-to-day operating records live. The two use different
    top-level labels on purpose (for example, this site's **How We Work**
    corresponds to the internal KB's **How We Deliver** pillar).

How OPI organizes its internal knowledge so staff can find what they need, trust what they find, and rely on it surviving turnover.

## Why the Wiki exists

The OPI Wiki is the single internal home for the way OPI works: mission, model, methods, templates, and active project records. It is not a file dump. It is a maintained operating manual with named owners, review cadences, and a quality bar. The goal: anyone joining OPI can find the official document, the right template, the active project list, and the owner of each, in under five minutes.

### Three jobs of the Wiki

**Find.** Surface the official document, person, or routine the user needs, fast.

**Trust.** Make it obvious which documents are current, who owns them, and when they were last reviewed.

**Survive.** Outlast turnover. The Wiki is a record of how OPI works, not how any one person works.

## Platform and scope

OPI uses Microsoft SharePoint as the wiki platform, consistent with the rest of City government. SharePoint provides pages for living guidance, document libraries for controlled artifacts, and lists for systems of record (project directory, people directory, change log). Other tools (Teams chats, OneDrive, personal folders) are not the system of record. That is policy.

### What lives in the Wiki

- The official OPI Foundations documents (this set), in their final approved form.

- Service playbooks and methods (CitiStat, data governance, Innovation Lab methods, Tiger Teams).

- Templates (charter, problem statement, intake form, pre-read, after-action review).

- Project Directory — the live list of every active and recent OPI project.

- People and Contacts Directory — OPI staff, agency liaisons, and key partners.

- Change Log — what was added, updated, or retired in the last 90 days.

### What does not live in the Wiki

- Personally identifiable information about residents.

- Live HR or compensation data — owned in Workday and HR systems.

- Sensitive operational drafts — stored in restricted Leadership space, not the open Wiki.

- Working chat threads — those live in Teams; only decisions and outcomes flow into the Wiki.

## Top-level navigation

The internal SharePoint KB uses six top-level pillars. Depth comes from consistent subpages, not from adding more tabs. Every pillar has a named owner.

| **Pillar**                   | **What lives here**                                                                                 | **Owner**         |
|------------------------------|-----------------------------------------------------------------------------------------------------|-------------------|
| About OPI                    | Mission, north star, portfolios, services, leadership, organization chart, what we are and are not. | Director’s Office |
| How We Deliver               | Operating model, intake, charters, decision forums, escalation, governance cadences.                | Chief of Staff    |
| Playbooks and Methods        | CitiStat, Innovation Lab methods, Tiger Teams, data governance, responsible AI.                     | Portfolio leads   |
| Tools and Systems            | City systems 101, OPI tooling, engineering and data platform standards.                             | Deputy CDO        |
| Operations and Governance    | Policies, telework, productivity playbook, HR and IT how-tos, QA standards, change control.         | Chief of Staff    |
| People and Project Directory | People directory, Project Directory list, agency liaisons, contact lookup.                          | Chief of Staff    |

### Persistent utility links (top of every page)

- Start Here — new hire onboarding hub.

- Directory — people and contacts.

- Project Directory — active project list.

- Templates — controlled library.

- Change Log — what is new and updated.

## What each pillar must contain

### About OPI

- OPI in one paragraph (mission, north star, who we report to).

- Portfolios and services — the four teams and five services, with leads.

- Organization chart (current).

- Leadership team — photos, titles, two-line bios.

- What OPI does and does not do (scope and boundaries).

### How We Deliver

- Operating Model — staff version (this set, doc 27).

- Intake SOP — the single front door process.

- Charter and Problem Statement templates.

- Decision forums and cadences (weekly ops, monthly portfolio, quarterly review).

- Escalation paths — who decides what, with timeboxes.

### Playbooks and Methods

- CitiStat Method Playbook — staff and agency version (this set, doc 28).

- Tiger Teams Playbook (this set, doc 30).

- Innovation Lab methods — discovery, prototyping, sustain.

- Data governance and KPI Dictionary standards.

- Responsible AI readiness — use-case intake and review process.

### Tools and Systems

- City systems 101 — 311, Accela, Workday, BCIT supported tooling.

- OPI productivity stack — M365, Teams, Planner, Jira (see Productivity Playbook).

- Engineering and data platform standards — source control, CI/CD, secrets, runbooks.

- Data and analytics tools — warehouse, BI, open data publishing.

### Operations and Governance

- Telework Policy and Productivity Playbook (this set, Wave 2).

- Leadership Norms and Performance Standards (this set, Wave 2).

- Onboarding and Offboarding processes (this set, Wave 1).

- QA Standards (this set, Wave 2), and the SharePoint operating-system standards maintained in the internal KB.

- Equity, accessibility, and privacy standards.

### People and Project Directory

- People Directory — every OPI staff member, role, portfolio, contact.

- Project Directory — every active and recent OPI project, with owner, status, sponsor, and last update.

- Agency Liaisons — named partners at every City agency we work with.

- Position Descriptions Index (this set, doc 31).

## Page types — what to use, when

Every Wiki contributor must know which content type to use. Mismatch is the leading cause of drift.

| **Type**         | **Use it for**                                                      | **Examples**                                  |
|------------------|---------------------------------------------------------------------|-----------------------------------------------|
| SharePoint page  | Living guidance that needs to be read and searched.                 | How to run a Stat session; charter standards. |
| Document library | Controlled artifacts and templates that need versioning.            | Charter template; KPI Dictionary template.    |
| List             | Systems of record — structured, sortable, filterable, reportable.   | Project Directory; People Directory.          |
| Folder           | Supporting files inside a project space; never the official record. | Meeting attachments inside a project hub.     |

## Metadata — minimum effective tagging

Every Wiki page and every controlled artifact carries a small set of tags so the Wiki stays findable and governable. The principle: minimum effective metadata. Required fields must be accurate; everything else is optional.

| **Field**           | **Required** | **Notes**                                                  |
|---------------------|--------------|------------------------------------------------------------|
| Title               | Yes          | Plain language, no acronyms unless universally understood. |
| Owner               | Yes          | A named OPI staff role (not a person’s name alone).        |
| Service / Portfolio | Yes          | Tag to one of the five services or four teams.        |
| Last reviewed       | Yes          | Quarterly review minimum; flagged red after 6 months.      |
| Next review         | Yes          | Date when the next review is due.                          |
| Status              | Yes          | Draft · Active · Retired · Archived.                       |
| Sensitivity         | Yes          | Public · Internal · Restricted.                            |
| Change log          | Yes          | A short note of what changed in the last update.           |

## Governance — keep it sharp

### Roles

**Site steward (Chief of Staff).** Owns navigation, standards, change control, and the overall structure.

**Taxonomy owner (DCDO with Chief of Staff).** Owns term sets, sensitivity labels, and metadata rules.

**Service owners (DCPO, DCDO, Innovation Lab lead).** Own content for their service playbooks and standards.

**Ops librarian (AdminOps).** Audits broken links, archives stale content, enforces naming conventions.

### Cadence

- Weekly: ops librarian sweeps for broken links and stale items in active spaces.

- Monthly: each team lead reviews their playbooks and methods pages.

- Quarterly: every page owner confirms or updates the page; site steward publishes a Change Log digest.

- Annually: site steward leads a full taxonomy and IA review.

### Quality bar

- Every page has an owner, a review date, and a change log.

- Every list has an update cadence, validation rules, and a single "how to use this list" page.

- Every template has a version, an owner, change notes, and an approved usage context.

- Stale content (no review for 6+ months) is flagged red and reviewed or retired.

## Implementation — three releases

The Wiki is built in three releases so it is useful on day one and improves with use.

**MVP (2 weeks).** Top-level structure, Project Directory, People Directory, Templates library, Start Here, Change Log. Linked from the OPI Foundations document set.

**V1 (30 to 45 days).** Service playbooks, methods pages, City systems 101, engineering standards, full Foundations set published in final approved form.

**V2 (quarterly).** Expand systems-of-record lists, add dashboards and views, harden governance (audits, term updates, archive policy).

## Access and sensitivity

- **Default open:** Most of the Wiki is open to all OPI staff. Defaulting to open is intentional.

- **Leadership space:** A small Leadership space holds sensitive operational documents (recruitment trackers, draft personnel actions, equity assessment drafts, and partner due-diligence notes).

- **Partner space:** Some agency-shared spaces are joint with our partners; access is granted by named role.

- **No resident PII:** Resident PII does not live in SharePoint. Operational data with PII lives in the system of record (for example, Workday, BCIT-managed systems).

## Rollout to staff

- All-hands launch with a 20-minute walkthrough: where to find what, how to contribute, how to flag stale content.

- Every new hire is added to a Wiki orientation in the first week.

- Every recurring meeting (weekly ops, portfolio reviews, Stat) starts the year with the Wiki location for its agenda, pre-read, and follow-up.

- Quarterly demo at all-hands: what was added or changed, what is being retired.

## Method pages as sources of truth

Method pages should define how OPI works, not just describe past work. When a method page is created or updated, it should answer:

1. What routine is this?
2. When should staff use it?
3. When should staff not use it?
4. Who authorizes it?
5. Who runs it day to day?
6. What artifacts are required?
7. What is the handoff or sustainment path?
8. What public or internal language should other pages reuse?

If a page introduces a new term, update the glossary in the same PR. If a page changes a method, update the relevant template or playbook in the same PR.
