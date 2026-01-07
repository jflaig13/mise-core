"""Integration tests for the full transrouter pipeline with payroll agent."""

import json
from unittest.mock import MagicMock, patch

from transrouter.src import transrouter_orchestrator as orch
from transrouter.src.schemas import RouterResponse
from transrouter.src.claude_client import ClaudeResponse


# Sample approval JSON that Claude would return
MOCK_APPROVAL_JSON = {
    "out_base": "TipReport_122925_010426",
    "header": "Week of December 29 – January 4, 2026",
    "shift_cols": [
        "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
        "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM",
        "SuAM", "SuPM"
    ],
    "per_shift": {
        "Austin Kelley": {"MAM": 59.87, "MPM": 345.95},
        "Brooke Neal": {"MAM": 59.87, "MPM": 345.95},
        "Ryan Alexander": {"MAM": 41.10, "MPM": 46.34}
    },
    "cook_tips": {},
    "weekly_totals": {
        "Austin Kelley": 405.82,
        "Brooke Neal": 405.82,
        "Ryan Alexander": 87.44
    },
    "detail_blocks": [
        ["Mon Dec 29 — AM (tip pool)", [
            "Pool: Austin $80.89 + Brooke $79.94 = $160.83",
            "Tipout to Ryan: $41.10",
            "Pool after tipout: $119.73",
            "Each server: $59.87"
        ]]
    ]
}


SAMPLE_TRANSCRIPT = """
This is the payroll recording for pay period December 29th 2025 to January
4th 2026. Starting off with Monday December 29th AM shift. Ryan was utility.
Austin before tipout $80.89 food sales $275. Brooke before tipout $79.94
food sales $547.
"""


def test_full_pipeline_payroll_routing():
    """Test that payroll transcript routes to payroll agent and returns approval JSON."""

    # Mock the Claude client at the module level
    with patch("transrouter.src.agents.payroll_agent.ClaudeClient") as MockClient:
        # Configure mock
        mock_instance = MagicMock()
        mock_instance.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(MOCK_APPROVAL_JSON),
            json_data=MOCK_APPROVAL_JSON,
            model="claude-sonnet-4-20250514",
            usage={"input_tokens": 2000, "output_tokens": 1000},
        )
        MockClient.return_value = mock_instance

        # Clear any cached agent
        import transrouter.src.agents.payroll_agent as pa
        pa._default_agent = None

        # Route the transcript through the full pipeline
        response = orch.handle_text_request(
            SAMPLE_TRANSCRIPT,
            {"source": "test", "transcript": SAMPLE_TRANSCRIPT}
        )

        # Verify routing
        assert isinstance(response, RouterResponse)
        assert response.domain == "payroll"
        assert response.errors == []

        # Verify payload contains agent response
        payload = response.payload
        assert payload is not None
        assert payload.get("agent") == "payroll"
        assert payload.get("status") == "success"

        # Verify approval JSON is present
        approval = payload.get("approval_json")
        assert approval is not None
        assert approval.get("out_base") == "TipReport_122925_010426"
        assert "Austin Kelley" in approval.get("weekly_totals", {})


def test_pipeline_preserves_transcript_in_response():
    """Test that the transcript is preserved in the router response."""
    with patch("transrouter.src.agents.payroll_agent.ClaudeClient") as MockClient:
        mock_instance = MagicMock()
        mock_instance.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(MOCK_APPROVAL_JSON),
            json_data=MOCK_APPROVAL_JSON,
        )
        MockClient.return_value = mock_instance

        import transrouter.src.agents.payroll_agent as pa
        pa._default_agent = None

        response = orch.handle_text_request(SAMPLE_TRANSCRIPT, {})

        assert response.transcript == SAMPLE_TRANSCRIPT


def test_pipeline_inventory_still_returns_not_implemented():
    """Test that inventory domain still returns not_implemented."""
    transcript = "I need to count the inventory for beer and wine"

    response = orch.handle_text_request(transcript, {})

    assert response.domain == "inventory"
    assert response.payload.get("status") == "not_implemented"


def test_pipeline_extracts_entities():
    """Test that entities are extracted from transcript."""
    with patch("transrouter.src.agents.payroll_agent.ClaudeClient") as MockClient:
        mock_instance = MagicMock()
        mock_instance.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(MOCK_APPROVAL_JSON),
            json_data=MOCK_APPROVAL_JSON,
        )
        MockClient.return_value = mock_instance

        import transrouter.src.agents.payroll_agent as pa
        pa._default_agent = None

        response = orch.handle_text_request(SAMPLE_TRANSCRIPT, {})

        # Should extract dates and numbers
        assert response.entities is not None
        # December 29 or similar date patterns should be found
        assert len(response.entities) > 0


def test_pipeline_handles_claude_error_gracefully():
    """Test that Claude errors are handled and returned in response."""
    with patch("transrouter.src.agents.payroll_agent.ClaudeClient") as MockClient:
        mock_instance = MagicMock()
        mock_instance.call.return_value = ClaudeResponse(
            success=False,
            content="",
            error="Connection timeout",
        )
        MockClient.return_value = mock_instance

        import transrouter.src.agents.payroll_agent as pa
        pa._default_agent = None

        response = orch.handle_text_request(
            SAMPLE_TRANSCRIPT,
            {"transcript": SAMPLE_TRANSCRIPT}
        )

        assert response.domain == "payroll"
        # The router itself doesn't error, but the payload contains the error
        payload = response.payload
        assert payload.get("status") == "error"
        assert "timeout" in payload.get("error", "").lower()
