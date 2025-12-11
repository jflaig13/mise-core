"""ASR adapter interface for Transrouter.

Provides a pluggable API to different transcription providers (Whisper, Amazon Transcribe, etc.).
"""

import importlib
import tempfile
from typing import Any, Dict, Optional

from .schemas import TranscriptResult


class ASRAdapter:
    """Abstract adapter for ASR providers."""

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        """Transcribe audio into a TranscriptResult."""
        raise NotImplementedError


class WhisperAdapter(ASRAdapter):
    """Whisper implementation with optional dependency on openai/whisper."""

    def __init__(self, model_name: str = "base", language: str = "en"):
        self.model_name = model_name
        self.language = language
        self._model = None

    def _load_model(self):
        """Lazily import whisper to avoid hard dependency when unused."""
        if self._model is not None:
            return self._model
        whisper = importlib.import_module("whisper")
        self._model = whisper.load_model(self.model_name)
        return self._model

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        try:
            model = self._load_model()
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Whisper provider requires the 'whisper' package. Install openai-whisper to enable."
            ) from exc

        with tempfile.NamedTemporaryFile(suffix=f".{audio_format}") as tmp:
            tmp.write(audio_bytes)
            tmp.flush()
            result = model.transcribe(tmp.name, language=self.language)

        transcript = (result.get("text") or "").strip()
        words = result.get("segments")
        confidence = None
        if words:
            scores = [seg.get("avg_logprob") for seg in words if seg.get("avg_logprob") is not None]
            if scores:
                confidence = sum(scores) / len(scores)

        return TranscriptResult(transcript=transcript, confidence=confidence, words=words)


class AmazonTranscribeAdapter(ASRAdapter):
    """Placeholder Amazon Transcribe implementation."""

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        raise NotImplementedError("Amazon Transcribe provider not implemented")


class GoogleASRAdapter(ASRAdapter):
    """Placeholder Google ASR implementation."""

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        raise NotImplementedError("Google ASR provider not implemented")


class AzureASRAdapter(ASRAdapter):
    """Placeholder Azure Speech implementation."""

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        raise NotImplementedError("Azure ASR provider not implemented")


def get_asr_provider(config: Optional[Dict[str, Any]] = None) -> ASRAdapter:
    """Return a configured ASR adapter."""
    cfg = (config or {}).get("asr", {})
    provider = (cfg.get("provider") or "whisper").lower()
    language = cfg.get("language", "en")
    model_name = cfg.get("whisper_model", "base")

    if provider == "whisper":
        return WhisperAdapter(model_name=model_name, language=language)
    if provider in ("amazon", "amazon_transcribe"):
        return AmazonTranscribeAdapter()
    if provider in ("google", "google_asr"):
        return GoogleASRAdapter()
    if provider in ("azure", "azure_speech"):
        return AzureASRAdapter()

    raise ValueError(f"Unknown ASR provider: {provider}")
