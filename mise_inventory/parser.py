"""Inventory transcript parser utilities.

This module handles reading a transcript of spoken inventory counts,
matching each line against the catalog, and writing out a structured
JSON summary. It can be used as a script or imported by other parts of
the Mise inventory package.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from rapidfuzz import fuzz, process
from unidecode import unidecode

from .catalog_loader import DEFAULT_CATALOG_PATH, load_catalog


def normalize(text: str) -> str:
    """Lowercase, remove accents, and strip whitespace for matching."""

    return unidecode(text).strip().lower()


def parse_quantity(phrase: str, global_rules: dict) -> float | None:
    """Extract a numeric quantity from a phrase with basic unit awareness."""

    fraction_words = global_rules.get("fraction_words", {})
    phrase_norm = normalize(phrase)

    # Patterns like "4 six packs" or "four six packs"
    pack_patterns = [
        (r"^(\d+(?:\.\d+)?)\s+(six|6)\s+pack", 6),
        (r"^(\d+(?:\.\d+)?)\s+(twelve|12)\s+pack", 12),
        (r"^(\d+(?:\.\d+)?)\s+(twenty four|24)\s+pack", 24),
    ]
    for pat, mult in pack_patterns:
        m = re.match(pat, phrase_norm)
        if m:
            return float(m.group(1)) * mult

    # Leading numeric
    m = re.match(r"^([0-9]+(\.[0-9]+)?)", phrase_norm)
    if m:
        return float(m.group(1))

    # Fractions / words
    for word, value in fraction_words.items():
        if word in phrase_norm:
            return value

    numbers = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }
    words = phrase_norm.split()
    if words and words[0] in numbers:
        return float(numbers[words[0]])

    return None


def normalize_line_with_catalog(line: str, catalog: dict, threshold: float = 0.85) -> str:
    """Normalize a line by replacing matched product mentions with canonical item names."""

    line_norm = normalize(line)
    replacements = []
    choices = []

    for cat, items in catalog.items():
        if not isinstance(items, list):
            continue
        for obj in items:
            name = obj.get("item")
            if not name:
                continue
            synonyms = [name]
            synonyms += obj.get("keywords", [])
            synonyms += obj.get("phonetic", [])
            for syn in synonyms:
                syn_norm = normalize(syn)
                if syn_norm and syn_norm not in [c[0] for c in choices]:
                    choices.append((syn_norm, name))

    # Direct substring replacements
    for syn_norm, canon in choices:
        if syn_norm and syn_norm in line_norm:
            replacements.append((syn_norm, canon))

    # Fuzzy replacements when no direct hit
    if not replacements and choices:
        vocab = [c[0] for c in choices]
        match = process.extractOne(line_norm, vocab, score_cutoff=int(threshold * 100))
        if match:
            syn_norm = match[0]
            canon = next(c for c in choices if c[0] == syn_norm)[1]
            replacements.append((syn_norm, canon))

    for syn_norm, canon in replacements:
        line_norm = line_norm.replace(syn_norm, canon.lower())

    return line_norm


def parse_line(line: str, catalog: dict, global_rules: dict):
    """Return details for a transcript line if it matches the catalog.

    Returns a tuple of:
        (category, canonical_name, qty, match_score, matched_keyword)
    or a tuple of Nones when the line does not match.
    """

    line = normalize(line)

    if any(nk in line for nk in global_rules.get("negative_keywords", [])):
        return None, None, None, None, None

    qty = parse_quantity(line, global_rules)
    if qty is None:
        if "full" in line:
            qty = 1.0
        elif "empty" in line:
            qty = 0.0
        else:
            return None, None, None, None, None

    best_score = 0
    best_item = None
    best_cat = None
    best_keyword = None
    best_obj = None

    for cat, items in catalog.items():
        if not isinstance(items, list):
            continue
        for obj in items:
            keywords = obj.get("keywords", [])
            phonetics = obj.get("phonetic", [])

            for kw in keywords + phonetics + [obj["item"].lower()]:
                score = fuzz.partial_ratio(line, normalize(kw)) / 100
                if score > best_score:
                    best_score = score
                    best_item = obj["item"]
                    best_cat = cat
                    best_keyword = kw
                    best_obj = obj

            if best_score == 1.0:
                break
        if best_score == 1.0:
            break

    threshold = global_rules.get("fuzzy_match_threshold", 0.78)
    if best_score < threshold:
        return None, None, None, best_score, None

    # If we matched and the line mentions cases, apply case size multiplier
    if best_obj:
        default_case_size = global_rules.get("default_case_size", 12)
        case_size = best_obj.get("case_size", default_case_size)

        if "case" in line or "cases" in line:
            # If canned/pack context, assume 24 unless overridden
            if any(word in line for word in ("can", "pack")):
                can_case_size = best_obj.get("case_size", global_rules.get("case_size_cans", 24))
                qty = qty * can_case_size
            else:
                qty = qty * case_size

    return best_cat, best_item, qty, best_score, best_keyword


def main() -> None:
    """CLI entry point for parsing an inventory transcript."""

    if len(sys.argv) not in (3, 4, 5):
        print(
            "Usage: python -m mise_inventory.parser <transcript.txt> [catalog.json] <output.json> [--no-normalize]"
        )
        sys.exit(1)

    transcript_path = Path(sys.argv[1])
    if len(sys.argv) >= 4 and sys.argv[2].endswith('.json'):
        catalog_path = Path(sys.argv[2])
        output_json = Path(sys.argv[3])
        normalize_flag_arg = sys.argv[4] if len(sys.argv) == 5 else None
    else:
        catalog_path = DEFAULT_CATALOG_PATH
        output_json = Path(sys.argv[2])
        normalize_flag_arg = sys.argv[3] if len(sys.argv) == 4 else None

    normalize_on = True
    if normalize_flag_arg == "--no-normalize":
        normalize_on = False

    catalog_data = load_catalog(catalog_path)
    global_rules = catalog_data.get("global_rules", {})

    results = {cat: {} for cat in catalog_data if isinstance(catalog_data[cat], list)}
    unmatched = []

    with transcript_path.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if normalize_on:
                line = normalize_line_with_catalog(line, catalog_data)
            cat, canonical, qty, score, kw = parse_line(line, catalog_data, global_rules)
            if cat and canonical and qty is not None:
                results[cat][canonical] = results[cat].get(canonical, 0) + qty
            else:
                unmatched.append({"line": line, "score": score})

    out_json = {}
    for cat in results:
        out_json[cat] = [
            {"Item": item, "Count": count} for item, count in sorted(results[cat].items())
        ]

    with output_json.open("w") as f:
        json.dump(out_json, f, indent=2)
    print(f"✔ Inventory JSON generated: {output_json}")

    if unmatched:
        print("\n⚠️ Unmatched lines (review these for catalog growth):")
        for entry in unmatched:
            print(f"  {entry['line']} (score: {entry['score']})")


if __name__ == "__main__":
    main()
