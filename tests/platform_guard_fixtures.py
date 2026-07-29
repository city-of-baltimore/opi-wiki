"""Shared repository fixtures for platform-gate contract tests."""

from __future__ import annotations

from pathlib import Path

from scripts.repo_tools.platform_guard_evidence import (
    MEASURED_PLATFORM_CHECK_VERSION,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATHS = (
    Path(".baltimore-lab-app.toml"),
    Path("AGENTS.md"),
    Path("MAINTAINERS.md"),
    Path("README.md"),
    Path("Taskfile.yml"),
    Path("scripts/repo_tools/hosted_ci_policy.py"),
    Path("scripts/verify.py"),
    Path("tests/test_verify.py"),
)


def write_contract(
    root: Path,
    *,
    dependency: str = f"baltimore-patapsco=={MEASURED_PLATFORM_CHECK_VERSION}",
    dependabot: str | None = None,
) -> None:
    """Write the smallest repository contract accepted by the validator."""

    (root / "pyproject.toml").write_text(
        f'[dependency-groups]\ndev = ["{dependency}"]\n',
        encoding="utf-8",
    )
    dependabot_path = root / ".github" / "dependabot.yml"
    dependabot_path.parent.mkdir(parents=True)
    dependabot_path.write_text(
        dependabot
        or """version: 2
updates:
  - package-ecosystem: uv
    directory: "/"
    schedule:
      interval: weekly
    groups:
      platform-gate:
        patterns: ["baltimore-patapsco"]
      python:
        patterns: ["*"]
        exclude-patterns: ["baltimore-patapsco"]
""",
        encoding="utf-8",
    )
    for relative_path in EVIDENCE_PATHS:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
