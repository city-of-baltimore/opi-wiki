"""Shared helpers for rendering and validating OPI card-grid data."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any

from scripts.repo_tools.data import load_docs_yaml_file


@dataclass(frozen=True)
class Card:
    """Structured content for a single site card."""

    meta: str
    title: str
    body: str
    href: str | None = None
    link_label: str | None = None


def _normalize_card(raw_card: Any, source: str, index: int) -> Card:
    """Validate and normalize a raw card mapping from YAML data."""

    if not isinstance(raw_card, dict):
        raise ValueError(f"{source} card #{index} must be a mapping.")

    required_fields = ("meta", "title", "body")
    missing = [field for field in required_fields if not raw_card.get(field)]
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise ValueError(f"{source} card #{index} is missing required fields: {missing_fields}")

    raw_href = str(raw_card.get("href", "")).strip()
    href = raw_href or None
    raw_link_label = str(raw_card.get("link_label", "")).strip()
    link_label = raw_link_label or None

    if href is None and link_label is not None:
        raise ValueError(f"{source} card #{index} cannot define 'link_label' without 'href'.")

    return Card(
        meta=str(raw_card["meta"]).strip(),
        title=str(raw_card["title"]).strip(),
        body=str(raw_card["body"]).strip(),
        href=href,
        link_label=link_label or ("Read more" if href else None),
    )


def load_card_sections(docs_dir: Path, relative_path: str) -> dict[str, list[Card]]:
    """Load card sections from a YAML file under the docs directory."""

    raw_data = load_docs_yaml_file(docs_dir, relative_path, label="Card data")

    if isinstance(raw_data, list):
        return {
            "default": [
                _normalize_card(card, relative_path, index)
                for index, card in enumerate(raw_data, start=1)
            ]
        }

    if not isinstance(raw_data, dict):
        raise ValueError(f"Card data file must contain a list or mapping: {relative_path}")

    sections: dict[str, list[Card]] = {}
    for section_name, raw_cards in raw_data.items():
        if not isinstance(raw_cards, list):
            raise ValueError(f"Card section '{section_name}' in {relative_path} must be a list.")
        sections[str(section_name)] = [
            _normalize_card(card, f"{relative_path}:{section_name}", index)
            for index, card in enumerate(raw_cards, start=1)
        ]
    return sections


def render_card_grid(cards: list[Card]) -> str:
    """Render a validated card list as shared card-grid HTML."""

    fragments = ['<div class="opi-card-grid">']

    for card in cards:
        if card.href:
            fragments.extend(
                [
                    '  <article class="opi-card">',
                    f'    <a class="opi-card-link" href="{escape(card.href, quote=True)}">',
                    f'      <span class="opi-card-meta">{escape(card.meta)}</span>',
                    f"      <h3>{escape(card.title)}</h3>",
                    f"      <p>{escape(card.body)}</p>",
                    (
                        f'      <span class="opi-card-action">'
                        f"{escape(card.link_label or 'Read more')}"
                        "</span>"
                    ),
                    "    </a>",
                    "  </article>",
                ]
            )
            continue

        fragments.extend(
            [
                '  <article class="opi-card">',
                '    <div class="opi-card-copy">',
                f'      <span class="opi-card-meta">{escape(card.meta)}</span>',
                f"      <h3>{escape(card.title)}</h3>",
                f"      <p>{escape(card.body)}</p>",
                "    </div>",
                "  </article>",
            ]
        )

    fragments.append("</div>")
    return "\n".join(fragments)
