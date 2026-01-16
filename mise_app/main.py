"""Mise - Restaurant operations platform.

A mobile-first web app for restaurant payroll, inventory, and operations.
"""

from __future__ import annotations

import logging
import os
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mise_app.config import ShiftyConfig, shifty_state_manager, PayPeriod
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

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# No-cache middleware to prevent stale content on mobile
class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


app.add_middleware(NoCacheMiddleware)

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
app.state.shifty_state = shifty_state_manager


@app.get("/", response_class=RedirectResponse)
async def root():
    """Redirect to current pay period."""
    current = PayPeriod.current()
    return RedirectResponse(f"/period/{current.id}", status_code=302)


@app.get("/home", response_class=RedirectResponse)
async def legacy_home():
    """Legacy redirect - /home now redirects to /period/{current}."""
    current = PayPeriod.current()
    return RedirectResponse(f"/period/{current.id}", status_code=302)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "app": "mise"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
