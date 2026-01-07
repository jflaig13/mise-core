#!/usr/bin/env python3
"""
Process Papa Surf inventory JSON to MarginEdge export CSV.
Follows LIM workflow specification from workflow_specs/LIM/LIM_Workflow_Master.txt
"""

import json
import csv
import os
from pathlib import Path

# Load the inventory count
with open('papa_surf_inventory_2026_01_02.json', 'r') as f:
    inventory_data = json.load(f)

# Load all product catalogs
products_dir = Path(__file__).parent.parent / 'products'

def normalize_product_name(name):
    """Normalize product name for dictionary key"""
    name = name.lower().strip()
    # Remove accents and umlauts
    name = name.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    name = name.replace('ä', 'a').replace('ë', 'e').replace('ï', 'i').replace('ö', 'o').replace('ü', 'u')
    name = name.replace('ñ', 'n').replace('ç', 'c')
    # Standardize punctuation
    name = name.replace(',', '')
    name = name.replace("'", "")  # Straight apostrophe
    name = name.replace('\u2019', '')  # Curly apostrophe
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
                # Normalize the key for matching
                key = normalize_product_name(name)
                products[key] = {
                    'name': name,
                    'category': row['Category'],
                    'unit': row['Report By Unit']
                }
    return products

# Load all product catalogs
# Use the updated comprehensive catalog from 123125
all_products = load_products('products_123125.csv')

# Manually add Red Bull even though it's marked "On Inventory = No" in catalog
# User wants both Red Bull and Red Bull Sugar Free counted under this SKU
all_products[normalize_product_name('Red Bull Assorted 8.4oz Can')] = {
    'name': 'Red Bull Assorted 8.4oz Can',
    'category': 'N/A Beverage Cost',
    'unit': 'Can'
}

# Create normalization mapping
def normalize_name(name):
    """Normalize item name for matching (same as normalize_product_name for consistency)"""
    return normalize_product_name(name)

# Manual mapping for products with different names in count vs catalog
MANUAL_MAPPINGS = {
    'blantons single barrel': 'blantons single barrel bourbon',
    'blue curacao': 'blue curacao',
    'colonel e.h. taylor': 'eh taylor small batch bourbon',
    'crop cucumber vodka': 'crop cucumber vodka',
    'crop lemon vodka': 'crop harvest meyer lemon vodka',
    'farmers gin': 'farmers gin',
    'jagermeister': 'jagermeister',
    'myerss dark rum': 'myerss dark rum',
    'wheatleys vodka': 'wheatley vodka',
    'faretti espresso coffee liqueur': 'faretti espresso liqueur',
    'grand gala orange liqueur': 'gran gala orange liqueur',
    'herradura anejo': 'herradura anejo tequila',
    'herradura legend anejo': 'herradura legend anejo tequila',
    'jagermeister': 'jagermeister',
    'michters single barrel straight rye': 'michters us1 single barrel straight rye whiskey',
    'mr. boston blue curacao': 'blue curacao',
    'mr. boston peach schnapps': 'mr boston peach schnapps',
    'papas pilar rum': 'papas pilar 24yr spanish sherry cask solera dark rum',
    'pueblo viejo tequila': 'pueblo viejo blanco tequila',
    'redwood empire whiskey': 'redwood empire lost monarch whiskey',
    'yave jalapeno tequila': 'yave jalapeño tequila',
    'bar mix margarita': 'bar mix margarita',
    'bar mix mojito': 'bar mix mojito',
    'bar mix watermelon': 'bar mix watermelon',
    'bloody mary mix': 'bar mix bloody mary',
    'blue agave syrup': 'agave nectar',
    'jalapeno simple syrup': 'syrup jalapeno',
    'strawberry puree': 'puree strawberry',
    'bar mix margarita strawberry 64oz': 'bar mix margarita strawberry 64oz',
    'tajin seasoning': 'seasoning tajin',
    '30a provence rose': '30a provence rose',
    'carter cellars lot rose': 'carters lot rose of pinot noir 2020',
    'gearbox pinot noir': 'gearbox california pinot noir',
    'marques de caceres brut': 'marques de caceres nv brut cava',
    'windstorm cabernet sauvignon': 'windstorm red hills cabernet sauvignon',
    'windstorm chardonnay': 'windstorm central coast chardonnay',
    'athletic upside dawn': 'athletic upside dawn golden 12oz can',
    'athletic upside dawn na': 'athletic upside dawn golden 12oz can',
    'corona extra': 'corona 12oz can',
    'grayton 30a ipa': 'grayton ipa 12oz can',
    'grayton 30a rose gose': 'grayton beach 30a rose 12oz can',
    'red bull': 'red bull assorted 8.4oz can',
    'red bull sugar free': 'red bull assorted 8.4oz can',  # Both counted under same SKU
    'yave jalapeno tequila': 'yave coconut tequila',  # Map to Yave Coconut if no jalapeño in catalog
    '30a beach blonde ale': 'grayton 30a beach blonde keg (1/2bbl)',
    'perfect plain citrus spin hazy ipa': 'urban south holy roller hazy ipa keg (1/6bbl)',
    'perfect plain yacht side lime lager': 'perfect plain yachtside keg (1/6bbl)',
    'urban south paradise park american lager': 'urban south paradise park keg (1/6bbl)',
}

def find_product(item_name):
    """Find product in catalog with fuzzy matching"""
    normalized = normalize_name(item_name)

    # Check manual mappings first
    if normalized in MANUAL_MAPPINGS:
        mapped = MANUAL_MAPPINGS[normalized]
        if mapped in all_products:
            return all_products[mapped]

    # Direct match
    if normalized in all_products:
        return all_products[normalized]

    # Try with common variations
    variations = [
        normalized,
        normalized.replace("'s", ""),
        normalized.replace("'", ""),
        normalized.replace(" single barrel", ""),
        normalized.replace("blanco original", "blanco"),
        normalized.replace(" single barrel straight rye", ""),
    ]

    for var in variations:
        if var in all_products:
            return all_products[var]

    # Partial match (only if reasonably specific)
    for var in variations:
        for key, product in all_products.items():
            # Check if the variation is in the key
            if len(var) > 5 and var in key:
                return product

    return None

# Parse units from Report By Unit field
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
    elif 'gallon' in unit_lower:
        return 'Gallon'
    else:
        return report_by_unit

# Build MarginEdge export rows
me_rows = []
unmapped_items = []

# Process liquor
for item in inventory_data['inventory']['liquor']:
    product = find_product(item['item'])
    if product:
        me_rows.append({
            'Category': product['category'],
            'Item Name': product['name'],
            'Unit': parse_unit(product['unit']),
            'Quantity': item['qty']
        })
    else:
        unmapped_items.append({
            'raw_item': item['item'],
            'qty': item['qty'],
            'source_category': 'liquor'
        })

# Process mixers/syrups (map to Liquor Cost or N/A Beverage Cost)
for item in inventory_data['inventory']['mixers_syrups']:
    product = find_product(item['item'])
    if product:
        me_rows.append({
            'Category': product['category'],
            'Item Name': product['name'],
            'Unit': parse_unit(product['unit']),
            'Quantity': item['qty']
        })
    else:
        unmapped_items.append({
            'raw_item': item['item'],
            'qty': item['qty'],
            'source_category': 'mixers_syrups'
        })

# Process wine
for item in inventory_data['inventory']['wine']:
    product = find_product(item['item'])
    if product:
        me_rows.append({
            'Category': product['category'],
            'Item Name': product['name'],
            'Unit': parse_unit(product['unit']),
            'Quantity': item['qty']
        })
    else:
        unmapped_items.append({
            'raw_item': item['item'],
            'qty': item['qty'],
            'source_category': 'wine'
        })

# Process beer
for item in inventory_data['inventory']['beer']:
    product = find_product(item['item'])
    if product:
        me_rows.append({
            'Category': product['category'],
            'Item Name': product['name'],
            'Unit': parse_unit(product['unit']),
            'Quantity': item['qty']
        })
    else:
        unmapped_items.append({
            'raw_item': item['item'],
            'qty': item['qty'],
            'source_category': 'beer'
        })

# Process seltzers/RTD
for item in inventory_data['inventory']['seltzers_rtd']:
    product = find_product(item['item'])
    if product:
        me_rows.append({
            'Category': product['category'],
            'Item Name': product['name'],
            'Unit': parse_unit(product['unit']),
            'Quantity': item['qty']
        })
    else:
        unmapped_items.append({
            'raw_item': item['item'],
            'qty': item['qty'],
            'source_category': 'seltzers_rtd'
        })

# Process kegs
for item in inventory_data['inventory']['kegs']:
    product = find_product(item['item'])
    if product:
        me_rows.append({
            'Category': product['category'],
            'Item Name': product['name'],
            'Unit': parse_unit(product['unit']),
            'Quantity': item['qty']
        })
    else:
        unmapped_items.append({
            'raw_item': item['item'],
            'qty': item['qty'],
            'source_category': 'kegs'
        })

# Sort by category then item name
category_order = ['Beer Cost', 'Liquor Cost', 'Wine Cost', 'N/A Beverage Cost', 'Grocery/Dry Goods']
me_rows.sort(key=lambda x: (category_order.index(x['Category']) if x['Category'] in category_order else 99, x['Item Name']))

# Write MarginEdge export CSV
with open('123125_Inventory_MEExport.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Category', 'Item Name', 'Unit', 'Quantity'])
    writer.writeheader()
    writer.writerows(me_rows)

print(f"✅ Created 123125_Inventory_MEExport.csv with {len(me_rows)} items")

if unmapped_items:
    print(f"\n⚠️  {len(unmapped_items)} unmapped items:")
    for item in unmapped_items:
        print(f"  - {item['raw_item']} ({item['qty']}) from {item['source_category']}")

    # Write unmapped items to file for review
    with open('123125_unmapped_items.json', 'w') as f:
        json.dump(unmapped_items, f, indent=2)
    print("\n📝 Unmapped items saved to 123125_unmapped_items.json")
else:
    print("\n✅ All items mapped successfully!")
