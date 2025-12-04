#!/bin/bash

FILE="$1"

if [[ -z "$FILE" ]]; then
  echo "Usage: test_transcript <filename.wav>"
  exit 1
fi

TRANSCRIBE_URL=$(gcloud run services describe payroll-transcribe --region us-central1 --format='value(status.url)')
ENGINE_URL=$(gcloud run services describe payroll-engine --region us-central1 --format='value(status.url)')
TOKEN=$(gcloud auth print-identity-token)

AUDIO="/Users/jonathanflaig/Google Drive/My Drive/Papa Staff Resources/Payroll Voice Recordings/$FILE"

echo "📡 Sending to /parse_only for transcript + preview..."

curl_output=$(curl -sS -H "Authorization: Bearer $TOKEN" -X POST "$ENGINE_URL/parse_only" \
  -F "audio=@$AUDIO" \
  -F "filename=$FILE")

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