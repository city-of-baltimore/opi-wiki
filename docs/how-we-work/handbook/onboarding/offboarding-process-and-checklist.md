# Offboarding Process and Checklist

{{ page_header(summary="How we handle transitions, knowledge handoff, and access changes.", category="SERIES · OPI FOUNDATIONS") }}

Protecting continuity, security, and OPI’s credibility through humane, predictable transitions.

## Principles

- **No surprises:** Leaders and key partners know the transition plan early.

- **Continuity by design:** Work is easy to pick up because documentation is current.

- **Security and privacy:** Access is removed on time and sensitive data is handled correctly.

- **Respectful transitions:** Clear expectations, predictable steps, and professional closure.

> *Offboarding is how we protect the trust we built during onboarding.*

## When notice is received (Day 0 – Day 2)

| **When** | **Task**                                                                                   | **Owner**                   | **How**                                                                    |
|----------|--------------------------------------------------------------------------------------------|-----------------------------|----------------------------------------------------------------------------|
| Day 0–2  | Confirm separation date and transition approach (internal transfer or vacancy).            | Manager + Director’s Office | Align on stakeholder communication and continuity owner.                   |
| Day 0–2  | Create an offboarding plan in SharePoint (handoff document, timeline, owners).             | Manager                     | Use the Handoff Pack template. Link in the relevant Planner or Jira board. |
| Day 0–2  | Identify critical work at risk: commitments, deadlines, meetings, dependencies.            | Departing staff + Manager   | Surface risks early. Propose options: re-scope, reassign, or pause.        |
| Day 0–2  | Initiate AdminOps and IT tickets for access removal, mailbox delegation, equipment return. | AdminOps + Manager          | Coordinate with BCIT and building admin. Document ticket numbers.          |

## Two weeks before last day

Or immediately, if shorter notice.

| **When**  | **Task**                                                                                          | **Owner**                 | **How**                                                                |
|-----------|---------------------------------------------------------------------------------------------------|---------------------------|------------------------------------------------------------------------|
| T-10 days | Complete the Handoff Pack: work in progress, next steps, key links, stakeholders, decisions.      | Departing staff           | Store in SharePoint. Make sure everything is discoverable and current. |
| T-10 days | Transfer ownership of work items: Planner tasks, Jira tickets, shared mailboxes, calendars.       | Departing staff + Manager | Reassign owners. Add context in ticket descriptions.                   |
| T-10 days | Update documentation: runbooks, decision logs, KPI definitions, data dictionaries, meeting notes. | Departing staff           | Anything that lives in your head must be written down.                 |
| T-10 days | Schedule knowledge transfer sessions with the continuity owner.                                   | Departing staff + Manager | Record decisions. Focus on pitfalls and watch-outs.                    |
| T-7 days  | Draft a stakeholder communications plan (internal and agency partners, where appropriate).        | Manager + Departing staff | Keep messaging aligned. Avoid over-promising post-departure support.   |

## Last week

| **When** | **Task**                                                                                     | **Owner**            | **How**                                                              |
|----------|----------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------|
| T-5 days | Finalize transition of meeting ownership (recurring invites, agendas, notes locations).      | Departing staff      | Update meeting series owners. Link notes locations.                  |
| T-3 days | Confirm access removals are scheduled and identify shared credentials that require rotation. | Manager + IT         | Rotate secrets and tokens where relevant, especially in engineering. |
| T-3 days | Close out open work where possible. Document what is paused and why.                         | Departing staff      | Update boards so work is legible.                                    |
| T-2 days | Complete exit interview and feedback (if applicable).                                        | Departing staff + HR | Capture suggestions to improve onboarding and systems.               |

## Last day

| **When** | **Task**                                                                                               | **Owner**                  | **How**                                                               |
|----------|--------------------------------------------------------------------------------------------------------|----------------------------|-----------------------------------------------------------------------|
| Last day | Return equipment (laptop, peripherals, keys, badge) and confirm receipt.                               | Departing staff + AdminOps | Follow City guidance. Document chain of custody for devices.          |
| Last day | Set Out-of-Office message with routing instructions. Remove yourself from critical distribution lists. | Departing staff            | Include the continuity owner and the shared mailbox where applicable. |
| Last day | Final transition check: Handoff Pack complete, owners assigned, stakeholders informed.                 | Manager + Departing staff  | Manager confirms all critical items have a named owner.               |

## After departure

| **When**    | **Task**                                                                                          | **Owner**          | **How**                                                           |
|-------------|---------------------------------------------------------------------------------------------------|--------------------|-------------------------------------------------------------------|
| +1 day      | Disable accounts and remove access (Teams, SharePoint, Jira, Azure DevOps, GitHub).               | IT + AdminOps      | Confirm no shared links remain open.                              |
| +1 – 7 days | Remove from Active Directory groups and distribution lists. Revoke building access.               | IT + AdminOps      | Coordinate with BCIT and building administration.                 |
| +7 days     | Archive or reassign files in OneDrive. Ensure SharePoint is the system of record.                 | Manager + AdminOps | Avoid knowledge loss. Copy necessary work products to SharePoint. |
| +14 days    | Confirm continuity is stable: no orphaned projects, missing credentials, or unclear stakeholders. | Manager            | Use a brief after-action to improve the offboarding process.      |

## Portfolio-specific add-ons

### Director's Office

Ensure portfolio visibility and decision support artifacts remain current and owned.

- T-10 days: transfer ownership of operating cadences (Ops Review, Portfolio Council, status reporting).

- T-10 days: ensure SharePoint governance responsibilities are reassigned (taxonomy, permissions, archives).

- T-5 days: finalize any public or executive artifacts in flight (QA complete, sources linked, version history intact).

### Performance

Protect continuity of performance routines, Stat preparation, and agency relationships.

- T-10 days: transfer ownership of Stat calendars, pre-read folders, memo templates, and follow-up trackers.

- T-10 days: document key agency relationships — contacts, sensitivities, open commitments, next decision points.

- T-7 days: ensure KPI Dictionary updates are complete. Avoid orphaned metric definitions and stale dashboards.

### Data and Analytics

Prevent security and reliability risks. Rotate credentials, reassign repos and pipelines, and keep runbooks current.

- T-10 days: transfer ownership of repos, Azure DevOps pipelines, and Jira epics. Ensure bus-factor documentation.

- T-7 days: rotate secrets, tokens, service accounts, and shared credentials tied to the departing staff member.

- T-7 days: update on-call and incident response coverage. Ensure paging and alerts do not route to departing staff.

- T-5 days: confirm data access and permission groups are adjusted. No personal accounts remain in production workflows.

### Innovation Lab

Protect engagement continuity and design artifact integrity.

- T-10 days: transfer ownership of active discovery and prototype workstreams to the continuity owner.

- T-10 days: update partner and stakeholder relationship logs. Note open commitments and sensitive context.

- T-7 days: ensure design files, research notes, and prototypes are stored in SharePoint with current metadata.

- T-5 days: hand off any external partner relationships (universities, philanthropy, civic tech) to the Innovation Program Manager or the Data Storyteller.

### Manager responsibilities (all portfolios)

- Day 0–2: clarify communications — who needs to know, when, and what will be shared.

- T-10 days: re-plan commitments. Reassign owners, re-scope, or formally pause work.

- T-7 days: confirm HR and Workday steps (supervisory org changes, manager assignments, role backfills).

- Post-departure: conduct a lightweight after-action review. Capture learnings in templates and processes.

## Appendix. Handoff Pack template

Create a SharePoint document titled: \[LastName\] — Handoff Pack — \[Role\] — \[YYYY-MM-DD\]. The template has eight sections.

1.  Work summary — what I owned and what I contributed to.

2.  Current status — what is done, what is in progress, what is blocked.

3.  Next 30 days — critical deadlines, meetings, decisions.

4.  Key stakeholders and relationships — internal and agency partners.

5.  Key links — SharePoint folders, Planner plans, Jira boards, dashboards, repos.

6.  Risks and watch-outs — what can go wrong, early warning signals.

7.  Decisions and rationale — what we decided and why.

8.  Open questions and recommendations.
