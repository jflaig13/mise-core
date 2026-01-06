#!/usr/bin/env python3
"""
Parse bar inventory transcript and match to products catalog.
Follows LIM workflow specification.

Usage: python3 parse_bar_inventory.py <date_folder>
Example: python3 parse_bar_inventory.py 123125
"""

import re
import csv
import json
import sys
from pathlib import Path

# Get date folder from command line argument
if len(sys.argv) < 2:
    print("Usage: python3 parse_bar_inventory.py <date_folder>")
    print("Example: python3 parse_bar_inventory.py 123125")
    sys.exit(1)

date_folder = sys.argv[1]
inventory_dir = Path(__file__).parent / date_folder

# Read the transcript
transcript_file = inventory_dir / f'{date_folder}_inventory_bar.txt'
with open(transcript_file, 'r') as f:
    transcript = f.read()

# Load products catalog
products_dir = Path(__file__).parent / 'products'

def normalize_product_name(name):
    """Normalize product name for matching"""
    name = name.lower().strip()
    # Remove accents and umlauts
    name = name.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    name = name.replace('ä', 'a').replace('ë', 'e').replace('ï', 'i').replace('ö', 'o').replace('ü', 'u')
    name = name.replace('ñ', 'n').replace('ç', 'c')
    # Standardize punctuation
    name = name.replace(',', '')
    name = name.replace("'", "")
    name = name.replace('\u2019', '')
    # Remove filler words
    name = name.replace(' organic', '')
    name = name.replace(' original', '')
    name = name.replace('  ', ' ')
    return name

def load_products(csv_file):
    """Load products from CSV where On Inventory = Yes"""
    products = {}
    with open(products_dir / csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['On Inventory'] == 'Yes':
                name = row['Name']
                key = normalize_product_name(name)
                products[key] = {
                    'name': name,
                    'category': row['Category'],
                    'unit': row['Report By Unit']
                }
    return products

all_products = load_products(f'products_{date_folder}.csv')

# Manually add Red Bull even though it's marked "On Inventory = No" in catalog
# User wants both Red Bull and Red Bull Sugar Free counted under this SKU
all_products[normalize_product_name('Red Bull Assorted 8.4oz Can')] = {
    'name': 'Red Bull Assorted 8.4oz Can',
    'category': 'N/A Beverage Cost',
    'unit': 'Can'
}

# Load bar item mappings
bar_mappings_file = Path(__file__).parent / 'bar_item_mappings.json'
bar_mappings = {}
if bar_mappings_file.exists():
    with open(bar_mappings_file, 'r') as f:
        bar_mappings.update(json.load(f).get('mappings', {}))

# Also load food item mappings (for N/A Bev and Grocery/Dry Goods overlap)
food_mappings_file = Path(__file__).parent / 'food_item_mappings.json'
if food_mappings_file.exists():
    with open(food_mappings_file, 'r') as f:
        food_mappings = json.load(f).get('mappings', {})
        # Merge food mappings, but bar_mappings take precedence
        for key, value in food_mappings.items():
            if key not in bar_mappings:
                bar_mappings[key] = value

def parse_unit(report_by_unit):
    """Extract base unit from Report By Unit field"""
    unit_lower = report_by_unit.lower()
    if 'bottle' in unit_lower:
        return 'Bottle'
    elif 'can' in unit_lower:
        return 'Can'
    elif 'keg' in unit_lower:
        return 'Keg'
    elif 'gallon' in unit_lower:
        return 'Gallon'
    elif 'each' in unit_lower:
        return 'Each'
    elif 'liter' in unit_lower:
        return 'Liter'
    else:
        return report_by_unit

def word_to_number(word):
    """Convert word numbers to digits"""
    word_map = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
        'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
        'eighteen': 18, 'nineteen': 19, 'twenty': 20
    }
    return word_map.get(word.lower(), None)

def parse_transcript(text):
    """Parse transcript into item-quantity pairs"""
    items = []

    # Split by lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    for line in lines:
        # Pattern: "Item name, quantity." where quantity can be a number or word
        match = re.match(r'^(.+?),\s*(.+?)\s*\.?$', line)
        if match:
            item_name = match.group(1).strip()
            qty_str = match.group(2).strip()

            # Try to parse as number first
            try:
                qty = float(qty_str)
            except ValueError:
                # Try to convert word to number
                qty = word_to_number(qty_str)
                if qty is None:
                    continue

            # Skip items with zero quantity
            if qty > 0:
                items.append({'item': item_name, 'qty': qty})

    return items

def find_product(item_name):
    """Find product in catalog with fuzzy matching"""
    normalized = normalize_product_name(item_name)

    # Check manual mappings first
    if normalized in bar_mappings:
        mapped_name = bar_mappings[normalized]
        mapped_normalized = normalize_product_name(mapped_name)
        if mapped_normalized in all_products:
            return all_products[mapped_normalized]

    # Direct match
    if normalized in all_products:
        return all_products[normalized]

    # Try partial matching with scoring
    best_match = None
    best_score = 0

    for key, product in all_products.items():
        # Calculate a simple match score
        if len(normalized) > 5:
            if normalized in key:
                score = len(normalized) / len(key)
                if score > best_score and score > 0.5:
                    best_score = score
                    best_match = product
            elif key in normalized:
                score = len(key) / len(normalized)
                if score > best_score and score > 0.5:
                    best_score = score
                    best_match = product

    return best_match

def suggest_product_matches(item_name, top_n=3):
    """Suggest possible product matches from catalog"""
    normalized = normalize_product_name(item_name)
    suggestions = []

    # Find products that contain any word from the item name
    words = normalized.split()
    for key, product in all_products.items():
        score = 0
        for word in words:
            if len(word) > 3 and word in key:
                score += len(word)

        if score > 0:
            suggestions.append((score, product['name'], key))

    # Sort by score and return top N
    suggestions.sort(reverse=True, key=lambda x: x[0])
    return [s[1] for s in suggestions[:top_n]]

# Parse transcript
parsed_items = parse_transcript(transcript)

print(f"📋 Parsed {len(parsed_items)} items from transcript")

# Match to products
matched_items = []
unmapped_items = []

for item in parsed_items:
    product = find_product(item['item'])
    if product:
        matched_items.append({
            'Category': product['category'],
            'Item Name': product['name'],
            'Unit': parse_unit(product['unit']),
            'Quantity': item['qty']
        })
    else:
        unmapped_items.append(item)

# Sort by category
category_order = ['Beer Cost', 'Liquor Cost', 'Wine Cost', 'N/A Beverage Cost', 'Grocery/Dry Goods']
matched_items.sort(key=lambda x: (category_order.index(x['Category']) if x['Category'] in category_order else 99, x['Item Name']))

# Write MarginEdge export CSV
output_csv = inventory_dir / f'{date_folder}_Bar_Inventory_MEExport.csv'
with open(output_csv, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Category', 'Item Name', 'Unit', 'Quantity'])
    writer.writeheader()
    writer.writerows(matched_items)

print(f"\n✅ Created {output_csv} with {len(matched_items)} items")

if unmapped_items:
    print(f"\n⚠️  {len(unmapped_items)} unmapped items:")

    # Create suggestions for unmapped items
    unmapped_with_suggestions = []
    for item in unmapped_items:
        suggestions = suggest_product_matches(item['item'])
        unmapped_with_suggestions.append({
            'spoken_name': item['item'],
            'quantity': item['qty'],
            'suggestions': suggestions
        })

    # Show all unmapped items with suggestions
    print("\nUnmapped items with catalog suggestions:")
    print("=" * 80)
    for i, item in enumerate(unmapped_with_suggestions, 1):
        print(f"\n{i}. \"{item['spoken_name']}\" (qty: {item['quantity']})")
        if item['suggestions']:
            print(f"   Suggestions:")
            for j, suggestion in enumerate(item['suggestions'], 1):
                print(f"      {j}. {suggestion}")
        else:
            print(f"   No suggestions found")

    # Write full unmapped items with suggestions to file
    unmapped_json = inventory_dir / f'{date_folder}_bar_unmapped_items.json'
    with open(unmapped_json, 'w') as f:
        json.dump(unmapped_with_suggestions, f, indent=2)
    print(f"\n📝 All unmapped items with suggestions saved to {unmapped_json}")
else:
    print("\n✅ All items mapped successfully!")
