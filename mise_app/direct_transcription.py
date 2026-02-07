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
    Parse inventory transcript using Claude API directly.

    Args:
        transcript: Transcription text
        category: Inventory category (bar, food, etc.)

    Returns:
        Dict with status and inventory_json
    """
    log.info(f"Parsing {len(transcript)} character transcript with Claude")

    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    # Build system prompt
    system_prompt = f"""You are an expert inventory parser for restaurant operations.

Your task: Convert a voice transcript of inventory counts into structured JSON.

CATEGORY: {category}

OUTPUT FORMAT:
{{
  "category": "{category}",
  "items": [
    {{
      "product_name": "Product Name",
      "quantity": 10,
      "unit": "bottles",
      "conversion": "4-pack",
      "converted_quantity": 40,
      "base_unit": "cans",
      "notes": "",
      "confidence": 0.95,
      "spoken_name": "what was said",
      "needs_review": false
    }}
  ]
}}

RULES:
1. Extract product names, quantities, and units from the transcript
2. ALWAYS use clear product names - NEVER set product_name to "Unknown"
3. Use the spoken product name with proper capitalization (e.g., "Stella Artois Keg", "Kona Big Wave Keg", "30A Beach Blonde Ale Keg")
4. For conversions (e.g., "6 4-packs"), include:
   - quantity: outer quantity (6)
   - unit: outer unit (4-pack)
   - conversion: conversion factor (4-pack)
   - converted_quantity: total base units (24)
   - base_unit: base unit (cans)
5. If no conversion, set converted_quantity = quantity and base_unit = unit
6. Handle ASR errors (e.g., "cab sauv" → "Cabernet Sauvignon")
7. If quantity unclear, set to null and add note
8. DO NOT invent products not in transcript
9. DO NOT use "Unknown" as product_name - always use the actual product name from the transcript
10. CONFIDENCE SCORING - For EVERY item include:
    - confidence: 0.0-1.0 (1.0=exact match, 0.8+=high, 0.5-0.79=medium, <0.5=low)
    - spoken_name: exact text from transcript
    - needs_review: true if confidence < 0.8

Respond ONLY with the JSON, no other text."""

    user_prompt = f"""Parse this inventory transcript into JSON:

TRANSCRIPT:
{transcript}

CATEGORY: {category}

Output JSON only."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            temperature=0.0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        # Extract JSON from response
        response_text = message.content[0].text

        # Parse JSON
        import json
        import re

        # Look for JSON in response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in Claude response")

        json_str = json_match.group(0)
        inventory_json = json.loads(json_str)

        log.info(f"Parsing complete: {len(inventory_json.get('items', []))} items")

        return {
            "status": "success",
            "inventory_json": inventory_json
        }

    except Exception as e:
        log.error(f"Claude parsing failed: {e}")
        return {
            "status": "error",
            "error": str(e)
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
