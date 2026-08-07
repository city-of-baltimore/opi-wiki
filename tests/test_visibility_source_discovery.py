"""Tests for repository-source discovery in the retired-label ratchet."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from scripts.repo_tools import authored_sources
from scripts.repo_tools.visibility_labels import find_visibility_label_issues
from tests.git_fixtures import init_git_repo


def test_visibility_labels_reject_retired_labels_across_sources(tmp_path: Path) -> None:
    """Every authored repository surface must produce line-level findings."""

    init_git_repo(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (tmp_path / "README.md").write_text(
        "A public-facing reference, public docs site, and public MkDocs site.\n",
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
    director_letter = docs_dir / "about-us" / "letters-from-the-director" / "letter.md"
    director_letter.parent.mkdir(parents=True)
    director_letter.write_text(
        "# Letter\n\nA public letter.\n\n## Public Purpose\n",
        encoding="utf-8",
    )
    (docs_dir / "index.cards.yaml").write_text(
        '- body: "Read the public leadership chart with its public audience label."\n',
        encoding="utf-8",
    )
    (docs_dir / ".pages").write_text(
        'title: "Public Foundations site"\n',
        encoding="utf-8",
    )
    stylesheet = docs_dir / "assets" / "stylesheets" / "components.css"
    stylesheet.parent.mkdir(parents=True)
    stylesheet.write_text(".opi-pill { display: inline-flex; }\n", encoding="utf-8")
    override = tmp_path / "overrides" / "main.html"
    override.parent.mkdir()
    override.write_text('{{ badge("reference") }}\n', encoding="utf-8")
    nested_guidance = tmp_path / "guidance" / "decision.md"
    nested_guidance.parent.mkdir()
    nested_guidance.write_text("Use the approved version.\n", encoding="utf-8")
    nested_published = docs_dir / "site" / "index.md"
    nested_published.parent.mkdir()
    nested_published.write_text("Public MkDocs site.\n", encoding="utf-8")

    generated = tmp_path / "site" / "index.html"
    generated.parent.mkdir()
    generated.write_text('<span class="opi-pill">Generated</span>\n', encoding="utf-8")
    cache = tmp_path / ".pytest_cache" / "README.md"
    cache.parent.mkdir()
    cache.write_text("Public MkDocs site.\n", encoding="utf-8")
    dependency = tmp_path / ".venv" / "dependency.md"
    dependency.parent.mkdir()
    dependency.write_text("Public MkDocs site.\n", encoding="utf-8")

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
    assert any(
        "docs/about-us/letters-from-the-director/letter.md:3:" in issue
        and "A public letter" in issue
        for issue in issues
    )
    assert any(
        "docs/about-us/letters-from-the-director/letter.md:5:" in issue
        and "Public Purpose" in issue
        for issue in issues
    )
    assert any(
        "docs/index.cards.yaml:1:" in issue and "public leadership chart" in issue
        for issue in issues
    )
    assert any(
        "docs/index.cards.yaml:1:" in issue and "public audience" in issue for issue in issues
    )
    assert any("docs/.pages:1:" in issue and "Public Foundations site" in issue for issue in issues)
    assert any(
        "docs/assets/stylesheets/components.css:1:" in issue and "opi-pill" in issue
        for issue in issues
    )
    assert any("overrides/main.html:1:" in issue and "{{ badge(" in issue for issue in issues)
    assert any(
        "guidance/decision.md:1:" in issue and "approved version" in issue for issue in issues
    )
    assert any(
        "docs/site/index.md:1:" in issue and "Public MkDocs site" in issue for issue in issues
    )
    assert not any(issue.startswith("site/") for issue in issues)
    assert not any(issue.startswith(".pytest_cache/") for issue in issues)
    assert not any(issue.startswith(".venv/") for issue in issues)


def test_visibility_labels_respect_git_ignored_working_files(tmp_path: Path) -> None:
    """Local ignored notes must never become repository-source findings."""

    init_git_repo(tmp_path)
    (tmp_path / ".gitignore").write_text("/ignored/\n", encoding="utf-8")
    ignored = tmp_path / "ignored" / "decision.md"
    ignored.parent.mkdir()
    ignored.write_text("Public MkDocs site.\n", encoding="utf-8")
    guidance = tmp_path / "guidance" / "decision.md"
    guidance.parent.mkdir()
    guidance.write_text("Use the approved version.\n", encoding="utf-8")

    issues = find_visibility_label_issues(tmp_path, tmp_path / "docs")

    assert len(issues) == 1
    assert issues[0].startswith("guidance/decision.md:1:")
    assert not any(issue.startswith("ignored/") for issue in issues)


def test_visibility_labels_discover_noncanonical_markup_surfaces(tmp_path: Path) -> None:
    """Repository notes and overrides need lexical coverage alongside rendered pages."""

    init_git_repo(tmp_path)
    docs_dir = tmp_path / "docs"
    product_note = tmp_path / "product" / "notes.md"
    product_note.parent.mkdir(parents=True)
    product_note.write_text(
        "Use the internal [documentation](guide.md).\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        "Use the public **site**.\n",
        encoding="utf-8",
    )
    override = tmp_path / "overrides" / "main.html"
    override.parent.mkdir()
    override.write_text(
        "Use the approved <em>version</em>.\n",
        encoding="utf-8",
    )
    issue_template = tmp_path / ".github" / "ISSUE_TEMPLATE" / "help.yml"
    issue_template.parent.mkdir(parents=True)
    issue_template.write_text(
        'description: "Use the public **site**."\n',
        encoding="utf-8",
    )

    issues = find_visibility_label_issues(tmp_path, docs_dir)

    assert len(issues) == 4
    assert any(issue.startswith("README.md:1:") and "public site" in issue for issue in issues)
    assert any(
        issue.startswith("product/notes.md:1:") and "internal documentation" in issue
        for issue in issues
    )
    assert any(
        issue.startswith("overrides/main.html:1:") and "approved version" in issue
        for issue in issues
    )
    assert any(
        issue.startswith(".github/ISSUE_TEMPLATE/help.yml:1:") and "public site" in issue
        for issue in issues
    )


def test_visibility_labels_include_tracked_files_after_they_become_ignored(
    tmp_path: Path,
) -> None:
    """The Git source contract must include cached files and exclude generated paths."""

    git = init_git_repo(tmp_path)
    tracked = tmp_path / "guidance" / "decision.md"
    tracked.parent.mkdir()
    tracked.write_text("Use the approved version.\n", encoding="utf-8")
    tracked_note = tmp_path / "notes" / "decision.md"
    tracked_note.parent.mkdir()
    tracked_note.write_text("Keep the internal copies here.\n", encoding="utf-8")
    generated = tmp_path / "site" / "index.html"
    generated.parent.mkdir()
    generated.write_text('<span class="opi-pill">Generated</span>\n', encoding="utf-8")
    (tmp_path / ".gitignore").write_text(
        "/guidance/\n/notes/\n/site/\n",
        encoding="utf-8",
    )
    # S603: git is an absolute executable and argv stages three explicit fixture paths.
    subprocess.run(  # noqa: S603
        (
            git,
            "-C",
            str(tmp_path),
            "add",
            "-f",
            "guidance/decision.md",
            "notes/decision.md",
            "site/index.html",
        ),
        check=True,
        capture_output=True,
        text=True,
    )

    issues = find_visibility_label_issues(tmp_path, tmp_path / "docs")

    assert len(issues) == 2
    assert any(issue.startswith("guidance/decision.md:1:") for issue in issues)
    assert any(issue.startswith("notes/decision.md:1:") for issue in issues)
    assert not any(issue.startswith("site/") for issue in issues)


@pytest.mark.parametrize("target_exists", (True, False))
def test_visibility_labels_fail_closed_for_tracked_source_symlinks(
    tmp_path: Path,
    target_exists: bool,
) -> None:
    """Regular and dangling authored symlinks must fail without following targets."""

    git = init_git_repo(tmp_path)
    target = tmp_path / "source.txt"
    if target_exists:
        target.write_text("Public MkDocs site.\n", encoding="utf-8")
    link = tmp_path / "docs" / "published.md"
    link.parent.mkdir()
    link.symlink_to("../source.txt")
    # S603: git is an absolute executable and argv stages one explicit fixture path.
    subprocess.run(  # noqa: S603
        (git, "-C", str(tmp_path), "add", "docs/published.md"),
        check=True,
        capture_output=True,
        text=True,
    )

    assert find_visibility_label_issues(tmp_path, tmp_path / "docs") == [
        "repository: unable to discover authored sources: repository source is a symbolic link: "
        "docs/published.md; replace it with a regular repository file"
    ]


@pytest.mark.parametrize(
    ("relative_link", "relative_target"),
    (
        (Path("docs/linked"), "../notes/linked-content"),
        (Path("overrides"), "notes/linked-content"),
    ),
)
def test_visibility_labels_fail_closed_for_tracked_source_directory_symlinks(
    tmp_path: Path,
    relative_link: Path,
    relative_target: str,
) -> None:
    """A deployed source-directory symlink must fail before its target is read."""

    git = init_git_repo(tmp_path)
    target = tmp_path / "notes" / "linked-content"
    target.mkdir(parents=True)
    (target / "page.md").write_text("Public MkDocs site.\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("/notes/\n", encoding="utf-8")
    link = tmp_path / relative_link
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(relative_target, target_is_directory=True)
    # S603: git is an absolute executable and argv stages one explicit fixture path.
    subprocess.run(  # noqa: S603
        (git, "-C", str(tmp_path), "add", str(relative_link)),
        check=True,
        capture_output=True,
        text=True,
    )

    assert find_visibility_label_issues(tmp_path, tmp_path / "docs") == [
        "repository: unable to discover authored sources: repository source is a symbolic link: "
        f"{relative_link}; replace it with a regular repository file"
    ]


def test_visibility_labels_can_exclude_docs_without_missing_other_sources(
    tmp_path: Path,
) -> None:
    """The consistency scan's non-docs pass must still cover templates."""

    init_git_repo(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "page.md").write_text("Public MkDocs site.\n", encoding="utf-8")
    override = tmp_path / "overrides" / "main.html"
    override.parent.mkdir()
    override.write_text('<span class="opi-pill">Reference</span>\n', encoding="utf-8")

    issues = find_visibility_label_issues(
        tmp_path,
        docs_dir,
        include_docs=False,
    )

    assert len(issues) == 1
    assert issues[0].startswith("overrides/main.html:1:")


def test_visibility_labels_report_read_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unreadable covered sources must fail with the affected path."""

    init_git_repo(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    source = docs_dir / ".pages"
    source.write_text("# Page\n", encoding="utf-8")
    original_read_text = Path.read_text

    def fail_source(path: Path, *, encoding: str) -> str:
        if path == source:
            raise OSError("read failed")
        return original_read_text(path, encoding=encoding)

    monkeypatch.setattr(Path, "read_text", fail_source)

    assert find_visibility_label_issues(tmp_path, docs_dir) == [
        "docs/.pages: unable to read source for visibility-label validation: read failed"
    ]


def test_visibility_labels_report_git_discovery_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Git failures must close the gate with actionable evidence."""

    (tmp_path / ".git").mkdir()

    def fail_git(*_args: object, **_kwargs: object) -> None:
        raise OSError("git unavailable")

    monkeypatch.setattr(authored_sources.shutil, "which", lambda _name: "/usr/bin/git")
    monkeypatch.setattr(authored_sources.subprocess, "run", fail_git)

    assert find_visibility_label_issues(tmp_path, tmp_path / "docs") == [
        "repository: unable to discover authored sources: "
        "Git source discovery could not run: git unavailable"
    ]


def test_visibility_labels_fail_closed_without_git_metadata(tmp_path: Path) -> None:
    """A source tree without Git metadata must not substitute different semantics."""

    issues = find_visibility_label_issues(tmp_path, tmp_path / "docs")

    assert len(issues) == 1
    assert issues[0].startswith(
        "repository: unable to discover authored sources: Git metadata not found at "
    )
    assert issues[0].endswith("; run validation from a Git worktree")
