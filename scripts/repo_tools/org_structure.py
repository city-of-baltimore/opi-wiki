"""Shared rendering helpers for OPI organization data."""

from __future__ import annotations

from html import escape

from scripts.repo_tools.markdown_text import render_inert_markdown_text
from scripts.repo_tools.organization import OrgPerson, OrgStructure, Portfolio


def _display_name(person: OrgPerson) -> str:
    """Return the name shown in an org-chart card."""

    if person.is_vacant:
        return "(Vacant)"
    return person.name


def _org_chart_node(
    person: OrgPerson,
    level: str,
    *,
    class_name: str = "",
    accent: str = "",
) -> str:
    """Render one escaped, semantic org-chart card."""

    classes = "opi-org-chart__node"
    if class_name:
        classes = f"{classes} {class_name}"
    accent_attr = f' data-org-accent="{escape(accent, quote=True)}"' if accent else ""

    return (
        f'<div class="{classes}" '
        f'data-org-level="{escape(level, quote=True)}"{accent_attr}>'
        f'<span class="opi-org-chart__title">{escape(person.title)}</span>'
        f'<strong class="opi-org-chart__name">{escape(_display_name(person))}</strong>'
        "</div>"
    )


def _team_node(label: str, accent: str) -> str:
    """Render a lightweight team grouping node inside the chart."""

    return (
        '<div class="opi-org-chart__node opi-org-chart__node--team" '
        f'data-org-level="team" data-org-accent="{escape(accent, quote=True)}">'
        f'<strong class="opi-org-chart__name">{escape(label)}</strong>'
        "</div>"
    )


def _portfolio_by_key(structure: OrgStructure, key: str) -> Portfolio:
    """Return one portfolio by key, failing clearly if the source data drifts."""

    for portfolio in structure.portfolios:
        if portfolio.key == key:
            return portfolio
    raise ValueError(f"Org-structure data is missing required portfolio: {key}")


def _staff_stack(people: tuple[OrgPerson, ...], accent: str) -> str:
    """Render a stack of staff cards for one reporting group."""

    escaped_accent = escape(accent, quote=True)
    opening = f'      <div class="opi-org-chart__reports" data-org-accent="{escaped_accent}">'
    items = [
        "        "
        + _org_chart_node(
            person,
            "staff",
            class_name="opi-org-chart__node--staff",
            accent=accent,
        )
        for person in people
    ]
    return "\n".join(
        [
            opening,
            *items,
            "      </div>",
        ]
    )


def _lead_column(portfolio: Portfolio, accent: str) -> str:
    """Render a senior lead and direct reports as one chart column."""

    escaped_accent = escape(accent, quote=True)
    opening = f'    <section class="opi-org-chart__column" data-org-accent="{escaped_accent}">'
    return "\n".join(
        [
            opening,
            "      " + _org_chart_node(portfolio.lead, "senior-lead", accent=accent),
            _staff_stack(portfolio.staff, accent),
            "    </section>",
        ]
    )


def _data_and_innovation_column(data: Portfolio, innovation: Portfolio) -> str:
    """Render Deputy CDO, Data and Analytics, and Innovation Lab reporting lines."""

    return "\n".join(
        [
            '    <section class="opi-org-chart__column '
            'opi-org-chart__column--wide" data-org-accent="data">',
            "      " + _org_chart_node(data.lead, "senior-lead", accent="data"),
            '      <div class="opi-org-chart__split">',
            '        <section class="opi-org-chart__subcolumn" data-org-accent="data">',
            "          " + _team_node(data.label, "data"),
            _staff_stack(data.staff, "data"),
            "        </section>",
            '        <section class="opi-org-chart__subcolumn" data-org-accent="innovation">',
            "          " + _org_chart_node(innovation.lead, "manager", accent="innovation"),
            _staff_stack(innovation.staff, "innovation"),
            "        </section>",
            "      </div>",
            "    </section>",
        ]
    )


def render_org_structure(structure: OrgStructure, section: str) -> str:
    """Render one org-structure section as repository-owned markup."""

    if section == "leadership_chart":
        directors_office = _portfolio_by_key(structure, "directors-office")
        performance = _portfolio_by_key(structure, "performance")
        data = _portfolio_by_key(structure, "data-and-analytics")
        innovation = _portfolio_by_key(structure, "innovation-lab")
        return "\n".join(
            [
                '<figure class="opi-org-chart" aria-labelledby="opi-org-chart-caption">',
                '  <figcaption id="opi-org-chart-caption" class="opi-org-chart__caption">',
                "    Mayor's Office of Performance and Innovation organizational structure",
                "  </figcaption>",
                '  <div class="opi-org-chart__leadership">',
                "    "
                + _org_chart_node(
                    structure.mayor, "mayor", class_name="opi-org-chart__node--plain"
                ),
                "    "
                + _org_chart_node(
                    structure.city_administrator,
                    "city",
                    class_name="opi-org-chart__node--plain",
                ),
                "    " + _org_chart_node(structure.executive_director, "executive"),
                "  </div>",
                '  <div class="opi-org-chart__columns">',
                _lead_column(directors_office, "directors-office"),
                _lead_column(performance, "performance"),
                _data_and_innovation_column(data, innovation),
                "  </div>",
                "</figure>",
            ]
        )

    if section == "team_roles":
        return _render_team_roles(structure)

    raise ValueError(
        f"Unknown org-structure section '{section}'. Expected one of: leadership_chart, team_roles."
    )


def _team_roles_group(heading: str, people: list[OrgPerson]) -> list[str]:
    """Render one team's roles table: name, title, and what the role does."""

    lines = [
        f"## {render_inert_markdown_text(heading)}",
        "",
        "| Name | Title | What the role does |",
        "| --- | --- | --- |",
    ]
    for person in people:
        lines.append(
            f"| {render_inert_markdown_text(_display_name(person))} "
            f"| {render_inert_markdown_text(person.title)} "
            f"| {render_inert_markdown_text(person.summary)} |"
        )
    lines.append("")
    return lines


def _render_team_roles(structure: OrgStructure) -> str:
    """Render the combined team-and-roles tables, grouped by team."""

    # The Executive Director leads a group of one; the heading uses the role
    # title rather than "office" framing so it does not read as an office of one.
    lines = _team_roles_group(
        structure.executive_director.title,
        [structure.executive_director],
    )
    for portfolio in structure.portfolios:
        lines.extend(_team_roles_group(portfolio.label, [portfolio.lead, *portfolio.staff]))
    return "\n".join(lines).rstrip()
