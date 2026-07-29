"""Parse reviewed source-level Dockerfile semantics for repository contracts."""

from __future__ import annotations

import re
import shlex
from dataclasses import dataclass

_DOCKERFILE = "Dockerfile"
_INSTRUCTION = re.compile(r"^([A-Za-z]+)(?:\s+(.*))?$", flags=re.DOTALL)
_ESCAPE_DIRECTIVE = re.compile(r"^#\s*escape\s*=\s*([\\`])\s*$", flags=re.IGNORECASE)
_ENVIRONMENT_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class DockerfileInstruction:
    """One effective Dockerfile instruction after line continuation."""

    keyword: str
    body: str
    line_number: int


def _has_continuation(line: str, escape_character: str) -> bool:
    """Return whether one physical Dockerfile line continues logically."""

    trailing_count = len(line) - len(line.rstrip(escape_character))
    return trailing_count % 2 == 1


def dockerfile_instructions(text: str) -> tuple[DockerfileInstruction, ...]:
    """Parse logical Dockerfile instructions without treating comments as code."""

    instructions: list[DockerfileInstruction] = []
    parts: list[str] = []
    start_line: int | None = None
    escape_character = "\\"

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not parts and not instructions:
            directive = _ESCAPE_DIRECTIVE.fullmatch(stripped)
            if directive is not None:
                escape_character = directive.group(1)
                continue
        if not stripped or stripped.startswith("#"):
            continue

        if start_line is None:
            start_line = line_number
        continued = _has_continuation(stripped, escape_character)
        if continued:
            stripped = stripped[:-1].rstrip()
        parts.append(stripped)
        if continued:
            continue

        logical_line = " ".join(part for part in parts if part)
        match = _INSTRUCTION.fullmatch(logical_line)
        if match is None:
            raise RuntimeError(
                f"Unable to parse {_DOCKERFILE} instruction beginning at line {start_line}"
            )
        instructions.append(
            DockerfileInstruction(
                keyword=match.group(1).casefold(),
                body=(match.group(2) or "").strip(),
                line_number=start_line,
            )
        )
        parts = []
        start_line = None

    if parts:
        raise RuntimeError(
            f"{_DOCKERFILE} ends with an unterminated continuation from line {start_line}"
        )
    return tuple(instructions)


def _environment_assignments(
    instruction: DockerfileInstruction,
) -> tuple[tuple[str, str], ...]:
    """Parse one Docker ``ENV`` instruction in modern or legacy form."""

    try:
        tokens = shlex.split(instruction.body, comments=False, posix=True)
    except ValueError as error:
        raise RuntimeError(
            f"Unable to parse {_DOCKERFILE} ENV instruction at line "
            f"{instruction.line_number}: {error}"
        ) from error
    if not tokens:
        raise RuntimeError(
            f"{_DOCKERFILE} ENV instruction at line {instruction.line_number} is empty"
        )

    if "=" not in tokens[0]:
        name = tokens[0]
        if len(tokens) < 2 or _ENVIRONMENT_NAME.fullmatch(name) is None:
            raise RuntimeError(
                f"Unable to parse {_DOCKERFILE} ENV instruction at line {instruction.line_number}"
            )
        return ((name, " ".join(tokens[1:])),)

    assignments: list[tuple[str, str]] = []
    for token in tokens:
        name, separator, value = token.partition("=")
        if separator != "=" or _ENVIRONMENT_NAME.fullmatch(name) is None:
            raise RuntimeError(
                f"Unable to parse {_DOCKERFILE} ENV instruction at line {instruction.line_number}"
            )
        assignments.append((name, value))
    return tuple(assignments)


def effective_dockerfile_environment(text: str) -> dict[str, str]:
    """Return Docker environment values after applying effective ``ENV`` instructions."""

    environment: dict[str, str] = {}
    for instruction in dockerfile_instructions(text):
        if instruction.keyword == "env":
            environment.update(_environment_assignments(instruction))
    return environment
