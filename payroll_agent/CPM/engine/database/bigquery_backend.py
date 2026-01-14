"""BigQuery database backend for production."""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from google.cloud import bigquery

from .interface import DatabaseBackend


class BigQueryBackend(DatabaseBackend):
    """BigQuery implementation for production Cloud Run deployment."""

    def __init__(self):
        self.project_id = os.getenv("PROJECT_ID", "")
        self.dataset = os.getenv("BQ_DATASET", "payroll")
        self.table_shifts = os.getenv("BQ_TABLE_SHIFTS", "shifts")
        self._client = None

    def _get_client(self) -> bigquery.Client:
        """Lazy-load BigQuery client to avoid blocking container startup."""
        if self._client is None:
            self._client = bigquery.Client(project=self.project_id)
        return self._client

    def insert_shift_rows(
        self,
        rows: List[Dict[str, Any]],
        row_ids: List[str],
    ) -> Dict[str, Any]:
        """Insert shift rows into BigQuery with deduplication."""
        table = f"{self.project_id}.{self.dataset}.{self.table_shifts}"

        errors = self._get_client().insert_rows_json(
            table,
            rows,
            row_ids=row_ids,
        )

        if errors:
            raise Exception(f"BigQuery insert errors: {errors}")

        return {"ok": True, "inserted": len(rows)}

    def get_shifts(
        self,
        employee: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query shifts from BigQuery."""
        query = f"""
            SELECT *
            FROM `{self.project_id}.{self.dataset}.{self.table_shifts}`
            WHERE 1=1
        """

        if employee:
            query += f" AND employee = '{employee}'"
        if start_date:
            query += f" AND shift_date >= '{start_date.date().isoformat()}'"
        if end_date:
            query += f" AND shift_date <= '{end_date.date().isoformat()}'"

        query += f" ORDER BY shift_date DESC LIMIT {limit}"

        query_job = self._get_client().query(query)
        results = query_job.result()

        return [dict(row) for row in results]

    def health_check(self) -> Dict[str, Any]:
        """Check BigQuery connection health."""
        try:
            client = self._get_client()
            table_ref = f"{self.project_id}.{self.dataset}.{self.table_shifts}"
            table = client.get_table(table_ref)

            return {
                "status": "healthy",
                "backend": "bigquery",
                "project_id": self.project_id,
                "dataset": self.dataset,
                "table": self.table_shifts,
                "row_count": table.num_rows,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "bigquery",
                "error": str(e),
            }
