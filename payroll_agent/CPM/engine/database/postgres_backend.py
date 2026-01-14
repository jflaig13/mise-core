"""PostgreSQL database backend for local development."""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2
import psycopg2.extras
from psycopg2.pool import SimpleConnectionPool

from .interface import DatabaseBackend


class PostgresBackend(DatabaseBackend):
    """PostgreSQL implementation for local Docker development."""

    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = int(os.getenv("POSTGRES_PORT", "5432"))
        self.database = os.getenv("POSTGRES_DB", "payroll")
        self.user = os.getenv("POSTGRES_USER", "payroll_user")
        self.password = os.getenv("POSTGRES_PASSWORD", "payroll_pass")
        self._pool = None

    def _get_pool(self) -> SimpleConnectionPool:
        """Lazy-load connection pool."""
        if self._pool is None:
            self._pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
        return self._pool

    def insert_shift_rows(
        self,
        rows: List[Dict[str, Any]],
        row_ids: List[str],
    ) -> Dict[str, Any]:
        """Insert shift rows into PostgreSQL with deduplication."""
        pool = self._get_pool()
        conn = pool.getconn()

        try:
            with conn.cursor() as cur:
                # Prepare data with row_id for deduplication
                for row, row_id in zip(rows, row_ids):
                    row["row_id"] = row_id

                # Insert with ON CONFLICT DO NOTHING for deduplication
                insert_query = """
                    INSERT INTO shifts (
                        row_id, shift_date, shift, employee, role, category,
                        amount_final, pool_hours, food_sales, filename, file_id,
                        parsed_confidence, parser_version, inserted_at
                    ) VALUES (
                        %(row_id)s, %(shift_date)s, %(shift)s, %(employee)s,
                        %(role)s, %(category)s, %(amount_final)s, %(pool_hours)s,
                        %(food_sales)s, %(filename)s, %(file_id)s,
                        %(parsed_confidence)s, %(parser_version)s, %(inserted_at)s
                    )
                    ON CONFLICT (row_id) DO NOTHING
                """

                psycopg2.extras.execute_batch(cur, insert_query, rows)
                conn.commit()

                return {"ok": True, "inserted": len(rows)}

        except Exception as e:
            conn.rollback()
            raise Exception(f"PostgreSQL insert error: {e}")
        finally:
            pool.putconn(conn)

    def get_shifts(
        self,
        employee: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query shifts from PostgreSQL."""
        pool = self._get_pool()
        conn = pool.getconn()

        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                query = "SELECT * FROM shifts WHERE 1=1"
                params = []

                if employee:
                    query += " AND employee = %s"
                    params.append(employee)
                if start_date:
                    query += " AND shift_date >= %s"
                    params.append(start_date.date())
                if end_date:
                    query += " AND shift_date <= %s"
                    params.append(end_date.date())

                query += " ORDER BY shift_date DESC LIMIT %s"
                params.append(limit)

                cur.execute(query, params)
                results = cur.fetchall()

                return [dict(row) for row in results]

        finally:
            pool.putconn(conn)

    def health_check(self) -> Dict[str, Any]:
        """Check PostgreSQL connection health."""
        try:
            pool = self._get_pool()
            conn = pool.getconn()

            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM shifts")
                row_count = cur.fetchone()[0]

            pool.putconn(conn)

            return {
                "status": "healthy",
                "backend": "postgres",
                "host": self.host,
                "database": self.database,
                "row_count": row_count,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "postgres",
                "error": str(e),
            }
