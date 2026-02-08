"""Consolidation prompt builder for inventory post-aggregation cleanup.

After all shelfies are aggregated by summing quantities grouped by product_name,
this prompt asks Claude to review the aggregated list and fix:
- Duplicate product names (spelling variants, ASR errors, abbreviations)
- Miscategorized items (e.g., Merlot under Beer)
- Generic/unresolvable items (no product name, ambiguous)
- Items with null quantities that were silently dropped

Reuses load_catalog() and load_manual_mappings() from inventory_prompt.py.
"""

from __future__ import annotations

import json
import logging
from typing import Dict, List, Any

from .inventory_prompt import (
    load_catalog,
    load_manual_mappings,
    format_catalog_for_prompt,
    format_manual_mappings_for_prompt,
)

log = logging.getLogger(__name__)


def build_consolidation_system_prompt(category: str = "bar") -> str:
    """Build system prompt for the consolidation pass.

    Args:
        category: Inventory category (bar, kitchen)

    Returns:
        System prompt string for Claude API call.
    """
    catalog = load_catalog(category)
    manual_mappings = load_manual_mappings()

    total_products = sum(len(products) for products in catalog.values())
    log.info(
        "Building consolidation prompt (category=%s, products=%d, mappings=%d)",
        category, total_products, len(manual_mappings),
    )

    # Use higher limits for consolidation since we need full catalog context
    catalog_text = format_catalog_for_prompt(catalog, limit=250)
    mappings_text = format_manual_mappings_for_prompt(manual_mappings, limit=100)

    return f'''# Inventory Consolidation Agent

You are reviewing an **already-aggregated** inventory list for Papa Surf restaurant.

The list was built by summing quantities from multiple shelfy counts (storage areas).
Each shelfy was parsed independently, so the aggregated list may contain:

1. **Duplicate products** with different spellings (ASR errors, abbreviations, typos)
   - Example: "Bowls Elderflower Liqueur" and "Bols Elderflower Liqueur" are the same product
   - Example: "Titos" and "Tito's Handmade Vodka" are the same product

2. **Miscategorized items** (product listed under wrong category)
   - Example: "Canoe Ridge Merlot" showing up in the beer category — should be wine

3. **Generic/unresolvable items** that need human input
   - Example: "kegs" with no brand or product name
   - Example: "bottles" with no product specified

4. **Items with null quantities** that were counted but quantity was unclear

## Your Task

Review the aggregated items below and:
1. **Merge duplicates**: If two entries are clearly the same product, combine their quantities and breakdowns. Use the canonical catalog name.
2. **Fix categories**: If a product is miscategorized, note the correction.
3. **Flag unresolvable items**: If a product name is too generic to identify, flag it for human input.
4. **Preserve everything else**: Do NOT remove items. Do NOT change quantities unless merging duplicates.

## Product Catalog (Papa Surf — {category.upper()})

Total products: **{total_products}**

{catalog_text}

## Manual Mappings (Known Spoken → Canonical)

{mappings_text}

## Output Schema

Return ONLY valid JSON matching this schema:

```json
{{{{
  "consolidated_items": [
    {{{{
      "product_name": "Canonical product name",
      "total_quantity": <number>,
      "unit": "bottles|cases|cans|kegs|etc",
      "category": "{category}",
      "breakdown": [
        {{{{"area": "Inside Bar", "quantity": 12, "shelfy_id": "..."}}}},
        {{{{"area": "Back Bar", "quantity": 3.4, "shelfy_id": "..."}}}}
      ]
    }}}}
  ],
  "issues": [
    {{{{
      "type": "merged_duplicate",
      "original_names": ["Name A", "Name B"],
      "merged_as": "Canonical Name",
      "combined_quantity": 15.4
    }}}},
    {{{{
      "type": "category_fix",
      "product": "Product Name",
      "was": "beer",
      "corrected_to": "wine"
    }}}},
    {{{{
      "type": "needs_human_input",
      "product": "kegs",
      "quantity": 3,
      "reason": "No product name — which brand/size?"
    }}}}
  ]
}}}}
```

## Rules

- **Do NOT invent products.** Only work with what's in the input.
- **Do NOT change quantities** unless merging two entries of the same product.
- **When merging**, combine breakdowns from both entries and sum their quantities.
- **Use the catalog name** when merging (e.g., merge "Titos" into "Tito's Handmade Vodka").
- **Every input item must appear in the output** — either as-is or merged into another entry.
- **If no issues found**, return the items unchanged with an empty issues array.
- **Respond ONLY with valid JSON.** No markdown, no explanations, no chain-of-thought.
'''


def build_consolidation_user_prompt(aggregated_items: List[Dict[str, Any]]) -> str:
    """Build user prompt with the aggregated items to review.

    Args:
        aggregated_items: List of aggregated item dicts from get_aggregated_totals()

    Returns:
        User prompt string with formatted items.
    """
    items_json = json.dumps(aggregated_items, indent=2)

    return f"""Review and consolidate the following aggregated inventory items.

AGGREGATED ITEMS ({len(aggregated_items)} products):

{items_json}

Return consolidated JSON only (no markdown, no explanations).
"""
