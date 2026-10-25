#!/usr/bin/env python3
"""Build site/, the GitHub Pages artifact, from the committed redirect stubs.

The stubs are already the site: building is a copy of ``redirects/stubs/`` into
a fresh ``site/``, which is the directory ``deploy.yml`` uploads. Nothing is
generated here, so the published bytes are exactly the reviewed ones.
"""

from __future__ import annotations

import shutil
import sys

try:
    from check_cli import REPO_ROOT
except ModuleNotFoundError:
    from scripts.check_cli import REPO_ROOT

SOURCE = REPO_ROOT / "redirects" / "stubs"
SITE = REPO_ROOT / "site"


def main() -> int:
    """Replace site/ with a copy of the committed stubs."""

    if not SOURCE.is_dir():
        sys.stderr.write(f"{SOURCE} is missing; there is nothing to publish.\n")
        return 1
    if SITE.exists():
        shutil.rmtree(SITE)
    shutil.copytree(SOURCE, SITE)
    count = sum(1 for path in SITE.rglob("*") if path.is_file())
    sys.stdout.write(f"Built site/ from redirects/stubs: {count} files.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
