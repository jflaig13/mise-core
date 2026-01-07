"""Payroll API routes.

Endpoints for parsing payroll transcripts and returning structured approval JSON.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ...src.transrouter_orchestrator import handle_text_request
from ..auth import require_api_key

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/payroll", tags=["Payroll"])


# ============================================================================
# Request/Response Models
# ============================================================================

class PayrollParseRequest(BaseModel):
    """Request body for parsing a payroll transcript."""

    transcript: str = Field(
        ...,
        description="The payroll transcript text to parse",
        min_length=10,
        examples=["Monday AM shift. Ryan was utility. Austin before tipout $200, food sales $500."]
    )
    pay_period_hint: Optional[str] = Field(
        None,
        description="Optional hint about the pay period dates (e.g., '12/29/25 - 01/04/26')"
    )


class PayrollParseResponse(BaseModel):
    """Response from parsing a payroll transcript."""

    status: str = Field(..., description="'success' or 'error'")
    agent: str = Field(default="payroll", description="The agent that processed the request")
    approval_json: Optional[Dict[str, Any]] = Field(
        None,
        description="The structured approval JSON (LPM schema) if successful"
    )
    error: Optional[str] = Field(None, description="Error message if status is 'error'")
    usage: Optional[Dict[str, int]] = Field(
        None,
        description="Token usage from Claude API call"
    )


class PayrollErrorResponse(BaseModel):
    """Error response for payroll endpoints."""

    status: str = "error"
    agent: str = "payroll"
    error: str
    detail: Optional[str] = None


# ============================================================================
# Endpoints
# ============================================================================

@router.post(
    "/parse",
    response_model=PayrollParseResponse,
    responses={
        200: {"description": "Transcript parsed successfully"},
        400: {"model": PayrollErrorResponse, "description": "Invalid request"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
        500: {"model": PayrollErrorResponse, "description": "Processing error"},
    },
    summary="Parse payroll transcript",
    description="""
    Parse a payroll transcript and return structured approval JSON.

    **Requires authentication**: Include `X-API-Key` header.

    The transcript should contain shift information including:
    - Date and shift (AM/PM)
    - Support staff (expo, busser, utility)
    - Server tips and food sales

    Returns the approval JSON matching the LPM (Local Payroll Machine) schema.
    """
)
async def parse_payroll(
    request: PayrollParseRequest,
    client: str = Depends(require_api_key),
) -> PayrollParseResponse:
    """Parse a payroll transcript and return approval JSON."""
    log.info(
        "Payroll parse request from client=%s (transcript_length=%d)",
        client,
        len(request.transcript),
    )

    try:
        # Route through the transrouter orchestrator
        # This handles intent classification and calls the payroll agent
        response = handle_text_request(
            request.transcript,
            {"transcript": request.transcript, "pay_period_hint": request.pay_period_hint}
        )

        # Check if it routed to payroll
        if response.domain != "payroll":
            log.warning(
                "Transcript routed to '%s' instead of payroll",
                response.domain
            )
            return PayrollParseResponse(
                status="error",
                error=f"Transcript was classified as '{response.domain}', not payroll. "
                      f"Please ensure the transcript contains payroll information.",
            )

        # Extract the payload from the router response
        payload = response.payload or {}

        if payload.get("status") == "success":
            log.info("Payroll transcript parsed successfully")
            return PayrollParseResponse(
                status="success",
                agent="payroll",
                approval_json=payload.get("approval_json"),
                usage=payload.get("usage"),
            )
        else:
            error_msg = payload.get("error", "Unknown error during parsing")
            log.error("Payroll parsing failed: %s", error_msg)
            return PayrollParseResponse(
                status="error",
                agent="payroll",
                error=error_msg,
            )

    except Exception as e:
        log.exception("Unexpected error in payroll parse endpoint")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )
