"""Tests for payroll agent."""

import json
from unittest.mock import MagicMock, patch

from transrouter.src.agents.payroll_agent import (
    PayrollAgent,
    handle_payroll_request,
)
from transrouter.src.claude_client import ClaudeClient, ClaudeResponse


# Sample valid approval JSON for testing
SAMPLE_APPROVAL_JSON = {
    "out_base": "TipReport_010626_011226",
    "header": "Week of January 6–12, 2026",
    "shift_cols": [
        "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
        "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM",
        "SuAM", "SuPM"
    ],
    "per_shift": {
        "Austin Kelley": {"MAM": 150.00, "MPM": 200.00},
        "Brooke Neal": {"MAM": 150.00, "TPM": 180.00},
        "Ryan Alexander": {"MAM": 30.00, "MPM": 40.00}
    },
    "cook_tips": {},
    "weekly_totals": {
        "Austin Kelley": 350.00,
        "Brooke Neal": 330.00,
        "Ryan Alexander": 70.00
    },
    "detail_blocks": [
        ["Mon Jan 6 — AM (tip pool)", [
            "Pool: Austin $200 + Brooke $200 = $400",
            "Tipout to Ryan: $60",
            "Each server: $170"
        ]]
    ]
}


def create_mock_claude_client(response_json: dict) -> ClaudeClient:
    """Create a mock Claude client that returns the given JSON."""
    mock_client = MagicMock(spec=ClaudeClient)
    mock_client.call.return_value = ClaudeResponse(
        success=True,
        content=json.dumps(response_json),
        json_data=response_json,
        model="claude-sonnet-4-20250514",
        usage={"input_tokens": 1000, "output_tokens": 500},
    )
    return mock_client


def test_payroll_agent_parse_transcript_success():
    """Test successful transcript parsing."""
    mock_client = create_mock_claude_client(SAMPLE_APPROVAL_JSON)
    agent = PayrollAgent(claude_client=mock_client)

    result = agent.parse_transcript("Test payroll transcript...")

    assert result["status"] == "success"
    assert result["agent"] == "payroll"
    assert result["approval_json"] == SAMPLE_APPROVAL_JSON
    assert "usage" in result


def test_payroll_agent_validates_required_keys():
    """Test that agent validates required JSON keys."""
    invalid_json = {"out_base": "test"}  # Missing required keys

    mock_client = create_mock_claude_client(invalid_json)
    agent = PayrollAgent(claude_client=mock_client)

    result = agent.parse_transcript("Test transcript")

    assert result["status"] == "error"
    assert "Missing required keys" in result["error"]


def test_payroll_agent_validates_shift_cols():
    """Test that agent validates shift_cols array."""
    bad_json = SAMPLE_APPROVAL_JSON.copy()
    bad_json["shift_cols"] = ["MAM", "MPM"]  # Wrong array

    mock_client = create_mock_claude_client(bad_json)
    agent = PayrollAgent(claude_client=mock_client)

    result = agent.parse_transcript("Test transcript")

    assert result["status"] == "error"
    assert "shift_cols" in result["error"]


def test_payroll_agent_validates_weekly_totals_coverage():
    """Test that all employees appear in weekly_totals."""
    bad_json = SAMPLE_APPROVAL_JSON.copy()
    bad_json = {**bad_json}  # Shallow copy
    bad_json["weekly_totals"] = {"Austin Kelley": 350.00}  # Missing others

    mock_client = create_mock_claude_client(bad_json)
    agent = PayrollAgent(claude_client=mock_client)

    result = agent.parse_transcript("Test transcript")

    assert result["status"] == "error"
    assert "missing from weekly_totals" in result["error"].lower()


def test_payroll_agent_handles_api_error():
    """Test handling of Claude API errors."""
    mock_client = MagicMock(spec=ClaudeClient)
    mock_client.call.return_value = ClaudeResponse(
        success=False,
        content="",
        error="API rate limit exceeded",
    )

    agent = PayrollAgent(claude_client=mock_client)
    result = agent.parse_transcript("Test transcript")

    assert result["status"] == "error"
    assert "API" in result["error"]


def test_payroll_agent_handles_no_json_in_response():
    """Test handling when Claude doesn't return valid JSON."""
    mock_client = MagicMock(spec=ClaudeClient)
    mock_client.call.return_value = ClaudeResponse(
        success=True,
        content="I couldn't parse that transcript properly.",
        json_data=None,  # No JSON extracted
    )

    agent = PayrollAgent(claude_client=mock_client)
    result = agent.parse_transcript("Test transcript")

    assert result["status"] == "error"
    assert "JSON" in result["error"]


def test_handle_payroll_request_extracts_transcript():
    """Test that handle_payroll_request extracts transcript from meta."""
    mock_client = create_mock_claude_client(SAMPLE_APPROVAL_JSON)

    with patch("transrouter.src.agents.payroll_agent.get_agent") as mock_get:
        mock_agent = PayrollAgent(claude_client=mock_client)
        mock_get.return_value = mock_agent

        request = {
            "intent_type": "update",
            "entities": {},
            "meta": {"transcript": "Payroll transcript here..."}
        }

        result = handle_payroll_request(request)

        assert result["status"] == "success"
        assert result["agent"] == "payroll"


def test_handle_payroll_request_no_transcript_returns_error():
    """Test error when no transcript in request."""
    request = {
        "intent_type": "update",
        "entities": {},
        "meta": {}  # No transcript
    }

    result = handle_payroll_request(request)

    assert result["status"] == "error"
    assert "No transcript" in result["error"]


def test_payroll_agent_system_prompt_built():
    """Test that system prompt is built and cached."""
    mock_client = create_mock_claude_client(SAMPLE_APPROVAL_JSON)
    agent = PayrollAgent(claude_client=mock_client)

    # Access system_prompt property
    prompt = agent.system_prompt

    assert len(prompt) > 0
    assert "Payroll Agent" in prompt
    assert "tip pool" in prompt.lower()

    # Second access should return same (cached) prompt
    prompt2 = agent.system_prompt
    assert prompt == prompt2
