"""
Regression Test: No Assumptions / Grounding

CATEGORY: Grounding / "QAnon Shaman" Problem
PRIORITY: CRITICAL - Core trust and correctness

PURPOSE:
Ensure Mise NEVER assumes information that's not explicitly in the source data.

THE "QANON SHAMAN" PROBLEM (CoCounsel doc, page 5):
Example: QAnon Shaman was a public figure LLMs "know" about.
But if he's not mentioned in the legal document being analyzed,
CoCounsel must NOT reference him - even if contextually relevant.

For Mise, this means:
- Don't assume Tucker usually works 6 hours
- Don't assume Emily usually closes
- Don't assume tip pool is usually on
- Don't assume typical sales amounts
- Don't infer roles from patterns

GROUNDING RULE: If it impacts money, it must be supported by explicit evidence.

FAILURE MODE: "Confident wrong"
- Wrong answer with high confidence → user loses trust immediately
- Worse than saying "I don't know"
"""

import pytest


def test_no_assume_typical_hours():
    """
    Test that Mise doesn't assume typical hours based on historical patterns.

    SCENARIO:
    - Austin has worked 6 hours every Monday PM for the last 8 weeks
    - This Monday's transcript mentions Austin but not hours
    - Mise must NOT auto-fill 6 hours
    """
    transcript = "Monday PM shift. Austin $150."

    # With historical data showing Austin always works 6 hours:
    # historical_data = {
    #     "Austin Kelley": {"typical_pm_hours": 6.0, "confidence": 0.95}
    # }

    # result = parse_transcript(transcript, historical_data=historical_data)

    # MUST NOT contain auto-filled hours
    # assert "hours" not in result["employees"]["Austin Kelley"]
    # OR must explicitly flag as "inferred" and require confirmation
    # assert result["employees"]["Austin Kelley"]["hours_source"] != "assumed"

    pytest.skip("Grounding enforcement pending")


def test_no_assume_tip_pool_status():
    """
    Test that Mise doesn't assume tip pool based on usual behavior.

    SCENARIO:
    - Restaurant always pools tips on busy nights
    - Transcript doesn't mention tip pool
    - Mise must NOT assume pooling
    """
    transcript = "Friday PM shift. Austin $200. Brooke $180."

    # Typical pattern: Friday PM always pools
    # pattern_data = {"Friday PM": {"tip_pool": True, "historical_frequency": 1.0}}

    # result = parse_transcript(transcript, pattern_data=pattern_data)

    # Should either:
    # 1. Ask: "Should this be tip pool?" OR
    # 2. Default to restaurant's explicit policy (not pattern)
    # assert result["tip_pool_source"] in ["explicit", "policy", "clarification_needed"]
    # assert result["tip_pool_source"] != "inferred_from_pattern"

    pytest.skip("Tip pool grounding pending")


def test_no_infer_role_from_typical():
    """
    Test that Mise doesn't infer role based on typical assignment.

    SCENARIO:
    - Ryan is always utility (support staff)
    - One shift Ryan fills in as a server
    - Transcript says "Ryan $150" (server-level amount)
    - Mise must NOT auto-assign "utility" role
    """
    transcript = "Monday AM. Ryan $150."  # Server-level amount

    # Historical data: Ryan is always utility
    # employee_data = {
    #     "Ryan Alexander": {"typical_role": "utility", "historical_accuracy": 0.99}
    # }

    # result = parse_transcript(transcript, employee_data=employee_data)

    # Must either:
    # 1. Ask: "Ryan usually works utility. Is this a server shift?" OR
    # 2. Infer from amount (if policy allows) and flag for review
    # assert result["employees"]["Ryan Alexander"]["role_source"] == "amount_based"
    # assert result["employees"]["Ryan Alexander"]["flag_for_review"] == True

    pytest.skip("Role inference grounding pending")


def test_no_assume_sales_amounts():
    """
    Test that Mise doesn't fill in missing sales data from averages.

    SCENARIO:
    - Typical Friday PM sales: $2,500
    - Transcript mentions tipout % but not sales
    - Mise must NOT use average sales to calculate tipout
    """
    transcript = "Friday PM. Austin $180. Tipout 5% to utility."

    # Historical data: Friday PM averages $2,500 sales
    # sales_data = {"Friday PM": {"avg_sales": 2500.00, "std_dev": 200.00}}

    # result = parse_transcript(transcript, sales_data=sales_data)

    # Should request sales amount, not assume
    # assert "sales_amount" in result["missing_fields"]
    # assert result["employees"]["utility"]["tipout_source"] != "calculated_from_avg_sales"

    pytest.skip("Sales grounding pending")


def test_no_pattern_based_employee_matching():
    """
    Test that Mise doesn't match employees based on typical pairing patterns.

    SCENARIO:
    - Austin and Brooke always work together on Mondays
    - Transcript mentions "Austin $150" but not Brooke
    - Mise must NOT add Brooke automatically
    """
    transcript = "Monday AM. Austin $150. Ryan $30."

    # Pattern data: Austin and Brooke always paired
    # pairing_patterns = {
    #     "Monday AM": {"typical_pairs": [("Austin Kelley", "Brooke Neal")]}
    # }

    # result = parse_transcript(transcript, pairing_patterns=pairing_patterns)

    # Brooke should NOT appear unless explicitly mentioned
    # assert "Brooke Neal" not in result["employees"]

    pytest.skip("Employee matching grounding pending")


def test_explicit_source_attribution():
    """
    Test that every data point can be traced to its source.

    For auditing and trust, every piece of data should have provenance:
    - "amount": 150.00, "source": "transcript line 3"
    - "hours": 6.0, "source": "manager_confirmation"
    - "role": "server", "source": "inferred_from_roster"
    """
    transcript = "Monday AM. Austin $150."

    # result = parse_transcript(transcript)

    # Every field should have source attribution
    # austin = result["employees"]["Austin Kelley"]
    # assert austin["amount_source"] == "transcript"
    # assert austin["name_source"] == "roster_normalized"
    # if "role" in austin:
    #     assert "role_source" in austin

    pytest.skip("Source attribution pending")


def test_warn_on_unusual_patterns():
    """
    Test that Mise flags unusual patterns for review without auto-correcting.

    SCENARIO:
    - Ryan (utility) usually makes $30-40
    - Transcript says "Ryan $150" (server amount)
    - Mise should FLAG this as unusual, not auto-correct it
    """
    transcript = "Monday AM. Ryan $150."

    # Historical data: Ryan's typical range is $30-40
    # employee_ranges = {
    #     "Ryan Alexander": {"typical_range": (30.00, 40.00), "role": "utility"}
    # }

    # result = parse_transcript(transcript, employee_ranges=employee_ranges)

    # Should flag but NOT change
    # assert result["employees"]["Ryan Alexander"]["amount"] == 150.00
    # assert result["employees"]["Ryan Alexander"]["flagged"] == True
    # assert result["employees"]["Ryan Alexander"]["flag_reason"] == "amount_outside_typical_range"

    pytest.skip("Pattern warning logic pending")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
