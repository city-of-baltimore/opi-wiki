"""Hold the source-level browser readiness architecture in hosted CI."""

from __future__ import annotations

import ast
from collections.abc import Mapping, Sequence
from io import StringIO
from pathlib import Path

import yaml
from mkdocs.utils.yaml import yaml_load
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode

from scripts.repo_tools.docker_preview_contract import (
    find_docker_preview_contract_issues,
)
from scripts.repo_tools.dockerfile_source import effective_dockerfile_environment

REPO_ROOT = Path(__file__).resolve().parents[2]
BROWSER_READINESS_SEAM = Path("scripts/repo_tools/browser_routes.py")
BROWSER_RUNTIME_PATHS = (
    Path("scripts/repo_tools/browser_smoke.py"),
    Path("scripts/repo_tools/browser_accessibility.py"),
)
_CONTRACT_SOURCE = Path("scripts/repo_tools/browser_readiness_contract.py")
_BANNED_WAIT_CALLS = frozenset({"wait_for_load_state", "wait_for_url"})
_MKDOCS_CONFIG = Path("mkdocs.yml")
_COMPOSE_CONFIG = Path("docker-compose.yml")
_DOCKERFILE = Path("Dockerfile")
_TASKFILE = Path("Taskfile.yml")
_SITE_URL_HOOK = Path("scripts/mkdocs_site_url.py")
_MKDOCS_DEV_ADDR_ENVIRONMENT = "MKDOCS_DEV_ADDR"
_MKDOCS_HOST_DEV_ADDR = "127.0.0.1:5208"
_DOCKER_DEV_ADDR = "0.0.0.0:8000"
_COMPOSE_SITE_URL = "http://127.0.0.1:5208/opi-wiki/"
_COMPOSE_PORT_MAPPING = "127.0.0.1:5208:8000"
_COMPOSE_SERVICE_KEYS = frozenset({"build", "environment", "ports", "volumes"})
_COMPOSE_VOLUMES = (".:/app", "/app/.venv", "/app/site")
_TASK_BUILD_COMMAND = "uv run python -m mkdocs build --strict"
_TASK_SERVE_COMMAND = f"uv run python -m mkdocs serve -a {_MKDOCS_HOST_DEV_ADDR}"


def _mapping_value(node: Node | None, name: str) -> Node | None:
    """Return a top-level YAML mapping value without constructing custom tags."""

    if not isinstance(node, MappingNode):
        return None
    matches: list[Node] = []
    for key_node, value_node in node.value:
        if (
            isinstance(key_node, ScalarNode)
            and key_node.value == name
            and isinstance(value_node, Node)
        ):
            matches.append(value_node)
    return matches[0] if len(matches) == 1 else None


def _is_expected_mkdocs_dev_addr(node: Node | None) -> bool:
    """Return whether ``dev_addr`` preserves its environment hook and safe default."""

    return (
        isinstance(node, SequenceNode)
        and node.tag == "!ENV"
        and len(node.value) == 2
        and all(isinstance(item, ScalarNode) for item in node.value)
        and [item.value for item in node.value]
        == [_MKDOCS_DEV_ADDR_ENVIRONMENT, _MKDOCS_HOST_DEV_ADDR]
    )


def _default_source_paths(repo_root: Path) -> tuple[Path, ...]:
    """Return every Python automation source governed by browser readiness."""

    candidates = list((repo_root / "scripts").rglob("*.py"))
    main_source = repo_root / "main.py"
    if main_source.is_file():
        candidates.append(main_source)
    return tuple(
        path.relative_to(repo_root)
        for path in sorted(candidates)
        if path.relative_to(repo_root) != _CONTRACT_SOURCE
    )


def _preview_wiring_issues(repo_root: Path) -> list[str]:
    """Return drift across the reviewed local-preview configuration seams."""

    try:
        mkdocs_text = (repo_root / _MKDOCS_CONFIG).read_text(encoding="utf-8")
        compose_text = (repo_root / _COMPOSE_CONFIG).read_text(encoding="utf-8")
        dockerfile_text = (repo_root / _DOCKERFILE).read_text(encoding="utf-8")
        taskfile_text = (repo_root / _TASKFILE).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise RuntimeError("Unable to read live-preview configuration") from error
    try:
        mkdocs_config = yaml_load(StringIO(mkdocs_text))
        mkdocs_source = yaml.compose(mkdocs_text, Loader=yaml.SafeLoader)
        compose_config = yaml.safe_load(compose_text)
        taskfile_config = yaml.safe_load(taskfile_text)
    except (TypeError, yaml.YAMLError) as error:
        raise RuntimeError("Unable to parse live-preview configuration") from error
    if not isinstance(mkdocs_source, MappingNode) or not all(
        isinstance(config, Mapping) for config in (mkdocs_config, compose_config, taskfile_config)
    ):
        raise RuntimeError("Live-preview configuration roots must be YAML mappings")

    issues: list[str] = []
    if not _is_expected_mkdocs_dev_addr(_mapping_value(mkdocs_source, "dev_addr")):
        issues.append(
            f"{_MKDOCS_CONFIG}: dev_addr must remain "
            f"!ENV [{_MKDOCS_DEV_ADDR_ENVIRONMENT}, {_MKDOCS_HOST_DEV_ADDR!r}]"
        )
    if mkdocs_config.get("hooks") != [str(_SITE_URL_HOOK)]:
        issues.append(f"{_MKDOCS_CONFIG}: must register {_SITE_URL_HOOK} as its sole MkDocs hook")
    try:
        wiki_service = compose_config["services"]["wiki"]
    except (KeyError, TypeError) as error:
        raise RuntimeError(f"Unable to read services.wiki from {_COMPOSE_CONFIG}") from error
    if not isinstance(wiki_service, Mapping):
        raise RuntimeError(f"services.wiki in {_COMPOSE_CONFIG} must be a YAML mapping")
    configured_keys = frozenset(wiki_service)
    if configured_keys != _COMPOSE_SERVICE_KEYS:
        found_keys = sorted(str(key) for key in configured_keys)
        issues.append(
            f"{_COMPOSE_CONFIG}: services.wiki must define only "
            f"{sorted(_COMPOSE_SERVICE_KEYS)!r}; found {found_keys!r}"
        )
    if wiki_service.get("build") != ".":
        issues.append(f"{_COMPOSE_CONFIG}: services.wiki.build must remain '.'")
    if wiki_service.get("environment") != {"OPI_SITE_URL": _COMPOSE_SITE_URL}:
        issues.append(
            f"{_COMPOSE_CONFIG}: services.wiki.environment must remain "
            f"{{'OPI_SITE_URL': {_COMPOSE_SITE_URL!r}}}"
        )
    if wiki_service.get("ports") != [_COMPOSE_PORT_MAPPING]:
        issues.append(
            f"{_COMPOSE_CONFIG}: services.wiki.ports must remain [{_COMPOSE_PORT_MAPPING!r}]"
        )
    if wiki_service.get("volumes") != list(_COMPOSE_VOLUMES):
        issues.append(
            f"{_COMPOSE_CONFIG}: services.wiki.volumes must remain {list(_COMPOSE_VOLUMES)!r}"
        )
    docker_environment = effective_dockerfile_environment(dockerfile_text)
    if docker_environment.get(_MKDOCS_DEV_ADDR_ENVIRONMENT) != _DOCKER_DEV_ADDR:
        issues.append(
            f"{_DOCKERFILE}: {_MKDOCS_DEV_ADDR_ENVIRONMENT} must remain {_DOCKER_DEV_ADDR!r}"
        )
    if not (repo_root / _SITE_URL_HOOK).is_file():
        issues.append(f"{_SITE_URL_HOOK}: registered MkDocs hook file is missing")
    try:
        build_commands = taskfile_config["tasks"]["build"]["cmds"]
        serve_commands = taskfile_config["tasks"]["serve"]["cmds"]
    except (KeyError, TypeError) as error:
        raise RuntimeError(
            f"Unable to read tasks.build.cmds or tasks.serve.cmds from {_TASKFILE}"
        ) from error
    if build_commands != [_TASK_BUILD_COMMAND]:
        issues.append(
            f"{_TASKFILE}: task build must run {_TASK_BUILD_COMMAND!r} so the "
            "registered hook can import repository code"
        )
    if serve_commands != [_TASK_SERVE_COMMAND]:
        issues.append(
            f"{_TASKFILE}: task serve must run {_TASK_SERVE_COMMAND!r} so the "
            "registered hook can import repository code"
        )
    issues.extend(find_docker_preview_contract_issues(dockerfile_text))
    return issues


def find_browser_readiness_contract_issues(
    repo_root: Path = REPO_ROOT,
    *,
    source_paths: Sequence[Path] | None = None,
) -> list[str]:
    """Reject browser lifecycle calls outside the shared seam across repo automation."""

    required_paths = (BROWSER_READINESS_SEAM, *BROWSER_RUNTIME_PATHS)
    for relative_path in required_paths:
        if not (repo_root / relative_path).is_file():
            raise RuntimeError(
                f"Unable to read browser runtime source: {repo_root / relative_path}"
            )
    selected_paths = (
        tuple(source_paths) if source_paths is not None else _default_source_paths(repo_root)
    )

    issues = _preview_wiring_issues(repo_root)
    for relative_path in selected_paths:
        path = repo_root / relative_path
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise RuntimeError(f"Unable to read browser runtime source: {path}") from error
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as error:
            raise RuntimeError(
                f"Unable to parse browser runtime source: {path}: {error}"
            ) from error

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value.casefold() == "networkidle"
            ):
                issues.append(
                    f"{relative_path}:{node.lineno}: networkidle is not a valid "
                    "readiness signal for MkDocs live preview"
                )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in _BANNED_WAIT_CALLS
            ):
                issues.append(
                    f"{relative_path}:{node.lineno}: page.{node.func.attr}() is not "
                    "a supported browser readiness signal"
                )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "goto"
                and relative_path != BROWSER_READINESS_SEAM
            ):
                issues.append(
                    f"{relative_path}:{node.lineno}: page.goto() must go through "
                    "scripts/repo_tools/browser_routes.py"
                )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "new_context"
                and relative_path != BROWSER_READINESS_SEAM
            ):
                issues.append(
                    f"{relative_path}:{node.lineno}: browser.new_context() must go "
                    "through scripts/repo_tools/browser_routes.py"
                )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "new_context"
                and relative_path == BROWSER_READINESS_SEAM
            ):
                service_workers = next(
                    (
                        keyword.value
                        for keyword in node.keywords
                        if keyword.arg == "service_workers"
                    ),
                    None,
                )
                if not (
                    isinstance(service_workers, ast.Constant) and service_workers.value == "block"
                ):
                    issues.append(
                        f"{relative_path}:{node.lineno}: browser.new_context() must "
                        "declare service_workers='block' literally"
                    )
                offline = next(
                    (keyword.value for keyword in node.keywords if keyword.arg == "offline"),
                    None,
                )
                is_static_artifact_boundary = (
                    isinstance(offline, ast.Compare)
                    and isinstance(offline.left, ast.Attribute)
                    and isinstance(offline.left.value, ast.Name)
                    and offline.left.value.id == "target"
                    and offline.left.attr == "artifact_dir"
                    and len(offline.ops) == 1
                    and isinstance(offline.ops[0], ast.IsNot)
                    and len(offline.comparators) == 1
                    and isinstance(offline.comparators[0], ast.Constant)
                    and offline.comparators[0].value is None
                )
                if not is_static_artifact_boundary:
                    issues.append(
                        f"{relative_path}:{node.lineno}: browser.new_context() must "
                        "set offline=target.artifact_dir is not None literally"
                    )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "goto"
                and relative_path == BROWSER_READINESS_SEAM
            ):
                wait_until = next(
                    (keyword.value for keyword in node.keywords if keyword.arg == "wait_until"),
                    None,
                )
                if not (isinstance(wait_until, ast.Constant) and wait_until.value == "load"):
                    issues.append(
                        f"{relative_path}:{node.lineno}: page.goto() must declare "
                        "wait_until='load' literally"
                    )
        if relative_path == BROWSER_READINESS_SEAM:
            context_calls = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "new_context"
            ]
            artifact_route_calls = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "install_canonical_artifact_route"
            ]
            live_route_calls = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_install_live_preview_transport_route"
            ]
            if (
                len(context_calls) != 1
                or len(artifact_route_calls) != 1
                or len(live_route_calls) != 1
            ):
                issues.append(
                    f"{relative_path}: the shared seam must create exactly one "
                    "browser context and install exactly one canonical artifact "
                    "route and one live-preview transport route"
                )
    return sorted(issues)
