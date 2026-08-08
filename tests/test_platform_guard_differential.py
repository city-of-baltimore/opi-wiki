"""Executable evidence for why both hosted-CI policy checkers remain necessary."""

from __future__ import annotations

import importlib.metadata
import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest
from scripts.repo_tools.platform_guard_evidence import (
    MEASURED_PLATFORM_CHECK_VERSION,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
COPY_IGNORE = shutil.ignore_patterns(
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "site",
)


def _materialize_repository(tmp_path: Path) -> Path:
    """Copy this repository to an isolated path the two checkers can both read.

    The object database is deliberately not copied — the matrix needs the
    working tree, not the history. Git's ``config`` is the one exception:
    ``platform-check`` corroborates repository identity from ``remote.origin``,
    and a copy with no remote is not a differently *configured* repository, it
    is an unidentifiable one. Without it every case — including the control —
    fails on identity rather than on the injected violation, which would make
    the whole comparison vacuous.
    """

    repository = tmp_path / "repository"
    shutil.copytree(REPOSITORY_ROOT, repository, ignore=COPY_IGNORE)
    source_config = REPOSITORY_ROOT / ".git" / "config"
    if source_config.is_file():
        git_directory = repository / ".git"
        git_directory.mkdir(exist_ok=True)
        shutil.copy2(source_config, git_directory / "config")
    return repository


@dataclass(frozen=True, slots=True)
class DifferentialCase:
    """One independently injected violation in the five-case comparison."""

    name: str
    inject: Callable[[Path], None]
    local_evidence: str


def _replace_once(path: Path, before: str, after: str) -> None:
    """Replace one stable contract seam, failing loudly if the fixture drifted."""

    source = path.read_text(encoding="utf-8")
    assert source.count(before) == 1, f"expected one injection seam in {path}: {before!r}"
    path.write_text(source.replace(before, after, 1), encoding="utf-8")


def _sub_once(path: Path, pattern: str, replacement: str) -> None:
    """Replace one regex-delimited seam, failing loudly if its shape drifted."""

    source = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.MULTILINE)
    assert count == 1, f"expected one injection seam in {path}: {pattern!r}"
    path.write_text(updated, encoding="utf-8")


def _inject_python_plan_test(repository: Path) -> None:
    """Put pytest inside the Python aggregate that Patapsco cannot expand."""

    _replace_once(
        repository / "scripts" / "verify.py",
        '    if plan == "ci":\n        return steps\n',
        """    if plan == "ci":
        steps.append(
            VerifyStep(
                name="Injected test suite",
                command=(python, "-m", "pytest"),
            )
        )
        return steps
""",
    )


def _inject_shell_to_python_plan(repository: Path) -> None:
    """Reach the heavy Python plan through a shell wrapper."""

    _replace_once(
        repository / "Taskfile.yml",
        "      - uv run python scripts/verify.py --plan ci\n",
        "      - ./scripts/verify.sh --plan prepush\n",
    )


def _remove_job_timeout(repository: Path) -> None:
    """Remove the workflow-level timeout while leaving step timeouts intact."""

    _sub_once(
        repository / ".github" / "workflows" / "ci.yml",
        r"^    timeout-minutes: \d+\n",
        "",
    )


def _inject_arbitrary_run_command(repository: Path) -> None:
    """Add a harmless command outside the repository's exact run allowlist."""

    _replace_once(
        repository / ".github" / "workflows" / "ci.yml",
        "      - name: Run the lean gate\n",
        "      - run: echo probe\n\n      - name: Run the lean gate\n",
    )


CASES = (
    DifferentialCase(
        "Python plan hides pytest",
        _inject_python_plan_test,
        "[unit/integration test suite]",
    ),
    DifferentialCase(
        "shell wrapper reaches Python plan",
        _inject_shell_to_python_plan,
        "[unit/integration test suite]",
    ),
    DifferentialCase(
        "workflow job has no timeout",
        _remove_job_timeout,
        "declares no timeout-minutes",
    ),
    DifferentialCase(
        "workflow adds arbitrary run command",
        _inject_arbitrary_run_command,
        "run: echo probe",
    ),
)
# Retired at 0.6.17: "workflow action uses mutable ref". ``platform-check`` now
# reports any ``uses:`` that is not a SHA-pinned trusted action, so that case no
# longer belongs in a matrix whose whole claim is "the shared checker misses
# this". The local guard still enforces the SHA pin, with its own direct
# regression coverage in tests/test_hosted_ci_policy.py; what changed is the
# evidence claim, not the enforcement.


def _run(command: tuple[str, ...], repository: Path) -> subprocess.CompletedProcess[str]:
    """Run one checker against an isolated repository copy."""

    # S603: every argv tuple is assembled above from fixed interpreter/module
    # names and a test-owned temporary path; no caller-controlled command exists.
    return subprocess.run(  # noqa: S603
        command,
        cwd=repository,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def test_installed_platform_check_matches_the_measured_release() -> None:
    """The matrix must execute the exact gate named by the evidence marker."""

    assert importlib.metadata.version("baltimore-patapsco") == MEASURED_PLATFORM_CHECK_VERSION


def test_unmodified_repository_copy_is_accepted_by_both_checkers(tmp_path: Path) -> None:
    """The differential starts from a green control, not an already-broken copy."""

    repository = _materialize_repository(tmp_path)

    local = _run((sys.executable, "scripts/check_hosted_ci_policy.py"), repository)
    shared = _run(
        (
            sys.executable,
            "-m",
            "baltimore.patapsco.baseline.cli",
            "--repo",
            str(repository),
        ),
        repository,
    )

    assert local.returncode == 0, f"stdout:\n{local.stdout}\nstderr:\n{local.stderr}"
    assert shared.returncode == 0, f"stdout:\n{shared.stdout}\nstderr:\n{shared.stderr}"


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.name)
def test_local_guard_blocks_each_case_platform_check_still_misses(
    case: DifferentialCase,
    tmp_path: Path,
) -> None:
    """Each stable injected violation proves the local guard remains load-bearing."""

    repository = _materialize_repository(tmp_path)
    case.inject(repository)

    local = _run((sys.executable, "scripts/check_hosted_ci_policy.py"), repository)
    shared = _run(
        (
            sys.executable,
            "-m",
            "baltimore.patapsco.baseline.cli",
            "--repo",
            str(repository),
        ),
        repository,
    )

    assert local.returncode == 1, (
        f"local guard failed to block {case.name}\nstdout:\n{local.stdout}\nstderr:\n{local.stderr}"
    )
    assert case.local_evidence in f"{local.stdout}\n{local.stderr}"
    assert shared.returncode == 0, (
        f"Patapsco now catches {case.name}; review the local guard's retirement "
        f"condition\nstdout:\n{shared.stdout}\nstderr:\n{shared.stderr}"
    )
