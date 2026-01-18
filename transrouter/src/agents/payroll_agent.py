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
        shift_code: str = "",
    ) -> Dict[str, Any]:
        """Parse a payroll transcript into approval JSON.

        Args:
            transcript: The payroll transcript text to parse.
            pay_period_hint: Optional hint about pay period dates.
            shift_code: Optional shift code from filename (e.g., "ThAM", "FPM").

        Returns:
            Dict with keys:
                - agent: "payroll"
                - status: "success" or "error"
                - approval_json: The parsed approval JSON (if successful)
                - raw_response: Claude's full response text
                - error: Error message (if failed)
                - usage: Token usage stats
        """
        log.info("Parsing payroll transcript (%d chars, shift_code=%s)", len(transcript), shift_code or "none")

        user_prompt = build_payroll_user_prompt(transcript, pay_period_hint, shift_code)

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

        # Auto-correct any inconsistencies between detail_blocks and per_shift
        corrections = self._auto_correct_approval_json(response.json_data)
        if corrections:
            log.info("Auto-corrected %d inconsistencies in approval JSON", len(corrections))
            for correction in corrections:
                log.info("  CORRECTED: %s", correction)

        log.info(
            "Successfully parsed payroll transcript (employees=%d, corrections=%d)",
            len(response.json_data.get("weekly_totals", {})),
            len(corrections),
        )

        return {
            "agent": "payroll",
            "status": "success",
            "approval_json": response.json_data,
            "raw_response": response.content,
            "usage": response.usage,
            "corrections": corrections if corrections else None,
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

        # Validate per_shift sums match weekly_totals
        warnings = []
        for employee, shifts in data.get("per_shift", {}).items():
            calculated_total = sum(shifts.values())
            stated_total = data.get("weekly_totals", {}).get(employee, 0)
            diff = abs(calculated_total - stated_total)
            if diff > 0.02:  # Allow 2 cent rounding tolerance
                warnings.append(
                    f"{employee}: per_shift sum ${calculated_total:.2f} != weekly_total ${stated_total:.2f} (diff: ${diff:.2f})"
                )

        # Log warnings but don't fail validation (Claude inconsistency, not error)
        if warnings:
            log.warning("Validation warnings (per_shift vs weekly_totals mismatch):")
            for w in warnings:
                log.warning("  %s", w)

        # Check detail_blocks for amounts that should be in per_shift
        detail_warnings = self._check_detail_block_consistency(data)
        if detail_warnings:
            log.warning("Validation warnings (detail_blocks vs per_shift):")
            for w in detail_warnings:
                log.warning("  %s", w)

        return None

    def _check_detail_block_consistency(self, data: Dict[str, Any]) -> list:
        """Check if amounts mentioned in detail_blocks are in per_shift.

        Returns list of warning strings (doesn't fail validation).
        """
        import re

        warnings = []
        per_shift = data.get("per_shift", {})

        # Map shift labels to shift codes
        day_map = {
            "Mon": "M", "Tue": "T", "Wed": "W", "Thu": "Th",
            "Fri": "F", "Sat": "Sa", "Sun": "Su"
        }

        for block in data.get("detail_blocks", []):
            if not isinstance(block, list) or len(block) < 2:
                continue

            label = block[0]  # e.g., "Thu Jan 8 — PM (tip pool)"
            lines = block[1]

            # Parse day and AM/PM from label
            shift_code = None
            for day_name, day_code in day_map.items():
                if day_name in label:
                    if "AM" in label:
                        shift_code = f"{day_code}AM"
                    elif "PM" in label:
                        shift_code = f"{day_code}PM"
                    break

            if not shift_code:
                continue

            # Look for employee amounts in the detail lines
            # Pattern: "Employee Name: $XX.XX" at end of line
            for line in lines:
                # Match patterns like "Kevin Worley: $99.98" or "Austin Kelley: $99.98"
                match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+): \$(\d+\.?\d*)\s*$', line)
                if match:
                    employee = match.group(1)
                    amount = float(match.group(2))

                    # Check if this employee has this shift in per_shift
                    if employee in per_shift:
                        employee_shifts = per_shift[employee]
                        if shift_code not in employee_shifts:
                            warnings.append(
                                f"{employee} has ${amount:.2f} in {label} detail but {shift_code} missing from per_shift"
                            )
                        else:
                            per_shift_amount = employee_shifts[shift_code]
                            if abs(per_shift_amount - amount) > 0.02:
                                warnings.append(
                                    f"{employee} {shift_code}: detail shows ${amount:.2f} but per_shift has ${per_shift_amount:.2f}"
                                )

        return warnings

    def _auto_correct_approval_json(self, data: Dict[str, Any]) -> list:
        """Auto-correct inconsistencies between detail_blocks and per_shift.

        Parses detail_blocks, finds missing/incorrect per_shift entries,
        fixes them, and recalculates weekly_totals.

        Returns list of correction descriptions for audit trail.
        """
        import re

        corrections = []
        per_shift = data.get("per_shift", {})
        weekly_totals = data.get("weekly_totals", {})

        # Map shift labels to shift codes
        day_map = {
            "Mon": "M", "Tue": "T", "Wed": "W", "Thu": "Th",
            "Fri": "F", "Sat": "Sa", "Sun": "Su"
        }

        # Extract expected values from detail_blocks
        expected_values = {}  # {employee: {shift_code: amount}}

        for block in data.get("detail_blocks", []):
            if not isinstance(block, list) or len(block) < 2:
                continue

            label = block[0]
            lines = block[1]

            # Parse day and AM/PM from label
            shift_code = None
            for day_name, day_code in day_map.items():
                if day_name in label:
                    if "AM" in label:
                        shift_code = f"{day_code}AM"
                    elif "PM" in label:
                        shift_code = f"{day_code}PM"
                    break

            if not shift_code:
                continue

            # Extract employee amounts from detail lines
            for line in lines:
                # Pattern: "Employee Name: $XX.XX" at end of line (final amount)
                match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+): \$(\d+\.?\d*)\s*$', line)
                if match:
                    employee = match.group(1)
                    amount = float(match.group(2))

                    # Skip utility/support staff lines (they have "(utility)" suffix)
                    if "(utility)" in line.lower():
                        continue

                    if employee not in expected_values:
                        expected_values[employee] = {}
                    expected_values[employee][shift_code] = amount

        # Compare and correct per_shift
        for employee, shifts in expected_values.items():
            if employee not in per_shift:
                per_shift[employee] = {}
                corrections.append(f"Added missing employee to per_shift: {employee}")

            for shift_code, expected_amount in shifts.items():
                actual_amount = per_shift[employee].get(shift_code)

                if actual_amount is None:
                    # Missing shift - add it
                    per_shift[employee][shift_code] = expected_amount
                    corrections.append(
                        f"{employee} {shift_code}: ADDED ${expected_amount:.2f} (was missing)"
                    )
                elif abs(actual_amount - expected_amount) > 0.02:
                    # Wrong amount - correct it
                    old_amount = actual_amount
                    per_shift[employee][shift_code] = expected_amount
                    corrections.append(
                        f"{employee} {shift_code}: CORRECTED ${old_amount:.2f} → ${expected_amount:.2f}"
                    )

        # Recalculate weekly_totals from corrected per_shift
        for employee, shifts in per_shift.items():
            calculated_total = sum(shifts.values())
            old_total = weekly_totals.get(employee, 0)

            if abs(calculated_total - old_total) > 0.02:
                weekly_totals[employee] = round(calculated_total, 2)
                corrections.append(
                    f"{employee} weekly_total: CORRECTED ${old_total:.2f} → ${calculated_total:.2f}"
                )

        # Ensure all per_shift employees are in weekly_totals
        for employee in per_shift:
            if employee not in weekly_totals:
                total = sum(per_shift[employee].values())
                weekly_totals[employee] = round(total, 2)
                corrections.append(
                    f"{employee}: ADDED to weekly_totals (${total:.2f})"
                )

        return corrections


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

    # Extract shift code from filename (e.g., "ThAM.wav" -> "ThAM")
    filename = request.get("meta", {}).get("filename", "")
    shift_code = ""
    if filename:
        # Remove extension and extract shift code
        shift_code = filename.replace(".wav", "").replace(".mp3", "").replace(".m4a", "")
        log.info("Extracted shift code from filename: %s -> %s", filename, shift_code)

    # Parse the transcript
    agent = get_agent()
    return agent.parse_transcript(transcript, pay_period_hint, shift_code)
