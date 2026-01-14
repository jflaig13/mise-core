"""
Database abstraction interface for CPM payroll engine.

This allows switching between BigQuery (production) and PostgreSQL (local dev)
without changing business logic.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime


class DatabaseBackend(ABC):
    """Abstract base class for database backends."""

    @abstractmethod
    def insert_shift_rows(
        self,
        rows: List[Dict[str, Any]],
        row_ids: List[str],
    ) -> Dict[str, Any]:
        """
        Insert shift rows with deduplication.

        Args:
            rows: List of row dictionaries with fields:
                - shift_date (str): ISO date
                - shift (str): AM/PM
                - employee (str): Canonical name
                - role (str): server/busser/expo/utility
                - category (str): foh/support
                - amount_final (float): Tip amount
                - pool_hours (float|None)
                - food_sales (float|None)
                - filename (str)
                - file_id (str)
                - parsed_confidence (str)
                - parser_version (str)
                - inserted_at (str): ISO timestamp
            row_ids: Deduplication keys (filename-employee-date)

        Returns:
            {"ok": True, "inserted": count}

        Raises:
            Exception if insert fails
        """
        pass

    @abstractmethod
    def get_shifts(
        self,
        employee: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Query shifts from database.

        Args:
            employee: Filter by employee name
            start_date: Filter by date >= start_date
            end_date: Filter by date <= end_date
            limit: Max rows to return

        Returns:
            List of shift row dictionaries
        """
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """
        Check database connection health.

        Returns:
            {"status": "healthy"|"unhealthy", "backend": "bigquery"|"postgres", ...}
        """
        pass
