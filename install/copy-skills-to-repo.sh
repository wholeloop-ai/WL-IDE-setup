#!/usr/bin/env bash
# Install WholeLoop into a target app repo.
# Prefer: pipx install wholeloop-cli && wholeloop init /path/to/app
# Usage: ./install/copy-skills-to-repo.sh /absolute/path/to/target-app [--force]

set -euo pipefail

if command -v wholeloop >/dev/null 2>&1; then
  ARGS=()
  [[ "${2:-}" == "--force" ]] && ARGS+=(--force)
  exec wholeloop init "${1:-.}" "${ARGS[@]}"
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "wholeloop CLI not found — using bundled Python module." >&2
echo "Tip: pipx install $ROOT  OR  pipx install git+<this-repo-url>" >&2
exec python3 -m wholeloop.cli init "${1:-.}" ${2:+--force}
