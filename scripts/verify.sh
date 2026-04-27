#!/usr/bin/env bash

set -euo pipefail

if ! command -v poetry >/dev/null 2>&1; then
  echo "Poetry is required. Install Poetry and run 'poetry install' first." >&2
  exit 1
fi

poetry run python scripts/verify.py "$@"
