"""Happy- and failure-path tests for thin validator CLI entry points."""

from __future__ import annotations

import importlib

import pytest

VALIDATOR_CASES = (
    (
        "scripts.check_platform_guard_evidence",
        "scripts.repo_tools.platform_guard_evidence",
        "find_platform_guard_evidence_issues",
        "Platform guard evidence validated.",
    ),
)


@pytest.mark.parametrize(
    ("cli_module_name", "finder_module_name", "finder_name", "success_message"),
    VALIDATOR_CASES,
)
def test_validator_cli_reports_success(
    cli_module_name: str,
    finder_module_name: str,
    finder_name: str,
    success_message: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Each thin CLI should return zero and its own success message."""

    cli_module = importlib.import_module(cli_module_name)
    finder_module = importlib.import_module(finder_module_name)
    monkeypatch.setattr(finder_module, finder_name, lambda _target: [])

    assert cli_module.main() == 0
    captured = capsys.readouterr()
    assert captured.out == f"{success_message}\n"
    assert captured.err == ""


@pytest.mark.parametrize(
    ("cli_module_name", "finder_module_name", "finder_name", "_success_message"),
    VALIDATOR_CASES,
)
def test_validator_cli_reports_findings(
    cli_module_name: str,
    finder_module_name: str,
    finder_name: str,
    _success_message: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Each thin CLI should return nonzero and surface validator evidence."""

    cli_module = importlib.import_module(cli_module_name)
    finder_module = importlib.import_module(finder_module_name)
    monkeypatch.setattr(finder_module, finder_name, lambda _target: ["fixture issue"])

    assert cli_module.main() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "fixture issue" in captured.err
