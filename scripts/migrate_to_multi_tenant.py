#!/usr/bin/env python3
"""Migrate existing data to multi-tenant structure.

Moves all existing Papa Surf data to data/papasurf/ and creates
empty SoWal House directory structure.

Run from repo root:
    python scripts/migrate_to_multi_tenant.py
"""

import json
import shutil
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "mise_app" / "data"


def migrate():
    print("=" * 60)
    print("Multi-Tenant Data Migration")
    print("=" * 60)

    # Create papasurf directory
    papasurf_dir = DATA_DIR / "papasurf"
    papasurf_dir.mkdir(exist_ok=True)
    print(f"\n✓ Created {papasurf_dir}")

    # Move all period directories (20XX-*)
    moved_periods = []
    for item in list(DATA_DIR.iterdir()):
        if item.is_dir() and item.name.startswith("20") and item.name != "papasurf" and item.name != "sowalhouse":
            target = papasurf_dir / item.name
            if not target.exists():
                shutil.move(str(item), str(target))
                moved_periods.append(item.name)
                print(f"  → Moved {item.name}/ to papasurf/")
            else:
                print(f"  ⚠ Skipped {item.name}/ (already exists in papasurf/)")

    # Move inventory if exists and not already moved
    inventory_src = DATA_DIR / "inventory"
    inventory_dst = papasurf_dir / "inventory"
    if inventory_src.exists() and inventory_src.is_dir():
        if not inventory_dst.exists():
            shutil.move(str(inventory_src), str(inventory_dst))
            print(f"  → Moved inventory/ to papasurf/")
        else:
            print(f"  ⚠ Skipped inventory/ (already exists in papasurf/)")

    # Move loose JSON files to papasurf root (legacy files)
    for json_file in ["approval_queue.json", "weekly_totals.json"]:
        src = DATA_DIR / json_file
        if src.exists():
            dst = papasurf_dir / json_file
            if not dst.exists():
                shutil.move(str(src), str(dst))
                print(f"  → Moved {json_file} to papasurf/")

    # Create papasurf metadata
    metadata_papasurf = {
        "restaurant_id": "papasurf",
        "name": "Papa Surf",
        "location": "Panama City Beach, FL",
        "branding": {
            "logo_url": "/static/logos/papasurf.png",
            "primary_color": "#2D8A4E"
        }
    }
    with open(papasurf_dir / "metadata.json", "w") as f:
        json.dump(metadata_papasurf, f, indent=2)
    print(f"✓ Created papasurf/metadata.json")

    # Create SoWal House (clean slate)
    sowalhouse_dir = DATA_DIR / "sowalhouse"
    sowalhouse_dir.mkdir(exist_ok=True)
    print(f"\n✓ Created {sowalhouse_dir}")

    metadata_sowalhouse = {
        "restaurant_id": "sowalhouse",
        "name": "SoWal House",
        "location": "Seaside, FL",
        "branding": {
            "logo_url": "/static/logos/sowalhouse.png",
            "primary_color": "#1B2A4E"
        }
    }
    with open(sowalhouse_dir / "metadata.json", "w") as f:
        json.dump(metadata_sowalhouse, f, indent=2)
    print(f"✓ Created sowalhouse/metadata.json")

    # Summary
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print(f"\nPapa Surf data:")
    print(f"  - Periods migrated: {len(moved_periods)}")
    if moved_periods:
        for p in moved_periods:
            print(f"    • {p}")

    print(f"\nSoWal House:")
    print(f"  - Clean slate (empty data directory)")

    print(f"\nVerify with:")
    print(f"  ls -la {papasurf_dir}/")
    print(f"  ls -la {sowalhouse_dir}/")


if __name__ == "__main__":
    migrate()
