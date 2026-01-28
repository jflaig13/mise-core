"""Lightweight schema definitions for the Transrouter.

Defines typed request/response containers shared across the Transrouter modules.

UPDATED (Phase 1): Added Pydantic models for multi-turn clarification system.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field


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


# ============================================================================
# CLARIFICATION SYSTEM (Phase 1)
# ============================================================================


class QuestionType(str, Enum):
    """Types of clarification questions."""
    MISSING_DATA = "missing_data"          # Required field missing
    AMBIGUOUS = "ambiguous"                # Multiple interpretations
    CONFLICT = "conflict"                  # Sources disagree
    UNUSUAL_PATTERN = "unusual_pattern"    # Deviates from normal
    CONFIRMATION = "confirmation"          # Verify assumption


class ClarificationQuestion(BaseModel):
    """
    A question Mise needs answered before proceeding.

    Example:
        {
            "question_id": "q_001_austin_hours",
            "question_text": "How many hours did Austin work?",
            "question_type": "missing_data",
            "field_name": "hours",
            "affected_entity": "Austin Kelley",
            "context": "Transcript mentions Austin but no hours stated",
            "suggested_answer": "6.0",
            "suggestion_source": "scheduled_hours",
            "priority": "required"
        }
    """
    question_id: str = Field(
        ...,
        description="Unique identifier for tracking this question"
    )

    question_text: str = Field(
        ...,
        description="Human-readable question for manager",
        min_length=5,
        max_length=500
    )

    question_type: QuestionType = Field(
        ...,
        description="Category of question (missing_data, ambiguous, etc.)"
    )

    field_name: str = Field(
        ...,
        description="What data field is in question (hours, amount, role, etc.)"
    )

    affected_entity: Optional[str] = Field(
        None,
        description="Employee or entity this question is about"
    )

    context: str = Field(
        ...,
        description="Why is Mise asking? What's the situation?",
        max_length=1000
    )

    suggested_answer: Optional[Any] = Field(
        None,
        description="Suggested answer if policy/pattern exists (not assumed)"
    )

    suggestion_source: Optional[str] = Field(
        None,
        description="Where suggestion came from (schedule, policy, pattern)"
    )

    priority: Literal["required", "recommended", "optional"] = Field(
        "required",
        description="Is this blocking or just nice-to-have?"
    )

    validation_rules: Optional[Dict[str, Any]] = Field(
        None,
        description="Validation rules for answer (e.g., min/max hours)"
    )


class ClarificationResponse(BaseModel):
    """
    Manager's answer to a clarification question.

    Example:
        {
            "question_id": "q_001_austin_hours",
            "answer": "6",
            "confidence": 1.0,
            "notes": "Scheduled hours, confirmed by closing report"
        }
    """
    question_id: str = Field(
        ...,
        description="Which question is this answering?"
    )

    answer: str = Field(
        ...,
        description="Manager's answer (as string, will be cast to appropriate type)",
        min_length=1,
        max_length=1000
    )

    confidence: float = Field(
        1.0,
        description="Manager's confidence in answer (0-1)",
        ge=0.0,
        le=1.0
    )

    notes: Optional[str] = Field(
        None,
        description="Optional context/notes from manager",
        max_length=2000
    )

    source: Optional[str] = Field(
        None,
        description="Where did manager get this answer? (memory, schedule, Toast, etc.)"
    )


class ConversationState(BaseModel):
    """
    State of a multi-turn conversation.

    Tracks original input, clarifications needed, responses received.
    """
    conversation_id: str = Field(
        ...,
        description="Unique ID for this conversation"
    )

    skill_name: str = Field(
        ...,
        description="Which skill is executing (payroll, inventory, etc.)"
    )

    original_input: Dict[str, Any] = Field(
        ...,
        description="Original inputs (transcript, period_id, etc.)"
    )

    clarifications_needed: List[ClarificationQuestion] = Field(
        default_factory=list,
        description="Questions that need answers"
    )

    clarifications_received: List[ClarificationResponse] = Field(
        default_factory=list,
        description="Answers provided by manager"
    )

    iteration: int = Field(
        0,
        description="How many rounds of clarification so far?",
        ge=0
    )

    max_iterations: int = Field(
        5,
        description="Max clarification rounds before giving up",
        ge=1,
        le=10
    )

    created_at: str = Field(
        ...,
        description="ISO timestamp when conversation started"
    )

    updated_at: str = Field(
        ...,
        description="ISO timestamp of last update"
    )


class ParseResult(BaseModel):
    """
    Result from skill execution, possibly with clarifications needed.

    Three possible outcomes:
    1. SUCCESS - Complete, ready to use
    2. NEEDS_CLARIFICATION - Missing data, need manager input
    3. ERROR - Something went wrong
    """
    model_config = {"protected_namespaces": ()}  # Allow 'model_' prefix

    status: Literal["success", "needs_clarification", "error"] = Field(
        ...,
        description="Outcome of parsing attempt"
    )

    conversation_id: str = Field(
        ...,
        description="ID for tracking multi-turn conversation"
    )

    # Success path
    approval_json: Optional[dict] = Field(
        None,
        description="Complete approval JSON (only if status=success)"
    )

    # Clarification path
    clarifications: List[ClarificationQuestion] = Field(
        default_factory=list,
        description="Questions to ask manager (if status=needs_clarification)"
    )

    partial_result: Optional[dict] = Field(
        None,
        description="Partial approval JSON with missing fields (if needs_clarification)"
    )

    # Error path
    error: Optional[str] = Field(
        None,
        description="Error message (if status=error)"
    )

    error_code: Optional[str] = Field(
        None,
        description="Machine-readable error code"
    )

    # Metadata
    model_used: Optional[str] = Field(
        None,
        description="Which LLM model was used"
    )

    tokens_used: Optional[Dict[str, int]] = Field(
        None,
        description="Token usage (input, output)"
    )

    execution_time_ms: Optional[int] = Field(
        None,
        description="How long did this take?"
    )

    grounding_check: Optional[Dict[str, Any]] = Field(
        None,
        description="Results of grounding validation"
    )
