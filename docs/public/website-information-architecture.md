# Website Information Architecture

{{ page_header(summary="Information architecture for the public OPI website.", category="SERIES · OPI FOUNDATIONS") }}

Site map, navigation, URL structure, content priority, and a CMS-ready page inventory.

VERSION
:   v1.0

UPDATED
:   April 2026

AUDIENCE
:   Web publisher, OPI Director’s Office, Communications

OWNER
:   OPI Director’s Office

## Purpose

This document defines the information architecture for opi.baltimorecity.gov before any CMS build begins. It pairs with the OPI Website Copy Master, which is the canonical source for page content. Together, the two documents allow the City’s web publisher to plan the site, scope the build, and lift copy directly into the CMS.

## Design principles

- Two audiences, every page: an agency partner and a resident.

- Three things on every page: what it is, why it exists, and how to engage.

- Plain language. Define acronyms once, then use the short form.

- No dead ends. Every page has a clear next step.

- Accessibility first. WCAG 2.1 AA across the site.

- Predictable structure. The four sections are Teams, Programs, Services, and About.

## Top-level navigation

*Five primary nav items, in order. A subdued utility bar holds About and Contact.*

| **Nav item** | **URL**   | **Purpose**                                                                                            |
|--------------|-----------|--------------------------------------------------------------------------------------------------------|
| Home         | /         | OPI in one minute. Featured CitiStat brief, featured Open Baltimore dataset, Innovation Lab spotlight. |
| Teams        | /teams    | The four OPI portfolios.                                                                               |
| Programs     | /programs | CitiStat, Open Baltimore, Data Fellows, Innovation Lab program portfolio.                              |
| Services     | /services | The five OPI services and how to use them.                                                             |
| Reports      | /reports  | CitiStat impact briefs, annual reports, public summaries.                                              |

*Utility bar: About (/about), Contact (/contact), Search.*

## Site map

### Home — /

- Hero with primary calls to action.

- What we do (three columns: Performance, Data and Analytics, Innovation Lab).

- How we work (one paragraph).

- Featured modules: latest CitiStat impact brief, featured dataset, Innovation Lab project, recent annual report.

- Audience pathways block (agency / resident).

- Newsletter or updates feed signup.

### About OPI — /about

- Mission and North Star.

- Responsibilities.

- How OPI is organized (the four portfolios and five services).

- Leadership.

- Where we sit in City government.

- Contact and ways to engage.

### Teams — /teams

*Four tiles linking to portfolio detail pages. Each detail page follows the same structure.*

- Director’s Office — /teams/directors-office

- Performance — /teams/performance-citistat

- Data and Analytics — /teams/data-analytics

- Innovation Lab — /teams/innovation-lab

### Programs — /programs

*Four primary programs. Each has a detail page.*

- CitiStat — /programs/citistat

- Open Baltimore — /programs/open-baltimore

- Innovation Lab portfolio — /programs/innovation-lab

- Data Fellows — /programs/data-fellows

### Services — /services

*Five service pages. Each follows the same template.*

- Citywide Performance Management — /services/performance-management

- Citywide Data and Analytics — /services/data-analytics

- Innovation Lab — /services/innovation-lab

- Cross-Agency Delivery — /services/cross-agency-delivery

- AdminOps — /services/administration-operations

### Reports — /reports

- CitiStat impact briefs — /reports/citistat

- Annual reports — /reports/annual

- Public summaries — /reports/summaries

### How to work with OPI — /work-with-us

- Intake form (single front door).

- Pathways: agency, partner, resident, journalist, researcher.

- What to expect at each work size: quick request, project, major engagement.

### Contact — /contact

- General contact.

- Press contact.

- Partnership contact.

- Open Baltimore feedback.

### Utility pages

- Accessibility — /accessibility

- Language access — /language-access

- Privacy — /privacy

- Search — /search

- Glossary — /glossary

## Page template inventory

| **Template**        | **Used for**                                     | **Required components**                                                                                                                          |
|---------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Home template       | Home                                             | Hero, three-column overview, how-we-work paragraph, featured modules, audience pathways, updates feed.                                           |
| Section landing     | Teams, Programs, Services, Reports               | Section intro, tile grid linking to detail pages, audience pathways.                                                                             |
| Team detail         | Each portfolio                                   | Lead paragraph, why we exist, what we do, what it means for agencies, what it means for residents, how to engage, related programs and services. |
| Program detail      | Each program                                     | Lead paragraph, why it exists, how it works, where to see results, authority (where applicable), how to engage.                                  |
| Service detail      | Each service                                     | Lead paragraph, when to use this service, what to expect from OPI, how we work, what success looks like, how to start.                           |
| Report detail       | Each report or brief                             | Title, date, authoring team, summary, downloadable artifacts, contact for questions, methodology note where relevant.                            |
| Engagement / intake | Work with OPI                                    | Audience pathways, intake form, definition of done at each work size.                                                                            |
| Static / utility    | About, Contact, Glossary, Accessibility, Privacy | Plain text, structured headings, contact details, accessible link patterns.                                                                      |

## URL and slug standards

- Lower-case slugs separated by hyphens. No underscores.

- Short, descriptive slugs. Avoid acronyms in URLs unless the acronym is the official name (for example, /programs/citistat).

- Stable slugs. Avoid renaming after launch. If a slug must change, set up a permanent redirect.

- No dates in slugs for evergreen content. Reports use date in the page metadata, not the URL.

- External links open in the same tab unless they leave the City’s domain.

## Content priority by page

*The first 200 words of each page do the heaviest work. Use this priority order.*

| **Priority**                      | **What it includes**                                                     |
|-----------------------------------|--------------------------------------------------------------------------|
| 1\. What it is                    | A one-paragraph plain-language description.                              |
| 2\. Why it exists                 | The problem this team, program, or service helps solve.                  |
| 3\. What you can expect           | Concrete actions, deliverables, or outcomes.                             |
| 4\. How to engage                 | A clear next step with a route or contact.                               |
| 5\. Proof or transparency         | A recent example, a metric, an annual report, or an authority reference. |
| 6\. Page-level engagement element | Featured story, audience pathways, or updates feed.                      |

## Accessibility and language access

- All pages meet WCAG 2.1 AA. Color contrast at or above 4.5 to 1 for body text and 3 to 1 for large text.

- Heading hierarchy is consistent: one H1 per page, then nested H2 and H3 in order.

- All images have meaningful alternative text. Decorative images are marked as such.

- Forms include labels, error messages, and keyboard support.

- Plain-language pass on all pages before publication.

- Translation pathway is documented on each page (Spanish at minimum, others as supported).

## Search and discoverability

- Site search is enabled and tuned to favor service pages and program detail pages over reports.

- Each page sets a clean title tag, meta description, and canonical URL.

- Each page lists tags for cross-linking: portfolio, program, service, agency, audience.

- Reports include structured metadata: type, date, authoring team, agencies covered.

## Performance, security, and analytics

- Site loads quickly on low-bandwidth connections. Images compressed. No unnecessary scripts.

- HTTPS only. Cookie use is minimal and disclosed.

- Web analytics are privacy-respecting. No third-party trackers. Aggregate data only.

- Quarterly review of top pages, drop-offs, and search queries to refine content.

## CMS implementation notes

- The site can be implemented on the City’s standard CMS or as a static site, provided accessibility and search standards are met.

- Templates above should be implemented as reusable components.

- A simple workflow: editor drafts, OPI Director’s Office reviews, web publisher publishes. Updates use the same workflow.

- Versioning: track when each page was last reviewed and by whom.

## Open questions to resolve before launch

- Which CMS will host the site? Is OPI building on a Baltimore City template or a standalone site?

- Who is the named web publisher and editor of record?

- What is the language access scope at launch (Spanish only, or additional languages)?

- What integrations are required (Open Baltimore, 311, Baltimore City Code) and what is their content owner?

- What is the launch date and the rollout sequence (soft launch with a small audience, then public)?

## Owner and cadence

Owned by the OPI Director’s Office. Reviewed quarterly. Major IA changes go through Communications and the web publisher before publishing.
