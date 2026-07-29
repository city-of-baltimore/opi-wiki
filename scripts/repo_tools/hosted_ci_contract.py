"""Define and compare the exact hosted-CI Taskfile and verification-plan shapes."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from scripts.repo_tools.taskfile_graph import TaskGraph
from scripts.repo_tools.workflow_policy import project_workflow_contract_lines

REQUIRED_CI_AGGREGATE_COMMAND = "uv run python scripts/verify.py --plan ci"
EXPECTED_TASKFILE_TOP_LEVEL = (
    ("version", "3"),
    ("tasks", ""),
)
EXPECTED_CI_TASK_SHAPES = (
    (
        "ci",
        ("desc", "cmds"),
        ("ci:policy",),
        (REQUIRED_CI_AGGREGATE_COMMAND,),
        ("task", "plain"),
    ),
    (
        "ci:policy",
        ("desc", "cmds"),
        (),
        ("uv run python scripts/check_hosted_ci_policy.py",),
        ("plain",),
    ),
)
EXPECTED_CI_WORKFLOW_PATHS = ("ci.yml",)
EXPECTED_CI_WORKFLOW_LINES = (
    "name: CI",
    "on:",
    "  pull_request:",
    "    branches: [main]",
    "  workflow_dispatch:",
    "permissions:",
    "  contents: read",
    "concurrency:",
    "  group: ci-${{ github.ref }}",
    "  cancel-in-progress: true",
    "jobs:",
    "  checks:",
    "    name: Static checks",
    "    runs-on: ubuntu-latest",
    "    timeout-minutes: 10",
    "    steps:",
    "      - uses: actions/checkout@<revision>",
    "        with:",
    "          persist-credentials: false",
    "      - uses: actions/setup-python@<revision>",
    "        with:",
    '          python-version: "3.14"',
    "      - uses: arduino/setup-task@<revision>",
    "        with:",
    "          version: 3.49.1",
    "      - name: Install uv",
    "        timeout-minutes: 5",
    "        run: pip install uv==0.11.28",
    "      - name: Install dependencies",
    "        timeout-minutes: 5",
    "        run: uv sync --frozen",
    "      - name: Run the lean gate",
    "        timeout-minutes: 5",
    "        run: task ci",
)
# Deliberately independent of ``scripts.verify.build_steps``: deriving this
# sequence from the plan would auto-approve the exact drift it exists to catch.
# Order and cardinality are contractual; callers normalize the interpreter
# token to ``python`` before comparison.
EXPECTED_CI_PLAN_COMMANDS = (
    "python scripts/check_hosted_ci_policy.py",
    "python scripts/check_browser_readiness_contract.py",
    "python scripts/check_platform_guard_evidence.py",
    "python -m baltimore.patapsco.baseline.cli --repo .",
    "python -m ruff format --check main.py scripts tests",
    "python -m ruff check main.py scripts tests",
    "python -m mypy",
    "python -m bandit -q -c pyproject.toml -r main.py scripts",
    "python scripts/check_page_metadata.py",
    "python scripts/check_organization_data.py",
    "python scripts/check_brand_terms.py",
    "python scripts/check_style.py",
    "python scripts/check_consistency.py",
    "python scripts/check_html_links.py",
)


def find_ci_workflow_inventory_violations(actual: Sequence[str]) -> list[str]:
    """Return missing, unexpected, duplicate, or reordered hosted workflows."""

    actual_paths = tuple(actual)
    if actual_paths == EXPECTED_CI_WORKFLOW_PATHS:
        return []

    expected_counts = Counter(EXPECTED_CI_WORKFLOW_PATHS)
    actual_counts = Counter(actual_paths)
    findings = [
        f"missing required hosted-CI workflow: {candidate}"
        for candidate, expected_count in expected_counts.items()
        if actual_counts[candidate] < expected_count
    ]
    findings.extend(
        (
            f"unexpected hosted-CI workflow: {candidate}"
            if expected_counts[candidate] == 0
            else f"duplicate hosted-CI workflow: {candidate}"
        )
        for candidate, actual_count in actual_counts.items()
        if actual_count > expected_counts[candidate]
    )
    if not findings:
        findings.append("hosted-CI workflows are not in the required order")
    return findings


def find_ci_workflow_shape_violations(source: str) -> list[str]:
    """Return exact-shape violations for the one hosted CI workflow."""

    actual_lines = project_workflow_contract_lines(source)
    if actual_lines == EXPECTED_CI_WORKFLOW_LINES:
        return []

    expected_counts = Counter(EXPECTED_CI_WORKFLOW_LINES)
    actual_counts = Counter(actual_lines)
    findings = [
        f"missing required hosted-CI workflow line: {candidate!r}"
        for candidate, expected_count in expected_counts.items()
        if actual_counts[candidate] < expected_count
    ]
    findings.extend(
        (
            f"unexpected hosted-CI workflow line: {candidate!r}"
            if expected_counts[candidate] == 0
            else f"duplicate hosted-CI workflow line: {candidate!r}"
        )
        for candidate, actual_count in actual_counts.items()
        if actual_count > expected_counts[candidate]
    )
    if not findings:
        findings.append("hosted-CI workflow lines are not in the required order")
    return findings


def find_ci_plan_shape_violations(actual: Sequence[str]) -> list[str]:
    """Return missing, unexpected, duplicate, or reordered ``ci`` commands."""

    actual_commands = tuple(actual)
    if actual_commands == EXPECTED_CI_PLAN_COMMANDS:
        return []

    expected_counts = Counter(EXPECTED_CI_PLAN_COMMANDS)
    actual_counts = Counter(actual_commands)
    findings = [
        f"missing required hosted-CI plan command: {candidate}"
        for candidate, expected_count in expected_counts.items()
        if actual_counts[candidate] < expected_count
    ]
    findings.extend(
        (
            f"unexpected hosted-CI plan command: {candidate}"
            if expected_counts[candidate] == 0
            else f"duplicate hosted-CI plan command: {candidate}"
        )
        for candidate, actual_count in actual_counts.items()
        if actual_count > expected_counts[candidate]
    )
    if not findings:
        findings.append("hosted-CI plan commands are not in the required order")
    return findings


def find_ci_task_shape_violations(graph: TaskGraph) -> list[str]:
    """Return exact-shape violations for the hosted ``ci`` task chain."""

    findings: list[str] = []
    actual_top_level = tuple(graph.top_level_entries)
    if actual_top_level != EXPECTED_TASKFILE_TOP_LEVEL:
        findings.append(
            "Taskfile top-level shape differs (key, normalized value): "
            f"expected {EXPECTED_TASKFILE_TOP_LEVEL!r}; found {actual_top_level!r}"
        )
    for (
        task,
        expected_properties,
        expected_subtasks,
        expected_commands,
        expected_forms,
    ) in EXPECTED_CI_TASK_SHAPES:
        declaration_count = graph.task_headers.count(task)
        if declaration_count != 1:
            findings.append(f"task:{task} must be declared exactly once; found {declaration_count}")
        actual_properties = tuple(graph.properties.get(task, ()))
        actual_subtasks = tuple(graph.subtasks.get(task, ()))
        actual_commands = tuple(graph.commands.get(task, ()))
        actual_forms = tuple(graph.command_forms.get(task, ()))
        actual_modifiers = tuple(graph.command_modifiers.get(task, ()))
        actual_shape = (
            actual_properties,
            actual_subtasks,
            actual_commands,
            actual_forms,
            actual_modifiers,
        )
        expected_shape = (
            expected_properties,
            expected_subtasks,
            expected_commands,
            expected_forms,
            (),
        )
        if actual_shape == expected_shape:
            continue
        findings.append(
            f"task:{task} shape differs "
            "(properties, subtasks, commands, command forms, command modifiers): "
            f"expected {expected_shape!r}; found {actual_shape!r}"
        )
    return findings
