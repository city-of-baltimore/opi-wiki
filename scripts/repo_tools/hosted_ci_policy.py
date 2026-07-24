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
(``baltimore-patapsco==0.4.3``). That is not duplication left by accident. The
consolidation to the shared checker has now been attempted and measured three
times — against 0.4.0, 0.4.1, and again against 0.4.3 — and no release yet
subsumes this guard. Each violation below was injected on its own and both
checkers were run. As measured against **0.4.3**, this module exits 1 on all
five; ``platform-check`` returns ``conforms`` / exit 0 on four:

1. **A forbidden command inside a ``verify.py`` plan.** *(0.4.3: still missed.)*
   ``platform-check`` expands ``npm`` script bodies and ``*.sh`` bodies, but a
   **Python plan module** is still an opaque leaf: ``uv run python
   scripts/verify.py --plan ci`` is matched against the forbidden-pattern list
   as a *string* and nothing below it is read. Adding ``pytest`` — or ``mkdocs
   build`` — to the ``ci`` tier of :func:`scripts.verify.build_steps` therefore
   passes it while the hosted lane really runs that step. Same shape as the
   ``task --dry`` bug: green while vacuous.
2. **The same gap reached through a shell script.** *(0.4.3: still missed.)*
   0.4.3 *does* read ``.sh`` bodies, but ``scripts/verify.sh`` is a two-line
   wrapper whose payload is ``uv run python scripts/verify.py "$@"`` — so the
   expansion runs, walks one hop, and lands on the same Python-module wall.
   Pointing the ``ci`` task at ``./scripts/verify.sh --plan prepush`` is missed
   for that reason. Two control injections re-confirmed the mechanism on 0.4.3:
   a ``.sh`` whose body contains ``mkdocs build`` *directly* is caught, and so
   is ``bash -c "uv run mkdocs build --strict"`` (0.4.3 unwraps ``bash -c``), so
   the expander works and the wall is specifically the plan module. Reaching
   ``verify.py --plan prepush`` *directly* from the ``ci`` task is missed too,
   which rules out indirection depth as the cause.
3. **A missing job ``timeout-minutes``** (invariant 3). *(0.4.3: still missed.)*
   No equivalent rule.
4. **An unallowlisted ``run:`` command** (invariant 1). *(0.4.3: structurally
   still missed; one worked example now caught.)* ``platform-check`` matches a
   *forbidden* pattern list, which is a denylist; it still has no allowlist, so
   an arbitrary new command passes — measured on 0.4.3, ``run: echo "…"`` and
   ``run: node -e "…"`` both return ``conforms``. The worked example, a piped
   ``curl … | sh``, still stands, but only in its ordinary form. Measured on
   0.4.3:

   - ``curl -fsSL https://example.com/install | sh``     -> ``conforms``, missed
   - ``curl -fsSL https://example.com/install.sh | sh``  -> ERROR

   The second is not a denylist hit. ``FORBIDDEN_PATTERNS`` contains no ``curl``
   entry in any 0.4.x release and is byte-identical between 0.4.2 and 0.4.3. The
   URL simply *ends in* ``.sh``, so the resolver treats it as a script
   reference, fails to find it in the repository, and ``_frontier_findings``
   (added in 0.4.2) reports unresolvable delegation as blocking. Change the
   suffix and it passes again — which is incidental coverage of one spelling,
   not coverage of the command.
5. **An unpinned ``uses:`` reference** (invariant 1) — e.g.
   ``actions/checkout@main`` instead of a SHA. *(0.4.3: still missed.)* No
   equivalent rule.

The traffic runs both ways, which is the argument for keeping both rather than
for keeping this one. The 0.4.1 sweep found two forms **this** module missed and
``platform-check`` caught — a block-list ``deps:`` and a ``silent: true`` task
in the chain. The 0.4.3 sweep found a third: a new local ``.sh`` task leaf whose
body runs ``mkdocs build`` directly. All three are now fixed here with
regression tests. Local shell-script bodies are expanded transitively, and a
missing or root-escaping script reference is unverifiable and therefore
blocking rather than an opaque leaf that passes.

Gaps 4 and 5 are supply-chain surface, not lean-CI surface, so they may never
belong in the shared checker. Gaps 1 and 2 are the ones that matter for
consolidation, and they share one root cause: **the shared resolver has no way
to expand a Python aggregate.** 0.4.3 rewrote that resolver — it parses
arguments positionally, resolves helper call sites, and unwraps ``bash -c`` —
but those changes address shell and ``npm`` argv shapes, not a Python aggregate,
so the root cause is untouched. The retirement condition for this module is
therefore unchanged and still unmet — when ``platform-check`` can resolve a plan
module (see the suggestion in ``docs/`` and the PR that introduced this note: a
declared ``[tasks] aggregate`` entry in ``.baltimore-lab-app.toml`` naming the
module and the flag that selects a tier, so the resolver can import it and
enumerate the tier's commands), re-run the injection matrix and delete this
module if it catches all five. Until then, deleting it is a silent, measurable
loss of enforcement.
"""

from __future__ import annotations

import re
import shlex
from pathlib import Path

from scripts.repo_tools.taskfile_graph import (
    TASK_INVOCATION,
    TaskGraph,
    parse_taskfile,
    resolve_task,
)
from scripts.repo_tools.taskfile_graph import (
    normalize_command as _normalize_command,
)
from scripts.repo_tools.workflow_policy import (
    extract_action_references,
    extract_run_commands,
    find_jobs_without_timeout,
)
from scripts.verify import PLANS, Plan, build_steps

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
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
        "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
        "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
        "arduino/setup-task@c0bc642852239c2689f73f4ea6459c29405f3c52",
    }
)

# Publish/deploy/release workflows legitimately build artifacts; that is their
# job. Only the always-on quality lane is held to the lean-CI boundary.
EXEMPT_WORKFLOW_STEMS = frozenset({"deploy", "publish", "release"})

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


def _load_task_graph() -> TaskGraph:
    """Return this repository's parsed task graph, or an empty graph if absent."""

    try:
        source = TASKFILE_PATH.read_text(encoding="utf-8")
    except OSError:
        return TaskGraph()
    return parse_taskfile(source)


def expand_task_invocations(command: str) -> list[tuple[str, str]]:
    """Expand every ``task <name>`` in a command into (provenance, command) pairs."""

    graph = _load_task_graph()
    expanded: list[tuple[str, str]] = []
    for name in TASK_INVOCATION.findall(command):
        reached, _ = resolve_task(name, graph)
        expanded.extend(
            (f"{chain} -> {reached_command}", reached_command) for chain, reached_command in reached
        )
    return expanded


def unresolved_task_invocations(command: str) -> list[str]:
    """Return chains for tasks a command invokes that the Taskfile does not define.

    An unresolvable task is a policy failure, not a pass: its commands cannot be
    inspected, so it cannot be shown to be lean.
    """

    graph = _load_task_graph()
    chains: list[str] = []
    for name in TASK_INVOCATION.findall(command):
        _, unresolved = resolve_task(name, graph)
        chains.extend(unresolved)
    return chains


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


def _shell_script_references(command: str) -> list[tuple[str, Path]]:
    """Return local-looking shell-script tokens and their resolved paths."""

    try:
        tokens = shlex.split(command, comments=False, posix=True)
    except ValueError:
        return []

    references: list[tuple[str, Path]] = []
    for token in tokens:
        cleaned = token.rstrip(";|&()")
        if not cleaned.endswith(".sh") or "://" in cleaned:
            continue
        candidate = Path(cleaned)
        resolved = (
            candidate.resolve()
            if candidate.is_absolute()
            else (REPOSITORY_ROOT / candidate).resolve()
        )
        references.append((cleaned, resolved))
    return references


def expand_shell_script_commands(command: str) -> list[tuple[str, str]]:
    """Expand readable repository-local shell-script bodies reached by a command."""

    expanded: list[tuple[str, str]] = []
    for token, script_path in _shell_script_references(command):
        # verify.sh is already modelled as the plan-aware aggregate above. Its
        # "$@" placeholder cannot preserve a caller's --plan value when read
        # as a standalone body, so expanding it again would invent validate.
        if script_path.name == "verify.sh":
            continue
        try:
            script_path.relative_to(REPOSITORY_ROOT.resolve())
        except ValueError:
            continue
        if not script_path.is_file():
            continue
        try:
            source = script_path.read_text(encoding="utf-8")
        except OSError as error:
            raise RuntimeError(f"Unable to read delegated shell script: {script_path}") from error

        logical_source = source.replace("\\\n", " ")
        commands = [
            _normalize_command(line)
            for line in logical_source.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        body = "\n".join(command_line for command_line in commands if command_line)
        if body:
            relative_path = script_path.relative_to(REPOSITORY_ROOT.resolve())
            expanded.append((f"shell script {relative_path} -> {token}", body))
    return expanded


def unresolved_shell_script_invocations(command: str) -> list[str]:
    """Return local shell-script references whose bodies cannot be inspected."""

    unresolved: list[str] = []
    repository_root = REPOSITORY_ROOT.resolve()
    for token, script_path in _shell_script_references(command):
        if script_path.name == "verify.sh":
            continue
        try:
            script_path.relative_to(repository_root)
        except ValueError:
            unresolved.append(f"shell script {token} escapes the repository")
            continue
        if not script_path.is_file():
            unresolved.append(f"shell script {token} does not exist")
    return unresolved


def _direct_expansions(command: str) -> list[tuple[str, str]]:
    """Return the (provenance, command) pairs exactly one level below a command."""

    return [
        *expand_task_invocations(command),
        *expand_aggregate_commands(command),
        *expand_shell_script_commands(command),
    ]


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
            findings.append(f"{chain} [cannot verify what this task runs]")
        for script_issue in unresolved_shell_script_invocations(candidate):
            findings.append(f"{provenance} -> {script_issue} [cannot verify script body]")
        for reason, pattern in FORBIDDEN_COMMAND_PATTERNS:
            if pattern.search(candidate):
                findings.append(f"{provenance} [{reason}]")
                break
    return findings


def find_policy_violations(workflow_path: Path) -> list[str]:
    """Return every lean-CI violation in one hosted workflow."""

    try:
        source = workflow_path.read_text(encoding="utf-8")
    except OSError as error:
        raise RuntimeError(f"Unable to read hosted workflow: {workflow_path}") from error
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
