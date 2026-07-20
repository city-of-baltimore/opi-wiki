#!/usr/bin/env bash
#
# Install this repository's git hooks.
#
# Hooks are tracked in scripts/hooks/ and copied into the repo's .git/hooks/ so
# they are versioned and reviewable. A machine-wide core.hooksPath (if one is
# configured) still takes precedence for dispatch, but the conventional global
# dispatcher delegates to $GIT_DIR/hooks/<hook>, so an installed hook here runs
# either way.
#
# Run once after cloning:
#
#   ./scripts/install-hooks.sh

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
git_dir="$(git rev-parse --git-dir)"
source_dir="${repo_root}/scripts/hooks"
target_dir="${git_dir}/hooks"

mkdir -p "${target_dir}"

for hook_path in "${source_dir}"/*; do
  hook_name="$(basename "${hook_path}")"
  cp "${hook_path}" "${target_dir}/${hook_name}"
  chmod +x "${target_dir}/${hook_name}"
  echo "Installed ${hook_name} -> ${target_dir}/${hook_name}"
done

hooks_path="$(git config --get core.hooksPath || true)"
if [ -n "${hooks_path}" ]; then
  echo
  echo "Note: core.hooksPath is set to ${hooks_path}."
  echo "Hooks there run first; the standard dispatcher delegates to ${target_dir}."
fi
