"""Home page routes for Shifty app."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from mise_app.config import PayPeriod
from mise_app.local_storage import get_approval_storage, get_totals_storage

router = APIRouter(prefix="/payroll/period/{period_id}", tags=["Payroll Home"])


@router.get("", response_class=HTMLResponse)
async def home_page(request: Request, period_id: str):
    """Render the 'tap to record a shifty' page (the main payroll landing)."""
    templates = request.app.state.templates

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse(f"Invalid pay period: {period_id}", status_code=404)

    return templates.TemplateResponse(
        "record_home.html",
        {
            "request": request,
            "period": period,
            "periods": PayPeriod.get_available_periods(),
            "pay_period": period.label,
            "active_tab": "shifties",
        }
    )


@router.get("/shifties", response_class=HTMLResponse)
async def shifties_page(request: Request, period_id: str):
    """Render the weekly shifties grid showing all 14 shifties."""
    templates = request.app.state.templates
    shifty_state = request.app.state.shifty_state

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse(f"Invalid pay period: {period_id}", status_code=404)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "period": period,
            "periods": PayPeriod.get_available_periods(),
            "shifties": shifty_state.get_all_shifties(period),
            "pay_period": period.label,
            "active_tab": "shifties",
        }
    )


@router.get("/reset", response_class=HTMLResponse)
async def reset_shifties(request: Request, period_id: str):
    """Reset all shifty statuses and clear all data for a pay period."""
    templates = request.app.state.templates
    shifty_state = request.app.state.shifty_state

    try:
        period = PayPeriod.from_id(period_id)
    except ValueError:
        return HTMLResponse(f"Invalid pay period: {period_id}", status_code=404)

    # Clear shifty state for this period
    shifty_state.reset(period_id)

    # Clear all stored data for this period
    get_approval_storage().clear(period_id)
    get_totals_storage().clear(period_id)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "period": period,
            "periods": PayPeriod.get_available_periods(),
            "shifties": shifty_state.get_all_shifties(period),
            "pay_period": period.label,
            "message": "Week reset! All data cleared.",
            "active_tab": "shifties",
        }
    )
