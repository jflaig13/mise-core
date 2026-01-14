"""FastAPI application for the Transrouter API.

This is the main entry point for the HTTP API layer. It wraps the
transrouter core logic (orchestrator, agents, brain sync) in a
REST API that can be deployed to Cloud Run or any container platform.

Run locally:
    uvicorn transrouter.api.main:app --reload --port 8080

Run in production:
    uvicorn transrouter.api.main:app --host 0.0.0.0 --port 8080
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..src.brain_sync import get_brain
from ..src.logging_utils import configure_logging, get_logger
from .routes import payroll_router, audio_router

# Configure logging with file output
configure_logging()
log = get_logger(__name__)

# API metadata
API_VERSION = "1.0.0"
API_TITLE = "Mise Transrouter API"
API_DESCRIPTION = """
Mise restaurant operations API. Routes voice/text input to domain agents
(payroll, inventory, scheduling) and returns structured JSON.
"""


# ============================================================================
# Lifespan Handler (startup/shutdown)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown lifecycle."""
    # Startup
    log.info("Starting Mise Transrouter API v%s", API_VERSION)

    # Pre-load the brain to catch config errors early
    try:
        brain = get_brain()
        log.info(
            "Brain loaded: %d domains, %d employees in roster",
            len(brain.domains),
            len(brain.employee_roster)
        )
    except Exception as e:
        log.error("Failed to load brain on startup: %s", e)
        # Don't crash - health endpoint will report unhealthy

    yield  # Server is running

    # Shutdown
    log.info("Shutting down Mise Transrouter API")


# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware - configure for your frontend domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Response Models
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: str
    brain_loaded: bool
    domains: list[str]


class ErrorResponse(BaseModel):
    """Standard error response."""
    status: str = "error"
    error: str
    detail: str | None = None


# ============================================================================
# Health Endpoint
# ============================================================================

@app.get(
    "/api/v1/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check",
    description="Returns API health status. Use for load balancer health checks."
)
async def health_check() -> HealthResponse:
    """Health check endpoint for load balancers and monitoring."""
    try:
        brain = get_brain()
        brain_loaded = brain.loaded
        domains = list(brain.domains.keys())
    except Exception:
        brain_loaded = False
        domains = []

    return HealthResponse(
        status="healthy" if brain_loaded else "degraded",
        version=API_VERSION,
        timestamp=datetime.utcnow().isoformat() + "Z",
        brain_loaded=brain_loaded,
        domains=domains,
    )


# Also respond to root health check (some load balancers use /)
@app.get("/", include_in_schema=False)
async def root_health():
    """Root path health check (for simple load balancers)."""
    return {"status": "healthy", "service": "mise-transrouter"}


# ============================================================================
# Include Routers
# ============================================================================

app.include_router(payroll_router)
app.include_router(audio_router)
