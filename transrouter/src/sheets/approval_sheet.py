"""Approval sheet manager for Shifty workflow.

Manages the "Shifty Approval Queue" sheet where parsed shift data
is reviewed and approved before being added to weekly totals.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import gspread

from .sheets_client import SheetsClient, get_sheets_client

log = logging.getLogger(__name__)


class ApprovalSheet:
    """Manages the Shifty Approval Queue sheet.

    Columns:
        A: Date (MM/DD/YYYY)
        B: Shift (AM/PM)
        C: Employee
        D: Role
        E: Amount
        F: Status (Pending/Approved)
        G: Filename
        H: Transcript
    """

    COLUMNS = ["Date", "Shift", "Employee", "Role", "Amount", "Status", "Filename", "Transcript"]
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"

    def __init__(
        self,
        client: Optional[SheetsClient] = None,
        sheet_id: Optional[str] = None,
    ):
        """Initialize approval sheet manager.

        Args:
            client: SheetsClient instance (uses singleton if not provided)
            sheet_id: ID of the approval sheet (from env var if not provided)
        """
        self.client = client or get_sheets_client()
        self.sheet_id = sheet_id or os.environ.get('APPROVAL_SHEET_ID', '')
        self._worksheet: Optional[gspread.Worksheet] = None

    @property
    def worksheet(self) -> gspread.Worksheet:
        """Lazy-load the worksheet."""
        if self._worksheet is None:
            if not self.sheet_id:
                raise ValueError(
                    "APPROVAL_SHEET_ID environment variable not set. "
                    "Please set it to the Google Sheet ID."
                )
            spreadsheet = self.client.get_sheet(self.sheet_id)
            self._worksheet = spreadsheet.sheet1

            # Ensure headers exist
            self._ensure_headers()

        return self._worksheet

    def _ensure_headers(self):
        """Ensure the header row exists."""
        try:
            first_row = self._worksheet.row_values(1)
            if not first_row or first_row != self.COLUMNS:
                self._worksheet.update('A1:H1', [self.COLUMNS])
                log.info("Added headers to approval sheet")
        except Exception as e:
            log.warning(f"Could not check/set headers: {e}")

    def add_shifty(
        self,
        rows: List[Dict[str, Any]],
        filename: str,
        transcript: str,
    ) -> int:
        """Add parsed shifty data to the approval queue.

        Args:
            rows: List of dicts with keys: date, shift, employee, role, amount
            filename: The audio filename (e.g., "MAM.wav")
            transcript: The full transcript text

        Returns:
            Starting row number of the added data
        """
        if not rows:
            log.warning("No rows to add")
            return 0

        # Convert rows to sheet format
        sheet_rows = []
        for row in rows:
            sheet_rows.append([
                row.get("date", ""),
                row.get("shift", ""),
                row.get("employee", ""),
                row.get("role", "Server"),
                row.get("amount", 0),
                self.STATUS_PENDING,
                filename,
                transcript if len(sheet_rows) == 0 else "",  # Only first row gets transcript
            ])

        # Find next empty row
        all_values = self.worksheet.get_all_values()
        next_row = len(all_values) + 1

        # Append rows
        self.worksheet.append_rows(sheet_rows, value_input_option='USER_ENTERED')

        log.info(f"Added {len(sheet_rows)} rows for {filename} starting at row {next_row}")
        return next_row

    def get_pending_by_filename(self, filename: str) -> List[Dict[str, Any]]:
        """Get all pending rows for a specific filename."""
        all_records = self.worksheet.get_all_records()
        return [
            r for r in all_records
            if r.get("Filename") == filename and r.get("Status") == self.STATUS_PENDING
        ]

    def get_approved_by_filename(self, filename: str) -> List[Dict[str, Any]]:
        """Get all approved rows for a specific filename."""
        all_records = self.worksheet.get_all_records()
        return [
            r for r in all_records
            if r.get("Filename") == filename and r.get("Status") == self.STATUS_APPROVED
        ]

    def is_approved(self, filename: str) -> bool:
        """Check if all rows for a filename are approved."""
        all_records = self.worksheet.get_all_records()
        matching = [r for r in all_records if r.get("Filename") == filename]

        if not matching:
            return False

        return all(r.get("Status") == self.STATUS_APPROVED for r in matching)

    def get_approved_data(self, filename: str) -> List[Dict[str, Any]]:
        """Get approved data with any edits for a filename.

        Returns empty list if not all rows are approved.
        """
        if not self.is_approved(filename):
            return []

        return self.get_approved_by_filename(filename)

    def clear_all(self):
        """Clear all data except headers (for testing)."""
        self.worksheet.delete_rows(2, self.worksheet.row_count)
        log.info("Cleared approval sheet")


# Module-level singleton
_approval_sheet: Optional[ApprovalSheet] = None


def get_approval_sheet(sheet_id: Optional[str] = None) -> ApprovalSheet:
    """Get or create the approval sheet singleton."""
    global _approval_sheet

    if sheet_id:
        return ApprovalSheet(sheet_id=sheet_id)

    if _approval_sheet is None:
        _approval_sheet = ApprovalSheet()

    return _approval_sheet
