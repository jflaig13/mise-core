"""Inventory agent system prompt builder.

Constructs the system prompt for the inventory agent by loading:
- Product catalog (inventory_catalog.json with 880 products)
- Manual item mappings (bar_item_mappings.json, food_item_mappings.json)
- Inventory parsing rules

This follows the same pattern as payroll_prompt.py.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List

log = logging.getLogger(__name__)


def load_catalog(category: str = "bar") -> Dict[str, List[Dict]]:
    """Load product catalog for a specific category.

    Args:
        category: Category to load (bar, food, supplies, or "all")

    Returns:
        Dict with category keys and product lists
    """
    catalog_path = Path(__file__).parent.parent.parent.parent / "data" / "inventory_catalog.json"

    if not catalog_path.exists():
        log.warning("Inventory catalog not found at %s", catalog_path)
        return {}

    with catalog_path.open("r") as f:
        full_catalog = json.load(f)

    # If requesting specific category, return just that
    if category != "all":
        # Map category name to catalog key
        category_map = {
            "bar": ["beer_cost", "wine_cost", "liquor_cost", "n_a_beverage_cost"],
            "food": ["grocery_and_dry_goods"],
            "supplies": ["grocery_and_dry_goods"],  # Overlap with food
        }

        catalog = {}
        for cat_key in category_map.get(category, []):
            if cat_key in full_catalog:
                catalog[cat_key] = full_catalog[cat_key]

        return catalog

    # Return all categories
    return {k: v for k, v in full_catalog.items() if k != "global_rules"}


def load_manual_mappings() -> Dict[str, str]:
    """Load manual item mappings from bar_item_mappings.json and food_item_mappings.json.

    Returns:
        Dict of spoken_name -> canonical_product_name
    """
    mappings = {}

    # Load bar mappings
    bar_path = Path(__file__).parent.parent.parent.parent / "inventory_agent" / "bar_item_mappings.json"
    if bar_path.exists():
        with bar_path.open("r") as f:
            data = json.load(f)
            mappings.update(data.get("mappings", {}))

    # Load food mappings
    food_path = Path(__file__).parent.parent.parent.parent / "inventory_agent" / "food_item_mappings.json"
    if food_path.exists():
        with food_path.open("r") as f:
            data = json.load(f)
            # Merge, bar takes precedence
            food_mappings = data.get("mappings", {})
            for key, value in food_mappings.items():
                if key not in mappings:
                    mappings[key] = value

    log.info("Loaded %d manual item mappings", len(mappings))
    return mappings


def format_catalog_for_prompt(catalog: Dict[str, List[Dict]], limit: int = 100) -> str:
    """Format catalog for inclusion in prompt (limited to avoid token bloat).

    Args:
        catalog: Full catalog dict
        limit: Max number of products to include per category

    Returns:
        Formatted string for prompt
    """
    lines = []

    for category_key, products in catalog.items():
        lines.append(f"\n### {category_key.upper().replace('_', ' ')}")

        for product in products[:limit]:
            item_name = product.get("item", "Unknown")
            keywords = product.get("keywords", [])
            unit = product.get("report_by_unit", "")

            # Format: "Product Name (unit: bottles, keywords: cab, sauv, red)"
            keyword_str = ", ".join(keywords[:5]) if keywords else "none"
            lines.append(f"- {item_name} (unit: {unit}, keywords: {keyword_str})")

        if len(products) > limit:
            lines.append(f"... and {len(products) - limit} more products")

    return "\n".join(lines)


def format_manual_mappings_for_prompt(mappings: Dict[str, str], limit: int = 50) -> str:
    """Format manual mappings for inclusion in prompt.

    Args:
        mappings: Dict of spoken_name -> canonical_name
        limit: Max mappings to include

    Returns:
        Formatted string for prompt
    """
    lines = []

    for idx, (spoken, canonical) in enumerate(mappings.items()):
        if idx >= limit:
            lines.append(f"... and {len(mappings) - limit} more mappings")
            break
        lines.append(f'  "{spoken}" → "{canonical}"')

    return "\n".join(lines)


def build_inventory_system_prompt(category: str = "bar") -> str:
    """Build the complete system prompt for the inventory agent.

    Args:
        category: Inventory category (bar, food, supplies)

    Returns:
        Complete system prompt string for Claude API call.
    """
    # Load catalog and mappings
    catalog = load_catalog(category)
    manual_mappings = load_manual_mappings()

    # Count products
    total_products = sum(len(products) for products in catalog.values())
    log.info("Building inventory prompt (category=%s, products=%d, mappings=%d)",
             category, total_products, len(manual_mappings))

    # Format for prompt (limit to avoid token bloat)
    catalog_text = format_catalog_for_prompt(catalog, limit=100)
    mappings_text = format_manual_mappings_for_prompt(manual_mappings, limit=50)

    return f'''# Inventory Agent - Shelfy Inventory Parser

You are the Inventory Agent for Papa Surf restaurant, responsible for parsing inventory count transcripts and producing structured JSON.

## Your Task

Parse the provided inventory transcript and:
1. Extract all product names, quantities, and units
2. Normalize product names to the canonical catalog names
3. Handle Whisper ASR transcription errors
4. Return a valid inventory JSON

## CRITICAL RULES

### Product Name Normalization

The transcript comes from Whisper ASR, so names may be misspelled or incomplete.

**Your job**: Match spoken names to canonical catalog names.

**Sources of truth (in priority order):**
1. **Manual mappings** (see below) - these are EXACT mappings
2. **Product catalog keywords** - fuzzy match using keywords
3. **Your knowledge** - use context clues (brand names, sizes, etc.)

### Manual Mappings (Highest Priority)

These are known spoken-name → canonical-name mappings:

{mappings_text}

**RULE**: If the transcript says "margarita mix", you MUST use "Bar Mix, Margarita" (from manual mapping).

### Product Catalog (Papa Surf Products)

Category: **{category.upper()}**

Total products in catalog: **{total_products}**

{catalog_text}

**RULE**: Match transcript names to catalog names using keywords. For example:
- Transcript: "cab sauv" → Match: "Cabernet Sauvignon" (keywords: cab, sauv)
- Transcript: "pinot g" → Match: "Pinot Grigio" (keywords: pinot, grigio)
- Transcript: "blue moon" → Match: "Blue Moon Belgian White Ale" (keywords: blue, moon)

### Handling Whisper ASR Errors

Common transcription errors:
- "tree" → "three"
- "to" → "two"
- "for" → "four"
- "cab sauv" → "Cabernet Sauvignon"
- "pinot g" → "Pinot Grigio"
- Brand names often garbled (e.g., "stirrings" → "stir rings")

**RULE**: Use your knowledge to correct obvious ASR errors.

### Quantity and Unit Inference

**Quantities:**
- If clear number stated: use it
- If unclear (e.g., "about half"): estimate and add note
- If missing: set to `null` and add note

**Units:**
- Wine: usually "bottles"
- Beer: usually "cases" (but can be "kegs" or individual cans)
- Liquor: usually "bottles"
- Food: varies (lbs, oz, each, cases, etc.)

**Fractions:**
- "half" = 0.5
- "quarter" = 0.25
- "three quarters" = 0.75
- "full" or "one" = 1.0

### Output Schema

You must return JSON matching this schema:

```json
{{
  "category": "{category}",
  "area": "optional area (front bar, back bar, kitchen, etc.)",
  "items": [
    {{
      "product_name": "canonical product name from catalog",
      "quantity": <number or null>,
      "unit": "bottles|cases|kegs|lbs|oz|each|etc",
      "notes": "optional notes if ambiguous",
      "confidence": <0.0-1.0 match confidence>,
      "spoken_name": "what was actually said in transcript",
      "needs_review": <true if confidence < 0.8, false otherwise>
    }}
  ],
  "counted_by": "person who did inventory (if mentioned)",
  "timestamp": "ISO 8601 timestamp (if mentioned, else null)"
}}
```

**Critical**:
- `product_name` MUST be your best guess at the canonical name from the catalog
- NEVER set product_name to "Unknown" - always provide your best match
- If you match spoken "30A Beach Blonde" to catalog "Grayton 30A Beach Blonde Ale Keg", use "Grayton 30A Beach Blonde Ale Keg" as product_name
- DO NOT invent products not in the transcript
- DO NOT assume quantities not stated

### Confidence Scoring

For EVERY item, you MUST include:
- `confidence`: Float 0.0-1.0 indicating how confident you are in the product_name match
  - 1.0 = Exact match or manual mapping hit
  - 0.8-0.99 = High confidence (clear keyword match, well-known product)
  - 0.5-0.79 = Medium confidence (partial match, could be multiple products)
  - 0.0-0.49 = Low confidence (guessing, unclear transcription)
- `spoken_name`: The exact text from the transcript (before normalization)
- `needs_review`: Set to `true` if confidence < 0.8, otherwise `false`

This allows users to verify uncertain matches.

### What NOT to Do

❌ DO NOT add products not mentioned in transcript
❌ DO NOT guess quantities if not stated (use null instead)
❌ DO NOT use spoken names (e.g., "margarita mix") - use canonical names (e.g., "Bar Mix, Margarita")
❌ DO NOT set product_name to "Unknown" - always use the matched canonical catalog name
❌ DO NOT put the canonical name in notes - put it in product_name
❌ DO NOT include reasoning or chain-of-thought in your response

## Example

**Transcript:**
"Front bar inventory. We have 12 bottles of margarita mix, those 750 milliliter ones from Stirrings. And about half a case of Coors Light cans left. Also got some stella kegs."

**Your output:**
```json
{{
  "category": "bar",
  "area": "front bar",
  "items": [
    {{
      "product_name": "Bar Mix, Margarita",
      "quantity": 12,
      "unit": "bottles",
      "notes": "750ml Stirrings brand",
      "confidence": 1.0,
      "spoken_name": "margarita mix",
      "needs_review": false
    }},
    {{
      "product_name": "Coors Light 12oz Can",
      "quantity": 0.5,
      "unit": "cases",
      "notes": "Approximate - 'about half a case'",
      "confidence": 0.95,
      "spoken_name": "Coors Light cans",
      "needs_review": false
    }},
    {{
      "product_name": "Stella Artois Keg",
      "quantity": null,
      "unit": "kegs",
      "notes": "Quantity not specified",
      "confidence": 0.7,
      "spoken_name": "stella kegs",
      "needs_review": true
    }}
  ],
  "counted_by": null,
  "timestamp": null
}}
```

**Why this works:**
- "margarita mix" → "Bar Mix, Margarita" (from manual mapping, confidence=1.0)
- "Coors Light cans" → "Coors Light 12oz Can" (from catalog keywords, confidence=0.95)
- "stella kegs" → "Stella Artois Keg" (partial match, confidence=0.7, needs_review=true)
- "about half a case" → 0.5 (fraction inference)
- Added notes for clarity

---

**Remember**: Respond ONLY with valid JSON. No markdown, no explanations, no chain-of-thought. Just the JSON.
'''


def build_inventory_user_prompt(
    transcript: str,
    category: str = "bar",
    area: str = "",
) -> str:
    """Build user prompt with transcript.

    Args:
        transcript: Raw transcript from ASR
        category: Inventory category
        area: Optional area hint

    Returns:
        User prompt string
    """
    area_hint = f"\nArea hint: {area}" if area else ""

    return f"""Parse this inventory transcript into JSON:

TRANSCRIPT:
\"\"\"
{transcript}
\"\"\"

CATEGORY: {category}{area_hint}

Output valid JSON only (no markdown, no explanations).
"""
