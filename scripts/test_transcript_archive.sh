#!/bin/zsh

FILENAME="$1"

if [ -z "$FILENAME" ]; then
  echo "Usage: archive_transcript <filename.wav>"
  exit 1
fi

ARCHIVE_DIR="/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Papa Staff Resources/Payroll Voice Recordings Archive"

FILEPATH="$ARCHIVE_DIR/$FILENAME"

if [ ! -f "$FILEPATH" ]; then
  echo "❌ File not found in Archive:"
  echo "   $FILEPATH"
  exit 1
fi

echo "📡 Sending to /parse_only for transcript + preview..."
echo ""


# Capture server response first
curl_output=$(curl -sS -X POST "https://payroll-engine-147422626167.us-central1.run.app/parse_only" \
  -F "audio=@$FILEPATH" \
  -F "filename=$FILENAME")

# Print raw output for debugging
echo "Server response: $curl_output"

echo "$curl_output" | python3 - << 'PY'
import sys, json
raw = sys.stdin.read()
try:
    data = json.loads(raw)
    print("\nTRANSCRIPT:\n")
    print(data.get("transcript", "<no transcript>"))
    print("\nPARSED ROWS:\n")
    for r in data.get("rows", []):
        print(r)
    print("\n")
except Exception:
    print("\n❌ Could not parse JSON. Raw response was:\n")
    print(raw)
PY
