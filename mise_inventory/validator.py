"""Validation helpers to ensure parsed output matches the catalog."""

from __future__ import annotations

from typing import Dict, List


def validate_output(results: Dict[str, dict], catalog: Dict[str, list]) -> List[str]:
    """Validate that all items live in the catalog categories.

    Returns a list of validation error strings (empty if valid).
    """

    errors: List[str] = []
    for cat, items in results.items():
        if cat not in catalog or not isinstance(catalog.get(cat), list):
            errors.append(f"Unknown category: {cat}")
            continue
        catalog_items = {obj.get("item") for obj in catalog.get(cat, []) if isinstance(obj, dict)}
        for item in items:
            if item not in catalog_items:
                errors.append(f"Unknown item '{item}' in category '{cat}'")
    return errors
