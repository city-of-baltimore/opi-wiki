"""Helpers for rendering the shared page header component.

The page header is the canonical eyebrow + summary block that replaces the
hand-built stack of ``{{ page_badge() }}``, a blockquote summary, a bold
category kicker, a duplicated bold title, and an italic tagline that pages used
to repeat by hand. Driving it through one macro keeps the markup consistent and
accessible (the page title stays a single ``<h1>`` instead of being restated as
a bold paragraph).
"""

from __future__ import annotations

from html import escape

from scripts.repo_tools.badges import render_badge


def render_page_header(
    badge_value: str,
    *,
    summary: str | None = None,
    category: str | None = None,
    tagline: str | None = None,
) -> str:
    """Render the shared page header as HTML.

    Args:
        badge_value: The badge token to render in the eyebrow row.
        summary: Optional one-line lede describing the page.
        category: Optional short category label shown before the badge.
        tagline: Optional supporting italic line shown under the summary.

    Returns:
        The page header markup as an HTML string.
    """

    summary = (summary or "").strip()
    category = (category or "").strip()
    tagline = (tagline or "").strip()

    eyebrow = ['  <p class="opi-page-header__eyebrow">']
    if category:
        eyebrow.append(
            f'<span class="opi-page-header__category">{escape(category)}</span>'
        )
    eyebrow.append(render_badge(badge_value))
    eyebrow.append("</p>")

    fragments = ['<div class="opi-page-header">', "".join(eyebrow)]
    if summary:
        fragments.append(
            f'  <p class="opi-page-header__summary">{escape(summary)}</p>'
        )
    if tagline:
        fragments.append(
            f'  <p class="opi-page-header__tagline">{escape(tagline)}</p>'
        )
    fragments.append("</div>")
    return "\n".join(fragments)
