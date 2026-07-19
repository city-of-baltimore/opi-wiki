# Digital Product Methodology

{{ page_header(summary="How OPI ships digital products inside city government.", category="METHOD GUIDE", tagline="Start with the service, design with users, build in disciplined increments, and plan for sustainment.") }}

This is OPI's playbook for how digital products get designed and shipped. It is the Innovation Lab's build method, and any team building a digital product for the City can use it.

## Start with the service, not the screen

A digital product should not begin with a screen. It begins with a problem: who is trying to do what, where the service breaks, why it matters, and what would have to change for residents or staff to be better off.

Starting with the service protects OPI from building tools that just digitize a broken process. If a handoff is unclear, the product will not fix it. If ownership is unresolved, the product will expose it. If the underlying data is weak, the product will amplify the weakness. So the first job is always to understand the service end to end, before anyone designs a screen.

From there the work moves through a handful of phases: frame the problem, map the service, design the product, build it, test it, and launch and sustain it. OPI owns this method through the Innovation Lab, in partnership with Data and Analytics, BCIT, agencies, and AdminOps. It applies to operational tools, public portals, field data-collection apps, dashboards with workflow, and anything else meant to improve service delivery.

## The work, phase by phase

### Frame the problem

Every product starts with intake. Before any design, the team gets clear on the requestor, the users, the problem, the affected agencies, the outcome we want, the timeline, the risks, the data needed, and who will own the product after launch. The first real question is whether this should be a product at all. Often the right answer is a Stat, a data product, a process redesign, a decision memo, a procurement, training, or a change the agency owns. If it is a product, the team writes a short brief: what problem we are solving, who feels it, what workflow or decision will change, what success looks like, what data is required, and who owns it after launch.

### Map the service

Next the team maps the service as it actually works, not as policy says it should. That means laying out the front-stage and back-stage steps, the experience for the resident or staff member, and the agencies, systems, and decision points involved, with the pain points and root causes marked. For a permitting portal, that might run from application through review, plan review, agency sign-off, approval, inspection scheduling, and closure. This is collaborative work, so the team does it on a shared whiteboard where agencies and users can align on one picture.

### Design the product

With the service mapped, the team designs how the product works before how it looks. The first pass stays deliberately rough: the goal is to test whether the logic holds up, including navigation, forms, status changes, permissions, notifications, review steps, and error states, with every step tracing back to the service map. Once the flow makes sense, the team designs the real screens, components, and a clickable prototype, working from OPI's shared design system so products stay consistent and accessible. Then the team tests that prototype with real residents or staff before engineering ramps up. A polished prototype that users cannot follow is not ready.

### Build it

Engineering turns the validated design into working software under OPI's standard discipline: modular design, API contracts, tests, documented configuration, version control, code review, deployment checks, and no gap between what the front end assumes and what the back end provides. A good handoff includes the brief, the service map, user stories, acceptance criteria, accessibility requirements, and data definitions, not just the screens. AI-assisted coding can speed the work, but it does not remove the need for human review, testing, security, and maintainability.

### Test and pilot

No product is demoed, piloted, or launched without vetting. QA covers usability, accessibility, performance, security, data quality, permissions, error handling, mobile, and operational readiness, and known issues are written down before any demo. A typical readiness check includes an accessibility pass (forms, contrast, keyboard navigation, alt text, plain language), a data-quality check against source systems, a security and permissions review with BCIT where needed, user testing with agency staff and representative users, a support and incident path, and a go/no-go memo that lays out the risks and the decision.

### Launch and sustain

Launch is not success; adoption and sustainment are. Every product ships with a named owner, a runbook, a support model, a release schedule, usage metrics, and a review date. If a product is not being used, or is not changing a decision or a workflow, the team redesigns it, retrains users, narrows its scope, or retires it. The sustainment plan says who owns the content, the data, and the code, who handles support, how bugs are reported, how enhancements are prioritized, how the product is funded, and when it will be reviewed for continued value.

## A note on tools

Tools serve the method, not the other way around. OPI maps services on a shared whiteboard (Miro), designs flows and interfaces in Figma against a common design system, builds on an approved engineering stack with AI-assisted coding where it helps, and produces public documents in a separate publishing track (Adobe InDesign). The tools can change; the sequence, from service to design to working software, does not.

## Publications are a separate track

Public reports, playbooks, briefs, and polished PDFs are not part of the product pipeline, and they should not be built as if they were. A digital product moves from service design to interface design to engineering. A policy report or public publication moves from writing and review to layout and PDF production. The two tracks share narrative, screenshots, data definitions, and lessons learned, but they are different work: one designs products, the other publishes documents.

## Who owns what

| Role | Decision rights |
|------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Innovation Lab   | Owns product discovery, service design, user research, product briefs, prototypes, and product quality. |
| Product Owner    | Owns scope, outcomes, user value, release priorities, and go/no-go recommendations. |
| Agency Sponsor   | Owns workflow adoption, staff participation, operational sustainment, and business decisions. |
| Data and Analytics | Owns shared datasets, methodology, data quality, APIs, analytics, and AI and data-readiness review. |
| BCIT             | Owns enterprise infrastructure, security, identity, the production environment, architecture partnership, and technology governance. |
| AdminOps         | Owns public narrative, Council coordination, publication readiness, and portfolio visibility. |

## How we know a product is working

A product is working when users can complete the core task without avoidable confusion or support, and when it cuts the time to complete or manage the workflow. Beyond that, we look for real adoption (named users using it on a recurring basis), reliability against uptime and incident expectations, and a measurable service impact: smaller backlogs, shorter cycle times, fewer repeat contacts, less rework, or less resident confusion. Finally, a working product is one that lasts, with an owner, a runbook, a support model, a data-refresh plan, and a review schedule, and whose components, patterns, and APIs get reused in future OPI products.

## Better services through products

OPI's product workflow is built to avoid two common failures: building tools without understanding the service, and producing design artifacts that never become operational change. The method starts with reality, designs with users, builds in disciplined increments, tests before launch, and plans sustainment from the start. Better services are the goal; a product is one way OPI gets there.

## Relationship to Cross-Agency Delivery

Digital product work belongs in the Innovation Lab when the problem needs discovery, user research, prototyping, engineering, or product management. If the product cannot succeed unless several agencies change workflows, decision rights, or sustainment commitments together, the work also needs Cross-Agency Delivery activation. The distinction is simple: the Lab owns the product work, and Cross-Agency Delivery owns the cross-agency authority and implementation schedule.
