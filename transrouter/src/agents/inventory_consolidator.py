"""Inventory Consolidator — Claude-powered cleanup after aggregation.

Runs after get_aggregated_totals() but before the totals page renders.
Merges duplicate product names, fixes miscategorizations, and flags
generic items that need human input.

On failure, returns the original aggregated_totals unchanged (graceful fallback).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from ..claude_client import ClaudeClient, ClaudeConfig
from ..prompts.consolidation_prompt import (
    build_consolidation_system_prompt,
    build_consolidation_user_prompt,
)

log = logging.getLogger(__name__)


class InventoryConsolidator:
    """Consolidates aggregated inventory totals using Claude.

    Usage:
        consolidator = InventoryConsolidator()
        result = consolidator.consolidate(aggregated_totals, category="bar")
        # result has same shape as aggregated_totals + optional 'issues' and 'merge_log'
    """

    def __init__(
        self,
        claude_client: Optional[ClaudeClient] = None,
    ):
        """Initialize consolidator.

        Args:
            claude_client: Optional pre-configured Claude client.
                If not provided, creates one with consolidation-tuned config.
        """
        if claude_client:
            self.claude_client = claude_client
        else:
            config = ClaudeConfig(
                max_input_tokens=25000,  # Consolidation reviews more data than a single shelfy
            )
            self.claude_client = ClaudeClient(config=config)

        self._system_prompt_cache: Dict[str, str] = {}

    def _get_system_prompt(self, category: str) -> str:
        """Get cached system prompt for category."""
        if category not in self._system_prompt_cache:
            self._system_prompt_cache[category] = build_consolidation_system_prompt(category)
        return self._system_prompt_cache[category]

    def consolidate(
        self,
        aggregated_totals: Dict[str, Any],
        category: str = "bar",
    ) -> Dict[str, Any]:
        """Run consolidation on aggregated inventory totals.

        Args:
            aggregated_totals: Output from shelfy_storage.get_aggregated_totals().
                Expected shape: {items: [...], shelfies_count: N, areas_covered: [...]}
            category: Inventory category (bar, kitchen).

        Returns:
            Same shape as input with consolidated items, plus:
            - issues: List of problems found (duplicates merged, categories fixed, items flagged)
            - merge_log: What was merged and why
            On failure: returns the original aggregated_totals unchanged.
        """
        items = aggregated_totals.get("items", [])

        # Skip consolidation if there are no items or only one item
        if len(items) <= 1:
            log.info("Consolidation skipped: %d items (nothing to consolidate)", len(items))
            return aggregated_totals

        log.info(
            "Starting consolidation for %s: %d items from %d shelfies",
            category,
            len(items),
            aggregated_totals.get("shelfies_count", 0),
        )

        try:
            system_prompt = self._get_system_prompt(category)
            user_prompt = build_consolidation_user_prompt(items)

            response = self.claude_client.call(
                system_prompt=system_prompt,
                user_content=user_prompt,
                extract_json=True,
            )

            if not response.success:
                log.error("Consolidation Claude call failed: %s", response.error)
                return aggregated_totals

            if not response.json_data:
                log.error("Consolidation: no JSON extracted from response")
                return aggregated_totals

            json_data = response.json_data
            consolidated_items = json_data.get("consolidated_items", [])
            issues = json_data.get("issues", [])

            if not consolidated_items:
                log.warning("Consolidation returned empty items, using original")
                return aggregated_totals

            log.info(
                "Consolidation complete: %d → %d items, %d issues found (input=%d, output=%d tokens)",
                len(items),
                len(consolidated_items),
                len(issues),
                response.usage.get("input_tokens", 0) if response.usage else 0,
                response.usage.get("output_tokens", 0) if response.usage else 0,
            )

            # Build merge_log from issues for display
            merge_log = []
            for issue in issues:
                if issue.get("type") == "merged_duplicate":
                    originals = issue.get("original_names", [])
                    merged_as = issue.get("merged_as", "")
                    qty = issue.get("combined_quantity", "")
                    merge_log.append(
                        f"Merged {' + '.join(repr(n) for n in originals)} → '{merged_as}' ({qty})"
                    )
                elif issue.get("type") == "category_fix":
                    merge_log.append(
                        f"Moved '{issue.get('product', '')}' from {issue.get('was', '')} to {issue.get('corrected_to', '')}"
                    )
                elif issue.get("type") == "needs_human_input":
                    merge_log.append(
                        f"Flagged: '{issue.get('product', '')}' — {issue.get('reason', 'needs review')}"
                    )

            # Return in the same shape the template expects
            return {
                "items": consolidated_items,
                "shelfies_count": aggregated_totals.get("shelfies_count", 0),
                "areas_covered": aggregated_totals.get("areas_covered", []),
                "issues": issues,
                "merge_log": merge_log,
            }

        except Exception as e:
            log.error("Consolidation failed (returning raw totals): %s", e, exc_info=True)
            return aggregated_totals
