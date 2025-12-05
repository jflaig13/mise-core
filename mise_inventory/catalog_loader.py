"""Helpers for loading inventory catalog data and schema paths."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

PACKAGE_ROOT = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_ROOT.parent / "data"
DEFAULT_CATALOG_PATH = DATA_DIR / "inventory_catalog.json"
SCHEMA_PATH = PACKAGE_ROOT / "inventory_schema.json"


def load_catalog(catalog_path: str | Path | None = None) -> Dict[str, Any]:
    """Load the inventory catalog from disk.

    If no path is provided, we default to ``data/inventory_catalog.json`` so
    callers do not need to remember the file layout.
    """

    path = Path(catalog_path) if catalog_path else DEFAULT_CATALOG_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Catalog file not found at {path}. Ensure the data files are in place."
        )

    with path.open("r") as f:
        return json.load(f)
