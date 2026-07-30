# OPI Foundations Product Documentation

This directory contains the repository's product contracts. It is outside
`docs/`, so MkDocs does not publish these files on the OPI Foundations Wiki.

Read the documents in this order:

1. [Product Requirements](product-requirements.md) defines the product purpose,
   audiences, scope, capabilities, commitments, current assurance, success
   measures, and owner decisions.
2. [User Stories](user-stories.md) turns that contract into 30 reader,
   contributor, content-owner, product-manager, and maintainer journeys with
   observable acceptance criteria.
3. [Technical Specification](technical-spec.md) explains how the current
   content, rendering, preview, verification, and GitHub Pages publication
   system implements the contract.

[Repository onboarding](../onboarding.md) remains the short plain-language
entry point. These three documents provide the deeper product and engineering
contract; they do not replace published service, program, product, method, or
accessibility pages.

The OPI Foundations Docs Maintainer is the operational steward for this
documentation set. Accountable product ownership remains
[Product Decision 12](product-requirements.md#decision-12-who-is-accountable-for-opi-foundations-product-governance);
this index does not infer it from page metadata or a technical maintainer role.

## Maintenance rule

Update these documents in the same slice when a change alters an audience,
journey, capability, product boundary, architecture seam, or release
guarantee. A wording correction that does not change behavior does not need a
new requirement or story.

Business questions remain explicit in the requirements document until the
named owner resolves them. Technical facts must be checked against the current
repository before they are updated here. The fast product-contract link check
must pass for every change to this directory.
