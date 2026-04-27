"""Tests for the structured verification runner."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from scripts.verify import VerifyStep, build_steps, run_verification


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


def test_build_steps_keeps_fly_validation_optional(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fly validation should only appear when both the binary and config are present."""

    repo_root = Path("/tmp/example")

    monkeypatch.setattr("scripts.verify.shutil.which", lambda command: None)
    assert [step.name for step in build_steps(repo_root)][-1] != "Validating Fly config"

    monkeypatch.setattr("scripts.verify.shutil.which", lambda command: "/usr/local/bin/flyctl")
    monkeypatch.setattr(Path, "exists", lambda self: self.name == "fly.toml")
    assert [step.name for step in build_steps(repo_root)][-1] == "Validating Fly config"
