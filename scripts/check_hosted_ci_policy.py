#!/usr/bin/env python3
"""CLI entry point for the hosted-CI lean-lane policy guard."""

from __future__ import annotations

import sys

try:
    from check_cli import ensure_repo_root_on_path
except ModuleNotFoundError:
    from scripts.check_cli import ensure_repo_root_on_path

ensure_repo_root_on_path()

from scripts.repo_tools.hosted_ci_policy import find_all_policy_violations  # noqa: E402


def main() -> int:
    """Report hosted-CI policy violations and return a shell exit code."""

    try:
        violations, workflow_paths = find_all_policy_violations()
    except RuntimeError as error:
        print(f"Hosted CI policy check failed unexpectedly: {error}", file=sys.stderr)
        return 1

    if violations:
        print(
            "Hosted CI is static checks, contracts, and security only. It must "
            "never reach a test suite, a site build, an image build, or a browser "
            "suite — directly or through an aggregate runner — and every job must "
            "declare timeout-minutes. Run the heavy tiers locally with "
            "'./scripts/verify.sh --plan prepush' or '--plan validate'.",
            file=sys.stderr,
        )
        for violation in violations:
            print(f"- {violation}", file=sys.stderr)
        return 1

    print(
        f"Hosted CI policy holds across {len(workflow_paths)} workflow(s): "
        "static configuration checks only."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
