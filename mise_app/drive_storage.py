"""Google Drive storage for audio recordings."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from io import BytesIO
from typing import Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

log = logging.getLogger(__name__)

# Default folder ID for Payroll Voice Recordings Archive
# This is the "Payroll Voice Recordings Archive" folder in Papa Staff Resources
# Set via DRIVE_ARCHIVE_FOLDER_ID environment variable, or use hardcoded default
DEFAULT_ARCHIVE_FOLDER_ID = os.environ.get(
    'DRIVE_ARCHIVE_FOLDER_ID',
    '1TMDU6H6f5NGOyYNtnOZtawo0-I_IDJOu'  # Papa Staff Resources/Payroll Voice Recordings Archive
)


class DriveClient:
    """Client for uploading files to Google Drive."""

    SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
    ]

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize with service account credentials.

        Args:
            credentials_path: Path to service account JSON file.
                Defaults to ~/.config/mise/sheets_credentials.json
                or SHEETS_CREDENTIALS_PATH env var.
        """
        self._service = None
        self._credentials_path = credentials_path or os.environ.get(
            'SHEETS_CREDENTIALS_PATH',
            os.path.expanduser('~/.config/mise/sheets_credentials.json')
        )

    @property
    def service(self):
        """Lazy-load the Drive service."""
        if self._service is None:
            if not os.path.exists(self._credentials_path):
                log.warning(
                    f"Google Drive credentials not found at: {self._credentials_path}. "
                    "Audio files will not be archived to Drive."
                )
                return None

            creds = Credentials.from_service_account_file(
                self._credentials_path,
                scopes=self.SCOPES
            )
            self._service = build('drive', 'v3', credentials=creds)
            log.info("Google Drive client initialized")

        return self._service

    def upload_audio(
        self,
        audio_bytes: bytes,
        filename: str,
        folder_id: Optional[str] = None,
        mime_type: str = 'audio/webm'
    ) -> Optional[str]:
        """Upload audio file to Google Drive.

        Args:
            audio_bytes: Raw audio bytes
            filename: Name for the file in Drive
            folder_id: Drive folder ID to upload to (uses default archive if not specified)
            mime_type: MIME type of the audio file

        Returns:
            Drive file ID if successful, None if failed
        """
        if self.service is None:
            log.warning("Drive service not available, skipping upload")
            return None

        folder_id = folder_id or DEFAULT_ARCHIVE_FOLDER_ID

        if not folder_id:
            log.warning("No Drive folder ID configured (set DRIVE_ARCHIVE_FOLDER_ID)")
            return None

        try:
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }

            media = MediaIoBaseUpload(
                BytesIO(audio_bytes),
                mimetype=mime_type,
                resumable=True
            )

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()

            log.info(f"📤 Uploaded to Drive: {filename} (ID: {file.get('id')})")
            return file.get('id')

        except Exception as e:
            log.error(f"Failed to upload to Drive: {e}")
            return None

    def get_or_create_period_folder(
        self,
        period_id: str,
        parent_folder_id: Optional[str] = None
    ) -> Optional[str]:
        """Get or create a folder for a pay period.

        Args:
            period_id: Pay period ID (e.g., '2026-01-19')
            parent_folder_id: Parent folder ID (uses default archive if not specified)

        Returns:
            Folder ID if successful, None if failed
        """
        if self.service is None:
            return None

        parent_folder_id = parent_folder_id or DEFAULT_ARCHIVE_FOLDER_ID

        if not parent_folder_id:
            log.warning("No Drive folder ID configured (set DRIVE_ARCHIVE_FOLDER_ID)")
            return None

        try:
            # Check if folder already exists
            query = (
                f"name='{period_id}' and "
                f"'{parent_folder_id}' in parents and "
                f"mimeType='application/vnd.google-apps.folder' and "
                f"trashed=false"
            )
            results = self.service.files().list(
                q=query,
                fields='files(id, name)'
            ).execute()

            files = results.get('files', [])
            if files:
                log.info(f"Found existing folder for {period_id}: {files[0]['id']}")
                return files[0]['id']

            # Create new folder
            folder_metadata = {
                'name': period_id,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]
            }

            folder = self.service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()

            log.info(f"Created new folder for {period_id}: {folder.get('id')}")
            return folder.get('id')

        except Exception as e:
            log.error(f"Failed to get/create period folder: {e}")
            return None


# Module-level singleton
_client: Optional[DriveClient] = None


def get_drive_client(credentials_path: Optional[str] = None) -> DriveClient:
    """Get or create the Drive client singleton."""
    global _client

    if credentials_path:
        return DriveClient(credentials_path)

    if _client is None:
        _client = DriveClient()

    return _client


def upload_recording_to_drive(
    audio_bytes: bytes,
    period_id: str,
    shifty_code: str,
    original_filename: Optional[str] = None
) -> Optional[str]:
    """Upload a recording to Google Drive, organized by pay period.

    Args:
        audio_bytes: Raw audio bytes
        period_id: Pay period ID (e.g., '2026-01-19')
        shifty_code: Shifty code (e.g., 'MAM', 'TPM')
        original_filename: Original filename for extension detection

    Returns:
        Drive file ID if successful, None if failed
    """
    client = get_drive_client()

    # Determine file extension and mime type
    ext = ".webm"
    mime_type = "audio/webm"
    if original_filename:
        if original_filename.endswith(".wav"):
            ext = ".wav"
            mime_type = "audio/wav"
        elif original_filename.endswith(".m4a"):
            ext = ".m4a"
            mime_type = "audio/mp4"
        elif original_filename.endswith(".mp3"):
            ext = ".mp3"
            mime_type = "audio/mpeg"

    # Build filename: {shifty_code}_{timestamp}{ext}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{shifty_code}_{timestamp}{ext}"

    # Get or create period folder
    folder_id = client.get_or_create_period_folder(period_id)

    # Upload to the period folder (or root archive folder if period folder failed)
    return client.upload_audio(audio_bytes, filename, folder_id, mime_type)
