"""Integration tests for the repository consistency scan."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools import consistency_scan
from scripts.repo_tools.consistency import SERVICE_REQUIRED
from scripts.repo_tools.consistency_scan import ConsistencyScan, scan_consistency
from tests.git_fixtures import init_git_repo


def test_consistency_scan_reports_each_retired_presentation_path_once(
    tmp_path: Path,
) -> None:
    """The unified source ratchet should own both former rendering paths."""

    init_git_repo(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "page.md").write_text(
        '# Page\n\n{{ badge("reference") }}\n\n<span class="opi-pill neutral">Reference</span>\n',
        encoding="utf-8",
    )
    (docs_dir / ".pages").write_text(
        'title: "Public Foundations site"\n',
        encoding="utf-8",
    )
    stylesheet = docs_dir / "assets" / "stylesheets" / "components.css"
    stylesheet.parent.mkdir(parents=True)
    stylesheet.write_text(".opi-pill { display: inline-flex; }\n", encoding="utf-8")

    issues = scan_consistency(docs_dir, repo_root=tmp_path).structural_issues

    assert len(issues) == 4
    assert any(issue.startswith("docs/page.md:3:") and "{{ badge(" in issue for issue in issues)
    assert any(issue.startswith("docs/page.md:5:") and "opi-pill" in issue for issue in issues)
    assert any(issue.startswith("docs/.pages:1:") for issue in issues)
    assert any(
        issue.startswith("docs/assets/stylesheets/components.css:1:") and "opi-pill" in issue
        for issue in issues
    )


def test_scan_consistency_collects_a_clean_page(tmp_path: Path) -> None:
    """The repository scan should return an empty result for clean Markdown."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    docs_dir = repo_root / "docs"
    page = docs_dir / "guide" / "page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Page\n\nPlain site copy.\n", encoding="utf-8")

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result == ConsistencyScan(structural_issues=(), acronyms=())


def test_scan_consistency_fails_closed_when_source_discovery_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A source-listing failure must become a structural gate finding."""

    repo_root = tmp_path / "repo"
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(parents=True)

    def fail_discovery(
        _repo_root: Path,
        _docs_dir: Path,
        *,
        include_docs: bool,
    ) -> tuple[Path, ...]:
        del include_docs
        raise RuntimeError("fixture discovery failure")

    monkeypatch.setattr(consistency_scan, "authored_source_paths", fail_discovery)

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result == ConsistencyScan(
        structural_issues=(
            "repository: unable to discover authored sources: fixture discovery failure",
        ),
        acronyms=(),
    )


def test_scan_consistency_integrates_visibility_ratchet_across_sources(tmp_path: Path) -> None:
    """Root guidance, Markdown, and either YAML suffix must share the CI ratchet."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(parents=True)
    (repo_root / "README.md").write_text("Public-facing guide.\n", encoding="utf-8")
    (docs_dir / "page.md").write_text("# Page\n\nInternal copy.\n", encoding="utf-8")
    (docs_dir / "page.yaml").write_text(
        'summary: "Approved audience label."\n',
        encoding="utf-8",
    )

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert len(result.structural_issues) == 3
    assert any(
        "README.md:1:" in issue and "Public-facing" in issue for issue in result.structural_issues
    )
    assert any(
        "docs/page.md:3:" in issue and "Internal copy" in issue
        for issue in result.structural_issues
    )
    assert any(
        "docs/page.yaml:1:" in issue and "Approved audience" in issue
        for issue in result.structural_issues
    )


def test_scan_consistency_respects_git_ignored_docs(tmp_path: Path) -> None:
    """The gated scan must not bypass Git-aware source discovery under docs."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    (repo_root / ".gitignore").write_text("/docs/ignored/\n", encoding="utf-8")
    docs_dir = repo_root / "docs"
    ignored = docs_dir / "ignored" / "note.md"
    ignored.parent.mkdir(parents=True)
    ignored.write_text("Public MkDocs site.\n", encoding="utf-8")
    (docs_dir / "page.md").write_text("# Page\n\nPlain site copy.\n", encoding="utf-8")

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result == ConsistencyScan(structural_issues=(), acronyms=())


def test_scan_consistency_collects_citistat_card_narrative_drift(tmp_path: Path) -> None:
    """The integrated scan must inspect the card source that held the original drift."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    docs_dir = repo_root / "docs"
    cards = docs_dir / "what-we-do" / "programs" / "citistat" / "index.cards.yml"
    cards.parent.mkdir(parents=True)
    cards.write_text('body: "The full agency portfolio: 19 agency briefs."\n', encoding="utf-8")

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert len(result.structural_issues) == 2
    assert all("index.cards.yml:1" in issue for issue in result.structural_issues)
    assert any("agency and thematic Stats" in issue for issue in result.structural_issues)


def test_scan_consistency_collects_an_unreadable_citistat_card_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A card-source IO failure should retain its path and cause."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    docs_dir = repo_root / "docs"
    cards = docs_dir / "what-we-do" / "programs" / "citistat" / "index.cards.yml"
    cards.parent.mkdir(parents=True)
    cards.touch()
    original_read_text = Path.read_text

    def fail_cards(path: Path, *, encoding: str) -> str:
        if path == cards:
            raise OSError("card read failed")
        return original_read_text(path, encoding=encoding)

    monkeypatch.setattr(Path, "read_text", fail_cards)

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result.structural_issues == (
        "docs/what-we-do/programs/citistat/index.cards.yml: "
        "unable to read card source: card read failed",
    )


def test_scan_consistency_collects_an_unreadable_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page read failure should be collected instead of raising a traceback."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    docs_dir = repo_root / "docs"
    page = docs_dir / "guide" / "page.md"
    page.parent.mkdir(parents=True)
    page.touch()
    original_read_text = Path.read_text

    def fail_page(path: Path, *, encoding: str) -> str:
        if path == page:
            raise OSError("read failed")
        return original_read_text(path, encoding=encoding)

    monkeypatch.setattr(Path, "read_text", fail_page)

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result.acronyms == ()
    assert result.structural_issues == (
        "docs/guide/page.md: unable to read Markdown source: read failed",
    )


def test_scan_consistency_collects_invalid_utf8_sources(tmp_path: Path) -> None:
    """Decode failures in primary source types must retain actionable paths."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(parents=True)
    (docs_dir / "bad.md").write_bytes(b"\xff")
    (docs_dir / "bad.yml").write_bytes(b"\xff")

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert len(result.structural_issues) == 2
    assert any(
        issue.startswith("docs/bad.md: unable to read Markdown source:")
        for issue in result.structural_issues
    )
    assert any(
        issue.startswith("docs/bad.yml: unable to read YAML source:")
        for issue in result.structural_issues
    )


@pytest.mark.parametrize(
    ("glossary_bytes", "page_text", "expected_acronyms"),
    (
        (
            b"# Glossary\n\nIGNR is a fixture term.\n",
            "# Page\n\nIGNR appears here.\n",
            (("docs/page.md", "IGNR"),),
        ),
        (
            b"\xff",
            "# Page\n\nPlain site copy.\n",
            (),
        ),
    ),
    ids=("does-not-contribute-terms", "does-not-decode"),
)
def test_scan_consistency_does_not_read_an_ignored_glossary(
    tmp_path: Path,
    glossary_bytes: bytes,
    page_text: str,
    expected_acronyms: tuple[tuple[str, str], ...],
) -> None:
    """Ignored untracked content must neither alter nor break the authored scan."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    (repo_root / ".gitignore").write_text(
        "/docs/resources/reference/glossary.md\n",
        encoding="utf-8",
    )
    docs_dir = repo_root / "docs"
    glossary = docs_dir / "resources" / "reference" / "glossary.md"
    glossary.parent.mkdir(parents=True)
    glossary.write_bytes(glossary_bytes)
    (docs_dir / "page.md").write_text(page_text, encoding="utf-8")

    result = scan_consistency(docs_dir, repo_root=repo_root)

    assert result.structural_issues == ()
    assert result.acronyms == expected_acronyms


def test_scan_consistency_collects_an_unreadable_eligible_glossary(
    tmp_path: Path,
) -> None:
    """A source-of-truth glossary decode failure must not escape the scanner."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    glossary = repo_root / "docs" / "resources" / "reference" / "glossary.md"
    glossary.parent.mkdir(parents=True)
    glossary.write_bytes(b"\xff")
    (repo_root / "docs" / "page.md").write_text(
        "# Page\n\nQZXQ remains informational.\n",
        encoding="utf-8",
    )

    result = scan_consistency(repo_root / "docs", repo_root=repo_root)

    assert result.acronyms == (("docs/page.md", "QZXQ"),)
    assert len(result.structural_issues) == 1
    assert result.structural_issues[0].startswith(
        "docs/resources/reference/glossary.md: unable to read acronym glossary:"
    )


def test_scan_consistency_resolves_a_relative_docs_root_for_the_glossary(
    tmp_path: Path,
) -> None:
    """Relative callers must read the same eligible glossary as absolute callers."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    glossary = repo_root / "docs" / "resources" / "reference" / "glossary.md"
    glossary.parent.mkdir(parents=True)
    glossary.write_text("# Glossary\n\nQZXQ is a fixture term.\n", encoding="utf-8")
    (repo_root / "docs" / "page.md").write_text(
        "# Page\n\nQZXQ appears here.\n",
        encoding="utf-8",
    )

    result = scan_consistency(Path("docs"), repo_root=repo_root)

    assert result == ConsistencyScan(structural_issues=(), acronyms=())


def test_scan_consistency_resolves_a_relative_service_root(tmp_path: Path) -> None:
    """Relative callers must retain canonical service-section validation."""

    repo_root = tmp_path / "repo"
    init_git_repo(repo_root)
    service = repo_root / "docs" / "what-we-do" / "services" / "example.md"
    service.parent.mkdir(parents=True)
    service.write_text("# Example\n\nDescription.\n", encoding="utf-8")

    result = scan_consistency(Path("docs"), repo_root=repo_root)

    assert len(result.structural_issues) == len(SERVICE_REQUIRED)
    assert all(
        "service page missing required section" in issue for issue in result.structural_issues
    )
