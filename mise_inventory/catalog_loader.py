"""Helpers for loading inventory catalog data."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_CATALOG = Path(__file__).with_name("inventory_catalog.json")


def load_catalog(path: Path | str | None = None) -> Dict[str, Any]:
    """Load the inventory catalog JSON.

    If no path is provided, the catalog alongside this module is used.
    """

    catalog_path = Path(path) if path else DEFAULT_CATALOG
    with catalog_path.open("r") as f:
        return json.load(f)
