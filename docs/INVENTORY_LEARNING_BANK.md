# Inventory Learning Bank

## Purpose

The Inventory Learning Bank is a curated repository of real production voice recordings used for:

1. **Continuous Learning** - Building corpus of real inventory phrasings and patterns
2. **Model Improvement** - Training data for ASR and parsing model fine-tuning
3. **Automated Testing** - Regression testing for new features
4. **Quality Assurance** - Reference examples for validation
5. **Pattern Recognition** - Understanding common mistakes, edge cases, product name variants

## Storage Architecture

### Primary Storage (GCS)
```
gs://mise-production-data/recordings/
├── 2026-01-31/          # Organized by inventory date
│   ├── Bar_TheOffice_YYYYMMDD_HHMMSS.webm
│   ├── Bar_Walk-in_YYYYMMDD_HHMMSS.webm
│   └── ...
├── 2026-02-28/
│   └── ...
└── 2026-03-31/
    └── ...
```

### Metadata Storage (Local + GCS)
```
tests/test_data/
├── inventory_audio_manifest.json      # Test cases (curated subset)
└── learning_bank_catalog.json         # Full catalog with annotations
```

## Recording Metadata

Each recording should capture:

### Automatic Metadata (captured by system)
- **Recording timestamp** - When it was recorded
- **Period ID** - Which inventory period (YYYY-MM-DD)
- **Category** - bar, kitchen, dry goods
- **Area** - Specific location (The Office, Walk-in, etc.)
- **Transcript** - ASR output
- **Parsed items** - What Mise extracted
- **User corrections** - If user edited after parsing

### Manual Annotations (added during review)
- **Quality score** - Audio clarity (1-5)
- **Difficulty level** - Easy/Medium/Hard parsing
- **Edge cases** - What makes it interesting (accents, background noise, unclear quantities)
- **Parsing accuracy** - How well did Mise do?
- **Product name variants** - Alternative phrasings discovered

## Learning Use Cases

### 1. ASR Fine-Tuning
- Collect examples of commonly misheard product names
- Example: "Cab Sauv" → "Cabernet Sauvignon"
- Build custom vocabulary for restaurant inventory

### 2. Parsing Model Training
- Examples of different quantity phrasings:
  - "six four-packs"
  - "6 four packs"
  - "half a case"
  - "about 5 bottles"
- Unit inference patterns
- Ambiguity resolution

### 3. Error Pattern Analysis
- What products are frequently misidentified?
- Which units cause confusion?
- Common transcription errors
- Background noise interference

### 4. Product Catalog Enhancement
- Discover missing products (not in catalog)
- Find alternative names/variants
- Identify regional naming differences
- Update SKU mappings

## Workflow Integration

### During Inventory
1. User records audio → Auto-saved to GCS
2. System transcribes and parses
3. User reviews and corrects if needed
4. **Corrections automatically logged** as learning data

### Post-Inventory Review
1. Review flagged recordings (low confidence, user corrections)
2. Add manual annotations
3. Update catalog based on discoveries
4. Tag recordings for specific training purposes

### Periodic Analysis
1. Run analytics on learning bank
2. Identify improvement opportunities
3. Generate training datasets for model fine-tuning
4. Update system prompts based on patterns

## Learning Bank Catalog Schema

```json
{
  "recordings": [
    {
      "id": "unique-recording-id",
      "gcs_path": "gs://mise-production-data/recordings/2026-01-31/Bar_TheOffice_20260201_023142.webm",
      "metadata": {
        "recorded_at": "2026-01-31T20:31:42-06:00",
        "period_id": "2026-01-31",
        "category": "bar",
        "area": "The Office",
        "duration_seconds": 45.2,
        "file_size_bytes": 123456
      },
      "transcript": {
        "text": "Bar inventory for The Office. Six four-packs of High Rise Blueberry...",
        "confidence": 0.95,
        "model": "whisper-1"
      },
      "parsed_items": [
        {
          "product_name": "High Rise Blueberry",
          "quantity": 6,
          "unit": "4-packs",
          "conversion_display": "6 × 4 = 24 cans",
          "confidence": 0.92
        }
      ],
      "corrections": {
        "user_edited": false,
        "changes": []
      },
      "annotations": {
        "quality_score": 5,
        "difficulty": "medium",
        "edge_cases": ["pack_conversion", "new_product"],
        "parsing_accuracy": "perfect",
        "notes": "Good example of pack conversion working correctly"
      },
      "usage": {
        "test_case": true,
        "test_case_id": "bar_office_blueberry_4packs",
        "training_data": true,
        "tags": ["pack_conversion", "blueberry", "4-packs"]
      }
    }
  ],
  "summary": {
    "total_recordings": 13,
    "date_range": {
      "earliest": "2026-01-31",
      "latest": "2026-01-31"
    },
    "categories": {
      "bar": 10,
      "kitchen": 3
    },
    "total_duration_seconds": 542.6,
    "tagged_for_training": 8,
    "tagged_for_testing": 4
  }
}
```

## Comparison to Payroll Learning Bank

### Similarities
- Real production audio stored permanently
- Used for both testing and learning
- Captures corrections as feedback
- Builds over time organically

### Differences
- **Inventory** - More product variety, pack conversions, unit inference
- **Payroll** - More date/time parsing, shift calculations, tip splitting

## Future Enhancements

### Phase 1 (Current)
- ✅ Store all recordings in GCS
- ✅ Basic test case manifest
- ⏳ Learning bank catalog with annotations

### Phase 2 (Next)
- Auto-generate learning bank entries from recordings
- User feedback capture (thumbs up/down on parsing)
- Periodic analytics reports

### Phase 3 (Advanced)
- Fine-tune Whisper model on inventory vocabulary
- Custom parsing model trained on corrections
- Automated discovery of new products/variants
- Cross-reference with Toast POS data for validation

## Maintenance

### Adding New Recordings
All recordings automatically saved to GCS. To curate for learning:
1. Review new recordings periodically
2. Add high-quality examples to learning bank catalog
3. Annotate interesting edge cases
4. Tag for specific training purposes

### Cleaning/Pruning
- Keep **all** recordings indefinitely (storage is cheap)
- Archive low-quality audio separately
- Maintain curated subset for active training

### Privacy/Security
- Audio contains business data (inventory counts)
- Store in private GCS bucket (mise-production-data)
- No PII in inventory recordings
- Access controlled via IAM

## Documentation Links

- Test Infrastructure: `tests/test_data/README.md`
- Test Manifest: `tests/test_data/inventory_audio_manifest.json`
- Learning Catalog: `tests/test_data/learning_bank_catalog.json` (to be created)
- GCS Bucket: `gs://mise-production-data/recordings/`
