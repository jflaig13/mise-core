"""Configuration for Shifty app."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List


@dataclass
class ShiftyConfig:
    """Configuration for the Shifty app."""

    # API endpoints
    transrouter_url: str = "http://localhost:8080"
    transrouter_api_key: str = "mise-core"

    # Google Sheets
    approval_sheet_id: str = ""
    totals_sheet_id: str = ""
    credentials_path: str = ""

    # Pay period
    pay_period_start: date = field(default_factory=lambda: date(2026, 1, 5))
    pay_period_end: date = field(default_factory=lambda: date(2026, 1, 11))

    @classmethod
    def from_env(cls) -> "ShiftyConfig":
        """Load config from environment variables."""
        return cls(
            transrouter_url=os.environ.get("TRANSROUTER_URL", "http://localhost:8080"),
            transrouter_api_key=os.environ.get("MISE_API_KEYS", "mise-core:mise").split(":")[0],
            approval_sheet_id=os.environ.get("APPROVAL_SHEET_ID", ""),
            totals_sheet_id=os.environ.get("TOTALS_SHEET_ID", ""),
            credentials_path=os.environ.get(
                "SHEETS_CREDENTIALS_PATH",
                os.path.expanduser("~/.config/mise/sheets_credentials.json")
            ),
        )

    @property
    def pay_period_label(self) -> str:
        """Human-readable pay period string."""
        return f"Jan {self.pay_period_start.day} - Jan {self.pay_period_end.day}, 2026"


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


# In-memory state for demo (would be DB in production)
class ShiftyState:
    """Track shifty status in memory."""

    def __init__(self):
        self._status: Dict[str, str] = {}  # code -> "not_started" | "pending" | "complete"

    def get_status(self, code: str) -> str:
        return self._status.get(code, "not_started")

    def set_status(self, code: str, status: str):
        self._status[code] = status

    def get_all_shifties(self, config: ShiftyConfig) -> List[dict]:
        """Get all shifties with current status."""
        result = []
        for defn in SHIFTY_DEFINITIONS:
            shifty_date = config.pay_period_start + timedelta(days=defn["date_offset"])
            result.append({
                "code": defn["code"],
                "label": defn["label"],
                "day": defn["day"],
                "date": shifty_date.strftime("%m/%d/%Y"),
                "status": self.get_status(defn["code"]),
            })
        return result

    def reset(self):
        """Reset all statuses."""
        self._status.clear()


# Global state instance
shifty_state = ShiftyState()
