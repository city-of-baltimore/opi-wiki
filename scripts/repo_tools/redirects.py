"""Validation helpers for MkDocs redirect-map maintenance."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml

ALLOWED_DUPLICATE_DESTINATIONS = {
    "resources/index.md",
    "resources/reference/position-descriptions/innovation-lab/pd-civic-designer.md",
    "resources/reference/position-descriptions/directors-office/pd-data-storyteller.md",
    "resources/reference/position-descriptions/directors-office/pd-operations-analyst.md",
    "resources/reference/position-descriptions/data-and-analytics/pd-applied-data-scientist.md",
    "resources/reference/position-descriptions/innovation-lab/pd-innovation-program-manager.md",
    "resources/reference/position-descriptions/innovation-lab/pd-product-engineer-full-stack.md",
    # Added with the June 2026 reorg (PD consolidations, performance rename, CAD moves):
    "resources/reference/position-descriptions/data-and-analytics/pd-principal-data-engineer.md",
    "resources/reference/position-descriptions/innovation-lab/pd-applied-data-scientist.md",
    "resources/reference/position-descriptions/performance/pd-citistat-analyst.md",
    "resources/reference/position-descriptions/performance/pd-citistat-program-manager.md",
    "resources/reference/position-descriptions/performance/pd-deputy-chief-performance-officer.md",
    "resources/reference/position-descriptions/performance/pd-senior-performance-analyst.md",
    "about-us/our-teams/innovation-lab/cross-agency-delivery-service-definition.md",
    "what-we-do/services/cross-agency-delivery.md",
    # Added with the How We Work regroup (Organization / Handbook sub-sections):
    "how-we-work/organization/org-structure.md",
    "how-we-work/organization/team-and-roles/index.md",
    # The two operating-model omnibus pages folded into the canonical loop page:
    "how-we-work/how-work-moves-through-opi.md",
    # Our Teams folded under About Us (performance pages have 2 legacy paths each):
    "about-us/our-teams/performance/index.md",
    "about-us/our-teams/performance/about-performance.md",
    "about-us/our-teams/performance/performance-strategy.md",
    "about-us/our-teams/performance/performance-theory-of-change.md",
}


class _MkDocsConfigLoader(yaml.SafeLoader):
    """Safe loader that tolerates MkDocs Python-name and !ENV tags."""


def _construct_python_name(loader: _MkDocsConfigLoader, node: yaml.Node) -> str:
    """Treat Python-name tags as plain scalar strings for config inspection."""

    if not isinstance(node, yaml.ScalarNode):
        raise ValueError(f"Expected a scalar node for Python-name tag, got {node!r}.")
    return str(loader.construct_scalar(node))


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


_MkDocsConfigLoader.add_constructor(
    "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format",
    _construct_python_name,
)
_MkDocsConfigLoader.add_constructor("!ENV", _construct_env_default)


def load_redirect_map(config_path: Path) -> dict[str, str]:
    """Return the configured MkDocs redirect map."""

    config = yaml.load(
        config_path.read_text(encoding="utf-8"),
        Loader=_MkDocsConfigLoader,
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
