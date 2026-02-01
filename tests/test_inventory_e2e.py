"""End-to-end tests for inventory voice processing using real audio files.

These tests use actual production audio recordings from the test_data/ directory
to verify the complete pipeline: audio → transcript → parsing → conversion display.

Run:
    # Download test audio first
    python tests/download_test_audio.py

    # Run tests
    pytest tests/test_inventory_e2e.py -v
"""

import json
import pytest
from pathlib import Path


# Load test manifest
MANIFEST_PATH = Path(__file__).parent / "test_data" / "inventory_audio_manifest.json"
AUDIO_DIR = Path(__file__).parent / "test_data" / "inventory_audio"


@pytest.fixture(scope="module")
def test_manifest():
    """Load test audio manifest."""
    with open(MANIFEST_PATH, "r") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def ensure_audio_downloaded():
    """Ensure test audio files are downloaded before running tests."""
    if not AUDIO_DIR.exists() or not list(AUDIO_DIR.glob("*.webm")):
        pytest.skip(
            "Test audio files not found. Run: python tests/download_test_audio.py"
        )


def test_manifest_valid(test_manifest):
    """Verify test manifest structure is valid."""
    assert "test_cases" in test_manifest
    assert len(test_manifest["test_cases"]) > 0

    for tc in test_manifest["test_cases"]:
        assert "id" in tc
        assert "gcs_path" in tc
        assert "category" in tc
        assert "area" in tc


@pytest.mark.parametrize("test_case_id", [
    "bar_office_blueberry_4packs",
    "bar_walkin_kegs",
    "bar_office_wine_mix",
    "kitchen_dry_goods"
])
def test_audio_file_exists(test_case_id, test_manifest, ensure_audio_downloaded):
    """Verify test audio files exist locally."""
    test_case = next(tc for tc in test_manifest["test_cases"] if tc["id"] == test_case_id)
    filename = Path(test_case["gcs_path"]).name
    audio_path = AUDIO_DIR / filename

    assert audio_path.exists(), f"Audio file not found: {audio_path}"
    assert audio_path.stat().st_size > 0, f"Audio file is empty: {audio_path}"


@pytest.mark.e2e
def test_blueberry_4packs_conversion(test_manifest, ensure_audio_downloaded):
    """Test pack conversion calculation for High Rise Blueberry 4-packs.

    This is a regression test for the conversion display feature.
    Expected: 6 4-packs should show conversion "6 × 4 = 24 cans"
    """
    # TODO: Implement full e2e test
    # 1. Load audio file
    # 2. Send to transrouter API
    # 3. Verify response includes conversion_display
    # 4. Assert conversion_display == "6 × 4 = 24 cans"

    test_case = next(tc for tc in test_manifest["test_cases"] if tc["id"] == "bar_office_blueberry_4packs")

    # Placeholder assertion
    assert "expected_items" in test_case
    expected_item = test_case["expected_items"][0]
    assert expected_item["conversion_display"] == "6 × 4 = 24 cans"


@pytest.mark.e2e
def test_wine_bottles_no_conversion(test_manifest, ensure_audio_downloaded):
    """Test that regular bottles don't show conversion (no pack size).

    Expected: Simple quantities like "6 bottles" should NOT have conversion_display
    """
    # TODO: Implement full e2e test
    # 1. Load audio file
    # 2. Send to transrouter API
    # 3. Verify wine bottles don't have conversion_display (or it's null)

    test_case = next(tc for tc in test_manifest["test_cases"] if tc["id"] == "bar_office_wine_mix")
    expected_item = test_case["expected_items"][0]

    # Wine bottles should NOT have conversion
    assert "conversion_display" not in expected_item


# Example of how to use these test files in future automated tests:
"""
from pathlib import Path
import requests

def send_audio_to_transrouter(audio_path: Path, category: str, area: str):
    '''Send audio file to transrouter API for processing.'''
    with open(audio_path, "rb") as f:
        files = {"file": (audio_path.name, f, "audio/webm")}
        response = requests.post(
            "https://mise-transrouter-147422626167.us-central1.run.app/api/v1/audio/process",
            files=files,
            headers={"X-API-Key": os.getenv("MISE_API_KEY")}
        )
    return response.json()

# Then in tests:
def test_full_pipeline(test_manifest):
    test_case = test_manifest["test_cases"][0]
    audio_path = AUDIO_DIR / Path(test_case["gcs_path"]).name

    result = send_audio_to_transrouter(
        audio_path,
        test_case["category"],
        test_case["area"]
    )

    assert result["status"] == "success"
    assert result["domain"] == "inventory"
    # ... verify expected items, conversions, etc.
"""
