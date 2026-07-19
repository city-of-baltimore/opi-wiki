#!/usr/bin/env bash
#
# Manual, advisory Snyk scan. This is NOT part of any gate.
#
# It is deliberately not wired into scripts/verify.sh, .github/workflows/ci.yml,
# or the deploy gate: Snyk plans cap the number of scans, so it runs on demand
# only. The recurring enforcement path is the server-side Snyk SCM integration.
# See patapsco/docs/operations/snyk-scanning.md.
#
#   npm install --global snyk && snyk auth      # one-time setup
#   ./scripts/security_snyk.sh                  # run it
#
# Pass extra flags straight through, e.g.:
#
#   ./scripts/security_snyk.sh --severity-threshold=high
#
# Scope note: this repo has no npm workspace, so there is no `snyk test`
# dependency scan to run. Its Python dependencies are uv-managed, and the Snyk
# CLI does not parse uv-managed pyproject.toml reliably — a temporary pip export
# can report versions that do not match uv.lock. Python dependency coverage
# therefore comes from the server-side Snyk integration, not from here. What is
# left, and what this script runs, is stack-agnostic source-code analysis.

set -euo pipefail

if ! command -v snyk >/dev/null 2>&1; then
  echo "snyk is required. Install it with 'npm install --global snyk' and run 'snyk auth' first." >&2
  echo "See patapsco/docs/operations/snyk-scanning.md." >&2
  exit 1
fi

echo "Running Snyk source-code analysis (advisory; not a gate)..."
snyk code test . "$@"
