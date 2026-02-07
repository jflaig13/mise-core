"""Weekly totals routes for Shifty app."""

from __future__ import annotations

import base64
import io
import json
import logging
import zipfile
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from mise_app.config import PayPeriod
from mise_app.tenant import require_restaurant, get_template_context
from mise_app.email_sender import (
    send_deliverables_email,
    format_payroll_email_subject,
    format_payroll_email_body
)
from mise_app.auth import DEMO_USERS

log = logging.getLogger(__name__)

router = APIRouter(prefix="/payroll/period/{period_id}", tags=["Payroll Totals"])


@router.get("/totals", response_class=HTMLResponse)
async def totals_page(request: Request, period_id: str):
    """Render the weekly totals page for a pay period."""
    restaurant_id = require_restaurant(request)
    config = request.app.state.config
    templates = request.app.state.templates

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse(f"Invalid pay period: {period_id}", status_code=404)

    # Get totals from local storage (with restaurant and period isolation)
    from mise_app.local_storage import get_totals_storage
    totals_storage = get_totals_storage()
    employees = totals_storage.get_all_totals(period_id, restaurant_id=restaurant_id)

    # Generate QR code for staff access
    qr_code = None
    if config.totals_sheet_id:
        sheet_url = f"https://docs.google.com/spreadsheets/d/{config.totals_sheet_id}/edit"
        qr_code = generate_qr_code(sheet_url)

    context = get_template_context(request)
    context.update({
        "period": period,
        "periods": PayPeriod.get_available_periods(),
        "employees": employees,
        "pay_period": period.label,
        "sheet_id": config.totals_sheet_id,
        "qr_code": qr_code,
        "active_tab": "totals",
    })
    return templates.TemplateResponse("totals.html", context)


@router.get("/qr", response_class=HTMLResponse)
async def qr_page(request: Request, period_id: str):
    """Render a full-screen QR code for staff access."""
    restaurant_id = require_restaurant(request)
    config = request.app.state.config
    templates = request.app.state.templates

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse(f"Invalid pay period: {period_id}", status_code=404)

    if not config.totals_sheet_id:
        return HTMLResponse("No totals sheet configured", status_code=404)

    sheet_url = f"https://docs.google.com/spreadsheets/d/{config.totals_sheet_id}/edit"
    qr_code = generate_qr_code(sheet_url)

    context = get_template_context(request)
    context.update({
        "period": period,
        "periods": PayPeriod.get_available_periods(),
        "qr_code": qr_code,
        "sheet_url": sheet_url,
        "pay_period": period.label,
        "active_tab": "qr",
    })
    return templates.TemplateResponse("qr.html", context)


def generate_qr_code(url: str) -> str:
    """Generate QR code as base64 data URL.

    Args:
        url: The URL to encode

    Returns:
        Base64 data URL for the QR code image
    """
    try:
        import qrcode
        qr = qrcode.make(url)
        buffer = io.BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
    except ImportError:
        log.warning("qrcode not installed, skipping QR generation")
        return ""


@router.get("/generate-deliverables")
async def generate_deliverables(request: Request, period_id: str):
    """Generate Tip Report PDF for the pay period."""
    restaurant_id = require_restaurant(request)

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse("<h1>Invalid pay period</h1>", status_code=404)

    from mise_app.local_storage import get_approval_storage, get_totals_storage
    approval_storage = get_approval_storage()
    totals_storage = get_totals_storage()

    # Get all approved shifty data
    all_rows = approval_storage.get_all(period_id, restaurant_id=restaurant_id)
    approved_rows = [r for r in all_rows if r.get("Status") == "Approved"]

    if not approved_rows:
        return HTMLResponse("<h1>No approved shifties found for this period</h1>", status_code=404)

    # Get totals (per_shift data)
    employees_data = totals_storage.get_all_totals(period_id, restaurant_id=restaurant_id)

    # Build per_shift structure
    per_shift = {}
    for emp_data in employees_data:
        emp_name = emp_data["name"]
        shifts = emp_data["shifts"]
        # Only include shifts with non-zero amounts
        per_shift[emp_name] = {shift_code: amt for shift_code, amt in shifts.items() if amt > 0}

    # Build weekly_totals
    weekly_totals = {emp_data["name"]: emp_data["total"] for emp_data in employees_data}

    # Extract detail_blocks from approved rows
    detail_blocks = []
    seen_filenames = set()
    for row in approved_rows:
        filename = row.get("Filename", "")
        if filename and filename not in seen_filenames and row.get("DetailBlocks"):
            seen_filenames.add(filename)
            try:
                blocks = json.loads(row["DetailBlocks"])
                if blocks:
                    detail_blocks.extend(blocks)
            except Exception as e:
                log.warning(f"Failed to parse DetailBlocks for {filename}: {e}")

    # Extract cook_tips from detail blocks (if any)
    cook_tips = {}
    # TODO: Parse cook tips from detail blocks if present

    # Format period dates for filename and header
    start_date = period.start_date
    end_date = period.end_date

    # Header format: "Week of Month Day–Day, Year"
    header = f"Week of {start_date.strftime('%B %d')}–{end_date.strftime('%d, %Y')}"

    # Out base format: TipReport_MMDDYY_MMDDYY
    out_base = f"TipReport_{start_date.strftime('%m%d%y')}_{end_date.strftime('%m%d%y')}"

    shift_cols = totals_storage.SHIFT_COLS

    # Generate PDF in memory
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

    pdf_buffer = io.BytesIO()

    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_heading = ParagraphStyle("Heading", parent=styles["Heading2"], spaceAfter=10, textColor=colors.darkblue)
    style_shift = ParagraphStyle("Shift", parent=styles["Heading3"], spaceAfter=6, textColor=colors.darkred)
    style_norm = styles["Normal"]

    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                            leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    # Title
    story += [
        Paragraph("Papa Surf Burger Bar — Tip Report", style_title),
        Paragraph(header, style_heading),
        Spacer(1, 12)
    ]

    # Page 1: Weekly Totals (alphabetical by last name)
    tot_rows = [["Employee", "Weekly Total ($)"]]
    for emp, val in sorted(weekly_totals.items(), key=lambda x: (x[0].split()[-1].lower(), x[0].split()[0].lower())):
        tot_rows.append([emp, f"${val:,.2f}"])

    t = Table(tot_rows, hAlign="LEFT", colWidths=[320, 140])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))
    story += [
        Paragraph("Weekly Totals (Alphabetical by Last Name; cooks included)", style_heading),
        t,
        PageBreak()
    ]

    # Page 2: Shift Matrix - Split into 2 tables (7 shifts each) for portrait
    all_emps = sorted(set(per_shift.keys()) | set(cook_tips.keys()),
                      key=lambda s: (s.split()[-1].lower(), s.split()[0].lower()))

    # First half: MAM through ThPM
    first_half_shifts = shift_cols[:7]  # MAM, MPM, TAM, TPM, WAM, WPM, ThAM
    matrix1 = [["Employee"] + first_half_shifts]
    for emp in all_emps:
        row = [emp] + [
            ("" if per_shift.get(emp, {}).get(c, "") == "" else f"${per_shift[emp][c]:,.2f}")
            for c in first_half_shifts
        ]
        matrix1.append(row)

    tm1 = Table(matrix1, hAlign="LEFT", repeatRows=1)
    tm1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))

    # Second half: ThPM through SuPM
    second_half_shifts = shift_cols[7:]  # ThPM, FAM, FPM, SaAM, SaPM, SuAM, SuPM
    matrix2 = [["Employee"] + second_half_shifts]
    for emp in all_emps:
        row = [emp] + [
            ("" if per_shift.get(emp, {}).get(c, "") == "" else f"${per_shift[emp][c]:,.2f}")
            for c in second_half_shifts
        ]
        matrix2.append(row)

    tm2 = Table(matrix2, hAlign="LEFT", repeatRows=1)
    tm2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))

    story += [
        Paragraph("Shift Breakdown (MAM → ThAM)", style_heading),
        tm1,
        Spacer(1, 20),
        Paragraph("Shift Breakdown (ThPM → SuPM)", style_heading),
        tm2,
        PageBreak()
    ]

    # Page 3+: Detailed math
    for title, lines in detail_blocks:
        story.append(Paragraph(title, style_shift))
        for ln in lines:
            story.append(Paragraph(ln, style_norm))
        story.append(Spacer(1, 10))

    doc.build(story)
    pdf_buffer.seek(0)

    # Generate Excel file
    import pandas as pd
    excel_buffer = io.BytesIO()

    # Sheet 1: Weekly Totals (alphabetical by last name)
    weekly_df = pd.DataFrame(
        sorted(weekly_totals.items(), key=lambda x: (x[0].split()[-1].lower(), x[0].split()[0].lower())),
        columns=["Employee", "Weekly Total ($)"]
    )

    # Sheet 2: Shift Breakdown
    all_emps = sorted(set(per_shift.keys()) | set(cook_tips.keys()),
                      key=lambda s: (s.split()[-1].lower(), s.split()[0].lower()))
    shift_rows = []
    for emp in all_emps:
        row = {"Employee": emp}
        for c in shift_cols:
            row[c] = per_shift.get(emp, {}).get(c, "")
        shift_rows.append(row)
    shift_df = pd.DataFrame(shift_rows, columns=["Employee"] + shift_cols)

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        weekly_df.to_excel(writer, index=False, sheet_name="Weekly Totals")
        shift_df.to_excel(writer, index=False, sheet_name="Shift Breakdown")

    excel_buffer.seek(0)

    # Generate PayrollExport CSV (Toast-ready)
    csv_buffer = io.BytesIO()

    # Load roster to get Employee IDs from active employees export
    import os
    roster_path = os.path.join(os.path.dirname(__file__), "../data/active_employees.csv")
    roster_map = {}

    try:
        roster_df = pd.read_csv(roster_path)
        for _, row in roster_df.iterrows():
            # Build full name from First Name and Last Name columns
            first_name = str(row['First Name']).strip() if pd.notna(row['First Name']) else ""
            last_name = str(row['Last Name']).strip() if pd.notna(row['Last Name']) else ""

            if first_name and last_name:
                full_name = f"{first_name} {last_name}"

                # Get Employee ID (might be string or int)
                emp_id = row['Employee ID']
                if pd.notna(emp_id) and str(emp_id).strip() != '':
                    try:
                        roster_map[full_name] = int(emp_id)
                    except (ValueError, TypeError):
                        log.warning(f"Invalid Employee ID for {full_name}: {emp_id}")
    except Exception as e:
        log.warning(f"Failed to load roster file: {e}")

    # Build PayrollExport CSV: Employee ID | Tips Owed | Employee Name
    payroll_rows = []
    for emp_name, total in weekly_totals.items():
        emp_id = roster_map.get(emp_name, "")
        payroll_rows.append({
            "Employee ID": emp_id,
            "Tips Owed": total,
            "Employee Name": emp_name
        })

    payroll_df = pd.DataFrame(payroll_rows)
    payroll_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Create zip file with all three files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(f"{out_base}.pdf", pdf_buffer.getvalue())
        zip_file.writestr(f"{out_base}.xlsx", excel_buffer.getvalue())

        # CSV filename format: MMDDYY_MMDDYY_PayrollExport.csv
        csv_filename = f"{start_date.strftime('%m%d%y')}_{end_date.strftime('%m%d%y')}_PayrollExport.csv"
        zip_file.writestr(csv_filename, csv_buffer.getvalue())

    # Get the complete zip file as bytes
    zip_data = zip_buffer.getvalue()

    # Send email with deliverables
    # Get user email from restaurant_id
    user_email = None
    restaurant_name = "Restaurant"

    # Find the user account for this restaurant
    for username, user_data in DEMO_USERS.items():
        if user_data.get("restaurant_id") == restaurant_id:
            user_email = user_data.get("email")
            restaurant_name = user_data.get("name", "Restaurant")
            break

    if user_email:
        try:
            # Format email
            subject = format_payroll_email_subject(start_date, end_date)
            body = format_payroll_email_body(restaurant_name, start_date, end_date)
            attachment_filename = f"{out_base}_deliverables.zip"

            # Send email (non-blocking - we still return the file regardless)
            email_sent = send_deliverables_email(
                to_email=user_email,
                subject=subject,
                body=body,
                attachment_data=zip_data,
                attachment_filename=attachment_filename
            )

            if email_sent:
                log.info(f"Deliverables emailed to {user_email}")
            else:
                log.warning(f"Failed to email deliverables to {user_email}")
        except Exception as e:
            log.error(f"Error sending deliverables email: {e}")
            # Continue regardless of email failure
    else:
        log.warning(f"No email configured for restaurant_id: {restaurant_id}")

    # Create fresh buffer for download response
    download_buffer = io.BytesIO(zip_data)
    download_buffer.seek(0)

    # Return zip file
    return StreamingResponse(
        download_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{out_base}_deliverables.zip"'
        }
    )
