#!/usr/bin/env python3
"""Keep hosted CI limited to static checks, contracts, and security.

Ownership: repository tooling, enforcing section 4 ("Lean CI") of
``patapsco/docs/app-consistency-standard.md`` for this repository.

Invariants enforced here:

1. Every ``run:`` step in a hosted workflow matches the exact allowlist in
   :data:`ALLOWED_RUN_COMMANDS`, and every ``uses:`` reference matches
   :data:`ALLOWED_ACTION_REFERENCES`.
2. No hosted workflow step reaches a forbidden command — a test suite, a
   coverage run, a site/application build, an image build, or a browser suite —
   **directly or transitively, at any depth**. Invariant 1 alone would let
   ``task ci`` or ``scripts/verify.py --plan prepush`` smuggle the whole heavy
   chain in behind one allowlisted-looking string, so this module walks two
   graphs and scans every command they expand to:

   * ``Taskfile.yml`` — ``task ci`` resolves through its ``task:``/``deps:``
     edges to the leaf shell commands it actually runs.
   * ``scripts/verify.py`` — a resolved plan expands to its subprocess list.

   The two compose: ``task ci`` → ``verify.py --plan ci`` → the step commands.
   A task that cannot be resolved is reported, never assumed innocent.
3. Every hosted job declares ``timeout-minutes``. Without one, a hung step burns
   GitHub's six-hour default instead of failing fast.

Publish/deploy/release workflows are exempt: building the site is their job.

Boundary: this module reads workflow YAML, ``Taskfile.yml``, and the
verification plan definition. Resolution is **static** — it never shells out to
``task --dry``, which writes its plan to stderr and so silently returns nothing
to a stdout-reading resolver, passing vacuously. It stays free of third-party
dependencies so it can run under a bare interpreter.

Two checkers, on purpose
------------------------
The ``ci`` plan runs **both** this module and Patapsco's ``platform-check``
(``baltimore-patapsco==0.4.0``). That is not duplication left by accident; the
consolidation to the shared checker was attempted and measured, and 0.4.0 does
not yet subsume this guard. Four violations this module fails on were injected
one at a time and ``platform-check`` returned ``conforms`` / exit 0 for each:

1. **A forbidden command inside a ``verify.py`` plan.** ``platform-check``
   resolves the ``Taskfile.yml`` graph but treats
   ``uv run python scripts/verify.py --plan ci`` as an opaque leaf string. This
   repository's hosted lane has *two* indirection layers, and the shared
   checker walks only the first — so adding ``pytest`` to the ``ci`` tier of
   :func:`scripts.verify.build_steps` passes it while the hosted lane really
   runs the test suite. This is the same shape as the ``task --dry`` bug: green
   while vacuous.
2. **A missing job ``timeout-minutes``** (invariant 3). No equivalent rule.
3. **An unallowlisted ``run:`` command** (invariant 1) — e.g. a piped
   ``curl … | sh``. ``platform-check`` matches a *forbidden* pattern list, which
   is a denylist; it has no allowlist, so an arbitrary new command passes.
4. **An unpinned ``uses:`` reference** (invariant 1) — e.g.
   ``actions/checkout@main`` instead of a SHA. No equivalent rule.

Gaps 3 and 4 are supply-chain surface, not lean-CI surface, so they may never
belong in the shared checker. Gap 1 is the one that matters for consolidation:
when ``platform-check`` learns to expand an aggregate runner's plans, re-run the
injection above and delete this module if it catches all four. Until then,
deleting this module would be a silent, measurable loss of enforcement.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.verify import PLANS, Plan, build_steps  # noqa: E402

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIRECTORY = REPOSITORY_ROOT / ".github" / "workflows"
TASKFILE_PATH = REPOSITORY_ROOT / "Taskfile.yml"

ALLOWED_RUN_COMMANDS = frozenset(
    {
        "pip install uv==0.11.28",
        "uv sync --frozen",
        "task ci",
    }
)
ALLOWED_ACTION_REFERENCES = frozenset(
    {
        "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
        "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1",
        "arduino/setup-task@c0bc642852239c2689f73f4ea6459c29405f3c52",
    }
)

# Publish/deploy/release workflows legitimately build artifacts; that is their
# job. Only the always-on quality lane is held to the lean-CI boundary.
EXEMPT_WORKFLOW_STEMS = frozenset({"deploy", "publish", "release"})

BLOCK_SCALAR_MARKERS = frozenset({"|", "|-", "|+", ">", ">-", ">+"})

# Section 4 of the consistency standard, expressed mechanically. Each entry is
# (human-readable reason, pattern) and is matched against every shell command a
# hosted workflow step can reach.
FORBIDDEN_COMMAND_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("unit/integration test suite", re.compile(r"\bpytest\b")),
    ("unit/integration test suite", re.compile(r"\bvitest\b")),
    ("unit/integration test suite", re.compile(r"\bnpm\s+(run\s+)?test\b")),
    ("unit/integration test suite", re.compile(r"\bpython3?\s+-m\s+unittest\b")),
    ("unit/integration test suite", re.compile(r"\btask\s+[\w:-]*test[\w:-]*\b")),
    ("coverage run", re.compile(r"\bcoverage\s+run\b")),
    ("coverage run", re.compile(r"--cov(-fail-under|-report)?\b")),
    ("application or site build", re.compile(r"\bmkdocs\b[^\n]*\bbuild\b")),
    ("application or site build", re.compile(r"\bnpm\s+run\s+build\b")),
    ("application or site build", re.compile(r"\bvite\s+build\b")),
    ("application or site build", re.compile(r"\btask\s+build\b")),
    ("image build", re.compile(r"\bdocker\s+build\b")),
    ("image build", re.compile(r"\bdocker\s+compose\b[^\n]*\bbuild\b")),
    ("image build", re.compile(r"\bdocker\s+compose\b[^\n]*--build\b")),
    ("browser/e2e/visual suite", re.compile(r"\bplaywright\b", re.IGNORECASE)),
    ("browser/e2e/visual suite", re.compile(r"\baxe\b")),
    ("browser/e2e/visual suite", re.compile(r"\bcheck_browser_smoke\b")),
)


#: A ``task <name>`` invocation. ``(?!-)`` skips flags such as ``task --list``.
TASK_INVOCATION = re.compile(r"\btask\s+(?!-)([A-Za-z][\w:.-]*)")
#: Taskfile structure: task headers sit at exactly this indent under ``tasks:``.
TASK_HEADER_INDENT = 2


def _normalize_command(command: str) -> str:
    normalized = " ".join(command.split(" #", maxsplit=1)[0].split())
    if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in {"'", '"'}:
        return normalized[1:-1]
    return normalized


def parse_taskfile(source: str) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Parse a Taskfile into ``(subtasks, commands)``, both keyed by task name.

    Deliberately hand-rolled rather than YAML-parsed so the guard runs under a
    bare interpreter. Only the two edges that can carry a forbidden command are
    modelled: ``task:``/``deps:`` references and ``cmds:`` shell strings.
    """

    subtasks: dict[str, list[str]] = {}
    commands: dict[str, list[str]] = {}
    inside_tasks = False
    current: str | None = None

    for raw_line in source.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indentation = len(line) - len(line.lstrip())
        stripped = line.strip()

        if indentation == 0:
            inside_tasks = stripped == "tasks:"
            current = None
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
            subtasks.setdefault(current, [])
            commands.setdefault(current, [])
            continue
        if current is None:
            continue

        if match := re.match(r"-?\s*task:\s*([A-Za-z][\w:.-]*)", stripped):
            subtasks[current].append(match.group(1))
            continue
        if match := re.match(r"deps:\s*\[(.+)\]", stripped):
            subtasks[current].extend(
                dependency.strip().strip("\"'") for dependency in match.group(1).split(",")
            )
            continue
        if match := re.match(r"-\s*cmd:\s*(.+)", stripped):
            commands[current].append(_normalize_command(match.group(1)))
            continue
        if stripped.startswith("- "):
            commands[current].append(_normalize_command(stripped[2:]))

    return subtasks, commands


def _load_task_graph() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Return this repository's parsed task graph, or empty graphs if absent."""

    try:
        source = TASKFILE_PATH.read_text(encoding="utf-8")
    except OSError:
        return {}, {}
    return parse_taskfile(source)


def resolve_task(
    name: str,
    subtasks: dict[str, list[str]],
    commands: dict[str, list[str]],
) -> tuple[list[tuple[str, str]], list[str]]:
    """Walk a task transitively.

    Returns ``(reached, unresolved)``, where *reached* pairs each leaf shell
    command with the ``task:a -> task:b`` chain that reaches it, and
    *unresolved* lists chains ending at a task this file does not define.
    """

    reached: list[tuple[str, str]] = []
    unresolved: list[str] = []
    seen: set[str] = set()

    def walk(task_name: str, chain: list[str]) -> None:
        if task_name in seen:
            return
        seen.add(task_name)
        path = [*chain, f"task:{task_name}"]
        if task_name not in commands:
            unresolved.append(" -> ".join(path))
            return
        for command in commands[task_name]:
            reached.append((" -> ".join(path), command))
        for child in subtasks.get(task_name, []):
            walk(child, path)

    walk(name, [])
    return reached, unresolved


def expand_task_invocations(command: str) -> list[tuple[str, str]]:
    """Expand every ``task <name>`` in a command into (provenance, command) pairs."""

    subtasks, commands = _load_task_graph()
    expanded: list[tuple[str, str]] = []
    for name in TASK_INVOCATION.findall(command):
        reached, _ = resolve_task(name, subtasks, commands)
        expanded.extend(
            (f"{chain} -> {reached_command}", reached_command) for chain, reached_command in reached
        )
    return expanded


def unresolved_task_invocations(command: str) -> list[str]:
    """Return chains for tasks a command invokes that the Taskfile does not define.

    An unresolvable task is a policy failure, not a pass: its commands cannot be
    inspected, so it cannot be shown to be lean.
    """

    subtasks, commands = _load_task_graph()
    chains: list[str] = []
    for name in TASK_INVOCATION.findall(command):
        _, unresolved = resolve_task(name, subtasks, commands)
        chains.extend(unresolved)
    return chains


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
        value = content.removeprefix("run:").strip()
        if value not in BLOCK_SCALAR_MARKERS:
            commands.append(_normalize_command(value))
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
        # Keep the line breaks: joining a block scalar into one line would let
        # two innocent adjacent commands read as one forbidden command.
        commands.append("\n".join(_normalize_command(entry) for entry in block_lines))

    return commands


def extract_action_references(source: str) -> list[str]:
    """Extract GitHub Action references from workflow steps and jobs."""

    references: list[str] = []
    for line in source.splitlines():
        stripped = line.lstrip()
        content = stripped[2:] if stripped.startswith("- ") else stripped
        if content.startswith("uses:"):
            references.append(_normalize_command(content.removeprefix("uses:").strip()))
    return references


def find_jobs_without_timeout(source: str) -> list[str]:
    """Return hosted job names that do not declare ``timeout-minutes``.

    A job without a timeout turns one hung step into a six-hour billed run, so
    the missing backstop is itself a policy violation.
    """

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


def _resolved_plan(command: str) -> Plan | None:
    """Return the verification plan a command runs, if it runs one at all."""

    if "scripts/verify.py" not in command and "verify.sh" not in command:
        return None
    match = re.search(r"--plan[= ]([\w-]+)", command)
    if match is None or match.group(1) not in PLANS:
        # An unrecognised or absent plan resolves to the heaviest tier: an
        # unpinned aggregate must never be assumed lean.
        return "validate"
    plan: Plan = match.group(1)  # type: ignore[assignment]
    return plan


def expand_aggregate_commands(command: str) -> list[tuple[str, str]]:
    """Expand an aggregate runner invocation into (provenance, command) pairs.

    ``scripts/verify.py`` is this repository's aggregate: one workflow string
    stands in for a whole plan of subprocesses. Scanning only the workflow text
    would miss a plan that quietly grows a ``pytest`` step, so the plan is
    resolved here and each expanded command is scanned on its own.
    """

    plan = _resolved_plan(command)
    if plan is None:
        return []

    expanded: list[tuple[str, str]] = []
    for step in build_steps(REPOSITORY_ROOT, python_executable="python", plan=plan):
        resolved = " ".join(step.command)
        expanded.append((f"verify.py --plan {plan} -> {resolved}", resolved))
    return expanded


def _direct_expansions(command: str) -> list[tuple[str, str]]:
    """Return the (provenance, command) pairs exactly one level below a command."""

    return [*expand_task_invocations(command), *expand_aggregate_commands(command)]


def reachable_commands(command: str) -> list[tuple[str, str]]:
    """Return every command reachable from ``command``, paired with how it is reached.

    Breadth-first across both indirection layers, so a chain that crosses them —
    ``task ci`` -> ``verify.py --plan ci`` -> a step command — is walked to the
    end rather than stopping at the first hop.
    """

    reachable: list[tuple[str, str]] = [(command, command)]
    seen: set[str] = {command}
    queue: list[tuple[str, str]] = [("", command)]

    while queue:
        parent_provenance, current = queue.pop(0)
        for label, expanded in _direct_expansions(current):
            if expanded in seen:
                continue
            seen.add(expanded)
            provenance = f"{parent_provenance} -> {label}" if parent_provenance else label
            reachable.append((provenance, expanded))
            queue.append((provenance, expanded))

    return reachable


def find_forbidden_reach(command: str) -> list[str]:
    """Return reasons ``command`` reaches a forbidden operation, at any depth."""

    findings: list[str] = []
    for provenance, candidate in reachable_commands(command):
        for chain in unresolved_task_invocations(candidate):
            findings.append(f"{chain} [unresolvable task: its commands cannot be inspected]")
        for reason, pattern in FORBIDDEN_COMMAND_PATTERNS:
            if pattern.search(candidate):
                findings.append(f"{provenance} [{reason}]")
                break
    return findings


def find_policy_violations(workflow_path: Path) -> list[str]:
    """Return every lean-CI violation in one hosted workflow."""

    source = workflow_path.read_text(encoding="utf-8")
    commands = extract_run_commands(source)

    violations = [f"run: {command}" for command in commands if command not in ALLOWED_RUN_COMMANDS]
    violations.extend(
        f"uses: {reference}"
        for reference in extract_action_references(source)
        if reference not in ALLOWED_ACTION_REFERENCES
    )
    for command in commands:
        violations.extend(find_forbidden_reach(command))
    violations.extend(
        f"job '{job}' declares no timeout-minutes" for job in find_jobs_without_timeout(source)
    )
    return violations


def find_all_policy_violations() -> tuple[list[str], list[Path]]:
    """Return violations across every non-exempt workflow, with the paths scanned."""

    workflow_paths = sorted(
        path
        for path in WORKFLOW_DIRECTORY.glob("*.y*ml")
        if path.stem.lower() not in EXEMPT_WORKFLOW_STEMS
    )

    violations: list[str] = []
    for workflow_path in workflow_paths:
        relative_path = workflow_path.relative_to(REPOSITORY_ROOT)
        violations.extend(
            f"{relative_path}: {violation}" for violation in find_policy_violations(workflow_path)
        )
    return violations, workflow_paths


def main() -> int:
    """Report hosted-CI policy violations and return a shell exit code."""

    violations, workflow_paths = find_all_policy_violations()

    if violations:
        print(
            "Hosted CI is static checks, contracts, and security only. It must "
            "never reach a test suite, a site build, an image build, or a browser "
            "suite — directly or through an aggregate runner — and every job must "
            "declare timeout-minutes. Run the heavy tiers locally with "
            "'./scripts/verify.sh --plan prepush' or '--plan validate'.",
            file=sys.stderr,
        )
        for violation in violations:
            print(f"- {violation}", file=sys.stderr)
        return 1

    print(
        f"Hosted CI policy holds across {len(workflow_paths)} workflow(s): "
        "static configuration checks only."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
