"""Tests for the retired visibility-label ratchet."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.visibility_labels import (
    check_visibility_labels,
    find_visibility_label_issues,
)


def test_visibility_label_check_accepts_domain_language(tmp_path: Path) -> None:
    """The one-source checker should accept a governed-data sentence."""

    path = tmp_path / "docs" / "page.md"

    assert (
        check_visibility_labels(
            path,
            "Approved users work from approved data for public safety.",
            repo_root=tmp_path,
        )
        == []
    )


def test_visibility_label_check_rejects_a_retired_phrase(tmp_path: Path) -> None:
    """The one-source checker should return exact line evidence."""

    path = tmp_path / "README.md"

    assert check_visibility_labels(
        path,
        "# Site\n\nA public-facing reference.\n",
        repo_root=tmp_path,
    ) == [
        "README.md:3: retired visibility label 'public-facing'; "
        "name the reader, review, or concrete data rule instead"
    ]


@pytest.mark.parametrize(
    "label",
    (
        "Public MkDocs site",
        "public effect",
        "public roster",
        "public operating model",
        "public template pages",
        "public summaries",
        "internal copy",
        "approved version",
    ),
)
def test_visibility_label_check_rejects_each_removed_family_once(
    tmp_path: Path,
    label: str,
) -> None:
    """Corpus-derived retired labels should produce one actionable diagnostic."""

    issues = check_visibility_labels(
        tmp_path / "README.md",
        f"{label}.\n",
        repo_root=tmp_path,
    )

    assert len(issues) == 1
    assert f"retired visibility label '{label}'" in issues[0]


def test_visibility_labels_accept_required_domain_language(tmp_path: Path) -> None:
    """Civic, legal, operational, and compatibility meanings must remain valid."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "page.md").write_text(
        "# Data governance\n\n"
        "The Public Innovation Toolkit supports public safety, public service, and "
        "public trust. Internal Stat and Internal Services are formal operating terms. "
        "Built-site internal links stay local. Public data may be used by approved "
        "users from approved sources. The tier is Public | Approved for publication. "
        "A Justfile may contain [private].\n",
        encoding="utf-8",
    )
    (tmp_path / "mkdocs.yml").write_text(
        "redirect_maps:\n  public/legacy-public-brief.md: index.md\n",
        encoding="utf-8",
    )

    assert find_visibility_label_issues(tmp_path, docs_dir) == []


def test_visibility_labels_reject_retired_labels_across_sources(tmp_path: Path) -> None:
    """Root guidance, Markdown, and YAML must all produce line-level findings."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (tmp_path / "README.md").write_text(
        "A public-facing public docs site and public MkDocs site.\n",
        encoding="utf-8",
    )
    (tmp_path / "LICENSE-CONTENT.md").write_text(
        "The public operating model.\n",
        encoding="utf-8",
    )
    issue_template = tmp_path / ".github" / "ISSUE_TEMPLATE" / "content.yml"
    issue_template.parent.mkdir(parents=True)
    issue_template.write_text(
        'description: "Update the public template pages."\n',
        encoding="utf-8",
    )
    (docs_dir / "letter.md").write_text(
        "# Letter\n\nA public letter.\n\n## Public Purpose\n",
        encoding="utf-8",
    )
    (docs_dir / "index.cards.yaml").write_text(
        '- body: "Read the public leadership chart with its public audience label."\n',
        encoding="utf-8",
    )

    issues = find_visibility_label_issues(tmp_path, docs_dir)

    assert any("README.md:1:" in issue and "public-facing" in issue for issue in issues)
    assert any("README.md:1:" in issue and "public docs site" in issue for issue in issues)
    assert any("README.md:1:" in issue and "public MkDocs site" in issue for issue in issues)
    assert any(
        "LICENSE-CONTENT.md:1:" in issue and "public operating model" in issue for issue in issues
    )
    assert any(
        ".github/ISSUE_TEMPLATE/content.yml:1:" in issue and "public template pages" in issue
        for issue in issues
    )
    assert any("docs/letter.md:3:" in issue and "A public letter" in issue for issue in issues)
    assert any("docs/letter.md:5:" in issue and "Public Purpose" in issue for issue in issues)
    assert any(
        "docs/index.cards.yaml:1:" in issue and "public leadership chart" in issue
        for issue in issues
    )
    assert any(
        "docs/index.cards.yaml:1:" in issue and "public audience" in issue for issue in issues
    )


def test_visibility_labels_report_read_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unreadable covered sources must fail with the affected path."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    source = docs_dir / "page.md"
    source.write_text("# Page\n", encoding="utf-8")
    original_read_text = Path.read_text

    def fail_source(path: Path, *, encoding: str) -> str:
        if path == source:
            raise OSError("read failed")
        return original_read_text(path, encoding=encoding)

    monkeypatch.setattr(Path, "read_text", fail_source)

    assert find_visibility_label_issues(tmp_path, docs_dir) == [
        "docs/page.md: unable to read source for visibility-label validation: read failed"
    ]
