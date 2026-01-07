# Cloud Payroll Machine (CPM)

Purpose
- Fully automated cloud workflow for ingesting server payroll audio in real time.
- Handles audio ingestion → Whisper transcription → LLM cleanup → parsing/normalization → validation → shift object construction → BigQuery writes.
- Production-intended, continuously running cloud-facing system.

Repo Location
- engine/
  - payroll_engine.py (primary entrypoint)
  - parse_only.py, commit_shift.py, parse_shift.py
  - normalizer.py, tokenizer.py, validator.py
  - schemas/payroll_schema.json
- transcribe/
  - app.py (Whisper service), requirements.txt, Dockerfile
  - cleanup/llm_cleanup.py (LLM transcript normalization)
- scripts/: check_shift.sh, test_transcript.sh, test_transcript_archive.sh, convert_m4a_to_wav.sh

Primary Entry Points
- Cloud Run: Transcribe Service — `transcribe/app.py`
  - Accepts audio uploads, converts .m4a→.wav, runs Whisper base.en
  - Sends raw Whisper output through LLM cleanup layer (cleanup/llm_cleanup.py)
  - LLM cleanup normalizes transcript for better parsing (fixes typos, standardizes formatting)
  - Returns cleaned transcript text to caller
- Cloud Run: Payroll Engine — `engine/payroll_engine.py` (replaces app.py)
  - `/parse_only`: transcript → structured rows (servers, supports, amounts)
  - `/commit_shift`: validates shift & writes to BigQuery
  - Supporting modules: normalizer.py, tokenizer.py, validator.py, parse_shift.py, schemas/payroll_schema.json

LLM Cleanup Layer
- Inserted between Whisper transcription and engine parsing (December 2025)
- Location: `transcribe/cleanup/llm_cleanup.py`
- Purpose: Normalizes Whisper output before parsing to improve accuracy
  - Fixes common transcription errors and typos
  - Standardizes date/time formatting
  - Corrects obvious mistakes (e.g., "December 9th 2025" vs "December 9th, 2025")
- Integration: Called automatically in `transcribe/app.py` after Whisper completes
- Graceful degradation: Falls back to raw Whisper text if LLM cleanup service unavailable
- Uses Claude API (Haiku model) for fast, cost-effective normalization

Audio File Conventions
- Filenames: `MMDDYY_MMDDYY` (no employee names/timestamps)
  - First date = payroll period start; second = payroll period end (e.g., 111025_111625).

Key Inputs
- .m4a or .wav audio file
- Whisper transcript from transcribe service
- Parsing directives inside CPM
- Local note: `transcribe` relies on `.venv/bin/whisper`; if missing on a fresh machine, run `.venv/bin/pip install openai-whisper`.

Key Outputs
- Shift JSON conforming to `schemas/payroll_schema.json`
- Rows written to BigQuery (shifts table + linked views)
- Parsed data feeding dashboards/operational reporting

Environment Variables
- GOOGLE_APPLICATION_CREDENTIALS
- PROJECT_ID
- BIGQUERY_DATASET
- BIGQUERY_TABLE
- TRANSCRIBE_URL
- ENGINE_URL
- REGION

Notes
- Architecture reflects repo consolidation and the new filename behavior.
- Clear division between transcribe service and engine service.
