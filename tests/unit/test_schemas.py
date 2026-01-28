"""Unit tests for schemas."""

import pytest
from transrouter.src.schemas import (
    ClarificationQuestion,
    ClarificationResponse,
    ConversationState,
    ParseResult,
    QuestionType
)


def test_clarification_question_valid():
    """Test creating valid clarification question."""
    q = ClarificationQuestion(
        question_id="q_001",
        question_text="How many hours did Austin work?",
        question_type=QuestionType.MISSING_DATA,
        field_name="hours",
        affected_entity="Austin Kelley",
        context="Transcript mentions Austin but no hours stated"
    )

    assert q.question_id == "q_001"
    assert q.priority == "required"  # Default
    assert q.question_type == QuestionType.MISSING_DATA


def test_clarification_question_with_suggestion():
    """Test question with suggested answer."""
    q = ClarificationQuestion(
        question_id="q_002",
        question_text="Was tip pool enabled?",
        question_type=QuestionType.MISSING_DATA,
        field_name="tip_pool",
        context="Tip pool not mentioned in transcript",
        suggested_answer=True,
        suggestion_source="historical_pattern",
        priority="recommended"
    )

    assert q.suggested_answer == True
    assert q.suggestion_source == "historical_pattern"
    assert q.priority == "recommended"


def test_clarification_response_valid():
    """Test creating valid clarification response."""
    r = ClarificationResponse(
        question_id="q_001",
        answer="6",
        confidence=1.0,
        notes="Scheduled hours"
    )

    assert r.question_id == "q_001"
    assert r.answer == "6"
    assert r.confidence == 1.0


def test_clarification_response_defaults():
    """Test clarification response default values."""
    r = ClarificationResponse(
        question_id="q_001",
        answer="Yes"
    )

    assert r.confidence == 1.0  # Default
    assert r.notes is None
    assert r.source is None


def test_parse_result_success():
    """Test successful parse result."""
    result = ParseResult(
        status="success",
        conversation_id="conv_123",
        approval_json={"per_shift": {}, "weekly_totals": {}}
    )

    assert result.status == "success"
    assert result.approval_json is not None
    assert len(result.clarifications) == 0
    assert result.error is None


def test_parse_result_needs_clarification():
    """Test parse result needing clarification."""
    questions = [
        ClarificationQuestion(
            question_id="q_001",
            question_text="How many hours?",
            question_type=QuestionType.MISSING_DATA,
            field_name="hours",
            context="Missing hours"
        )
    ]

    result = ParseResult(
        status="needs_clarification",
        conversation_id="conv_123",
        clarifications=questions
    )

    assert result.status == "needs_clarification"
    assert len(result.clarifications) == 1
    assert result.approval_json is None


def test_parse_result_error():
    """Test parse result with error."""
    result = ParseResult(
        status="error",
        conversation_id="conv_456",
        error="Failed to parse transcript",
        error_code="PARSE_ERROR"
    )

    assert result.status == "error"
    assert result.error == "Failed to parse transcript"
    assert result.error_code == "PARSE_ERROR"
    assert result.approval_json is None


def test_conversation_state_tracking():
    """Test conversation state tracking."""
    state = ConversationState(
        conversation_id="conv_123",
        skill_name="payroll",
        original_input={"transcript": "Austin $150"},
        created_at="2026-01-27T10:00:00Z",
        updated_at="2026-01-27T10:00:00Z"
    )

    assert state.conversation_id == "conv_123"
    assert state.skill_name == "payroll"
    assert state.iteration == 0
    assert state.max_iterations == 5
    assert len(state.clarifications_needed) == 0
    assert len(state.clarifications_received) == 0


def test_conversation_state_with_clarifications():
    """Test conversation state with clarifications."""
    question = ClarificationQuestion(
        question_id="q_001",
        question_text="How many hours?",
        question_type=QuestionType.MISSING_DATA,
        field_name="hours",
        context="Missing"
    )

    response = ClarificationResponse(
        question_id="q_001",
        answer="6"
    )

    state = ConversationState(
        conversation_id="conv_123",
        skill_name="payroll",
        original_input={"transcript": "Austin $150"},
        clarifications_needed=[question],
        clarifications_received=[response],
        iteration=1,
        created_at="2026-01-27T10:00:00Z",
        updated_at="2026-01-27T10:05:00Z"
    )

    assert len(state.clarifications_needed) == 1
    assert len(state.clarifications_received) == 1
    assert state.iteration == 1


def test_question_type_enum():
    """Test QuestionType enum values."""
    assert QuestionType.MISSING_DATA == "missing_data"
    assert QuestionType.AMBIGUOUS == "ambiguous"
    assert QuestionType.CONFLICT == "conflict"
    assert QuestionType.UNUSUAL_PATTERN == "unusual_pattern"
    assert QuestionType.CONFIRMATION == "confirmation"


def test_clarification_question_validation():
    """Test Pydantic validation on ClarificationQuestion."""
    # Test minimum length validation on question_text
    with pytest.raises(Exception):  # Pydantic ValidationError
        ClarificationQuestion(
            question_id="q_001",
            question_text="Hi",  # Too short (min 5 chars)
            question_type=QuestionType.MISSING_DATA,
            field_name="hours",
            context="Test"
        )


def test_clarification_response_confidence_bounds():
    """Test confidence is bounded between 0 and 1."""
    # Valid confidence
    r1 = ClarificationResponse(
        question_id="q_001",
        answer="Yes",
        confidence=0.5
    )
    assert r1.confidence == 0.5

    # Confidence = 0 (valid)
    r2 = ClarificationResponse(
        question_id="q_002",
        answer="Maybe",
        confidence=0.0
    )
    assert r2.confidence == 0.0

    # Confidence = 1 (valid)
    r3 = ClarificationResponse(
        question_id="q_003",
        answer="Yes",
        confidence=1.0
    )
    assert r3.confidence == 1.0

    # Confidence > 1 (invalid)
    with pytest.raises(Exception):  # Pydantic ValidationError
        ClarificationResponse(
            question_id="q_004",
            answer="Yes",
            confidence=1.5
        )

    # Confidence < 0 (invalid)
    with pytest.raises(Exception):  # Pydantic ValidationError
        ClarificationResponse(
            question_id="q_005",
            answer="Yes",
            confidence=-0.1
        )


# Run with: pytest tests/unit/test_schemas.py -v
