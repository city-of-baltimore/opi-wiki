"""Helpers for rendering shared display badges in Markdown pages."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from html import escape

DISPLAY_BADGE_FIELD = "display_badge"


@dataclass(frozen=True)
class BadgeDefinition:
    """Normalized badge style and visible label."""

    css_variant: str
    label: str


# "approved" was retired on purpose: approval is the default state of published
# pages, so labeling it added noise. Badges are opt-in signals for the
# exceptions (draft) and content types (template, reference).
BADGE_DEFINITIONS = {
    "draft": BadgeDefinition(css_variant="draft", label="Draft"),
    "reference": BadgeDefinition(css_variant="neutral", label="Reference"),
    "template": BadgeDefinition(css_variant="neutral", label="Template"),
}


def normalize_badge_key(value: str) -> str:
    """Normalize a badge token from metadata or macro input."""

    return value.strip().casefold().replace("_", "-").replace(" ", "-")


def get_badge_definition(value: str) -> BadgeDefinition:
    """Return the configured badge definition for a token."""

    normalized_value = normalize_badge_key(value)
    try:
        return BADGE_DEFINITIONS[normalized_value]
    except KeyError as error:
        available = ", ".join(sorted(BADGE_DEFINITIONS))
        raise ValueError(
            f"Unknown display badge '{value}'. Expected one of: {available}."
        ) from error


def render_badge(value: str) -> str:
    """Render a shared badge as HTML."""

    definition = get_badge_definition(value)
    return (
        f'<span class="opi-pill {escape(definition.css_variant, quote=True)}">'
        f"{escape(definition.label)}</span>"
    )


def resolve_optional_page_badge_value(metadata: Mapping[str, str]) -> str | None:
    """Return the page's badge token, or None when no badge is configured.

    Badges are opt-in: most pages set no display_badge and render no pill.
    """

    raw_value = metadata.get(DISPLAY_BADGE_FIELD, "")
    if not raw_value:
        return None
    return normalize_badge_key(raw_value)
