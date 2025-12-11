"""Lightweight schema definitions for the Transrouter.

Defines typed request/response containers shared across the Transrouter modules.
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
    audio_base64: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    """ASR output container."""

    transcript: str
    confidence: Optional[float] = None
    words: Optional[List[Dict[str, Any]]] = None


@dataclass
class IntentClassification:
    """Intent classification result."""

    domain_agent: Optional[str]
    intent_type: Optional[str]
    confidence: Optional[float] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EntityExtraction:
    """Entity extraction result."""

    entities: Dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RoutingDecision:
    """Decision describing how the request will be routed."""

    domain_agent: Optional[str]
    intent_type: Optional[str]
    entities: Dict[str, Any] = field(default_factory=dict)
    intent_confidence: Optional[float] = None
    entity_confidence: Optional[float] = None
    reason: Optional[str] = None


@dataclass
class RouterResponse:
    """Router outcome delivered back to the caller."""

    domain: Optional[str]
    intent: Optional[str]
    entities: Dict[str, Any] = field(default_factory=dict)
    payload: Optional[Any] = None
    errors: List[str] = field(default_factory=list)
    transcript: Optional[str] = None
    intent_confidence: Optional[float] = None
    entity_confidence: Optional[float] = None
    decision_reason: Optional[str] = None
