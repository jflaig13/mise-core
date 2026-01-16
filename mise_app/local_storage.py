"""Local JSON storage for Shifty app (fallback when Sheets unavailable)."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)

# Storage directory
STORAGE_DIR = Path(__file__).parent / "data"


class LocalApprovalStorage:
    """Local JSON storage for approval queue (replaces Google Sheets)."""

    def __init__(self, storage_dir: Path = STORAGE_DIR):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.approval_file = self.storage_dir / "approval_queue.json"
        self._ensure_file()

    def _ensure_file(self):
        if not self.approval_file.exists():
            self._save([])

    def _load(self) -> List[Dict[str, Any]]:
        try:
            with open(self.approval_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, data: List[Dict[str, Any]]):
        with open(self.approval_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_shifty(self, rows: List[Dict[str, Any]], filename: str, transcript: str) -> int:
        """Add parsed shifty data to approval queue."""
        data = self._load()
        start_idx = len(data)

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
                "created_at": datetime.now().isoformat(),
            })

        self._save(data)
        log.info(f"Added {len(rows)} rows for {filename}")
        return start_idx

    def get_by_filename(self, filename: str) -> List[Dict[str, Any]]:
        """Get all rows for a filename."""
        data = self._load()
        return [r for r in data if r.get("Filename") == filename]

    def get_pending_by_filename(self, filename: str) -> List[Dict[str, Any]]:
        """Get pending rows for a filename."""
        return [r for r in self.get_by_filename(filename) if r.get("Status") == "Pending"]

    def is_approved(self, filename: str) -> bool:
        """Check if all rows for a filename are approved."""
        rows = self.get_by_filename(filename)
        if not rows:
            return False
        return all(r.get("Status") == "Approved" for r in rows)

    def approve_all(self, filename: str):
        """Approve all rows for a filename."""
        data = self._load()
        for row in data:
            if row.get("Filename") == filename:
                row["Status"] = "Approved"
                row["approved_at"] = datetime.now().isoformat()
        self._save(data)
        log.info(f"Approved all rows for {filename}")

    def get_approved_data(self, filename: str) -> List[Dict[str, Any]]:
        """Get approved data for a filename."""
        return [r for r in self.get_by_filename(filename) if r.get("Status") == "Approved"]

    def update_row(self, row_id: str, updates: Dict[str, Any]):
        """Update a specific row."""
        data = self._load()
        for row in data:
            if row.get("id") == row_id:
                row.update(updates)
                break
        self._save(data)

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all rows."""
        return self._load()

    def clear(self):
        """Clear all data."""
        self._save([])


class LocalTotalsStorage:
    """Local JSON storage for weekly totals."""

    SHIFT_COLS = [
        "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
        "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM", "SuAM", "SuPM"
    ]

    def __init__(self, storage_dir: Path = STORAGE_DIR):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.totals_file = self.storage_dir / "weekly_totals.json"
        self._ensure_file()

    def _ensure_file(self):
        if not self.totals_file.exists():
            self._save({})

    def _load(self) -> Dict[str, Dict[str, float]]:
        try:
            with open(self.totals_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save(self, data: Dict[str, Dict[str, float]]):
        with open(self.totals_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_shift_amount(self, employee: str, shift_code: str, amount: float):
        """Add/update amount for employee's shift."""
        data = self._load()

        if employee not in data:
            data[employee] = {}

        data[employee][shift_code] = amount
        self._save(data)
        log.info(f"Updated {employee} {shift_code} = ${amount:.2f}")

    def get_employee_total(self, employee: str) -> float:
        """Get current weekly total for an employee."""
        data = self._load()
        if employee not in data:
            return 0.0
        return sum(data[employee].values())

    def get_all_totals(self) -> List[Dict[str, Any]]:
        """Get all employee totals for display."""
        data = self._load()
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

    def clear(self):
        """Clear all data."""
        self._save({})


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
