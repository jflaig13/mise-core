#!/usr/bin/env python3
"""Build the inventory learning bank catalog from GCS recordings.

This script scans GCS for all inventory recordings and generates a comprehensive
catalog with metadata for machine learning and continuous improvement.

Usage:
    python tests/build_learning_catalog.py                    # Build full catalog
    python tests/build_learning_catalog.py --period 2026-01-31  # Specific period only
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def get_gcs_recordings(period_id: str = None) -> List[str]:
    """Get list of all recordings from GCS.

    Args:
        period_id: Optional period to filter by (YYYY-MM-DD)

    Returns:
        List of GCS paths
    """
    if period_id:
        pattern = f"gs://mise-production-data/recordings/{period_id}/"
    else:
        pattern = "gs://mise-production-data/recordings/**/*.webm"

    try:
        result = subprocess.run(
            ["gsutil", "ls", pattern],
            capture_output=True,
            text=True,
            check=True
        )
        paths = [line.strip() for line in result.stdout.strip().split("\n") if line.strip().endswith(".webm")]
        return paths
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to list GCS recordings: {e.stderr}")
        return []


def parse_filename_metadata(gcs_path: str) -> Dict[str, Any]:
    """Extract metadata from recording filename.

    Filename format: Category_Area_YYYYMMDD_HHMMSS.webm
    Example: Bar_TheOffice_20260201_023142.webm

    Args:
        gcs_path: GCS path to recording

    Returns:
        Dict with parsed metadata
    """
    filename = Path(gcs_path).name
    period_id = gcs_path.split("/")[-2]  # Extract period from path

    # Parse filename components
    parts = filename.replace(".webm", "").split("_")

    if len(parts) >= 4:
        category = parts[0].lower()
        area = parts[1].replace("-", " ")  # "Walk-in" -> "Walk in"
        date_str = parts[2]  # YYYYMMDD
        time_str = parts[3]  # HHMMSS

        # Parse datetime
        recorded_at = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")

        return {
            "category": category,
            "area": area,
            "period_id": period_id,
            "recorded_at": recorded_at.isoformat(),
            "filename": filename
        }
    else:
        return {
            "category": "unknown",
            "area": "unknown",
            "period_id": period_id,
            "recorded_at": None,
            "filename": filename
        }


def get_file_size(gcs_path: str) -> int:
    """Get file size in bytes from GCS.

    Args:
        gcs_path: GCS path to file

    Returns:
        File size in bytes, or 0 if error
    """
    try:
        result = subprocess.run(
            ["gsutil", "stat", gcs_path],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse size from stat output
        for line in result.stdout.split("\n"):
            if "Content-Length:" in line:
                return int(line.split(":")[1].strip())

        return 0
    except subprocess.CalledProcessError:
        return 0


def build_catalog_entry(gcs_path: str, index: int) -> Dict[str, Any]:
    """Build a catalog entry for a recording.

    Args:
        gcs_path: GCS path to recording
        index: Recording index for ID generation

    Returns:
        Catalog entry dict
    """
    metadata = parse_filename_metadata(gcs_path)
    file_size = get_file_size(gcs_path)

    # Generate unique ID
    recording_id = f"inv_{metadata['period_id']}_{index:03d}"

    entry = {
        "id": recording_id,
        "gcs_path": gcs_path,
        "metadata": {
            "recorded_at": metadata["recorded_at"],
            "period_id": metadata["period_id"],
            "category": metadata["category"],
            "area": metadata["area"],
            "duration_seconds": None,  # TODO: Extract from audio file
            "file_size_bytes": file_size
        },
        "transcript": {
            "text": None,  # TODO: Fetch from shelfy data if available
            "confidence": None,
            "model": "whisper-1"
        },
        "parsed_items": [],  # TODO: Fetch from shelfy data
        "corrections": {
            "user_edited": False,
            "changes": []
        },
        "annotations": {
            "quality_score": None,  # Manual annotation needed
            "difficulty": None,
            "edge_cases": [],
            "parsing_accuracy": None,
            "notes": ""
        },
        "usage": {
            "test_case": False,
            "test_case_id": None,
            "training_data": True,  # All recordings are potential training data
            "tags": [metadata["category"], metadata["area"].lower().replace(" ", "_")]
        }
    }

    return entry


def build_catalog(period_id: str = None) -> Dict[str, Any]:
    """Build complete learning bank catalog.

    Args:
        period_id: Optional period to filter by

    Returns:
        Complete catalog dict
    """
    print("📦 Building inventory learning bank catalog...")

    # Get all recordings
    recordings = get_gcs_recordings(period_id)
    print(f"   Found {len(recordings)} recordings in GCS")

    # Build catalog entries
    catalog_entries = []
    for idx, gcs_path in enumerate(recordings):
        print(f"   Processing {idx + 1}/{len(recordings)}: {Path(gcs_path).name}")
        entry = build_catalog_entry(gcs_path, idx)
        catalog_entries.append(entry)

    # Calculate summary stats
    categories = {}
    total_size = 0
    earliest_date = None
    latest_date = None

    for entry in catalog_entries:
        cat = entry["metadata"]["category"]
        categories[cat] = categories.get(cat, 0) + 1
        total_size += entry["metadata"]["file_size_bytes"] or 0

        recorded_at = entry["metadata"]["recorded_at"]
        if recorded_at:
            if earliest_date is None or recorded_at < earliest_date:
                earliest_date = recorded_at
            if latest_date is None or recorded_at > latest_date:
                latest_date = recorded_at

    catalog = {
        "recordings": catalog_entries,
        "summary": {
            "total_recordings": len(catalog_entries),
            "date_range": {
                "earliest": earliest_date,
                "latest": latest_date
            },
            "categories": categories,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "tagged_for_training": len([e for e in catalog_entries if e["usage"]["training_data"]]),
            "tagged_for_testing": len([e for e in catalog_entries if e["usage"]["test_case"]])
        },
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0",
            "purpose": "Inventory learning bank for model training and testing"
        }
    }

    return catalog


def main():
    period_id = None
    if len(sys.argv) > 2 and sys.argv[1] == "--period":
        period_id = sys.argv[2]

    catalog = build_catalog(period_id)

    # Write catalog
    output_path = Path(__file__).parent / "test_data" / "learning_bank_catalog.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(catalog, f, indent=2)

    print(f"\n✨ Catalog built successfully!")
    print(f"📊 Summary:")
    print(f"   - Total recordings: {catalog['summary']['total_recordings']}")
    print(f"   - Categories: {catalog['summary']['categories']}")
    print(f"   - Total size: {catalog['summary']['total_size_mb']} MB")
    print(f"   - Date range: {catalog['summary']['date_range']['earliest']} to {catalog['summary']['date_range']['latest']}")
    print(f"\n📝 Catalog saved to: {output_path}")
    print(f"\n💡 Next steps:")
    print(f"   1. Review catalog and add manual annotations")
    print(f"   2. Tag recordings for specific training purposes")
    print(f"   3. Mark high-quality examples as test cases")


if __name__ == "__main__":
    main()
