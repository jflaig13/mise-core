#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEFAULT_BASE="$SCRIPT_DIR"
FALLBACK_BASE="/Users/jonathanflaig/Transcripts"
BASE="${LPM_TRANSCRIPTS_BASE:-$DEFAULT_BASE}"
if [ ! -d "$BASE" ] && [ -d "$FALLBACK_BASE" ]; then
  BASE="$FALLBACK_BASE"
fi

WATCH_DIR="$BASE/approvals"
RUNNER="$SCRIPT_DIR/tipreport_runner.sh"

mkdir -p "$WATCH_DIR"

# Ensure fswatch exists
if ! command -v fswatch >/dev/null 2>&1; then
  echo "ERROR: fswatch not installed. Install with: brew install fswatch"
  exit 1
fi

echo "📡 Local watcher active — watching $WATCH_DIR for new .approve.json files..."

fswatch -0 "$WATCH_DIR" | while read -d "" file; do
  if [[ "$file" == *.approve.json ]]; then
    echo "🔥 Detected new approval file: $file"
    bash "$RUNNER"
  fi
done
