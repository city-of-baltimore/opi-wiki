"""Tests for the Patapsco pin and living-evidence contract."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.platform_guard_evidence import (
    MEASURED_PLATFORM_CHECK_VERSION,
    find_platform_guard_evidence_issues,
)
from tests.platform_guard_fixtures import (
    REPOSITORY_ROOT,
)
from tests.platform_guard_fixtures import (
    write_contract as _write_contract,
)


def test_current_repository_platform_guard_evidence_is_coherent() -> None:
    """The checked-in pin, update policy, and living evidence should agree."""

    assert find_platform_guard_evidence_issues(REPOSITORY_ROOT) == []


def test_pin_bump_fails_until_differential_evidence_moves_with_it(tmp_path: Path) -> None:
    """A policy-gate bump cannot pass as an unattended manifest-only change."""

    _write_contract(tmp_path, dependency="baltimore-patapsco==9.9.9")

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("pinned at 9.9.9" in issue for issue in issues)
    assert any("test_platform_guard_differential.py" in issue for issue in issues)


def test_non_exact_patapsco_requirement_is_rejected(tmp_path: Path) -> None:
    """Ranges would make the measured checker version nondeterministic."""

    _write_contract(tmp_path, dependency="baltimore-patapsco>=0.4.5")

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("must use one exact" in issue for issue in issues)


def test_adjacent_package_name_does_not_count_as_a_second_patapsco_pin(
    tmp_path: Path,
) -> None:
    """A similarly prefixed package is not the platform-gate distribution."""

    _write_contract(tmp_path)
    (tmp_path / "pyproject.toml").write_text(
        f"""[dependency-groups]
dev = [
  "baltimore-patapsco=={MEASURED_PLATFORM_CHECK_VERSION}",
  "baltimore-patapsco-tools==1.0.0",
]
""",
        encoding="utf-8",
    )

    assert find_platform_guard_evidence_issues(tmp_path) == []


def test_each_current_measurement_reference_moves_with_the_marker(tmp_path: Path) -> None:
    """Living guidance cannot keep naming an earlier measured release."""

    _write_contract(tmp_path)
    stale_path = tmp_path / "README.md"
    stale_path.write_text(
        stale_path.read_text(encoding="utf-8").replace(
            f"re-measured against `platform-check` {MEASURED_PLATFORM_CHECK_VERSION}",
            "re-measured against `platform-check` 0.4.3\n\n"
            f"Historical comparison: {MEASURED_PLATFORM_CHECK_VERSION}",
        ),
        encoding="utf-8",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("README.md: current platform-check evidence" in issue for issue in issues)


def test_malformed_manifest_and_missing_evidence_are_reported(tmp_path: Path) -> None:
    """Unreadable contract state should produce actionable findings, not a traceback."""

    _write_contract(tmp_path)
    (tmp_path / "pyproject.toml").write_text("[dependency-groups\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").unlink()

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("pyproject.toml: invalid TOML" in issue for issue in issues)
    assert any("AGENTS.md: cannot read platform-gate contract" in issue for issue in issues)
