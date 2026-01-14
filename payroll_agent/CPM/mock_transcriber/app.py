"""
Mock transcriber service for local CPM testing.

Returns pre-recorded transcripts from fixture files based on audio filename.
Eliminates dependency on real transcription service during local development.
"""

import json
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Mock Transcriber")

# Load fixtures on startup
FIXTURES = {}
FIXTURES_DIR = Path("/app/fixtures")


class TranscriptResponse(BaseModel):
    text: str
    language: Optional[str] = "en"


@app.on_event("startup")
def load_fixtures():
    """Load all JSON fixture files into memory."""
    if not FIXTURES_DIR.exists():
        print(f"⚠️  Fixtures directory not found: {FIXTURES_DIR}")
        return

    for fixture_file in FIXTURES_DIR.glob("*.json"):
        try:
            with open(fixture_file, "r") as f:
                data = json.load(f)
                # Use filename stem as key (e.g., "monday_am_simple")
                fixture_name = fixture_file.stem
                FIXTURES[fixture_name] = data
                print(f"✓ Loaded fixture: {fixture_name}")
        except Exception as e:
            print(f"✗ Failed to load {fixture_file}: {e}")

    print(f"\n📦 Loaded {len(FIXTURES)} fixtures total")


@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "ok": True,
        "service": "mock_transcriber",
        "fixtures_loaded": len(FIXTURES),
    }


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)) -> TranscriptResponse:
    """
    Mock transcription endpoint.

    Matches audio filename to fixture files and returns the pre-recorded transcript.
    If no match is found, returns a generic test transcript.
    """
    filename = audio.filename or "unknown.wav"
    filename_stem = Path(filename).stem  # Remove extension

    # Try to find matching fixture
    if filename_stem in FIXTURES:
        fixture = FIXTURES[filename_stem]
        transcript = fixture.get("transcript", "")
        print(f"✓ Matched fixture: {filename_stem}")
        return TranscriptResponse(text=transcript)

    # Try partial matches (e.g., "monday_am" matches "monday_am_simple")
    for fixture_name, fixture_data in FIXTURES.items():
        if filename_stem in fixture_name or fixture_name in filename_stem:
            transcript = fixture_data.get("transcript", "")
            print(f"✓ Partial match: {filename_stem} → {fixture_name}")
            return TranscriptResponse(text=transcript)

    # No match found - return default test transcript
    print(f"⚠️  No fixture match for: {filename_stem}")
    default_transcript = (
        "Monday December 9th, 2025. AM shift. "
        "Servers Mike Walton $300.67, John Neal $250.45."
    )
    return TranscriptResponse(text=default_transcript)


@app.get("/")
def root():
    """Root endpoint with usage info."""
    return {
        "service": "mock_transcriber",
        "fixtures_loaded": list(FIXTURES.keys()),
        "usage": "POST /transcribe with audio file",
    }
