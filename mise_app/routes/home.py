"""Home page routes for Shifty app."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Home"])


@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    """Render the home page with all shifties."""
    config = request.app.state.config
    templates = request.app.state.templates
    shifty_state = request.app.state.shifty_state

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "shifties": shifty_state.get_all_shifties(config),
            "pay_period": config.pay_period_label,
        }
    )


@router.get("/reset", response_class=HTMLResponse)
async def reset_shifties(request: Request):
    """Reset all shifty statuses (for demo purposes)."""
    shifty_state = request.app.state.shifty_state
    shifty_state.reset()

    config = request.app.state.config
    templates = request.app.state.templates

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "shifties": shifty_state.get_all_shifties(config),
            "pay_period": config.pay_period_label,
            "message": "All shifties reset!",
        }
    )
