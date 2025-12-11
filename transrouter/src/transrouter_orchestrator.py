"""Orchestrator for the Transrouter pipeline.

Responsibilities:
- Entrypoints for audio/text handling
- Wire ASR -> intent classification -> entity extraction -> routing
- Return RouterResponse

No real logic yet; placeholder functions and docstrings only.
"""

from typing import Any, Dict
from .schemas import AudioRequest, RouterResponse


def handle_audio_request(audio_request: AudioRequest) -> RouterResponse:
    """Main entry for audio requests: transcribe -> interpret -> route.

    TODO: implement orchestration once modules are complete.
    """
    raise NotImplementedError


def handle_text_request(transcript: str, meta: Dict[str, Any]) -> RouterResponse:
    """Entry for pre-transcribed text: interpret -> route.

    TODO: implement orchestration once modules are complete.
    """
    raise NotImplementedError
