# Baltimore Intelligence Center

{{ page_header(summary="Baltimore's product for governed city intelligence and responsible AI.") }}

The Baltimore Intelligence Center (BIC) is an OPI product that connects governed city data to reusable analytics and artificial-intelligence capabilities. It is designed for city-led operation, with governance, documentation, and maintainability built into the product from the start.

BIC helps approved users work from consistent definitions, explore city-service information, and ask questions in plain language without bypassing the controls that protect city data.

## The problem it solves

City information lives across many source systems, and the same measure can be defined differently from one workflow to another. Artificial intelligence adds another responsibility: new uses need clear approval, oversight, and monitoring before they enter city workflows. BIC creates a governed path from approved data to consistent measures and decision support.

## How it fits together

BIC is layered, and each layer has one job. The [Baltimore City Data Platform](../baltimore-city-data-platform.md) is the governed foundation: it ingests city data and turns it into governed data products. BIC adds shared definitions, relationships, analytical services, and plain-language interfaces on top of that foundation. User-facing experiences read only approved outputs.

One firm rule holds the seam together: the intelligence layer reads the platform's governed marts and never re-ingests raw data. OPI decides what the data means, and the platform enforces it.

## What it delivers

BIC delivers a shared [intelligence architecture](architecture-and-roadmap.md), reusable [analytical and AI capabilities](products-and-capabilities.md), and a practical model for [responsible data and AI](responsible-data-and-ai.md). Together, those parts support city-service analysis and performance questions while keeping classification, access control, human oversight, source grounding, and monitoring in the workflow.

## Where it's headed

BIC develops in stages. OPI first establishes the governed foundation, then tests narrowly scoped uses with approved data, and expands only after the controls and results have been reviewed. This keeps the product useful while allowing governance, accessibility, security, and operational readiness to mature with it.

## In this section

- [Architecture](architecture-and-roadmap.md): how the platform and intelligence layers fit together.
- [Capabilities](products-and-capabilities.md): the analytical and AI capabilities the product can support.
- [Responsible data & AI](responsible-data-and-ai.md): how classification, approval, oversight, and monitoring apply.
