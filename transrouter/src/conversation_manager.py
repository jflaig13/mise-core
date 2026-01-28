"""
Conversation Manager for Multi-Turn Clarification Flows.

Manages conversation state for skills that require clarification from the user.
Stores questions, answers, and tracks iteration count to prevent infinite loops.

Part of Phase 1 (Clarification System).
"""

import uuid
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
import json

from transrouter.src.schemas import (
    ConversationState,
    ClarificationQuestion,
    ClarificationResponse
)


class ConversationManager:
    """
    Manages multi-turn conversation state for clarification flows.

    Stores conversation state to disk (JSON) so conversations can be resumed
    across requests.
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize conversation manager.

        Args:
            storage_dir: Directory to store conversation state files.
                        Defaults to ~/mise-core/mise_app/data/conversations/
        """
        if storage_dir is None:
            storage_dir = Path.home() / "mise-core/mise_app/data/conversations"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def create_conversation(
        self,
        skill_name: str,
        original_input: Dict
    ) -> ConversationState:
        """
        Create a new conversation.

        Args:
            skill_name: Name of the skill executing (e.g., "payroll")
            original_input: Original input data (transcript, period_id, etc.)

        Returns:
            New ConversationState
        """
        conversation_id = f"conv_{uuid.uuid4().hex[:12]}"
        now = datetime.now().isoformat()

        state = ConversationState(
            conversation_id=conversation_id,
            skill_name=skill_name,
            original_input=original_input,
            created_at=now,
            updated_at=now
        )

        self._save(state)
        return state

    def load_conversation(self, conversation_id: str) -> Optional[ConversationState]:
        """
        Load conversation state from disk.

        Args:
            conversation_id: Conversation ID to load

        Returns:
            ConversationState if found, None otherwise
        """
        file_path = self._get_file_path(conversation_id)

        if not file_path.exists():
            return None

        with open(file_path, 'r') as f:
            data = json.load(f)

        # Reconstruct Pydantic models
        state = ConversationState(**data)
        return state

    def add_clarifications_needed(
        self,
        conversation_id: str,
        questions: List[ClarificationQuestion]
    ) -> ConversationState:
        """
        Add clarification questions to a conversation.

        Args:
            conversation_id: Conversation to update
            questions: List of questions to add

        Returns:
            Updated ConversationState

        Raises:
            ValueError: If conversation not found
        """
        state = self.load_conversation(conversation_id)
        if state is None:
            raise ValueError(f"Conversation {conversation_id} not found")

        state.clarifications_needed.extend(questions)
        state.updated_at = datetime.now().isoformat()

        self._save(state)
        return state

    def add_clarifications_received(
        self,
        conversation_id: str,
        responses: List[ClarificationResponse]
    ) -> ConversationState:
        """
        Add clarification responses from user.

        Args:
            conversation_id: Conversation to update
            responses: List of user responses

        Returns:
            Updated ConversationState

        Raises:
            ValueError: If conversation not found
        """
        state = self.load_conversation(conversation_id)
        if state is None:
            raise ValueError(f"Conversation {conversation_id} not found")

        state.clarifications_received.extend(responses)
        state.iteration += 1
        state.updated_at = datetime.now().isoformat()

        self._save(state)
        return state

    def is_complete(self, conversation_id: str) -> bool:
        """
        Check if all clarifications have been answered.

        Args:
            conversation_id: Conversation to check

        Returns:
            True if all questions answered, False otherwise
        """
        state = self.load_conversation(conversation_id)
        if state is None:
            return False

        # Get question IDs that still need answers
        answered_ids = {r.question_id for r in state.clarifications_received}
        needed_ids = {q.question_id for q in state.clarifications_needed}

        return needed_ids.issubset(answered_ids)

    def has_exceeded_max_iterations(self, conversation_id: str) -> bool:
        """
        Check if conversation has exceeded max iterations.

        Args:
            conversation_id: Conversation to check

        Returns:
            True if exceeded, False otherwise
        """
        state = self.load_conversation(conversation_id)
        if state is None:
            return False

        return state.iteration >= state.max_iterations

    def get_unanswered_questions(
        self,
        conversation_id: str
    ) -> List[ClarificationQuestion]:
        """
        Get questions that still need answers.

        Args:
            conversation_id: Conversation to check

        Returns:
            List of unanswered questions
        """
        state = self.load_conversation(conversation_id)
        if state is None:
            return []

        answered_ids = {r.question_id for r in state.clarifications_received}
        unanswered = [
            q for q in state.clarifications_needed
            if q.question_id not in answered_ids
        ]

        return unanswered

    def get_answer(
        self,
        conversation_id: str,
        question_id: str
    ) -> Optional[ClarificationResponse]:
        """
        Get user's answer to a specific question.

        Args:
            conversation_id: Conversation to search
            question_id: Question ID to find answer for

        Returns:
            ClarificationResponse if found, None otherwise
        """
        state = self.load_conversation(conversation_id)
        if state is None:
            return None

        for response in state.clarifications_received:
            if response.question_id == question_id:
                return response

        return None

    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete conversation from disk.

        Args:
            conversation_id: Conversation to delete

        Returns:
            True if deleted, False if not found
        """
        file_path = self._get_file_path(conversation_id)

        if file_path.exists():
            file_path.unlink()
            return True

        return False

    def _save(self, state: ConversationState) -> None:
        """Save conversation state to disk."""
        file_path = self._get_file_path(state.conversation_id)

        with open(file_path, 'w') as f:
            # Convert Pydantic model to dict, then to JSON
            json.dump(state.model_dump(), f, indent=2)

    def _get_file_path(self, conversation_id: str) -> Path:
        """Get file path for a conversation ID."""
        return self.storage_dir / f"{conversation_id}.json"
