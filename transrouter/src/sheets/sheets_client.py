"""Google Sheets client for Shifty approval workflow."""

from __future__ import annotations

import logging
import os
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

log = logging.getLogger(__name__)


class SheetsClient:
    """Client for interacting with Google Sheets API.

    Usage:
        client = SheetsClient()
        sheet = client.get_sheet("1abc...")
        worksheet = sheet.sheet1
        worksheet.append_row(["data", "here"])
    """

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
    ]

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize with service account credentials.

        Args:
            credentials_path: Path to service account JSON file.
                Defaults to ~/.config/mise/sheets_credentials.json
                or SHEETS_CREDENTIALS_PATH env var.
        """
        self._gc: Optional[gspread.Client] = None
        self._credentials_path = credentials_path or os.environ.get(
            'SHEETS_CREDENTIALS_PATH',
            os.path.expanduser('~/.config/mise/sheets_credentials.json')
        )

    @property
    def gc(self) -> gspread.Client:
        """Lazy-load the gspread client."""
        if self._gc is None:
            if not os.path.exists(self._credentials_path):
                raise FileNotFoundError(
                    f"Google Sheets credentials not found at: {self._credentials_path}\n"
                    "Please create a service account and download the JSON key."
                )

            creds = Credentials.from_service_account_file(
                self._credentials_path,
                scopes=self.SCOPES
            )
            self._gc = gspread.authorize(creds)
            log.info("Google Sheets client initialized")

        return self._gc

    def get_sheet(self, sheet_id: str) -> gspread.Spreadsheet:
        """Get a spreadsheet by ID.

        Args:
            sheet_id: The spreadsheet ID from the URL
                (e.g., https://docs.google.com/spreadsheets/d/{sheet_id}/edit)

        Returns:
            gspread Spreadsheet object
        """
        return self.gc.open_by_key(sheet_id)

    def get_service_account_email(self) -> str:
        """Get the service account email for sharing sheets."""
        return self.gc.auth.service_account_email


# Module-level singleton
_client: Optional[SheetsClient] = None


def get_sheets_client(credentials_path: Optional[str] = None) -> SheetsClient:
    """Get or create the sheets client singleton."""
    global _client

    if credentials_path:
        return SheetsClient(credentials_path)

    if _client is None:
        _client = SheetsClient()

    return _client
