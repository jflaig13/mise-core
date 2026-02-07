#!/usr/bin/env python3
"""
Generate Inventory Breakdown Report - Mobile-friendly HTML showing per-item breakdown by shelfy.

Usage: python3 generate_breakdown_report.py <date_code> [--food]
Example: python3 generate_breakdown_report.py 013126

Output: <date_code>_Inventory_Breakdown.html
"""

import re
import sys
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Configuration
MISE_CORE = Path.home() / "mise-core"
TRANSCRIPTS_DIR = MISE_CORE / "transcripts"
OUTPUT_DIR = MISE_CORE / "inventory_agent"

# Word to number mapping
WORD_TO_NUM = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
    'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
    'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'twenty-one': 21,
    'twenty-two': 22, 'twenty-three': 23, 'twenty-four': 24,
    'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28,
    'thirty': 30, 'thirty-three': 33, 'thirty-four': 34,
    'thirty-eight': 38, 'half': 0.5, 'quarter': 0.25,
    'three-quarters': 0.75, 'full': 1.0
}

# Product name normalization (same as clean script)
NAME_MAPPINGS = {
    # Beer - Cans
    "coors light": "Coors Light 12oz Can",
    "coors lights": "Coors Light 12oz Can",
    "coors": "Coors Light 12oz Can",
    "miller lite": "Miller Lite 12oz Can",
    "miller light": "Miller Lite 12oz Can",
    "miller lights": "Miller Lite 12oz Can",
    "michelob ultra": "Michelob Ultra 12oz Can",
    "michelob ultras": "Michelob Ultra 12oz Can",
    "pacifico": "Pacifico 12oz Can",
    "pacificos": "Pacifico 12oz Can",
    "yingling": "Yuengling 12oz Can",
    "yinglings": "Yuengling 12oz Can",
    "athletic non-alcoholic brews": "Athletic N/A 12oz Can",
    "athletic non-alcoholic beers": "Athletic N/A 12oz Can",
    "athletic": "Athletic N/A 12oz Can",
    "high noon watermelon": "High Noon Watermelon 12oz Can",
    "high noon watermelons": "High Noon Watermelon 12oz Can",
    "watermelon high noons": "High Noon Watermelon 12oz Can",
    "more high noon watermelons": "High Noon Watermelon 12oz Can",
    "high noon pineapple": "High Noon Pineapple 12oz Can",
    "high noon pineapples": "High Noon Pineapple 12oz Can",
    "pineapple high noon": "High Noon Pineapple 12oz Can",
    "pineapple high rises": "D9 High Rise Pineapple 12oz Can",
    "high rise pineapple": "D9 High Rise Pineapple 12oz Can",
    "high rise blueberry": "D9 High Rise Blueberry 12oz Can",
    "blueberry high rises": "D9 High Rise Blueberry 12oz Can",
    "high-rise blue bear": "D9 High Rise Blueberry 12oz Can",
    "mom waters": "Mom Water Assorted 12oz Can",
    "more 4-pack of mom waters": "Mom Water Assorted 12oz Can",
    "30a ipa cans": "Grayton 30A IPA 12oz Can",
    "30a rosé gose cans": "Grayton 30A Rose Gose 12oz Can",
    "red bull regular": "Red Bull 8.4oz Can",
    "red bulls": "Red Bull 8.4oz Can",
    "red bull sugar-free": "Red Bull Sugar Free 8.4oz Can",
    "red bull sugar free": "Red Bull Sugar Free 8.4oz Can",

    # Beer - Kegs
    "30a beach blonde ale": "Grayton 30A Beach Blonde Ale Keg",
    "kona big wave": "Kona Big Wave Keg",
    "paradise park": "Urban South Paradise Park Keg",
    "stella artois": "Stella Artois Keg",
    "urban south holy roller": "Urban South Holy Roller Keg",

    # Wine
    "30a chardonnay": "30A Chardonnay",
    "bottles 30a chardonnay": "30A Chardonnay",
    "30a pinot noir": "30A Pinot Noir",
    "30a rose": "30A Rose",
    "30a sauvignon blanc": "30A Sauvignon Blanc",
    "scarpetta": "Scarpetta Pinot Grigio",
    "scarpetta pinot grigio": "Scarpetta Pinot Grigio",
    "more bottles of scarpetta": "Scarpetta Pinot Grigio",
    "squealing pig": "Squealing Pig Sauvignon Blanc",
    "more bottle of squealing pig": "Squealing Pig Sauvignon Blanc",
    "squealing": "Squealing Pig Sauvignon Blanc",
    "windstorm chardonnay": "Windstorm Chardonnay",
    "more bottle of windstorm chardonnay": "Windstorm Chardonnay",
    "windstorm cabernet sauvignon": "Windstorm Cabernet Sauvignon",
    "canoe ridge merlot": "Canoe Ridge Merlot",
    "bottles canoe ridge merlot": "Canoe Ridge Merlot",
    "gearbox": "Gearbox Pinot Noir",
    "gearbox pinot": "Gearbox Pinot Noir",
    "gearbox pinot noir": "Gearbox Pinot Noir",
    "carter's lot rose": "Carter's Lot Rose",
    "charles de fer brut": "Charles De Fere Brut",
    "charles de fair brute": "Charles De Fere Brut",
    "bottles charles": "Charles De Fere Brut",
    "more bottle of charles de fer": "Charles De Fere Brut",
    "marca de caceres cava brute": "Marca De Caceres Cava Brut",
    "bottles marque de caseres cava brut": "Marca De Caceres Cava Brut",
    "shaker red blend": "Shaker Red Blend",

    # Liquor - keep the list manageable, add more as needed
    "aperol": "Aperol",
    "campari": "Campari",
    "crown royal": "Crown Royal",
    "fireball": "Fireball",
    "hendrick's gin": "Hendrick's Gin",
    "jägermeister": "Jagermeister",
    "jack daniel's": "Jack Daniel's",
    "jack daniels": "Jack Daniel's",
    "jim beam": "Jim Beam",
    "maker's mark": "Maker's Mark",
    "tankeray london dry gin": "Tanqueray Gin",
    "tankeray": "Tanqueray Gin",
    "tito's": "Tito's Vodka",
    "wheatley's vodka": "Wheatley's Vodka",
    "wheatley's": "Wheatley's Vodka",
    "wheatleys": "Wheatley's Vodka",
    "woodford": "Woodford Reserve",
    "woodford reserve": "Woodford Reserve",
    "grey goose": "Grey Goose Vodka 1L",
    "grey goose 1 liter": "Grey Goose Vodka 1L",
    "pueblo viejo tequila": "Pueblo Viejo Tequila",
    "pueblo viejo": "Pueblo Viejo Tequila",
    "yave coconut tequila": "Yave Coconut Tequila",
    "yave": "Yave Coconut Tequila",

    # Mixers
    "cream of coconut": "Cream of Coconut",
    "blue agave syrup": "Blue Agave Syrup",
    "strawberry puree": "Strawberry Puree",
    "grenadine": "Grenadine",
    "ginger beer": "Ginger Beer",
    "margarita mix": "Margarita Mix",
    "watermelon mixer": "Watermelon Mix",
    "watermelon": "Watermelon Mix",
    "mojito": "Mojito Mix",
    "margarita": "Margarita Mix",
}


def parse_quantity(text):
    """Extract numeric quantity from text."""
    text = text.lower().strip()
    for word, num in WORD_TO_NUM.items():
        if text.startswith(word):
            return num
    pct_match = re.match(r'^(\d+(?:\.\d+)?)\s*%', text)
    if pct_match:
        return float(pct_match.group(1)) / 100
    num_match = re.match(r'^(\d+(?:\.\d+)?)', text)
    if num_match:
        return float(num_match.group(1))
    return None


def parse_transcript_line(line):
    """Parse a single line into (quantity, item, unit) tuples."""
    items = []
    line = line.strip()
    if not line:
        return items

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

        # Pattern: "X [number]-packs of [Product]"
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

        # Pattern: "X [Product]" (e.g., "6 Pacificos")
        simple_match = re.match(r'^(\d+)\s+(.+)', part, re.I)
        if simple_match:
            qty = int(simple_match.group(1))
            product = simple_match.group(2).strip()
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


def normalize_product_name(raw_name):
    """Normalize product name using mappings."""
    key = raw_name.lower().strip().rstrip('.')
    return NAME_MAPPINGS.get(key, raw_name.strip().rstrip('.'))


def categorize_product(name, unit):
    """Categorize a product based on its name and unit."""
    name_lower = name.lower()
    if "keg" in name_lower or unit == "Keg":
        return "Beer (Kegs)"
    if any(x in name_lower for x in ['can', 'coors', 'miller', 'michelob', 'pacifico', 'yuengling', 'athletic', 'high noon', 'high rise', 'mom water', 'red bull', 'grayton', 'corona']):
        return "Beer (Cans)"
    if any(x in name_lower for x in ['chardonnay', 'pinot', 'merlot', 'rose', 'rosé', 'cabernet', 'sauvignon', 'brut', 'cava', 'gearbox', 'squealing', 'scarpetta', 'windstorm', 'carter', 'charles', 'marca', 'shaker']):
        return "Wine"
    if any(x in name_lower for x in ['mix', 'puree', 'syrup', 'grenadine', 'coconut', 'ginger']):
        return "Mixers & N/A"
    return "Liquor"


def format_quantity(qty):
    """Format quantity for display."""
    if qty == int(qty):
        return str(int(qty))
    return f"{qty:.2f}"


def generate_breakdown_html(date_code, inventory_data, output_path):
    """Generate mobile-friendly HTML breakdown report."""

    # Parse date for display
    try:
        month = int(date_code[:2])
        day = int(date_code[2:4])
        year = int("20" + date_code[4:6])
        date_display = f"{month}/{day}/{year}"
    except:
        date_display = date_code

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Breakdown - {date_display}</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #F9F6F1;
            color: #1B2A4E;
            padding: 16px;
            max-width: 600px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            padding: 20px 0;
            border-bottom: 3px solid #1B2A4E;
            margin-bottom: 20px;
        }}
        h1 {{
            font-size: 24px;
            color: #1B2A4E;
            margin-bottom: 8px;
        }}
        .date {{
            font-size: 16px;
            color: #666;
        }}
        .category {{
            margin-bottom: 24px;
        }}
        .category-header {{
            background: #1B2A4E;
            color: white;
            padding: 12px 16px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 8px 8px 0 0;
            position: sticky;
            top: 0;
        }}
        .item {{
            background: white;
            border: 1px solid #ddd;
            border-top: none;
            padding: 16px;
        }}
        .item:last-child {{
            border-radius: 0 0 8px 8px;
        }}
        .item-name {{
            font-weight: 600;
            font-size: 16px;
            color: #1B2A4E;
            margin-bottom: 8px;
        }}
        .final-count {{
            font-size: 20px;
            color: #B5402F;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .breakdown {{
            font-size: 14px;
            color: #666;
            background: #f5f5f5;
            padding: 8px 12px;
            border-radius: 4px;
            font-family: monospace;
        }}
        .breakdown-label {{
            font-weight: 600;
            color: #1B2A4E;
        }}
        .summary {{
            background: #1B2A4E;
            color: white;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .summary-number {{
            font-size: 32px;
            font-weight: 700;
        }}
        .summary-label {{
            font-size: 14px;
            opacity: 0.8;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Inventory Breakdown</h1>
        <div class="date">{date_display}</div>
    </header>

    <div class="summary">
        <div class="summary-number">{len(inventory_data)}</div>
        <div class="summary-label">Total Products Counted</div>
    </div>
'''

    # Group by category
    categories = defaultdict(list)
    for product_name, data in inventory_data.items():
        cat = categorize_product(product_name, data.get('unit', ''))
        categories[cat].append((product_name, data))

    # Sort categories in preferred order
    cat_order = ["Beer (Cans)", "Beer (Kegs)", "Wine", "Liquor", "Mixers & N/A", "Food"]

    for cat_name in cat_order:
        if cat_name not in categories:
            continue
        items = categories[cat_name]
        if not items:
            continue

        html += f'''
    <div class="category">
        <div class="category-header">{cat_name}</div>
'''
        for product_name, data in sorted(items, key=lambda x: x[0]):
            total = data['total']
            breakdown_parts = data['breakdown']
            unit = data.get('unit', '')

            # Format breakdown string
            breakdown_str = " + ".join([f"{format_quantity(qty)} ({loc})" for loc, qty in breakdown_parts])

            html += f'''        <div class="item">
            <div class="item-name">{product_name}</div>
            <div class="final-count">{format_quantity(total)} {unit}{"s" if total != 1 else ""}</div>
            <div class="breakdown">
                <span class="breakdown-label">Breakdown:</span> {breakdown_str}
            </div>
        </div>
'''
        html += '    </div>\n'

    html += f'''
    <footer>
        Generated by Mise &middot; {datetime.now().strftime("%Y-%m-%d %H:%M")}
    </footer>
</body>
</html>
'''

    with open(output_path, 'w') as f:
        f.write(html)

    return output_path


def process_inventory(date_code):
    """Process all shelfies for a given date and generate breakdown report."""

    # Find all shelfies for this date
    shelfies = list(TRANSCRIPTS_DIR.glob(f"{date_code}_*.txt"))

    if not shelfies:
        print(f"No shelfies found for {date_code} in {TRANSCRIPTS_DIR}")
        return None

    print(f"Found {len(shelfies)} shelfies for {date_code}:")
    for s in shelfies:
        print(f"  - {s.name}")

    # Track inventory by normalized product name
    # Structure: {normalized_name: {'total': X, 'breakdown': [(location, qty), ...], 'unit': 'Bottle'}}
    inventory = defaultdict(lambda: {'total': 0, 'breakdown': [], 'unit': None})

    for shelfy_path in shelfies:
        # Extract location from filename (e.g., "013126_TheOffice.txt" -> "The Office")
        location = shelfy_path.stem.replace(f"{date_code}_", "")
        # Add spaces before capitals for readability
        location = re.sub(r'([a-z])([A-Z])', r'\1 \2', location)

        print(f"\nProcessing {location}...")

        with open(shelfy_path, 'r') as f:
            content = f.read()

        # Parse lines
        lines = []
        for line in content.split('\n'):
            # Remove line number prefix
            line = re.sub(r'^\s*\d+→', '', line).strip()
            if line:
                lines.append(line)

        # Parse each line
        items_found = 0
        for line in lines:
            parsed = parse_transcript_line(line)
            for qty, product, unit in parsed:
                if qty and qty > 0 and product:
                    # Normalize product name
                    normalized = normalize_product_name(product)

                    # Skip junk entries
                    if normalized.lower() in ['bottle', 'bottles', 'mr', 'liter', 'milliliters', 'more bottle of']:
                        continue

                    inventory[normalized]['total'] += qty
                    inventory[normalized]['breakdown'].append((location, qty))
                    if unit:
                        inventory[normalized]['unit'] = unit
                    items_found += 1

        print(f"  Found {items_found} item entries")

    # Filter to only items with count > 0
    inventory = {k: v for k, v in inventory.items() if v['total'] > 0}

    # Generate output
    output_dir = OUTPUT_DIR / date_code
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{date_code}_Inventory_Breakdown.html"

    generate_breakdown_html(date_code, inventory, output_path)

    print(f"\n{'='*60}")
    print(f"Breakdown report generated: {output_path}")
    print(f"Total products: {len(inventory)}")
    print(f"{'='*60}")

    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_breakdown_report.py <date_code>")
        print("Example: python3 generate_breakdown_report.py 013126")
        sys.exit(1)

    date_code = sys.argv[1]
    process_inventory(date_code)
