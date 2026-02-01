"""Google Cloud Storage audio file uploads.

Simple module for uploading audio recordings to GCS bucket.
Replaces the Drive upload for Cloud Run deployments.
"""

import logging
import os
from typing import Optional

log = logging.getLogger(__name__)


def upload_audio_to_gcs(
    audio_bytes: bytes,
    period_id: str,
    filename: str,
    bucket_name: str = None,
) -> Optional[str]:
    """Upload audio file to Google Cloud Storage.

    Args:
        audio_bytes: Raw audio bytes
        period_id: Period ID (e.g., '2026-01-31')
        filename: Filename (e.g., 'FPM_20260131_183045.wav')
        bucket_name: GCS bucket name (defaults to ENVIRONMENT variable)

    Returns:
        GCS path (e.g., 'gs://bucket/recordings/2026-01-31/FPM_20260131_183045.wav')
        or None if upload fails
    """
    try:
        from google.cloud import storage

        # Get bucket name from env if not provided
        if not bucket_name:
            bucket_name = os.getenv("GCS_BUCKET_NAME", "mise-production-data")

        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        # Build blob path: recordings/{period_id}/{filename}
        blob_path = f"recordings/{period_id}/{filename}"
        blob = bucket.blob(blob_path)

        # Determine content type
        content_type = "audio/wav"
        if filename.endswith(".webm"):
            content_type = "audio/webm"
        elif filename.endswith(".m4a"):
            content_type = "audio/m4a"
        elif filename.endswith(".mp3"):
            content_type = "audio/mpeg"

        # Upload
        blob.upload_from_string(audio_bytes, content_type=content_type)

        gcs_path = f"gs://{bucket_name}/{blob_path}"
        log.info(f"☁️ ARCHIVED (GCS): {gcs_path} ({len(audio_bytes):,} bytes)")

        return gcs_path

    except Exception as e:
        log.error(f"Failed to upload to GCS: {e}")
        return None
