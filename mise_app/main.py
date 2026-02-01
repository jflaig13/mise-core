"""Mise - Restaurant operations platform.

A mobile-first web app for restaurant payroll, inventory, and operations.

DEPLOYMENT:
    Production service: "mise" in us-central1
    Domain: app.getmise.io
    Command: cd ~/mise-core/mise_app && gcloud run deploy mise --source . --region us-central1

    DO NOT create new services (mise-app, mise2, etc.)
    DO NOT deploy to other regions
    DO NOT change the service name from "mise"
"""

from __future__ import annotations

import logging
import os
import sys

# Set environment based on Cloud Run detection
if os.getenv("K_SERVICE"):  # Running on Cloud Run
    os.environ["ENVIRONMENT"] = "production"
else:
    os.environ["ENVIRONMENT"] = "development"

# GCS bucket name for production storage
os.environ.setdefault("GCS_BUCKET_NAME", "mise-production-data")

import requests as http_requests
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mise_app.config import ShiftyConfig, get_shifty_state_manager, PayPeriod
from mise_app.routes import home, recording, totals, inventory, auth
from mise_app.middleware import RestaurantContextMiddleware
from mise_app.tenant import get_template_context
from starlette.middleware.sessions import SessionMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

# Load config
config = ShiftyConfig.from_env()
log.info(f"🔧 LOADED CONFIG - TRANSROUTER_URL: {config.transrouter_url}")

# Create FastAPI app
app = FastAPI(
    title="Mise",
    description="Restaurant operations platform",
    version="1.0.0",
)

# Add CORS middleware for cross-origin requests
# SECURITY: Explicit origin whitelist (never use "*" with credentials=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",  # Local mise_app testing
        "http://localhost:8080",  # Local transrouter testing
        "https://payroll-engine-rdxbrrdtsa-uc.a.run.app",  # Production Cloud Run
        "https://app.getmise.io",  # Custom domain
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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

# Authentication middleware - protect all routes except login
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Allow public routes (login, health checks, static files)
        # AND large file upload API endpoints (no browser session needed)
        public_paths = [
            "/login",
            "/health",
            "/static",
            "/inventory/get_upload_url",
            "/inventory/process_uploaded"
        ]
        if any(request.url.path.startswith(p) for p in public_paths):
            return await call_next(request)

        # Check authentication
        if not request.session.get("authenticated"):
            return RedirectResponse("/login", status_code=302)

        # Authenticated - proceed
        return await call_next(request)

app.add_middleware(AuthMiddleware)

# Restaurant context middleware (runs after session, before auth in execution order)
app.add_middleware(RestaurantContextMiddleware)

# Session middleware for authentication (must be added AFTER AuthMiddleware)
SESSION_SECRET = os.environ.get(
    "SESSION_SECRET_KEY",
    "dev-secret-key-change-in-production-min-32-chars-long"
)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    session_cookie="mise_session",
    max_age=86400,  # 24 hours
    same_site="lax",
    https_only=False  # Set to True in production, False for local testing
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
app.include_router(inventory.router)
app.include_router(auth.router)

# Make config and templates available to routes
app.state.config = config
app.state.templates = templates
app.state.shifty_state = get_shifty_state_manager()


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Render the main landing page with voice-first interface."""
    # Explicit auth check - belt and suspenders
    if not request.session.get("authenticated"):
        return RedirectResponse("/login", status_code=302)

    current_period = PayPeriod.current()
    context = get_template_context(request)
    context.update({
        "active_tab": "home",
        "current_period_id": current_period.id,
    })
    return templates.TemplateResponse("landing.html", context)


@app.post("/process")
async def process_voice(request: Request, file: UploadFile = File(...)):
    """Process voice recording via transrouter and route to appropriate agent.

    This is the main entry point for the voice-first interface.
    The transrouter determines the domain (payroll, inventory, etc.) and routes accordingly.
    """
    log.info(f"Processing voice input from landing page: {file.filename}")

    # Read audio bytes
    audio_bytes = await file.read()
    if not audio_bytes:
        return JSONResponse(
            {"status": "error", "error": "Empty audio file"},
            status_code=400
        )

    # Call transrouter API
    try:
        response = http_requests.post(
            f"{config.transrouter_url}/api/v1/audio/process",
            headers={"X-API-Key": config.transrouter_api_key},
            files={"file": ("recording.wav", audio_bytes, "audio/wav")},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except http_requests.RequestException as e:
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

    # Determine domain and route accordingly
    domain = result.get("domain", "unknown")
    log.info(f"Transrouter detected domain: {domain}")

    if domain == "payroll":
        # Route to payroll flow
        current = PayPeriod.current()
        return JSONResponse({
            "status": "success",
            "domain": "payroll",
            "redirect_url": f"/payroll/period/{current.id}",
        })
    elif domain == "inventory":
        # Route to inventory flow (when implemented)
        return JSONResponse({
            "status": "success",
            "domain": "inventory",
            "redirect_url": "/inventory",
        })
    else:
        # Unknown domain - redirect to home
        return JSONResponse({
            "status": "success",
            "domain": domain,
            "redirect_url": "/",
        })


@app.get("/payroll", response_class=RedirectResponse)
async def payroll_root():
    """Redirect to current pay period's payroll page."""
    current = PayPeriod.current()
    return RedirectResponse(f"/payroll/period/{current.id}", status_code=302)


@app.get("/home", response_class=RedirectResponse)
async def legacy_home():
    """Legacy redirect - /home now redirects to landing."""
    return RedirectResponse("/", status_code=302)


# Legacy redirects for old /period URLs
@app.get("/period/{period_id}", response_class=RedirectResponse)
async def legacy_period(period_id: str):
    """Legacy redirect - /period/{id} now redirects to /payroll/period/{id}."""
    return RedirectResponse(f"/payroll/period/{period_id}", status_code=302)


@app.get("/period/{period_id}/{rest:path}", response_class=RedirectResponse)
async def legacy_period_path(period_id: str, rest: str):
    """Legacy redirect - /period/{id}/... now redirects to /payroll/period/{id}/..."""
    return RedirectResponse(f"/payroll/period/{period_id}/{rest}", status_code=302)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "app": "mise"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
