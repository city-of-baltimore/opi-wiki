"""Tests for Patapsco update isolation in Dependabot configuration."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.platform_guard_evidence import (
    find_platform_guard_evidence_issues,
)
from tests.platform_guard_fixtures import write_contract as _write_contract


def test_platform_gate_must_have_its_own_dependabot_group(tmp_path: Path) -> None:
    """A broad tooling group must not batch a policy change."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      python:
        patterns: ["*"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("platform-gate.patterns" in issue for issue in issues)
    assert any("'python' also matches baltimore-patapsco" in issue for issue in issues)


def test_platform_gate_group_cannot_batch_an_unrelated_dependency(tmp_path: Path) -> None:
    """The dedicated group is only isolated when its allowlist is exact."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco", "ruff"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("must contain only 'baltimore-patapsco'" in issue for issue in issues)


@pytest.mark.parametrize(
    "extra_filter",
    (
        '        exclude-patterns: ["baltimore-patapsco"]\n',
        "        applies-to: security-updates\n",
        '        update-types: ["patch"]\n',
    ),
)
def test_platform_gate_group_cannot_filter_out_version_bumps(
    tmp_path: Path,
    extra_filter: str,
) -> None:
    """Every ordinary Patapsco bump must enter the dedicated review group."""

    _write_contract(
        tmp_path,
        dependabot=f"""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
{extra_filter}""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("must define only its exact patterns list" in issue for issue in issues)


def test_criteria_only_group_must_explicitly_exclude_patapsco(tmp_path: Path) -> None:
    """A group without name patterns can still capture any matching update type."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      routine-patches:
        update-types: ["minor", "patch"]
      platform-gate:
        patterns: ["baltimore-patapsco"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("'routine-patches' also matches baltimore-patapsco" in issue for issue in issues)


def test_cross_ecosystem_grouping_is_rejected_for_the_uv_gate(tmp_path: Path) -> None:
    """Patapsco must not share a cross-ecosystem pull request with Actions."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
multi-ecosystem-groups:
  routine:
    schedule:
      interval: weekly
updates:
  - package-ecosystem: uv
    directory: "/"
    multi-ecosystem-group: routine
    patterns: ["*"]
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
  - package-ecosystem: github-actions
    directory: "/"
    multi-ecosystem-group: routine
    patterns: ["*"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("must not define 'multi-ecosystem-group'" in issue for issue in issues)
    assert any("must not define 'patterns'" in issue for issue in issues)


@pytest.mark.parametrize(
    ("root_fields", "unsupported_key"),
    (
        ('    directories: ["/"]\n', "directories"),
        ('    directory: "/"\n    target-branch: gate-audit\n', "target-branch"),
    ),
)
def test_alternate_root_or_branch_shapes_are_not_treated_as_the_update_contract(
    tmp_path: Path,
    root_fields: str,
    unsupported_key: str,
) -> None:
    """The isolated gate applies to the default-branch root configuration only."""

    _write_contract(
        tmp_path,
        dependabot=f"""version: 2
updates:
  - package-ecosystem: uv
{root_fields}    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any(f"must not define '{unsupported_key}'" in issue for issue in issues)


def test_alternate_root_and_target_branch_forms_cannot_hide_a_decoy_group(
    tmp_path: Path,
) -> None:
    """Only one default-branch root uv block may own update grouping."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
updates:
  - package-ecosystem: uv
    directories: ["/"]
    groups:
      python:
        patterns: ["*"]
  - package-ecosystem: uv
    directory: "/"
    target-branch: gate-audit
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("expected exactly one uv update configuration, found 2" in issue for issue in issues)


def test_dependabot_matching_uses_only_its_documented_star_wildcard(tmp_path: Path) -> None:
    """Python glob-only metacharacters must not masquerade as an exclusion."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
      python:
        patterns: ["*"]
        exclude-patterns: ["baltimore-patapsco?"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("'python' also matches baltimore-patapsco" in issue for issue in issues)


def test_dependabot_name_patterns_match_without_case_sensitivity(tmp_path: Path) -> None:
    """Grouping parity must follow Dependabot's case-insensitive name matcher."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      routine:
        patterns: ["BALTIMORE-*"]
      platform-gate:
        patterns: ["baltimore-patapsco"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("'routine' also matches baltimore-patapsco" in issue for issue in issues)


def test_dependabot_exclusions_match_without_case_sensitivity(tmp_path: Path) -> None:
    """A mixed-case exclusion still isolates the normalized dependency name."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
      routine:
        patterns: ["*"]
        exclude-patterns: ["BALTIMORE-PATAPSCO"]
""",
    )

    assert find_platform_guard_evidence_issues(tmp_path) == []


@pytest.mark.parametrize(
    ("group_source", "expected"),
    (
        ("      python: invalid\n", "group 'python' must be a mapping"),
        ("      python:\n        patterns: '*'\n", "patterns must be a list of strings"),
        ("      python:\n        patterns: []\n", "patterns must not be empty"),
    ),
)
def test_malformed_broad_groups_fail_closed(
    tmp_path: Path,
    group_source: str,
    expected: str,
) -> None:
    """Malformed grouping cannot be treated as proof that Patapsco is isolated."""

    _write_contract(
        tmp_path,
        dependabot=f"""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
{group_source}""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any(expected in issue for issue in issues)


def test_duplicate_dependabot_keys_fail_closed(tmp_path: Path) -> None:
    """A duplicate group key cannot silently replace the isolation contract."""

    _write_contract(
        tmp_path,
        dependabot="""version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
      platform-gate:
        patterns: ["*"]
""",
    )

    issues = find_platform_guard_evidence_issues(tmp_path)

    assert any("Duplicate YAML key 'platform-gate'" in issue for issue in issues)
