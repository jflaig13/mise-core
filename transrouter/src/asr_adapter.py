"""ASR adapter interface for Transrouter.

Provides a pluggable API to different transcription providers (Whisper, Amazon Transcribe, etc.).
Placeholder only; no real logic yet.
"""

from typing import Optional
from .schemas import TranscriptResult


class ASRAdapter:
    """Abstract adapter for ASR providers."""

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        """Transcribe audio into a TranscriptResult.

        TODO: implement provider selection and actual transcription.
        """
        raise NotImplementedError


class WhisperAdapter(ASRAdapter):
    """Placeholder Whisper implementation."""

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        raise NotImplementedError


class AmazonTranscribeAdapter(ASRAdapter):
    """Placeholder Amazon Transcribe implementation."""

    def transcribe(self, audio_bytes: bytes, audio_format: str, sample_rate_hz: int) -> TranscriptResult:
        raise NotImplementedError
