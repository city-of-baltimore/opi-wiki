"""Adversarial tests for the exact hosted-CI task and plan contract."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
import scripts.repo_tools.hosted_ci_policy as hosted_ci_policy
from scripts.repo_tools.hosted_ci_contract import (
    EXPECTED_CI_PLAN_COMMANDS,
    find_ci_task_shape_violations,
)
from scripts.repo_tools.hosted_ci_policy import (
    expand_aggregate_commands,
    find_ci_plan_contract_violations,
    find_forbidden_reach,
    find_policy_violations,
)
from scripts.repo_tools.taskfile_graph import parse_taskfile
from scripts.verify import Plan, VerifyStep


def _patch_ci_steps(
    monkeypatch: pytest.MonkeyPatch,
    mutation: Callable[[list[VerifyStep]], list[VerifyStep]],
) -> None:
    """Replace only the resolved ``ci`` step sequence for one mutation test."""

    original_build_steps = hosted_ci_policy.build_steps

    def mutated_build_steps(
        repo_root: Path,
        python_executable: str | None = None,
        *,
        plan: Plan = "prepush",
    ) -> list[VerifyStep]:
        steps = original_build_steps(
            repo_root,
            python_executable=python_executable,
            plan=plan,
        )
        return mutation(steps) if plan == "ci" else steps

    monkeypatch.setattr(hosted_ci_policy, "build_steps", mutated_build_steps)


def _patch_taskfile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: Callable[[str], str],
) -> None:
    """Write one mutated copy of the real Taskfile and route policy reads to it."""

    source = hosted_ci_policy.TASKFILE_PATH.read_text(encoding="utf-8")
    taskfile = tmp_path / "Taskfile.yml"
    taskfile.write_text(mutation(source), encoding="utf-8")
    monkeypatch.setattr(hosted_ci_policy, "TASKFILE_PATH", taskfile)


def test_current_taskfile_top_level_allows_comments_but_no_new_semantics() -> None:
    """Comments may move freely without weakening the exact execution contract."""

    source = hosted_ci_policy.TASKFILE_PATH.read_text(encoding="utf-8")
    source = source.replace('version: "3"\n', 'version: "3" # Task schema\n', 1)
    source = source.replace("tasks:\n", "tasks: # Exact command surface\n", 1)
    source = "# Maintainer context is safe.\n" + source

    assert find_ci_task_shape_violations(parse_taskfile(source)) == []


@pytest.mark.parametrize(
    "global_semantics",
    (
        'env:\n  PYTHONPATH: "scripts/shadow"\n',
        "dotenv:\n  - .env.ci\n",
        'vars:\n  PYTHON: "scripts/shadow-python"\n',
        "includes:\n  hidden: ./tasks/hidden.yml\n",
    ),
)
def test_global_taskfile_execution_semantics_fail_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    global_semantics: str,
) -> None:
    """Global environment, imports, and variables cannot alter the reviewed CI task."""

    _patch_taskfile(
        tmp_path,
        monkeypatch,
        lambda source: source.replace("tasks:\n", global_semantics + "\ntasks:\n", 1),
    )

    findings = find_forbidden_reach("task ci")

    assert len(findings) == 1
    assert "Taskfile top-level shape differs" in findings[0]
    assert global_semantics.partition(":")[0] in findings[0]


def test_a_duplicate_ci_task_header_cannot_override_the_reviewed_task() -> None:
    """A later empty YAML key must not erase the checked task at load time."""

    source = hosted_ci_policy.TASKFILE_PATH.read_text(encoding="utf-8")
    source += "\n  ci:\n"

    findings = find_ci_task_shape_violations(parse_taskfile(source))

    assert findings == ["task:ci must be declared exactly once; found 2"]


def test_the_ci_plan_matches_the_exact_ordered_contract() -> None:
    """The current plan is fully enumerated rather than assumed safe by absence."""

    command = "uv run python scripts/verify.py --plan ci"
    expanded = expand_aggregate_commands(command)

    assert all(candidate.startswith("python ") for _, candidate in expanded)
    assert tuple(candidate for _provenance, candidate in expanded) == EXPECTED_CI_PLAN_COMMANDS
    assert find_ci_plan_contract_violations(command) == []


def test_a_new_ci_plan_command_requires_explicit_policy_approval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unknown Python checker must fail even when no denylist pattern names it."""

    _patch_ci_steps(
        monkeypatch,
        lambda steps: [
            *steps,
            VerifyStep(
                name="Checking a new built-site contract",
                command=("python", "scripts/check_new_built_site_contract.py"),
            ),
        ],
    )

    findings = find_forbidden_reach("uv run python scripts/verify.py --plan ci")

    assert len(findings) == 1
    assert "unexpected hosted-CI plan command" in findings[0]
    assert "scripts/check_new_built_site_contract.py" in findings[0]


def test_removing_a_required_ci_plan_command_fails_the_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Subtraction must fail rather than quietly shrinking hosted assurance."""

    _patch_ci_steps(
        monkeypatch,
        lambda steps: [step for step in steps if "scripts/check_style.py" not in step.command],
    )

    findings = find_forbidden_reach("uv run python scripts/verify.py --plan ci")

    assert len(findings) == 1
    assert "missing required hosted-CI plan command" in findings[0]
    assert "scripts/check_style.py" in findings[0]


def test_duplicating_an_approved_ci_plan_command_fails_the_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Allowlisted commands retain exact cardinality rather than set semantics."""

    _patch_ci_steps(monkeypatch, lambda steps: [*steps, steps[-1]])

    findings = find_forbidden_reach("uv run python scripts/verify.py --plan ci")

    assert len(findings) == 1
    assert "duplicate hosted-CI plan command" in findings[0]
    assert "scripts/check_html_links.py" in findings[0]


def test_reordering_approved_ci_plan_commands_fails_the_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The plan order is part of the contract, not an unordered allowlist."""

    _patch_ci_steps(monkeypatch, lambda steps: [steps[1], steps[0], *steps[2:]])

    assert find_forbidden_reach("uv run python scripts/verify.py --plan ci") == [
        "uv run python scripts/verify.py --plan ci "
        "[hosted-CI plan commands are not in the required order]"
    ]


def test_ci_task_cannot_drop_the_required_plan_aggregate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A policy-only ``ci`` task must not make an empty hosted lane look green."""

    aggregate = "      - uv run python scripts/verify.py --plan ci\n"

    def hide_removed_aggregate_in_sources(source: str) -> str:
        without_aggregate = source.replace(aggregate, "", 1)
        return without_aggregate.replace(
            "  ci:\n",
            "  ci:\n    sources:\n      - uv run python scripts/verify.py --plan ci\n",
            1,
        )

    _patch_taskfile(tmp_path, monkeypatch, hide_removed_aggregate_in_sources)
    workflow = tmp_path / "ci.yml"
    workflow.write_text(
        "jobs:\n"
        "  checks:\n"
        "    runs-on: ubuntu-latest\n"
        "    timeout-minutes: 10\n"
        "    steps:\n"
        "      - run: task ci\n",
        encoding="utf-8",
    )

    findings = find_policy_violations(workflow, enforce_exact_contract=False)

    assert len(findings) == 1
    assert "task:ci shape differs" in findings[0]
    assert "'sources'" in findings[0]
    assert "found" in findings[0]


def test_ci_task_cannot_add_an_unreviewed_benign_command(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A command need not match a denylist to violate the exact hosted task."""

    aggregate = "      - uv run python scripts/verify.py --plan ci\n"
    _patch_taskfile(
        tmp_path,
        monkeypatch,
        lambda source: source.replace(aggregate, aggregate + "      - echo extra work\n", 1),
    )

    findings = find_forbidden_reach("task ci")

    assert len(findings) == 1
    assert "task:ci shape differs" in findings[0]
    assert "echo extra work" in findings[0]


def test_ci_task_cannot_duplicate_the_required_aggregate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The required aggregate has exact cardinality, even after reach deduplication."""

    aggregate = "      - uv run python scripts/verify.py --plan ci\n"
    _patch_taskfile(
        tmp_path,
        monkeypatch,
        lambda source: source.replace(aggregate, aggregate * 2, 1),
    )

    findings = find_forbidden_reach("task ci")

    assert len(findings) == 1
    assert "task:ci shape differs" in findings[0]
    assert findings[0].count("scripts/verify.py --plan ci") == 3


def test_ci_policy_task_cannot_grow_hidden_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The guard subtask itself owns one command and no subordinate task graph."""

    checker = "      - uv run python scripts/check_hosted_ci_policy.py\n"
    _patch_taskfile(
        tmp_path,
        monkeypatch,
        lambda source: source.replace(checker, checker + "      - echo hidden work\n", 1),
    )

    findings = find_forbidden_reach("task ci")

    assert len(findings) == 1
    assert "task:ci:policy shape differs" in findings[0]
    assert "echo hidden work" in findings[0]


def test_ci_aggregate_cannot_ignore_its_exit_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A command-object modifier must not turn failed assurance into green CI."""

    aggregate = "      - uv run python scripts/verify.py --plan ci\n"
    command_object = (
        "      - cmd: uv run python scripts/verify.py --plan ci\n        ignore_error: true\n"
    )
    _patch_taskfile(
        tmp_path,
        monkeypatch,
        lambda source: source.replace(aggregate, command_object, 1),
    )

    findings = find_forbidden_reach("task ci")

    assert len(findings) == 1
    assert "task:ci shape differs" in findings[0]
    assert "ignore_error: true" in findings[0]


def test_ci_policy_subtask_cannot_be_conditionally_skipped(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A platform condition cannot suppress the guard on a hosted runner."""

    policy_subtask = "      - task: ci:policy\n"
    conditioned_subtask = policy_subtask + "        platforms: [darwin]\n"
    _patch_taskfile(
        tmp_path,
        monkeypatch,
        lambda source: source.replace(policy_subtask, conditioned_subtask, 1),
    )

    findings = find_forbidden_reach("task ci")

    assert len(findings) == 1
    assert "task:ci shape differs" in findings[0]
    assert "platforms: [darwin]" in findings[0]
