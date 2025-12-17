#!/usr/bin/env python3
"""
Rebuild inventory_catalog.json from products CSVs with proper filtering.

Usage:
    # Generate catalog (bar only + Tajin)
    python scripts/rebuild_catalog.py

    # Preview without writing
    python scripts/rebuild_catalog.py --dry-run

    # Write to different location
    python scripts/rebuild_catalog.py --output data/inventory_catalog_test.json

    # Include all food products (for December onwards)
    python scripts/rebuild_catalog.py --include-all-food

Purpose:
    - Filter products where "On Inventory" = "Yes"
    - Exclude food products except Tajin (for November)
    - Generate clean catalog for LIM parser
"""

import argparse
import csv
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime


PRODUCTS_DIR = Path(__file__).resolve().parent.parent / "mise_inventory" / "products"
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "data" / "inventory_catalog.json"

BAR_PRODUCT_FILES = [
    "products_beer.csv",
    "products_liquor.csv",
    "products_wine.csv",
    "products_nabev.csv",
]

FOOD_PRODUCT_FILE = "products_food.csv"
FOOD_WHITELIST = ["Seasoning, Tajin"]  # Only these food items for now


def generate_sku(name: str) -> str:
    """Generate SKU from product name.

    Example: "Coors Light 12oz Can" -> "coors-light-12oz-can"
    """
    # Lowercase and replace non-alphanumeric with hyphens
    sku = re.sub(r"[^a-z0-9]+", "-", name.lower())
    # Strip leading/trailing hyphens and collapse multiple hyphens
    sku = re.sub(r"-+", "-", sku).strip("-")
    return sku


def extract_keywords(name: str) -> List[str]:
    """Extract keywords from product name for fuzzy matching.

    Example: "Coors Light 12oz Can" -> ["coors", "light", "12oz", "can"]
    """
    # Split on spaces, commas, slashes, parentheses
    tokens = re.split(r"[\s,/()]+", name.lower())
    # Remove empty strings and duplicates while preserving order
    seen: Set[str] = set()
    keywords = []
    for token in tokens:
        token = token.strip()
        if token and token not in seen:
            seen.add(token)
            keywords.append(token)
    return keywords


def load_products_csv(csv_path: Path, filter_inventory: bool = True) -> List[Dict]:
    """Load products from CSV, optionally filtering by 'On Inventory' column.

    Args:
        csv_path: Path to products CSV file
        filter_inventory: If True, only include rows where "On Inventory" = "Yes"

    Returns:
        List of row dictionaries
    """
    if not csv_path.exists():
        print(f"⚠️  CSV not found: {csv_path}")
        return []

    products = []
    with csv_path.open("r", encoding="utf-8-sig") as f:  # utf-8-sig handles BOM
        reader = csv.DictReader(f)
        for row in reader:
            # Filter by "On Inventory" column if requested
            if filter_inventory:
                on_inventory = row.get("On Inventory", "").strip()
                if on_inventory != "Yes":
                    continue

            # Only include if name is present
            name = row.get("Name", "").strip()
            if name:
                products.append(row)

    return products


def convert_to_catalog_entry(row: Dict, source_file: str) -> Dict:
    """Convert CSV row to catalog entry format.

    Args:
        row: Dictionary from csv.DictReader
        source_file: Name of source CSV file (e.g., "products_beer.csv")

    Returns:
        Catalog entry dictionary
    """
    name = row.get("Name", "").strip()
    sku = generate_sku(name)
    keywords = extract_keywords(name)

    entry = {
        "name": name,
        "category": row.get("Category", "").strip(),
        "sku": sku,
        "report_by_unit": row.get("Report By Unit", "").strip(),
        "latest_price": row.get("Latest Price", "").strip(),
        "accounting_code": row.get("Accounting Code", "").strip(),
        "tax_exempt": row.get("Tax Exempt", "").strip(),
        "source_file": source_file,
    }

    # Only add keywords if non-empty
    if keywords:
        entry["keywords"] = keywords

    return entry


def _normalize_category_key(category: str) -> str:
    """Normalize category name to lowercase key format.

    Example: "Beer Cost" -> "beer_cost"
    """
    return re.sub(r"[^a-z0-9]+", "_", category.lower()).strip("_")


def build_catalog(
    products_dir: Path,
    include_all_food: bool = False,
    food_whitelist: List[str] = None
) -> Dict[str, List[Dict]]:
    """Build catalog from all products CSVs with proper filtering.

    Args:
        products_dir: Directory containing products_*.csv files
        include_all_food: If True, include all food products (for December onwards)
        food_whitelist: List of food product names to include (default: Tajin only)

    Returns:
        Dictionary mapping category keys to lists of product entries
    """
    if food_whitelist is None:
        food_whitelist = FOOD_WHITELIST

    catalog: Dict[str, List[Dict]] = {}
    stats = {}

    # Load bar products (beer, liquor, wine, nabev)
    for csv_file in BAR_PRODUCT_FILES:
        csv_path = products_dir / csv_file
        products = load_products_csv(csv_path, filter_inventory=True)

        for row in products:
            entry = convert_to_catalog_entry(row, csv_file)
            category_key = _normalize_category_key(entry["category"])
            catalog.setdefault(category_key, [])
            catalog[category_key].append(entry)

        stats[csv_file] = len(products)
        print(f"✅ {csv_file}: {len(products)} products (On Inventory = Yes)")

    # Load food products (with whitelist or all)
    food_csv_path = products_dir / FOOD_PRODUCT_FILE
    if include_all_food:
        food_products = load_products_csv(food_csv_path, filter_inventory=True)
        print(f"✅ {FOOD_PRODUCT_FILE}: {len(food_products)} products (On Inventory = Yes, ALL FOOD)")
    else:
        # Load all food products but filter by whitelist
        all_food = load_products_csv(food_csv_path, filter_inventory=True)
        food_products = [row for row in all_food if row.get("Name", "").strip() in food_whitelist]
        print(f"✅ {FOOD_PRODUCT_FILE}: {len(food_products)} products (whitelist: {', '.join(food_whitelist)})")

    for row in food_products:
        entry = convert_to_catalog_entry(row, FOOD_PRODUCT_FILE)
        category_key = _normalize_category_key(entry["category"])
        catalog.setdefault(category_key, [])
        catalog[category_key].append(entry)

    stats[FOOD_PRODUCT_FILE] = len(food_products)

    # Print summary
    total = sum(stats.values())
    print(f"\n📊 Total products in catalog: {total}")
    print(f"📂 Categories: {', '.join(sorted(catalog.keys()))}")

    return catalog


def main():
    parser = argparse.ArgumentParser(
        description="Rebuild inventory_catalog.json from products CSVs"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output path for catalog JSON (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing to disk"
    )
    parser.add_argument(
        "--include-all-food",
        action="store_true",
        help="Include all food products (for December onwards)"
    )
    parser.add_argument(
        "--products-dir",
        type=Path,
        default=PRODUCTS_DIR,
        help=f"Directory containing products_*.csv files (default: {PRODUCTS_DIR})"
    )

    args = parser.parse_args()

    print("🔧 Rebuilding inventory catalog...")
    print(f"📁 Products directory: {args.products_dir}")
    print(f"📄 Output: {args.output}")

    if args.dry_run:
        print("⚠️  DRY RUN MODE - No files will be modified")

    print()

    # Build catalog
    catalog = build_catalog(
        args.products_dir,
        include_all_food=args.include_all_food
    )

    if args.dry_run:
        print("\n✅ Dry run complete. No files modified.")
        print(f"📊 Would have written {len(catalog)} products to {args.output}")

        # Show first 3 entries as preview
        if catalog:
            print("\n📋 Preview (first 3 entries):")
            for entry in catalog[:3]:
                print(f"  - {entry['name']} ({entry['category']}) [{entry['source_file']}]")

        return

    # Backup existing catalog if it exists
    if args.output.exists():
        backup_path = args.output.with_suffix(f".json.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy(args.output, backup_path)
        print(f"\n💾 Backed up existing catalog to: {backup_path}")

    # Write catalog
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")

    print(f"\n✅ Catalog written to: {args.output}")
    print(f"📊 Total products: {len(catalog)}")


if __name__ == "__main__":
    main()
