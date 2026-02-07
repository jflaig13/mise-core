#!/usr/bin/env python3
"""
Clean and aggregate 013126 inventory into final counts.
Consolidates duplicates and normalizes product names.
"""

import json
import csv
from pathlib import Path

# Load the raw parsed inventory
input_path = Path(__file__).parent / "013126_inventory_final.json"
with open(input_path, 'r') as f:
    data = json.load(f)

# Product name mappings to normalize duplicates
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
    "kegs": None,  # Skip generic "kegs"

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

    # Liquor
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
    "crop organic cucumber vodka": "Crop Cucumber Vodka",
    "crop organic meyer lemon flavored vodka": "Crop Meyer Lemon Vodka",
    "farmer's gin": "Farmer's Organic Gin",
    "meyer's dark rum": "Myers Dark Rum",
    "meyer's original dark rum": "Myers Dark Rum",
    "meyer's original": "Myers Dark Rum",
    "parrot bay coconut rum": "Parrot Bay Coconut Rum",
    "parrot bay coconut": "Parrot Bay Coconut Rum",
    "parrot bay white rum": "Parrot Bay White Rum",
    "pueblo viejo tequila": "Pueblo Viejo Tequila",
    "pueblo viejo": "Pueblo Viejo Tequila",
    "casamigos blanco": "Casamigos Blanco Tequila",
    "milagro reposado": "Milagro Reposado Tequila",
    "milagro silver": "Milagro Silver Tequila",
    "milagros silver": "Milagro Silver Tequila",
    "yave coconut tequila": "Yave Coconut Tequila",
    "yave": "Yave Coconut Tequila",
    "yahweh jalapeno tequila": "Yave Jalapeno Tequila",
    "yahweh coconut": "Yave Coconut Tequila",
    "siete mysterios mezcal": "Siete Misterios Mezcal",
    "siete mestadios mezcal": "Siete Misterios Mezcal",
    "siete mysterios": "Siete Misterios Mezcal",
    "campesino silver rum": "Campesino Silver Rum",
    "campesino": "Campesino Silver Rum",
    "campesino aged rum": "Campesino Aged Rum",
    "caravella limoncello": "Caravella Limoncello",
    "caravella limoncillo": "Caravella Limoncello",
    "bowls elderflower liqueur": "Bols Elderflower Liqueur",
    "bowls elderflower liqueur 750 milliliters": "Bols Elderflower Liqueur 750ml",
    "boll's elderflower liqueur": "Bols Elderflower Liqueur",
    "mr. boston peach schnapps": "Mr. Boston Peach Schnapps",
    "peach schnapps": "Mr. Boston Peach Schnapps",
    "peach": "Mr. Boston Peach Schnapps",
    "mr. boston blue curacao": "Mr. Boston Blue Curacao",
    "mr. boston blue curaçao": "Mr. Boston Blue Curacao",
    "mr. boston's blue curacao": "Mr. Boston Blue Curacao",
    "grand gala orange liqueur": "Grand Gala Orange Liqueur",
    "rumple mints": "Rumple Minze",
    "tia maria cold brew coffee liqueur": "Tia Maria Coffee Liqueur",
    "chambord": "Chambord",
    "nocello": "Nocello",
    "blanton's": "Blanton's Bourbon",
    "eagle rare": "Eagle Rare Bourbon",
    "redwood empire": "Redwood Empire Whiskey",
    "colonel e.h. taylor": "E.H. Taylor Bourbon",
    "michter's": "Michter's Rye",
    "tullamore dew": "Tullamore Dew",
    "papa's pilar": "Papa's Pilar Rum",
    "tahin": "Tahini (check if bar item)",
    "aradura": "Herradura Silver Tequila",
    "romana amaro": "Romana Sambuca",

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

    # Skip these incomplete entries
    "bottle": None,
    "bottles": None,
    "mr": None,
    "liter": None,
    "liter bottle": None,
    "liter bottle of michter's": "Michter's Rye 1L",
    "milliliters": None,
    "more bottle of": None,
}

# Aggregate by normalized name
aggregated = {}

for item in data["items"]:
    raw_name = item["product"].lower()
    qty = item["quantity"]
    unit = item["unit"]

    # Try to find mapping
    normalized = NAME_MAPPINGS.get(raw_name)

    if normalized is None:
        # Skip items marked as None
        if raw_name in NAME_MAPPINGS:
            continue
        # Use original name if no mapping
        normalized = item["product"]

    if normalized not in aggregated:
        aggregated[normalized] = {"qty": 0, "unit": unit}

    aggregated[normalized]["qty"] += qty

# Print clean inventory
print("=" * 80)
print("013126 FINAL INVENTORY - January 31, 2026")
print("=" * 80)

categories = {
    "BEER (Cans/Bottles)": [],
    "BEER (Kegs)": [],
    "WINE": [],
    "LIQUOR": [],
    "MIXERS & N/A": []
}

for name, data in sorted(aggregated.items()):
    qty = data["qty"]
    unit = data["unit"]
    name_lower = name.lower()

    if "keg" in name_lower:
        categories["BEER (Kegs)"].append((name, qty, unit))
    elif any(x in name_lower for x in ['can', 'coors', 'miller', 'michelob', 'pacifico', 'yuengling', 'athletic', 'high noon', 'high rise', 'mom water', 'red bull', 'grayton']):
        categories["BEER (Cans/Bottles)"].append((name, qty, unit))
    elif any(x in name_lower for x in ['chardonnay', 'pinot', 'merlot', 'rose', 'cabernet', 'sauvignon', 'brut', 'cava', 'gearbox', 'squealing', 'scarpetta', 'windstorm', 'carter', 'charles', 'marca', 'shaker']):
        categories["WINE"].append((name, qty, unit))
    elif any(x in name_lower for x in ['mix', 'puree', 'syrup', 'grenadine', 'coconut', 'ginger']):
        categories["MIXERS & N/A"].append((name, qty, unit))
    else:
        categories["LIQUOR"].append((name, qty, unit))

for cat_name, items in categories.items():
    if not items:
        continue
    print(f"\n{cat_name}")
    print("-" * 60)
    for name, qty, unit in sorted(items):
        qty_str = f"{qty:.2f}" if qty != int(qty) else str(int(qty))
        print(f"  {qty_str:>8} {unit:>6}  {name}")

# Save to CSV for MarginEdge
output_csv = Path(__file__).parent / "013126_Inventory_MEExport.csv"
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Category", "Item Name", "Unit", "Quantity"])
    for cat_name, items in categories.items():
        for name, qty, unit in sorted(items):
            writer.writerow([cat_name, name, unit, qty])

print(f"\n{'=' * 80}")
print(f"MarginEdge Export saved to: {output_csv}")
print(f"{'=' * 80}")

# Summary stats
total_items = sum(len(items) for items in categories.values())
print(f"\nSummary: {total_items} unique products across {len(categories)} categories")
