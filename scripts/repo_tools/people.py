"""Shared loaders and renderers for the canonical OPI people directory.

One YAML file (``docs/_data/people.yml``) is the single source of truth for
staff and contractors. These helpers render it into the team roster, the
position-description index, the "OPI at a glance" stats, and inline role
lookups, so every surface stays in sync from one file.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts.repo_tools.data import load_docs_yaml_file

CONTRACTOR_TYPES = frozenset({"contractor", "offshore-contractor"})
_LOCATION_LABEL = {"contractor": "Onshore", "offshore-contractor": "Offshore"}


def load_people(docs_dir: Path, relative_path: str) -> dict[str, Any]:
    """Load the raw people directory mapping from a YAML file under docs."""

    data = load_docs_yaml_file(docs_dir, relative_path, label="People data")
    if not isinstance(data, dict):
        raise ValueError(f"People data file must contain a mapping: {relative_path}")
    if not isinstance(data.get("portfolios"), list) or not data["portfolios"]:
        raise ValueError(f"{relative_path} must define a non-empty 'portfolios' list.")
    return data


def _team_people(portfolio: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a portfolio's lead followed by its staff, as person mappings."""

    people = [portfolio["lead"], *portfolio.get("staff", [])]
    return [p for p in people if isinstance(p, dict)]


def _is_contractor(person: dict[str, Any]) -> bool:
    return str(person.get("worker_type", "staff")) in CONTRACTOR_TYPES


def _iter_staff_by_team(data: dict[str, Any]) -> list[tuple[str, list[dict[str, Any]]]]:
    """Yield (team label, staff people) pairs, with the ED under Director's Office."""

    ed = data.get("executive_director")
    result: list[tuple[str, list[dict[str, Any]]]] = []
    for portfolio in data["portfolios"]:
        staff = [p for p in _team_people(portfolio) if not _is_contractor(p)]
        if portfolio.get("key") == "directors-office" and isinstance(ed, dict):
            staff = [ed, *staff]
        if staff:
            result.append((str(portfolio["label"]), staff))
    return result


def _all_people_with_team(data: dict[str, Any]) -> list[tuple[dict[str, Any], str]]:
    """Every person (ED first) paired with their team label."""

    result: list[tuple[dict[str, Any], str]] = []
    ed = data.get("executive_director")
    directors_office = next(
        (pf for pf in data["portfolios"] if pf.get("key") == "directors-office"), None
    )
    if isinstance(ed, dict) and directors_office is not None:
        result.append((ed, str(directors_office["label"])))
    for pf in data["portfolios"]:
        for p in _team_people(pf):
            result.append((p, str(pf["label"])))
    return result


def _status_label(person: dict[str, Any]) -> str:
    return "Open" if str(person.get("status", "filled")) == "open" else "Filled"


def _cell(value: Any) -> str:
    return str(value).strip() if value not in (None, "") else ""


def render_people(data: dict[str, Any], section: str) -> str:
    """Render one people-directory section as Markdown."""

    if section == "pd_index":
        return _render_pd_index(data)
    if section == "roster":
        return _render_roster(data)
    if section == "contractors":
        return _render_contractors(data)
    if section == "cost_centers":
        return _render_cost_centers(data)
    if section == "summary":
        return _render_summary(data)
    raise ValueError(
        "Unknown people section "
        f"'{section}'. Expected one of: pd_index, roster, contractors, cost_centers, summary."
    )


def _render_pd_index(data: dict[str, Any]) -> str:
    """Group roles by team and link each to its position description.

    One row per PD document: roles that share a PD (e.g. the CitiStat
    Analysts) collapse to a single entry, marked Filled when anyone holds it.
    """

    blocks: list[str] = []
    for team, staff in _iter_staff_by_team(data):
        seen: dict[str, dict[str, Any]] = {}
        for p in staff:
            pd = _cell(p.get("pd"))
            if not pd:
                continue
            existing = seen.get(pd)
            if existing is None:
                seen[pd] = dict(p)
            elif _status_label(p) == "Filled":
                existing["status"] = "filled"
        if not seen:
            continue
        blocks.append(f"### {team}")
        blocks.append("")
        blocks.append("| Role | Classification | Reports to | Status |")
        blocks.append("| --- | --- | --- | --- |")
        for pd, p in seen.items():
            link = f"[{_cell(p['title'])}]({pd})"
            blocks.append(
                f"| {link} | {_cell(p.get('classification'))} | "
                f"{_cell(p.get('reports_to'))} | {_status_label(p)} |"
            )
        blocks.append("")
    return "\n".join(blocks).rstrip()


def _render_roster(data: dict[str, Any]) -> str:
    """Render the full roster: leadership, per-team tables, open roles, contractors."""

    blocks: list[str] = []

    # Leadership: the ED plus each staffed portfolio lead.
    leaders = [data["executive_director"]] + [
        pf["lead"]
        for pf in data["portfolios"]
        if not _is_contractor(pf["lead"])
    ]
    blocks.append('??? info "Leadership"')
    blocks.append("")
    blocks.append("    | Role | Incumbent | Reports to | PIN |")
    blocks.append("    | --- | --- | --- | --- |")
    for p in leaders:
        blocks.append(
            f"    | {_cell(p['title'])} | {_cell(p['name'])} | "
            f"{_cell(p.get('reports_to'))} | {_cell(p.get('pin'))} |"
        )
    blocks.append("")

    # Per-team rosters.
    for team, staff in _iter_staff_by_team(data):
        blocks.append(f'??? info "{team} roster"')
        blocks.append("")
        blocks.append(
            "    | Name | Working title | Classification | Cost center | PIN | Email | Work phone |"
        )
        blocks.append("    | --- | --- | --- | --- | --- | --- | --- |")
        for p in staff:
            blocks.append(
                f"    | {_cell(p['name'])} | {_cell(p['title'])} | "
                f"{_cell(p.get('classification'))} | {_cell(p.get('cost_center'))} | "
                f"{_cell(p.get('pin'))} | {_cell(p.get('email'))} | {_cell(p.get('phone'))} |"
            )
        blocks.append("")

    # Open positions.
    open_roles = [
        (p, str(pf["label"]))
        for pf in data["portfolios"]
        for p in _team_people(pf)
        if str(p.get("status", "filled")) == "open"
    ]
    if open_roles:
        blocks.append('??? info "Open positions"')
        blocks.append("")
        blocks.append("    | Title | Team | PIN |")
        blocks.append("    | --- | --- | --- |")
        for p, team in open_roles:
            blocks.append(f"    | {_cell(p['title'])} | {team} | {_cell(p.get('pin'))} |")
        blocks.append("")

    return "\n".join(blocks).rstrip()


def _render_contractors(data: dict[str, Any]) -> str:
    """List embedded contractors by team as a self-contained admonition."""

    contractors = [
        (p, str(pf["label"]))
        for pf in data["portfolios"]
        for p in _team_people(pf)
        if _is_contractor(p)
    ]
    if not contractors:
        return ""
    lines = ['??? info "Contractors by team"', ""]
    lines.append("    | Name | Role | Team | Location |")
    lines.append("    | --- | --- | --- | --- |")
    for p, team in contractors:
        location = _cell(p.get("location")) or _LOCATION_LABEL.get(
            str(p.get("worker_type")), ""
        )
        lines.append(f"    | {_cell(p['name'])} | {_cell(p['title'])} | {team} | {location} |")
    return "\n".join(lines).rstrip()


def _render_cost_centers(data: dict[str, Any]) -> str:
    """Group staff by funding cost center as a self-contained admonition."""

    groups: dict[str, list[tuple[dict[str, Any], str]]] = {}
    for person, team in _all_people_with_team(data):
        if _is_contractor(person):
            continue
        cc = _cell(person.get("cost_center")) or "Unassigned"
        groups.setdefault(cc, []).append((person, team))

    lines = ['??? info "Cost center view"', ""]
    lines.append(
        "    OPI's budget is organized into cost centers. The same person may sit on a "
        "team that does not match their cost center — the Data Storyteller, for example, "
        "sits in the Director's Office while funded in the Innovation Lab cost center."
    )
    lines.append("")
    for cc in sorted(groups):
        lines.append(f"    **{cc}**")
        lines.append("")
        lines.append("    | Working title | Incumbent | Team | PIN |")
        lines.append("    | --- | --- | --- | --- |")
        for person, team in groups[cc]:
            lines.append(
                f"    | {_cell(person['title'])} | {_cell(person['name'])} | "
                f"{team} | {_cell(person.get('pin'))} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip()


def _render_summary(data: dict[str, Any]) -> str:
    """Render the 'OPI at a glance' counts, computed from the directory."""

    all_people = [data["executive_director"]] + [
        p for pf in data["portfolios"] for p in _team_people(pf)
    ]
    staff = [p for p in all_people if not _is_contractor(p)]
    filled = [p for p in staff if str(p.get("status", "filled")) == "filled"]
    open_roles = [p for p in staff if str(p.get("status", "filled")) == "open"]
    contractors = [p for p in all_people if _is_contractor(p)]
    teams = [pf["label"] for pf in data["portfolios"] if not _is_contractor(pf["lead"])]

    rows = [
        ("Total positions", str(len(staff))),
        ("Filled", str(len(filled))),
        ("Open / unfilled", str(len(open_roles))),
        ("Teams", f"{len(teams)} ({', '.join(teams)})"),
        (
            "Contractors",
            f"{len(contractors)} embedded across Data and Analytics, "
            "Innovation Lab, and AI Enablement (BIC)",
        ),
    ]
    lines = ["| | |", "| --- | --- |"]
    lines.extend(f"| **{label}** | {value} |" for label, value in rows)
    return "\n".join(lines)


def find_role_holder(data: dict[str, Any], title: str) -> str:
    """Return the name of the filled person holding the given working title."""

    wanted = title.strip().casefold()
    for pf in data["portfolios"]:
        for p in _team_people(pf):
            if str(p.get("title", "")).strip().casefold() == wanted and not _is_contractor(p):
                if str(p.get("status", "filled")) == "filled":
                    return str(p["name"]).strip()
    ed = data.get("executive_director", {})
    if str(ed.get("title", "")).strip().casefold() == wanted:
        return str(ed["name"]).strip()
    raise ValueError(f"No filled role holder found for title '{title}'.")
