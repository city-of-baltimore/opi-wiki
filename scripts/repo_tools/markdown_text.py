"""Inert text rendering for data inserted into authored Markdown."""

from __future__ import annotations

from html import escape

# Python-Markdown and the configured PyMdown extensions can activate all of
# these characters as markup, links, mentions, or references. Numeric entities
# preserve their visible characters while keeping every parser stage inert.
_ACTIVE_MARKDOWN_CHARACTERS = frozenset("\\`*_[]{}()<>!|~^#+=-:@./")


def render_inert_markdown_text(value: str) -> str:
    """Return single-line text that cannot become Markdown, HTML, or an automatic link."""

    if not isinstance(value, str):
        raise TypeError("Markdown text value must be a string.")
    if any(character in value for character in "\r\n\t\f\v"):
        raise ValueError("Markdown text value must be single-line text.")
    if value != value.strip():
        raise ValueError("Markdown text value must not have leading or trailing whitespace.")

    return "".join(
        f"&#{ord(character)};"
        if character in _ACTIVE_MARKDOWN_CHARACTERS
        else escape(character, quote=False)
        for character in value
    )
