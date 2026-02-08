"""Tier 1: Test the new process_audio/process_text agent methods — mocked.

Verifies the self-contained pipelines return correct dict structure
without calling any real APIs.
"""

import json
import pytest
from unittest.mock import MagicMock, patch

from tests.conftest import SAMPLE_PAYROLL_APPROVAL_JSON, SAMPLE_INVENTORY_JSON


# ============================================================================
# PayrollAgent.process_audio (mocked)
# ============================================================================


class TestPayrollProcessAudio:
    """Test PayrollAgent.process_audio() with mocked ASR + Claude."""

    def _make_agent(self, approval_json):
        from transrouter.src.agents.payroll_agent import PayrollAgent
        from transrouter.src.claude_client import ClaudeResponse

        mock_client = MagicMock()
        mock_client.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(approval_json),
            json_data=approval_json,
            model="claude-sonnet-4-20250514",
            usage={"input_tokens": 1000, "output_tokens": 500},
        )
        return PayrollAgent(claude_client=mock_client)

    def _mock_asr(self, transcript="Monday AM shift. Austin Kelley $200."):
        from transrouter.src.schemas import TranscriptResult
        mock = MagicMock()
        mock.transcribe.return_value = TranscriptResult(
            transcript=transcript,
            confidence=0.95,
        )
        return mock

    @patch("transrouter.src.agents.payroll_agent.get_asr_provider")
    def test_success_returns_correct_structure(self, mock_get_asr):
        mock_get_asr.return_value = self._mock_asr()
        agent = self._make_agent(SAMPLE_PAYROLL_APPROVAL_JSON)

        result = agent.process_audio(b"fake-audio-bytes")

        assert result["status"] == "success"
        assert "transcript" in result
        assert "approval_json" in result
        assert isinstance(result["approval_json"], dict)

    @patch("transrouter.src.agents.payroll_agent.get_asr_provider")
    def test_empty_transcript_returns_error(self, mock_get_asr):
        mock_get_asr.return_value = self._mock_asr(transcript="")
        agent = self._make_agent(SAMPLE_PAYROLL_APPROVAL_JSON)

        result = agent.process_audio(b"fake-audio-bytes")

        assert result["status"] == "error"
        assert "empty" in result["error"].lower()

    @patch("transrouter.src.agents.payroll_agent.get_asr_provider")
    def test_passes_shift_code_through(self, mock_get_asr):
        mock_get_asr.return_value = self._mock_asr()
        agent = self._make_agent(SAMPLE_PAYROLL_APPROVAL_JSON)

        # Should not crash with shift_code
        result = agent.process_audio(b"fake-audio-bytes", shift_code="ThPM")
        assert result["status"] == "success"


# ============================================================================
# PayrollAgent.process_with_clarification_dict (mocked)
# ============================================================================


class TestPayrollProcessWithClarification:
    """Test PayrollAgent.process_with_clarification_dict() with mocked Claude."""

    def _make_agent(self, approval_json):
        from transrouter.src.agents.payroll_agent import PayrollAgent
        from transrouter.src.claude_client import ClaudeResponse

        mock_client = MagicMock()
        mock_client.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(approval_json),
            json_data=approval_json,
            model="claude-sonnet-4-20250514",
            usage={"input_tokens": 1000, "output_tokens": 500},
        )
        return PayrollAgent(claude_client=mock_client)

    def test_returns_success_dict(self):
        agent = self._make_agent(SAMPLE_PAYROLL_APPROVAL_JSON)
        result = agent.process_with_clarification_dict(
            transcript="Monday AM shift. Austin Kelley $200.",
        )
        assert result["status"] == "success"
        assert "approval_json" in result

    def test_accepts_clarification_dicts(self):
        agent = self._make_agent(SAMPLE_PAYROLL_APPROVAL_JSON)
        result = agent.process_with_clarification_dict(
            transcript="Monday AM shift. Austin Kelley $200.",
            clarifications=[
                {"question_id": "q_test", "answer": "Yes, correct", "confidence": 1.0},
            ],
            conversation_id=None,
        )
        assert result["status"] == "success"


# ============================================================================
# InventoryAgent.process_audio (mocked)
# ============================================================================


class TestInventoryProcessAudio:
    """Test InventoryAgent.process_audio() with mocked ASR + Claude."""

    def _make_agent(self, inventory_json):
        from transrouter.src.agents.inventory_agent import InventoryAgent
        from transrouter.src.claude_client import ClaudeResponse

        mock_client = MagicMock()
        mock_client.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(inventory_json),
            json_data=inventory_json,
            model="claude-sonnet-4-20250514",
            usage={"input_tokens": 500, "output_tokens": 200},
        )
        return InventoryAgent(claude_client=mock_client)

    def _mock_asr(self, transcript="7 Coors Lights, 12 Michelob Ultras"):
        from transrouter.src.schemas import TranscriptResult
        mock = MagicMock()
        mock.transcribe.return_value = TranscriptResult(
            transcript=transcript,
            confidence=0.95,
        )
        return mock

    @patch("transrouter.src.agents.inventory_agent.get_asr_provider")
    def test_success_returns_correct_structure(self, mock_get_asr):
        mock_get_asr.return_value = self._mock_asr()
        agent = self._make_agent(SAMPLE_INVENTORY_JSON)

        result = agent.process_audio(b"fake-audio-bytes", category="bar")

        assert result["status"] == "success"
        assert "transcript" in result
        assert "approval_json" in result
        assert isinstance(result["approval_json"], dict)

    @patch("transrouter.src.agents.inventory_agent.get_asr_provider")
    def test_empty_transcript_returns_error(self, mock_get_asr):
        mock_get_asr.return_value = self._mock_asr(transcript="")
        agent = self._make_agent(SAMPLE_INVENTORY_JSON)

        result = agent.process_audio(b"fake-audio-bytes")

        assert result["status"] == "error"
        assert "empty" in result["error"].lower()


# ============================================================================
# InventoryAgent.process_text (mocked)
# ============================================================================


class TestInventoryProcessText:
    """Test InventoryAgent.process_text() with mocked Claude."""

    def _make_agent(self, inventory_json):
        from transrouter.src.agents.inventory_agent import InventoryAgent
        from transrouter.src.claude_client import ClaudeResponse

        mock_client = MagicMock()
        mock_client.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(inventory_json),
            json_data=inventory_json,
            model="claude-sonnet-4-20250514",
            usage={"input_tokens": 500, "output_tokens": 200},
        )
        return InventoryAgent(claude_client=mock_client)

    def test_success_returns_correct_structure(self):
        agent = self._make_agent(SAMPLE_INVENTORY_JSON)
        result = agent.process_text("7 Coors Lights, 12 Michelob Ultras", category="bar")

        assert result["status"] == "success"
        assert "transcript" in result
        assert "approval_json" in result

    def test_transcript_preserved_in_response(self):
        agent = self._make_agent(SAMPLE_INVENTORY_JSON)
        transcript = "Back bar inventory: 3 bottles of Tito's"
        result = agent.process_text(transcript, category="bar")

        assert result["transcript"] == transcript

    def test_error_propagated_from_agent(self):
        from transrouter.src.agents.inventory_agent import InventoryAgent
        from transrouter.src.claude_client import ClaudeResponse

        mock_client = MagicMock()
        mock_client.call.return_value = ClaudeResponse(
            success=False,
            content="",
            error="API rate limit exceeded",
        )
        agent = InventoryAgent(claude_client=mock_client)
        result = agent.process_text("test", category="bar")

        assert result["status"] == "error"
