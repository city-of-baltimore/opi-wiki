"""Adversarial tests for the exact hosted-CI workflow contract."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import scripts.repo_tools.hosted_ci_policy as hosted_ci_policy
from scripts.repo_tools.hosted_ci_contract import (
    find_ci_workflow_shape_violations,
)
from scripts.repo_tools.hosted_ci_policy import (
    find_all_policy_violations,
    find_policy_violations,
)

CI_WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"


def _current_source() -> str:
    """Return the exact workflow whose shape production enforces."""

    return CI_WORKFLOW.read_text(encoding="utf-8")


def _step_block(source: str, start: str, end: str) -> tuple[int, int, str]:
    """Return one step block bounded by two unique line prefixes."""

    start_index = source.index(start)
    end_index = source.index(end, start_index)
    return start_index, end_index, source[start_index:end_index]


def _remove_step(source: str, start: str, end: str) -> str:
    """Remove one complete step block from a workflow."""

    start_index, end_index, _block = _step_block(source, start, end)
    return source[:start_index] + source[end_index:]


def _swap_adjacent_steps(source: str, first: str, second: str, after: str) -> str:
    """Swap two adjacent complete steps without changing their contents."""

    first_index, second_index, first_block = _step_block(source, first, second)
    _second_index, after_index, second_block = _step_block(source, second, after)
    return source[:first_index] + second_block + first_block + source[after_index:]


def _write_workflow(tmp_path: Path, source: str) -> Path:
    """Write one workflow mutation for the public policy adapter."""

    path = tmp_path / "ci.yml"
    path.write_text(source, encoding="utf-8")
    return path


def test_current_ci_workflow_matches_the_exact_contract() -> None:
    """The committed workflow must be the one independently enumerated shape."""

    assert find_ci_workflow_shape_violations(_current_source()) == []


def test_action_revision_and_comments_are_safe_presentation_changes(
    tmp_path: Path,
) -> None:
    """Immutable revision bumps and comments do not change workflow semantics."""

    source = re.sub(
        r"(actions/checkout@)[0-9a-f]{40}",
        rf"\g<1>{'b' * 40}",
        _current_source(),
        count=1,
    )
    source = source.replace(
        "        run: task ci\n",
        "        run: task ci # still the exact gate\n",
        1,
    )
    source = source.replace("jobs:\n", "# Exact comments are safe.\njobs:\n", 1)

    assert find_policy_violations(_write_workflow(tmp_path, source)) == []


@pytest.mark.parametrize(
    ("start", "end", "expected_line"),
    (
        (
            "      - uses: actions/checkout@",
            "      - uses: actions/setup-python@",
            "actions/checkout@<revision>",
        ),
        (
            "      - name: Install dependencies\n",
            "      - name: Run the lean gate\n",
            "name: Install dependencies",
        ),
    ),
)
def test_missing_action_or_run_step_fails_closed(
    start: str,
    end: str,
    expected_line: str,
) -> None:
    """Neither setup assurance nor the required command sequence may shrink."""

    findings = find_ci_workflow_shape_violations(_remove_step(_current_source(), start, end))

    assert any(
        "missing required hosted-CI workflow line" in finding and expected_line in finding
        for finding in findings
    )


def test_an_extra_pinned_action_requires_explicit_contract_approval(
    tmp_path: Path,
) -> None:
    """A full SHA does not authorize a new action identity or hidden build."""

    source = _current_source().replace(
        "      - uses: actions/checkout@",
        f"      - uses: docker/build-push-action@{'a' * 40}\n      - uses: actions/checkout@",
        1,
    )

    findings = find_policy_violations(_write_workflow(tmp_path, source))

    assert any(
        "unexpected hosted-CI workflow line" in finding
        and "docker/build-push-action@<revision>" in finding
        for finding in findings
    )
    assert not any(finding.startswith("uses: docker/build-push-action@") for finding in findings)


def test_an_extra_run_step_fails_even_when_its_command_is_already_allowed() -> None:
    """Duplicating allowlisted work must not bypass exact step cardinality."""

    _start, end, block = _step_block(
        _current_source(),
        "      - name: Install dependencies\n",
        "      - name: Run the lean gate\n",
    )
    source = _current_source()[:end] + block + _current_source()[end:]

    findings = find_ci_workflow_shape_violations(source)

    assert any(
        "duplicate hosted-CI workflow line" in finding and "name: Install dependencies" in finding
        for finding in findings
    )


@pytest.mark.parametrize(
    ("first", "second", "after"),
    (
        (
            "      - uses: actions/checkout@",
            "      - uses: actions/setup-python@",
            "      - uses: arduino/setup-task@",
        ),
        (
            "      - name: Install uv\n",
            "      - name: Install dependencies\n",
            "      - name: Run the lean gate\n",
        ),
    ),
)
def test_reordered_actions_or_run_steps_fail_closed(
    first: str,
    second: str,
    after: str,
) -> None:
    """Order is part of the reviewed workflow, not unordered membership."""

    findings = find_ci_workflow_shape_violations(
        _swap_adjacent_steps(_current_source(), first, second, after)
    )

    assert findings == ["hosted-CI workflow lines are not in the required order"]


@pytest.mark.parametrize(
    "modifier",
    (
        "        if: false\n",
        "        continue-on-error: true\n",
        "        shell: bash\n",
        "        working-directory: /tmp\n",
    ),
)
def test_the_required_gate_rejects_execution_modifiers(modifier: str) -> None:
    """The gate cannot be skipped, ignored, or run through altered semantics."""

    source = _current_source().replace(
        "      - name: Run the lean gate\n",
        "      - name: Run the lean gate\n" + modifier,
        1,
    )

    findings = find_ci_workflow_shape_violations(source)

    assert any(
        "unexpected hosted-CI workflow line" in finding and modifier.strip() in finding
        for finding in findings
    )


def test_inventory_requires_ci_and_rejects_an_extra_nonexempt_workflow(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Renaming or silently growing the hosted workflow inventory must fail."""

    monkeypatch.setattr(hosted_ci_policy, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(hosted_ci_policy, "WORKFLOW_DIRECTORY", tmp_path)
    (tmp_path / "other.yml").write_text(_current_source(), encoding="utf-8")

    findings, paths = find_all_policy_violations()

    assert [path.name for path in paths] == ["other.yml"]
    assert any("missing required hosted-CI workflow: ci.yml" in finding for finding in findings)
    assert any("unexpected hosted-CI workflow: other.yml" in finding for finding in findings)


def test_publish_deploy_and_release_workflows_remain_exempt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Artifact-producing workflows stay outside the lean pull-request contract."""

    monkeypatch.setattr(hosted_ci_policy, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(hosted_ci_policy, "WORKFLOW_DIRECTORY", tmp_path)
    (tmp_path / "ci.yml").write_text(_current_source(), encoding="utf-8")
    for name in ("deploy.yml", "publish.yaml", "release.yml"):
        (tmp_path / name).write_text("not: a hosted CI workflow\n", encoding="utf-8")

    findings, paths = find_all_policy_violations()

    assert findings == []
    assert [path.name for path in paths] == ["ci.yml"]
