"""Helpers for rendering shared display badges in Markdown pages."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Mapping

DISPLAY_BADGE_FIELD = "display_badge"


@dataclass(frozen=True)
class BadgeDefinition:
    """Normalized badge style and visible label."""

    css_variant: str
    label: str


BADGE_DEFINITIONS = {
    "approved": BadgeDefinition(css_variant="approved", label="Approved"),
    "draft": BadgeDefinition(css_variant="draft", label="Draft"),
    "position-description": BadgeDefinition(
        css_variant="internal",
        label="Position Description",
    ),
    "reference": BadgeDefinition(css_variant="internal", label="Reference"),
    "template": BadgeDefinition(css_variant="internal", label="Template"),
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


def resolve_page_badge_value(metadata: Mapping[str, str]) -> str:
    """Return the configured badge token for a page."""

    raw_value = metadata.get(DISPLAY_BADGE_FIELD, "")
    if not raw_value:
        raise ValueError(
            f"Page metadata is missing the '{DISPLAY_BADGE_FIELD}' field needed "
            "for page_badge()."
        )
    return normalize_badge_key(raw_value)
