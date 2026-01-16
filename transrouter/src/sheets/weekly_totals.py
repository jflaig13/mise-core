"""Weekly totals sheet manager for Shifty workflow.

Manages the running weekly totals sheet that staff can view
to see their accumulated tips throughout the pay period.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import gspread

from .sheets_client import SheetsClient, get_sheets_client

log = logging.getLogger(__name__)


class WeeklyTotalsSheet:
    """Manages the Weekly Totals sheet.

    Structure:
        Row 1: Header (Employee, MAM, MPM, TAM, TPM, ..., SuPM, TOTAL)
        Row 2+: Employee data
    """

    SHIFT_COLS = [
        "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
        "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM", "SuAM", "SuPM"
    ]
    HEADER = ["Employee"] + SHIFT_COLS + ["TOTAL"]

    def __init__(
        self,
        client: Optional[SheetsClient] = None,
        sheet_id: Optional[str] = None,
    ):
        """Initialize weekly totals sheet manager."""
        self.client = client or get_sheets_client()
        self.sheet_id = sheet_id or os.environ.get('TOTALS_SHEET_ID', '')
        self._worksheet: Optional[gspread.Worksheet] = None

    @property
    def worksheet(self) -> gspread.Worksheet:
        """Lazy-load the worksheet."""
        if self._worksheet is None:
            if not self.sheet_id:
                raise ValueError(
                    "TOTALS_SHEET_ID environment variable not set. "
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
            if not first_row or first_row != self.HEADER:
                self._worksheet.update('A1:P1', [self.HEADER])
                log.info("Added headers to weekly totals sheet")
        except Exception as e:
            log.warning(f"Could not check/set headers: {e}")

    def _get_col_index(self, shift_code: str) -> int:
        """Get column index (1-based) for a shift code."""
        if shift_code in self.SHIFT_COLS:
            return self.SHIFT_COLS.index(shift_code) + 2  # +1 for Employee col, +1 for 1-based
        raise ValueError(f"Invalid shift code: {shift_code}")

    def _find_employee_row(self, employee: str) -> Optional[int]:
        """Find the row number for an employee, or None if not found."""
        col_a = self.worksheet.col_values(1)  # Employee names in column A
        for i, name in enumerate(col_a):
            if name == employee:
                return i + 1  # 1-based row number
        return None

    def add_shift_amount(self, employee: str, shift_code: str, amount: float):
        """Add or update an amount for an employee's shift.

        Args:
            employee: Employee name
            shift_code: Shift code (e.g., "MAM", "TPM")
            amount: Dollar amount
        """
        # Find or create employee row
        row_num = self._find_employee_row(employee)

        if row_num is None:
            # Add new employee
            all_values = self.worksheet.get_all_values()
            row_num = len(all_values) + 1

            # Initialize row with employee name and zeros
            new_row = [employee] + [0] * len(self.SHIFT_COLS) + [0]
            self.worksheet.append_row(new_row, value_input_option='USER_ENTERED')
            log.info(f"Added new employee row for {employee} at row {row_num}")

        # Update the specific shift cell
        col_index = self._get_col_index(shift_code)
        self.worksheet.update_cell(row_num, col_index, amount)

        # Recalculate total (sum of columns B through O)
        total_col = len(self.HEADER)  # Last column
        total_formula = f"=SUM(B{row_num}:O{row_num})"
        self.worksheet.update_cell(row_num, total_col, total_formula)

        log.info(f"Updated {employee} {shift_code} = ${amount:.2f}")

    def get_employee_total(self, employee: str) -> float:
        """Get current weekly total for an employee."""
        row_num = self._find_employee_row(employee)
        if row_num is None:
            return 0.0

        total_col = len(self.HEADER)
        value = self.worksheet.cell(row_num, total_col).value
        try:
            return float(value) if value else 0.0
        except ValueError:
            return 0.0

    def get_all_totals(self) -> List[Dict[str, Any]]:
        """Get all employee totals for display.

        Returns:
            List of dicts with keys: name, total, shifts_worked, shifts (dict of code->amount)
        """
        records = self.worksheet.get_all_records()
        results = []

        for record in records:
            employee = record.get("Employee", "")
            if not employee:
                continue

            shifts = {}
            shifts_worked = 0

            for shift_code in self.SHIFT_COLS:
                amount = record.get(shift_code, 0)
                if amount and float(amount) > 0:
                    shifts[shift_code] = float(amount)
                    shifts_worked += 1

            total = record.get("TOTAL", 0)
            try:
                total = float(total) if total else 0.0
            except ValueError:
                total = sum(shifts.values())

            results.append({
                "name": employee,
                "total": total,
                "shifts_worked": shifts_worked,
                "shifts": shifts,
            })

        # Sort by total descending
        results.sort(key=lambda x: x["total"], reverse=True)
        return results

    def clear_all(self):
        """Clear all data except headers (for new pay period)."""
        row_count = len(self.worksheet.get_all_values())
        if row_count > 1:
            self.worksheet.delete_rows(2, row_count)
        log.info("Cleared weekly totals sheet")


# Module-level singleton
_totals_sheet: Optional[WeeklyTotalsSheet] = None


def get_weekly_totals_sheet(sheet_id: Optional[str] = None) -> WeeklyTotalsSheet:
    """Get or create the weekly totals sheet singleton."""
    global _totals_sheet

    if sheet_id:
        return WeeklyTotalsSheet(sheet_id=sheet_id)

    if _totals_sheet is None:
        _totals_sheet = WeeklyTotalsSheet()

    return _totals_sheet
