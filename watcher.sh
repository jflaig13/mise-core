#!/bin/bash

# ------------------------------
# CONFIG
# ------------------------------

PROJECT_ID="automation-station-478103"
REGION="us-central1"
SERVICE="payroll-engine"

# REAL Google Drive for Desktop path (NOT the Finder-friendly overlay!)
WATCH_DIR="/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Papa Staff Resources/Payroll Voice Recordings"

# Resolve Cloud Run Engine URL dynamically
ENGINE_URL=$(gcloud run services describe $SERVICE \
    --region="$REGION" \
    --project="$PROJECT_ID" \
    --format='value(status.url)')

pretty_print_preview() {
  local json="$1"

  echo "========================================================"
  echo " SHIFT PREVIEW: $(echo "$json" | jq -r '.filename')"
  echo "========================================================"
  echo

  printf " %-12s %-7s %-16s %-9s %-7s\n" "DATE" "SHIFT" "EMPLOYEE" "ROLE" "AMOUNT"
  echo "--------------------------------------------------------"

  echo "$json" | jq -r '.rows[] | @tsv "\(.date) \(.shift) \(.employee) \(.role) \(.amount_final)"' | \
  while IFS=$'\t' read -r date shift employee role amount; do
    printf " %-12s %-7s %-16s %-9s $%0.2f\n" "$date" "$shift" "$employee" "$role" "$amount"
  done

  echo
  echo "(Transcript: $(echo "$json" | jq -r '.transcript' | cut -c1-80)... )"
  echo "========================================================"
  echo
}

echo ""
echo "🔥 REAL-TIME PAYROLL INGESTION ACTIVE"
echo "📂 Watching folder:"
echo "   $WATCH_DIR"
echo ""
echo "🚀 Sending audio to:"
echo "   $ENGINE_URL/transcribe_and_ingest"
echo ""
echo "Leave this window open. Press CTRL + C to stop."
echo ""

# ------------------------------
# MAIN WATCH LOOP
# ------------------------------

fswatch -0 "$WATCH_DIR" | while IFS= read -r -d "" file; do

# Only process WAV files (ignore M4A)
if [[ "$file" == *.wav ]]; then
    name=$(basename "$file")

    echo "---------------------------------------------"
    echo "🎤 Detected new or updated file: $name"
    echo "📄 Full path: $file"
    echo "---------------------------------------------"

    # Obtain Cloud Run auth token
    TOKEN=$(gcloud auth print-identity-token)

    # Submit audio to Cloud Run payroll engine
    RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" \
    -F "audio=@${file}" \
    -F "filename=${name}" \
    "$ENGINE_URL/transcribe_and_ingest")

    echo "➡️  Engine Response:"
    echo "$RESPONSE"
    echo ""

    # Archive processed file
    ARCHIVE_DIR="/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Papa Staff Resources/Payroll Voice Recordings Archive"

    echo "📦 Archiving file: $name"
    mv "$file" "$ARCHIVE_DIR"/
    echo "✅ Archived to: $ARCHIVE_DIR"

  fi

done