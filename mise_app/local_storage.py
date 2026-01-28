"""Local JSON storage for Shifty app with multi-tenant support."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from mise_app.storage_backend import get_storage_backend

log = logging.getLogger(__name__)

# Default restaurant_id for backward compatibility during migration
DEFAULT_RESTAURANT_ID = "papasurf"


class LocalApprovalStorage:
    """JSON storage for approval queue, isolated by restaurant and pay period."""

    def __init__(self):
        self.backend = get_storage_backend()

    def _get_approval_path(self, restaurant_id: str, period_id: str) -> str:
        return f"{restaurant_id}/{period_id}/approval_queue.json"

    def _load(self, restaurant_id: str, period_id: str) -> List[Dict[str, Any]]:
        path = self._get_approval_path(restaurant_id, period_id)
        if not self.backend.exists(path):
            return []
        try:
            return self.backend.read_json(path)
        except Exception:
            return []

    def _save(self, restaurant_id: str, period_id: str, data: List[Dict[str, Any]]):
        path = self._get_approval_path(restaurant_id, period_id)
        self.backend.write_json(path, data)

    def add_shifty(
        self,
        period_id: str,
        rows: List[Dict[str, Any]],
        filename: str,
        transcript: str,
        parsed_date: str = None,
        detail_blocks: List = None,
        restaurant_id: str = DEFAULT_RESTAURANT_ID
    ) -> int:
        """Add parsed shifty data to approval queue for a pay period.

        Args:
            period_id: Pay period ID
            rows: List of row dicts with employee, role, amount, etc.
            filename: Audio filename
            transcript: Transcribed text
            parsed_date: The actual date parsed from transcript (MM/DD/YYYY format)
            detail_blocks: Calculation details from approval_json (for display)
            restaurant_id: Restaurant identifier for data isolation (default: papasurf)
        """
        data = self._load(restaurant_id, period_id)
        start_idx = len(data)

        # Serialize detail_blocks as JSON string for storage
        detail_blocks_json = json.dumps(detail_blocks) if detail_blocks else ""

        for i, row in enumerate(rows):
            data.append({
                "id": f"{filename}_{i}",
                "Date": row.get("date", ""),
                "Shift": row.get("shift", ""),
                "Employee": row.get("employee", ""),
                "Role": row.get("role", "Server"),
                "Amount": row.get("amount", 0),
                "Status": "Pending",
                "Filename": filename,
                "Transcript": transcript if i == 0 else "",
                "ParsedDate": parsed_date or "",
                "DetailBlocks": detail_blocks_json if i == 0 else "",
                "created_at": datetime.now().isoformat(),
            })

        self._save(restaurant_id, period_id, data)
        log.info(f"[{restaurant_id}] Added {len(rows)} rows for {filename} in period {period_id}")
        return start_idx

    def get_by_filename(self, period_id: str, filename: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> List[Dict[str, Any]]:
        """Get all rows for a filename in a pay period."""
        data = self._load(restaurant_id, period_id)
        return [r for r in data if r.get("Filename") == filename]

    def delete_by_filename(self, period_id: str, filename: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> int:
        """Delete all rows for a filename in a pay period (for re-recording)."""
        data = self._load(restaurant_id, period_id)
        original_count = len(data)
        data = [r for r in data if r.get("Filename") != filename]
        deleted_count = original_count - len(data)

        if deleted_count > 0:
            self._save(restaurant_id, period_id, data)
            log.info(f"[{restaurant_id}] Deleted {deleted_count} rows for {filename} in period {period_id}")

        return deleted_count

    def get_pending_by_filename(self, period_id: str, filename: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> List[Dict[str, Any]]:
        """Get pending rows for a filename in a pay period."""
        return [r for r in self.get_by_filename(period_id, filename, restaurant_id) if r.get("Status") == "Pending"]

    def is_approved(self, period_id: str, filename: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> bool:
        """Check if all rows for a filename are approved in a pay period."""
        rows = self.get_by_filename(period_id, filename, restaurant_id)
        if not rows:
            return False
        return all(r.get("Status") == "Approved" for r in rows)

    def approve_all(self, period_id: str, filename: str, restaurant_id: str = DEFAULT_RESTAURANT_ID):
        """Approve all rows for a filename in a pay period."""
        data = self._load(restaurant_id, period_id)
        for row in data:
            if row.get("Filename") == filename:
                row["Status"] = "Approved"
                row["approved_at"] = datetime.now().isoformat()
        self._save(restaurant_id, period_id, data)
        log.info(f"[{restaurant_id}] Approved all rows for {filename} in period {period_id}")

    def get_approved_data(self, period_id: str, filename: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> List[Dict[str, Any]]:
        """Get approved data for a filename in a pay period."""
        return [r for r in self.get_by_filename(period_id, filename, restaurant_id) if r.get("Status") == "Approved"]

    def update_row(self, period_id: str, row_id: str, updates: Dict[str, Any], restaurant_id: str = DEFAULT_RESTAURANT_ID):
        """Update a specific row in a pay period."""
        data = self._load(restaurant_id, period_id)
        for row in data:
            if row.get("id") == row_id:
                row.update(updates)
                break
        self._save(restaurant_id, period_id, data)

    def get_all(self, period_id: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> List[Dict[str, Any]]:
        """Get all rows for a pay period."""
        return self._load(restaurant_id, period_id)

    def clear(self, period_id: str, restaurant_id: str = DEFAULT_RESTAURANT_ID):
        """Clear all data for a pay period."""
        self._save(restaurant_id, period_id, [])


class LocalTotalsStorage:
    """JSON storage for weekly totals, isolated by restaurant and pay period."""

    SHIFT_COLS = [
        "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
        "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM", "SuAM", "SuPM"
    ]

    def __init__(self):
        self.backend = get_storage_backend()

    def _get_totals_path(self, restaurant_id: str, period_id: str) -> str:
        return f"{restaurant_id}/{period_id}/weekly_totals.json"

    def _load(self, restaurant_id: str, period_id: str) -> Dict[str, Dict[str, float]]:
        path = self._get_totals_path(restaurant_id, period_id)
        if not self.backend.exists(path):
            return {}
        try:
            return self.backend.read_json(path)
        except Exception:
            return {}

    def _save(self, restaurant_id: str, period_id: str, data: Dict[str, Dict[str, float]]):
        path = self._get_totals_path(restaurant_id, period_id)
        self.backend.write_json(path, data)

    def add_shift_amount(self, period_id: str, employee: str, shift_code: str, amount: float, restaurant_id: str = DEFAULT_RESTAURANT_ID):
        """Add/update amount for employee's shift in a pay period."""
        data = self._load(restaurant_id, period_id)

        if employee not in data:
            data[employee] = {}

        data[employee][shift_code] = amount
        self._save(restaurant_id, period_id, data)
        log.info(f"[{restaurant_id}] Updated {employee} {shift_code} = ${amount:.2f} in period {period_id}")

    def get_employee_total(self, period_id: str, employee: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> float:
        """Get current weekly total for an employee in a pay period."""
        data = self._load(restaurant_id, period_id)
        if employee not in data:
            return 0.0
        return sum(data[employee].values())

    def get_all_totals(self, period_id: str, restaurant_id: str = DEFAULT_RESTAURANT_ID) -> List[Dict[str, Any]]:
        """Get all employee totals for display in a pay period."""
        data = self._load(restaurant_id, period_id)
        results = []

        for employee, shifts in data.items():
            total = sum(shifts.values())
            shifts_worked = len([v for v in shifts.values() if v > 0])

            results.append({
                "name": employee,
                "total": total,
                "shifts_worked": shifts_worked,
                "shifts": shifts,
            })

        # Sort by total descending
        results.sort(key=lambda x: x["total"], reverse=True)
        return results

    def clear_shifty(self, period_id: str, shifty_code: str, restaurant_id: str = DEFAULT_RESTAURANT_ID):
        """Clear a specific shifty from all employees' totals."""
        data = self._load(restaurant_id, period_id)
        for employee in data:
            if shifty_code in data[employee]:
                del data[employee][shifty_code]
        self._save(restaurant_id, period_id, data)
        log.info(f"[{restaurant_id}] Cleared {shifty_code} from all employees in period {period_id}")

    def clear(self, period_id: str, restaurant_id: str = DEFAULT_RESTAURANT_ID):
        """Clear all data for a pay period."""
        self._save(restaurant_id, period_id, {})


# Singletons
_approval_storage: Optional[LocalApprovalStorage] = None
_totals_storage: Optional[LocalTotalsStorage] = None


def get_approval_storage() -> LocalApprovalStorage:
    global _approval_storage
    if _approval_storage is None:
        _approval_storage = LocalApprovalStorage()
    return _approval_storage


def get_totals_storage() -> LocalTotalsStorage:
    global _totals_storage
    if _totals_storage is None:
        _totals_storage = LocalTotalsStorage()
    return _totals_storage
