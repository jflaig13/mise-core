from fastapi import APIRouter
from google.cloud import bigquery
from datetime import datetime

from .database import get_db

router = APIRouter()

# Lazy-load BigQuery client - replaced with database abstraction
# _bq = None
#
# def get_bq_client():
#     global _bq
#     if _bq is None:
#         _bq = bigquery.Client()
#     return _bq

@router.post("/commit_shift")
async def commit_shift(payload: dict):
    """
    Commit shift rows using database abstraction.
    Supports both BigQuery (production) and PostgreSQL (local dev).
    """
    rows = payload["rows"]
    filename = payload["filename"]

    # Add approval timestamp
    now = datetime.utcnow().isoformat(" ")

    formatted = []
    row_ids = []

    for r in rows:
        # Extract shift date for deduplication key
        shift_date = r.get("shift_date") or r.get("date")
        employee = r.get("employee")
        uid = f"{filename}-{employee}-{shift_date}"
        row_ids.append(uid)

        # Map parser output to actual database schema fields
        formatted.append(
            {
                "shift_date": shift_date,
                "shift": r.get("shift"),
                "employee": employee,
                "role": r.get("role"),
                "category": r.get("category", "foh"),
                "amount_final": r.get("amount_final"),
                "pool_hours": None,
                "food_sales": None,
                "filename": r.get("filename") or filename,
                "file_id": r.get("file_id", ""),
                "parsed_confidence": r.get("parsed_confidence", "high"),
                "parser_version": r.get("parser_version", "v1"),
                "inserted_at": now,
            }
        )

    try:
        result = get_db().insert_shift_rows(formatted, row_ids)
        return result
    except Exception as e:
        return {"ok": False, "inserted": 0, "error": str(e)}