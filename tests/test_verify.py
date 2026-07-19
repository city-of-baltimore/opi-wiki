"""Tests for the structured verification runner."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from scripts.verify import VerifyStep, build_steps, main, parse_args, run_verification


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


def test_parse_args_supports_optional_browser_smoke_flag() -> None:
    """The verification runner should support opting into browser smoke coverage."""

    args = parse_args(["--include-browser-smoke", "--json-output", "report.json"])

    assert args.include_browser_smoke is True
    assert args.json_output == Path("report.json")


def test_build_steps_can_append_browser_smoke_checks() -> None:
    """Optional browser smoke should append after the fast static checks."""

    step_names = [
        step.name for step in build_steps(Path("/tmp/example"), include_browser_smoke=True)
    ]

    assert "Running browser smoke checks" in step_names


def test_build_steps_checks_built_links_right_after_the_strict_build() -> None:
    """The built-site link crawl needs the freshly built site/ directory."""

    step_names = [step.name for step in build_steps(Path("/tmp/example"))]

    build_index = step_names.index("Building MkDocs site with strict validation")
    assert step_names[build_index + 1] == "Checking built-site internal links"


def test_lean_plan_excludes_the_build_and_every_built_site_check() -> None:
    """Hosted PR CI must stay static: no site build, nothing that reads site/."""

    lean_names = [step.name for step in build_steps(Path("/tmp/example"), lean=True)]

    assert "Building MkDocs site with strict validation" not in lean_names
    assert "Checking built-site internal links" not in lean_names
    assert "Running accessibility smoke checks" not in lean_names
    assert "Running browser smoke checks" not in lean_names


def test_lean_plan_keeps_every_static_check() -> None:
    """Moving the build out of PR CI must not drop any static check."""

    lean_names = [step.name for step in build_steps(Path("/tmp/example"), lean=True)]

    assert lean_names == [
        "Linting repo automation",
        "Type-checking repo automation",
        "Running repo automation tests",
        "Validating page metadata",
        "Validating brand terms",
        "Checking editorial voice guardrail",
        "Checking page consistency",
        "Checking raw HTML links",
    ]


def test_full_plan_is_the_lean_plan_plus_the_built_site_checks() -> None:
    """The deploy gate still runs everything; lean is a strict prefix of it."""

    lean_names = [step.name for step in build_steps(Path("/tmp/example"), lean=True)]
    full_names = [step.name for step in build_steps(Path("/tmp/example"))]

    assert full_names[: len(lean_names)] == lean_names
    assert full_names[len(lean_names) :] == [
        "Building MkDocs site with strict validation",
        "Checking built-site internal links",
        "Running accessibility smoke checks",
    ]


def test_parse_args_supports_the_lean_flag() -> None:
    """The runner exposes the lean plan to the hosted workflow."""

    assert parse_args(["--lean"]).lean is True
    assert parse_args([]).lean is False


def test_main_rejects_lean_plus_browser_smoke(capsys: pytest.CaptureFixture[str]) -> None:
    """Browser smoke needs the built site, so it cannot ride the lean plan."""

    exit_code = main(["--lean", "--include-browser-smoke"])

    assert exit_code == 2
    assert "mutually exclusive" in capsys.readouterr().err
