"""Inventory Agent - Parses inventory transcripts using Claude.

This agent receives inventory transcripts from the transrouter and uses
Claude to parse them into structured inventory JSON matching the Shelfy schema.

Pattern: Follows PayrollAgent structure (transrouter/src/agents/payroll_agent.py)
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional, List

from ..asr_adapter import get_asr_provider
from ..claude_client import ClaudeClient, ClaudeConfig, ClaudeResponse
from ..prompts.inventory_prompt import (
    build_inventory_system_prompt,
    build_inventory_user_prompt,
)

log = logging.getLogger(__name__)


class InventoryAgentError(Exception):
    """Raised when inventory agent encounters an error."""

    pass


def _load_catalog() -> Dict[str, Any]:
    """Load the inventory catalog JSON.

    Tries two paths:
    1. inventory_agent/inventory_catalog.json (local dev)
    2. data/inventory_catalog.json (Docker / production)
    """
    primary_path = Path(__file__).parent.parent.parent.parent / "inventory_agent" / "inventory_catalog.json"
    fallback_path = Path(__file__).parent.parent.parent.parent / "data" / "inventory_catalog.json"

    catalog_path = primary_path if primary_path.exists() else fallback_path

    if not catalog_path.exists():
        log.warning("Inventory catalog not found at %s or %s", primary_path, fallback_path)
        return {}

    try:
        with open(catalog_path, "r") as f:
            return json.load(f)
    except Exception as e:
        log.error("Failed to load inventory catalog: %s", e)
        return {}


def _extract_pack_multiplier(unit: str) -> Optional[tuple[int, str]]:
    """Extract pack multiplier from unit string.

    Examples:
        "4-pack" -> (4, "pack")
        "6-pack" -> (6, "pack")
        "12-pack" -> (12, "pack")
        "cases" -> None  # No assumed conversion — case sizes vary by product
        "bottles" -> None

    Returns:
        Tuple of (multiplier, base_unit) or None if no pack size detected.
    """
    unit_lower = unit.lower().strip()

    # Match patterns like "4-pack", "6-packs", "12 pack"
    pack_match = re.match(r"(\d+)[\s\-]?packs?", unit_lower)
    if pack_match:
        return (int(pack_match.group(1)), "pack")

    return None


def _find_catalog_unit(product_name: str, catalog: Dict[str, Any]) -> Optional[str]:
    """Find the catalog's report_by_unit for a product.

    Args:
        product_name: Product name to search for.
        catalog: Full catalog dict.

    Returns:
        The report_by_unit string, or None if not found.
    """
    product_lower = product_name.lower()

    # Search all categories
    for category_name, category_items in catalog.items():
        if category_name == "global_rules":
            continue

        if not isinstance(category_items, list):
            continue

        for item in category_items:
            if not isinstance(item, dict):
                continue

            item_name = item.get("item", "").lower()

            # Exact match or fuzzy match
            if item_name == product_lower or product_lower in item_name or item_name in product_lower:
                return item.get("report_by_unit")

    return None


def _calculate_conversion_display(
    quantity: Optional[float],
    unit: str,
    product_name: str,
    catalog: Dict[str, Any]
) -> Optional[str]:
    """Calculate conversion display string for an inventory item.

    Args:
        quantity: The quantity (e.g., 6)
        unit: The unit string (e.g., "4-packs")
        product_name: Product name to look up in catalog
        catalog: Full catalog

    Returns:
        Conversion display string like "6 × 4 = 24 cans" or None if no conversion needed.
    """
    if quantity is None or quantity == 0:
        return None

    # Extract pack multiplier
    pack_info = _extract_pack_multiplier(unit)
    if not pack_info:
        return None  # No pack size detected

    multiplier, _ = pack_info

    # Calculate total
    total = int(quantity * multiplier)

    # Try to find the catalog unit
    catalog_unit = _find_catalog_unit(product_name, catalog)

    if catalog_unit:
        # Extract base unit from catalog (e.g., "Can (12 Fluid Ounces)" -> "cans")
        base_unit_match = re.search(r"(can|bottle|each|keg|gallon|pound|case)", catalog_unit.lower())
        if base_unit_match:
            base_unit = base_unit_match.group(1) + "s" if not base_unit_match.group(1).endswith("s") else base_unit_match.group(1)
        else:
            base_unit = "units"
    else:
        # Default to generic unit
        base_unit = "units"

    return f"{int(quantity)} × {multiplier} = {total} {base_unit}"


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
        self._catalog: Optional[Dict[str, Any]] = None

    @property
    def catalog(self) -> Dict[str, Any]:
        """Lazy-load and cache the inventory catalog."""
        if self._catalog is None:
            self._catalog = _load_catalog()
        return self._catalog

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

        # Enrich with conversion displays for subfinal counts
        enriched_inventory = self._enrich_with_conversions(response.json_data)

        log.info(
            "Successfully parsed inventory transcript (items=%d, category=%s)",
            len(enriched_inventory.get("items", [])),
            category,
        )

        return {
            "agent": "inventory",
            "status": "success",
            "inventory_json": enriched_inventory,
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

    def _enrich_with_conversions(self, inventory_json: Dict[str, Any]) -> Dict[str, Any]:
        """Add conversion_display and converted_quantity fields to inventory items.

        This method enriches items with:
        - conversion_display: Human-readable conversion string (e.g., "6 × 4 = 24 cans")
        - converted_quantity: Actual converted quantity for aggregation (e.g., 24)

        Args:
            inventory_json: The parsed inventory JSON with items.

        Returns:
            Enriched inventory JSON with conversion fields added to items.
        """
        items = inventory_json.get("items", [])

        for item in items:
            if not isinstance(item, dict):
                continue

            quantity = item.get("quantity")
            unit = item.get("unit", "")
            product_name = item.get("product_name", "")

            # Calculate conversion display
            conversion_display = _calculate_conversion_display(
                quantity, unit, product_name, self.catalog
            )

            # Calculate converted quantity and base unit for aggregation
            pack_info = _extract_pack_multiplier(unit)
            if pack_info and quantity is not None:
                multiplier, _ = pack_info
                converted_quantity = int(quantity * multiplier)
                item["converted_quantity"] = converted_quantity

                # Extract base unit from catalog
                catalog_unit = _find_catalog_unit(product_name, self.catalog)
                if catalog_unit:
                    base_unit_match = re.search(r"(can|bottle|each|keg|gallon|pound|case)", catalog_unit.lower())
                    if base_unit_match:
                        base_unit = base_unit_match.group(1) + "s" if not base_unit_match.group(1).endswith("s") else base_unit_match.group(1)
                    else:
                        base_unit = "units"
                else:
                    base_unit = "units"

                item["base_unit"] = base_unit
                log.debug("Converted %s %s → %d %s", quantity, unit, converted_quantity, base_unit)
            else:
                # No conversion needed - use raw quantity and original unit
                item["converted_quantity"] = quantity
                item["base_unit"] = unit

            if conversion_display:
                item["conversion_display"] = conversion_display
                log.debug("Added conversion for %s: %s", product_name, conversion_display)

        return inventory_json

    # ========================================================================
    # Self-contained pipelines (ASR → parse → dict)
    # ========================================================================

    def process_audio(
        self,
        audio_bytes: bytes,
        category: str = "bar",
        area: str = "",
    ) -> Dict[str, Any]:
        """Full pipeline: ASR → parse → structured result dict.

        Args:
            audio_bytes: Raw audio data.
            category: Inventory category (bar, food, supplies).
            area: Optional area hint.

        Returns:
            Dict with {status, transcript, approval_json} matching route expectations.
        """
        log.info("InventoryAgent.process_audio: processing %d bytes (category=%s)", len(audio_bytes), category)

        # Step 1: Transcribe
        asr = get_asr_provider()
        asr_result = asr.transcribe(audio_bytes, "wav", sample_rate_hz=16000)
        transcript = asr_result.transcript

        if not transcript:
            return {"status": "error", "error": "Transcription returned empty result"}

        log.info("InventoryAgent.process_audio: transcript (%d chars)", len(transcript))

        # Step 2: Parse and return
        return self.process_text(transcript, category, area)

    def process_text(
        self,
        transcript: str,
        category: str = "bar",
        area: str = "",
    ) -> Dict[str, Any]:
        """Parse-only pipeline for pre-transcribed text.

        Args:
            transcript: Already-transcribed text.
            category: Inventory category (bar, food, supplies).
            area: Optional area hint.

        Returns:
            Dict with {status, transcript, approval_json} matching route expectations.
        """
        log.info("InventoryAgent.process_text: parsing %d chars (category=%s)", len(transcript), category)

        result = self.parse_transcript(transcript, category, area)

        if result.get("status") == "success":
            return {
                "status": "success",
                "transcript": transcript,
                "approval_json": result.get("inventory_json", {}),
            }
        else:
            return {
                "status": "error",
                "error": result.get("error", "Inventory parsing failed"),
                "transcript": transcript,
            }


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
