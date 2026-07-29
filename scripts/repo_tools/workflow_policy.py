"""Static GitHub Actions workflow parsing for repository policy checks."""

from __future__ import annotations

import re

from scripts.repo_tools.taskfile_graph import BLOCK_SCALAR_MARKER, normalize_command

_USES_CONTRACT_LINE = re.compile(
    r"^(?P<prefix>\s*(?:-\s+)?uses:\s*)(?P<identity>[^@\s]+)@(?P<revision>[^\s]+)$"
)


def project_workflow_contract_lines(source: str) -> tuple[str, ...]:
    """Return comment-free workflow lines with action revisions normalized.

    Indentation, key order, values, and step order remain exact. Only comments,
    blank lines, and immutable action revision values are presentation details:
    the separate SHA check validates each revision while this projection holds
    action identity and cardinality.
    """

    projected: list[str] = []
    for raw_line in source.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        line = raw_line.split(" #", maxsplit=1)[0].rstrip()
        uses_match = _USES_CONTRACT_LINE.fullmatch(line)
        if uses_match is not None:
            line = f"{uses_match.group('prefix')}{uses_match.group('identity')}@<revision>"
        projected.append(line)
    return tuple(projected)


def extract_run_commands(source: str) -> list[str]:
    """Extract inline and block-scalar GitHub Actions run commands."""

    lines = source.splitlines()
    commands: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip()
        content = stripped[2:] if stripped.startswith("- ") else stripped
        if not content.startswith("run:"):
            index += 1
            continue

        indentation = len(line) - len(stripped)
        value = normalize_command(content.removeprefix("run:").strip())
        if not BLOCK_SCALAR_MARKER.fullmatch(value):
            commands.append(normalize_command(value))
            index += 1
            continue

        block_lines: list[str] = []
        index += 1
        while index < len(lines):
            block_line = lines[index]
            if block_line.strip():
                block_indentation = len(block_line) - len(block_line.lstrip())
                if block_indentation <= indentation:
                    break
                block_lines.append(block_line.strip())
            index += 1
        # Keep line breaks: joining literal commands could create a forbidden
        # token sequence that the shell never runs as one command.
        commands.append("\n".join(normalize_command(entry) for entry in block_lines))

    return commands


def extract_action_references(source: str) -> list[str]:
    """Extract GitHub Action references from workflow steps and jobs."""

    references: list[str] = []
    for line in source.splitlines():
        stripped = line.lstrip()
        content = stripped[2:] if stripped.startswith("- ") else stripped
        if content.startswith("uses:"):
            references.append(normalize_command(content.removeprefix("uses:").strip()))
    return references


def find_jobs_without_timeout(source: str) -> list[str]:
    """Return hosted job names that do not declare ``timeout-minutes``."""

    lines = source.splitlines()
    jobs_index = next(
        (index for index, line in enumerate(lines) if line.rstrip() == "jobs:"),
        None,
    )
    if jobs_index is None:
        return []

    missing: list[str] = []
    current_job: str | None = None
    has_timeout = False

    def _flush() -> None:
        if current_job is not None and not has_timeout:
            missing.append(current_job)

    for line in lines[jobs_index + 1 :]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indentation = len(line) - len(line.lstrip())
        if indentation == 0:
            break

        if indentation == 2 and stripped.endswith(":"):
            _flush()
            current_job = stripped[:-1].strip().strip("\"'")
            has_timeout = False
            continue

        if indentation == 4 and stripped.startswith("timeout-minutes:"):
            has_timeout = True

    _flush()
    return missing
