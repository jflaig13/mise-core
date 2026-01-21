"""Recording and processing routes for Shifty app."""

from __future__ import annotations

import logging
import os
import re
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional

import requests
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from mise_app.config import SHIFTY_DEFINITIONS, get_shifty_by_code, PayPeriod
from mise_app.local_storage import get_approval_storage, get_totals_storage
from mise_app.drive_storage import upload_recording_to_drive

log = logging.getLogger(__name__)

# Recordings storage directory
RECORDINGS_DIR = Path(__file__).parent.parent.parent / "recordings"


def save_recording(audio_bytes: bytes, period_id: str, shifty_code: str = None, original_filename: str = None) -> Path:
    """ARCHIVE audio recording - PERMANENT STORAGE, NEVER DELETE.

    Every audio file ever recorded in Mise is saved here for:
    - Audit trail
    - Dispute resolution
    - Re-processing if needed
    - Historical analysis

    Saves to:
    1. Local filesystem (for local dev)
    2. Google Drive (for cloud persistence)

    Organized by pay period for easy retrieval.

    Args:
        audio_bytes: The raw audio bytes
        period_id: Pay period ID (e.g., '2025-01-12')
        shifty_code: Optional shifty code if known (e.g., 'MAM', 'TPM')
        original_filename: Original filename from upload

    Returns:
        Path to the saved file (local)
    """
    # Create period-specific archive directory
    period_dir = RECORDINGS_DIR / period_id
    period_dir.mkdir(parents=True, exist_ok=True)

    # Determine file extension
    ext = ".webm"  # Default for browser recordings
    if original_filename:
        if original_filename.endswith(".wav"):
            ext = ".wav"
        elif original_filename.endswith(".m4a"):
            ext = ".m4a"
        elif original_filename.endswith(".mp3"):
            ext = ".mp3"

    # Build filename: {shifty_code}_{timestamp}{ext}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if shifty_code:
        filename = f"{shifty_code}_{timestamp}{ext}"
    else:
        filename = f"unknown_{timestamp}{ext}"

    filepath = period_dir / filename
    filepath.write_bytes(audio_bytes)

    log.info(f"📼 ARCHIVED (local): {filepath.relative_to(RECORDINGS_DIR.parent)} ({len(audio_bytes):,} bytes)")

    # Also upload to Google Drive for permanent cloud storage
    try:
        drive_file_id = upload_recording_to_drive(
            audio_bytes, period_id, shifty_code or "unknown", original_filename
        )
        if drive_file_id:
            log.info(f"☁️ ARCHIVED (Drive): {filename} -> {drive_file_id}")
    except Exception as e:
        log.warning(f"Failed to upload to Drive (continuing anyway): {e}")

    return filepath

router = APIRouter(prefix="/payroll/period/{period_id}", tags=["Payroll Recording"])


def detect_shifty_from_transcript(transcript: str, period: PayPeriod) -> dict:
    """Detect the shifty code and actual date from transcript content.

    Looks for patterns like:
    - "Monday AM" / "Monday PM"
    - "Tuesday morning" / "Tuesday night"
    - "January 19th, 2026 AM shift"
    - "01/15 AM shift"

    Returns:
        dict with keys:
        - 'code': shifty code (e.g., 'MAM', 'TPM') or None
        - 'parsed_date': the actual date parsed from transcript, or None
    """
    transcript_lower = transcript.lower()
    parsed_date_result = None  # Track the actual date parsed

    # Day name mappings
    day_prefixes = {
        "monday": "M", "mon": "M",
        "tuesday": "T", "tue": "T", "tues": "T",
        "wednesday": "W", "wed": "W",
        "thursday": "Th", "thu": "Th", "thur": "Th", "thurs": "Th",
        "friday": "F", "fri": "F",
        "saturday": "Sa", "sat": "Sa",
        "sunday": "Su", "sun": "Su",
    }

    # Shift mappings
    am_indicators = ["a.m.", "am", "morning", "lunch", "day shift", "day"]
    pm_indicators = ["p.m.", "pm", "evening", "night", "dinner", "closing", "close"]

    detected_day = None
    detected_shift = None

    # Try to find day of week
    for day_word, prefix in day_prefixes.items():
        if day_word in transcript_lower:
            detected_day = prefix
            break

    # Try to find AM/PM
    for indicator in am_indicators:
        if indicator in transcript_lower:
            # For indicators with periods (a.m., p.m.), direct match is sufficient
            # For short ones (am, pm), use word boundary to avoid matching "dam", "spam", etc.
            if '.' in indicator:
                detected_shift = "AM"
                break
            else:
                pattern = r'\b' + re.escape(indicator) + r'\b'
                if re.search(pattern, transcript_lower):
                    detected_shift = "AM"
                    break

    if not detected_shift:
        for indicator in pm_indicators:
            if indicator in transcript_lower:
                if '.' in indicator:
                    detected_shift = "PM"
                    break
                else:
                    pattern = r'\b' + re.escape(indicator) + r'\b'
                    if re.search(pattern, transcript_lower):
                        detected_shift = "PM"
                        break

    # Try to find date from transcript (always try, for pay period auto-correction)
    # Month name mappings
    month_names = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9, "sept": 9,
        "october": 10, "oct": 10,
        "november": 11, "nov": 11,
        "december": 12, "dec": 12,
    }

    # Always try to parse a date for pay period auto-correction
    for month_word, month_num in month_names.items():
        # Match "January 19th" or "January 19"
        pattern = rf'\b{month_word}\s+(\d{{1,2}})(?:st|nd|rd|th)?\b'
        match = re.search(pattern, transcript_lower)
        if match:
            day_num = int(match.group(1))
            try:
                # Try to extract year from transcript (e.g., "January 12, 2026")
                year_pattern = rf'\b{month_word}\s+\d{{1,2}}(?:st|nd|rd|th)?(?:\s*,)?\s*(\d{{4}})\b'
                year_match = re.search(year_pattern, transcript_lower)
                if year_match:
                    year = int(year_match.group(1))
                else:
                    # Default to pay period year
                    year = period.start_date.year
                    # If month is less than period start month and we're near year boundary, use next year
                    if month_num < period.start_date.month and period.start_date.month >= 11:
                        year += 1
                parsed_date = date(year, month_num, day_num)
                parsed_date_result = parsed_date  # Store the actual parsed date
                # If we didn't already detect the day from a day name, use the parsed date
                if not detected_day:
                    day_names = ["M", "T", "W", "Th", "F", "Sa", "Su"]
                    detected_day = day_names[parsed_date.weekday()]
                log.info(f"Parsed date from transcript: {month_word} {day_num}, {year} -> {parsed_date.strftime('%A %B %d, %Y')}")
            except ValueError:
                pass
            break

    # Fallback: Try MM/DD format if no date found yet
    if not parsed_date_result:
        date_match = re.search(r'(\d{1,2})[/\-](\d{1,2})', transcript_lower)
        if date_match:
            month = int(date_match.group(1))
            day = int(date_match.group(2))
            try:
                parsed_date = date(period.start_date.year, month, day)
                parsed_date_result = parsed_date
                if not detected_day:
                    day_names = ["M", "T", "W", "Th", "F", "Sa", "Su"]
                    detected_day = day_names[parsed_date.weekday()]
            except ValueError:
                pass

    # Build shifty code and return with parsed date
    shifty_code = None
    if detected_day and detected_shift:
        shifty_code = f"{detected_day}{detected_shift}"

    return {
        "code": shifty_code,
        "parsed_date": parsed_date_result
    }


def get_shifty_date(shifty_code: str, period: PayPeriod) -> Optional[date]:
    """Get the actual date for a shifty code within a pay period."""
    try:
        shifty = get_shifty_by_code(shifty_code)
        return period.start_date + timedelta(days=shifty["date_offset"])
    except ValueError:
        return None


def fix_approval_json_shift_codes(approval_json: dict, correct_shifty_code: str) -> dict:
    """Fix shift codes in approval_json if Claude calculated wrong day of week.

    Claude sometimes miscalculates day-of-week (e.g., thinks Jan 19 2026 is Sunday
    when it's actually Monday). This causes amounts to be stored under wrong shift
    codes (e.g., SuPM instead of MPM).

    This function remaps all shift codes in per_shift to the correct one detected
    by mise-app from the actual date.

    Args:
        approval_json: The approval JSON from transrouter
        correct_shifty_code: The correct shift code (e.g., "MPM") from date detection

    Returns:
        Fixed approval_json with corrected shift codes
    """
    if not approval_json or not correct_shifty_code:
        return approval_json

    # All valid shift codes
    all_shift_codes = [
        "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
        "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM", "SuAM", "SuPM"
    ]

    # Fix per_shift: remap any wrong shift codes to the correct one
    per_shift = approval_json.get("per_shift", {})
    fixed_per_shift = {}

    for employee, shifts in per_shift.items():
        fixed_shifts = {}
        for shift_code, amount in shifts.items():
            if shift_code in all_shift_codes and shift_code != correct_shifty_code:
                # This is a wrong shift code - remap to correct one
                log.info(f"Fixing shift code for {employee}: {shift_code} → {correct_shifty_code}")
                fixed_shifts[correct_shifty_code] = amount
            else:
                fixed_shifts[shift_code] = amount
        fixed_per_shift[employee] = fixed_shifts

    approval_json["per_shift"] = fixed_per_shift

    # Recalculate weekly_totals from fixed per_shift
    weekly_totals = {}
    for employee, shifts in fixed_per_shift.items():
        weekly_totals[employee] = round(sum(shifts.values()), 2)
    approval_json["weekly_totals"] = weekly_totals

    return approval_json


@router.get("/record/{shifty_code}")
async def record_page(request: Request, period_id: str, shifty_code: str):
    """Redirect to main recording page (legacy route for re-recording)."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(f"/payroll/period/{period_id}", status_code=303)


@router.post("/process")
async def process_audio(
    request: Request,
    period_id: str,
    file: UploadFile = File(...),
):
    """Process an uploaded audio file and detect shifty from transcript.

    This is the primary endpoint - no pre-selection of day/shift required.
    Mise detects the date and shift from the transcript content.
    """
    config = request.app.state.config
    shifty_state = request.app.state.shifty_state

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return JSONResponse(
            {"status": "error", "error": f"Invalid pay period: {period_id}"},
            status_code=400
        )

    log.info(f"Processing audio for period {period_id} from file {file.filename}")

    # Read audio bytes
    audio_bytes = await file.read()
    log.info(f"Audio bytes received: {len(audio_bytes)} bytes")
    if not audio_bytes:
        log.error("Empty audio file received")
        return JSONResponse(
            {"status": "error", "error": "Empty audio file"},
            status_code=400
        )

    # Call transrouter API
    log.info(f"Calling transrouter at {config.transrouter_url}/api/v1/audio/process")
    try:
        response = requests.post(
            f"{config.transrouter_url}/api/v1/audio/process",
            headers={"X-API-Key": config.transrouter_api_key},
            files={"file": ("recording.wav", audio_bytes, "audio/wav")},
            timeout=120,
        )
        log.info(f"Transrouter response status: {response.status_code}")
        response.raise_for_status()
        result = response.json()
        log.info(f"Transrouter result status: {result.get('status')}")
    except requests.RequestException as e:
        log.error(f"Transrouter API error: {e}")
        return JSONResponse(
            {"status": "error", "error": f"API error: {e}"},
            status_code=500
        )

    if result.get("status") != "success":
        error = result.get("error", "Unknown error")
        log.error(f"Processing failed: {error}")
        return JSONResponse(
            {"status": "error", "error": error},
            status_code=400
        )

    # Get transcript and approval JSON
    transcript = result.get("transcript", "")
    approval_json = result.get("approval_json", {})

    log.info(f"Transcript received: '{transcript}'")

    # Detect shifty code and parsed date from transcript
    detection_result = detect_shifty_from_transcript(transcript, period)
    log.info(f"Detection result: {detection_result}")
    shifty_code = detection_result.get("code")
    parsed_date = detection_result.get("parsed_date")

    if not shifty_code:
        # Fallback: try to get from approval_json if Transrouter detected it
        detected_shift = approval_json.get("detected_shift", {})
        if detected_shift.get("code"):
            shifty_code = detected_shift["code"]

    if not shifty_code:
        log.error("Could not detect shifty from transcript")
        return JSONResponse(
            {"status": "error", "error": "Could not detect date/shift from recording. Please say the day and AM/PM clearly."},
            status_code=400
        )

    # If a specific date was parsed, use it to determine the correct pay period
    parsed_date_str = None
    if parsed_date:
        parsed_date_str = parsed_date.strftime("%m/%d/%Y")
        # Find the correct pay period for this date
        correct_period = PayPeriod.containing(parsed_date)
        if correct_period.id != period_id:
            log.info(f"Date {parsed_date_str} belongs to period {correct_period.id}, not {period_id} - auto-correcting")
            period = correct_period
            period_id = correct_period.id
        log.info(f"Detected shifty {shifty_code} for date {parsed_date_str} in period {period_id}")
    else:
        log.info(f"Detected shifty {shifty_code} from transcript (no specific date parsed, using period {period_id})")

    # Save recording to local storage
    save_recording(audio_bytes, period_id, shifty_code, file.filename)

    # Fix approval_json shift codes if Claude calculated wrong day of week
    # Claude sometimes gets day-of-week wrong (e.g., thinks Jan 19 2026 is Sunday when it's Monday)
    approval_json = fix_approval_json_shift_codes(approval_json, shifty_code)

    # Convert approval_json to flat rows
    log.info(f"Approval JSON from transrouter: {approval_json}")
    rows = flatten_approval_json(approval_json, shifty_code, period)
    log.info(f"Flattened rows: {rows}")

    # Store locally (with period isolation) - include parsed_date and detail_blocks
    filename = f"{shifty_code}.wav"
    approval_storage = get_approval_storage()

    # Delete any existing data for this shifty (in case of re-recording)
    approval_storage.delete_by_filename(period_id, filename)

    # Get detail_blocks for calculation display
    detail_blocks = approval_json.get("detail_blocks", [])

    # Add the new data
    approval_storage.add_shifty(period_id, rows, filename, transcript, parsed_date_str, detail_blocks)

    # Update shifty status
    shifty_state.set_status(period_id, shifty_code, "pending")

    # Return data for approval page
    return JSONResponse({
        "status": "success",
        "shifty_code": shifty_code,
        "transcript": transcript,
        "rows": rows,
        "parsed_date": parsed_date_str,
        "corrections": result.get("corrections"),
        "redirect_url": f"/payroll/period/{period_id}/approve/{shifty_code}",
    })


@router.post("/process/{shifty_code}")
async def process_shifty(
    request: Request,
    period_id: str,
    shifty_code: str,
    file: UploadFile = File(...),
):
    """Process an uploaded audio file for a specific shifty (legacy endpoint)."""
    config = request.app.state.config
    shifty_state = request.app.state.shifty_state

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return JSONResponse(
            {"status": "error", "error": f"Invalid pay period: {period_id}"},
            status_code=400
        )

    log.info(f"Processing shifty {shifty_code} for period {period_id} from file {file.filename}")

    # Read audio bytes
    audio_bytes = await file.read()
    if not audio_bytes:
        return JSONResponse(
            {"status": "error", "error": "Empty audio file"},
            status_code=400
        )

    # Call transrouter API
    try:
        response = requests.post(
            f"{config.transrouter_url}/api/v1/audio/process",
            headers={"X-API-Key": config.transrouter_api_key},
            files={"file": (f"{shifty_code}.wav", audio_bytes, "audio/wav")},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        log.error(f"Transrouter API error: {e}")
        return JSONResponse(
            {"status": "error", "error": f"API error: {e}"},
            status_code=500
        )

    if result.get("status") != "success":
        error = result.get("error", "Unknown error")
        log.error(f"Processing failed: {error}")
        return JSONResponse(
            {"status": "error", "error": error},
            status_code=400
        )

    # Get transcript and approval JSON
    transcript = result.get("transcript", "")
    approval_json = result.get("approval_json", {})

    log.info(f"Parsed shifty {shifty_code}: transcript length={len(transcript)}")

    # Save recording to local storage
    save_recording(audio_bytes, period_id, shifty_code, file.filename)

    # Convert approval_json to flat rows
    rows = flatten_approval_json(approval_json, shifty_code, period)

    # Store locally (with period isolation)
    filename = f"{shifty_code}.wav"
    approval_storage = get_approval_storage()

    # Delete any existing data for this shifty (in case of re-recording)
    approval_storage.delete_by_filename(period_id, filename)

    # Get detail_blocks for calculation display
    detail_blocks = approval_json.get("detail_blocks", [])

    # Add the new data
    approval_storage.add_shifty(period_id, rows, filename, transcript, None, detail_blocks)

    # Update shifty status
    shifty_state.set_status(period_id, shifty_code, "pending")

    # Return data for approval page
    return JSONResponse({
        "status": "success",
        "shifty_code": shifty_code,
        "transcript": transcript,
        "rows": rows,
        "corrections": result.get("corrections"),
        "redirect_url": f"/payroll/period/{period_id}/approve/{shifty_code}",
    })


@router.get("/approve/{shifty_code}", response_class=HTMLResponse)
async def approve_page(request: Request, period_id: str, shifty_code: str):
    """Show approval page for a shifty."""
    templates = request.app.state.templates

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse(f"Invalid pay period: {period_id}", status_code=404)

    try:
        shifty = get_shifty_by_code(shifty_code)
    except ValueError:
        return HTMLResponse(f"Unknown shifty code: {shifty_code}", status_code=404)

    # Get data from local storage (with period isolation)
    filename = f"{shifty_code}.wav"
    approval_storage = get_approval_storage()
    rows = approval_storage.get_by_filename(period_id, filename)

    # Get transcript, parsed date, and detail_blocks from first row
    # All three are stored on the first row only (see local_storage.py add_shifty)
    transcript = ""
    parsed_date_str = ""
    detail_blocks = []

    if rows:
        first_row = rows[0]
        transcript = first_row.get("Transcript", "")
        parsed_date_str = first_row.get("ParsedDate", "")

        if first_row.get("DetailBlocks"):
            try:
                import json
                detail_blocks = json.loads(first_row["DetailBlocks"])
            except (json.JSONDecodeError, TypeError):
                detail_blocks = []

    # Use parsed date from transcript if available, otherwise calculate from period
    if parsed_date_str:
        shifty_date_display = parsed_date_str
    else:
        shifty_date = period.start_date + timedelta(days=shifty["date_offset"])
        shifty_date_display = shifty_date.strftime("%m/%d/%Y")

    return templates.TemplateResponse(
        "approve.html",
        {
            "request": request,
            "period": period,
            "periods": PayPeriod.get_available_periods(),
            "shifty": shifty,
            "shifty_code": shifty_code,
            "shifty_date": shifty_date_display,
            "pay_period": period.label,
            "rows": rows,
            "transcript": transcript,
            "detail_blocks": detail_blocks,
            "active_tab": "shifties",
        }
    )


@router.post("/approve/{shifty_code}/confirm")
async def confirm_approval(request: Request, period_id: str, shifty_code: str):
    """Confirm approval of a shifty."""
    shifty_state = request.app.state.shifty_state

    filename = f"{shifty_code}.wav"
    approval_storage = get_approval_storage()
    totals_storage = get_totals_storage()

    # Get form data (in case user edited amounts)
    form_data = await request.form()

    # Update any edited amounts (with period isolation)
    rows = approval_storage.get_by_filename(period_id, filename)
    for row in rows:
        row_id = row.get("id")
        amount_key = f"amount_{row_id}"
        if amount_key in form_data:
            try:
                new_amount = float(form_data[amount_key])
                if new_amount != row.get("Amount"):
                    approval_storage.update_row(period_id, row_id, {"Amount": new_amount})
                    row["Amount"] = new_amount
                    log.info(f"Updated {row.get('Employee')} amount to ${new_amount:.2f}")
            except ValueError:
                pass

    # Approve all rows
    approval_storage.approve_all(period_id, filename)

    # Update weekly totals (with period isolation)
    approved_rows = approval_storage.get_approved_data(period_id, filename)
    for row in approved_rows:
        employee = row.get("Employee", "")
        amount = float(row.get("Amount", 0))
        if employee and amount > 0:
            totals_storage.add_shift_amount(period_id, employee, shifty_code, amount)

    # Mark shifty complete
    shifty_state.set_status(period_id, shifty_code, "complete")
    log.info(f"Approved and completed {shifty_code} for period {period_id}")

    return RedirectResponse(f"/payroll/period/{period_id}", status_code=303)


@router.get("/approved/{filename}")
async def handle_legacy_approval(request: Request, period_id: str, filename: str):
    """Legacy endpoint - redirect to new approval flow."""
    shifty_code = filename.replace(".wav", "")
    return RedirectResponse(f"/payroll/period/{period_id}/approve/{shifty_code}", status_code=303)


@router.get("/detail/{shifty_code}", response_class=HTMLResponse)
async def detail_page(request: Request, period_id: str, shifty_code: str):
    """Show detail page for a completed shifty."""
    templates = request.app.state.templates

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse(f"Invalid pay period: {period_id}", status_code=404)

    try:
        shifty = get_shifty_by_code(shifty_code)
    except ValueError:
        return HTMLResponse(f"Unknown shifty code: {shifty_code}", status_code=404)

    # Get data from local storage (with period isolation)
    filename = f"{shifty_code}.wav"
    approval_storage = get_approval_storage()
    rows = approval_storage.get_approved_data(period_id, filename)

    # Get transcript from first row
    transcript = ""
    for row in rows:
        if row.get("Transcript"):
            transcript = row["Transcript"]
            break

    shifty_date = period.start_date + timedelta(days=shifty["date_offset"])

    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "period": period,
            "periods": PayPeriod.get_available_periods(),
            "shifty": shifty,
            "shifty_code": shifty_code,
            "shifty_date": shifty_date.strftime("%m/%d/%Y"),
            "pay_period": period.label,
            "rows": rows,
            "transcript": transcript,
            "active_tab": "shifties",
        }
    )


def flatten_approval_json(approval_json: dict, shifty_code: str, period: PayPeriod) -> list:
    """Convert approval JSON to flat rows."""
    import re
    rows = []

    try:
        shifty = get_shifty_by_code(shifty_code)
        shifty_date = period.start_date + timedelta(days=shifty["date_offset"])
        date_str = shifty_date.strftime("%m/%d/%Y")
        shift = "AM" if "AM" in shifty_code else "PM"
    except ValueError:
        date_str = ""
        shift = ""
        shifty = {}

    # First pass: identify support staff roles from detail_blocks
    support_staff_roles = {}  # employee -> role
    detail_blocks = approval_json.get("detail_blocks", [])

    # Day abbreviation mappings for matching
    day_abbrevs = {
        "M": ["mon", "monday"],
        "T": ["tue", "tues", "tuesday"],
        "W": ["wed", "wednesday"],
        "Th": ["thu", "thur", "thurs", "thursday"],
        "F": ["fri", "friday"],
        "Sa": ["sat", "saturday"],
        "Su": ["sun", "sunday"],
    }

    for block in detail_blocks:
        if not isinstance(block, list) or len(block) < 2:
            continue

        label = block[0].lower()
        lines = block[1]

        # Check if this block matches our shifty by day and AM/PM
        day_prefix = shifty_code[:-2]  # e.g., "M" from "MPM"
        shift_suffix = shifty_code[-2:]  # e.g., "PM" from "MPM"

        # Check if any day abbreviation matches the label
        day_matches = any(abbrev in label for abbrev in day_abbrevs.get(day_prefix, []))
        shift_matches = shift_suffix.lower() in label

        if not (day_matches and shift_matches):
            continue

        for line in lines:
            line_lower = line.lower()
            # Check for support staff role markers
            if "(utility)" in line_lower:
                match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', line)
                if match:
                    support_staff_roles[match.group(1)] = "Utility"
            elif "(expo)" in line_lower:
                match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', line)
                if match:
                    support_staff_roles[match.group(1)] = "Expo"
            elif "(busser)" in line_lower:
                match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', line)
                if match:
                    support_staff_roles[match.group(1)] = "Busser"
            elif "(host)" in line_lower:
                match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', line)
                if match:
                    support_staff_roles[match.group(1)] = "Host"

    # Second pass: extract from per_shift with correct roles
    per_shift = approval_json.get("per_shift", {})
    for employee, shifts in per_shift.items():
        amount = shifts.get(shifty_code, 0)
        if amount > 0:
            # Use support staff role if identified, otherwise Server
            role = support_staff_roles.get(employee, "Server")
            rows.append({
                "date": date_str,
                "shift": shift,
                "employee": employee,
                "role": role,
                "amount": amount,
            })

    return rows
