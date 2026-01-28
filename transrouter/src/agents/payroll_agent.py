"""Payroll Agent - Parses payroll transcripts using Claude.

This agent receives payroll transcripts from the transrouter and uses
Claude to parse them into structured approval JSON matching the LPM schema.

UPDATED (Phase 1): Added multi-turn clarification support.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, List
import uuid

from ..claude_client import ClaudeClient, ClaudeConfig, ClaudeResponse
from ..prompts.payroll_prompt import (
    build_payroll_system_prompt,
    build_payroll_user_prompt,
)
from ..schemas import (
    ParseResult,
    ClarificationQuestion,
    ClarificationResponse,
    QuestionType,
)
from ..conversation_manager import ConversationManager

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
        conversation_manager: Optional[ConversationManager] = None,
    ):
        """Initialize payroll agent.

        Args:
            claude_client: Optional pre-configured Claude client.
            config: Optional configuration dict (used if claude_client not provided).
            conversation_manager: Optional conversation manager for multi-turn flows.
        """
        if claude_client:
            self.claude_client = claude_client
        else:
            claude_config = ClaudeConfig.from_dict(config or {})
            self.claude_client = ClaudeClient(config=claude_config)

        self._system_prompt: Optional[str] = None

        # NEW (Phase 1): Conversation manager for clarification flows
        self.conversation_manager = conversation_manager or ConversationManager()

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

    # ========================================================================
    # NEW (Phase 1): Multi-Turn Clarification Support
    # ========================================================================

    def parse_with_clarification(
        self,
        transcript: str,
        pay_period_hint: str = "",
        shift_code: str = "",
        clarifications: Optional[List[ClarificationResponse]] = None,
        conversation_id: Optional[str] = None,
    ) -> ParseResult:
        """
        Parse transcript with clarification support (multi-turn).

        This is the NEW entry point for clarification-aware parsing.
        It wraps the existing parse_transcript() and adds missing data detection.

        Args:
            transcript: Payroll transcript text
            pay_period_hint: Optional pay period hint
            shift_code: Optional shift code
            clarifications: Previous clarification responses (if resuming)
            conversation_id: Conversation ID (if resuming)

        Returns:
            ParseResult with status (success/needs_clarification/error)
        """
        # Create or load conversation
        if conversation_id:
            state = self.conversation_manager.load_conversation(conversation_id)
            if state is None:
                log.error(f"Conversation {conversation_id} not found")
                return ParseResult(
                    status="error",
                    conversation_id=conversation_id,
                    error=f"Conversation {conversation_id} not found"
                )
        else:
            # New conversation
            state = self.conversation_manager.create_conversation(
                skill_name="payroll",
                original_input={
                    "transcript": transcript,
                    "pay_period_hint": pay_period_hint,
                    "shift_code": shift_code,
                }
            )
            conversation_id = state.conversation_id

        # If clarifications provided, add them to conversation
        if clarifications:
            state = self.conversation_manager.add_clarifications_received(
                conversation_id,
                clarifications
            )

        # Build enriched prompt with clarifications
        if state.clarifications_received:
            user_prompt = self._build_clarification_prompt(
                transcript,
                state.clarifications_received,
                pay_period_hint,
                shift_code
            )
        else:
            user_prompt = build_payroll_user_prompt(transcript, pay_period_hint, shift_code)

        # Call Claude API
        log.info(f"Parsing payroll (conversation={conversation_id}, iteration={state.iteration})")
        response: ClaudeResponse = self.claude_client.call(
            system_prompt=self.system_prompt,
            user_content=user_prompt,
            extract_json=True,
        )

        # Handle API failure
        if not response.success:
            return ParseResult(
                status="error",
                conversation_id=conversation_id,
                error=response.error,
                model_used=response.model,
                tokens_used=response.usage
            )

        # Handle JSON extraction failure
        if not response.json_data:
            return ParseResult(
                status="error",
                conversation_id=conversation_id,
                error="Failed to extract JSON from response",
                model_used=response.model,
                tokens_used=response.usage
            )

        # Validate approval JSON
        validation_error = self._validate_approval_json(response.json_data)
        if validation_error:
            return ParseResult(
                status="error",
                conversation_id=conversation_id,
                error=validation_error,
                partial_result=response.json_data,
                model_used=response.model,
                tokens_used=response.usage
            )

        # Auto-correct inconsistencies
        corrections = self._auto_correct_approval_json(response.json_data)
        if corrections:
            log.info(f"Auto-corrected {len(corrections)} inconsistencies")

        # NEW: Detect missing data
        missing_data_questions = self.detect_missing_data(
            transcript,
            response.json_data,
            state
        )

        # If data is missing, return clarification request
        if missing_data_questions:
            log.info(f"Detected {len(missing_data_questions)} missing data points")
            self.conversation_manager.add_clarifications_needed(
                conversation_id,
                missing_data_questions
            )

            return ParseResult(
                status="needs_clarification",
                conversation_id=conversation_id,
                clarifications=missing_data_questions,
                partial_result=response.json_data,
                model_used=response.model,
                tokens_used=response.usage
            )

        # Success - parsing complete
        log.info(f"Successfully parsed payroll (conversation={conversation_id})")
        return ParseResult(
            status="success",
            conversation_id=conversation_id,
            approval_json=response.json_data,
            model_used=response.model,
            tokens_used=response.usage
        )

    def detect_missing_data(
        self,
        transcript: str,
        approval_json: Dict[str, Any],
        conversation_state,
    ) -> List[ClarificationQuestion]:
        """
        Detect missing or ambiguous data in approval JSON.

        This implements the grounding rule: "If it impacts money, it must be explicit."

        Args:
            transcript: Original transcript
            approval_json: Parsed approval JSON
            conversation_state: Current conversation state

        Returns:
            List of clarification questions (empty if no missing data)
        """
        questions = []

        # Check 1: Employees with amounts but missing hours
        # (This is an example - full implementation would be more comprehensive)
        per_shift = approval_json.get("per_shift", {})

        for employee, shifts in per_shift.items():
            # If employee worked multiple shifts but we don't have hours data,
            # we might need to ask (depending on restaurant policy)
            # For now, we'll skip this check as hours aren't in current schema

            # Check 2: Very low amounts (might be missing)
            for shift_code, amount in shifts.items():
                if amount < 1.0:  # Less than $1 might be missing/error
                    # Don't ask about amounts already answered
                    existing_answer = self._find_existing_answer(
                        conversation_state,
                        f"amount_{employee}_{shift_code}"
                    )
                    if not existing_answer:
                        questions.append(ClarificationQuestion(
                            question_id=f"q_{uuid.uuid4().hex[:8]}_{employee}_{shift_code}",
                            question_text=f"Did {employee} really make ${amount:.2f} on {shift_code}? (Very low amount)",
                            question_type=QuestionType.UNUSUAL_PATTERN,
                            field_name="amount",
                            affected_entity=employee,
                            context=f"Amount ${amount:.2f} is unusually low for a shift",
                            priority="recommended"
                        ))

        # TODO: Add more detection logic:
        # - Missing tip pool mention when Fridays usually pool
        # - Employee mentioned but no amount parsed
        # - Ambiguous employee names (partial matches)
        # - Conflicting data (if we integrate with Toast/schedule later)

        return questions

    def _build_clarification_prompt(
        self,
        original_transcript: str,
        clarifications: List[ClarificationResponse],
        pay_period_hint: str = "",
        shift_code: str = "",
    ) -> str:
        """
        Build enriched prompt that includes clarification responses.

        Args:
            original_transcript: Original transcript
            clarifications: Clarification responses from manager
            pay_period_hint: Pay period hint
            shift_code: Shift code

        Returns:
            Enriched user prompt
        """
        # Start with base prompt
        base_prompt = build_payroll_user_prompt(original_transcript, pay_period_hint, shift_code)

        # Add clarifications section
        clarifications_text = "\n\n**CLARIFICATIONS PROVIDED BY MANAGER:**\n\n"
        for clarification in clarifications:
            clarifications_text += f"- Question ID: {clarification.question_id}\n"
            clarifications_text += f"  Answer: {clarification.answer}\n"
            if clarification.notes:
                clarifications_text += f"  Notes: {clarification.notes}\n"
            if clarification.source:
                clarifications_text += f"  Source: {clarification.source}\n"
            clarifications_text += "\n"

        clarifications_text += "**Please use these clarifications when parsing the transcript.**\n"

        return base_prompt + clarifications_text

    def _find_existing_answer(
        self,
        conversation_state,
        field_identifier: str
    ) -> Optional[ClarificationResponse]:
        """
        Check if a clarification has already been answered.

        Args:
            conversation_state: Current conversation state
            field_identifier: Field identifier to search for

        Returns:
            ClarificationResponse if found, None otherwise
        """
        for response in conversation_state.clarifications_received:
            if field_identifier in response.question_id:
                return response
        return None

    # ========================================================================
    # End of Phase 1 additions
    # ========================================================================

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
            # For servers with tipouts, we need the AFTER tipout amount (after the = sign)
            # Pattern 1: "Name: $XX.XX - $YY.YY = $ZZ.ZZ" (with tipout calculation)
            # Pattern 2: "Name: $XX.XX" at end of line (simple, no tipout)
            for line in lines:
                employee = None
                amount = None

                # First try: calculation line with tipout (e.g., "Austin Kelley: $155.13 - $16.50 = $138.63")
                calc_match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+): \$[\d.]+ - \$[\d.]+ = \$(\d+\.?\d*)', line)
                if calc_match:
                    employee = calc_match.group(1)
                    amount = float(calc_match.group(2))  # AFTER tipout amount
                else:
                    # Fallback: simple amount line (e.g., "Kevin Worley: $99.98")
                    simple_match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+): \$(\d+\.?\d*)\s*$', line)
                    if simple_match:
                        employee = simple_match.group(1)
                        amount = float(simple_match.group(2))

                if employee and amount is not None:

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
            # For servers with tipouts, we need the AFTER tipout amount (after the = sign)
            for line in lines:
                employee = None
                amount = None

                # Skip utility/support staff lines (they have "(utility)" etc suffix)
                if "(utility)" in line.lower() or "(busser)" in line.lower() or "(expo)" in line.lower() or "(host)" in line.lower():
                    continue

                # First try: calculation line with tipout (e.g., "Austin Kelley: $155.13 - $16.50 = $138.63")
                calc_match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+): \$[\d.]+ - \$[\d.]+ = \$(\d+\.?\d*)', line)
                if calc_match:
                    employee = calc_match.group(1)
                    amount = float(calc_match.group(2))  # AFTER tipout amount
                else:
                    # Fallback: simple amount line (e.g., "Kevin Worley: $99.98")
                    simple_match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+): \$(\d+\.?\d*)\s*$', line)
                    if simple_match:
                        employee = simple_match.group(1)
                        amount = float(simple_match.group(2))

                if employee and amount is not None:
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
