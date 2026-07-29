"""Static Taskfile graph parsing for repository policy checks."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

BLOCK_SCALAR_MARKER = re.compile(r"^[|>](?:[+-][1-9]?|[1-9][+-]?)?$")
#: A ``task <name>`` invocation. ``(?!-)`` skips flags such as ``task --list``.
TASK_INVOCATION = re.compile(r"\btask\s+(?!-)([A-Za-z][\w:.-]*)")
#: Taskfile structure: task headers sit at exactly this indent under ``tasks:``.
TASK_HEADER_INDENT = 2
#: Task properties sit one level below a task header.
TASK_PROPERTY_INDENT = 4
#: Entries in a task property's YAML list sit one level below the property.
TASK_LIST_ENTRY_INDENT = 6
TASK_PROPERTY = re.compile(r"([A-Za-z][\w-]*):")
#: These Taskfile lists execute shell, unlike declarative lists such as
#: ``sources`` and ``generates``. Restricting generic ``- ...`` parsing to these
#: blocks prevents declarative data from masquerading as a reached command.
EXECUTABLE_LIST_PROPERTIES = frozenset({"cmds", "preconditions", "status"})


@dataclass(frozen=True)
class TaskGraph:
    """A parsed Taskfile: what each task runs, calls, and hides.

    ``silent`` is tracked because a ``silent: true`` task suppresses its own
    command echo. Its commands are still parsed here, but the flag is a signal
    that the task is deliberately opaque to any dry-run-based resolver, so it is
    reported rather than trusted.
    """

    top_level_entries: list[tuple[str, str]] = field(default_factory=list)
    task_headers: list[str] = field(default_factory=list)
    properties: dict[str, list[str]] = field(default_factory=dict)
    subtasks: dict[str, list[str]] = field(default_factory=dict)
    commands: dict[str, list[str]] = field(default_factory=dict)
    command_forms: dict[str, list[str]] = field(default_factory=dict)
    command_modifiers: dict[str, list[str]] = field(default_factory=dict)
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
    top-level semantics, ``task:``/``deps:`` edges, executable
    ``cmds:``/``preconditions:``/``status:`` lists, block scalars, and the
    ``silent:`` flag. Declarative lists remain data.
    """

    graph = TaskGraph()
    inside_tasks = False
    current: str | None = None
    active_property: str | None = None

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
            top_level_match = re.fullmatch(
                r"(?P<key>[A-Za-z][\w-]*):(?:\s*(?P<value>.*))?",
                stripped,
            )
            if top_level_match is None:
                graph.top_level_entries.append(("<unsupported>", stripped))
                inside_tasks = False
            else:
                key = top_level_match.group("key")
                raw_value = top_level_match.group("value") or ""
                value = "" if raw_value.startswith("#") else normalize_command(raw_value)
                graph.top_level_entries.append((key, value))
                inside_tasks = key == "tasks" and value == ""
            current = None
            active_property = None
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
            graph.task_headers.append(current)
            graph.properties.setdefault(current, [])
            graph.subtasks.setdefault(current, [])
            graph.commands.setdefault(current, [])
            graph.command_forms.setdefault(current, [])
            graph.command_modifiers.setdefault(current, [])
            active_property = None
            continue
        if current is None:
            continue

        if indentation == TASK_PROPERTY_INDENT and (
            property_match := TASK_PROPERTY.match(stripped)
        ):
            active_property = property_match.group(1)
            graph.properties[current].append(active_property)

        if active_property == "cmds" and indentation > TASK_LIST_ENTRY_INDENT:
            graph.command_modifiers[current].append(stripped)
            continue

        if re.match(r"silent:\s*true", stripped):
            graph.silent.add(current)
            continue

        if match := re.match(r"deps:\s*\[(.+)\]", stripped):
            graph.subtasks[current].extend(
                dependency.strip().strip("\"'") for dependency in match.group(1).split(",")
            )
            continue

        if active_property in {"cmds", "deps"} and (
            match := re.match(r"-?\s*task:\s*([A-Za-z][\w:.-]*)", stripped)
        ):
            graph.subtasks[current].append(match.group(1))
            if active_property == "cmds":
                graph.command_forms[current].append("task")
            continue
        if active_property == "deps" and (
            match := re.match(r"-\s*([A-Za-z][\w:.-]*)\s*$", stripped)
        ):
            graph.subtasks[current].append(match.group(1))
            continue
        if active_property == "cmds" and (match := re.match(r"-\s*cmd:\s*(.+)", stripped)):
            graph.command_forms[current].append("object")
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
        if active_property == "preconditions" and (match := re.match(r"-\s*sh:\s*(.+)", stripped)):
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
        if active_property in EXECUTABLE_LIST_PROPERTIES and stripped.startswith("- "):
            if active_property == "cmds":
                graph.command_forms[current].append("plain")
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
