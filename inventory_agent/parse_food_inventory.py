#!/usr/bin/env python3
"""
Parse food inventory transcript and match to products catalog.
Follows LIM workflow specification.

Usage: python3 parse_food_inventory.py <date_folder>
Example: python3 parse_food_inventory.py 123125
"""

import re
import csv
import json
import sys
from pathlib import Path

# Get date folder from command line argument
if len(sys.argv) < 2:
    print("Usage: python3 parse_food_inventory.py <date_folder>")
    print("Example: python3 parse_food_inventory.py 123125")
    sys.exit(1)

date_folder = sys.argv[1]
inventory_dir = Path(__file__).parent / date_folder

# Read the transcript
transcript_file = inventory_dir / f'{date_folder}_inventory_food.txt'
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

# Load food item mappings
mappings_file = Path(__file__).parent / 'food_item_mappings.json'
if mappings_file.exists():
    with open(mappings_file, 'r') as f:
        food_mappings = json.load(f).get('mappings', {})
else:
    food_mappings = {}

def parse_unit(report_by_unit):
    """Extract base unit from Report By Unit field"""
    unit_lower = report_by_unit.lower()
    if 'bottle' in unit_lower:
        return 'Bottle'
    elif 'can' in unit_lower:
        return 'Can'
    elif 'keg' in unit_lower:
        return 'Keg'
    elif 'each' in unit_lower:
        return 'Each'
    elif 'pound' in unit_lower:
        return 'Pound'
    elif 'gallon' in unit_lower:
        return 'Gallon'
    elif 'case' in unit_lower:
        return 'Case'
    else:
        return report_by_unit

def parse_transcript(text):
    """Parse transcript into item-quantity pairs"""
    items = []

    # Split by commas and clean up
    parts = [p.strip() for p in text.replace('\n', ' ').split(',')]

    # Process parts in pairs (trying to identify item-quantity patterns)
    i = 0
    while i < len(parts):
        if not parts[i]:
            i += 1
            continue

        part = parts[i]

        # Check if this part is just a number (quantity)
        if re.match(r'^[\d.]+$', part):
            # This is a quantity without an item - look back for item
            if items and items[-1]['qty'] is None:
                items[-1]['qty'] = float(part)
            i += 1
            continue

        # Check if part ends with a number
        match = re.search(r'^(.+?)\s+([\d.]+)$', part)
        if match:
            item_name = match.group(1).strip()
            qty = float(match.group(2))
            items.append({'item': item_name, 'qty': qty})
            i += 1
            continue

        # Check if next part is a number
        if i + 1 < len(parts) and re.match(r'^[\d.]+$', parts[i + 1]):
            item_name = part.strip()
            qty = float(parts[i + 1])
            items.append({'item': item_name, 'qty': qty})
            i += 2
            continue

        # Item without clear quantity - mark for review
        items.append({'item': part.strip(), 'qty': None})
        i += 1

    return items

def find_product(item_name):
    """Find product in catalog with fuzzy matching"""
    normalized = normalize_product_name(item_name)

    # Check manual mappings first
    if normalized in food_mappings:
        mapped_name = food_mappings[normalized]
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
                if score > best_score and score > 0.5:  # At least 50% match
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
print(f"⚠️  Items without quantities: {sum(1 for item in parsed_items if item['qty'] is None)}")

# Match to products
matched_items = []
unmapped_items = []

for item in parsed_items:
    if item['qty'] is None or item['qty'] == 0:
        continue  # Skip items with no quantity

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
category_order = ['Beer Cost', 'Liquor Cost', 'Wine Cost', 'N/A Beverage Cost', 'Grocery and Dry Goods',
                  'Bread', 'Meat', 'Produce', 'Dairy']
matched_items.sort(key=lambda x: (category_order.index(x['Category']) if x['Category'] in category_order else 99, x['Item Name']))

# Write MarginEdge export CSV
output_csv = inventory_dir / f'{date_folder}_Food_Inventory_MEExport.csv'
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

    # Show top 20 with suggestions
    print("\nTop 20 unmapped items with catalog suggestions:")
    print("=" * 80)
    for i, item in enumerate(unmapped_with_suggestions[:20], 1):
        print(f"\n{i}. \"{item['spoken_name']}\" (qty: {item['quantity']})")
        if item['suggestions']:
            print(f"   Suggestions:")
            for j, suggestion in enumerate(item['suggestions'], 1):
                print(f"      {j}. {suggestion}")
        else:
            print(f"   No suggestions found")

    if len(unmapped_items) > 20:
        print(f"\n... and {len(unmapped_items) - 20} more")

    # Write full unmapped items with suggestions to file
    unmapped_json = inventory_dir / f'{date_folder}_food_unmapped_items.json'
    with open(unmapped_json, 'w') as f:
        json.dump(unmapped_with_suggestions, f, indent=2)
    print(f"\n📝 All unmapped items with suggestions saved to {unmapped_json}")

    # Generate template for adding mappings
    print("\n" + "=" * 80)
    print("To add mappings, update food_item_mappings.json with:")
    print("=" * 80)
    print('  "spoken_name": "Catalog Name",')
    print("\nExample:")
    if unmapped_with_suggestions and unmapped_with_suggestions[0]['suggestions']:
        example = unmapped_with_suggestions[0]
        print(f'  "{example["spoken_name"]}": "{example["suggestions"][0]}",')
else:
    print("\n✅ All items mapped successfully!")
