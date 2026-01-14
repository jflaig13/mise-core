"""
Database abstraction layer for CPM payroll engine.

Factory function to get the appropriate database backend based on environment.
"""

import os
from typing import Optional

from .interface import DatabaseBackend
from .bigquery_backend import BigQueryBackend
from .postgres_backend import PostgresBackend


# Singleton instance
_db_instance: Optional[DatabaseBackend] = None


def get_database() -> DatabaseBackend:
    """
    Get the appropriate database backend based on DATABASE_BACKEND env var.

    Returns:
        DatabaseBackend instance (BigQuery or PostgreSQL)

    Environment Variables:
        DATABASE_BACKEND: "bigquery" or "postgres" (default: "bigquery")
    """
    global _db_instance

    if _db_instance is None:
        backend_type = os.getenv("DATABASE_BACKEND", "bigquery").lower()

        if backend_type == "postgres":
            _db_instance = PostgresBackend()
        elif backend_type == "bigquery":
            _db_instance = BigQueryBackend()
        else:
            raise ValueError(
                f"Unknown DATABASE_BACKEND: {backend_type}. "
                "Must be 'bigquery' or 'postgres'"
            )

    return _db_instance


def get_db() -> DatabaseBackend:
    """Alias for get_database() for convenience."""
    return get_database()


__all__ = ["DatabaseBackend", "get_database", "get_db"]
