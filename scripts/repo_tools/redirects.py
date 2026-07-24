"""Validation helpers for MkDocs redirect-map maintenance."""

from __future__ import annotations

from collections import Counter
from collections.abc import Hashable
from pathlib import Path
from typing import Any

import yaml

ALLOWED_DUPLICATE_DESTINATIONS = {
    "resources/index.md",
    "resources/reference/index.md",
    # Position descriptions were retired; role summaries now live on the public
    # Team and Roles page, where the legacy PD URLs converge.
    "about-us/our-teams/team-and-roles.md",
    "what-we-do/services/cross-agency-delivery/service-definition.md",
    "what-we-do/services/cross-agency-delivery/index.md",
    # Added with the How We Work regroup and public/private boundary cleanup:
    "how-we-work/organization/org-structure.md",
    "how-we-work/index.md",
    # The two operating-model omnibus pages folded into the canonical loop page:
    "how-we-work/how-work-moves-through-opi.md",
    # Our Teams folded under About Us (performance pages have 2 legacy paths each):
    "about-us/our-teams/performance/index.md",
    "about-us/our-teams/performance/about-performance.md",
    # July 2026 content consolidation: each team's About page absorbs its retired
    # Strategy and Theory-of-Change pages; the BIC 7-pager collapses to 4; the
    # CitiStat Method Playbook absorbs the Staff Quick Reference.
    "about-us/our-teams/data-and-analytics/about-data-analytics.md",
    "about-us/our-teams/innovation-lab/about-innovation-lab.md",
    "about-us/our-teams/directors-office/about-admin-ops.md",
    "what-we-do/products/baltimore-intelligence-center/index.md",
    "what-we-do/products/baltimore-intelligence-center/architecture-and-roadmap.md",
    "what-we-do/products/baltimore-intelligence-center/products-and-capabilities.md",
    "what-we-do/programs/citistat/method-playbook.md",
    # BIC's Responsible data & AI page folded into the Data Governance program.
    "what-we-do/programs/data-governance/index.md",
}


class _MkDocsConfigLoader(yaml.SafeLoader):
    """Safe loader that tolerates MkDocs !ENV tags."""

    def construct_mapping(
        self,
        node: yaml.MappingNode,
        deep: bool = False,
    ) -> dict[Any, Any]:
        """Construct a mapping while rejecting duplicate YAML keys."""

        if not isinstance(node, yaml.MappingNode):
            raise ValueError(f"Expected a YAML mapping node, got {node!r}.")

        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, Hashable):
                raise ValueError(f"Unhashable YAML mapping key at {key_node.start_mark}.")
            if key in mapping:
                line_number = key_node.start_mark.line + 1
                raise ValueError(f"Duplicate YAML key '{key}' on line {line_number}.")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def _construct_env_default(loader: _MkDocsConfigLoader, node: yaml.Node) -> str:
    """Resolve MkDocs !ENV tags to their default value for config inspection.

    ``!ENV [VAR, default]`` reads VAR at build time; for validation we only
    care about the committed default (the last sequence entry).
    """

    if isinstance(node, yaml.SequenceNode):
        values = loader.construct_sequence(node)
        return str(values[-1]) if values else ""
    if not isinstance(node, yaml.ScalarNode):
        raise ValueError(f"Expected a scalar or sequence !ENV node, got {node!r}.")
    return str(loader.construct_scalar(node))


_MkDocsConfigLoader.add_constructor("!ENV", _construct_env_default)


def load_redirect_map(config_path: Path) -> dict[str, str]:
    """Return the configured MkDocs redirect map."""

    # S506: _MkDocsConfigLoader subclasses yaml.SafeLoader — it only adds
    # a constructor for MkDocs' !ENV tag, and instantiates no arbitrary
    # objects. ruff cannot see the base class through the subclass.
    config = yaml.load(  # nosec B506
        config_path.read_text(encoding="utf-8"),
        Loader=_MkDocsConfigLoader,  # noqa: S506
    )
    plugins = config.get("plugins", [])

    for plugin in plugins:
        if isinstance(plugin, dict) and "redirects" in plugin:
            redirect_map = plugin["redirects"].get("redirect_maps", {})
            if not isinstance(redirect_map, dict):
                raise ValueError("mkdocs.yml redirects.redirect_maps must be a mapping.")
            return {str(source): str(destination) for source, destination in redirect_map.items()}

    raise ValueError("mkdocs.yml is missing the redirects plugin configuration.")


def find_redirect_issues(config_path: Path, docs_dir: Path) -> list[str]:
    """Return redirect-map issues that could cause drift or ambiguous routing."""

    redirect_map = load_redirect_map(config_path)
    issues: list[str] = []

    for source, destination in redirect_map.items():
        if source.startswith("/"):
            issues.append(f"Redirect source must be docs-relative: {source}")
        if destination.startswith("/"):
            issues.append(f"Redirect destination must be docs-relative: {destination}")
        if not source.endswith(".md"):
            issues.append(f"Redirect source must target a Markdown page: {source}")
        if not destination.endswith(".md"):
            issues.append(f"Redirect destination must target a Markdown page: {destination}")

        destination_path = docs_dir / destination
        if not destination_path.exists():
            issues.append(f"Redirect destination does not exist: {destination}")

        source_path = docs_dir / source
        if source_path.exists():
            issues.append(f"Redirect source still exists as a docs page: {source}")

    destination_counts = Counter(redirect_map.values())
    for destination, count in sorted(destination_counts.items()):
        if count <= 1 or destination in ALLOWED_DUPLICATE_DESTINATIONS:
            continue
        issues.append(
            f"Redirect destination is shared by {count} legacy paths "
            f"without an explicit allowlist: "
            f"{destination}"
        )

    return issues
