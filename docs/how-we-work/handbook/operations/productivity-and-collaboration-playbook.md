# Productivity and Collaboration Playbook

{{ page_header(summary="Tools, rituals, and conventions for getting work done together.", category="SERIES · OPI FOUNDATIONS") }}

How OPI works in Microsoft 365 (Outlook, Teams, OneDrive, OneNote, SharePoint, Planner) and Jira. The minimum standards for work that is clear, lasting, and accountable.

## Why this exists

OPI works across performance, data, design, and delivery. We move fast, and we work in settings where the public has to trust the result. This playbook sets the minimum standards for how we communicate, document, plan, and deliver, so our work is easy to find, easy to reuse, and trustworthy when it leaves the building.

### OPI in 10 working norms

Quick reference. Each item is expanded later in this guide.

1.  Use the right tool for the job. Keep a single system of record.

2.  Share links, not attachments. Avoid duplicate “final” versions.

3.  If it is a decision, it gets written down with owner and date.

4.  If it is work, it is tracked in Planner or Jira. No invisible tasks.

5.  No surprises. Surface blockers early with a clear ask.

6.  Meetings produce an agenda, notes, decisions, and action items.

7.  Documents are discoverable. Good titles, dates, owners, and locations.

8.  Sensitive data stays protected. Least privilege, approved storage, no email dumps.

9.  Ship quality. QA before sharing. Peer review for high-stakes artifacts.

10. Close the loop. Confirm completion with evidence and next steps.

## 1. Tool roles and systems of record

Our tools are powerful but only if we use them consistently. The goal is simple: reduce tool sprawl and make it easy to find the truth.

### Three systems of record (non-negotiable)

Three systems hold the truth. Work is tracked in Planner for most staff and in Jira for engineering. Artifacts live in SharePoint document libraries, which hold anything official or shared across the team. Decisions are captured in meeting notes and a simple decision log kept in the project or team space.

### Tool roles matrix

| **Tool**         | **Use it for**                                                                          | **Avoid using it for**                                                       | **System of record?**      |
|------------------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------|----------------------------|
| Outlook          | External communication, scheduling, approvals, formal requests, newsletters.            | Replacing task tracking; sharing sensitive data as attachments.              | No                         |
| Teams (channels) | Team collaboration, quick coordination, updates, meeting chat, persistent topics.       | Final approvals; long-form documentation; storing “final” artifacts in chat. | No                         |
| SharePoint       | Final deliverables, shared working docs, project folders, templates, version history.   | Personal drafts that aren’t ready; storing sensitive data without controls.  | Yes (artifacts)            |
| OneDrive         | Personal working drafts, short-lived files, early-stage content.                        | Team system of record; cross-team deliverables.                              | No                         |
| OneNote          | Meeting notes, agendas, decisions, running logs.                                        | Storing final deliverables that should be in SharePoint.                     | Yes (notes / decisions)    |
| Planner          | Team task boards, ad hoc intake, operational checklists, action items.                  | Complex engineering workflows that belong in Jira.                           | Yes (non-engineering work) |
| Jira             | Engineering epics, stories, bugs, sprint tracking, releases, incidents, technical debt. | Tracking non-engineering work for the whole org unless explicitly agreed.    | Yes (engineering work)     |

The practical rule: drafts can live in OneDrive, but anything you expect others to use or reference moves to the appropriate SharePoint space.

## 2. Document hygiene and sharing

### Minimum standard

- Every official doc has a clear title, date, owner, status (Draft / For Review / Final), and a link to where it lives.

- Share links, not files. Use version history rather than creating duplicates.

- Keep one official copy. Do not keep parallel copies in Teams chat, email attachments, and OneDrive.

### Naming conventions

Use names that sort, scan, and survive context loss. Recommended format: YYYY-MM-DD – Topic – Audience or Project – Status.

- 2026-02-18 – All Staff – Agenda and Notes – Final

- 2026-03-05 – DPW Metrics – Definition Sheet – For Review

- 2026-02 – Snow Ops – Data Pipeline Runbook – Final

### Versioning and “final”

- Prefer SharePoint version history (v1, v2, v3) over “FINAL_FINAL_v7.”

- If a document must be exported (PDF for Council), store the export next to the source doc in SharePoint and link them.

### Sharing and permissions

- Default to People in the organization or named people, not Anyone with the link.

- Grant the minimum access needed (read vs. edit). Time-bound access where possible.

- For sensitive data: do not share via email attachment. Use approved storage and access controls. Ask your manager or the Deputy Chief Data Officer designee if unsure.

## 3. Email standards (Outlook)

### When to use email vs. Teams

Use email for external stakeholders, approvals, formal requests, and anything that has to be forwarded. Use Teams for internal coordination, quick questions, and team updates, and capture any decisions in the system of record.

### Subject line tags

- **\[ACTION\]:** Needs a response or work.

- **\[DECISION\]:** Needs a decision by a date.

- **\[FYI\]:** No reply needed.

- **\[REQUEST\]:** Request for support; include a due date.

- **\[DUE mm/dd\]:** Time bound. Use mm/dd format.

### Email body standard

- Lead with the ask: what you need, by when, and why it matters.

- Provide context in bullets, not paragraphs. Link to the official doc.

- End with next steps and owner.

### Email signature standard

Keep signatures consistent, professional, and accessible. No oversized images.

> *First Last \| Title \| Mayor’s Office of Performance and Innovation (OPI), City of Baltimore \| m: (###) \###-#### \| e: first.last@baltimorecity.gov*

## 4. Teams standards

### Minimum standard

- Use channels for work that should be visible and searchable. Avoid doing real work exclusively in 1:1 chats.

- Summarize decisions in the system of record (notes / decision log) even if first discussed in chat.

- Store shared files in the appropriate SharePoint or Team site, not in ad hoc chat threads.

### Channel hygiene

- One topic per channel where possible (for example, \#requests-intake, \#project-snow-ops, \#announcements).

- Use threaded replies to keep context.

- Avoid @channel unless urgent and relevant to most members.

### Teams meetings and files

- Meeting chat is not a system of record. Copy key decisions and action items into notes.

- If you share a file in Teams, confirm where it is stored. Teams Files are backed by SharePoint, but duplicates happen. Use a single official link.

## 5. Meeting management

### Every meeting must produce

- Agenda. Even a short one.

- Notes. Key points, not a transcript.

- Decisions. What was decided and by whom.

- Action items. Owner, due date, and where the work is tracked.

### Roles for key meetings

- **Facilitator:** Keeps flow and ensures outcomes.

- **Timekeeper:** Protects timeboxes.

- **Notetaker:** Captures decisions and actions.

- **Driver:** Accountable for follow-through after the meeting.

### Calendar hygiene and OOO

- Default to 25 or 50-minute meetings to create transition time.

- Publish agendas 24 hours in advance for recurring meetings where feasible.

- Keep calendars accurate and current. Update meeting titles so they are searchable.

- Add time off to the shared OPI calendar. Add it. Do not email broad distribution lists.

## 6. Project and task management

Work is only manageable if it is visible. We use boards to make work, ownership, and deadlines explicit.

### Minimum standard

- Every deliverable has an owner, a due date, and a definition of done.

- Every ongoing initiative has a single board (Planner or Jira) that reflects the truth.

- Meeting action items are entered into the board within 24 hours.

### Planner (for most OPI work)

- Use buckets that match your workflow (Backlog, Doing, Blocked, Done) or project phases.

- Use labels for priority and work type (Ops, Stakeholder, Deliverable, Risk).

- Use checklists for definition of done (review, QA, approvals, posted).

- Link the source doc in the task description.

### Jira (engineering)

The engineering rule is simple: if there is no ticket, there is no work. Tickets carry acceptance criteria, risk notes, and links to designs and data definitions. The definition of done covers testing, documentation, and deployment and verification steps.

- Use Epics for multi-sprint initiatives and link them to non-engineering artifacts (SharePoint, briefs).

- Use Stories for deliverable work; Bugs for defects; Tasks for technical chores.

- Link PRs, dashboards, runbooks, and deployment notes to the ticket.

- Track incidents with a lightweight post-incident note and follow-up tickets.

### Status updates (one format)

Use the same format across teams to reduce cognitive load.

- **Wins:** 1–3 wins.

- **Next:** Next 2–4 weeks.

- **Risks / Blockers:** With owner and mitigation.

- **Asks:** What you need from leadership or partners.

## 7. Handling ad hoc asks and interrupts

Ad hoc work is the number-one cause of missed deadlines. We manage it like a queue.

### Minimum standard

- Every ad hoc ask is logged within 24 hours in Planner or Jira.

- Triage: accept, decline, or park with a stated reason and next step.

- Tradeoffs are explicit. If a new ask displaces planned work, escalate with options.

- Blockers lasting more than 48 hours are surfaced with a clear ask.

### Recommended intake fields

- Requester and contact.

- What is needed (deliverable).

- Why it matters (impact).

- Due date and time sensitivity.

- Who approves or decides.

- Links to background information.

- OPI owner.

## 8. Data and performance product hygiene

OPI’s data and performance outputs are products. They must be trustworthy, documented, and maintainable.

### KPI and metric hygiene

- Metric definition (plain language and technical definition).

- Owner and update cadence.

- Baseline, target, and timeframe.

- Data source and data quality notes.

- Confidence level (high / medium / low) and known limitations.

### Data product hygiene

- Named product owner and a documented support path.

- Documentation: purpose, schema or fields, refresh schedule, change log.

- QA checks and monitoring where appropriate.

- Access controls aligned to sensitivity.

- Dashboards include definitions and a “last refreshed” timestamp.

- Pipelines have runbooks and an escalation path for failures.

- Avoid distributing extracts via email. Prefer governed access and links.

## 9. Templates

Copy and paste these templates to reduce friction and keep norms consistent.

### Template A: Meeting agenda and notes

- Title format: YYYY-MM-DD – Meeting Name.

- Attendees.

- Purpose.

- Agenda (timeboxed).

- Notes.

- Decisions: Decision \| Date \| Decider.

- Action items: Task \| Owner \| Due date \| Where tracked.

- Links.

### Template B: Decision log

| **Date** | **Decision** | **Context / options** | **Owner** | **Link** |
|----------|--------------|-----------------------|-----------|----------|
|          |              |                       |           |          |
|          |              |                       |           |          |
|          |              |                       |           |          |

### Template C: Status update

- Subject: OPI – \[Team / Project\] – Weekly Status – YYYY-MM-DD.

- Wins.

- Next.

- Risks / Blockers (with asks).

- Decisions needed.

- Links.

### Template D: Ad hoc request

- What you need.

- When you need it.

- Why it matters or what decision it supports.

- Background links.

- Primary contact and approver.

### Template E: Planner task standard

- Title: verb + object (for example, Draft Council memo on X).

- Description: three bullets on scope plus a link to the doc.

- Checklist: QA, review, approval, publish.

- Due date: real deadline, not aspirational.

- Labels: priority, work type.

- Attachments: links only (SharePoint). Avoid file uploads.

### Template F: Jira story standard

- User story or objective.

- Acceptance criteria (testable).

- Dependencies and risks.

- Links: designs, data definitions, runbooks.

- Definition of done: tests, docs, deploy, verification.

### Owner and maintenance

This playbook is a living standard. The Director’s Office owns updates. Propose changes via a tracked request (Planner or Jira) with a brief rationale.
