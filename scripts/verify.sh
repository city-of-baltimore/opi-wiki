#!/usr/bin/env bash

set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required. Install uv (https://docs.astral.sh/uv/) and run 'uv sync' first." >&2
  exit 1
fi

uv run python scripts/verify.py "$@"
