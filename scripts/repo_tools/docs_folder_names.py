"""Reject a `docs/` folder name that Git's ignore rules silently swallow.

WHY THIS EXISTS
===============
Folder names under `docs/` are public URLs — `docs/what-we-do/` is served as
`/what-we-do/`. They are also ordinary paths, so they are matched by the ignore
file like anything else, and the estate's managed ignore block in `.gitignore`
carries several **unanchored** directory patterns for Python packaging output.
`build/` and `dist/` are the live examples: written without a leading slash,
they match at *any* depth, so `docs/build/` is ignored exactly as `./build/` is.

That combination fails silently and in the worst possible direction. A page
authored at `docs/build/overview.md` is:

- invisible to Git — it never appears in `git status`, so it is never committed;
- invisible to this repository's own checks — source discovery in
  :mod:`scripts.repo_tools.authored_sources` reads Git's tracked and
  non-ignored-untracked sets, so an ignored path is not in the source set at
  all and every content ratchet passes over it;
- **visible to MkDocs**, which reads the filesystem. It renders in `task serve`
  and in a local `mkdocs build`.

So the author sees their page working locally, the gate reports green, and the
page is simply absent from production — or, if something links to it, the
hosted build fails later with a broken link whose cause is several steps
removed. Measured on 2026-08-11 against this repository: with a page present at
`docs/build/`, `git status` was empty, source discovery returned 0 of 195
authored sources for it, `task ci` passed, and `mkdocs build --strict`
published it.

WHY NOT JUST ANCHOR THE IGNORE PATTERNS
=======================================
Because they are not ours to anchor. `.gitignore`'s upper block is Patapsco's
managed baseline, carried verbatim and checked by that package's
``ignore_baseline`` rule; rewriting `build/` to `/build/` locally makes
`platform-check` report the block as drifted. Per `AGENTS.md`, a rule believed
wrong is changed in Patapsco rather than worked around here. This check is the
repository-local half: it cannot fix the pattern, but it can refuse to let a
colliding folder name be adopted quietly.

WHY A CHECK RATHER THAN A LINE OF GUIDANCE
==========================================
Guidance is read once, at the wrong time. The collision is invisible by
construction, so the only reliable moment to catch it is when the directory
first exists — which is what this does, in the fast tier, before the author has
written a section against a name that cannot survive.

Git owns the answer to "is this path ignored?", so this asks Git rather than
reimplementing ignore-matching. `git check-ignore` distinguishes its outcomes by
exit status: 0 when something matched, 1 when nothing did, and anything else is
a real error that fails closed rather than reading as "nothing ignored".
"""

from __future__ import annotations

import shutil

# B404: subprocess runs one fixed, read-only Git ignore-query command below.
import subprocess  # nosec B404
from pathlib import Path

#: Directory names that never carry published content, so an ignore match on
#: them is intended rather than a collision.
_NOT_PUBLISHED = frozenset({"__pycache__"})

_CHECK_IGNORE_MATCHED = 0
_CHECK_IGNORE_NO_MATCH = 1


def _candidate_directories(docs_dir: Path) -> tuple[Path, ...]:
    """Return every directory under ``docs_dir``, nearest the root first."""

    directories = [path for path in docs_dir.rglob("*") if path.is_dir()]
    kept = [path for path in directories if path.name not in _NOT_PUBLISHED]
    return tuple(sorted(kept, key=lambda path: (len(path.parts), path.as_posix())))


def _ignored_paths(repo_root: Path, candidates: tuple[Path, ...]) -> frozenset[Path]:
    """Return the candidates Git's ignore rules match, asking Git directly."""

    if not candidates:
        return frozenset()

    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git executable not found; ignore rules cannot be resolved")

    payload = "\n".join(path.as_posix() for path in candidates)
    try:
        # S603: git is resolved to an absolute executable and the rest of argv
        # is a fixed literal; every candidate path arrives on stdin, so no
        # folder name can be read as an option or a shell token.
        completed = subprocess.run(  # nosec B603  # noqa: S603
            (git, "check-ignore", "--stdin"),
            cwd=repo_root,
            input=payload,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise RuntimeError(f"cannot ask Git which docs/ paths are ignored: {error}") from error

    if completed.returncode not in (_CHECK_IGNORE_MATCHED, _CHECK_IGNORE_NO_MATCH):
        raise RuntimeError(
            "git check-ignore failed with exit status "
            f"{completed.returncode}: {completed.stderr.strip() or 'no stderr'}"
        )

    return frozenset(Path(line) for line in completed.stdout.splitlines() if line)


def find_docs_folder_name_issues(repo_root: Path, *, docs_dir: Path | None = None) -> list[str]:
    """Return one issue for every ``docs/`` directory Git's ignore rules hide.

    ``docs_dir`` stays injectable for tests but takes exactly one positional
    argument in ordinary use, matching every other validator this repository's
    thin CLIs call.
    """

    relative_docs_dir = docs_dir if docs_dir is not None else Path("docs")
    effective_docs_dir = (
        relative_docs_dir if relative_docs_dir.is_absolute() else repo_root / relative_docs_dir
    )
    if not effective_docs_dir.is_dir():
        return [f"{relative_docs_dir}: documentation directory not found"]
    if not (repo_root / ".git").exists():
        raise RuntimeError(f"Git metadata not found at {repo_root}; run from a Git worktree")

    candidates = _candidate_directories(effective_docs_dir)
    relative = {path: path.relative_to(repo_root) for path in candidates}
    ignored = _ignored_paths(repo_root, tuple(relative.values()))

    return [
        f"{relative[path].as_posix()}/: this folder name is matched by an ignore rule, so Git "
        "cannot see the pages inside it while MkDocs still publishes them. Rename the folder — "
        "the name is also its public URL, so pick the one readers should see."
        for path in candidates
        if relative[path] in ignored
    ]
