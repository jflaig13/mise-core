"""Payroll Agent - Parses payroll transcripts using Claude.

This agent receives payroll transcripts from the transrouter and uses
Claude to parse them into structured approval JSON matching the LPM schema.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from ..claude_client import ClaudeClient, ClaudeConfig, ClaudeResponse
from ..prompts.payroll_prompt import (
    build_payroll_system_prompt,
    build_payroll_user_prompt,
)

log = logging.getLogger(__name__)


class PayrollAgentError(Exception):
    """Raised when payroll agent encounters an error."""

    pass


class PayrollAgent:
    """Agent for parsing payroll transcripts into approval JSON.

    Usage:
        agent = PayrollAgent()
        result = agent.parse_transcript(transcript_text)

        if result["status"] == "success":
            approval_json = result["approval_json"]
        else:
            error = result["error"]
    """

    def __init__(
        self,
        claude_client: Optional[ClaudeClient] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize payroll agent.

        Args:
            claude_client: Optional pre-configured Claude client.
            config: Optional configuration dict (used if claude_client not provided).
        """
        if claude_client:
            self.claude_client = claude_client
        else:
            claude_config = ClaudeConfig.from_dict(config or {})
            self.claude_client = ClaudeClient(config=claude_config)

        self._system_prompt: Optional[str] = None

    @property
    def system_prompt(self) -> str:
        """Lazy-load and cache the system prompt."""
        if self._system_prompt is None:
            self._system_prompt = build_payroll_system_prompt()
            log.debug("Built payroll system prompt (%d chars)", len(self._system_prompt))
        return self._system_prompt

    def parse_transcript(
        self,
        transcript: str,
        pay_period_hint: str = "",
    ) -> Dict[str, Any]:
        """Parse a payroll transcript into approval JSON.

        Args:
            transcript: The payroll transcript text to parse.
            pay_period_hint: Optional hint about pay period dates.

        Returns:
            Dict with keys:
                - agent: "payroll"
                - status: "success" or "error"
                - approval_json: The parsed approval JSON (if successful)
                - raw_response: Claude's full response text
                - error: Error message (if failed)
                - usage: Token usage stats
        """
        log.info("Parsing payroll transcript (%d chars)", len(transcript))

        user_prompt = build_payroll_user_prompt(transcript, pay_period_hint)

        response: ClaudeResponse = self.claude_client.call(
            system_prompt=self.system_prompt,
            user_content=user_prompt,
            extract_json=True,
        )

        if not response.success:
            log.error("Claude API call failed: %s", response.error)
            return {
                "agent": "payroll",
                "status": "error",
                "error": response.error,
                "raw_response": response.content,
            }

        if not response.json_data:
            log.error("Failed to extract JSON from Claude response")
            return {
                "agent": "payroll",
                "status": "error",
                "error": "Failed to extract JSON from response",
                "raw_response": response.content,
            }

        # Validate the approval JSON has required keys
        validation_error = self._validate_approval_json(response.json_data)
        if validation_error:
            log.error("Approval JSON validation failed: %s", validation_error)
            return {
                "agent": "payroll",
                "status": "error",
                "error": validation_error,
                "approval_json": response.json_data,
                "raw_response": response.content,
            }

        log.info(
            "Successfully parsed payroll transcript (employees=%d)",
            len(response.json_data.get("weekly_totals", {})),
        )

        return {
            "agent": "payroll",
            "status": "success",
            "approval_json": response.json_data,
            "raw_response": response.content,
            "usage": response.usage,
        }

    def _validate_approval_json(self, data: Dict[str, Any]) -> Optional[str]:
        """Validate that approval JSON has required structure.

        Args:
            data: The parsed JSON data.

        Returns:
            Error message if validation fails, None if valid.
        """
        required_keys = [
            "out_base",
            "header",
            "shift_cols",
            "per_shift",
            "cook_tips",
            "weekly_totals",
            "detail_blocks",
        ]

        missing_keys = [k for k in required_keys if k not in data]
        if missing_keys:
            return f"Missing required keys: {missing_keys}"

        # Validate shift_cols is the expected array
        expected_shift_cols = [
            "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
            "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM",
            "SuAM", "SuPM",
        ]
        if data.get("shift_cols") != expected_shift_cols:
            return "shift_cols does not match expected format"

        # Validate per_shift and weekly_totals are dicts
        if not isinstance(data.get("per_shift"), dict):
            return "per_shift must be an object"
        if not isinstance(data.get("weekly_totals"), dict):
            return "weekly_totals must be an object"
        if not isinstance(data.get("cook_tips"), dict):
            return "cook_tips must be an object"
        if not isinstance(data.get("detail_blocks"), list):
            return "detail_blocks must be an array"

        # Validate all per_shift employees are in weekly_totals
        per_shift_employees = set(data.get("per_shift", {}).keys())
        weekly_totals_employees = set(data.get("weekly_totals", {}).keys())
        cook_employees = set(data.get("cook_tips", {}).keys())

        all_employees = per_shift_employees | cook_employees
        missing_from_totals = all_employees - weekly_totals_employees
        if missing_from_totals:
            return f"Employees missing from weekly_totals: {missing_from_totals}"

        return None


# Module-level instance for simple usage
_default_agent: Optional[PayrollAgent] = None


def get_agent(config: Optional[Dict[str, Any]] = None) -> PayrollAgent:
    """Get or create the default payroll agent."""
    global _default_agent

    if config:
        return PayrollAgent(config=config)

    if _default_agent is None:
        _default_agent = PayrollAgent()

    return _default_agent


def handle_payroll_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a payroll request from the domain router.

    This is the main entry point called by domain_router.py.

    Args:
        request: Dict with keys:
            - intent_type: The classified intent type
            - entities: Extracted entities
            - meta: Metadata including transcript

    Returns:
        Dict with agent response (see PayrollAgent.parse_transcript).
    """
    log.info("Handling payroll request (intent=%s)", request.get("intent_type"))

    # Extract transcript from request
    transcript = request.get("meta", {}).get("transcript", "")

    if not transcript:
        # Try to get transcript from entities or other locations
        transcript = request.get("entities", {}).get("transcript", "")

    if not transcript:
        log.error("No transcript found in payroll request")
        return {
            "agent": "payroll",
            "status": "error",
            "error": "No transcript provided in request",
            "request": request,
        }

    # Get pay period hint if available
    pay_period_hint = request.get("meta", {}).get("pay_period", "")

    # Parse the transcript
    agent = get_agent()
    return agent.parse_transcript(transcript, pay_period_hint)
