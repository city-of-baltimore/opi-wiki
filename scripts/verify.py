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
  workflow's command string. Note that it is the *only* check that does so:
  Patapsco's ``platform-check`` (0.6.17), which the ``ci`` plan also runs,
  expands ``npm`` and ``.sh`` bodies but not a Python plan module, so it cannot
  see a forbidden step added to the ``ci`` tier of :func:`build_steps`. Both
  checks are therefore load-bearing.

  Both policy checkers are *also* invoked directly from the ``ci:policy`` task.
  The estate's own enforcement rule proves the hosted gate reaches a policy
  command by walking ``Taskfile`` edges and cannot follow a Python plan module,
  so the ordinary Taskfile edge is what makes this gate visible from outside.
* No step can hang the runner: stdin is closed and every step is bounded by a
  timeout.

Boundary: this module only sequences subprocesses and reports results. The
checks themselves live in ``scripts/check_*.py`` and ``scripts/repo_tools/``.
"""

from __future__ import annotations

import argparse
import json

# B404: sequencing subprocesses is this module's entire job. Every command is a
# literal tuple from build_steps(); none is built from caller input, and none
# runs through a shell.
import subprocess  # nosec B404
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

# The exhaustive canonical-route browser audit intentionally takes several
# minutes. No step should approach ten minutes, so cap it and fail with a named
# step instead of letting a runner sit at GitHub's six-hour default. The
# workflows also set `timeout-minutes` as an outer backstop.
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
        The local pre-push hook. Everything in ``ci`` plus the repo-automation
        test suite, the strict MkDocs build, and the checks that inspect the
        built ``site/`` output.

    ``validate``
        The pre-mutation boundary: everything in ``prepush`` plus browser
        interaction and full-route accessibility assurance. These need a
        downloaded browser, so they run locally before a release and in the
        Pages deploy gate, which installs one — never in the pull-request lane.

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
            name="Checking browser readiness source contract",
            command=(python, "scripts/check_browser_readiness_contract.py"),
        ),
        VerifyStep(
            name="Validating platform guard evidence",
            command=(python, "scripts/check_platform_guard_evidence.py"),
        ),
        # Patapsco's shared estate baseline that applies to this docs site: the
        # app marker, shared task surface, ruff/mypy/bandit configuration,
        # ignore-file baseline, workflow shapes, and pre-push hook. Invoked as
        # `-m` rather than via the `platform-check` console script so it
        # resolves through this interpreter like every other step, instead of
        # depending on what is first on PATH.
        #
        # This is additive to the guard above, not a replacement for it. The
        # local guard walks the verify.py plans and holds the workflow
        # allowlists; platform-check 0.6.17 does neither.
        #
        # `ci:policy` invokes the same checker directly, exactly as it already
        # does for the local guard above. That is not an accident: the estate's
        # own enforcement rule proves the hosted gate reaches a policy command
        # by walking Taskfile edges, and it cannot see into a Python plan
        # module, so the ordinary edge is what makes this gate visible. The
        # step stays here so a plan remains runnable and self-contained.
        VerifyStep(
            name="Checking platform baseline conformance",
            command=(python, "-m", "baltimore.patapsco.baseline.cli", "--repo", "."),
        ),
        # Both ruff runs pin --config for the same reason the Taskfile does:
        # without it ruff selects a configuration by walking up from each
        # discovered file, so the enforced rule set would depend on the paths
        # passed rather than on this repository's declared lint contract.
        VerifyStep(
            name="Checking repo automation formatting",
            command=(
                python,
                "-m",
                "ruff",
                "format",
                "--config",
                "pyproject.toml",
                "--check",
                "main.py",
                "scripts",
                "tests",
            ),
        ),
        VerifyStep(
            name="Linting repo automation",
            command=(
                python,
                "-m",
                "ruff",
                "check",
                "--config",
                "pyproject.toml",
                "main.py",
                "scripts",
                "tests",
            ),
        ),
        VerifyStep(
            name="Type-checking repo automation",
            command=(python, "-m", "mypy"),
        ),
        VerifyStep(
            name="Scanning repo automation for security issues",
            command=(
                python,
                "-m",
                "bandit",
                "-q",
                "-c",
                "pyproject.toml",
                "-r",
                "main.py",
                "scripts",
            ),
        ),
        VerifyStep(
            name="Validating page metadata",
            command=(python, "scripts/check_page_metadata.py"),
        ),
        VerifyStep(
            name="Validating organization data",
            command=(python, "scripts/check_organization_data.py"),
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
            name="Checking product contract links",
            command=(python, "scripts/check_product_contract_links.py"),
        ),
        VerifyStep(
            name="Checking raw HTML links",
            command=(python, "scripts/check_html_links.py"),
        ),
    ]

    if plan == "ci":
        return steps

    # Tier 2 — pre-push: the test suite, the build, and everything that needs a
    # freshly built site/ directory.
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
            name="Checking built-content visibility",
            command=(python, "scripts/check_built_visibility.py"),
        ),
        VerifyStep(
            name="Checking built-artifact safety",
            command=(python, "scripts/check_built_artifact.py"),
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

    # Tier 3 — the pre-mutation boundary: drives a real browser, so it runs
    # locally and in the Pages deploy gate, never in the pull-request lane.
    steps += [
        VerifyStep(
            name="Running browser smoke checks",
            command=(python, "scripts/check_browser_smoke.py"),
        ),
        VerifyStep(
            name="Running full browser accessibility audit",
            command=(python, "scripts/check_browser_accessibility.py"),
        ),
    ]

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
        # S603: every command is a literal tuple built in build_steps() above and
        # run without a shell. No caller-supplied string reaches this call.
        completed = subprocess.run(  # nosec B603  # noqa: S603
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
                "Even the exhaustive browser audit should finish within this "
                "bounded allowance.\n"
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
        lines.append(f"- {result.name}: {status} in {result.duration_seconds:.2f}s")
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
                f"[{index}/{len(steps)}] {step.name} passed in {result.duration_seconds:.2f}s.",
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
            "MkDocs build, and the built-site checks. 'validate' adds browser "
            "interaction and full-route accessibility assurance. "
            f"Defaults to '{DEFAULT_PLAN}'."
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
