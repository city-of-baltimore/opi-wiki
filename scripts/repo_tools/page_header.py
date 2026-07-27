"""Helpers for rendering the shared page header component.

The page header is the canonical category, summary, and tagline block. Driving
it through one macro keeps the markup consistent and accessible: the page title
stays a single ``<h1>`` instead of being restated as a bold paragraph.
"""

from __future__ import annotations

from html import escape


def render_page_header(
    *,
    summary: str | None = None,
    category: str | None = None,
    tagline: str | None = None,
) -> str:
    """Render the shared page header as HTML.

    Args:
        summary: Optional one-line lede describing the page.
        category: Optional short category label shown above the summary.
        tagline: Optional supporting italic line shown under the summary.

    Returns:
        The page header markup as an HTML string.
    """

    summary = (summary or "").strip()
    category = (category or "").strip()
    tagline = (tagline or "").strip()

    fragments = ['<div class="opi-page-header">']
    if category:
        fragments.append(
            '  <p class="opi-page-header__eyebrow">'
            f'<span class="opi-page-header__category">{escape(category)}</span>'
            "</p>"
        )
    if summary:
        fragments.append(f'  <p class="opi-page-header__summary">{escape(summary)}</p>')
    if tagline:
        fragments.append(f'  <p class="opi-page-header__tagline">{escape(tagline)}</p>')
    fragments.append("</div>")
    return "\n".join(fragments)
