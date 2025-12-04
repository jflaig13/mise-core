#!/bin/bash

# ------------------------------
# CONFIG
# ------------------------------

WATCH_DIR="/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Papa Staff Resources/Payroll Voice Recordings"

echo "🎧 M4A → WAV converter running..."
echo "Watching: $WATCH_DIR"
echo ""

# ------------------------------
# MAIN LOOP
# ------------------------------

fswatch -0 "$WATCH_DIR" | while IFS= read -r -d "" file; do

  # Only act on .m4a files
  if [[ "$file" == *.m4a ]]; then
    base=$(basename "$file")
    name="${base%.*}"
    wav_path="$WATCH_DIR/${name}.wav"

    echo "🎤 Detected new M4A: $base"
    echo "🔄 Converting to WAV..."

    # Convert m4a → wav
    ffmpeg -y -i "$file" -ac 1 -ar 48000 "$wav_path" >/dev/null 2>&1

    echo "✅ Created WAV: ${name}.wav"

    # Remove the original m4a file
    rm "$file"
    echo "🗑️ Removed original: $base"
    echo ""
  fi

done