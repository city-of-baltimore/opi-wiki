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
    node_id: str
    lead: OrgPerson
    primary_value: str
    table_lead: str
    staff: tuple[OrgPerson, ...] = ()


@dataclass(frozen=True)
class OrgStructure:
    """Complete structured data for the org-structure page."""

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
        "node_id",
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
        node_id=str(raw_portfolio["node_id"]).strip(),
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


def _org_chart_node(
    person: OrgPerson,
    level: str,
    *,
    team: str | None = None,
    key: str | None = None,
    node_id: str | None = None,
) -> str:
    """Render one escaped, semantic public-leadership card."""

    attributes = [
        'class="opi-org-chart__node"',
        f'data-org-level="{escape(level, quote=True)}"',
    ]
    if key:
        attributes.append(f'data-org-key="{escape(key, quote=True)}"')
    if node_id:
        attributes.append(f'data-org-node="{escape(node_id, quote=True)}"')

    team_markup = (
        f'<span class="opi-org-chart__team">{escape(team)}</span>' if team is not None else ""
    )
    return (
        f"<div {' '.join(attributes)}>"
        f"{team_markup}"
        f'<strong class="opi-org-chart__name">{escape(person.name)}</strong>'
        f'<span class="opi-org-chart__title">{escape(person.title)}</span>'
        "</div>"
    )


def render_org_structure(structure: OrgStructure, section: str) -> str:
    """Render one org-structure section as repository-owned markup."""

    if section == "leadership_chart":
        lines = [
            '<figure class="opi-org-chart" aria-labelledby="opi-org-chart-caption">',
            '  <figcaption id="opi-org-chart-caption" class="opi-org-chart__caption">',
            "    OPI public reporting hierarchy",
            "  </figcaption>",
            '  <ul class="opi-org-chart__tree" role="list">',
            '    <li class="opi-org-chart__root">',
            "      "
            + _org_chart_node(
                structure.city_administrator,
                "city",
                node_id="CA",
            ),
            '      <ul class="opi-org-chart__branch" role="list">',
            '        <li class="opi-org-chart__executive">',
            "          "
            + _org_chart_node(
                structure.executive_director,
                "executive",
                node_id="ED",
            ),
            '          <ul class="opi-org-chart__teams" role="list">',
        ]
        for portfolio in structure.portfolios:
            lines.append('            <li class="opi-org-chart__team-item">')
            lines.append(
                "              "
                + _org_chart_node(
                    portfolio.lead,
                    "team",
                    team=portfolio.label,
                    key=portfolio.key,
                    node_id=portfolio.node_id,
                )
            )
            if portfolio.staff:
                lines.append('              <ul class="opi-org-chart__reports" role="list">')
                for member in portfolio.staff:
                    lines.append(
                        '                <li class="opi-org-chart__report-item">'
                        + _org_chart_node(member, "report", key=portfolio.key)
                        + "</li>"
                    )
                lines.append("              </ul>")
            lines.append("            </li>")
        lines.extend(
            [
                "          </ul>",
                "        </li>",
                "      </ul>",
                "    </li>",
                "  </ul>",
                "</figure>",
            ]
        )
        return "\n".join(lines)

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
        "leadership_chart, portfolio_table, team_roles."
    )


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
        lines.append(f"| {person.name} | {person.title} | {summary} |")
    lines.append("")
    return lines


def _render_team_roles(structure: OrgStructure) -> str:
    """Render the combined team-and-roles tables, grouped by team."""

    lines = _team_roles_group("Office of the Executive Director", [structure.executive_director])
    for portfolio in structure.portfolios:
        lines.extend(_team_roles_group(portfolio.label, [portfolio.lead, *portfolio.staff]))
    return "\n".join(lines).rstrip()
