"""Shared loaders and renderers for the OPI org-structure page."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any

from scripts.repo_tools.data import load_docs_yaml_file


@dataclass(frozen=True)
class OrgPerson:
    """A named org-chart node, with an optional public role summary."""

    name: str
    title: str
    summary: str = ""


@dataclass(frozen=True)
class Portfolio:
    """Structured portfolio data for the org-structure page."""

    key: str
    label: str
    lead: OrgPerson
    primary_value: str
    table_lead: str
    staff: tuple[OrgPerson, ...] = ()


@dataclass(frozen=True)
class OrgStructure:
    """Complete structured data for the org-structure page."""

    mayor: OrgPerson
    city_administrator: OrgPerson
    executive_director: OrgPerson
    portfolios: list[Portfolio]


def _normalize_person(raw_person: Any, source: str) -> OrgPerson:
    """Validate and normalize a person mapping from YAML data."""

    if not isinstance(raw_person, dict):
        raise ValueError(f"{source} must be a mapping.")

    missing = [field for field in ("name", "title") if not str(raw_person.get(field, "")).strip()]
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise ValueError(f"{source} is missing required fields: {missing_fields}")

    return OrgPerson(
        name=str(raw_person["name"]).strip(),
        title=str(raw_person["title"]).strip(),
        summary=str(raw_person.get("summary", "")).strip(),
    )


def _normalize_portfolio(raw_portfolio: Any, index: int, source: str) -> Portfolio:
    """Validate and normalize a portfolio mapping from YAML data."""

    if not isinstance(raw_portfolio, dict):
        raise ValueError(f"{source} portfolio #{index} must be a mapping.")

    required_fields = (
        "key",
        "label",
        "lead",
        "primary_value",
        "table_lead",
    )
    missing = [field for field in required_fields if not raw_portfolio.get(field)]
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise ValueError(
            f"{source} portfolio #{index} is missing required fields: {missing_fields}"
        )

    raw_staff = raw_portfolio.get("staff") or []
    if not isinstance(raw_staff, list):
        raise ValueError(f"{source} portfolio #{index} 'staff' must be a list when present.")

    return Portfolio(
        key=str(raw_portfolio["key"]).strip(),
        label=str(raw_portfolio["label"]).strip(),
        lead=_normalize_person(raw_portfolio["lead"], f"{source} portfolio #{index} lead"),
        primary_value=str(raw_portfolio["primary_value"]).strip(),
        table_lead=str(raw_portfolio["table_lead"]).strip(),
        staff=tuple(
            _normalize_person(member, f"{source} portfolio #{index} staff #{member_index}")
            for member_index, member in enumerate(raw_staff, start=1)
        ),
    )


def load_org_structure(docs_dir: Path, relative_path: str) -> OrgStructure:
    """Load structured org data from a YAML file under the docs directory."""

    raw_data = load_docs_yaml_file(docs_dir, relative_path, label="Org-structure data")

    if not isinstance(raw_data, dict):
        raise ValueError(f"Org-structure data file must contain a mapping: {relative_path}")

    raw_portfolios = raw_data.get("portfolios")
    if not isinstance(raw_portfolios, list) or not raw_portfolios:
        raise ValueError(f"{relative_path} must define a non-empty 'portfolios' list.")

    return OrgStructure(
        mayor=_normalize_person(
            raw_data.get("mayor"),
            f"{relative_path}:mayor",
        ),
        city_administrator=_normalize_person(
            raw_data.get("city_administrator"),
            f"{relative_path}:city_administrator",
        ),
        executive_director=_normalize_person(
            raw_data.get("executive_director"),
            f"{relative_path}:executive_director",
        ),
        portfolios=[
            _normalize_portfolio(portfolio, index, relative_path)
            for index, portfolio in enumerate(raw_portfolios, start=1)
        ],
    )


def _display_name(person: OrgPerson) -> str:
    """Return the public name shown in an org-chart card."""

    if person.name.strip().lower() == "open":
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

    if section == "team_reports_table":
        return _render_team_reports_table(structure)

    if section == "portfolio_table":
        lines = [
            "| **Team** | **Lead** | **Primary value** |",
            "| --- | --- | --- |",
        ]
        for portfolio in structure.portfolios:
            row = f"| {portfolio.label} | {portfolio.table_lead} | {portfolio.primary_value} |"
            lines.append(row)
        return "\n".join(lines)

    if section == "team_roles":
        return _render_team_roles(structure)

    raise ValueError(
        f"Unknown org-structure section '{section}'. Expected one of: "
        "leadership_chart, team_reports_table, portfolio_table, team_roles."
    )


def _report_label(person: OrgPerson) -> str:
    """Label a report by name, or by the title marked open for a vacancy."""

    if person.name.strip().lower() == "open":
        return f"{person.title} (Vacant)"
    return person.name


def _render_team_reports_table(structure: OrgStructure) -> str:
    """Render the four teams as a table: team, its lead, and the lead's reports."""

    lines = [
        "| **Team** | **Lead** | **Reports** |",
        "| --- | --- | --- |",
    ]
    for portfolio in structure.portfolios:
        reports = " · ".join(_report_label(person) for person in portfolio.staff)
        lines.append(f"| {portfolio.label} | {portfolio.table_lead} | {reports} |")
    return "\n".join(lines)


def _team_roles_group(heading: str, people: list[OrgPerson]) -> list[str]:
    """Render one team's roles table: name, title, and what the role does."""

    lines = [
        f"## {heading}",
        "",
        "| Name | Title | What the role does |",
        "| --- | --- | --- |",
    ]
    for person in people:
        summary = person.summary or ""
        lines.append(f"| {_display_name(person)} | {person.title} | {summary} |")
    lines.append("")
    return lines


def _render_team_roles(structure: OrgStructure) -> str:
    """Render the combined team-and-roles tables, grouped by team."""

    # The Executive Director leads a group of one; the heading uses the role
    # title rather than "office" framing so it does not read as an office of one.
    lines = _team_roles_group(
        "Executive Director and Chief Data Officer",
        [structure.executive_director],
    )
    for portfolio in structure.portfolios:
        lines.extend(_team_roles_group(portfolio.label, [portfolio.lead, *portfolio.staff]))
    return "\n".join(lines).rstrip()
