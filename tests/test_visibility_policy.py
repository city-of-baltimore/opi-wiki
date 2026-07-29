"""Unit tests for the shared retired-visibility policy."""

from __future__ import annotations

import pytest
from scripts.repo_tools.visibility_policy import (
    PRESENTATION_HOOK_KIND,
    VISIBILITY_LABEL_KIND,
    VisibilityPolicyMatch,
    find_presentation_hook_matches,
    find_visibility_label_matches,
)


def test_visibility_policy_returns_typed_matches_in_source_order() -> None:
    """Distinct label occurrences should retain deterministic spans and text."""

    text = "public site; approved version"

    assert find_visibility_label_matches(text) == (
        VisibilityPolicyMatch(
            kind=VISIBILITY_LABEL_KIND,
            start=0,
            end=11,
            text="public site",
        ),
        VisibilityPolicyMatch(
            kind=VISIBILITY_LABEL_KIND,
            start=13,
            end=29,
            text="approved version",
        ),
    )


@pytest.mark.parametrize(
    "text",
    (
        "",
        "Approved users work from approved data for public safety.",
        "A public-facing service must meet accessibility requirements.",
        "The public/private boundary controls disclosure.",
        "An internal-only dataset requires approved access.",
    ),
)
def test_visibility_policy_preserves_domain_language(text: str) -> None:
    """Civic, service, and formal access meanings are not repository labels."""

    assert find_visibility_label_matches(text) == ()


@pytest.mark.parametrize(
    "text",
    (
        "public website",
        "public websites",
        "public wiki",
        "public documentation",
        "public-facing documentation",
        "internal website",
        "internal wiki",
        "internal documentation",
        "internal-only documentation",
        "approved website",
        "approved wiki",
        "approved documentation",
    ),
)
def test_visibility_policy_rejects_statuses_applied_to_repository_surfaces(
    text: str,
) -> None:
    """Equivalent repository-surface nouns must share one status policy."""

    matches = find_visibility_label_matches(text)

    assert len(matches) == 1
    assert matches[0].text == text


@pytest.mark.parametrize(
    "text",
    (
        "The website publishes public data for approved users.",
        "Documentation describes internal controls and approved access.",
        "The wiki explains public records disclosure requirements.",
    ),
)
def test_repository_surface_nouns_remain_valid_without_a_status_label(
    text: str,
) -> None:
    """Repository nouns alone must not suppress civic and governance language."""

    assert find_visibility_label_matches(text) == ()


def test_approved_verb_is_not_a_repository_state_label() -> None:
    """A named actor's completed review action must remain valid civic prose."""

    assert find_visibility_label_matches("The Board approved guidance on grants.") == ()


@pytest.mark.parametrize(
    "text",
    (
        "approved documentation",
        "Use the approved guidance.",
        "This is approved documentation.",
    ),
)
def test_approved_repository_state_requires_bounded_label_context(text: str) -> None:
    """Standalone and explicitly introduced approved states remain retired."""

    assert find_visibility_label_matches(text)


def test_internal_facing_repository_state_is_retired() -> None:
    """Internal-facing is the same generic posture as internal-only."""

    assert find_visibility_label_matches("internal-facing documentation")


def test_director_letter_policy_is_explicitly_scoped() -> None:
    """Letter-only framing must require the caller's director-section context."""

    text = "A **public** letter."

    assert find_visibility_label_matches(text) == ()
    assert find_visibility_label_matches(text, director_letter=True) == (
        VisibilityPolicyMatch(
            kind=VISIBILITY_LABEL_KIND,
            start=0,
            end=19,
            text="A public letter",
        ),
    )


@pytest.mark.parametrize(
    "text",
    (
        "Public Purpose",
        "## Public Purpose {#purpose} ##",
        "## **Public Purpose**",
        "## [Public Purpose](#purpose)",
        "Public Purpose {.summary}\n---",
    ),
)
def test_director_heading_policy_accepts_rendered_and_source_heading_text(
    text: str,
) -> None:
    """One policy should serve rendered heading spans and source heading regions."""

    assert find_visibility_label_matches(text, director_letter=True) == ()
    matches = find_visibility_label_matches(
        text,
        director_letter=True,
        heading=True,
    )

    assert len(matches) == 1
    assert matches[0].kind == VISIBILITY_LABEL_KIND
    assert "Public Purpose" in matches[0].text


def test_heading_policy_requires_director_letter_context() -> None:
    """A governance heading outside director letters must remain ordinary text."""

    assert find_visibility_label_matches("Public Purpose", heading=True) == ()


def test_presentation_policy_returns_macro_and_bem_hook_occurrences() -> None:
    """Both retired rendering mechanisms should expose stable source spans."""

    text = '{{- badge("reference") }} .opi-pill__label'

    assert find_presentation_hook_matches(text) == (
        VisibilityPolicyMatch(
            kind=PRESENTATION_HOOK_KIND,
            start=0,
            end=10,
            text="{{- badge(",
        ),
        VisibilityPolicyMatch(
            kind=PRESENTATION_HOOK_KIND,
            start=27,
            end=35,
            text="opi-pill",
        ),
    )


@pytest.mark.parametrize(
    "text",
    (
        "",
        "Activate an employee badge.",
        ".opi-pillar { display: block; }",
        ".opi-pillow { display: block; }",
    ),
)
def test_presentation_policy_preserves_unrelated_terms(text: str) -> None:
    """Physical badges and similarly named components are outside the policy."""

    assert find_presentation_hook_matches(text) == ()


def test_visibility_policy_is_repeatably_deterministic() -> None:
    """Repeated calls must return identical occurrence ordering and values."""

    text = "approved version; public site; approved version"

    first = find_visibility_label_matches(text)

    assert first == find_visibility_label_matches(text)
    assert tuple(match.start for match in first) == tuple(sorted(match.start for match in first))
