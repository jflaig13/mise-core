#!/bin/zsh

# ===== CONFIG =====

WATCH_DIR="/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Papa Staff Resources/Payroll Voice Recordings"
ARCHIVE_DIR="/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Papa Staff Resources/Payroll Voice Recordings Archive"
ENGINE_URL="https://payroll-engine-147422626167.us-central1.run.app"
PYTHON_BIN="${PYTHON_BIN:-$HOME/mise-core/venv/bin/python3}"

pretty_print_preview() {
  local json="$1"

  "$PYTHON_BIN" - "$json" << 'PYCODE'
import sys, json

if len(sys.argv) < 2:
    sys.exit(0)
raw = sys.argv[1]
try:
    data = json.loads(raw)
except Exception:
    print(raw)
    sys.exit(0)

fn = data.get("filename", "")
rows = data.get("rows", [])
transcript = data.get("transcript", "")

width = 72
print("=" * width)
print(f" SHIFT PREVIEW: {fn}")
print("=" * width)
print()
print(f" {'DATE':<12} {'SHIFT':<7} {'EMPLOYEE':<18} {'ROLE':<9} {'AMOUNT':>8}")
print("-" * width)
for r in rows:
    date = r.get('date', '')
    shift = r.get('shift', '')
    emp = r.get('employee', '')
    role = r.get('role', '')
    amt = r.get('amount_final', 0)
    try:
        amt_val = float(amt)
    except Exception:
        amt_val = 0.0
    print(f" {date:<12} {shift:<7} {emp:<18} {role:<9} ${amt_val:8.2f}")
print()
print("FULL TRANSCRIPT:\n")
print(transcript or "<no transcript>")
print()
print("=" * width)
PYCODE
}

echo "👀 Watching for new .wav files in:"
echo "   $WATCH_DIR"
echo ""

mkdir -p "$ARCHIVE_DIR"

# ===== MAIN LOOP =====

fswatch -0 "$WATCH_DIR" | while IFS= read -r -d "" path; do
  # Ignore m4a files
  if [[ "$path" == *.m4a ]]; then
    continue
  fi

  # Ignore temporary/sync artifacts
  if [[ "$path" == *.tmp || "$path" == *.part || "$path" == *.download ]]; then
    continue
  fi

  # Process only .wav files
  if [[ "$path" != *.wav ]]; then
    continue
  fi

  file="$path"
  # Get just the filename without using basename
  name="${file##*/}"

  echo "---------------------------------------------"
  echo "🎤 Detected new WAV file: $name"
  echo "Full path: $file"
  echo ""

  echo "📡 Sending to /parse_only for PREVIEW..."
  # If the file was moved or deleted (e.g., after archiving), skip
  if [[ ! -f "$file" ]]; then
    echo "⚠️ File no longer exists on disk. Skipping."
    continue
  fi

  PREVIEW_JSON=$(/usr/bin/curl -sS -X POST "$ENGINE_URL/parse_only" \
    -F "audio=@$file" \
    -F "filename=$name")

  if [[ -z "$PREVIEW_JSON" ]]; then
    echo "❌ Empty response from /parse_only. Skipping."
    continue
  fi

  echo ""
  echo "🧾 Preview (what WOULD be sent to BigQuery):"
  pretty_print_preview "$PREVIEW_JSON"
  echo ""

  # Ask for approval
  echo -n "✅ Approve and commit this shift to BigQuery? [y/N]: "
  read APPROVE < /dev/tty

  if [[ "$APPROVE" == "y" || "$APPROVE" == "Y" ]]; then
    echo ""
    echo "🚀 Committing to BigQuery via /commit_shift..."
    COMMIT_RESPONSE=$(/usr/bin/curl -sS -X POST "$ENGINE_URL/commit_shift" \
      -H "Content-Type: application/json" \
      -d "$PREVIEW_JSON")

    echo "🔁 Commit response:"
    echo "$COMMIT_RESPONSE"
  else
    echo ""
    echo "⏹ Skipping commit for $name (not approved)."
  fi

  echo ""
  echo "📦 Archiving file: $name"
  /bin/mv "$file" "$ARCHIVE_DIR"/
  echo "✅ Archived to: $ARCHIVE_DIR"
  echo "---------------------------------------------"
  echo ""
done
