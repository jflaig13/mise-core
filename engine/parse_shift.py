from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()


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

    # Transcribe the audio via the transcriber service
    transcript = await transcribe_audio(audio)

    # Build payload for the parser
    payload = TranscriptIn(
        filename=filename or (audio.filename or "shift.wav"),
        transcript=transcript,
    )

    # Parse into structured rows
    rows = parse_transcript_to_rows(payload)

    return {
        "filename": payload.filename,
        "transcript": transcript,
        "rows": [r.dict() for r in rows],
    }
