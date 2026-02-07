#!/usr/bin/env python3
"""
Parse 013126 inventory transcripts into structured inventory counts.
This handles the specific natural language format from the shelfies.
"""

import re
from collections import defaultdict
from pathlib import Path

# Read all transcript files
transcripts_dir = Path.home() / "mise-core/transcripts"
shelfies = [
    "013126_TheOffice.txt",
    "013126_InsideBar.txt",
    "013126_BackBar.txt",
    "013126_WalkIn.txt",
    "013126_Storage.txt"
]

# Word to number mapping
WORD_TO_NUM = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
    'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
    'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'twenty-one': 21,
    'twenty-two': 22, 'twenty-three': 23, 'twenty-four': 24,
    'twenty-eight': 28, 'thirty': 30, 'thirty-three': 33, 'thirty-four': 34,
    'thirty-eight': 38, 'half': 0.5, 'quarter': 0.25,
    'three-quarters': 0.75, 'full': 1.0
}

def parse_quantity(text):
    """Extract numeric quantity from text."""
    text = text.lower().strip()

    # Check word numbers first
    for word, num in WORD_TO_NUM.items():
        if text.startswith(word):
            return num

    # Check for percentage (e.g., "70%", "10%")
    pct_match = re.match(r'^(\d+(?:\.\d+)?)\s*%', text)
    if pct_match:
        return float(pct_match.group(1)) / 100

    # Check for decimal/integer
    num_match = re.match(r'^(\d+(?:\.\d+)?)', text)
    if num_match:
        return float(num_match.group(1))

    return None

def parse_line(line):
    """Parse a single line into (quantity, item, unit) tuples."""
    items = []
    line = line.strip()
    if not line:
        return items

    # Split by commas for multiple items
    parts = re.split(r',\s*', line)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Pattern: "X% of a bottle/keg of [Product]"
        pct_match = re.match(r'^(\d+(?:\.\d+)?)\s*%\s+of\s+a\s+(bottle|keg)\s+of\s+(.+)', part, re.I)
        if pct_match:
            qty = float(pct_match.group(1)) / 100
            unit = pct_match.group(2).capitalize()
            product = pct_match.group(3).strip()
            items.append((qty, product, unit))
            continue

        # Pattern: "half/quarter/full of a bottle/keg of [Product]"
        frac_match = re.match(r'^(half|quarter|three-quarters|full)\s+of\s+a\s+(bottle|keg)\s+of\s+(.+)', part, re.I)
        if frac_match:
            qty = WORD_TO_NUM.get(frac_match.group(1).lower(), 1)
            unit = frac_match.group(2).capitalize()
            product = frac_match.group(3).strip()
            items.append((qty, product, unit))
            continue

        # Pattern: "X bottles/kegs of [Product]"
        bottles_match = re.match(r'^(\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s+(bottles?|kegs?|cans?)\s+of\s+(.+)', part, re.I)
        if bottles_match:
            qty = parse_quantity(bottles_match.group(1))
            unit = bottles_match.group(2).rstrip('s').capitalize()
            product = bottles_match.group(3).strip()
            items.append((qty, product, unit))
            continue

        # Pattern: "X [number]-packs of [Product]" (e.g., "three 24-packs yingling")
        packs_match = re.match(r'^(\d+|one|two|three|four|five|six|seven|eight)\s+(\d+)-packs?\s+(?:of\s+)?(.+)', part, re.I)
        if packs_match:
            num_packs = parse_quantity(packs_match.group(1))
            pack_size = int(packs_match.group(2))
            qty = num_packs * pack_size
            product = packs_match.group(3).strip()
            items.append((qty, product, "Can"))
            continue

        # Pattern: "X 4-packs of [Product]"
        fourpack_match = re.match(r'^(\d+)\s+(4-packs?|four-packs?)\s+(?:of\s+)?(.+)', part, re.I)
        if fourpack_match:
            num_packs = int(fourpack_match.group(1))
            qty = num_packs * 4
            product = fourpack_match.group(3).strip()
            items.append((qty, product, "Can"))
            continue

        # Pattern: "X [Product]" (e.g., "6 Pacificos", "13 Athletic Non-Alcoholic Brews")
        simple_match = re.match(r'^(\d+)\s+(.+)', part, re.I)
        if simple_match:
            qty = int(simple_match.group(1))
            product = simple_match.group(2).strip()
            # Guess unit based on product name
            if 'keg' in product.lower():
                unit = 'Keg'
            elif any(x in product.lower() for x in ['bottle', 'wine', 'liqueur', 'vodka', 'rum', 'tequila', 'whiskey', 'gin', 'bourbon']):
                unit = 'Bottle'
            else:
                unit = 'Can'
            items.append((qty, product, unit))
            continue

        # Pattern: "X bottle of [Product]" (singular)
        single_match = re.match(r'^(\d+|one|two|three)\s+bottle\s+of\s+(.+)', part, re.I)
        if single_match:
            qty = parse_quantity(single_match.group(1))
            product = single_match.group(2).strip()
            items.append((qty, product, "Bottle"))
            continue

    return items

# Aggregate inventory
inventory = defaultdict(lambda: {"qty": 0, "unit": None, "sources": []})

for shelfy in shelfies:
    filepath = transcripts_dir / shelfy
    location = shelfy.replace("013126_", "").replace(".txt", "")

    if not filepath.exists():
        print(f"Warning: {shelfy} not found")
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    # Remove line numbers if present
    lines = []
    for line in content.split('\n'):
        # Remove line number prefix (e.g., "     1→")
        line = re.sub(r'^\s*\d+→', '', line).strip()
        if line:
            lines.append(line)

    # Parse each line
    for line in lines:
        parsed = parse_line(line)
        for qty, product, unit in parsed:
            if qty and product:
                # Normalize product name
                product = product.strip().rstrip('.')
                key = product.lower()
                inventory[key]["qty"] += qty
                inventory[key]["unit"] = unit
                inventory[key]["sources"].append(f"{location}: {qty}")
                inventory[key]["name"] = product

# Print inventory report
print("=" * 80)
print("013126 INVENTORY COUNT - January 31, 2026")
print("=" * 80)

# Group by category (simplified)
categories = {
    "LIQUOR": [],
    "BEER (Cans)": [],
    "BEER (Kegs)": [],
    "WINE": [],
    "MIXERS & N/A": [],
    "OTHER": []
}

def categorize(name, unit):
    name_lower = name.lower()
    if unit == "Keg":
        return "BEER (Kegs)"
    if any(x in name_lower for x in ['vodka', 'rum', 'tequila', 'whiskey', 'gin', 'bourbon', 'mezcal', 'liqueur', 'schnapps', 'aperol', 'campari', 'jager', 'fireball', 'curacao', 'triple sec', 'chambord', 'nocello', 'limoncello']):
        return "LIQUOR"
    if any(x in name_lower for x in ['wine', 'rose', 'rosé', 'chardonnay', 'cabernet', 'pinot', 'merlot', 'sauvignon', 'brut', 'cava', 'champagne', 'prosecco', 'squealing pig', 'scarpetta', 'gearbox']):
        return "WINE"
    if any(x in name_lower for x in ['beer', 'ale', 'ipa', 'lager', 'coors', 'miller', 'michelob', 'pacifico', 'corona', 'yingling', 'yuengling', 'stella', 'athletic', 'high noon', 'high rise', 'mom water']):
        return "BEER (Cans)"
    if any(x in name_lower for x in ['mix', 'juice', 'syrup', 'puree', 'grenadine', 'bitters', 'coconut', 'red bull', 'ginger beer']):
        return "MIXERS & N/A"
    return "OTHER"

for key, data in sorted(inventory.items()):
    cat = categorize(data["name"], data["unit"])
    categories[cat].append(data)

# Output by category
for cat_name, items in categories.items():
    if not items:
        continue
    print(f"\n{cat_name}")
    print("-" * 40)
    for item in sorted(items, key=lambda x: x["name"]):
        qty = item["qty"]
        unit = item["unit"]
        name = item["name"]
        # Format quantity nicely
        if qty == int(qty):
            qty_str = str(int(qty))
        else:
            qty_str = f"{qty:.2f}"
        print(f"  {qty_str} {unit}(s) - {name}")

print("\n" + "=" * 80)
print("Note: This is the raw parsed count. Review for accuracy before importing to MarginEdge.")
print("=" * 80)

# Also save to JSON
import json
output_path = Path(__file__).parent / "013126_inventory_final.json"
output_data = {
    "date": "2026-01-31",
    "count_type": "full_bar_inventory",
    "locations": ["TheOffice", "InsideBar", "BackBar", "WalkIn", "Storage"],
    "items": [
        {
            "product": data["name"],
            "quantity": data["qty"],
            "unit": data["unit"],
            "breakdown": data["sources"]
        }
        for key, data in sorted(inventory.items())
    ]
}

with open(output_path, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"\nJSON saved to: {output_path}")
