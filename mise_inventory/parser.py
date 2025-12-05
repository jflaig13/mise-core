import json
import sys
import re
from unidecode import unidecode
from rapidfuzz import fuzz, process

from .catalog_loader import load_catalog

def normalize(text):
    """Lowercase, unidecode, strip."""
    return unidecode(text).strip().lower()

def parse_quantity(phrase, global_rules):
    """Extract float quantity from a phrase, e.g. 'half', '1.5', 'three-quarters'"""
    fraction_words = global_rules.get("fraction_words", {})
    phrase = normalize(phrase)
    # Check for decimal numbers
    match = re.match(r"^([0-9]+(\.[0-9]+)?)", phrase)
    if match:
        return float(match.group(1))
    # Check for 'half', 'quarter', etc.
    for word, value in fraction_words.items():
        if word in phrase:
            return value
    # Written out numbers (one, two, three, etc.)
    numbers = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    words = phrase.split()
    if words and words[0] in numbers:
        return float(numbers[words[0]])
    return None

def parse_line(line, catalog, global_rules):
    """Returns: (category, canonical_name, qty, match_score, matched_keyword) or (None, None, None, None, None)"""
    line = normalize(line)
    # Quick negative logic (don't count/zero)
    if any(nk in line for nk in global_rules.get("negative_keywords", [])):
        return None, None, None, None, None

    qty = parse_quantity(line, global_rules)
    if qty is None:
        # try for 'full', 'empty', etc.
        if "full" in line:
            qty = 1.0
        elif "empty" in line:
            qty = 0.0
        else:
            return None, None, None, None, None

    # Match to catalog
    best_score = 0
    best_item = None
    best_cat = None
    best_keyword = None
    for cat, items in catalog.items():
        if not isinstance(items, list): continue
        for obj in items:
            # Fuzzy/phonetic/keyword match
            keywords = obj.get("keywords", [])
            phonetics = obj.get("phonetic", [])
            fuzzy_weight = obj.get("fuzzy_weight", 0.85)
            # Try all keywords
            for kw in keywords + phonetics + [obj["item"].lower()]:
                score = fuzz.partial_ratio(line, normalize(kw))/100
                if score > best_score:
                    best_score = score
                    best_item = obj["item"]
                    best_cat = cat
                    best_keyword = kw
            # Early stop if perfect
            if best_score == 1.0:
                break
        if best_score == 1.0:
            break
    threshold = global_rules.get("fuzzy_match_threshold", 0.78)
    if best_score < threshold:
        return None, None, None, best_score, None
    return best_cat, best_item, qty, best_score, best_keyword

def main():
    if len(sys.argv) != 4:
        print("Usage: python -m mise_inventory.parser <transcript.txt> <inventory_catalog.json> <output.json>")
        sys.exit(1)

    transcript_path, catalog_path, output_json = sys.argv[1:4]
    catalog_data = load_catalog(catalog_path)
    global_rules = catalog_data.get("global_rules", {})

    # Read transcript and process
    results = {cat: {} for cat in catalog_data if isinstance(catalog_data[cat], list)}
    unmatched = []
    with open(transcript_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            cat, canonical, qty, score, kw = parse_line(line, catalog_data, global_rules)
            if cat and canonical and qty is not None:
                # Add up any repeated counts (aggregate)
                results[cat][canonical] = results[cat].get(canonical, 0) + qty
            else:
                unmatched.append({"line": line, "score": score})

    # Convert results to JSON format
    out_json = {}
    for cat in results:
        out_json[cat] = [{"Item": item, "Count": count} for item, count in sorted(results[cat].items())]

    with open(output_json, "w") as f:
        json.dump(out_json, f, indent=2)
    print(f"✔ Inventory JSON generated: {output_json}")

    if unmatched:
        print("\n⚠️ Unmatched lines (review these for catalog growth):")
        for entry in unmatched:
            print(f"  {entry['line']} (score: {entry['score']})")

if __name__ == "__main__":
    main()
