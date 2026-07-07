"""Shared loaders and renderers for the OPI org-structure page."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from textwrap import wrap
from typing import Any

from scripts.repo_tools.data import load_docs_yaml_file

MERMAID_LABEL_WRAP = 26

WORKER_TYPES = frozenset({"staff", "contractor", "offshore-contractor"})
_WORKER_MERMAID_CLASS = {"contractor": "contractor", "offshore-contractor": "offshore"}
_WORKER_ROSTER_TAG = {
    "contractor": "(Contractor)",
    "offshore-contractor": "(Contractor · offshore)",
}
_MERMAID_CLASSDEFS = (
    "  classDef contractor fill:#7e57c2,stroke:#5e35b1,color:#ffffff;",
    "  classDef offshore fill:#78909c,stroke:#546e7a,color:#ffffff;",
)


@dataclass(frozen=True)
class OrgPerson:
    """A named org-chart node."""

    name: str
    title: str
    edge_style: str = "solid"
    worker_type: str = "staff"


@dataclass(frozen=True)
class Portfolio:
    """Structured portfolio data for the org-structure page."""

    key: str
    label: str
    node_id: str
    lead: OrgPerson
    cost_center: str
    primary_value: str
    table_lead: str
    staff: list[OrgPerson]
    leadership_edge_style: str = "solid"
    leadership_edge_label: str | None = None
    staff_alignment_note: str | None = None


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

    edge_style = str(raw_person.get("edge_style", "solid")).strip() or "solid"
    if edge_style not in {"solid", "dotted"}:
        raise ValueError(f"{source} has unsupported edge_style '{edge_style}'.")

    worker_type = str(raw_person.get("worker_type", "staff")).strip() or "staff"
    if worker_type not in WORKER_TYPES:
        raise ValueError(f"{source} has unsupported worker_type '{worker_type}'.")

    return OrgPerson(
        name=str(raw_person["name"]).strip(),
        title=str(raw_person["title"]).strip(),
        edge_style=edge_style,
        worker_type=worker_type,
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
        "cost_center",
        "primary_value",
        "table_lead",
        "staff",
    )
    missing = [field for field in required_fields if not raw_portfolio.get(field)]
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise ValueError(
            f"{source} portfolio #{index} is missing required fields: {missing_fields}"
        )

    raw_staff = raw_portfolio["staff"]
    if not isinstance(raw_staff, list):
        raise ValueError(f"{source} portfolio #{index} field 'staff' must be a list.")

    leadership_edge_style = (
        str(raw_portfolio.get("leadership_edge_style", "solid")).strip() or "solid"
    )
    if leadership_edge_style not in {"solid", "dotted"}:
        raise ValueError(
            f"{source} portfolio #{index} has unsupported leadership_edge_style "
            f"'{leadership_edge_style}'."
        )

    return Portfolio(
        key=str(raw_portfolio["key"]).strip(),
        label=str(raw_portfolio["label"]).strip(),
        node_id=str(raw_portfolio["node_id"]).strip(),
        lead=_normalize_person(raw_portfolio["lead"], f"{source} portfolio #{index} lead"),
        cost_center=str(raw_portfolio["cost_center"]).strip(),
        primary_value=str(raw_portfolio["primary_value"]).strip(),
        table_lead=str(raw_portfolio["table_lead"]).strip(),
        staff=[
            _normalize_person(person, f"{source} portfolio #{index} staff #{staff_index}")
            for staff_index, person in enumerate(raw_staff, start=1)
        ],
        leadership_edge_style=leadership_edge_style,
        leadership_edge_label=str(raw_portfolio.get("leadership_edge_label", "")).strip() or None,
        staff_alignment_note=str(raw_portfolio.get("staff_alignment_note", "")).strip() or None,
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


def _mermaid_node(node_id: str, *parts: str, css_class: str | None = None) -> str:
    """Render a Mermaid node with escaped HTML line breaks."""

    label_lines: list[str] = []
    for part in parts:
        label_lines.extend(
            wrap(
                part.strip(),
                width=MERMAID_LABEL_WRAP,
                break_long_words=False,
                break_on_hyphens=False,
            )
            or [part.strip()]
        )

    label = "<br/>".join(
        escape(line, quote=False).replace('"', "&quot;")
        for line in label_lines
    )
    node = f'  {node_id}["{label}"]'
    if css_class:
        node = f"{node}:::{css_class}"
    return node


def _mermaid_edge(origin: str, target: str, style: str = "solid", label: str | None = None) -> str:
    """Render a Mermaid edge with optional text."""

    if style == "solid":
        connector = "-->"
        return f"  {origin} {connector} {target}"

    if style == "dotted":
        if label:
            return f"  {origin} -. {escape(label)} .-> {target}"
        return f"  {origin} -.-> {target}"

    raise ValueError(f"Unsupported Mermaid edge style '{style}'.")


def render_org_structure(structure: OrgStructure, section: str) -> str:
    """Render one org-structure section as Markdown."""

    if section == "leadership_chart":
        lines = [
            "```mermaid",
            "flowchart TD",
            *_MERMAID_CLASSDEFS,
            _mermaid_node(
                "CA",
                structure.city_administrator.name,
                structure.city_administrator.title,
            ),
            _mermaid_node(
                "ED",
                structure.executive_director.name,
                structure.executive_director.title,
            ),
        ]
        for portfolio in structure.portfolios:
            lines.append(
                _mermaid_node(
                    portfolio.node_id,
                    portfolio.label,
                    portfolio.lead.name,
                    portfolio.lead.title,
                    css_class=_WORKER_MERMAID_CLASS.get(portfolio.lead.worker_type),
                )
            )
        lines.extend(
            [
                "",
                _mermaid_edge("CA", "ED"),
            ]
        )
        for portfolio in structure.portfolios:
            lines.append(
                _mermaid_edge(
                    "ED",
                    portfolio.node_id,
                    style=portfolio.leadership_edge_style,
                    label=portfolio.leadership_edge_label,
                )
            )
        lines.append("```")
        return "\n".join(lines)

    if section == "staff_cards":
        tab_blocks: list[str] = []
        for portfolio in structure.portfolios:
            lines = [f'=== "{portfolio.label}"', ""]
            cards = ['    <div class="opi-org-grid">']
            people = [(portfolio.lead, True)] + [(p, False) for p in portfolio.staff]
            for person, is_lead in people:
                classes = ["opi-org-card"]
                if is_lead:
                    classes.append("opi-org-card--lead")
                if person.worker_type == "contractor":
                    classes.append("opi-org-card--contractor")
                elif person.worker_type == "offshore-contractor":
                    classes.append("opi-org-card--offshore")
                if person.name.casefold() in {"vacant", "tbd", "open — recruiting"}:
                    classes.append("opi-org-card--open")
                tag = _WORKER_ROSTER_TAG.get(person.worker_type, "")
                tag_html = (
                    f'<span class="opi-org-card__tag">{escape(tag.strip("()"))}</span>'
                    if tag
                    else ""
                )
                cards.append(
                    f'      <div class="{" ".join(classes)}">'
                    f'<span class="opi-org-card__name">{escape(person.name)}</span>'
                    f'<span class="opi-org-card__title">{escape(person.title)}</span>'
                    f"{tag_html}</div>"
                )
            cards.append("    </div>")
            lines.extend(cards)
            lines.append("")
            tab_blocks.extend(lines)
        return "\n".join(tab_blocks).rstrip()

    if section == "portfolio_table":
        lines = [
            "| **Team** | **Lead** | **Cost Center** | **Primary Value** |",
            "|--------------------------|----------------------------------------------------------------------------------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------|",
        ]
        for portfolio in structure.portfolios:
            row = (
                f"| {portfolio.label} | {portfolio.table_lead} | "
                f"{portfolio.cost_center} | {portfolio.primary_value} |"
            )
            lines.append(row)
        return "\n".join(lines)

    if section == "staff_alignment":
        blocks: list[str] = []
        for portfolio in structure.portfolios:
            blocks.append(f"**{portfolio.label}**")
            blocks.append("")
            if portfolio.staff_alignment_note:
                blocks.append(portfolio.staff_alignment_note)
                blocks.append("")
                continue

            lead_tag = _WORKER_ROSTER_TAG.get(portfolio.lead.worker_type)
            lead_suffix = f" {lead_tag}" if lead_tag else ""
            blocks.append(f"- {portfolio.lead.name} — {portfolio.lead.title}{lead_suffix}")
            blocks.append("")
            for person in portfolio.staff:
                tag = _WORKER_ROSTER_TAG.get(person.worker_type)
                suffix = f" {tag}" if tag else ""
                blocks.append(f"- {person.name} — {person.title}{suffix}")
                blocks.append("")
        return "\n".join(blocks).rstrip()

    raise ValueError(
        f"Unknown org-structure section '{section}'. Expected one of: "
        "leadership_chart, staff_cards, portfolio_table, staff_alignment."
    )
