#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_BASE="$ROOT_DIR/transcripts"
FALLBACK_BASES=(
  "/Users/jonathanflaig/transcripts"
  "/Users/jonathanflaig/Transcripts"
)
BASE="${LPM_TRANSCRIPTS_BASE:-$DEFAULT_BASE}"
if [ ! -d "$BASE" ]; then
  for fb in "${FALLBACK_BASES[@]}"; do
    if [ -d "$fb" ]; then
      BASE="$fb"
      break
    fi
  done
fi
export LPM_TRANSCRIPTS_BASE="$BASE"

IN="$BASE/approvals"
ARCH="$BASE/archive"
LOG="$BASE/logs/tipreport.log"
PY="$ROOT_DIR/transcripts/build_from_json.py"
PYBIN="$BASE/venv311/bin/python"
JQ="/opt/homebrew/bin/jq"

mkdir -p "$ARCH" "$BASE/logs" "$IN"
/usr/bin/printf "%s :: BASE %s\n" "$(date '+%F %T')" "$BASE" >> "$LOG"
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

# Full output directory = /Transcripts/Tip_Reports/<OUT_BASE>/
output_dir = os.path.join(base, "Tip_Reports", out_base.replace("TipReport_", ""))
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
    if emp_id is None:
        emp_id_str = ""
    else:
        try:
            emp_id_str = str(int(emp_id))
        except Exception:
            emp_id_str = str(emp_id)
    rows.append({
        "Employee ID": emp_id_str,
        "Tips Owed": total,
        "Employee Name": full_name
    })

df = pd.DataFrame(rows)
out = Path(output_dir) / filename
df.to_csv(out, index=False)
EOF

  /bin/mv "$f" "$ARCH"/

  if [ -n "$OUT_BASE" ]; then
    report_dir="$BASE/Tip_Reports/${OUT_BASE#TipReport_}"
    /usr/bin/open "$report_dir/${OUT_BASE}.pdf" || true
  fi

  /usr/bin/printf "%s :: done %s\n" "$(date '+%F %T')" "$f" >> "$LOG"
done
