# CitiStat Quality Standards

{{ page_header(summary="The QA bar for every Stat artifact — from raw data to the session itself.", category="QUALITY STANDARDS · AUDIENCE: STAFF", tagline="The standards every Stat product is held to before it leaves the analyst, the Stat lead, and the room.") }}

*Read alongside: OPI CitiStat Method Playbook and OPI CitiStat Templates.*

*The Method Playbook describes the operating system. The Templates page provides the artifacts. This page is the quality bar each artifact must meet.*

## How quality control runs

Quality control runs from raw data through the analytic product to the session itself. Every Stat product has a named lead and a named QCer; the QCer is not the same person who built the work. The lead and the QCer sign off before materials go out.

The standards on this page apply in sequence:

1. **Code and data QC** — checked before any visualization is built.
2. **Visualization and product standards** — applied as the lead builds visuals from QCed data.
3. **Pre-memo quality checklist** — confirmed before the pre-memo is distributed.
4. **Session quality checklist** — observed during and immediately after the session.
5. **Follow-up quality checklist** — confirmed before follow-up materials are issued and as commitments close.

## Code and data QC

QCed before any visualization is built. The QCer fills out this part first.

### Code

- Every business-rule decision is documented in the code or a paired memo, and the document is linked from the deck or pre-memo.

- Code is commented well enough that the QCer can read each section and understand its intent without asking the analyst.

- Code is version-controlled and can be re-run end to end against the source data.

- The QCer ran the code line by line, confirmed each line accomplishes its intent, and confirmed intermediate outputs match the intent. Issues are returned to the lead with line-by-line notes.

### Spreadsheet output and data table

- The output follows the documented business rules.

- Edge cases and outliers have been examined; any unusual values are explained.

- No cells in the final output are unexplained or implausible.

- The output contains the data needed for the final deliverable — nothing missing, nothing extraneous.

## Visualization and product standards

Applied once the data table is QCed and the lead is building visuals.

- The chart type is chosen to answer the question and avoid clutter.

- Scales are inclusive of all data; graphs measuring the same unit on the same page use consistent scales.

- Zero is the baseline unless the data justifies otherwise; the justification is noted.

- Notes and keys live outside the plot area; notes show the current data refresh date.

- Data labels appear on every visualization but do not crowd the visual.

- Markers are present so every data point is visible and distinguishable.

- Numbers of four digits or more use comma separators; gridlines are removed unless they aid reading.

- Business rules and definitions are documented as footnotes or in a glossary on the product.

- The correct CitiStat or Stat-specific logo is used; brand and color usage match the standard.

- If any of the above is missing because of time, the lead names a written iteration plan in the deck or memo.

- External products meet Section 508 accessibility standards (see [Data standards and evidence](method-playbook.md#data-standards-and-evidence) in the Method Playbook).

## Pre-memo quality checklist

- Purpose is clear and written in plain language.

- At least one decision, commitment, or learning objective is explicit.

- Prior commitments are updated with status and evidence.

- KPIs are defined, sourced, and paired with caveats.

- Underlying data and visuals have passed Code and data QC and Visualization and product standards.

- Resident signals, maps, or field validation are included where relevant.

- No budget or policy debate is placed in the room without pre-coordination.

- The right decision-makers, data owners, and central command staff are invited.

- The memo was distributed at least 48 hours before the session.

## Session quality checklist

- Agency voice came first.

- The session focused on 2–3 priority issues rather than a long list of updates.

- Facilitation balanced candor, urgency, and respect.

- Conversation stayed anchored in data, resident impact, root causes, and options.

- Budget and policy issues were captured and routed instead of consuming the session.

- Every commitment had an owner, date, evidence standard, and escalation path.

- Unresolved issues were explicitly kept on the tracker, escalated, or routed to another routine.

## Follow-up quality checklist

- Follow-up memo was issued within two business days.

- Tracker entries are specific enough that a new staff member could understand the commitment.

- Evidence of done is named before the commitment is closed.

- Delayed items have a revised plan, not just a revised date.

- Open items are carried into the next pre-memo.

- Major changes are embedded into SOPs, dashboards, alerts, training, or sustainment plans.

- Public summaries are updated where appropriate.

## See also

- [CitiStat Method Playbook](method-playbook.md) — the operating standards these quality bars enforce.
- [CitiStat Templates](templates.md) — the artifacts these standards apply to.
- [CitiStat — Staff Quick Reference](method-staff-quick-reference.md) — the at-a-glance method companion.
- [CitiStat Method Playbook → Data standards and evidence](method-playbook.md#data-standards-and-evidence) — the data discipline that feeds these checklists.
- [CitiStat Method Playbook → Follow-up, escalation, and sustainment](method-playbook.md#follow-up-escalation-and-sustainment) — what the follow-up checklist supports.
