"""Shared Git worktree fixtures for repository-source tests."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


def init_git_repo(repo_root: Path) -> str:
    """Initialize a quiet fixture worktree and return the resolved Git executable."""

    git = shutil.which("git")
    if git is None:
        pytest.skip("Git is required to exercise repository-source discovery.")
    repo_root.mkdir(parents=True, exist_ok=True)
    # S603: git is resolved to an absolute executable and argv is a fixed local init.
    subprocess.run(  # noqa: S603
        (git, "init", "--quiet", str(repo_root)),
        check=True,
        capture_output=True,
        text=True,
    )
    return git
