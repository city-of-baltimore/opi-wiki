# Digital Product Methodology

{{ page_header(summary="How OPI ships digital products inside city government.", category="METHOD GUIDE", tagline="A practical workflow for service design, product discovery, prototyping, engineering, documentation, and sustainment.") }}

*Read alongside: OPI Innovation Lab Strategy*

*The Lab Strategy explains why we build and the discipline we use. This Methodology is the citywide playbook for how we design and ship digital products. More than the Innovation Lab uses it.*

**EXECUTIVE SUMMARY**

**Start with the service, not the screen**

OPI designs and ships digital products by starting with the service, not the screen. The goal is not to produce attractive interfaces or tools for their own sake. The goal is to improve how city services work for residents and staff.

This method guide defines a practical workflow for moving from problem framing to service design, UX flows, prototypes, engineering, testing, launch, documentation, and sustainment. It also clarifies how tools such as Miro, Figma, AI-assisted coding, engineering stacks, and Adobe InDesign fit together without creating confusion or duplicate work.

The methodology is owned through the Innovation Lab, in partnership with Data & Analytics, BCIT, agencies, and AdminOps. It is intended for citywide use. It applies to operational tools, public-facing portals, field data collection apps, dashboards with workflow components, and other products that improve service delivery.

**THE CORE RULE**

**Start with the service**

A digital product should not begin with a screen. It should begin with a problem: who is trying to do what, where the service breaks, why it matters, and what would have to change for residents or staff to be better off.

This protects OPI from building tools that digitize broken processes. If the handoff is unclear, the product will not fix it. If ownership is unresolved, the product will expose it. If data quality is weak, the product will amplify the weakness. The first design task is therefore to understand the service end to end.

**WORKFLOW AT A GLANCE**

**Eight stages from intake to publication**

| **Stage**              | **Primary tool**                                     | **Purpose**                                                                                    | **Standard outputs**                                        |
|------------------------|------------------------------------------------------|------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| 1\. Intake and framing | OPI intake / brief                                   | Confirm problem, users, owner, decision context, urgency, sustainment.                         | Intake stub; product brief; routing decision.               |
| 2\. Service design     | Miro                                                 | Map service, journey, actors, handoffs, pain points, root causes.                              | Service blueprint; process map; journey map; system actors. |
| 3\. UX flow            | Figma                                                | Translate service design into product flows and interaction logic.                             | Wireframes; user flows; navigation model.                   |
| 4\. UI prototype       | Figma                                                | Design screens, components, responsive layouts, clickable prototypes.                          | Prototype; component specs; design system elements.         |
| 5\. Engineering build  | Approved stack; AI-assisted coding where appropriate | Turn validated designs into working software with tests, APIs, deployment discipline.          | Production code; API contracts; tests; changelog.           |
| 6\. QA and pilot       | Testing tools; analytics; user feedback              | Validate accessibility, security, performance, usability, data quality, readiness.             | QA checklist; pilot report; issues log; go/no-go memo.      |
| 7\. Launch and sustain | Runbook / knowledge base / status tool               | Release responsibly, monitor use, support users, transfer ownership.                           | Runbook; support model; sustainment plan; annual review.    |
| 8\. Publication track  | InDesign / document tools                            | Create public reports, playbooks, briefs, polished documentation separate from product design. | Publication PDF; implementation playbook; public summary.   |

**STAGE 1**

**Intake and problem framing**

Every product begins with intake. Intake should clarify the requestor, user, problem, affected agencies, desired outcome, timeline, risks, public visibility, data needs, and sustainment owner. The key question is whether the request is truly a product, or whether it should be handled through a Stat, data product, process redesign, decision memo, procurement, training, or agency-owned operational change.

The product brief should answer: What problem are we solving? Who experiences it? What decision or workflow will change? What does success look like? What data is required? Who will own the product after launch?

**STAGE 2**

**Service design in Miro**

Miro is best for collaborative service design. It helps teams map complex systems, align stakeholders, and visualize the experience across agencies and users. For a permitting portal, this might include resident application, review queue, plan review, agency review, approval, inspection scheduling, communication, and closure.

- Service blueprint showing frontstage and backstage steps.

- Process map showing what actually happens, not only what policy says should happen.

- User journey showing resident or staff experience.

- System actor map showing agencies, systems, vendors, and decision points.

- Pain point and root cause analysis.

**STAGE 3**

**UX flow and interaction logic in Figma**

Figma translates the service design into product flows. At this stage, designs can remain low fidelity. The goal is not visual polish. The goal is to test whether the product logic makes sense: navigation, forms, status changes, user permissions, notifications, review steps, and error states.

For a permitting product, the UX flow might move from dashboard to permit list, new application form, upload documents, review status, agency comments, applicant action needed, approval, and inspection scheduling. Each step should map back to the service blueprint.

**STAGE 4**

**UI design, components, and prototypes in Figma**

Once the flow is validated, Figma becomes the place for detailed UI design. Designers create screens, responsive layouts, components, and clickable prototypes. This is where OPI’s design system matters. Reusable components reduce inconsistency, improve accessibility, and make future products faster to build.

The prototype should be tested with users before engineering begins at full speed. Testing should include residents or staff who reflect the real users of the service. A beautiful prototype that users cannot understand is not ready.

**STAGE 5**

**Developer handoff and implementation**

Figma Dev Mode supports handoff by giving developers access to spacing, fonts, colors, component definitions, and layout specs. Handoff should also include the product brief, service blueprint, user stories, API assumptions, acceptance criteria, accessibility requirements, and data definitions.

Engineering should follow OPI’s standard discipline: modular design, API contracts, smoke tests, documented environment variables, version control, code review, deployment checks, and no drift between frontend assumptions and backend schemas. AI-assisted coding tools can accelerate implementation, but they do not remove the need for human review, testing, security, and maintainability.

**STAGE 6**

**QA, pilot, and readiness gates**

No product should be demonstrated, piloted, or launched without internal vetting. QA should include usability, accessibility, performance, security, data quality, permissions, error handling, mobile responsiveness, and operational readiness. Known issues should be documented before any demo or pilot.

- Accessibility check for forms, contrast, keyboard navigation, alt text, labels, and plain language.

- Data quality check against source systems and methodology cards.

- Security and permissions review with BCIT where appropriate.

- User acceptance testing with agency staff and representative users.

- Support path and incident process before pilot launch.

- Go/no-go memo summarizing risks, decisions, and mitigation.

**STAGE 7**

**Launch, adoption, and sustainment**

Launch is not success. Adoption and sustainment are success. Every product should have a named owner, runbook, support model, release cadence, usage metrics, and review date. If a product is not being used or is not changing a decision or workflow, the team should redesign it, retrain users, narrow scope, or retire it.

A sustainment plan should define who owns content, who owns data, who owns code, who handles support, how bugs are reported, how enhancements are prioritized, how the product is funded, and when the product will be reviewed for continued value.

**PUBLICATION TRACK**

**Where Adobe InDesign fits**

InDesign and publication tools belong in a parallel track, not inside the product design pipeline. They are best for strategy playbooks, annual reports, policy briefs, public guides, case studies, and polished PDFs. A digital product should move from service design to Figma to engineering. A policy report or public publication should move from writing and review to design and PDF production.

The two tracks should connect through shared narrative, screenshots, data definitions, and implementation learning. But they should not be confused. Figma designs products. Adobe InDesign publishes documents.

**GOVERNANCE AND DECISION RIGHTS**

**Who owns what across the workflow**

| **Role**         | **Decision rights**                                                                                                              |
|------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Innovation Lab   | Owns product discovery, service design, user research, product briefs, prototypes, and product quality.                          |
| Product Owner    | Owns scope, outcomes, user value, release priorities, and go/no-go recommendations.                                              |
| Agency Sponsor   | Owns workflow adoption, staff participation, operational sustainment, and business decisions.                                    |
| Data & Analytics | Owns shared datasets, methodology, data quality, APIs, analytics, and AI/data readiness review.                                  |
| BCIT             | Owns enterprise infrastructure, security, identity, production environment, architecture partnership, and technology governance. |
| AdminOps         | Owns public narrative, Council coordination, publication readiness, and portfolio visibility.                                    |

**METRICS FOR PRODUCT SUCCESS**

**How we know a product is working**

- Task success: users can complete the core task without avoidable confusion or support.

- Time on task: the product reduces the time needed to complete or manage a service workflow.

- Adoption: named users use the product on a recurring basis.

- Reliability: the product meets uptime, performance, and incident response expectations.

- Service impact: backlog, cycle time, repeat contacts, rework, or resident confusion decreases.

- Sustainment: product has an owner, runbook, support model, data refresh plan, and review cadence.

- Reuse: components, patterns, APIs, or methods are reused in future OPI products.

**CLOSING**

**Better services, not more products**

OPI’s product workflow is built to avoid two common failures: building tools without understanding the service, and producing design artifacts that never become operational change. The method starts with reality, designs with users, builds in disciplined increments, tests before launch, and plans sustainment from the beginning.

> *The goal is not more products. The goal is better services. Products are one way we make that real.*

## Relationship to Cross-Agency Delivery

Digital product work belongs in the Innovation Lab when the problem requires discovery, user research, prototyping, engineering, or product management. If the product cannot succeed unless multiple agencies change workflows, decision rights, or sustainment commitments together, the work also needs Cross-Agency Delivery activation.

The distinction is simple: the Lab owns the product craft; Cross-Agency Delivery owns the cross-agency authority and implementation cadence.
