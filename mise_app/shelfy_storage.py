"""Local JSON storage for Shelfy (inventory) feature."""

from __future__ import annotations

import json
import logging
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional
import calendar

log = logging.getLogger(__name__)

# Storage directory - same as local_storage.py
STORAGE_DIR = Path(__file__).parent / "data"

# Valid areas by category
KITCHEN_AREAS = [
    "Dry Goods",
    "Kitchen/Line",
    "Walk-in",
    "Dish Pit/Chest Freezers",
    "Inside Bar",
    "Back Bar",
    "Misc",
]

BAR_AREAS = [
    "The Office",
    "Inside Bar",
    "Back Bar",
    "Walk-in",
    "Offsite Storage Unit",
    "Misc",
]


def get_last_day_of_month(year: int, month: int) -> date:
    """Get the last day of a given month."""
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)


def normalize_period_id(transcript: str = None, fallback_date: date = None) -> str:
    """Normalize a date reference to period_id (last day of month).

    Args:
        transcript: Optional transcript to scan for date mentions
        fallback_date: Date to use if no date found in transcript (defaults to today)

    Returns:
        Period ID as YYYY-MM-DD (last day of month)
    """
    target_date = fallback_date or date.today()

    if transcript:
        # Try to detect month from transcript
        transcript_lower = transcript.lower()

        month_names = {
            "january": 1, "jan": 1,
            "february": 2, "feb": 2,
            "march": 3, "mar": 3,
            "april": 4, "apr": 4,
            "may": 5,
            "june": 6, "jun": 6,
            "july": 7, "jul": 7,
            "august": 8, "aug": 8,
            "september": 9, "sep": 9, "sept": 9,
            "october": 10, "oct": 10,
            "november": 11, "nov": 11,
            "december": 12, "dec": 12,
        }

        for month_name, month_num in month_names.items():
            if month_name in transcript_lower:
                # Use current year, but handle year boundary
                year = target_date.year
                # If mentioned month is far ahead, might be talking about last year
                if month_num > target_date.month + 6:
                    year -= 1
                # If mentioned month is far behind, might be talking about next year
                elif month_num < target_date.month - 6:
                    year += 1

                target_date = get_last_day_of_month(year, month_num)
                log.info(f"🗄️ Detected month '{month_name}' → period {target_date.isoformat()}")
                break

    # Return last day of the month containing target_date
    last_day = get_last_day_of_month(target_date.year, target_date.month)
    return last_day.isoformat()


def generate_shelfy_id(area: str, timestamp: datetime = None) -> str:
    """Generate a unique shelfy ID.

    Format: shelfy_{timestamp}_{area_slug}
    """
    ts = timestamp or datetime.now()
    ts_str = ts.strftime("%Y%m%d_%H%M%S")
    area_slug = area.lower().replace(" ", "_").replace("/", "_")
    return f"shelfy_{ts_str}_{area_slug}"


def get_audio_archive_path(period_id: str, category: str, area: str, ext: str = ".wav") -> str:
    """Get the archive path for shelfy audio.

    Format: recordings/{period_id}/{Category}_{Area}_{timestamp}{ext}
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    category_cap = category.capitalize()
    area_clean = area.replace(" ", "").replace("/", "")
    return f"recordings/{period_id}/{category_cap}_{area_clean}_{timestamp}{ext}"


class ShelfyStorage:
    """Local JSON storage for shelfies, isolated by inventory period."""

    def __init__(self, storage_dir: Path = STORAGE_DIR):
        self.storage_dir = storage_dir

    def _get_shelfy_file(self, period_id: str) -> Path:
        """Get the shelfies JSON file for a period."""
        period_dir = self.storage_dir / "inventory" / period_id
        period_dir.mkdir(parents=True, exist_ok=True)
        return period_dir / "shelfies.json"

    def _load(self, period_id: str) -> List[Dict[str, Any]]:
        """Load all shelfies for a period."""
        shelfy_file = self._get_shelfy_file(period_id)
        if not shelfy_file.exists():
            return []
        try:
            with open(shelfy_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, period_id: str, data: List[Dict[str, Any]]):
        """Save shelfies for a period."""
        shelfy_file = self._get_shelfy_file(period_id)
        with open(shelfy_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_shelfy(
        self,
        period_id: str,
        shelfy_id: str,
        area: str,
        category: str,
        transcript: str,
        audio_path: str,
    ) -> Dict[str, Any]:
        """Add a new shelfy record.

        Returns the created shelfy dict.
        """
        data = self._load(period_id)
        now = datetime.now()

        shelfy = {
            "shelfy_id": shelfy_id,
            "area": area,
            "category": category,
            "period_id": period_id,
            "transcript": transcript,
            "audio_path": audio_path,
            "status": "pending_approval",
            "recorded_at": now.isoformat() + "Z",
            "created_at": now.isoformat(),
        }

        data.append(shelfy)
        self._save(period_id, data)
        log.info(f"🗄️ Added shelfy {shelfy_id} for {area} ({category}) in period {period_id}")

        return shelfy

    def get_shelfy(self, period_id: str, shelfy_id: str) -> Optional[Dict[str, Any]]:
        """Get a single shelfy by ID."""
        data = self._load(period_id)
        for shelfy in data:
            if shelfy.get("shelfy_id") == shelfy_id:
                return shelfy
        return None

    def get_all_shelfies(self, period_id: str) -> List[Dict[str, Any]]:
        """Get all shelfies for a period."""
        return self._load(period_id)

    def approve_shelfy(self, period_id: str, shelfy_id: str) -> bool:
        """Mark a shelfy as approved.

        Returns True if found and updated, False otherwise.
        """
        data = self._load(period_id)
        for shelfy in data:
            if shelfy.get("shelfy_id") == shelfy_id:
                shelfy["status"] = "approved"
                shelfy["approved_at"] = datetime.now().isoformat()
                self._save(period_id, data)
                log.info(f"🗄️ Approved shelfy {shelfy_id} in period {period_id}")
                return True
        return False

    def delete_shelfy(self, period_id: str, shelfy_id: str) -> bool:
        """Delete a shelfy (for re-recording).

        Returns True if found and deleted, False otherwise.
        """
        data = self._load(period_id)
        original_len = len(data)
        data = [s for s in data if s.get("shelfy_id") != shelfy_id]

        if len(data) < original_len:
            self._save(period_id, data)
            log.info(f"🗄️ Deleted shelfy {shelfy_id} from period {period_id}")
            return True
        return False

    def get_period_summary(self, period_id: str) -> Dict[str, Any]:
        """Get summary stats for a period."""
        data = self._load(period_id)

        kitchen_count = len([s for s in data if s.get("category") == "kitchen"])
        bar_count = len([s for s in data if s.get("category") == "bar"])
        approved_count = len([s for s in data if s.get("status") == "approved"])
        pending_count = len([s for s in data if s.get("status") == "pending_approval"])

        return {
            "period_id": period_id,
            "total_shelfies": len(data),
            "kitchen_count": kitchen_count,
            "bar_count": bar_count,
            "approved_count": approved_count,
            "pending_count": pending_count,
        }


# Singleton
_shelfy_storage: Optional[ShelfyStorage] = None


def get_shelfy_storage() -> ShelfyStorage:
    """Get the singleton ShelfyStorage instance."""
    global _shelfy_storage
    if _shelfy_storage is None:
        _shelfy_storage = ShelfyStorage()
    return _shelfy_storage
