"""Claude API client for Mise domain agents.

Provides a clean interface for calling Claude from domain agents with:
- Environment-based API key configuration
- Configurable model selection
- Structured JSON response parsing
- Error handling with graceful fallback
- Logging for debugging and audit trails
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

import anthropic

log = logging.getLogger(__name__)


@dataclass
class ClaudeConfig:
    """Configuration for Claude API calls."""

    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 16000  # Max OUTPUT tokens
    max_input_tokens: int = 15000  # Max INPUT tokens (warn if exceeded)
    timeout_seconds: float = 120.0

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "ClaudeConfig":
        """Create config from dictionary (e.g., from YAML config)."""
        claude_config = config.get("claude", {})
        return cls(
            model=claude_config.get("model", cls.model),
            max_tokens=claude_config.get("max_tokens", cls.max_tokens),
            max_input_tokens=claude_config.get("max_input_tokens", cls.max_input_tokens),
            timeout_seconds=claude_config.get("timeout_seconds", cls.timeout_seconds),
        )


@dataclass
class ClaudeResponse:
    """Response from Claude API call."""

    success: bool
    content: str
    json_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    model: Optional[str] = None
    usage: Optional[Dict[str, int]] = None


class ClaudeClient:
    """Client for calling Claude API.

    Usage:
        client = ClaudeClient()
        response = client.call(
            system_prompt="You are a payroll parser...",
            user_content="Parse this transcript: ..."
        )

        if response.success:
            print(response.json_data)
        else:
            print(f"Error: {response.error}")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[ClaudeConfig] = None,
    ):
        """Initialize Claude client.

        Args:
            api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY env var.
            config: Optional configuration. Uses defaults if not provided.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            log.warning("No ANTHROPIC_API_KEY found; Claude calls will fail")

        self.config = config or ClaudeConfig()
        self._client: Optional[anthropic.Anthropic] = None

    @property
    def client(self) -> anthropic.Anthropic:
        """Lazy-load the Anthropic client."""
        if self._client is None:
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self._client = anthropic.Anthropic(
                api_key=self.api_key,
                timeout=self.config.timeout_seconds,
            )
        return self._client

    def call(
        self,
        system_prompt: str,
        user_content: str,
        *,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        extract_json: bool = True,
    ) -> ClaudeResponse:
        """Call Claude API with system prompt and user content.

        Args:
            system_prompt: The system prompt defining agent behavior and rules.
            user_content: The user's input (e.g., transcript to parse).
            model: Override model selection.
            max_tokens: Override max tokens.
            extract_json: If True, attempt to extract JSON from response.

        Returns:
            ClaudeResponse with success status, content, and optional parsed JSON.
        """
        model = model or self.config.model
        max_tokens = max_tokens or self.config.max_tokens

        # Estimate input tokens (rough: ~4 chars per token)
        estimated_input_tokens = (len(system_prompt) + len(user_content)) // 4

        if estimated_input_tokens > self.config.max_input_tokens:
            log.warning(
                "Input tokens (~%d) exceed limit (%d). Consider reducing prompt size.",
                estimated_input_tokens,
                self.config.max_input_tokens,
            )

        log.info(
            "Calling Claude API (model=%s, max_output=%d, est_input=%d)",
            model, max_tokens, estimated_input_tokens
        )

        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_content}
                ],
            )

            content = message.content[0].text if message.content else ""
            usage = {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
            }

            log.info(
                "Claude API call successful (input=%d, output=%d tokens)",
                usage["input_tokens"],
                usage["output_tokens"],
            )

            json_data = None
            if extract_json:
                json_data = self._extract_json(content)

            return ClaudeResponse(
                success=True,
                content=content,
                json_data=json_data,
                model=model,
                usage=usage,
            )

        except anthropic.APIError as exc:
            log.error("Claude API error: %s", exc)
            return ClaudeResponse(
                success=False,
                content="",
                error=f"API error: {exc}",
            )
        except Exception as exc:
            log.error("Unexpected error calling Claude: %s", exc)
            return ClaudeResponse(
                success=False,
                content="",
                error=f"Unexpected error: {exc}",
            )

    def _extract_json(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from Claude's response.

        Handles responses that may contain JSON within markdown code blocks
        or as raw JSON.
        """
        # Try to find JSON in code blocks first
        json_block_pattern = r"```(?:json)?\s*\n?([\s\S]*?)\n?```"
        matches = re.findall(json_block_pattern, content)

        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue

        # Try parsing the entire content as JSON
        try:
            return json.loads(content.strip())
        except json.JSONDecodeError:
            pass

        # Try to find JSON object in content (starts with { ends with })
        json_obj_pattern = r"\{[\s\S]*\}"
        match = re.search(json_obj_pattern, content)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        log.debug("Could not extract JSON from response")
        return None


# Module-level convenience function
_default_client: Optional[ClaudeClient] = None


def get_client(config: Optional[Dict[str, Any]] = None) -> ClaudeClient:
    """Get or create a Claude client with optional config."""
    global _default_client

    if config:
        return ClaudeClient(config=ClaudeConfig.from_dict(config))

    if _default_client is None:
        _default_client = ClaudeClient()

    return _default_client


def call_claude(
    system_prompt: str,
    user_content: str,
    *,
    model: Optional[str] = None,
    extract_json: bool = True,
) -> ClaudeResponse:
    """Convenience function to call Claude with defaults.

    Args:
        system_prompt: The system prompt.
        user_content: The user's input.
        model: Optional model override.
        extract_json: Whether to extract JSON from response.

    Returns:
        ClaudeResponse with results.

    Example:
        response = call_claude(
            system_prompt="You are a helpful assistant.",
            user_content="What is 2 + 2?"
        )
        print(response.content)
    """
    client = get_client()
    return client.call(
        system_prompt=system_prompt,
        user_content=user_content,
        model=model,
        extract_json=extract_json,
    )
