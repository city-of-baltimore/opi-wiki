#!/usr/bin/env bash

set -euo pipefail

if ! command -v poetry >/dev/null 2>&1; then
  echo "Poetry is required. Install Poetry and run 'poetry install' first." >&2
  exit 1
fi

echo "Linting repo automation..."
poetry run ruff check main.py scripts tests

echo "Running repo automation tests..."
poetry run pytest

echo "Validating page metadata..."
poetry run python scripts/check_page_metadata.py

echo "Validating brand terms..."
poetry run python scripts/check_brand_terms.py

echo "Building MkDocs site with strict validation..."
poetry run mkdocs build --strict

echo "Checking raw HTML links..."
poetry run python scripts/check_html_links.py

echo "Running accessibility smoke checks..."
poetry run python scripts/check_accessibility_smoke.py

if command -v flyctl >/dev/null 2>&1 && [ -f fly.toml ]; then
  echo "Validating Fly config..."
  flyctl config validate >/dev/null
fi

echo "Verification passed."
