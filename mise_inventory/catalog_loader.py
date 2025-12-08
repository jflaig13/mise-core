"""Helpers for loading inventory catalog data and schema paths."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict
import csv

PACKAGE_ROOT = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_ROOT.parent / "data"
DEFAULT_CATALOG_PATH = DATA_DIR / "inventory_catalog.json"
SCHEMA_PATH = PACKAGE_ROOT / "inventory_schema.json"
DEFAULT_ROSTER_PATH = PACKAGE_ROOT.parent / "papa_surf_roster.csv"


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
        catalog = json.load(f)

    roster_path = Path(
        os.getenv("ROSTER_CSV_PATH", DEFAULT_ROSTER_PATH)
    )
    if roster_path.exists():
        catalog = merge_roster_into_catalog(catalog, roster_path)

    return catalog


def _normalize_category(name: str) -> str:
    """Normalize category strings to match catalog keys."""

    return (
        "".join(ch if ch.isalnum() else "_" for ch in name.lower())
        .replace("__", "_")
        .strip("_")
    )


def merge_roster_into_catalog(catalog: Dict[str, Any], roster_csv: Path) -> Dict[str, Any]:
    """Merge items from a product roster CSV into the catalog structure."""

    if not roster_csv.exists():
        return catalog

    with roster_csv.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_name = (row.get("Item Name") or "").strip()
            if not item_name:
                continue
            raw_cat = (row.get("Category") or "misc").strip()
            cat = _normalize_category(raw_cat)
            case_size = row.get("Case Size") or ""

            entry = {"item": item_name}

            kws = []
            for part in item_name.replace("/", " ").replace(",", " ").split():
                p = part.strip().lower()
                if p and p not in kws:
                    kws.append(p)
            if kws:
                entry["keywords"] = kws

            try:
                cs_val = float(case_size)
                if cs_val > 0:
                    entry["case_size"] = cs_val
            except Exception:
                pass

            catalog.setdefault(cat, [])
            existing = next((e for e in catalog[cat] if e.get("item") == item_name), None)
            if existing:
                # Merge keywords and case size
                if "keywords" in entry:
                    existing.setdefault("keywords", [])
                    for kw in entry["keywords"]:
                        if kw not in existing["keywords"]:
                            existing["keywords"].append(kw)
                if "case_size" in entry and "case_size" not in existing:
                    existing["case_size"] = entry["case_size"]
            else:
                catalog[cat].append(entry)

    return catalog
