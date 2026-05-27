#!/usr/bin/env bash
# Copy WholeLoop generic skills into a target application repository.
# Usage: ./install/copy-skills-to-repo.sh /absolute/path/to/target-app [--force]

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/agents/skills"
FORCE=false
[[ "${2:-}" == "--force" ]] && FORCE=true

if [[ -z "${1:-}" ]]; then
  echo "Usage: $0 /absolute/path/to/target-app [--force]" >&2
  exit 1
fi

DEST="$1/.agents/skills"
if [[ -d "$DEST" ]] && [[ "$FORCE" != true ]]; then
  echo "Destination exists: $DEST" >&2
  echo "Re-run with --force to overwrite, or remove the directory first." >&2
  exit 1
fi

mkdir -p "$1/.agents"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"
REF_OUT="$DEST/references"
mkdir -p "$REF_OUT"
if [[ ! -f "$REF_OUT/project-conventions.md" ]]; then
  cp "$ROOT/references/PROJECT_CONVENTIONS.template.md" "$REF_OUT/project-conventions.md"
  echo "Created $REF_OUT/project-conventions.md from template — edit before running agents."
fi
echo "Copied skills to $DEST"
