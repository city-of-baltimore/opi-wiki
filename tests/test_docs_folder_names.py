"""Cover the docs folder-name ignore-collision check on both paths."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
from scripts.repo_tools.docs_folder_names import find_docs_folder_name_issues

from git_fixtures import init_git_repo


def _docs_repo(root: Path, *, ignore: str = "") -> Path:
    """Build a fixture worktree with a docs tree and an optional ignore file."""

    init_git_repo(root)
    docs = root / "docs"
    (docs / "what-we-do").mkdir(parents=True)
    (docs / "what-we-do" / "index.md").write_text("# What We Do\n", encoding="utf-8")
    if ignore:
        (root / ".gitignore").write_text(ignore, encoding="utf-8")
    return docs


def test_ordinary_docs_tree_reports_no_issue(tmp_path: Path) -> None:
    """A tree whose folder names no ignore rule matches passes cleanly."""

    root = tmp_path / "repo"
    _docs_repo(root, ignore="build/\ndist/\n/site/\n")

    assert find_docs_folder_name_issues(root, docs_dir=Path("docs")) == []


@pytest.mark.parametrize("folder", ["build", "dist"])
def test_unanchored_ignore_pattern_is_reported(tmp_path: Path, folder: str) -> None:
    """A docs folder matched by an unanchored pattern is a finding, not silence."""

    root = tmp_path / "repo"
    docs = _docs_repo(root, ignore="build/\ndist/\n")
    (docs / folder).mkdir()
    (docs / folder / "overview.md").write_text("# Overview\n", encoding="utf-8")

    issues = find_docs_folder_name_issues(root, docs_dir=Path("docs"))

    assert len(issues) == 1
    assert issues[0].startswith(f"docs/{folder}/:")
    assert "MkDocs still publishes them" in issues[0]


def test_nested_ignored_folder_is_reported(tmp_path: Path) -> None:
    """The collision is depth-independent, because the pattern is unanchored."""

    root = tmp_path / "repo"
    docs = _docs_repo(root, ignore="build/\n")
    nested = docs / "what-we-do" / "build"
    nested.mkdir()
    (nested / "page.md").write_text("# Page\n", encoding="utf-8")

    issues = find_docs_folder_name_issues(root, docs_dir=Path("docs"))

    assert [issue.split(":")[0] for issue in issues] == ["docs/what-we-do/build/"]


def test_force_added_folder_is_still_reported(tmp_path: Path) -> None:
    """A `git add -f` folder is the worse half-state, so the name still fails.

    Git skips indexed paths unless asked not to. Without ``--no-index`` this
    folder reports clean while the next page dropped into it still vanishes.
    """

    root = tmp_path / "repo"
    docs = _docs_repo(root, ignore="build/\n")
    (docs / "build").mkdir()
    forced = docs / "build" / "overview.md"
    forced.write_text("# Overview\n", encoding="utf-8")

    git = shutil.which("git")
    assert git is not None
    # S603: git is an absolute resolved path and argv is fixed apart from the
    # fixture path this test just created.
    subprocess.run(  # noqa: S603
        (git, "add", "-f", str(forced)),
        cwd=root,
        check=True,
        capture_output=True,
    )

    issues = find_docs_folder_name_issues(root, docs_dir=Path("docs"))

    assert [issue.split(":")[0] for issue in issues] == ["docs/build/"]


def test_pycache_is_not_treated_as_published_content(tmp_path: Path) -> None:
    """A directory that never carries pages is exempt rather than a finding."""

    root = tmp_path / "repo"
    docs = _docs_repo(root, ignore="__pycache__/\n")
    (docs / "__pycache__").mkdir()

    assert find_docs_folder_name_issues(root, docs_dir=Path("docs")) == []


def test_missing_docs_directory_is_reported(tmp_path: Path) -> None:
    """An absent documentation directory is an issue, not an empty pass."""

    root = tmp_path / "repo"
    init_git_repo(root)

    assert find_docs_folder_name_issues(root, docs_dir=Path("docs")) == [
        "docs: documentation directory not found"
    ]


def test_missing_git_metadata_fails_closed(tmp_path: Path) -> None:
    """Without a worktree the check raises rather than reporting a false pass."""

    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)

    with pytest.raises(RuntimeError, match="Git metadata not found"):
        find_docs_folder_name_issues(root, docs_dir=Path("docs"))
