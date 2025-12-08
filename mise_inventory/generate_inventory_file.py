"""Utility to convert parsed inventory JSON into an Excel workbook."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


def sanitize_sheet_name(name: str) -> str:
    """Make a sheet name safe for Excel/openpyxl."""
    invalid = set(r'[]:*?/\\')
    cleaned = "".join(ch if ch not in invalid else "-" for ch in name)
    cleaned = cleaned.strip()
    if not cleaned:
        cleaned = "Sheet"
    return cleaned[:31]


def make_excel(json_path: str | Path) -> Path:
    """Create an Excel file from the structured inventory JSON."""

    json_path = Path(json_path)
    with json_path.open("r") as f:
        data = json.load(f)

    # Output file name: <stem>_final.xlsx (e.g., 113025_inventory_output -> 113025_inventory_final.xlsx)
    stem = json_path.stem
    if stem.endswith("_output"):
        stem = stem[: -len("_output")]
    output_name = (Path(__file__).resolve().parent / f"{stem}_final.xlsx")

    sheet_titles = {
        "grocery_drygoods": "Grocery & Dry Goods",
        "beer_cost": "Beer Cost",
        "wine_cost": "Wine Cost",
        "liquor_cost": "Liquor Cost",
        "na_bev_cost": "N/A Beverage Cost",
    }

    with pd.ExcelWriter(output_name, engine="openpyxl") as writer:
        for key, rows in data.items():
            if key == "breakdown":
                continue
            sheet_name = sheet_titles.get(key, key)
            sheet_name = sanitize_sheet_name(sheet_name)
            df = pd.DataFrame(rows)
            if len(df) > 0:
                df = df.sort_values(by="Item")
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Optional breakdown sheet
        if "breakdown" in data:
            records = []
            for cat, items in data["breakdown"].items():
                for item, entries in items.items():
                    for entry in entries:
                        records.append(
                            {
                                "Category": sheet_titles.get(cat, cat),
                                "Item": item,
                                "Quantity": entry.get("qty"),
                                "Source": entry.get("line"),
                            }
                        )
            if records:
                df_break = pd.DataFrame(records)
                df_break = df_break.sort_values(by=["Category", "Item"])
                df_break.to_excel(writer, sheet_name="Breakdown", index=False)

    print(f"\n✔ Inventory Excel created: {output_name}\n")
    return output_name


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m mise_inventory.generate_inventory_file <json_file>")
        sys.exit(1)
    make_excel(sys.argv[1])
