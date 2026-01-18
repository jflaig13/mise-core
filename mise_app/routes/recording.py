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

log = logging.getLogger(__name__)

# Recordings storage directory
RECORDINGS_DIR = Path(__file__).parent.parent.parent / "recordings"


def save_recording(audio_bytes: bytes, period_id: str, shifty_code: str = None, original_filename: str = None) -> Path:
    """Save audio recording to the recordings folder.

    Args:
        audio_bytes: The raw audio bytes
        period_id: Pay period ID (e.g., '2025-01-12')
        shifty_code: Optional shifty code if known (e.g., 'MAM', 'TPM')
        original_filename: Original filename from upload

    Returns:
        Path to the saved file
    """
    # Ensure recordings directory exists
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

    # Determine file extension
    ext = ".webm"  # Default for browser recordings
    if original_filename:
        if original_filename.endswith(".wav"):
            ext = ".wav"
        elif original_filename.endswith(".m4a"):
            ext = ".m4a"
        elif original_filename.endswith(".mp3"):
            ext = ".mp3"

    # Build filename: {period_id}_{shifty_code}_{timestamp}{ext}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if shifty_code:
        filename = f"{period_id}_{shifty_code}_{timestamp}{ext}"
    else:
        filename = f"{period_id}_unknown_{timestamp}{ext}"

    filepath = RECORDINGS_DIR / filename
    filepath.write_bytes(audio_bytes)

    log.info(f"Saved recording to {filepath}")
    return filepath

router = APIRouter(prefix="/payroll/period/{period_id}", tags=["Payroll Recording"])


def detect_shifty_from_transcript(transcript: str, period: PayPeriod) -> Optional[str]:
    """Detect the shifty code (e.g., 'MAM', 'TPM') from transcript content.

    Looks for patterns like:
    - "Monday AM" / "Monday PM"
    - "Tuesday morning" / "Tuesday night"
    - "01/15 AM shift"
    - Date references that map to a day of the week
    """
    transcript_lower = transcript.lower()

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
    am_indicators = ["am", "morning", "lunch", "day shift", "day"]
    pm_indicators = ["pm", "evening", "night", "dinner", "closing", "close"]

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
            # Make sure it's not just part of a word
            pattern = r'\b' + re.escape(indicator) + r'\b'
            if re.search(pattern, transcript_lower):
                detected_shift = "AM"
                break

    if not detected_shift:
        for indicator in pm_indicators:
            if indicator in transcript_lower:
                pattern = r'\b' + re.escape(indicator) + r'\b'
                if re.search(pattern, transcript_lower):
                    detected_shift = "PM"
                    break

    # Try to find date (MM/DD format)
    date_match = re.search(r'(\d{1,2})[/\-](\d{1,2})', transcript_lower)
    if date_match and not detected_day:
        month = int(date_match.group(1))
        day = int(date_match.group(2))
        try:
            # Assume current year
            parsed_date = date(period.start_date.year, month, day)
            # Get day of week
            day_names = ["M", "T", "W", "Th", "F", "Sa", "Su"]
            detected_day = day_names[parsed_date.weekday()]
        except ValueError:
            pass

    # Build shifty code
    if detected_day and detected_shift:
        return f"{detected_day}{detected_shift}"

    return None


def get_shifty_date(shifty_code: str, period: PayPeriod) -> Optional[date]:
    """Get the actual date for a shifty code within a pay period."""
    try:
        shifty = get_shifty_by_code(shifty_code)
        return period.start_date + timedelta(days=shifty["date_offset"])
    except ValueError:
        return None


@router.get("/record/{shifty_code}", response_class=HTMLResponse)
async def record_page(request: Request, period_id: str, shifty_code: str):
    """Render the recording page for a specific shifty."""
    templates = request.app.state.templates

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse(f"Invalid pay period: {period_id}", status_code=404)

    try:
        shifty = get_shifty_by_code(shifty_code)
    except ValueError:
        return HTMLResponse(f"Unknown shifty code: {shifty_code}", status_code=404)

    # Calculate the date for this shifty
    shifty_date = period.start_date + timedelta(days=shifty["date_offset"])

    return templates.TemplateResponse(
        "record.html",
        {
            "request": request,
            "period": period,
            "periods": PayPeriod.get_available_periods(),
            "shifty": shifty,
            "shifty_date": shifty_date.strftime("%m/%d/%Y"),
            "pay_period": period.label,
            "active_tab": "shifties",
        }
    )


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
            files={"file": ("recording.wav", audio_bytes, "audio/wav")},
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

    # Detect shifty code from transcript
    shifty_code = detect_shifty_from_transcript(transcript, period)

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

    log.info(f"Detected shifty {shifty_code} from transcript, length={len(transcript)}")

    # Save recording to local storage
    save_recording(audio_bytes, period_id, shifty_code, file.filename)

    # Convert approval_json to flat rows
    rows = flatten_approval_json(approval_json, shifty_code, period)

    # Store locally (with period isolation)
    filename = f"{shifty_code}.wav"
    approval_storage = get_approval_storage()
    approval_storage.add_shifty(period_id, rows, filename, transcript)

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
    approval_storage.add_shifty(period_id, rows, filename, transcript)

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

    # Get transcript from first row
    transcript = ""
    for row in rows:
        if row.get("Transcript"):
            transcript = row["Transcript"]
            break

    shifty_date = period.start_date + timedelta(days=shifty["date_offset"])

    return templates.TemplateResponse(
        "approve.html",
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

    for block in detail_blocks:
        if not isinstance(block, list) or len(block) < 2:
            continue

        label = block[0]
        lines = block[1]

        # Check if this block matches our shifty
        shifty_label = shifty.get("label", "").split()[0] if shifty else ""
        if shifty_code not in label and shifty_label not in label:
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
