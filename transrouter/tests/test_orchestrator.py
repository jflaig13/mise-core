"""Tests for the Transrouter orchestrator pipeline."""

import base64

from transrouter.src import transrouter_orchestrator as orch
from transrouter.src.schemas import AudioRequest, RouterResponse, TranscriptResult


class StubASR:
    def __init__(self, transcript: str):
        self.transcript = transcript

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        return TranscriptResult(transcript=self.transcript, confidence=0.9)


def test_handle_text_request_inventory_routes():
    transcript = "We need an inventory count for tomatoes and onions"
    response = orch.handle_text_request(transcript, {})
    assert isinstance(response, RouterResponse)
    assert response.domain == "inventory"
    assert response.intent is not None
    assert response.payload and response.payload.get("agent") == "inventory"


def test_handle_audio_request_with_base64_and_stub_asr():
    fake_audio = b"fake-bytes"
    audio_b64 = base64.b64encode(fake_audio).decode("utf-8")
    req = AudioRequest(audio_bytes=b"", audio_base64=audio_b64, audio_format="wav", sample_rate_hz=16000, meta={})

    response = orch.handle_audio_request(req, asr_provider=StubASR("I worked 40 hours last week on payroll"))
    assert response.domain == "payroll"
    assert response.intent in ("update", "query")
    assert "40" in response.entities.get("numbers", [])
    assert response.errors == []


def test_handle_audio_request_invalid_base64_returns_error():
    req = AudioRequest(audio_bytes=b"", audio_base64="not-base64", audio_format="wav", sample_rate_hz=16000, meta={})
    response = orch.handle_audio_request(req, asr_provider=StubASR("anything"))
    assert response.errors
    assert response.domain is None
