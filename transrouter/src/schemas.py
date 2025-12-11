"""Lightweight schema definitions for the Transrouter.

Defines typed request/response containers shared across the router modules.
Placeholder only; no runtime validation yet.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AudioRequest:
    """Inbound audio payload."""

    audio_bytes: bytes
    audio_format: str
    sample_rate_hz: int
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    """ASR output container."""

    transcript: str
    confidence: Optional[float] = None
    words: Optional[List[Dict[str, Any]]] = None


@dataclass
class RouterResponse:
    """Router outcome delivered back to the caller."""

    domain: Optional[str]
    intent: Optional[str]
    entities: Dict[str, Any] = field(default_factory=dict)
    payload: Optional[Any] = None
    errors: List[str] = field(default_factory=list)
