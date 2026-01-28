"""
Regression Test: Missing Clock-Out

CATEGORY: Missing Data / Edge Case
PRIORITY: Critical - Tests "QAnon Shaman" problem

PURPOSE:
Test that Mise handles missing information correctly without assuming/hallucinating.

THE PROBLEM (from CoCounsel doc, page 5-6):
If Mise "knows" that:
- "Tucker usually works 6 hours"
- "Emily usually closes"

But the transcript doesn't mention hours/time → Mise must NOT assume.

GROUNDING RULE: If it impacts money, it must be supported by explicit evidence.

EXPECTED BEHAVIOR:
Option 1: Ask clarification - "How many hours did Tucker work?"
Option 2: Use policy - "Assume scheduled hours per restaurant policy"
Option 3: Block export - "Cannot process without hours worked"

WRONG BEHAVIOR (confident wrong):
- Assuming "Tucker usually works 6 hours so use 6"
- Inferring hours from sales data
- Using historical averages without manager confirmation
"""

import pytest


# Test input - notice NO HOURS mentioned
TRANSCRIPT_NO_HOURS = """
Monday January 6 2026 PM shift.
Austin worked.
Brooke worked.
Ryan helped.
"""

# Test input - partial hours
TRANSCRIPT_PARTIAL_HOURS = """
Monday January 6 2026 PM shift.
Austin 6 hours $150
Brooke worked $140
Ryan $30
"""


def test_missing_hours_triggers_clarification():
    """
    Test that completely missing hours information triggers clarification.

    EXPECTED: Mise should ask "How many hours did each person work?"
    NOT EXPECTED: Mise assumes typical/average hours
    """
    # result = parse_transcript(TRANSCRIPT_NO_HOURS)

    # # Should request clarification
    # assert result["status"] == "clarification_needed"
    # assert "hours" in result["clarification_question"].lower()
    # assert len(result["missing_fields"]) > 0

    pytest.skip("Clarification logic integration pending")


def test_partial_hours_identifies_missing():
    """
    Test that Mise identifies WHICH employees are missing hour data.

    If Austin has hours but Brooke doesn't, Mise should ask specifically about Brooke.
    """
    # result = parse_transcript(TRANSCRIPT_PARTIAL_HOURS)

    # # Should identify Brooke and Ryan as missing hours
    # assert "Brooke Neal" in result["missing_hours"]
    # assert "Ryan Alexander" in result["missing_hours"]
    # assert "Austin Kelley" not in result["missing_hours"]

    pytest.skip("Missing field detection pending")


def test_no_assumption_from_historical_data():
    """
    CRITICAL GROUNDING TEST: Mise must not use historical hours data.

    Even if Mise "knows" from previous weeks that:
    - Austin usually works 6 hours
    - Brooke usually closes (7-8 hours)

    It must NOT use that unless explicitly in the transcript or approved by manager.
    """
    # This test would need to:
    # 1. Load historical data showing Austin usually works 6 hours
    # 2. Parse transcript with Austin but no hours
    # 3. Verify Mise does NOT auto-fill 6 hours
    # 4. Verify Mise ASKS for hours instead

    pytest.skip("Historical data isolation test pending")


def test_missing_clock_out_policy_application():
    """
    Test that if restaurant has a policy, Mise applies it correctly.

    Example policy: "If clock-out missing, use scheduled end time"

    This is OK because it's an explicit policy, not an assumption.
    """
    # restaurant_policy = {
    #     "missing_clock_out": "use_scheduled_time",
    #     "schedule": {
    #         "Austin Kelley": {"PM": "4:30-9:00"}
    #     }
    # }

    # result = parse_transcript(
    #     TRANSCRIPT_NO_HOURS,
    #     policy=restaurant_policy
    # )

    # # Should apply policy, not ask (policy is explicit guidance)
    # assert result["status"] == "success"
    # assert result["applied_policy"] == "missing_clock_out: use_scheduled_time"

    pytest.skip("Policy application logic pending")


def test_block_export_without_critical_data():
    """
    Test that Mise blocks payroll export when critical data is missing.

    If hours are required for hourly employees and missing, export should fail.
    """
    # result = parse_transcript(TRANSCRIPT_NO_HOURS)
    # export_result = attempt_export(result)

    # assert export_result["status"] == "blocked"
    # assert "missing required data" in export_result["error"].lower()
    # assert export_result["blocking_reason"] == "hours_missing"

    pytest.skip("Export blocking logic pending")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
