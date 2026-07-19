#!/usr/bin/env python3
"""Structured verification runner for local and CI maintainers.

Ownership: repository tooling. This module is the single source of truth for
*which* checks run and *when*, so hosted CI, the pre-push hook, and the deploy
gate can never drift apart. Workflows call it; they never list steps themselves.

Invariants:

* The three plans are nested — ``ci`` ⊂ ``prepush`` ⊂ ``validate`` — so moving a
  check between tiers can never drop it. ``tests/test_verify.py`` enforces this.
* The ``ci`` plan contains nothing forbidden in the hosted lane by section 4 of
  ``patapsco/docs/app-consistency-standard.md``: no test suite, no site build,
  no browser suite. ``scripts/check_hosted_ci_policy.py`` enforces that
  mechanically, by resolving this module's plans rather than trusting the
  workflow's command string.
* No step can hang the runner: stdin is closed and every step is bounded by a
  timeout.

Boundary: this module only sequences subprocesses and reports results. The
checks themselves live in ``scripts/check_*.py`` and ``scripts/repo_tools/``.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, TextIO, get_args

REPO_ROOT = Path(__file__).resolve().parents[1]

Plan = Literal["ci", "prepush", "validate"]
PLANS: tuple[str, ...] = get_args(Plan)
DEFAULT_PLAN: Plan = "prepush"

# No verification step in this repository takes more than a couple of seconds.
# A step that runs for ten minutes is hung, not slow, so cap it and fail with a
# named step instead of letting the hosted runner sit at GitHub's six-hour
# default. The workflows also set `timeout-minutes` as an outer backstop.
DEFAULT_STEP_TIMEOUT_SECONDS = 600.0


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
    plan: Plan = DEFAULT_PLAN,
) -> list[VerifyStep]:
    """Return the ordered verification steps for one tier of the check plan.

    The three tiers are the ones section 4 of the civic-app consistency
    standard (``patapsco/docs/app-consistency-standard.md``) defines for every
    repository in the family, and each is a strict superset of the one above it:

    ``ci``
        What hosted GitHub Actions runs. Static checks, contracts, and the
        workflow-policy guard only: linting, type-checking, and the validators
        that read ``docs/`` source. **No test suite, no site build, and nothing
        that reads ``site/``** — those are forbidden in the hosted lane.

    ``prepush``
        The local pre-push hook and the pre-deploy gate. Everything in ``ci``
        plus the repo-automation test suite, the strict MkDocs build, and the
        checks that inspect the built ``site/`` output.

    ``validate``
        Everything in ``prepush`` plus the Playwright browser smoke checks,
        which need a downloaded browser and so stay a deliberate local step.

    Nothing is dropped when a step leaves the hosted lane — every assertion
    still runs, in the tier that can afford it.
    """

    python = python_executable or sys.executable

    # Tier 1 — hosted CI. Static analysis and source validators only.
    steps = [
        VerifyStep(
            name="Checking hosted CI policy",
            command=(python, "scripts/check_hosted_ci_policy.py"),
        ),
        VerifyStep(
            name="Linting repo automation",
            command=(python, "-m", "ruff", "check", "main.py", "scripts", "tests"),
        ),
        VerifyStep(
            name="Type-checking repo automation",
            command=(python, "-m", "mypy"),
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
            name="Checking raw HTML links",
            command=(python, "scripts/check_html_links.py"),
        ),
    ]

    if plan == "ci":
        return steps

    # Tier 2 — pre-push and pre-deploy: the test suite, the build, and
    # everything that needs a freshly built site/ directory.
    steps += [
        VerifyStep(
            name="Running repo automation tests",
            command=(python, "-m", "pytest"),
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
            name="Running accessibility smoke checks",
            command=(python, "scripts/check_accessibility_smoke.py"),
        ),
    ]

    if plan == "prepush":
        return steps

    # Tier 3 — pre-deploy, local only: drives a real browser.
    steps.append(
        VerifyStep(
            name="Running browser smoke checks",
            command=(python, "scripts/check_browser_smoke.py"),
        )
    )

    return steps


def run_step(
    step: VerifyStep,
    cwd: Path,
    *,
    timeout_seconds: float = DEFAULT_STEP_TIMEOUT_SECONDS,
) -> VerifyResult:
    """Run one verification step and capture its output.

    Two guards keep a misbehaving step from hanging a hosted run forever:

    * ``stdin`` is closed. A child that decides to prompt gets EOF and exits
      instead of blocking on a runner stdin that will never produce a line.
    * ``timeout_seconds`` bounds the step. On expiry the step fails, by name,
      with whatever output it managed to produce.
    """

    started_at = time.monotonic()
    try:
        completed = subprocess.run(
            step.command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            stdin=subprocess.DEVNULL,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as timeout:
        duration_seconds = time.monotonic() - started_at
        return VerifyResult(
            name=step.name,
            command=step.command,
            exit_code=124,
            duration_seconds=duration_seconds,
            stdout=_decode_stream(timeout.stdout),
            stderr=(
                f"{step.name} timed out after {timeout_seconds:.0f}s and was killed. "
                "It is hung, not slow — no step in this repository takes more than "
                "a few seconds.\n"
            ),
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


def _decode_stream(content: str | bytes | None) -> str:
    """Normalize partial subprocess output, which may be bytes or missing."""

    if content is None:
        return ""
    if isinstance(content, bytes):
        return content.decode("utf-8", errors="replace")
    return content


def _flush(stream: TextIO) -> None:
    """Flush a stream, tolerating the in-memory buffers tests substitute."""

    try:
        stream.flush()
    except (AttributeError, ValueError):  # pragma: no cover - closed/fake streams
        pass


def _write_line(stream: TextIO, line: str) -> None:
    """Write one progress line and flush it so live logs stay current."""

    stream.write(f"{line}\n")
    _flush(stream)


def _write_output(stream: TextIO, content: str) -> None:
    """Write captured command output to a stream without adding extra blank lines."""

    if not content:
        return
    stream.write(content)
    if not content.endswith("\n"):
        stream.write("\n")
    _flush(stream)


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
    timeout_seconds: float = DEFAULT_STEP_TIMEOUT_SECONDS,
) -> int:
    """Run the verification plan and return a shell-compatible exit code.

    Progress is flushed after every write. Piped stdout is block-buffered by
    default, which on a hosted runner means the whole log lands only when the
    process exits — so a slow or hung step looks like a dead job with no output
    at all. Flushing keeps the running step visible in the live log.
    """

    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    results: list[VerifyResult] = []

    for index, step in enumerate(steps, start=1):
        _write_line(stdout, f"[{index}/{len(steps)}] {step.name}...")
        result = run_step(step, cwd, timeout_seconds=timeout_seconds)
        results.append(result)

        _write_output(stdout, result.stdout)
        _write_output(stderr, result.stderr)

        if result.exit_code == 0:
            _write_line(
                stdout,
                f"[{index}/{len(steps)}] {step.name} passed in "
                f"{result.duration_seconds:.2f}s.",
            )
            continue

        _write_line(
            stderr,
            f"[{index}/{len(steps)}] {step.name} failed in "
            f"{result.duration_seconds:.2f}s with exit code {result.exit_code}.",
        )
        if json_output_path is not None:
            write_json_report(results, json_output_path)
        _write_line(stderr, "Verification failed.")
        for line in _summary_lines(results):
            _write_line(stderr, line)
        return 1

    if json_output_path is not None:
        write_json_report(results, json_output_path)

    _write_line(stdout, "Verification passed.")
    for line in _summary_lines(results):
        _write_line(stdout, line)
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI flags for the structured verification runner."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plan",
        choices=PLANS,
        default=DEFAULT_PLAN,
        help=(
            "Which tier to run. 'ci' is the hosted lane: static checks only, no "
            "tests and no site build. 'prepush' adds the test suite, the strict "
            "MkDocs build, and the built-site checks. 'validate' adds the "
            f"Playwright browser smoke checks. Defaults to '{DEFAULT_PLAN}'."
        ),
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Write a machine-readable verification report to this path.",
    )
    parser.add_argument(
        "--step-timeout",
        type=float,
        default=DEFAULT_STEP_TIMEOUT_SECONDS,
        help=(
            "Seconds any single step may run before it is killed as hung. "
            f"Defaults to {DEFAULT_STEP_TIMEOUT_SECONDS:.0f}."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the repository verification plan from the command line."""

    args = parse_args(argv)

    try:
        steps = build_steps(REPO_ROOT, plan=args.plan)
        return run_verification(
            steps,
            REPO_ROOT,
            json_output_path=args.json_output,
            timeout_seconds=args.step_timeout,
        )
    except Exception as error:  # noqa: BLE001
        sys.stderr.write(f"Verification runner failed unexpectedly: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
