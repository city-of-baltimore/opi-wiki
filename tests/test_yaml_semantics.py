"""Tests for decoded YAML scalar projection and failure containment."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.visibility_labels import check_visibility_labels
from scripts.repo_tools.yaml_semantics import YamlSemanticError, yaml_scalar_projections


@pytest.mark.parametrize(
    ("source", "expected_value", "expected_line"),
    (
        ("summary: >\n  public\n  site\n", "public site\n", 2),
        ('summary: "approved\n  version"\n', "approved version", 1),
        ('summary: "public\\x20site"\n', "public site", 1),
        ('summary: "\\x70ublic site"\n', "public site", 1),
        ("summary: 'approved\n  version'\n", "approved version", 1),
    ),
)
def test_yaml_scalar_projections_decode_with_exact_source_evidence(
    source: str,
    expected_value: str,
    expected_line: int,
) -> None:
    """Decoded values and their first semantic character must map to source."""

    projection = yaml_scalar_projections(source)[1]
    raw_start = projection.raw_offsets[0]

    assert projection.text == expected_value
    assert source.count("\n", 0, raw_start) + 1 == expected_line


def test_yaml_scalar_projections_terminate_for_recursive_aliases() -> None:
    """Valid recursive aliases must not recurse through the composed node graph."""

    projections = yaml_scalar_projections("loop: &loop [*loop]\n")

    assert tuple(projection.text for projection in projections) == ("loop",)


@pytest.mark.parametrize(
    "source",
    (
        "summary: [\n",
        "summary: *missing\n",
    ),
)
def test_yaml_scalar_projections_fail_closed_for_invalid_yaml(source: str) -> None:
    """Malformed structure and undefined aliases must carry line-level evidence."""

    with pytest.raises(YamlSemanticError) as caught:
        yaml_scalar_projections(source)

    assert caught.value.line_number >= 1
    assert caught.value.detail.startswith("invalid YAML:")


@pytest.mark.parametrize(
    ("text", "expected_line"),
    (
        ("summary: >\n  public\n  site\n", 2),
        ('summary: "harmless\n  approved version"\n', 2),
        ('summary: "\\x70ublic site"\n', 1),
    ),
)
def test_yaml_policy_matches_report_the_exact_authored_line_once(
    tmp_path: Path,
    text: str,
    expected_line: int,
) -> None:
    """Decoded matches should retain exact evidence without raw/semantic duplicates."""

    issues = check_visibility_labels(
        tmp_path / "config.yml",
        text,
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert issues[0].startswith(f"config.yml:{expected_line}:")


def test_yaml_policy_preserves_folded_paragraph_boundaries(tmp_path: Path) -> None:
    """A blank line in a folded scalar remains a hard semantic boundary."""

    assert (
        check_visibility_labels(
            tmp_path / "config.yml",
            "summary: >\n  public\n\n  site\n",
            repo_root=tmp_path,
        )
        == []
    )


def test_yaml_policy_reports_an_actionable_parse_failure(tmp_path: Path) -> None:
    """Invalid YAML must fail the source gate at the parser's exact line."""

    issues = check_visibility_labels(
        tmp_path / "config.yml",
        "summary: >\n  public\n  site\n[\n",
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert issues[0].startswith(
        "config.yml:5: unable to validate semantic YAML text: invalid YAML:"
    )


def test_yaml_policy_terminates_cleanly_for_recursive_aliases(tmp_path: Path) -> None:
    """A recursive alias must be finite at both projection and policy seams."""

    assert (
        check_visibility_labels(
            tmp_path / "config.yml",
            "loop: &loop [*loop]\n",
            repo_root=tmp_path,
        )
        == []
    )
