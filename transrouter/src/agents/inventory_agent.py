"""Inventory Agent - Parses inventory transcripts using Claude.

This agent receives inventory transcripts from the transrouter and uses
Claude to parse them into structured inventory JSON matching the Shelfy schema.

Pattern: Follows PayrollAgent structure (transrouter/src/agents/payroll_agent.py)
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, List

from ..claude_client import ClaudeClient, ClaudeConfig, ClaudeResponse
from ..prompts.inventory_prompt import (
    build_inventory_system_prompt,
    build_inventory_user_prompt,
)

log = logging.getLogger(__name__)


class InventoryAgentError(Exception):
    """Raised when inventory agent encounters an error."""

    pass


class InventoryAgent:
    """Agent for parsing inventory transcripts into structured JSON.

    Usage:
        agent = InventoryAgent()
        result = agent.parse_transcript(transcript_text, category="bar")

        if result["status"] == "success":
            inventory_json = result["inventory_json"]
        else:
            error = result["error"]
    """

    def __init__(
        self,
        claude_client: Optional[ClaudeClient] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize inventory agent.

        Args:
            claude_client: Optional pre-configured Claude client.
            config: Optional configuration dict (used if claude_client not provided).
        """
        if claude_client:
            self.claude_client = claude_client
        else:
            claude_config = ClaudeConfig.from_dict(config or {})
            self.claude_client = ClaudeClient(config=claude_config)

        self._system_prompt_cache: Dict[str, str] = {}

    def system_prompt(self, category: str) -> str:
        """Get cached system prompt for category."""
        if category not in self._system_prompt_cache:
            self._system_prompt_cache[category] = build_inventory_system_prompt(category)
            log.debug("Built inventory system prompt for %s (%d chars)",
                     category, len(self._system_prompt_cache[category]))
        return self._system_prompt_cache[category]

    def parse_transcript(
        self,
        transcript: str,
        category: str = "bar",
        area: str = "",
    ) -> Dict[str, Any]:
        """Parse an inventory transcript into structured JSON.

        Args:
            transcript: The inventory transcript text to parse.
            category: Inventory category (bar, food, supplies).
            area: Optional area hint (front bar, back bar, kitchen, etc.).

        Returns:
            Dict with keys:
                - agent: "inventory"
                - status: "success" or "error"
                - inventory_json: The parsed inventory JSON (if successful)
                - raw_response: Claude's full response text
                - error: Error message (if failed)
                - usage: Token usage stats
        """
        log.info("Parsing inventory transcript (%d chars, category=%s, area=%s)",
                len(transcript), category, area or "none")

        user_prompt = build_inventory_user_prompt(transcript, category, area)

        response: ClaudeResponse = self.claude_client.call(
            system_prompt=self.system_prompt(category),
            user_content=user_prompt,
            extract_json=True,
        )

        if not response.success:
            log.error("Claude API call failed: %s", response.error)
            return {
                "agent": "inventory",
                "status": "error",
                "error": response.error,
                "raw_response": response.content,
            }

        if not response.json_data:
            log.error("Failed to extract JSON from Claude response")
            return {
                "agent": "inventory",
                "status": "error",
                "error": "Failed to extract JSON from response",
                "raw_response": response.content,
            }

        # Validate the inventory JSON has required keys
        validation_error = self._validate_inventory_json(response.json_data, category)
        if validation_error:
            log.error("Inventory JSON validation failed: %s", validation_error)
            return {
                "agent": "inventory",
                "status": "error",
                "error": validation_error,
                "inventory_json": response.json_data,
                "raw_response": response.content,
            }

        log.info(
            "Successfully parsed inventory transcript (items=%d, category=%s)",
            len(response.json_data.get("items", [])),
            category,
        )

        return {
            "agent": "inventory",
            "status": "success",
            "inventory_json": response.json_data,
            "raw_response": response.content,
            "usage": response.usage,
        }

    def _validate_inventory_json(self, data: Dict[str, Any], category: str) -> Optional[str]:
        """Validate that inventory JSON has required structure.

        Args:
            data: The parsed JSON data.
            category: Expected category.

        Returns:
            Error message if validation fails, None if valid.
        """
        required_keys = ["category", "items"]

        missing_keys = [k for k in required_keys if k not in data]
        if missing_keys:
            return f"Missing required keys: {missing_keys}"

        # Validate category matches
        if data.get("category") != category:
            return f"Category mismatch: expected {category}, got {data.get('category')}"

        # Validate items is a list
        if not isinstance(data.get("items"), list):
            return "items must be an array"

        # Validate each item has required fields
        for idx, item in enumerate(data.get("items", [])):
            if not isinstance(item, dict):
                return f"Item {idx} is not an object"

            if "product_name" not in item:
                return f"Item {idx} missing product_name"

            # Quantity can be null for unclear counts
            if "quantity" in item and item["quantity"] is not None:
                if not isinstance(item["quantity"], (int, float)):
                    return f"Item {idx} quantity must be a number or null"

        return None


# Module-level instance for simple usage
_default_agent: Optional[InventoryAgent] = None


def get_agent(config: Optional[Dict[str, Any]] = None) -> InventoryAgent:
    """Get or create the default inventory agent."""
    global _default_agent

    if config:
        return InventoryAgent(config=config)

    if _default_agent is None:
        _default_agent = InventoryAgent()

    return _default_agent


def handle_inventory_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle an inventory request from the domain router.

    This is the main entry point called by domain_router.py.

    Args:
        request: Dict with keys:
            - intent_type: The classified intent type
            - entities: Extracted entities
            - meta: Metadata including transcript

    Returns:
        Dict with agent response (see InventoryAgent.parse_transcript).
    """
    log.info("Handling inventory request (intent=%s)", request.get("intent_type"))

    # Extract transcript from request
    transcript = request.get("meta", {}).get("transcript", "")

    if not transcript:
        # Try to get transcript from entities or other locations
        transcript = request.get("entities", {}).get("transcript", "")

    if not transcript:
        log.error("No transcript found in inventory request")
        return {
            "agent": "inventory",
            "status": "error",
            "error": "No transcript provided in request",
            "request": request,
        }

    # Get category from entities (default to "bar")
    category = request.get("entities", {}).get("category", "bar")

    # Get area hint if available
    area = request.get("entities", {}).get("area", "")

    # Parse the transcript
    agent = get_agent()
    return agent.parse_transcript(transcript, category, area)
