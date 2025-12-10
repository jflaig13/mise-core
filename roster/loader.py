import json
from functools import lru_cache
from pathlib import Path
from typing import Optional


def get_roster_path() -> Path:
    """Return the canonical roster JSON path."""
    return Path(__file__).resolve().parent.parent / "workflow_specs" / "roster" / "employee_roster.json"


@lru_cache(maxsize=1)
def load_roster(path: Optional[Path] = None) -> dict:
    roster_path = Path(path) if path else get_roster_path()
    with roster_path.open("r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _first_name_index() -> dict:
    roster = load_roster()
    first_map = {}
    for full_name in set(roster.values()):
        first = full_name.split()[0].lower()
        if first not in first_map:
            first_map[first] = full_name
        else:
            # Ambiguous first name: mark as None to avoid incorrect mapping
            if first_map[first] != full_name:
                first_map[first] = None
    return first_map


def normalize_employee_name(raw: str) -> Optional[str]:
    """
    Normalize any employee reference (first name only or variants) to canonical "First Last"
    using the standalone roster. No other name lists are allowed.
    """
    if raw is None:
        return None
    roster = load_roster()
    key = " ".join(raw.strip().lower().split())
    if not key:
        return None

    # Direct match (full or variant)
    if key in roster:
        return roster[key]

    # First-name-only mapping if unambiguous
    first_map = _first_name_index()
    if key in first_map:
        return first_map[key]

    return None
