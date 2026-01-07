from fastapi import APIRouter
from google.cloud import bigquery
from datetime import datetime

router = APIRouter()

# Lazy-load BigQuery client to avoid blocking container startup
_bq = None

def get_bq_client():
    global _bq
    if _bq is None:
        _bq = bigquery.Client()
    return _bq

@router.post("/commit_shift")
async def commit_shift(payload: dict):
    rows = payload["rows"]
    filename = payload["filename"]

    table = "automation-station-478103.payroll.shifts"

    # Add approval timestamp
    now = datetime.utcnow().isoformat()

    formatted = []
    for r in rows:
        # Map parser output to actual BigQuery schema fields
        formatted.append(
            {
                "shift_date": r.get("shift_date") or r.get("date"),
                "shift": r.get("shift"),
                "employee": r.get("employee"),
                "role": r.get("role"),
                "amount_final": r.get("amount_final"),
                "filename": r.get("filename") or filename,
            }
        )

    errors = get_bq_client().insert_rows_json(table, formatted)
    if errors:
        return {"ok": False, "inserted": 0, "errors": errors}
    return {"ok": True, "inserted": len(formatted)}