#!/usr/bin/env python3
"""Structured verification runner for local and CI maintainers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TextIO

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class VerifyStep:
    """A named verification command."""

    name: str
    command: tuple[str, ...]


@dataclass(frozen=True)
class VerifyResult:
    """The outcome of one verification command."""

    name: str
    command: tuple[str, ...]
    exit_code: int
    duration_seconds: float
    stdout: str
    stderr: str


def build_steps(
    repo_root: Path,
    python_executable: str | None = None,
    *,
    include_browser_smoke: bool = False,
) -> list[VerifyStep]:
    """Return the ordered verification steps for this repository."""

    python = python_executable or sys.executable
    steps = [
        VerifyStep(
            name="Linting repo automation",
            command=(python, "-m", "ruff", "check", "main.py", "scripts", "tests"),
        ),
        VerifyStep(
            name="Type-checking repo automation",
            command=(python, "-m", "mypy"),
        ),
        VerifyStep(
            name="Running repo automation tests",
            command=(python, "-m", "pytest"),
        ),
        VerifyStep(
            name="Validating page metadata",
            command=(python, "scripts/check_page_metadata.py"),
        ),
        VerifyStep(
            name="Validating brand terms",
            command=(python, "scripts/check_brand_terms.py"),
        ),
        VerifyStep(
            name="Checking editorial voice guardrail",
            command=(python, "scripts/check_style.py"),
        ),
        VerifyStep(
            name="Checking page consistency",
            command=(python, "scripts/check_consistency.py"),
        ),
        VerifyStep(
            name="Building MkDocs site with strict validation",
            command=(python, "-m", "mkdocs", "build", "--strict"),
        ),
        VerifyStep(
            name="Checking built-site internal links",
            command=(python, "scripts/check_built_links.py", "site"),
        ),
        VerifyStep(
            name="Checking raw HTML links",
            command=(python, "scripts/check_html_links.py"),
        ),
        VerifyStep(
            name="Running accessibility smoke checks",
            command=(python, "scripts/check_accessibility_smoke.py"),
        ),
    ]

    if include_browser_smoke:
        steps.append(
            VerifyStep(
                name="Running browser smoke checks",
                command=(python, "scripts/check_browser_smoke.py"),
            )
        )

    return steps


def run_step(step: VerifyStep, cwd: Path) -> VerifyResult:
    """Run one verification step and capture its output."""

    started_at = time.monotonic()
    try:
        completed = subprocess.run(
            step.command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:
        duration_seconds = time.monotonic() - started_at
        return VerifyResult(
            name=step.name,
            command=step.command,
            exit_code=1,
            duration_seconds=duration_seconds,
            stdout="",
            stderr=f"{step.name} could not start: {error}\n",
        )

    duration_seconds = time.monotonic() - started_at
    return VerifyResult(
        name=step.name,
        command=step.command,
        exit_code=completed.returncode,
        duration_seconds=duration_seconds,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def _write_output(stream: TextIO, content: str) -> None:
    """Write captured command output to a stream without adding extra blank lines."""

    if not content:
        return
    stream.write(content)
    if not content.endswith("\n"):
        stream.write("\n")


def _summary_lines(results: Sequence[VerifyResult]) -> list[str]:
    """Build human-readable summary lines for a verification run."""

    lines: list[str] = []
    for result in results:
        status = "passed" if result.exit_code == 0 else f"failed (exit {result.exit_code})"
        lines.append(
            f"- {result.name}: {status} in {result.duration_seconds:.2f}s"
        )
    return lines


def write_json_report(results: Sequence[VerifyResult], output_path: Path) -> None:
    """Persist a machine-readable verification report."""

    report = {
        "generated_at_epoch": time.time(),
        "all_passed": all(result.exit_code == 0 for result in results),
        "results": [asdict(result) for result in results],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def run_verification(
    steps: Sequence[VerifyStep],
    cwd: Path,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    json_output_path: Path | None = None,
) -> int:
    """Run the verification plan and return a shell-compatible exit code."""

    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    results: list[VerifyResult] = []

    for index, step in enumerate(steps, start=1):
        stdout.write(f"[{index}/{len(steps)}] {step.name}...\n")
        result = run_step(step, cwd)
        results.append(result)

        _write_output(stdout, result.stdout)
        _write_output(stderr, result.stderr)

        if result.exit_code == 0:
            stdout.write(
                f"[{index}/{len(steps)}] {step.name} passed in "
                f"{result.duration_seconds:.2f}s.\n"
            )
            continue

        stderr.write(
            f"[{index}/{len(steps)}] {step.name} failed in "
            f"{result.duration_seconds:.2f}s with exit code {result.exit_code}.\n"
        )
        if json_output_path is not None:
            write_json_report(results, json_output_path)
        stderr.write("Verification failed.\n")
        for line in _summary_lines(results):
            stderr.write(f"{line}\n")
        return 1

    if json_output_path is not None:
        write_json_report(results, json_output_path)

    stdout.write("Verification passed.\n")
    for line in _summary_lines(results):
        stdout.write(f"{line}\n")
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI flags for the structured verification runner."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--include-browser-smoke",
        action="store_true",
        help="Run optional Playwright smoke checks against the built site.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Write a machine-readable verification report to this path.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the repository verification plan from the command line."""

    args = parse_args(argv)

    try:
        steps = build_steps(REPO_ROOT, include_browser_smoke=args.include_browser_smoke)
        return run_verification(
            steps,
            REPO_ROOT,
            json_output_path=args.json_output,
        )
    except Exception as error:  # noqa: BLE001
        sys.stderr.write(f"Verification runner failed unexpectedly: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
