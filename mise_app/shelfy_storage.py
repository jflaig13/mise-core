"""GCS-based JSON storage for Shelfy (inventory) feature.

Uses Google Cloud Storage for persistent inventory data across container restarts.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional
import calendar
import os
from google.cloud import storage

log = logging.getLogger(__name__)

# GCS bucket for inventory data
PROJECT_ID = os.environ.get("PROJECT_ID", "automation-station-478103")
INVENTORY_BUCKET = f"{PROJECT_ID}_inventory"

# Storage directory - kept for backwards compatibility, but not used for GCS
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
    """GCS-based JSON storage for shelfies, isolated by inventory period.

    Data is stored in GCS at: gs://{PROJECT_ID}_inventory/periods/{period_id}/shelfies.json
    """

    def __init__(self, bucket_name: str = INVENTORY_BUCKET):
        self.bucket_name = bucket_name
        self._gcs_client = None
        self._bucket = None

    @property
    def gcs_client(self):
        """Lazy-load GCS client."""
        if self._gcs_client is None:
            self._gcs_client = storage.Client(project=PROJECT_ID)
        return self._gcs_client

    @property
    def bucket(self):
        """Lazy-load GCS bucket (creates if doesn't exist)."""
        if self._bucket is None:
            try:
                self._bucket = self.gcs_client.bucket(self.bucket_name)
                # Check if bucket exists, create if not
                if not self._bucket.exists():
                    log.info(f"📦 Creating GCS bucket: {self.bucket_name}")
                    self._bucket = self.gcs_client.create_bucket(
                        self.bucket_name,
                        location="us-central1"
                    )
                else:
                    # Bucket exists, just get reference
                    self._bucket = self.gcs_client.get_bucket(self.bucket_name)
            except Exception as e:
                log.error(f"Failed to access/create bucket {self.bucket_name}: {e}")
                raise
        return self._bucket

    def _get_shelfy_blob_path(self, period_id: str) -> str:
        """Get the GCS blob path for a period's shelfies.

        Format: periods/{period_id}/shelfies.json
        """
        return f"periods/{period_id}/shelfies.json"

    def _load(self, period_id: str) -> List[Dict[str, Any]]:
        """Load all shelfies for a period from GCS."""
        blob_path = self._get_shelfy_blob_path(period_id)
        blob = self.bucket.blob(blob_path)

        if not blob.exists():
            log.debug(f"📭 No shelfies found for period {period_id} (blob doesn't exist)")
            return []

        try:
            content = blob.download_as_text()
            data = json.loads(content)
            log.debug(f"📥 Loaded {len(data)} shelfies from GCS for period {period_id}")
            return data
        except (json.JSONDecodeError, Exception) as e:
            log.error(f"Failed to load shelfies from GCS: {e}")
            return []

    def _save(self, period_id: str, data: List[Dict[str, Any]]):
        """Save shelfies for a period to GCS."""
        blob_path = self._get_shelfy_blob_path(period_id)
        blob = self.bucket.blob(blob_path)

        content = json.dumps(data, indent=2)
        blob.upload_from_string(
            content,
            content_type="application/json"
        )
        log.debug(f"💾 Saved {len(data)} shelfies to GCS for period {period_id}")

    def add_shelfy(
        self,
        period_id: str,
        shelfy_id: str,
        area: str,
        category: str,
        transcript: str,
        audio_path: str,
        inventory_json: Optional[Dict[str, Any]] = None,
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

        # Add inventory_json if provided
        if inventory_json:
            shelfy["inventory_json"] = inventory_json

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

    def update_shelfy_inventory(self, period_id: str, shelfy_id: str, inventory_json: Dict[str, Any]) -> bool:
        """Update the inventory_json for a shelfy.

        Used when user accepts/edits product matches.

        Returns True if found and updated, False otherwise.
        """
        data = self._load(period_id)
        for shelfy in data:
            if shelfy.get("shelfy_id") == shelfy_id:
                shelfy["inventory_json"] = inventory_json
                shelfy["updated_at"] = datetime.now().isoformat()
                self._save(period_id, data)
                log.info(f"🗄️ Updated inventory_json for shelfy {shelfy_id}")
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

    def get_aggregated_totals(self, period_id: str, category: Optional[str] = None) -> Dict[str, Any]:
        """Get aggregated inventory totals for a period.

        Combines all approved shelfies and sums quantities by product name.
        Also tracks breakdown by shelfy/area for each product.

        Args:
            period_id: Period to aggregate
            category: Optional filter by category (kitchen/bar)

        Returns:
            Dict with:
            - items: List of aggregated items (product_name, total_quantity, unit, category, breakdown)
            - shelfies_count: Number of shelfies aggregated
            - areas_covered: List of unique areas
        """
        data = self._load(period_id)

        # Filter to approved shelfies with inventory_json
        approved = [
            s for s in data
            if s.get("status") == "approved"
            and s.get("inventory_json")
            and s["inventory_json"].get("items")
        ]

        # Filter by category if specified
        if category:
            approved = [s for s in approved if s.get("category") == category]

        # Aggregate items by product name
        product_totals = {}
        areas_covered = set()

        for shelfy in approved:
            area = shelfy.get("area", "Unknown")
            areas_covered.add(area)
            shelfy_category = shelfy.get("category", "unknown")
            shelfy_id = shelfy.get("shelfy_id", "")

            for item in shelfy["inventory_json"]["items"]:
                product_name = item.get("product_name", "").strip()
                quantity = item.get("quantity")
                unit = item.get("unit", "")

                # Use converted_quantity if available (e.g., 24 cans), otherwise fallback to raw quantity
                converted_quantity = item.get("converted_quantity", quantity)

                # Use base_unit if available (e.g., "cans"), otherwise use original unit
                base_unit = item.get("base_unit", unit)

                if not product_name:
                    continue

                # Normalize product name (case-insensitive key)
                key = product_name.lower()

                if key not in product_totals:
                    product_totals[key] = {
                        "product_name": product_name,  # Keep original casing from first occurrence
                        "total_quantity": 0,
                        "unit": base_unit,  # Use base unit for final aggregated display
                        "category": shelfy_category,
                        "breakdown": [],  # Track contributions by shelfy/area
                    }

                # Sum converted quantity (skip if null)
                # This ensures "6 4-packs" contributes 24 to the total, not 6
                if converted_quantity is not None:
                    product_totals[key]["total_quantity"] += converted_quantity
                    # Track breakdown: which area contributed how much
                    product_totals[key]["breakdown"].append({
                        "area": area,
                        "quantity": converted_quantity,
                        "shelfy_id": shelfy_id,
                    })

        # Sort by product name
        items = sorted(product_totals.values(), key=lambda x: x["product_name"])

        return {
            "items": items,
            "shelfies_count": len(approved),
            "areas_covered": sorted(areas_covered),
        }


# Singleton
_shelfy_storage: Optional[ShelfyStorage] = None


def get_shelfy_storage() -> ShelfyStorage:
    """Get the singleton ShelfyStorage instance."""
    global _shelfy_storage
    if _shelfy_storage is None:
        _shelfy_storage = ShelfyStorage()
    return _shelfy_storage
