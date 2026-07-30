"""Hold the evidence boundary around the exact-pinned Patapsco policy gate.

Patapsco's ``platform-check`` and this repository's hosted-CI guard cover
different failures. A Patapsco bump therefore needs its own review, a rerun of
the differential matrix, and a coordinated update to every current-measurement
claim. This module makes those obligations fail closed instead of relying on a
reviewer remembering them.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from scripts.repo_tools.data import load_yaml_file

MEASURED_PLATFORM_CHECK_VERSION = "0.4.8"

_DEPENDENCY_NAME = "baltimore-patapsco"
_REQUIREMENT_NAME = re.compile(r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)")
_EXACT_PIN = re.compile(r"^baltimore-patapsco==(?P<version>[A-Za-z0-9][A-Za-z0-9.!+_-]*)$")
_CURRENT_EVIDENCE_CLAIMS = (
    (
        Path(".baltimore-lab-app.toml"),
        f"({MEASURED_PLATFORM_CHECK_VERSION}) for the shared estate baseline",
    ),
    (
        Path("AGENTS.md"),
        f"cases are still missed at {MEASURED_PLATFORM_CHECK_VERSION} in their ordinary form",
    ),
    (
        Path("MAINTAINERS.md"),
        f"still unmet at {MEASURED_PLATFORM_CHECK_VERSION}",
    ),
    (
        Path("README.md"),
        f"re-measured against `platform-check` {MEASURED_PLATFORM_CHECK_VERSION}",
    ),
    (
        Path("Taskfile.yml"),
        f"platform-check ({MEASURED_PLATFORM_CHECK_VERSION}) runs inside",
    ),
    (
        Path("scripts/repo_tools/hosted_ci_policy.py"),
        f"As measured against **{MEASURED_PLATFORM_CHECK_VERSION}**",
    ),
    (
        Path("scripts/verify.py"),
        f"Patapsco's ``platform-check`` ({MEASURED_PLATFORM_CHECK_VERSION})",
    ),
    (
        Path("tests/test_verify.py"),
        f"``platform-check`` {MEASURED_PLATFORM_CHECK_VERSION} expands",
    ),
)


def _read_text(path: Path, issues: list[str]) -> str | None:
    """Read one contract file, recording an actionable issue at the IO boundary."""

    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        issues.append(f"{path}: cannot read platform-gate contract: {error}")
        return None


def _string_mapping(value: object) -> dict[str, object] | None:
    """Narrow a parsed value to a string-keyed mapping."""

    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        return None
    return {key: item for key, item in value.items() if isinstance(key, str)}


def _string_list(value: object) -> list[str] | None:
    """Narrow a parsed value to a list of strings."""

    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return [item for item in value if isinstance(item, str)]


def _dependabot_pattern_matches(dependency: str, pattern: str) -> bool:
    """Match Dependabot's documented ``*`` wildcard and no extra glob syntax."""

    expression = re.escape(pattern.lower()).replace(r"\*", ".*")
    return re.fullmatch(expression, dependency.lower()) is not None


def _normalized_requirement_name(requirement: str) -> str | None:
    """Return a PEP 503-normalized distribution name from a requirement string."""

    match = _REQUIREMENT_NAME.match(requirement)
    if match is None:
        return None
    return re.sub(r"[-_.]+", "-", match.group("name")).lower()


def _pinned_version(pyproject_path: Path, issues: list[str]) -> str | None:
    """Return the exact Patapsco pin after validating its manifest shape."""

    source = _read_text(pyproject_path, issues)
    if source is None:
        return None
    try:
        parsed: object = tomllib.loads(source)
    except tomllib.TOMLDecodeError as error:
        issues.append(f"{pyproject_path}: invalid TOML: {error}")
        return None

    project = _string_mapping(parsed)
    groups = _string_mapping(project.get("dependency-groups")) if project is not None else None
    dev = _string_list(groups.get("dev")) if groups is not None else None
    if dev is None:
        issues.append(
            f"{pyproject_path}: [dependency-groups].dev must be a list of dependency strings"
        )
        return None

    candidates = [entry for entry in dev if _normalized_requirement_name(entry) == _DEPENDENCY_NAME]
    if len(candidates) != 1:
        issues.append(
            f"{pyproject_path}: expected exactly one {_DEPENDENCY_NAME} dev dependency, "
            f"found {len(candidates)}"
        )
        return None

    match = _EXACT_PIN.fullmatch(candidates[0])
    if match is None:
        issues.append(
            f"{pyproject_path}: {_DEPENDENCY_NAME} must use one exact '==<version>' pin, "
            f"found {candidates[0]!r}"
        )
        return None
    return match.group("version")


def _validate_dependabot(path: Path, issues: list[str]) -> None:
    """Require Patapsco updates to arrive alone, outside broad dependency groups."""

    try:
        parsed: object = load_yaml_file(path, label="Dependabot configuration")
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        issues.append(f"{path}: cannot load platform-gate update contract: {error}")
        return

    root = _string_mapping(parsed)
    updates_raw = root.get("updates") if root is not None else None
    if not isinstance(updates_raw, list):
        issues.append(f"{path}: updates must be a list")
        return

    uv_updates: list[dict[str, object]] = []
    for item in updates_raw:
        update = _string_mapping(item)
        if update is not None and update.get("package-ecosystem") == "uv":
            uv_updates.append(update)
    if len(uv_updates) != 1:
        issues.append(
            f"{path}: expected exactly one uv update configuration, found {len(uv_updates)}"
        )
        return

    uv_update = uv_updates[0]
    if uv_update.get("directory") != "/":
        issues.append(f"{path}: the uv update must use the single root directory '/'")
    unsupported_keys = (
        "directories",
        "multi-ecosystem-group",
        "patterns",
        "target-branch",
    )
    for key in unsupported_keys:
        if key in uv_update:
            issues.append(
                f"{path}: the uv update must not define {key!r}; "
                "the platform gate requires one default-branch, single-ecosystem root PR"
            )

    groups = _string_mapping(uv_update.get("groups"))
    if groups is None:
        issues.append(f"{path}: root uv updates must define dependency groups")
        return

    platform_group = _string_mapping(groups.get("platform-gate"))
    patterns = _string_list(platform_group.get("patterns")) if platform_group is not None else None
    if patterns != [_DEPENDENCY_NAME]:
        issues.append(
            f"{path}: groups.platform-gate.patterns must contain only {_DEPENDENCY_NAME!r}"
        )
    if platform_group is not None and set(platform_group) != {"patterns"}:
        issues.append(
            f"{path}: groups.platform-gate must define only its exact patterns list; "
            "filters or exclusions would let some Patapsco version bumps escape the group"
        )

    for group_name, group_raw in groups.items():
        if group_name == "platform-gate":
            continue
        group = _string_mapping(group_raw)
        if group is None:
            issues.append(f"{path}: group {group_name!r} must be a mapping")
            continue
        patterns_raw = group.get("patterns")
        group_patterns = _string_list(patterns_raw)
        if patterns_raw is not None and group_patterns is None:
            issues.append(f"{path}: group {group_name!r} patterns must be a list of strings")
        elif group_patterns == []:
            issues.append(f"{path}: group {group_name!r} patterns must not be empty")
        # Dependabot permits criteria-only groups. With no name patterns, any
        # dependency that satisfies those criteria can enter the group.
        matches = group_patterns is None or any(
            _dependabot_pattern_matches(_DEPENDENCY_NAME, pattern) for pattern in group_patterns
        )

        exclusions_raw = group.get("exclude-patterns")
        exclusions = _string_list(exclusions_raw)
        if exclusions_raw is not None and exclusions is None:
            issues.append(
                f"{path}: group {group_name!r} exclude-patterns must be a list of strings"
            )
        excluded = any(
            _dependabot_pattern_matches(_DEPENDENCY_NAME, pattern) for pattern in (exclusions or [])
        )
        if matches and not excluded:
            issues.append(
                f"{path}: group {group_name!r} also matches {_DEPENDENCY_NAME}; "
                "exclude the policy gate so its bump cannot be batched"
            )


def find_platform_guard_evidence_issues(repository_root: Path) -> list[str]:
    """Return pin, evidence, and update-group drift for the Patapsco gate."""

    issues: list[str] = []
    pinned_version = _pinned_version(repository_root / "pyproject.toml", issues)
    if pinned_version is not None and pinned_version != MEASURED_PLATFORM_CHECK_VERSION:
        issues.append(
            "pyproject.toml: baltimore-patapsco is pinned at "
            f"{pinned_version}, but differential evidence is recorded for "
            f"{MEASURED_PLATFORM_CHECK_VERSION}; run "
            "tests/test_platform_guard_differential.py against the new pin, "
            "review both checkers' results, then update the marker and living evidence"
        )

    _validate_dependabot(repository_root / ".github" / "dependabot.yml", issues)

    for relative_path, current_claim in _CURRENT_EVIDENCE_CLAIMS:
        source = _read_text(repository_root / relative_path, issues)
        if source is not None and current_claim not in source:
            issues.append(
                f"{relative_path}: current platform-check evidence must carry "
                f"the measured-release claim {current_claim!r}"
            )

    return issues
