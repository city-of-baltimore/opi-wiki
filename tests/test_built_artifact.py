"""Tests for built-artifact safety."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts import check_built_artifact
from scripts.repo_tools.built_artifact import find_built_artifact_issues


def test_built_artifact_accepts_ordinary_output(tmp_path: Path) -> None:
    """Ordinary built HTML and assets should pass."""

    (tmp_path / "index.html").write_text(
        "<h1>OPI Foundations</h1><p>Methods and services.</p>",
        encoding="utf-8",
    )
    (tmp_path / "logo.svg").write_text("<svg></svg>", encoding="utf-8")

    assert find_built_artifact_issues(tmp_path) == []


def test_built_artifact_rejects_yaml_pin_and_phone_output(tmp_path: Path) -> None:
    """Source data and the removed UI fields must not return in a build."""

    (tmp_path / "_data").mkdir()
    (tmp_path / "_data" / "people.yml").write_text("people: []\n", encoding="utf-8")
    (tmp_path / "index.html").write_text(
        "<table><tr><th>PIN</th><td>410-555-0100</td></tr></table>",
        encoding="utf-8",
    )

    assert find_built_artifact_issues(tmp_path) == [
        "_data/people.yml: structured YAML source entered the built artifact",
        "index.html: contains a phone-number pattern",
        "index.html: contains a visible PIN label",
    ]


def test_built_artifact_rejects_excluded_handbook_output(tmp_path: Path) -> None:
    """Source-only handbook pages must not reappear in the generated site."""

    handbook_page = tmp_path / "how-we-work" / "handbook" / "index.html"
    handbook_page.parent.mkdir(parents=True)
    handbook_page.write_text("<h1>Handbook</h1>", encoding="utf-8")

    assert find_built_artifact_issues(tmp_path) == [
        "how-we-work/handbook/index.html: excluded source path entered the built artifact"
    ]


def test_built_artifact_requires_a_built_site(tmp_path: Path) -> None:
    """A missing build must fail rather than pass vacuously."""

    with pytest.raises(FileNotFoundError, match="Built site directory was not found"):
        find_built_artifact_issues(tmp_path / "missing")


def test_built_artifact_wraps_read_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unreadable output should name the affected file."""

    output_file = tmp_path / "index.html"
    output_file.write_text("<h1>OPI</h1>", encoding="utf-8")

    def fail_read(path: Path, *, encoding: str, errors: str) -> str:
        assert path == output_file
        assert encoding == "utf-8"
        assert errors == "replace"
        raise OSError("read failed")

    monkeypatch.setattr(Path, "read_text", fail_read)

    with pytest.raises(RuntimeError, match=r"Unable to read built output: .*index\.html"):
        find_built_artifact_issues(tmp_path)


def test_built_artifact_cli_reports_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The thin CLI should report a clean build."""

    (tmp_path / "index.html").write_text("<h1>OPI</h1>", encoding="utf-8")
    monkeypatch.setattr(check_built_artifact, "SITE_DIR", tmp_path)

    assert check_built_artifact.main() == 0
    assert capsys.readouterr().out == "Built-artifact safety check passed.\n"


def test_built_artifact_cli_reports_findings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The thin CLI should return failure for an artifact leak."""

    (tmp_path / "source.yml").write_text("source: true\n", encoding="utf-8")
    monkeypatch.setattr(check_built_artifact, "SITE_DIR", tmp_path)

    assert check_built_artifact.main() == 1
    assert "structured YAML source entered the built artifact" in capsys.readouterr().err
