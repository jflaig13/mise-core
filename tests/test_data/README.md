# Inventory Test Audio Data

This directory contains real production audio recordings used for automated end-to-end testing of the inventory voice processing pipeline.

## Files

- **`inventory_audio_manifest.json`** - Test case definitions with expected results
- **`inventory_audio/`** - Downloaded audio files (not in git, downloaded on-demand)

## Usage

### 1. Download Test Audio Files

```bash
# Download all test audio files from GCS
python tests/download_test_audio.py

# Download a specific test case
python tests/download_test_audio.py --case bar_office_blueberry_4packs
```

### 2. Run Tests

```bash
# Run all inventory e2e tests
pytest tests/test_inventory_e2e.py -v

# Run specific test
pytest tests/test_inventory_e2e.py::test_blueberry_4packs_conversion -v

# Run only e2e tests (skip unit tests)
pytest tests/test_inventory_e2e.py -m e2e
```

## Test Cases

### bar_office_blueberry_4packs
**Purpose:** Test pack conversion display (6 × 4 = 24 cans)
**Audio:** Bar inventory with High Rise Blueberry 4-packs
**Expected:** conversion_display field shows "6 × 4 = 24 cans"

### bar_walkin_kegs
**Purpose:** Test keg/beer unit keywords for intent classification
**Audio:** Bar inventory with kegs
**Expected:** Routes to inventory domain (not payroll)

### bar_office_wine_mix
**Purpose:** Test wine bottles and bar mixes (no conversion)
**Audio:** Squealing Pig Sauvignon Blanc, Scarpetta Pinot Grigio
**Expected:** No conversion_display for simple bottle counts

### kitchen_dry_goods
**Purpose:** Test kitchen category inventory
**Audio:** Dry goods area inventory
**Expected:** Routes to inventory domain with category=kitchen

## Adding New Test Cases

1. Record audio in the Mise app
2. Note the GCS path from Cloud Storage
3. Add entry to `inventory_audio_manifest.json`:

```json
{
  "id": "unique_test_id",
  "description": "What this test verifies",
  "gcs_path": "gs://mise-production-data/recordings/YYYY-MM-DD/File.webm",
  "category": "bar|kitchen",
  "area": "Area Name",
  "expected_items": [
    {
      "product_name": "Product Name",
      "quantity": 6,
      "unit": "bottles",
      "conversion_display": "optional conversion string"
    }
  ]
}
```

4. Run download script to fetch the new audio
5. Add test case to `test_inventory_e2e.py`

## Storage

**Source:** GCS bucket `mise-production-data/recordings/`
**Local:** `tests/test_data/inventory_audio/` (gitignored)

Audio files are **not checked into git** - they're downloaded on-demand from GCS. This keeps the repo size small while ensuring tests always use real production audio.

## Notes

- Audio files are `.webm` format (browser-native recording format)
- All recordings are from Jan 31, 2026 full inventory
- These represent real edge cases and production scenarios
- Use these for regression testing when changing inventory parsing logic
