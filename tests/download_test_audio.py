#!/usr/bin/env python3
"""Download test audio files from GCS for automated testing.

Usage:
    python tests/download_test_audio.py              # Download all test cases
    python tests/download_test_audio.py --case bar_office_blueberry_4packs  # Download specific case
"""

import json
import subprocess
import sys
from pathlib import Path


def download_audio_file(gcs_path: str, local_path: Path) -> bool:
    """Download a single audio file from GCS.

    Args:
        gcs_path: GCS path like gs://bucket/path/file.webm
        local_path: Local destination path

    Returns:
        True if successful, False otherwise
    """
    local_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            ["gsutil", "cp", gcs_path, str(local_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Downloaded: {local_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download {gcs_path}: {e.stderr}")
        return False


def main():
    # Load manifest
    manifest_path = Path(__file__).parent / "test_data" / "inventory_audio_manifest.json"

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    test_cases = manifest["test_cases"]

    # Filter by case ID if specified
    if len(sys.argv) > 2 and sys.argv[1] == "--case":
        case_id = sys.argv[2]
        test_cases = [tc for tc in test_cases if tc["id"] == case_id]
        if not test_cases:
            print(f"❌ Test case '{case_id}' not found in manifest")
            sys.exit(1)

    # Download audio files
    audio_dir = Path(__file__).parent / "test_data" / "inventory_audio"

    print(f"📦 Downloading {len(test_cases)} test audio files...")
    print(f"📁 Destination: {audio_dir}\n")

    success_count = 0
    for tc in test_cases:
        gcs_path = tc["gcs_path"]
        filename = Path(gcs_path).name
        local_path = audio_dir / filename

        # Skip if already exists
        if local_path.exists():
            print(f"⏭️  Skipped (already exists): {filename}")
            success_count += 1
            continue

        if download_audio_file(gcs_path, local_path):
            success_count += 1

    print(f"\n✨ Done! {success_count}/{len(test_cases)} files ready")
    print(f"📂 Audio files location: {audio_dir}")


if __name__ == "__main__":
    main()
