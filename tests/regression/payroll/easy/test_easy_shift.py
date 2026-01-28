"""
Regression Test: Easy Shift (Baseline)

CATEGORY: Easy / Happy Path
PRIORITY: Critical - This should ALWAYS pass

PURPOSE:
Standard shift with clear data - no edge cases, no missing info.
This is the baseline test that validates core parsing functionality.

EXPECTED BEHAVIOR:
- Clean transcript parsing
- Correct employee name normalization
- Accurate amount extraction
- Proper role assignment (server vs support)
- Correct shift code mapping
"""

import pytest
from pathlib import Path


# Test input
TRANSCRIPT = """
Monday January 6 2026 AM shift.
Austin $150
Brooke $150
Ryan $30
"""

# Expected output
EXPECTED_EMPLOYEES = {
    "Austin Kelley": {
        "amount": 150.00,
        "role": "Server",
        "category": "server"
    },
    "Brooke Neal": {
        "amount": 150.00,
        "role": "Server",
        "category": "server"
    },
    "Ryan Alexander": {
        "amount": 30.00,
        "role": "utility",
        "category": "support"
    }
}

EXPECTED_SHIFT_CODE = "MAM"  # Monday AM
EXPECTED_DATE = "2026-01-06"


def test_easy_shift_parsing():
    """
    Test that a straightforward shift transcript parses correctly.

    This is the baseline test - if this fails, core functionality is broken.
    """
    # TODO: Import actual parsing function
    # from transrouter.src.agents.payroll_agent import parse_transcript

    # result = parse_transcript(TRANSCRIPT)

    # Assertions
    # assert result["status"] == "success"
    # assert result["shift_code"] == EXPECTED_SHIFT_CODE
    # assert result["date"] == EXPECTED_DATE

    # # Verify each employee
    # for employee_name, expected_data in EXPECTED_EMPLOYEES.items():
    #     employee_result = result["employees"][employee_name]
    #     assert employee_result["amount"] == expected_data["amount"]
    #     assert employee_result["role"] == expected_data["role"]
    #     assert employee_result["category"] == expected_data["category"]

    # Placeholder until parsing function is imported
    pytest.skip("Parsing function integration pending")


def test_easy_shift_approval_json_structure():
    """
    Test that the approval JSON has the correct structure for an easy shift.
    """
    # TODO: Test approval JSON generation
    # Expected structure:
    # {
    #     "out_base": "TipReport_...",
    #     "header": "Week of ...",
    #     "shift_cols": [...],
    #     "per_shift": {
    #         "Austin Kelley": {"MAM": 150.00},
    #         "Brooke Neal": {"MAM": 150.00},
    #         "Ryan Alexander": {"MAM": 30.00}
    #     },
    #     "weekly_totals": {...},
    #     "detail_blocks": [...]
    # }

    pytest.skip("Approval JSON validation pending")


def test_easy_shift_no_clarifications_needed():
    """
    Test that a clean shift doesn't trigger clarification requests.

    GROUNDING TEST: System should NOT ask questions when all info is present.
    """
    # Expected clarifications: [] (none)
    # If this triggers clarifications, it means the system is being too cautious

    pytest.skip("Clarification logic integration pending")


def test_easy_shift_deterministic():
    """
    Test that running the same transcript twice produces identical output.

    CRITICAL: Same input must always produce same output.
    """
    # Run parsing twice
    # result1 = parse_transcript(TRANSCRIPT)
    # result2 = parse_transcript(TRANSCRIPT)

    # assert result1 == result2

    pytest.skip("Determinism test pending")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
