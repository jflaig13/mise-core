"""LLM-backed cleanup helpers for Whisper transcripts.

This module keeps the shape of the request and response to the cleanup
model in one place so the rest of the code only deals with a predictable
"cleaned" transcript string.
"""

from __future__ import annotations

import logging
import os
from typing import Dict

import requests

log = logging.getLogger(__name__)


class LlmCleanupClient:
    """Call an LLM endpoint to normalize Whisper output.

    The goal is to smooth out spacing, casing, and small hallucinations so the
    downstream payroll parser has fewer edge cases to handle. If no endpoint is
    configured, the client simply trims the input and returns it as-is so the
    pipeline can continue to run.

    Parameters
    ----------
    endpoint_url:
        Override for the cleanup endpoint URL. Falls back to the
        ``TRANSCRIBE_CLEANUP_URL`` environment variable.
    timeout_seconds:
        Optional HTTP timeout so callers can tune the behavior in tests or slow
        environments. If omitted, the client looks for a
        ``TRANSCRIBE_CLEANUP_TIMEOUT_SECONDS`` environment variable and defaults
        to 30 seconds when none is supplied or parsing fails.
    """

    def __init__(self, endpoint_url: str | None = None, timeout_seconds: float | None = None):
        self.endpoint_url = (endpoint_url or os.getenv("TRANSCRIBE_CLEANUP_URL", "")).strip()
        self.timeout_seconds = self._resolve_timeout(timeout_seconds)

    def _resolve_timeout(self, explicit_timeout: float | None) -> float:
        """Pick a timeout from an explicit value, env override, or default."""

        if explicit_timeout is not None:
            return explicit_timeout

        env_timeout = os.getenv("TRANSCRIBE_CLEANUP_TIMEOUT_SECONDS")
        if env_timeout:
            try:
                return float(env_timeout)
            except ValueError:
                log.warning(
                    "Invalid TRANSCRIBE_CLEANUP_TIMEOUT_SECONDS='%s'; using 30s default",
                    env_timeout,
                )

        return 30.0

    def build_payload(self, raw_text: str) -> Dict[str, str]:
        """Shape the request expected by the cleanup model.

        Keeping this in one place makes it easy to evolve the prompt or schema
        without touching the call sites.
        """

        return {
            "prompt": "Normalize payroll shift transcript into tidy sentences.",
            "transcript": raw_text,
        }

    def parse_response(self, response_json: Dict[str, str] | None) -> str:
        """Extract the cleaned transcript from the model response."""

        cleaned = (response_json or {}).get("cleaned_text") or (response_json or {}).get("text")
        return (cleaned or "").strip()

    def clean_text(self, raw_text: str) -> str:
        """Run the cleanup call, falling back to the raw text on error.

        Even if the LLM call fails, we still want the engine to receive some
        transcript so payroll can continue to flow.
        """

        base_text = (raw_text or "").strip()

        if not self.endpoint_url:
            log.debug("No cleanup endpoint configured; returning trimmed transcript")
            return base_text

        try:
            response = requests.post(
                self.endpoint_url,
                json=self.build_payload(raw_text),
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            cleaned = self.parse_response(response.json())
            return cleaned or base_text
        except Exception as exc:  # noqa: BLE001 - we want to catch and log all failures
            log.warning("Cleanup failed, falling back to raw transcript: %s", exc)
            return base_text
