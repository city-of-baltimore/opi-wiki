"""Tests for hosted-CI Taskfile graph resolution."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.check_hosted_ci_policy as hosted_ci_cli
from scripts.repo_tools.hosted_ci_policy import (
    expand_task_invocations,
    find_forbidden_reach,
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

    graph = parse_taskfile(TASKFILE)

    assert graph.subtasks["ci"] == ["policy"]
    assert graph.commands["ci"] == ["uv run python scripts/verify.py --plan ci"]
    assert graph.commands["test"] == ["uv run python -m pytest"]


def test_parse_taskfile_reads_multiline_command_blocks() -> None:
    """Literal and cmd-object block scalars must expose their command bodies."""

    source = """version: "3"

tasks:
  direct:
    cmds:
      - |
        uv run python -m pytest
        echo finished

  object:
    cmds:
      - cmd: >-
        uv run mkdocs build
        --strict
"""

    graph = parse_taskfile(source)

    assert graph.commands["direct"] == ["uv run python -m pytest\necho finished"]
    assert graph.commands["object"] == ["uv run mkdocs build --strict"]


def test_taskfile_block_scalar_cannot_hide_a_forbidden_command() -> None:
    """Regression: a `- |` command body must be scanned instead of the marker."""

    source = """version: "3"

tasks:
  ci:
    cmds:
      - |
        uv run python -m pytest
"""
    graph = parse_taskfile(source)
    reached, unresolved = resolve_task("ci", graph)

    assert unresolved == []
    assert reached == [("task:ci", "uv run python -m pytest")]
    assert find_forbidden_reach(reached[0][1])


def test_taskfile_block_scalar_marker_may_have_a_yaml_comment() -> None:
    """A comment after `|-` must not turn the marker into an opaque command."""

    source = """version: "3"

tasks:
  ci:
    cmds:
      - |- # explain why this command is grouped
        uv run python -m pytest
"""
    graph = parse_taskfile(source)
    reached, unresolved = resolve_task("ci", graph)

    assert unresolved == []
    assert reached == [("task:ci", "uv run python -m pytest")]
    assert find_forbidden_reach(reached[0][1])


def test_taskfile_block_scalar_marker_may_have_an_indentation_indicator() -> None:
    """Valid `|2-` syntax must expose its body to the task resolver."""

    source = """version: "3"

tasks:
  ci:
    cmds:
      - |2-
        uv run python -m pytest
"""
    graph = parse_taskfile(source)
    reached, unresolved = resolve_task("ci", graph)

    assert unresolved == []
    assert reached == [("task:ci", "uv run python -m pytest")]
    assert find_forbidden_reach(reached[0][1])


def test_folded_taskfile_block_cannot_split_a_forbidden_command() -> None:
    """Folded YAML lines are one shell command and must be scanned that way."""

    source = """version: "3"

tasks:
  ci:
    cmds:
      - >-
        uv run mkdocs
        build --strict
"""
    graph = parse_taskfile(source)
    reached, unresolved = resolve_task("ci", graph)

    assert unresolved == []
    assert reached == [("task:ci", "uv run mkdocs build --strict")]
    assert find_forbidden_reach(reached[0][1])


def test_parse_taskfile_ignores_descriptions_and_non_task_blocks() -> None:
    """`desc:` text and top-level keys are not commands and must not be scanned."""

    graph = parse_taskfile(TASKFILE)

    assert all("Guard" not in command for command in graph.commands["policy"])
    assert "version" not in graph.commands


def test_parse_taskfile_reads_inline_deps() -> None:
    """The inline `deps: [a, b]` form is a graph edge."""

    source = TASKFILE.replace("  ci:\n    desc:", "  ci:\n    deps: [policy]\n    desc:")

    graph = parse_taskfile(source)

    assert "policy" in graph.subtasks["ci"]


def test_parse_taskfile_reads_block_list_deps() -> None:
    """A block-form `deps:` is an edge, not a command named after the task.

    Regression: only the inline `deps: [a, b]` form was parsed, so a block list
    fell through to the generic `- ` branch and was recorded as a *command*
    named `test` — which no forbidden pattern matches. A block `deps:` could
    therefore pull the whole test suite into the hosted lane unseen.
    """

    source = TASKFILE.replace(
        "  ci:\n    desc: Lean gate",
        "  ci:\n    deps:\n      - test\n    desc: Lean gate",
    )

    graph = parse_taskfile(source)

    assert "test" in graph.subtasks["ci"]
    assert "test" not in graph.commands["ci"]


def test_a_block_list_deps_edge_into_the_test_suite_is_a_violation() -> None:
    """End to end: a block `deps:` reaching pytest fails the guard."""

    source = TASKFILE.replace(
        "  ci:\n    desc: Lean gate",
        "  ci:\n    deps:\n      - test\n    desc: Lean gate",
    )
    graph = parse_taskfile(source)

    reached, _ = resolve_task("ci", graph)

    assert ("task:ci -> task:test", "uv run python -m pytest") in reached


def test_parse_taskfile_records_a_silent_task() -> None:
    """`silent: true` is tracked so the resolver can refuse to vouch for it."""

    source = TASKFILE.replace(
        "  policy:\n    desc: Guard",
        "  policy:\n    silent: true\n    desc: Guard",
    )

    graph = parse_taskfile(source)

    assert "policy" in graph.silent
    assert all("silent" not in command for command in graph.commands["policy"])


def test_resolve_task_refuses_a_silent_task_in_the_chain() -> None:
    """A task that hides its commands is reported, not trusted."""

    source = TASKFILE.replace(
        "  policy:\n    desc: Guard",
        "  policy:\n    silent: true\n    desc: Guard",
    )
    graph = parse_taskfile(source)

    _, unresolved = resolve_task("ci", graph)

    assert unresolved == ["task:ci -> task:policy -> silent: true (commands hidden)"]


def test_resolve_task_walks_transitively_with_a_chain() -> None:
    """A command two hops down is reported with the path that reaches it."""

    graph = parse_taskfile(TASKFILE)

    reached, unresolved = resolve_task("sneaky", graph)

    assert unresolved == []
    assert (
        "task:sneaky -> task:ci -> task:policy",
        "uv run python scripts/check_hosted_ci_policy.py",
    ) in reached
    assert ("task:sneaky -> task:test", "uv run python -m pytest") in reached


def test_resolve_task_reports_an_undefined_task_rather_than_passing_it() -> None:
    """A task that cannot be inspected is never assumed innocent."""

    graph = parse_taskfile(TASKFILE)

    _, unresolved = resolve_task("nope", graph)

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
    assert any("check_organization_data.py" in command for command in reached)


def test_a_heavy_task_is_caught_through_the_task_graph() -> None:
    """`task prepush` runs a test suite and a build; the hosted lane must refuse it."""

    reasons = " ".join(find_forbidden_reach("task prepush"))

    assert "unit/integration test suite" in reasons
    assert "application or site build" in reasons


def test_an_undefined_task_invocation_is_a_violation() -> None:
    """A workflow cannot point at a task this repository does not define."""

    reasons = " ".join(find_forbidden_reach("task ci:does-not-exist"))

    assert "cannot verify what this task runs" in reasons
    assert "ci:does-not-exist" in reasons


def test_find_policy_violations_reports_an_unallowlisted_command(tmp_path: Path) -> None:
    """Anything outside the exact allowlist is surfaced, not silently tolerated."""

    workflow = tmp_path / "ci.yml"
    workflow.write_text(_workflow("      - run: curl https://example.test | sh\n"), "utf-8")

    violations = find_policy_violations(workflow)

    assert any("curl https://example.test | sh" in violation for violation in violations)


def test_find_policy_violations_accepts_the_allowed_hosted_command(tmp_path: Path) -> None:
    """The committed hosted command shape should pass the complete workflow scan."""

    workflow = tmp_path / "ci.yml"
    workflow.write_text(_workflow("      - run: task ci\n"), encoding="utf-8")

    assert find_policy_violations(workflow) == []


def test_find_policy_violations_scans_a_taskfile_block_body(tmp_path: Path) -> None:
    """A workflow block containing a forbidden command should report both policy seams."""

    workflow = tmp_path / "ci.yml"
    workflow.write_text(
        _workflow("      - run: |2-\n          uv run python -m pytest\n"),
        encoding="utf-8",
    )

    reasons = " ".join(find_policy_violations(workflow))

    assert "run: uv run python -m pytest" in reasons
    assert "unit/integration test suite" in reasons


def test_find_policy_violations_reports_an_unreadable_workflow(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Workflow IO errors should retain the affected path."""

    workflow = tmp_path / "ci.yml"
    workflow.write_text(_workflow("      - run: task ci\n"), encoding="utf-8")

    def fail_read(path: Path, *, encoding: str) -> str:
        assert path == workflow
        assert encoding == "utf-8"
        raise OSError("read failed")

    monkeypatch.setattr(Path, "read_text", fail_read)

    with pytest.raises(RuntimeError, match=r"Unable to read hosted workflow: .*ci\.yml"):
        find_policy_violations(workflow)


def test_main_reports_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The hosted-policy CLI should report how many workflows passed."""

    monkeypatch.setattr(
        hosted_ci_cli,
        "find_all_policy_violations",
        lambda: ([], [Path("ci.yml")]),
    )

    assert hosted_ci_cli.main() == 0
    assert "holds across 1 workflow(s)" in capsys.readouterr().out


def test_main_reports_policy_findings(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A policy violation should produce a nonzero result and evidence."""

    monkeypatch.setattr(
        hosted_ci_cli,
        "find_all_policy_violations",
        lambda: (["ci.yml: run: pytest"], [Path("ci.yml")]),
    )

    assert hosted_ci_cli.main() == 1
    assert "ci.yml: run: pytest" in capsys.readouterr().err


def test_main_reports_an_unexpected_scan_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An unreadable workflow should fail concisely rather than traceback."""

    def fail_scan() -> tuple[list[str], list[Path]]:
        raise RuntimeError("Unable to read hosted workflow")

    monkeypatch.setattr(hosted_ci_cli, "find_all_policy_violations", fail_scan)

    assert hosted_ci_cli.main() == 1
    assert capsys.readouterr().err == (
        "Hosted CI policy check failed unexpectedly: Unable to read hosted workflow\n"
    )
