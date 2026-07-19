"""Tests for the structured verification runner."""

from __future__ import annotations

import io
import json
import sys
from collections.abc import Sequence
from pathlib import Path

import pytest
from scripts.verify import (
    PLANS,
    VerifyStep,
    build_steps,
    main,
    parse_args,
    run_step,
    run_verification,
)


def _python_command(source: str) -> tuple[str, ...]:
    """Return a portable Python one-liner command for test verification steps."""

    return (sys.executable, "-c", source)


def test_run_verification_reports_success_and_json(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """Successful runs should report step timing and write an optional JSON artifact."""

    json_output = tmp_path / "verify.json"
    steps = [
        VerifyStep("First step", _python_command("print('alpha')")),
        VerifyStep("Second step", _python_command("print('beta')")),
    ]

    exit_code = run_verification(steps, tmp_path, json_output_path=json_output)

    captured = capsys.readouterr()
    report = json.loads(json_output.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "[1/2] First step..." in captured.out
    assert "[2/2] Second step passed" in captured.out
    assert "Verification passed." in captured.out
    assert captured.err == ""
    assert report["all_passed"] is True
    assert [result["name"] for result in report["results"]] == ["First step", "Second step"]


def test_run_verification_stops_on_first_failure(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """Failures should stop the run and emit a concise stderr summary."""

    steps = [
        VerifyStep("Healthy step", _python_command("print('ok')")),
        VerifyStep(
            "Broken step",
            _python_command("import sys; print('boom', file=sys.stderr); raise SystemExit(3)"),
        ),
        VerifyStep("Skipped step", _python_command("print('should not run')")),
    ]

    exit_code = run_verification(steps, tmp_path)

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "ok" in captured.out
    assert "boom" in captured.err
    assert "Broken step failed" in captured.err
    assert "Skipped step" not in captured.out
    assert "- Healthy step: passed" in captured.err
    assert "- Broken step: failed (exit 3)" in captured.err


def test_ci_plan_excludes_the_test_suite_the_build_and_every_built_site_check() -> None:
    """Hosted CI must stay static: no test suite, no site build, nothing reading site/."""

    ci_names = [step.name for step in build_steps(Path("/tmp/example"), plan="ci")]

    assert "Running repo automation tests" not in ci_names
    assert "Building MkDocs site with strict validation" not in ci_names
    assert "Checking built-site internal links" not in ci_names
    assert "Running accessibility smoke checks" not in ci_names
    assert "Running browser smoke checks" not in ci_names


def test_ci_plan_keeps_every_static_check() -> None:
    """Trimming the hosted lane must not drop a static check."""

    ci_names = [step.name for step in build_steps(Path("/tmp/example"), plan="ci")]

    assert ci_names == [
        "Checking hosted CI policy",
        "Checking platform baseline conformance",
        "Linting repo automation",
        "Type-checking repo automation",
        "Scanning repo automation for security issues",
        "Validating page metadata",
        "Validating brand terms",
        "Checking editorial voice guardrail",
        "Checking page consistency",
        "Checking raw HTML links",
    ]


def test_ci_plan_runs_both_policy_checkers() -> None:
    """The lean gate runs the local guard AND Patapsco's shared baseline check.

    They are not interchangeable, and the difference is measured rather than
    assumed: ``platform-check`` 0.4.0 resolves the ``Taskfile.yml`` graph but
    treats ``verify.py --plan ci`` as an opaque leaf, so a forbidden command
    added to this module's ``ci`` tier passes it. It also has no job-timeout
    rule and no ``run:``/``uses:`` allowlist. Dropping either checker is a real
    loss of coverage; see the "Two checkers" note in
    ``scripts/check_hosted_ci_policy.py``.
    """

    commands = [" ".join(step.command) for step in build_steps(Path("/tmp/example"), plan="ci")]

    assert any("check_hosted_ci_policy.py" in command for command in commands)
    assert any("baltimore.patapsco.baseline.cli" in command for command in commands)


def test_prepush_plan_owns_the_tests_the_build_and_the_built_site_checks() -> None:
    """Everything removed from the hosted lane still runs, one tier down."""

    prepush_names = [step.name for step in build_steps(Path("/tmp/example"), plan="prepush")]

    assert "Running repo automation tests" in prepush_names
    assert "Building MkDocs site with strict validation" in prepush_names
    assert "Checking built-site internal links" in prepush_names
    assert "Running accessibility smoke checks" in prepush_names


def test_built_link_crawl_runs_right_after_the_strict_build() -> None:
    """The built-site link crawl needs the freshly built site/ directory."""

    step_names = [step.name for step in build_steps(Path("/tmp/example"), plan="prepush")]

    build_index = step_names.index("Building MkDocs site with strict validation")
    assert step_names[build_index + 1] == "Checking built-site internal links"


def test_validate_plan_adds_the_browser_smoke_checks() -> None:
    """Browser smoke is the pre-deploy tier: it needs a real downloaded browser."""

    validate_names = [step.name for step in build_steps(Path("/tmp/example"), plan="validate")]

    assert validate_names[-1] == "Running browser smoke checks"


def test_each_plan_is_a_strict_prefix_of_the_next() -> None:
    """Nested tiers are what guarantees moving a check between them never drops it."""

    ci_names = [step.name for step in build_steps(Path("/tmp/example"), plan="ci")]
    prepush_names = [step.name for step in build_steps(Path("/tmp/example"), plan="prepush")]
    validate_names = [step.name for step in build_steps(Path("/tmp/example"), plan="validate")]

    assert prepush_names[: len(ci_names)] == ci_names
    assert validate_names[: len(prepush_names)] == prepush_names
    assert len(ci_names) < len(prepush_names) < len(validate_names)


def test_every_declared_plan_builds() -> None:
    """The CLI choices and the plan builder cannot drift apart."""

    for plan in PLANS:
        assert build_steps(Path("/tmp/example"), plan=plan)  # type: ignore[arg-type]


def test_parse_args_defaults_to_the_prepush_plan() -> None:
    """A bare local run gets the tests and the build, not just the static checks."""

    assert parse_args([]).plan == "prepush"
    assert parse_args(["--plan", "ci"]).plan == "ci"
    assert parse_args(["--plan", "validate"]).plan == "validate"


def test_parse_args_rejects_an_unknown_plan() -> None:
    """An unrecognised tier is a typo, not a silent fall-through to a lean run."""

    with pytest.raises(SystemExit):
        parse_args(["--plan", "lean"])


def test_run_step_kills_a_hung_command_instead_of_hanging_the_runner(tmp_path: Path) -> None:
    """A step that never returns must fail by name, not stall the job."""

    step = VerifyStep("Hanging step", _python_command("import time; time.sleep(30)"))

    result = run_step(step, tmp_path, timeout_seconds=1)

    assert result.exit_code == 124
    assert "Hanging step timed out after 1s" in result.stderr
    assert result.duration_seconds < 30


def test_run_step_closes_stdin_so_a_prompting_command_cannot_block(tmp_path: Path) -> None:
    """Reading stdin must hit EOF immediately rather than wait on a runner forever."""

    step = VerifyStep(
        "Prompting step",
        _python_command("import sys; print(repr(sys.stdin.read()))"),
    )

    result = run_step(step, tmp_path, timeout_seconds=10)

    assert result.exit_code == 0
    assert "''" in result.stdout


def test_run_verification_flushes_progress_for_live_logs(tmp_path: Path) -> None:
    """Progress lines must reach the log as they happen, not in one dump at exit."""

    flushes: list[str] = []

    class RecordingStream(io.StringIO):
        def flush(self) -> None:
            flushes.append(self.getvalue())

    stdout = RecordingStream()
    steps = [VerifyStep("Only step", _python_command("print('alpha')"))]

    exit_code = run_verification(steps, tmp_path, stdout=stdout, stderr=io.StringIO())

    assert exit_code == 0
    assert flushes, "progress was never flushed"
    assert "[1/1] Only step..." in flushes[0]


def test_main_runs_the_requested_plan(monkeypatch: pytest.MonkeyPatch) -> None:
    """The CLI plan flag selects the tier that actually runs."""

    recorded: list[str] = []

    def _capture(steps: Sequence[VerifyStep], cwd: Path, **kwargs: object) -> int:
        recorded.extend(step.name for step in steps)
        return 0

    monkeypatch.setattr("scripts.verify.run_verification", _capture)

    assert main(["--plan", "ci"]) == 0
    assert "Checking hosted CI policy" in recorded
    assert "Running repo automation tests" not in recorded

    recorded.clear()
    assert main(["--plan", "validate"]) == 0
    assert "Running repo automation tests" in recorded
    assert "Running browser smoke checks" in recorded


def test_main_passes_the_step_timeout_through(monkeypatch: pytest.MonkeyPatch) -> None:
    """The hang guard must be reachable from the command line."""

    seen: dict[str, object] = {}

    def _capture(steps: Sequence[VerifyStep], cwd: Path, **kwargs: object) -> int:
        seen.update(kwargs)
        return 0

    monkeypatch.setattr("scripts.verify.run_verification", _capture)

    assert main(["--plan", "ci", "--step-timeout", "12"]) == 0
    assert seen["timeout_seconds"] == 12.0
