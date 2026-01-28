"""Weekly totals routes for Shifty app."""

from __future__ import annotations

import base64
import io
import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from mise_app.config import PayPeriod
from mise_app.tenant import require_restaurant, get_template_context

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
