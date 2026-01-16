"""Recording and processing routes for Shifty app."""

from __future__ import annotations

import logging
import os
from datetime import timedelta
from typing import Optional

import requests
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from mise_app.config import SHIFTY_DEFINITIONS, get_shifty_by_code, PayPeriod
from mise_app.local_storage import get_approval_storage, get_totals_storage

log = logging.getLogger(__name__)

router = APIRouter(prefix="/period/{period_id}", tags=["Recording"])


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
        }
    )


@router.post("/process/{shifty_code}")
async def process_shifty(
    request: Request,
    period_id: str,
    shifty_code: str,
    file: UploadFile = File(...),
):
    """Process an uploaded audio file for a shifty."""
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
        "redirect_url": f"/period/{period_id}/approve/{shifty_code}",
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

    return RedirectResponse(f"/period/{period_id}", status_code=303)


@router.get("/approved/{filename}")
async def handle_legacy_approval(request: Request, period_id: str, filename: str):
    """Legacy endpoint - redirect to new approval flow."""
    shifty_code = filename.replace(".wav", "")
    return RedirectResponse(f"/period/{period_id}/approve/{shifty_code}", status_code=303)


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
