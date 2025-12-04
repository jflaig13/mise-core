import json
import sys
import pandas as pd
from pathlib import Path

def make_excel(json_path):
    json_path = Path(json_path)
    with open(json_path, "r") as f:
        data = json.load(f)

    base = json_path.stem.replace("inventory_", "")
    output_name = f"Papa_Surf_Inventory_{base}.xlsx"

    sheet_titles = {
        "grocery_drygoods": "Grocery & Dry Goods",
        "beer_cost": "Beer Cost",
        "wine_cost": "Wine Cost",
        "liquor_cost": "Liquor Cost",
        "na_bev_cost": "N/A Beverage Cost"
    }

    with pd.ExcelWriter(output_name, engine="openpyxl") as writer:
        for key, rows in data.items():
            sheet_name = sheet_titles[key]
            df = pd.DataFrame(rows)
            if len(df) > 0:
                df = df.sort_values(by="Item")
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"\n✔ Inventory Excel created: {output_name}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_inventory_file.py <json_file>")
        sys.exit(1)
    make_excel(sys.argv[1])