"""Compatibility shim for the parse-only endpoint.

The new home for this router is ``engine.parse_shift``. Keeping this import path
alive avoids breaking existing callers while the migration is underway.
"""

from .parse_shift import *  # noqa: F401,F403

@router.post("/parse_only")
async def parse_only_endpoint(
    audio: UploadFile = File(...),
    filename: str = Form(...),
):
    """Transcribe audio and return parsed shift rows as a preview.
    Does NOT write anything to BigQuery.
    """
    # Import inside the function to avoid circular imports at module load time
    from .payroll_engine import transcribe_audio, parse_transcript_to_rows, TranscriptIn

    # Transcribe and clean the audio via the transcriber service
    cleaned_transcript = await transcribe_audio(audio)

    # Build payload for the parser
    payload = TranscriptIn(
        filename=filename or (audio.filename or "shift.wav"),
        transcript=cleaned_transcript,
    )

    # Parse into structured rows
    rows = parse_transcript_to_rows(payload)

    return {
        "filename": payload.filename,
        "transcript": cleaned_transcript,
        "rows": [r.dict() for r in rows],
    }
