"""
Interactive helper to grow the inventory catalog from unmatched transcript lines.

Usage:
    .venv/bin/python -m scripts.grow_catalog \
      --catalog data/inventory_catalog.json \
      --transcript data/Inventory/113025_Inventory.txt \
      --output data/inventory_catalog.json

Workflow:
 1) Run the parser to collect unmatched lines (or pass a --unmatched file).
 2) For each line, show top fuzzy matches from the catalog and let you:
       - pick an existing item
       - type a new item name (with category prompt)
       - skip
 3) Writes updated catalog JSON to --output (defaults to overwrite the input catalog).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

from rapidfuzz import process
from inventory_agent import parser as inv_parser
from inventory_agent.catalog_loader import load_catalog


def collect_unmatched(transcript_path: Path, catalog: Dict) -> List[str]:
    """Run the parser and return unmatched lines."""
    global_rules = catalog.get("global_rules", {})
    unmatched: List[str] = []
    with transcript_path.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cat, canonical, qty, score, kw = inv_parser.parse_line(line, catalog, global_rules)
            if not (cat and canonical and qty is not None):
                unmatched.append(line)
    return unmatched


def flatten_items(catalog: Dict) -> List[Tuple[str, str]]:
    """Return list of (category, item_name) pairs from catalog."""
    items: List[Tuple[str, str]] = []
    for cat, entries in catalog.items():
        if not isinstance(entries, list):
            continue
        for obj in entries:
            item = obj.get("item")
            if item:
                items.append((cat, item))
    return items


def prompt(prompt_text: str) -> str:
    try:
        return input(prompt_text).strip()
    except EOFError:
        return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", type=Path, required=True, help="Path to inventory_catalog.json")
    ap.add_argument("--transcript", type=Path, help="Transcript file to scan for unmatched lines")
    ap.add_argument("--unmatched", type=Path, help="Optional file containing unmatched lines (one per line)")
    ap.add_argument("--output", type=Path, help="Where to write updated catalog (defaults to --catalog)")
    ap.add_argument("--top", type=int, default=5, help="Number of fuzzy suggestions to show")
    args = ap.parse_args()

    catalog_path = args.catalog
    out_path = args.output or catalog_path

    catalog = load_catalog(catalog_path)

    if args.unmatched:
        unmatched = [ln.strip() for ln in args.unmatched.read_text().splitlines() if ln.strip()]
    elif args.transcript:
        unmatched = collect_unmatched(args.transcript, catalog)
    else:
        raise SystemExit("Provide --transcript or --unmatched")

    if not unmatched:
        print("No unmatched lines found.")
        return

    existing = flatten_items(catalog)
    existing_names = [name for _, name in existing]

    for line in unmatched:
        print(f"\nUnmatched: {line}")
        choices = process.extract(line, existing_names, limit=args.top)
        for idx, (name, score, _) in enumerate(choices, start=1):
            cat = next((c for c, n in existing if n == name), "?")
            print(f"  {idx}. {name} (cat={cat}, score={score:.2f})")
        print("  n. New item")
        print("  s. Skip")

        sel = prompt("Select option [s]: ") or "s"
        if sel.lower() == "s":
            continue
        if sel.lower() == "n":
            new_name = prompt("  New item name: ")
            if not new_name:
                continue
            new_cat = prompt("  Category: ")
            kw = prompt("  Comma-separated keywords (optional): ")
            entry = {"item": new_name}
            if kw:
                entry["keywords"] = [k.strip() for k in kw.split(",") if k.strip()]
            catalog.setdefault(new_cat, []).append(entry)
            print(f"  Added {new_name} to category {new_cat}")
            continue
        try:
            idx = int(sel)
        except ValueError:
            print("  Invalid selection; skipping.")
            continue
        if not (1 <= idx <= len(choices)):
            print("  Invalid selection; skipping.")
            continue
        chosen_name = choices[idx - 1][0]
        new_kw = prompt(f"  Add extra keyword for {chosen_name} (optional): ")
        if new_kw:
            # find the entry and append keyword
            for cat, entries in catalog.items():
                if not isinstance(entries, list):
                    continue
                for obj in entries:
                    if obj.get("item") == chosen_name:
                        obj.setdefault("keywords", [])
                        if new_kw not in obj["keywords"]:
                            obj["keywords"].append(new_kw)
                        print(f"  Added keyword '{new_kw}' to {chosen_name}")
                        break

    with out_path.open("w") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")
    print(f"\n✔ Updated catalog written to {out_path}")


if __name__ == "__main__":
    main()
