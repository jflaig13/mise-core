"""
Direct transcription and parsing for large inventory files.

Bypasses transrouter for files >32MB by calling Google Speech-to-Text
and Claude API directly.
"""

import logging
from typing import Dict, Any, Optional
from google.cloud import speech_v1
from google.cloud import storage as gcs
import anthropic
import os

log = logging.getLogger(__name__)


def transcribe_large_audio_from_gcs(gcs_path: str) -> str:
    """
    Transcribe audio file from GCS using Google Cloud Speech-to-Text.

    Uses long-running recognize for files of any size.

    Args:
        gcs_path: GCS path like "gs://bucket/path/to/file.wav"

    Returns:
        Transcription text
    """
    log.info(f"Starting GCS transcription for {gcs_path}")

    client = speech_v1.SpeechClient()

    audio = speech_v1.RecognitionAudio(uri=gcs_path)

    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        model="default",
        use_enhanced=True,
    )

    # Use long-running recognize for large files
    operation = client.long_running_recognize(config=config, audio=audio)

    log.info(f"Waiting for transcription operation to complete (this may take several minutes)...")
    response = operation.result(timeout=600)  # 10 minute timeout

    # Concatenate all results
    transcript = ""
    for result in response.results:
        # Get the first alternative (most confident)
        transcript += result.alternatives[0].transcript + " "

    log.info(f"Transcription complete: {len(transcript)} characters")
    return transcript.strip()


def parse_inventory_with_claude(transcript: str, category: str = "bar") -> Dict[str, Any]:
    """
    Parse inventory transcript using the InventoryAgent directly.

    Previously called Claude API directly with a duplicate prompt. Now delegates
    to InventoryAgent.process_text() which uses the canonical
    InventoryAgent with the full product catalog and manual mappings.

    Args:
        transcript: Transcription text
        category: Inventory category (bar, food, etc.)

    Returns:
        Dict with status and inventory_json
    """
    log.info(f"Parsing {len(transcript)} character transcript via InventoryAgent")

    try:
        from transrouter.src.agents.inventory_agent import get_agent as get_inventory_agent
        result = get_inventory_agent().process_text(transcript, category)

        if result.get("status") == "success":
            return {
                "status": "success",
                "inventory_json": result.get("approval_json", {}),
            }
        else:
            return {
                "status": "error",
                "error": result.get("error", "Inventory parsing failed"),
            }

    except Exception as e:
        log.error(f"Inventory agent parsing failed: {e}")
        return {
            "status": "error",
            "error": str(e),
        }


def process_large_inventory_file(gcs_path: str, category: str = "bar") -> Dict[str, Any]:
    """
    Process a large inventory file directly (bypassing transrouter).

    1. Transcribe audio from GCS using Google Speech-to-Text
    2. Parse with Claude API directly

    Args:
        gcs_path: GCS path to audio file
        category: Inventory category

    Returns:
        Dict with status, transcript, and inventory_json
    """
    try:
        # Step 1: Transcribe
        transcript = transcribe_large_audio_from_gcs(gcs_path)

        if not transcript:
            return {
                "status": "error",
                "error": "Transcription returned empty result"
            }

        # Step 2: Parse with Claude
        parse_result = parse_inventory_with_claude(transcript, category)

        if parse_result["status"] != "success":
            return parse_result

        # Return combined result
        return {
            "status": "success",
            "transcript": transcript,
            "approval_json": parse_result["inventory_json"]
        }

    except Exception as e:
        log.error(f"Large file processing failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
