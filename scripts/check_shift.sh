#!/bin/zsh

FILENAME="$1"

if [ -z "$FILENAME" ]; then
  echo "Usage: $0 <filename.wav>"
  exit 1
fi

bq query --use_legacy_sql=false \
"SELECT
   shift_date,
   shift,
   employee,
   role,
   amount_final,
   filename
 FROM \`automation-station-478103.payroll.shifts\`
 WHERE filename = \"$FILENAME\"
 ORDER BY employee"
