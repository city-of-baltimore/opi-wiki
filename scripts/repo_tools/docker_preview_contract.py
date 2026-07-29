"""Validate the Docker preview's effective startup and health instructions."""

from __future__ import annotations

import json
import re

from scripts.repo_tools.dockerfile_source import (
    DockerfileInstruction,
    dockerfile_instructions,
)

_DOCKERFILE = "Dockerfile"
_PREVIEW_ARGUMENTS = ("uv", "run", "--no-dev", "python", "-m", "mkdocs", "serve")
_PREVIEW_COMMAND = f"CMD {json.dumps(_PREVIEW_ARGUMENTS)}"
_HEALTH_OPTIONS = (
    ("interval", "30s"),
    ("timeout", "3s"),
    ("start-period", "10s"),
    ("retries", "3"),
)
_HEALTH_ARGUMENTS = ("python", "-m", "scripts.docker_healthcheck")
_HEALTH_COMMAND = (
    "HEALTHCHECK "
    + " ".join(f"--{name}={value}" for name, value in _HEALTH_OPTIONS)
    + f" CMD {json.dumps(_HEALTH_ARGUMENTS)}"
)
_HEALTH_BODY = re.compile(
    r"^(?P<options>(?:--[a-z][a-z-]*=\S+\s+)*)(?i:cmd)\s+(?P<command>.+)$",
    flags=re.DOTALL,
)
_HEALTH_OPTION = re.compile(r"^--([a-z][a-z-]*)=(\S+)$")


def _json_arguments(text: str) -> list[object] | None:
    """Return one JSON argument vector, or ``None`` for any other command form."""

    try:
        arguments = json.loads(text)
    except json.JSONDecodeError:
        return None
    return arguments if isinstance(arguments, list) else None


def _health_contract(
    instruction: DockerfileInstruction,
) -> tuple[tuple[tuple[str, str], ...], list[object]] | None:
    """Return the health options and JSON command, or ``None`` for another form."""

    match = _HEALTH_BODY.fullmatch(instruction.body)
    if match is None:
        return None
    options: list[tuple[str, str]] = []
    for token in match.group("options").split():
        option = _HEALTH_OPTION.fullmatch(token)
        if option is None:
            return None
        options.append((option.group(1), option.group(2)))
    arguments = _json_arguments(match.group("command").strip())
    if arguments is None:
        return None
    return tuple(options), arguments


def find_docker_preview_contract_issues(dockerfile_text: str) -> list[str]:
    """Require one exact preview command, exact health probe, and no entrypoint."""

    instructions = dockerfile_instructions(dockerfile_text)
    commands = tuple(instruction for instruction in instructions if instruction.keyword == "cmd")
    health_checks = tuple(
        instruction for instruction in instructions if instruction.keyword == "healthcheck"
    )
    entrypoints = tuple(
        instruction for instruction in instructions if instruction.keyword == "entrypoint"
    )

    issues: list[str] = []
    if len(commands) != 1:
        issues.append(
            f"{_DOCKERFILE}: must define exactly one effective preview CMD; found {len(commands)}"
        )
    elif _json_arguments(commands[0].body) != list(_PREVIEW_ARGUMENTS):
        issues.append(f"{_DOCKERFILE}: sole preview command must be {_PREVIEW_COMMAND!r}")

    if len(health_checks) != 1:
        issues.append(
            f"{_DOCKERFILE}: must define exactly one effective HEALTHCHECK; "
            f"found {len(health_checks)}"
        )
    else:
        health_contract = _health_contract(health_checks[0])
        if health_contract is None:
            issues.append(f"{_DOCKERFILE}: sole health check must be {_HEALTH_COMMAND}")
        else:
            options, arguments = health_contract
            if (
                len(options) != len(_HEALTH_OPTIONS)
                or dict(options) != dict(_HEALTH_OPTIONS)
                or arguments != list(_HEALTH_ARGUMENTS)
            ):
                issues.append(f"{_DOCKERFILE}: sole health check must be {_HEALTH_COMMAND}")

    if entrypoints:
        issues.append(f"{_DOCKERFILE}: must not define an ENTRYPOINT; found {len(entrypoints)}")
    return issues
