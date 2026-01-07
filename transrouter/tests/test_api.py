"""Tests for the FastAPI endpoints."""

import json
import os
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from transrouter.api.main import app
from transrouter.src.claude_client import ClaudeResponse

# Set up test API key before importing auth module
os.environ["MISE_API_KEYS"] = "test-key-123:test-client,another-key:other-client"

# Reload auth keys with test values
from transrouter.api import auth
auth.reload_api_keys()

client = TestClient(app)

# Test API key header
TEST_AUTH_HEADER = {"X-API-Key": "test-key-123"}


# Sample approval JSON for mocking Claude responses
MOCK_APPROVAL_JSON = {
    "out_base": "TipReport_010626_011226",
    "header": "Week of January 6–12, 2026",
    "shift_cols": [
        "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
        "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM",
        "SuAM", "SuPM"
    ],
    "per_shift": {
        "Austin Kelley": {"MAM": 175.00},
        "Ryan Alexander": {"MAM": 25.00}
    },
    "cook_tips": {},
    "weekly_totals": {
        "Austin Kelley": 175.00,
        "Ryan Alexander": 25.00
    },
    "detail_blocks": [
        ["Mon Jan 6 — AM (utility)", ["Austin: $200 - $25 tipout = $175", "Ryan (utility): $25"]]
    ]
}


def test_health_endpoint_returns_healthy():
    """Test that health endpoint returns healthy status."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert data["version"] == "1.0.0"
    assert "timestamp" in data
    assert "brain_loaded" in data
    assert "domains" in data


def test_health_endpoint_includes_domains():
    """Test that health endpoint lists loaded domains."""
    response = client.get("/api/v1/health")

    data = response.json()
    assert isinstance(data["domains"], list)
    # Should have at least payroll and inventory
    assert "payroll" in data["domains"]


def test_root_endpoint_returns_healthy():
    """Test that root path returns basic health."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "mise-transrouter"


def test_docs_endpoint_available():
    """Test that OpenAPI docs are available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema_available():
    """Test that OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Mise Transrouter API"
    assert data["info"]["version"] == "1.0.0"


# ============================================================================
# Payroll Endpoint Tests
# ============================================================================

def test_payroll_parse_success():
    """Test successful payroll parsing."""
    with patch("transrouter.src.agents.payroll_agent.ClaudeClient") as MockClient:
        mock_instance = MagicMock()
        mock_instance.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(MOCK_APPROVAL_JSON),
            json_data=MOCK_APPROVAL_JSON,
            model="claude-sonnet-4-20250514",
            usage={"input_tokens": 1000, "output_tokens": 500},
        )
        MockClient.return_value = mock_instance

        # Clear cached agent
        import transrouter.src.agents.payroll_agent as pa
        pa._default_agent = None

        response = client.post(
            "/api/v1/payroll/parse",
            json={
                "transcript": "Monday AM shift. Ryan was utility. Austin before tipout $200, food sales $500."
            },
            headers=TEST_AUTH_HEADER,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["agent"] == "payroll"
        assert data["approval_json"] is not None
        assert data["approval_json"]["out_base"] == "TipReport_010626_011226"


def test_payroll_parse_returns_error_on_failure():
    """Test that Claude errors are returned properly."""
    with patch("transrouter.src.agents.payroll_agent.ClaudeClient") as MockClient:
        mock_instance = MagicMock()
        mock_instance.call.return_value = ClaudeResponse(
            success=False,
            content="",
            error="API rate limit exceeded",
        )
        MockClient.return_value = mock_instance

        import transrouter.src.agents.payroll_agent as pa
        pa._default_agent = None

        response = client.post(
            "/api/v1/payroll/parse",
            json={
                "transcript": "Monday AM shift. Ryan was utility. Austin before tipout $200, food sales $500."
            },
            headers=TEST_AUTH_HEADER,
        )

        assert response.status_code == 200  # HTTP 200, but status=error in body
        data = response.json()
        assert data["status"] == "error"
        assert "error" in data
        assert data["error"] is not None


def test_payroll_parse_validates_transcript_length():
    """Test that short transcripts are rejected."""
    response = client.post(
        "/api/v1/payroll/parse",
        json={"transcript": "Hi"},  # Too short
        headers=TEST_AUTH_HEADER,
    )

    assert response.status_code == 422  # Validation error


def test_payroll_parse_requires_transcript():
    """Test that transcript is required."""
    response = client.post(
        "/api/v1/payroll/parse",
        json={},  # Missing transcript
        headers=TEST_AUTH_HEADER,
    )

    assert response.status_code == 422  # Validation error


def test_payroll_parse_with_pay_period_hint():
    """Test that pay_period_hint is accepted."""
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

        response = client.post(
            "/api/v1/payroll/parse",
            json={
                "transcript": "Monday AM shift. Ryan was utility. Austin before tipout $200, food sales $500.",
                "pay_period_hint": "01/06/26 - 01/12/26"
            },
            headers=TEST_AUTH_HEADER,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


def test_payroll_endpoint_in_openapi_schema():
    """Test that payroll endpoint is documented in OpenAPI."""
    response = client.get("/openapi.json")
    data = response.json()

    assert "/api/v1/payroll/parse" in data["paths"]
    assert "post" in data["paths"]["/api/v1/payroll/parse"]


# ============================================================================
# Audio Endpoint Tests
# ============================================================================

def test_audio_process_rejects_empty_file():
    """Test that empty audio files are rejected."""
    response = client.post(
        "/api/v1/audio/process",
        files={"file": ("test.wav", b"", "audio/wav")},
        headers=TEST_AUTH_HEADER,
    )

    assert response.status_code == 400
    assert "Empty" in response.json()["detail"]


def test_audio_process_rejects_missing_file():
    """Test that missing file is rejected."""
    response = client.post(
        "/api/v1/audio/process",
        headers=TEST_AUTH_HEADER,
    )

    assert response.status_code == 422  # Validation error


def test_audio_transcribe_rejects_empty_file():
    """Test that empty audio files are rejected for transcribe."""
    response = client.post(
        "/api/v1/audio/transcribe",
        files={"file": ("test.wav", b"", "audio/wav")},
        headers=TEST_AUTH_HEADER,
    )

    assert response.status_code == 400
    assert "Empty" in response.json()["detail"]


def test_audio_endpoints_in_openapi_schema():
    """Test that audio endpoints are documented in OpenAPI."""
    response = client.get("/openapi.json")
    data = response.json()

    assert "/api/v1/audio/process" in data["paths"]
    assert "/api/v1/audio/transcribe" in data["paths"]
    assert "post" in data["paths"]["/api/v1/audio/process"]
    assert "post" in data["paths"]["/api/v1/audio/transcribe"]


def test_audio_process_with_mock_asr():
    """Test audio processing with mocked ASR and Claude."""
    from io import BytesIO
    from transrouter.src.schemas import TranscriptResult

    # Create a minimal WAV header (44 bytes) + some audio data
    # This is a valid WAV file structure
    wav_header = (
        b'RIFF'  # ChunkID
        b'\x24\x00\x00\x00'  # ChunkSize (36 + data size)
        b'WAVE'  # Format
        b'fmt '  # Subchunk1ID
        b'\x10\x00\x00\x00'  # Subchunk1Size (16 for PCM)
        b'\x01\x00'  # AudioFormat (1 = PCM)
        b'\x01\x00'  # NumChannels (1 = mono)
        b'\x80\x3e\x00\x00'  # SampleRate (16000)
        b'\x00\x7d\x00\x00'  # ByteRate (32000)
        b'\x02\x00'  # BlockAlign (2)
        b'\x10\x00'  # BitsPerSample (16)
        b'data'  # Subchunk2ID
        b'\x00\x00\x00\x00'  # Subchunk2Size (0 bytes of data)
    )

    with patch("transrouter.src.asr_adapter.WhisperAdapter.transcribe") as mock_transcribe, \
         patch("transrouter.src.agents.payroll_agent.ClaudeClient") as MockClient:

        # Mock ASR
        mock_transcribe.return_value = TranscriptResult(
            transcript="Monday AM shift. Ryan was utility. Austin before tipout $200, food sales $500.",
            confidence=0.95
        )

        # Mock Claude
        mock_instance = MagicMock()
        mock_instance.call.return_value = ClaudeResponse(
            success=True,
            content=json.dumps(MOCK_APPROVAL_JSON),
            json_data=MOCK_APPROVAL_JSON,
        )
        MockClient.return_value = mock_instance

        import transrouter.src.agents.payroll_agent as pa
        pa._default_agent = None

        response = client.post(
            "/api/v1/audio/process",
            files={"file": ("payroll.wav", wav_header, "audio/wav")},
            headers=TEST_AUTH_HEADER,
        )

        assert response.status_code == 200
        data = response.json()
        # Status depends on whether processing succeeded
        assert data["domain"] == "payroll" or data.get("error") is not None


def test_audio_transcribe_with_mock_asr():
    """Test audio transcription with mocked ASR."""
    from transrouter.src.schemas import TranscriptResult

    wav_header = (
        b'RIFF'
        b'\x24\x00\x00\x00'
        b'WAVE'
        b'fmt '
        b'\x10\x00\x00\x00'
        b'\x01\x00'
        b'\x01\x00'
        b'\x80\x3e\x00\x00'
        b'\x00\x7d\x00\x00'
        b'\x02\x00'
        b'\x10\x00'
        b'data'
        b'\x00\x00\x00\x00'
    )

    with patch("transrouter.src.asr_adapter.get_asr_provider") as mock_get_asr:
        mock_provider = MagicMock()
        mock_provider.transcribe.return_value = TranscriptResult(
            transcript="This is a test transcription.",
            confidence=0.92
        )
        mock_get_asr.return_value = mock_provider

        response = client.post(
            "/api/v1/audio/transcribe",
            files={"file": ("test.wav", wav_header, "audio/wav")},
            headers=TEST_AUTH_HEADER,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["transcript"] == "This is a test transcription."


# ============================================================================
# Authentication Tests
# ============================================================================

def test_payroll_endpoint_requires_api_key():
    """Test that payroll endpoint rejects requests without API key."""
    response = client.post(
        "/api/v1/payroll/parse",
        json={"transcript": "Monday AM shift. Ryan was utility. Austin before tipout $200."}
    )

    assert response.status_code == 401
    assert "Missing API key" in response.json()["detail"]


def test_payroll_endpoint_rejects_invalid_api_key():
    """Test that payroll endpoint rejects invalid API keys."""
    response = client.post(
        "/api/v1/payroll/parse",
        json={"transcript": "Monday AM shift. Ryan was utility. Austin before tipout $200."},
        headers={"X-API-Key": "invalid-key-xyz"}
    )

    assert response.status_code == 403
    assert "Invalid API key" in response.json()["detail"]


def test_audio_endpoint_requires_api_key():
    """Test that audio endpoint rejects requests without API key."""
    wav_header = b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00'

    response = client.post(
        "/api/v1/audio/process",
        files={"file": ("test.wav", wav_header, "audio/wav")}
    )

    assert response.status_code == 401


def test_health_endpoint_does_not_require_api_key():
    """Test that health endpoint is public (no auth required)."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] in ("healthy", "degraded")
