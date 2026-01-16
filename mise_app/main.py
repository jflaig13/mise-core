"""Mise - Restaurant operations platform.

A mobile-first web app for restaurant payroll, inventory, and operations.
"""

from __future__ import annotations

import logging
import os
import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mise_app.config import ShiftyConfig, shifty_state
from mise_app.routes import home, recording, totals

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

# Load config
config = ShiftyConfig.from_env()

# Create FastAPI app
app = FastAPI(
    title="Mise",
    description="Restaurant operations platform",
    version="1.0.0",
)

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# Templates
templates_path = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_path)

# Include routers
app.include_router(home.router)
app.include_router(recording.router)
app.include_router(totals.router)

# Make config and templates available to routes
app.state.config = config
app.state.templates = templates
app.state.shifty_state = shifty_state


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect to home page."""
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "shifties": shifty_state.get_all_shifties(config),
            "pay_period": config.pay_period_label,
        }
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "app": "mise"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
