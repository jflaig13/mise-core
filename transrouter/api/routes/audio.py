"""Audio processing API routes.

Endpoints for uploading audio files, transcribing them, and routing
to the appropriate domain agent.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from ...src.schemas import AudioRequest
from ...src.transrouter_orchestrator import handle_audio_request
from ..auth import require_api_key

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/audio", tags=["Audio"])


# Supported audio formats and their extensions
SUPPORTED_FORMATS = {
    "wav": "wav",
    "wave": "wav",
    "mp3": "mp3",
    "mpeg": "mp3",
    "m4a": "m4a",
    "mp4": "m4a",
    "ogg": "ogg",
    "flac": "flac",
    "webm": "webm",
}

# Default sample rates by format (can be overridden)
DEFAULT_SAMPLE_RATES = {
    "wav": 16000,
    "mp3": 44100,
    "m4a": 44100,
    "ogg": 44100,
    "flac": 44100,
    "webm": 48000,
}


# ============================================================================
# Response Models
# ============================================================================

class AudioProcessResponse(BaseModel):
    """Response from processing an audio file."""

    status: str = Field(..., description="'success' or 'error'")
    domain: Optional[str] = Field(None, description="Detected domain (payroll, inventory, etc.)")
    transcript: Optional[str] = Field(None, description="Transcribed text from audio")
    agent: Optional[str] = Field(None, description="The agent that processed the request")
    approval_json: Optional[Dict[str, Any]] = Field(
        None,
        description="Structured output from the domain agent (e.g., LPM approval JSON)"
    )
    error: Optional[str] = Field(None, description="Error message if status is 'error'")
    errors: Optional[list[str]] = Field(None, description="List of errors if any occurred")
    usage: Optional[Dict[str, int]] = Field(None, description="Token usage if Claude was called")
    corrections: Optional[list[str]] = Field(
        None,
        description="Auto-corrections applied to fix inconsistencies (for audit trail)"
    )
    warnings: Optional[list[str]] = Field(
        None,
        description="Validation warnings that couldn't be auto-corrected"
    )


class AudioErrorResponse(BaseModel):
    """Error response for audio endpoints."""

    status: str = "error"
    error: str
    detail: Optional[str] = None


# ============================================================================
# Helper Functions
# ============================================================================

def detect_audio_format(filename: str, content_type: Optional[str]) -> str:
    """Detect audio format from filename or content type."""
    # Try filename extension first
    if filename:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext in SUPPORTED_FORMATS:
            return SUPPORTED_FORMATS[ext]

    # Try content type
    if content_type:
        # content_type like "audio/wav" or "audio/mpeg"
        subtype = content_type.split("/")[-1].lower()
        if subtype in SUPPORTED_FORMATS:
            return SUPPORTED_FORMATS[subtype]

    # Default to wav
    return "wav"


# ============================================================================
# Endpoints
# ============================================================================

@router.post(
    "/process",
    response_model=AudioProcessResponse,
    responses={
        200: {"description": "Audio processed successfully"},
        400: {"model": AudioErrorResponse, "description": "Invalid audio file"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
        500: {"model": AudioErrorResponse, "description": "Processing error"},
    },
    summary="Process audio file",
    description="""
    Upload an audio file to be transcribed and processed by the appropriate domain agent.

    **Requires authentication**: Include `X-API-Key` header.

    **Supported formats**: WAV, MP3, M4A, OGG, FLAC, WebM

    **Flow**:
    1. Audio is transcribed using Whisper
    2. Transcript is classified to determine domain (payroll, inventory, etc.)
    3. Domain agent processes the transcript
    4. Structured JSON is returned

    **Example**: Upload a payroll voice recording → get back approval JSON with
    calculated tips, totals, and shift breakdowns.
    """
)
async def process_audio(
    file: UploadFile = File(..., description="Audio file to process"),
    sample_rate: Optional[int] = None,
    client: str = Depends(require_api_key),
) -> AudioProcessResponse:
    """Process an uploaded audio file through transcription and domain routing."""

    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Read file contents
    try:
        audio_bytes = await file.read()
    except Exception as e:
        log.error("Failed to read uploaded file: %s", e)
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    # Detect format
    audio_format = detect_audio_format(file.filename, file.content_type)
    actual_sample_rate = sample_rate or DEFAULT_SAMPLE_RATES.get(audio_format, 16000)

    log.info(
        "Processing audio file from client=%s: %s (format=%s, size=%d bytes, sample_rate=%d)",
        client,
        file.filename,
        audio_format,
        len(audio_bytes),
        actual_sample_rate,
    )

    # Create AudioRequest
    audio_request = AudioRequest(
        audio_bytes=audio_bytes,
        audio_format=audio_format,
        sample_rate_hz=actual_sample_rate,
        meta={"filename": file.filename, "content_type": file.content_type},
    )

    # Process through orchestrator
    try:
        response = handle_audio_request(audio_request)
    except Exception as e:
        log.exception("Error processing audio")
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

    # Check for errors
    if response.errors:
        log.warning("Audio processing had errors: %s", response.errors)
        return AudioProcessResponse(
            status="error",
            domain=response.domain,
            transcript=response.transcript,
            error="; ".join(response.errors),
            errors=response.errors,
        )

    # Extract payload
    payload = response.payload or {}

    return AudioProcessResponse(
        status=payload.get("status", "success"),
        domain=response.domain,
        transcript=response.transcript,
        agent=payload.get("agent"),
        approval_json=payload.get("approval_json"),
        error=payload.get("error"),
        usage=payload.get("usage"),
        corrections=payload.get("corrections"),
        warnings=payload.get("warnings"),
    )


@router.post(
    "/transcribe",
    response_model=AudioProcessResponse,
    responses={
        200: {"description": "Audio transcribed successfully"},
        400: {"model": AudioErrorResponse, "description": "Invalid audio file"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
    },
    summary="Transcribe audio only",
    description="""
    Upload an audio file to be transcribed. Unlike `/process`, this does NOT
    route to a domain agent - it only returns the transcript.

    **Requires authentication**: Include `X-API-Key` header.

    Use this for:
    - Testing transcription quality
    - Getting raw transcript before processing
    - Non-domain-specific audio
    """
)
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe"),
    sample_rate: Optional[int] = None,
    client: str = Depends(require_api_key),
) -> AudioProcessResponse:
    """Transcribe audio without domain processing."""
    from ...src.asr_adapter import get_asr_provider
    from ...src.schemas import TranscriptResult

    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    try:
        audio_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    audio_format = detect_audio_format(file.filename, file.content_type)
    actual_sample_rate = sample_rate or DEFAULT_SAMPLE_RATES.get(audio_format, 16000)

    log.info(
        "Transcribing audio file from client=%s: %s (format=%s, size=%d bytes)",
        client,
        file.filename,
        audio_format,
        len(audio_bytes),
    )

    try:
        provider = get_asr_provider()
        result: TranscriptResult = provider.transcribe(
            audio_bytes, audio_format, actual_sample_rate
        )
    except Exception as e:
        log.exception("Transcription failed")
        return AudioProcessResponse(
            status="error",
            error=f"Transcription failed: {e}",
        )

    return AudioProcessResponse(
        status="success",
        transcript=result.transcript,
    )
