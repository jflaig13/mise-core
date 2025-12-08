#!/bin/bash
set -euo pipefail

WATCH_DIR="/Users/jonathanflaig/Transcripts/approvals"
RUNNER="/Users/jonathanflaig/Transcripts/tipreport_runner.sh"

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