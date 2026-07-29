"""Tests for the hosted-CI lean-lane policy guard."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.repo_tools.hosted_ci_policy as hosted_ci_policy
from scripts.repo_tools.hosted_ci_policy import (
    expand_aggregate_commands,
    expand_shell_script_commands,
    extract_action_references,
    extract_run_commands,
    find_all_policy_violations,
    find_forbidden_reach,
    find_jobs_without_timeout,
    find_policy_violations,
    unresolved_shell_script_invocations,
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


def test_extract_run_commands_supports_scalar_modifiers_and_comments() -> None:
    """Valid YAML chomping/indentation modifiers must not hide workflow commands."""

    source = _workflow(
        "      - name: Block\n"
        "        run: |2- # preserve command boundaries\n"
        "          uv run python -m pytest\n"
    )

    assert extract_run_commands(source) == ["uv run python -m pytest"]


def test_extract_action_references_reads_pinned_uses() -> None:
    """Action references are extracted for the SHA-pin check."""

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


def test_a_non_aggregate_command_expands_to_nothing() -> None:
    """Only the verification runner is treated as an aggregate."""

    assert expand_aggregate_commands("uv sync --frozen") == []


def test_local_shell_script_body_is_expanded_and_scanned(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A forbidden command in a delegated local script must fail the guard."""

    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "heavy.sh").write_text(
        "#!/usr/bin/env bash\nuv run mkdocs \\\n  build --strict\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(hosted_ci_policy, "REPOSITORY_ROOT", tmp_path)

    expanded = expand_shell_script_commands("./scripts/heavy.sh")
    reasons = " ".join(find_forbidden_reach("./scripts/heavy.sh"))

    assert expanded == [
        (
            "shell script scripts/heavy.sh -> ./scripts/heavy.sh",
            "uv run mkdocs build --strict",
        )
    ]
    assert "application or site build" in reasons
    assert "shell script scripts/heavy.sh" in reasons


def test_unresolvable_local_shell_scripts_are_blocking(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Missing and root-escaping script leaves must not pass as opaque strings."""

    monkeypatch.setattr(hosted_ci_policy, "REPOSITORY_ROOT", tmp_path)

    assert unresolved_shell_script_invocations("./scripts/missing.sh") == [
        "shell script ./scripts/missing.sh does not exist"
    ]
    assert unresolved_shell_script_invocations("../outside.sh") == [
        "shell script ../outside.sh escapes the repository"
    ]
    assert "cannot verify script body" in " ".join(find_forbidden_reach("./scripts/missing.sh"))


def test_a_job_without_a_timeout_is_a_violation() -> None:
    """A hung step must fail fast, not burn GitHub's six-hour default."""

    source = "jobs:\n  checks:\n    runs-on: ubuntu-latest\n    steps:\n      - run: true\n"

    assert find_jobs_without_timeout(source) == ["checks"]


def test_a_job_with_a_timeout_is_accepted() -> None:
    """The guard recognises a declared job-level timeout."""

    assert find_jobs_without_timeout(WORKFLOW_PREAMBLE) == []


def test_find_policy_violations_accepts_a_sha_pinned_action(tmp_path: Path) -> None:
    """A full-SHA action pin satisfies the supply-chain invariant on its own."""

    workflow = tmp_path / "ci.yml"
    workflow.write_text(
        _workflow(f"      - uses: actions/checkout@{'a' * 40} # v9.9.9\n"),
        encoding="utf-8",
    )

    assert find_policy_violations(workflow, enforce_exact_contract=False) == []


def test_find_policy_violations_reports_an_unpinned_action(tmp_path: Path) -> None:
    """A tag-pinned action is mutable upstream, so the guard must reject it."""

    workflow = tmp_path / "ci.yml"
    workflow.write_text(_workflow("      - uses: actions/checkout@v7\n"), encoding="utf-8")

    violations = find_policy_violations(workflow, enforce_exact_contract=False)

    assert any("uses: actions/checkout@v7" in violation for violation in violations)
