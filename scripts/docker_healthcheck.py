#!/usr/bin/env python3
"""Exit successfully only when the Docker preview serves its canonical page."""

from __future__ import annotations

import sys

from scripts.repo_tools.docker_health import PreviewHealthError, require_preview_health


def main() -> int:
    """Run the Docker preview probe and expose an actionable failure."""

    try:
        require_preview_health()
    except PreviewHealthError as error:
        sys.stderr.write(f"Docker preview is unhealthy: {error}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
