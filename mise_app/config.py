"""Configuration for Shifty app."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional


# Storage directory
STORAGE_DIR = Path(__file__).parent / "data"


@dataclass
class PayPeriod:
    """Represents a 7-day pay period."""

    start_date: date

    # Reference date from which all periods are calculated (a Monday)
    REFERENCE_DATE: date = field(default=date(2026, 1, 5), repr=False, compare=False)
    PERIOD_LENGTH: int = field(default=7, repr=False, compare=False)
    MAX_HISTORY: int = field(default=48, repr=False, compare=False)

    @property
    def id(self) -> str:
        """ISO date string identifier."""
        return self.start_date.isoformat()

    @property
    def end_date(self) -> date:
        """Last day of the pay period."""
        return self.start_date + timedelta(days=self.PERIOD_LENGTH - 1)

    @property
    def label(self) -> str:
        """Human-readable label."""
        start_month = self.start_date.strftime("%b")
        end_month = self.end_date.strftime("%b")
        if start_month == end_month:
            return f"{start_month} {self.start_date.day}-{self.end_date.day}, {self.end_date.year}"
        return f"{start_month} {self.start_date.day} - {end_month} {self.end_date.day}, {self.end_date.year}"

    @classmethod
    def from_id(cls, period_id: str) -> "PayPeriod":
        """Create from ISO date string."""
        return cls(start_date=date.fromisoformat(period_id))

    @classmethod
    def current(cls) -> "PayPeriod":
        """Get the current pay period containing today."""
        return cls.containing(date.today())

    @classmethod
    def containing(cls, target_date: date) -> "PayPeriod":
        """Get the pay period containing a specific date."""
        ref = cls.REFERENCE_DATE
        days_since_ref = (target_date - ref).days
        periods_since_ref = days_since_ref // cls.PERIOD_LENGTH
        period_start = ref + timedelta(days=periods_since_ref * cls.PERIOD_LENGTH)
        return cls(start_date=period_start)

    @classmethod
    def get_available_periods(cls) -> List["PayPeriod"]:
        """Get list of all available periods (current + history)."""
        current = cls.current()
        periods = []
        for i in range(cls.MAX_HISTORY):
            period_start = current.start_date - timedelta(days=i * cls.PERIOD_LENGTH)
            periods.append(cls(start_date=period_start))
        return periods

    def previous(self) -> Optional["PayPeriod"]:
        """Get the previous pay period (None if at history limit)."""
        prev_start = self.start_date - timedelta(days=self.PERIOD_LENGTH)
        oldest_allowed = self.current().start_date - timedelta(days=self.MAX_HISTORY * self.PERIOD_LENGTH)
        if prev_start < oldest_allowed:
            return None
        return PayPeriod(start_date=prev_start)

    def next(self) -> Optional["PayPeriod"]:
        """Get the next pay period (None if it would be future)."""
        next_start = self.start_date + timedelta(days=self.PERIOD_LENGTH)
        if next_start > self.current().start_date:
            return None
        return PayPeriod(start_date=next_start)

    def is_current(self) -> bool:
        """Check if this is the current period."""
        return self.start_date == self.current().start_date


@dataclass
class ShiftyConfig:
    """Configuration for the Shifty app."""

    # API endpoints (unused in direct-call architecture — kept for backward compat)
    transrouter_url: str = "http://localhost:8080"  # Dormant: agents called directly via Python imports
    transrouter_api_key: str = "mise-core"  # Dormant: agents called directly via Python imports

    # Google Sheets
    approval_sheet_id: str = ""
    totals_sheet_id: str = ""
    credentials_path: str = ""

    # Pay period reference date (first day of first pay period)
    pay_period_reference: date = field(default_factory=lambda: date(2026, 1, 5))

    @classmethod
    def from_env(cls) -> "ShiftyConfig":
        """Load config from environment variables."""
        ref_date_str = os.environ.get("PAY_PERIOD_REFERENCE", "2026-01-05")
        return cls(
            transrouter_url=os.environ.get("TRANSROUTER_URL", "http://localhost:8080"),
            transrouter_api_key=os.environ.get("MISE_API_KEYS", "mise-core:mise").split(":")[0],
            approval_sheet_id=os.environ.get("APPROVAL_SHEET_ID", ""),
            totals_sheet_id=os.environ.get("TOTALS_SHEET_ID", ""),
            credentials_path=os.environ.get(
                "SHEETS_CREDENTIALS_PATH",
                os.path.expanduser("~/.config/mise/sheets_credentials.json")
            ),
            pay_period_reference=date.fromisoformat(ref_date_str),
        )


# Shifty definitions - 14 shifts per week
SHIFTY_DEFINITIONS = [
    {"code": "MAM", "label": "Monday AM", "day": "Mon", "date_offset": 0},
    {"code": "MPM", "label": "Monday PM", "day": "Mon", "date_offset": 0},
    {"code": "TAM", "label": "Tuesday AM", "day": "Tue", "date_offset": 1},
    {"code": "TPM", "label": "Tuesday PM", "day": "Tue", "date_offset": 1},
    {"code": "WAM", "label": "Wednesday AM", "day": "Wed", "date_offset": 2},
    {"code": "WPM", "label": "Wednesday PM", "day": "Wed", "date_offset": 2},
    {"code": "ThAM", "label": "Thursday AM", "day": "Thu", "date_offset": 3},
    {"code": "ThPM", "label": "Thursday PM", "day": "Thu", "date_offset": 3},
    {"code": "FAM", "label": "Friday AM", "day": "Fri", "date_offset": 4},
    {"code": "FPM", "label": "Friday PM", "day": "Fri", "date_offset": 4},
    {"code": "SaAM", "label": "Saturday AM", "day": "Sat", "date_offset": 5},
    {"code": "SaPM", "label": "Saturday PM", "day": "Sat", "date_offset": 5},
    {"code": "SuAM", "label": "Sunday AM", "day": "Sun", "date_offset": 6},
    {"code": "SuPM", "label": "Sunday PM", "day": "Sun", "date_offset": 6},
]


def get_shifty_by_code(code: str) -> dict:
    """Get shifty definition by code."""
    for shifty in SHIFTY_DEFINITIONS:
        if shifty["code"] == code:
            return shifty
    raise ValueError(f"Unknown shifty code: {code}")


# Default restaurant_id for backward compatibility during migration
DEFAULT_RESTAURANT_ID = "papasurf"


# Shifty state management with per-period persistence and multi-tenant support
class ShiftyStateManager:
    """Manage shifty states across restaurants and pay periods with persistence."""

    def __init__(self):
        from mise_app.storage_backend import get_storage_backend
        self.backend = get_storage_backend()
        # Cache key is "restaurant_id/period_id" -> {code -> status}
        self._cache: Dict[str, Dict[str, str]] = {}

    def _cache_key(self, restaurant_id: str, period_id: str) -> str:
        return f"{restaurant_id}/{period_id}"

    def _get_state_path(self, restaurant_id: str, period_id: str) -> str:
        return f"{restaurant_id}/{period_id}/shifty_state.json"

    def _load_state(self, restaurant_id: str, period_id: str) -> Dict[str, str]:
        cache_key = self._cache_key(restaurant_id, period_id)
        if cache_key in self._cache:
            return self._cache[cache_key]

        path = self._get_state_path(restaurant_id, period_id)
        if self.backend.exists(path):
            try:
                self._cache[cache_key] = self.backend.read_json(path)
            except Exception:
                self._cache[cache_key] = {}
        else:
            self._cache[cache_key] = {}
        return self._cache[cache_key]

    def _save_state(self, restaurant_id: str, period_id: str):
        cache_key = self._cache_key(restaurant_id, period_id)
        path = self._get_state_path(restaurant_id, period_id)
        self.backend.write_json(path, self._cache.get(cache_key, {}))

    def get_status(self, period_id: str, code: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> str:
        """Get status for a shifty in a specific restaurant and period."""
        state = self._load_state(restaurant_id, period_id)
        return state.get(code, "not_started")

    def set_status(self, period_id: str, code: str, status: str, restaurant_id: str = DEFAULT_RESTAURANT_ID):
        """Set status for a shifty in a specific restaurant and period."""
        state = self._load_state(restaurant_id, period_id)
        state[code] = status
        self._save_state(restaurant_id, period_id)

    def get_all_shifties(self, period: PayPeriod, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> List[dict]:
        """Get all shifties with current status for a restaurant and pay period."""
        state = self._load_state(restaurant_id, period.id)
        result = []
        for defn in SHIFTY_DEFINITIONS:
            shifty_date = period.start_date + timedelta(days=defn["date_offset"])
            result.append({
                "code": defn["code"],
                "label": defn["label"],
                "day": defn["day"],
                "date": shifty_date.strftime("%m/%d/%Y"),
                "status": state.get(defn["code"], "not_started"),
            })
        return result

    def reset(self, period_id: str, restaurant_id: str = DEFAULT_RESTAURANT_ID):
        """Reset all statuses for a restaurant and pay period."""
        cache_key = self._cache_key(restaurant_id, period_id)
        self._cache[cache_key] = {}
        self._save_state(restaurant_id, period_id)


# Global state manager instance (lazy initialization to avoid circular import)
_shifty_state_manager: Optional['ShiftyStateManager'] = None


def get_shifty_state_manager() -> ShiftyStateManager:
    global _shifty_state_manager
    if _shifty_state_manager is None:
        _shifty_state_manager = ShiftyStateManager()
    return _shifty_state_manager


# Backward compatibility alias
shifty_state_manager = None  # Will be initialized on first use
