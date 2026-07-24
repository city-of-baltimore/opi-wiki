"""Static Taskfile graph parsing for repository policy checks."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

BLOCK_SCALAR_MARKER = re.compile(r"^[|>](?:[+-][1-9]?|[1-9][+-]?)?$")
#: A ``task <name>`` invocation. ``(?!-)`` skips flags such as ``task --list``.
TASK_INVOCATION = re.compile(r"\btask\s+(?!-)([A-Za-z][\w:.-]*)")
#: Taskfile structure: task headers sit at exactly this indent under ``tasks:``.
TASK_HEADER_INDENT = 2
#: Keys that end a ``deps:`` block list. Anything else at list depth inside one
#: is a dependency name, not a shell command.
TASK_BLOCK_KEYS = re.compile(r"(cmds|vars|env|desc|dir|sources|generates|status|preconditions):")


@dataclass(frozen=True)
class TaskGraph:
    """A parsed Taskfile: what each task runs, calls, and hides.

    ``silent`` is tracked because a ``silent: true`` task suppresses its own
    command echo. Its commands are still parsed here, but the flag is a signal
    that the task is deliberately opaque to any dry-run-based resolver, so it is
    reported rather than trusted.
    """

    subtasks: dict[str, list[str]] = field(default_factory=dict)
    commands: dict[str, list[str]] = field(default_factory=dict)
    silent: set[str] = field(default_factory=set)


def normalize_command(command: str) -> str:
    """Normalize YAML quoting, comments, and insignificant command whitespace."""

    normalized = " ".join(command.split(" #", maxsplit=1)[0].split())
    if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in {"'", '"'}:
        return normalized[1:-1]
    return normalized


def _consume_task_block_scalar(
    lines: list[str],
    start_index: int,
    marker_indentation: int,
    marker: str,
) -> tuple[str, int]:
    """Return a Taskfile command block and the next unconsumed line index."""

    command_lines: list[str] = []
    index = start_index
    while index < len(lines):
        block_line = lines[index]
        if block_line.strip():
            indentation = len(block_line) - len(block_line.lstrip())
            if indentation <= marker_indentation:
                break
            command_lines.append(normalize_command(block_line.strip()))
        index += 1
    separator = "\n" if marker.startswith("|") else " "
    return separator.join(command_lines), index


def parse_taskfile(source: str) -> TaskGraph:
    """Parse a Taskfile into the graph a policy resolver can walk.

    Deliberately hand-rolled rather than YAML-parsed so callers can run under a
    bare interpreter. Only what can carry or hide a command is modelled:
    ``task:``/``deps:`` edges, ``cmds:`` shell strings, block scalars, and the
    ``silent:`` flag.
    """

    graph = TaskGraph()
    inside_tasks = False
    current: str | None = None
    in_deps_block = False

    lines = source.splitlines()
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        index += 1
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indentation = len(line) - len(line.lstrip())
        stripped = line.strip()

        if indentation == 0:
            inside_tasks = stripped == "tasks:"
            current = None
            in_deps_block = False
            continue
        if not inside_tasks:
            continue

        is_header = (
            indentation == TASK_HEADER_INDENT
            and stripped.endswith(":")
            and " " not in stripped[:-1]
        )
        if is_header:
            current = stripped[:-1]
            graph.subtasks.setdefault(current, [])
            graph.commands.setdefault(current, [])
            in_deps_block = False
            continue
        if current is None:
            continue

        if re.match(r"silent:\s*true", stripped):
            graph.silent.add(current)
            continue

        if match := re.match(r"deps:\s*\[(.+)\]", stripped):
            graph.subtasks[current].extend(
                dependency.strip().strip("\"'") for dependency in match.group(1).split(",")
            )
            in_deps_block = False
            continue
        if re.match(r"deps:\s*$", stripped):
            in_deps_block = True
            continue
        if TASK_BLOCK_KEYS.match(stripped):
            in_deps_block = False

        if match := re.match(r"-?\s*task:\s*([A-Za-z][\w:.-]*)", stripped):
            graph.subtasks[current].append(match.group(1))
            continue
        if in_deps_block and (match := re.match(r"-\s*([A-Za-z][\w:.-]*)\s*$", stripped)):
            graph.subtasks[current].append(match.group(1))
            continue
        if match := re.match(r"-\s*cmd:\s*(.+)", stripped):
            command = normalize_command(match.group(1))
            if BLOCK_SCALAR_MARKER.fullmatch(command):
                command, index = _consume_task_block_scalar(
                    lines,
                    index,
                    indentation,
                    command,
                )
                graph.commands[current].append(command)
            else:
                graph.commands[current].append(normalize_command(command))
            continue
        if stripped.startswith("- "):
            command = normalize_command(stripped[2:])
            if BLOCK_SCALAR_MARKER.fullmatch(command):
                command, index = _consume_task_block_scalar(
                    lines,
                    index,
                    indentation,
                    command,
                )
                graph.commands[current].append(command)
            else:
                graph.commands[current].append(normalize_command(command))

    return graph


def resolve_task(name: str, graph: TaskGraph) -> tuple[list[tuple[str, str]], list[str]]:
    """Walk a task transitively and return reached commands and unresolved chains."""

    reached: list[tuple[str, str]] = []
    unresolved: list[str] = []
    seen: set[str] = set()

    def walk(task_name: str, chain: list[str]) -> None:
        if task_name in seen:
            return
        seen.add(task_name)
        path = [*chain, f"task:{task_name}"]
        if task_name not in graph.commands:
            unresolved.append(" -> ".join(path))
            return
        if task_name in graph.silent:
            unresolved.append(" -> ".join([*path, "silent: true (commands hidden)"]))
        for command in graph.commands[task_name]:
            reached.append((" -> ".join(path), command))
        for child in graph.subtasks.get(task_name, []):
            walk(child, path)

    walk(name, [])
    return reached, unresolved
