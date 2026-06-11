<!--
Internal note. Not published to the wiki.
This file lives outside docs/ so MkDocs does not include it in the build.
-->

# Wiki Quality Review — April 2026

> Editorial, terminology, and information architecture review of the OPI Foundations wiki.

**OPI · REFERENCE**

**Wiki Quality Review and Recommendations**

*Focused on Bloomberg Cities + Harvard Kennedy School-quality clarity, consistency, and usability.*

## 1. Executive summary

The OPI Foundations wiki is already a strong operating reference. It has a coherent MkDocs structure, local navigation, reusable card grids, page badges, strong glossary discipline, and a clear effort to make OPI’s operating model durable rather than personality-dependent.

The highest-priority issue is terminology consistency. The wiki explains the right concepts, but several concepts are repeated from different angles: Innovation Lab, Cross-Agency Delivery, Tiger Teams, CitiStat, delivery review, and sustainment. New readers may understand each page individually but miss how the system fits together.

The recommended fix is not a broad rewrite. It is a small set of canonical language updates:

1. Add a single “How Work Moves Through OPI” explainer.
2. Make the Innovation Lab / Cross-Agency Delivery / Tiger Team distinction consistent everywhere.
3. Treat the Tiger Teams Playbook as the canonical Tiger Team reference.
4. Add glossary guardrails for terms that should be used carefully.
5. Tighten navigation so readers find the operating model before they dive into portfolio-specific pages.

## 2. Top terminology risks

| Term or concept | Current issue | Why it matters | Canonical usage |
| --- | --- | --- | --- |
| Innovation Lab vs. Cross-Agency Delivery | The distinction is right in several places but repeated differently. | Agency partners may confuse craft ownership with implementation authority. | “The Lab owns the craft. Cross-Agency Delivery owns the coordination overlay.” |
| Tiger Team | Sometimes reads as a Lab method and sometimes as a delivery method. | Tiger Teams need clear authorization, time-boxing, and sustainment. | “A Tiger Team is a time-boxed, cross-functional delivery + innovation sprint. The Lab provides the method and team. Cross-Agency Delivery charters it when cross-agency authority is required.” |
| Portfolio vs. service | Mostly clear, but not always repeated where readers need it. | People may confuse org structure with what OPI delivers. | Portfolio = people, leadership, budget. Service = value delivered to the city. |
| Data and Analytics vs. Data and Digital | Current canonical term is Data and Analytics; older phrasing may persist. | Stale terms make the org model feel unsettled. | Use Data and Analytics unless describing historical or transitional material. |
| Citywide Digital Services | Could be read as a separate team, brand, or service. | It can blur Innovation Lab ownership. | Use Innovation Lab for the portfolio; use citywide digital services only for brand stewardship or request routing where necessary. |
| Baltimore Design Lab | Could imply a separate portfolio. | It may compete with Innovation Lab in reader understanding. | Treat as a design community of practice or sub-capability, not a separate service unless formally approved. |
| Delivery room | Less precise than other terms. | It can sound theatrical or imported without definition. | Prefer delivery review, delivery cadence, or delivery activation. |
| Joint Stat | Needs clearer distinction from thematic Stat and delivery review. | Readers need to know when decisions happen versus when implementation is managed. | Define as a Stat that brings multiple agencies into one performance routine for a shared problem. |
| Authorizer vs. SRO | Strong in the glossary, but should be reinforced elsewhere. | Confusion here slows decisions. | Authorizer provides authority and air cover. SRO runs the work day to day. |
| Sustainment | Present throughout, but should become a gate. | Launch without ownership does not count as success. | Every product, Tiger Team, and delivery activation needs owner, SOPs, metrics, and handoff. |

## 3. Innovation Lab / Cross-Agency Delivery / Tiger Team clarity memo

### Clean conceptual model

Use this language consistently:

> CitiStat identifies the problem. Data helps explain it. The Innovation Lab designs and tests the solution. Cross-Agency Delivery coordinates implementation when multiple agencies must act together. AdminOps keeps the work visible, documented, and sustained.

### Where the wiki already explains this well

- The Innovation Lab Strategy contains the strongest distinction: the Lab is the capability and Cross-Agency Delivery is the service overlay.
- The Tiger Teams Playbook already explains when Tiger Teams are chartered through Cross-Agency Delivery versus Innovation Lab intake.
- The glossary already defines Authorizer, SRO, Cross-Agency Delivery, Innovation Lab, delivery review, and Tiger Team in strong plain language.

### Where confusion can still appear

- Section landing pages are too brief to teach the model to new readers.
- Cross-Agency Delivery language can accidentally make Performance and CitiStat sound like the delivery routine rather than the performance routine that monitors the gain.
- “Digital Services” and “Baltimore Design Lab” need explicit status so they do not compete with Innovation Lab terminology.

### Reusable language

> The Innovation Lab owns the craft of solving: discovery, service design, user research, product management, prototyping, civic technology, AI pilots, and MVP-and-handoff. Cross-Agency Delivery owns the coordination overlay when multiple agencies must ship together: Authorizer, SRO, decision rights, escalation, commitment tracking, and sustainment commitments.

> A Tiger Team is the right routine when a service problem needs a time-boxed team to diagnose, prototype, and test a fix in real conditions. It is not the right routine for routine reporting, a one-time executive decision, or a dashboard request without a service-change owner.

## 4. Page-by-page recommendations

| File | Current purpose | Audience | Quality rating | Recommendation | Priority |
| --- | --- | --- | --- | --- | --- |
| `docs/how-we-work/how-work-moves-through-opi.md` | New canonical explainer | Staff and partners | New | Add and promote | P0 |
| `docs/our-teams/innovation-lab/index.md` | Section landing page | Staff and partners | Needs light edit | Add clear distinction language | P0 |
| `docs/our-teams/cross-agency-delivery/index.md` | Section landing page | Staff and partners | Needs light edit | Clarify service overlay vs. performance routine | P0 |
| `docs/resources/reference/glossary.md` | Term source of truth | All audiences | Strong | Add “terms to use carefully” | P0 |
| `docs/resources/reference/tiger-teams-playbook.md` | Tiger Team playbook | OPI and agencies | Strong | Add “when to use / not use” test | P1 |
| `docs/our-teams/innovation-lab/innovation-lab-strategy.md` | Lab strategy | Leadership and partners | Strong | Keep; cross-link to new explainer | P1 |
| `docs/our-teams/cross-agency-delivery/about-cross-agency-delivery.md` | Cross-agency delivery explainer | Leadership and partners | Strong | Keep; align future edits to new explainer | P1 |
| `docs/resources/reference/theory-of-change-summaries.md` | ToC summary | Staff and partners | Strong | Add signal-to-solution loop language in future pass | P2 |
| `docs/public/website-copy-master.md` | Public copy | Public / comms | Needs future review | Ensure no alternate terms are introduced | P2 |
| `docs/about-us/about-opi/teams-programs-foundations.md` | Operating overview | Staff and partners | Strong | Reinforce portfolio/service/team/program distinctions | P2 |

## 5. Information architecture recommendations

1. Add `How Work Moves Through OPI` under `How We Work` immediately after the section index.
2. Add a landing-page card for the new explainer.
3. Keep Tiger Teams Playbook in Reference, but link to it from Innovation Lab, Cross-Agency Delivery, and the new explainer.
4. Keep Cross-Agency Delivery as its own section. Do not move it back under Performance and CitiStat, because the redirect map already indicates that separation is intentional.
5. Use the glossary as the source of truth and link to it from section landing pages.

## 6. Canonical terminology guide

### Active terms

- **Innovation Lab:** OPI’s craft capability for discovery, service design, product, prototyping, civic technology, AI pilots, and MVP-and-handoff.
- **Cross-Agency Delivery:** OPI’s coordination overlay for multi-agency implementation with named authority and sustainment commitments.
- **Tiger Team:** A time-boxed, cross-functional delivery + innovation sprint focused on one service problem.
- **CitiStat:** OPI’s executive performance routine for seeing performance clearly and driving follow-through.
- **Authorizer:** Executive who provides authority and air cover.
- **Senior Responsible Owner:** Person accountable for running the work day to day.
- **Sustainment:** The handoff, SOPs, owners, metric set, and review cadence that keep the gain after OPI steps back.

### Terms to use carefully

- **Citywide Digital Services:** Use only when referring to brand stewardship or digital service request routing. Do not use as a replacement for Innovation Lab.
- **Baltimore Design Lab:** Use as a design community of practice or sub-capability unless formally approved as a separate program.
- **Delivery room:** Prefer delivery review, delivery cadence, or delivery activation.
- **Joint Stat:** Define on first use and distinguish from a delivery review.

## 7. Editorial style guide

Write like OPI is a disciplined public-sector operator.

- Use plain, direct sentences.
- Define terms before relying on them.
- Use examples from city services when a concept is abstract.
- Avoid vague transformation language.
- Avoid “innovation” as a standalone virtue; connect it to service improvement.
- Avoid saying a tool is successful unless adoption, use, or impact is named.
- Use “resident and staff” when describing service experience.
- Use “public servants” when emphasizing the people doing the work.
- Use “sustainment” only when ownership, SOPs, metric set, and cadence are named.

## 8. Priority rewrite queue

1. Add `How Work Moves Through OPI`.
2. Tighten `Innovation Lab` section landing page.
3. Tighten `Cross-Agency Delivery` section landing page.
4. Add glossary guardrails.
5. Add “when to use / not use” test to Tiger Teams Playbook.
6. Add cross-links from Innovation Lab Strategy.
7. Add cross-links from About Cross-Agency Delivery.
8. Review public website copy for stale terminology.
9. Review theory of change summaries for loop language.
10. Review teams/programs/foundations for portfolio/service/team/program language.

## 9. Quick wins

- Add the signal-to-solution loop sentence to high-traffic pages.
- Add the new explainer to How We Work navigation.
- Standardize “AdminOps” spelling.
- Prefer Data and Analytics over Data and Digital.
- Avoid “delivery room” unless formally defined.
- Add explicit “not a standing team / not a cost center” language to Cross-Agency Delivery pages.
- Add “launch is not success; sustainment is success” to Lab and Tiger Team pages.

## 10. Open questions for OPI leadership

1. Should **Citywide Digital Services** remain a public-facing brand, or should it be fully retired in favor of Innovation Lab language except for transition references?
2. Should **Baltimore Design Lab** be formally defined as a design community of practice, a sub-capability of the Innovation Lab, or retired as a separate label?
3. Should **Joint Stat** remain an active term, or should OPI use thematic Stat plus delivery review to avoid another category?
4. Should the wiki include a public-facing version of the signal-to-solution loop, or should the new explainer remain internal-first under How We Work?
