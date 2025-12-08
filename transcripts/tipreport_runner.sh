#!/bin/bash
set -euo pipefail

BASE="/Users/jonathanflaig/Transcripts"
IN="$BASE/approvals"
ARCH="$BASE/archive"
LOG="$BASE/logs/tipreport.log"
PY="$BASE/build_from_json.py"
PYBIN="$BASE/venv311/bin/python"
JQ="/opt/homebrew/bin/jq"

mkdir -p "$ARCH" "$BASE/logs"
/usr/bin/printf "%s :: scan %s\n" "$(date '+%F %T')" "$IN" >> "$LOG"

shopt -s nullglob

for f in "$IN"/*.approve.json; do
  /usr/bin/printf "%s :: found %s\n" "$(date '+%F %T')" "$f" >> "$LOG"

  OUT_BASE=""
  if [ -x "$JQ" ]; then
    OUT_BASE="$("$JQ" -r .out_base "$f" 2>/dev/null || echo "")"
  fi

  "$PYBIN" "$PY" "$f" >> "$LOG" 2>&1 || {
    /usr/bin/printf "%s :: ERROR building %s\n" "$(date '+%F %T')" "$f" >> "$LOG"
    continue
  }

  # Generate PayrollExport CSV
  "$PYBIN" - <<EOF
import json, pandas as pd, os
from pathlib import Path

json_path = "$f"
base = "$BASE"
out_base = "$OUT_BASE"
roster_path = os.path.join(base, "PayrollExportTemplate.csv")

# Full output directory = /Transcripts/<OUT_BASE>/
output_dir = os.path.join(base, out_base)
os.makedirs(output_dir, exist_ok=True)

with open(json_path, 'r') as jf:
    data = json.load(jf)

# Derive pay period from out_base (format: TipReport_MMDDYY_MMDDYY)
parts = out_base.split("_")
if len(parts) >= 3:
    start = parts[1]
    end = parts[2]
else:
    raise ValueError(f"Cannot parse pay period from out_base: {out_base}")

filename = f"{start}_{end}_PayrollExport.csv"

roster = pd.read_csv(roster_path)

rows = []
# roster CSV must have Last Name, First Name, Employee ID
roster_map = {}
for _, r in roster.iterrows():
    full = f"{r['First Name']} {r['Last Name']}"
    roster_map[full] = int(r["Employee ID"])

# Build rows using weekly_totals from the JSON
for full_name, total in data["weekly_totals"].items():
    emp_id = roster_map.get(full_name, None)
    rows.append({
        "Employee ID": emp_id,
        "Tips Owed": total,
        "Employee Name": full_name
    })

df = pd.DataFrame(rows)
out = Path(output_dir) / filename
df.to_csv(out, index=False)
EOF

  /bin/mv "$f" "$ARCH"/

  if [ -n "$OUT_BASE" ]; then
    /usr/bin/open "$BASE/${OUT_BASE}.pdf" || true
  fi

  /usr/bin/printf "%s :: done %s\n" "$(date '+%F %T')" "$f" >> "$LOG"
done
