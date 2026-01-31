#!/usr/bin/env python3
"""
Rebuild inventory_catalog.json from products/*.csv files.

Reads all CSV files in inventory_agent/products/ and generates a complete
catalog with all Papa Surf products for the inventory parser.
"""

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Any


def normalize_category(category: str) -> str:
    """Convert 'Beer Cost' → 'beer_cost', etc."""
    return category.lower().replace(" ", "_").replace("&", "and").replace(",", "")


def generate_sku(name: str) -> str:
    """Generate SKU from product name."""
    # Remove special characters, convert to lowercase, replace spaces with hyphens
    sku = re.sub(r'[^\w\s-]', '', name.lower())
    sku = re.sub(r'[\s_]+', '-', sku)
    return sku.strip('-')


def generate_keywords(name: str) -> List[str]:
    """Extract keywords from product name for fuzzy matching."""
    # Common words to filter out (too generic for matching)
    stop_words = {
        'of', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
        'for', 'with', 'from', 'by', 'as', 'is', 'was', 'are', 'be', 'been'
    }

    # Split on spaces, commas, slashes, parentheses
    parts = re.split(r'[\s,/()]+', name)

    keywords = []
    for part in parts:
        # Remove special characters but keep alphanumeric
        cleaned = re.sub(r'[^\w]', '', part.lower())
        if cleaned and len(cleaned) > 1 and cleaned not in stop_words:  # Skip single chars and stop words
            keywords.append(cleaned)

    return keywords


def parse_case_size(report_by_unit: str) -> int:
    """Extract case size from Report By Unit field."""
    # Look for patterns like "12 Cans", "24 Bottles", "Case (24)"
    match = re.search(r'(\d+)', report_by_unit)
    if match:
        size = int(match.group(1))
        # Common case sizes
        if size in [6, 12, 24, 30]:
            return size

    # Defaults based on unit type
    if 'can' in report_by_unit.lower():
        return 24
    elif 'bottle' in report_by_unit.lower():
        return 12

    return None


def read_csv_products(csv_path: Path) -> List[Dict[str, Any]]:
    """Read products from a CSV file."""
    products = []

    with csv_path.open('r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if not name:
                continue

            category = row.get('Category', '').strip()
            report_by_unit = row.get('Report By Unit', '').strip()
            latest_price = row.get('Latest Price', '').strip()

            product = {
                'item': name,  # Parser expects 'item', not 'name'
                'category': category,
                'sku': generate_sku(name),
                'report_by_unit': report_by_unit,
                'latest_price': latest_price,
                'accounting_code': row.get('Accounting Code', '').strip(),
                'tax_exempt': row.get('Tax Exempt', 'No').strip(),
                'source_file': csv_path.name,
                'keywords': generate_keywords(name)
            }

            # Add case size if we can determine it
            case_size = parse_case_size(report_by_unit)
            if case_size:
                product['case_size'] = case_size

            products.append(product)

    return products


def enhance_keywords_with_mappings(catalog: Dict[str, Any], manual_mappings: Dict[str, str]) -> None:
    """Add manual mapping phrases as additional keywords."""
    # Reverse the mappings: canonical_name -> [spoken_names]
    reverse_map = {}
    for spoken, canonical in manual_mappings.items():
        reverse_map.setdefault(canonical, []).append(spoken)

    # Add spoken names as keywords
    for category_key, items in catalog.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            canonical_name = item.get('item', '')
            if canonical_name in reverse_map:
                # Add spoken name variants as keywords
                for spoken_name in reverse_map[canonical_name]:
                    # Split spoken name into words and add them
                    spoken_keywords = generate_keywords(spoken_name)
                    existing_keywords = item.get('keywords', [])
                    for kw in spoken_keywords:
                        if kw not in existing_keywords:
                            existing_keywords.append(kw)
                    item['keywords'] = existing_keywords


def read_csv_products(csv_path: Path, manual_mappings: Dict[str, str]) -> List[Dict[str, Any]]:
    """Read products from a CSV file and enhance with manual mappings."""
    products = []

    with csv_path.open('r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if not name:
                continue

            category = row.get('Category', '').strip()
            report_by_unit = row.get('Report By Unit', '').strip()
            latest_price = row.get('Latest Price', '').strip()

            product = {
                'item': name,  # Parser expects 'item', not 'name'
                'category': category,
                'sku': generate_sku(name),
                'report_by_unit': report_by_unit,
                'latest_price': latest_price,
                'accounting_code': row.get('Accounting Code', '').strip(),
                'tax_exempt': row.get('Tax Exempt', 'No').strip(),
                'source_file': csv_path.name,
                'keywords': generate_keywords(name)
            }

            # Add case size if we can determine it
            case_size = parse_case_size(report_by_unit)
            if case_size:
                product['case_size'] = case_size

            products.append(product)

    return products


def load_manual_mappings(project_root: Path) -> Dict[str, str]:
    """Load manual item mappings from JSON files."""
    mappings = {}

    # Load bar mappings
    bar_file = project_root / 'inventory_agent' / 'bar_item_mappings.json'
    if bar_file.exists():
        with bar_file.open('r') as f:
            data = json.load(f)
            mappings.update(data.get('mappings', {}))

    # Load food mappings
    food_file = project_root / 'inventory_agent' / 'food_item_mappings.json'
    if food_file.exists():
        with food_file.open('r') as f:
            data = json.load(f)
            # Merge, bar takes precedence
            food_mappings = data.get('mappings', {})
            for key, value in food_mappings.items():
                if key not in mappings:
                    mappings[key] = value

    return mappings


def build_catalog(products_dir: Path, manual_mappings: Dict[str, str]) -> Dict[str, Any]:
    """Build complete catalog from all CSV files."""

    # Start with global rules (preserve from existing catalog if available)
    catalog = {
        'global_rules': {
            'fuzzy_match_threshold': 0.65,
            'fraction_words': {
                'half': 0.5,
                'quarter': 0.25,
                'three quarters': 0.75,
                'full': 1.0
            },
            'negative_keywords': []
        }
    }

    # Category mapping
    category_keys = {
        'Beer Cost': 'beer_cost',
        'Wine Cost': 'wine_cost',
        'Liquor Cost': 'liquor_cost',
        'N/A Beverage Cost': 'n_a_beverage_cost',
        'Grocery and Dry Goods': 'grocery_and_dry_goods',
        'Bread': 'grocery_and_dry_goods',
        'Produce': 'grocery_and_dry_goods',
        'Meat': 'grocery_and_dry_goods',
        'Dairy': 'grocery_and_dry_goods',
        'Condiments': 'grocery_and_dry_goods',
        'Oil': 'grocery_and_dry_goods',
        'Spices': 'grocery_and_dry_goods'
    }

    # Initialize category lists
    for key in category_keys.values():
        if key not in catalog:
            catalog[key] = []

    # Read all CSV files
    csv_files = list(products_dir.glob('products_*.csv'))

    for csv_file in sorted(csv_files):
        print(f"Reading {csv_file.name}...")
        products = read_csv_products(csv_file, manual_mappings)

        for product in products:
            category = product['category']
            catalog_key = category_keys.get(category, 'grocery_and_dry_goods')

            # Check for duplicates
            existing = next(
                (p for p in catalog[catalog_key] if p['item'] == product['item']),
                None
            )

            if not existing:
                catalog[catalog_key].append(product)

    return catalog


def main():
    """Main entry point."""
    # Paths
    project_root = Path(__file__).resolve().parent.parent
    products_dir = project_root / 'inventory_agent' / 'products'
    output_path = project_root / 'data' / 'inventory_catalog.json'

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load manual mappings
    print(f"\n📖 Loading manual item mappings...\n")
    manual_mappings = load_manual_mappings(project_root)
    print(f"  Loaded {len(manual_mappings)} manual mappings\n")

    # Build catalog
    print(f"🔨 Building inventory catalog from {products_dir}...\n")
    catalog = build_catalog(products_dir, manual_mappings)

    # Enhance with manual mappings
    print(f"🔍 Enhancing keywords with manual mappings...\n")
    enhance_keywords_with_mappings(catalog, manual_mappings)

    # Count products
    total = 0
    for key, items in catalog.items():
        if isinstance(items, list):
            count = len(items)
            total += count
            print(f"  {key}: {count} items")

    print(f"\n✅ Total products: {total}\n")

    # Write catalog
    with output_path.open('w') as f:
        json.dump(catalog, f, indent=2)

    print(f"✅ Catalog written to: {output_path}\n")

    # Verify
    with output_path.open('r') as f:
        verification = json.load(f)

    verify_count = sum(len(v) for v in verification.values() if isinstance(v, list))
    print(f"✅ Verification: {verify_count} products in catalog\n")


if __name__ == '__main__':
    main()
