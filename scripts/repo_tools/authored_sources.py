"""Discover reviewable authored sources without following symbolic links."""

from __future__ import annotations

import shutil

# B404: subprocess runs one fixed, read-only Git source-listing command below.
import subprocess  # nosec B404
from pathlib import Path

AUTHORED_SOURCE_NAMES = frozenset({".gitignore", ".pages", "CODEOWNERS"})
AUTHORED_SOURCE_SUFFIXES = frozenset({".css", ".html", ".md", ".yaml", ".yml"})
EXCLUDED_SOURCE_ROOTS = frozenset(
    {
        ".cache",
        ".git",
        ".hypothesis",
        ".mypy_cache",
        ".nox",
        ".pixi",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "htmlcov",
        "node_modules",
        "site",
    }
)


def _is_excluded_source_path(path: Path, repo_root: Path) -> bool:
    """Return whether a candidate belongs to a generated or working directory."""

    try:
        relative_path = path.relative_to(repo_root)
    except ValueError:
        return True
    return len(relative_path.parts) > 1 and relative_path.parts[0] in EXCLUDED_SOURCE_ROOTS


def _is_authored_source_path(path: Path) -> bool:
    """Return whether a candidate has a source type covered by the ratchet."""

    return path.name in AUTHORED_SOURCE_NAMES or path.suffix.casefold() in AUTHORED_SOURCE_SUFFIXES


def _git_candidate_paths(repo_root: Path) -> tuple[Path, ...]:
    """Return tracked and non-ignored untracked paths from Git."""

    git = shutil.which("git")
    if git is None:
        raise RuntimeError("Git source discovery could not run: git executable not found")
    command = (
        git,
        "-C",
        str(repo_root),
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
    )
    try:
        # S603: argv is a fixed Git read-only query; repo_root remains one data argument.
        completed = subprocess.run(  # nosec B603  # noqa: S603
            command,
            check=False,
            capture_output=True,
            encoding="utf-8",
            errors="surrogateescape",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise RuntimeError(f"Git source discovery could not run: {error}") from error
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"exit code {completed.returncode}"
        raise RuntimeError(f"Git source discovery failed: {detail}")
    return tuple(
        repo_root / relative_path for relative_path in completed.stdout.split("\0") if relative_path
    )


def authored_source_paths(
    repo_root: Path,
    docs_dir: Path,
    *,
    include_docs: bool,
) -> tuple[Path, ...]:
    """Return deterministic regular authored sources covered by the ratchet."""

    effective_docs_dir = docs_dir if docs_dir.is_absolute() else repo_root / docs_dir
    if not (repo_root / ".git").exists():
        raise RuntimeError(
            f"Git metadata not found at {repo_root}; run validation from a Git worktree"
        )
    candidates = _git_candidate_paths(repo_root)
    sources: list[Path] = []
    for path in candidates:
        if _is_excluded_source_path(path, repo_root):
            continue
        is_docs_path = path.is_relative_to(effective_docs_dir)
        if not include_docs and is_docs_path:
            continue
        if path.is_symlink():
            relative_path = path.relative_to(repo_root)
            raise RuntimeError(
                f"repository source is a symbolic link: {relative_path}; "
                "replace it with a regular repository file"
            )
        is_authored_source = _is_authored_source_path(path)
        if not is_authored_source:
            continue
        if not path.exists():
            continue
        sources.append(path)
    return tuple(sorted(sources))
