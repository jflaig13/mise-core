# Learning Banks Architecture - Mise Multi-Agent System

## Vision

**Every domain agent in Mise has a learning bank as a fundamental part of its "brain."**

Learning banks are curated repositories of real production data (voice recordings, transcripts, corrections, outcomes) that enable:
- **Continuous Learning** - Agents improve from every interaction
- **Brain Enhancement** - Learning informs system prompts, examples, validation
- **Model Fine-Tuning** - Training data for custom ASR and LLM models
- **Quality Assurance** - Reference examples for regression testing
- **Pattern Discovery** - Understanding edge cases, common mistakes, user preferences

## Architecture Overview

```
Mise Multi-Agent System
├── Transrouter Learning Bank (Intent Classification)
├── Payroll Agent Learning Bank
├── Inventory Agent Learning Bank ✅ (First Implementation)
├── Ordering Agent Learning Bank
├── Scheduling Agent Learning Bank
└── Forecasting Agent Learning Bank
```

Each learning bank follows the same architecture but contains domain-specific data.

## Core Components

### 1. Primary Storage (GCS)
All raw recordings stored permanently in Google Cloud Storage:

```
gs://mise-production-data/
├── recordings/
│   ├── payroll/
│   │   ├── 2026-01-27/
│   │   └── 2026-02-03/
│   ├── inventory/
│   │   ├── 2026-01-31/
│   │   └── 2026-02-28/
│   ├── ordering/
│   ├── scheduling/
│   └── transrouter/       # Raw audio before routing
└── annotations/           # Manual labels and corrections
```

### 2. Learning Bank Catalogs
Structured metadata for each domain:

```
tests/learning_banks/
├── payroll_learning_bank.json
├── inventory_learning_bank.json
├── ordering_learning_bank.json
├── scheduling_learning_bank.json
├── transrouter_learning_bank.json
└── schemas/
    └── learning_bank_schema.json
```

### 3. Brain Integration
Learning banks feed into each agent's brain:

```
transrouter/src/
├── agents/
│   ├── payroll_agent.py         # Uses payroll learning bank
│   ├── inventory_agent.py       # Uses inventory learning bank
│   └── ...
├── prompts/
│   ├── payroll_prompt.py        # Few-shot examples from learning bank
│   ├── inventory_prompt.py      # Product name variants from learning bank
│   └── ...
└── brain/                       # NEW: Brain system
    ├── payroll_brain.py         # Memory, patterns, corrections
    ├── inventory_brain.py
    └── ...
```

## Domain-Specific Learning Banks

### Payroll Agent Learning Bank

**Purpose:** Learn payroll patterns, tip calculations, shift recognition

**Data Collected:**
- Voice recordings of tip approvals
- Transcripts with timestamp parsing
- Calculated tips vs. manual corrections
- Shift recognition accuracy
- Date/time parsing variants

**Learning Use Cases:**
- **Timestamp parsing** - "Last Friday at 5pm" → specific datetime
- **Tip calculation corrections** - When user overrides calculated amount
- **Shift pattern discovery** - Common shift types, durations, overlaps
- **Name recognition** - Employee name variants and nicknames
- **Edge cases** - Split shifts, overtime, double-time

**Brain Integration:**
```python
class PayrollBrain:
    def __init__(self):
        self.learning_bank = PayrollLearningBank()
        self.common_corrections = self.learning_bank.get_common_corrections()
        self.timestamp_examples = self.learning_bank.get_timestamp_examples()
        self.shift_patterns = self.learning_bank.discover_shift_patterns()

    def enhance_prompt(self, base_prompt):
        # Add few-shot examples from learning bank
        examples = self.learning_bank.get_best_examples(n=5)
        return base_prompt + format_examples(examples)
```

### Inventory Agent Learning Bank ✅

**Purpose:** Learn product names, pack conversions, unit inference

**Data Collected:**
- Voice recordings of inventory counts
- Product name variants (ASR errors)
- Pack size conversions (4-packs, 6-packs, cases)
- Unit inference patterns
- Catalog additions/corrections

**Learning Use Cases:**
- **Product name normalization** - "Cab Sauv" → "Cabernet Sauvignon"
- **Pack conversion patterns** - User says "6 four-packs" → system infers cans
- **Unit ambiguity** - "5 Stella" → 5 bottles? 5 kegs? (learn from context)
- **Missing products** - Discover products not in catalog
- **Regional variants** - Same product, different names

**Brain Integration:**
```python
class InventoryBrain:
    def __init__(self):
        self.learning_bank = InventoryLearningBank()
        self.product_variants = self.learning_bank.get_product_name_variants()
        self.pack_patterns = self.learning_bank.get_pack_conversion_patterns()
        self.common_units = self.learning_bank.get_unit_inference_rules()

    def normalize_product_name(self, raw_name):
        # Check learning bank for known variants
        normalized = self.product_variants.get(raw_name.lower())
        if normalized:
            return normalized
        # Otherwise use catalog fuzzy match
        return self.catalog.fuzzy_match(raw_name)
```

### Transrouter Learning Bank

**Purpose:** Learn intent classification patterns, routing decisions

**Data Collected:**
- Raw audio (before domain routing)
- Transcript with detected domain
- Classification confidence scores
- User corrections (if routed wrong)
- Ambiguous cases requiring clarification

**Learning Use Cases:**
- **Intent classification** - Keywords that indicate payroll vs inventory
- **Ambiguity detection** - "Check the schedule" → scheduling or payroll?
- **Confidence thresholds** - When to ask for clarification
- **Multi-intent handling** - "Pay Alex and count the bar" → payroll + inventory

**Brain Integration:**
```python
class TransrouterBrain:
    def __init__(self):
        self.learning_bank = TransrouterLearningBank()
        self.classification_patterns = self.learning_bank.get_classification_patterns()
        self.ambiguous_cases = self.learning_bank.get_ambiguous_cases()

    def classify_intent(self, transcript):
        # Check learning bank for known patterns
        for pattern in self.classification_patterns:
            if pattern.matches(transcript):
                return pattern.domain, pattern.confidence

        # Use keyword-based classification
        return self.keyword_classifier.classify(transcript)
```

### Ordering Agent Learning Bank

**Purpose:** Learn supplier names, product orders, quantity patterns

**Data Collected:**
- Voice recordings of orders
- Supplier name variants
- Product ordering patterns
- Quantity inference (par levels)
- Delivery day/time patterns

**Learning Use Cases:**
- **Supplier recognition** - "Sysco" vs "US Foods" from context
- **Product orders** - Common items ordered together
- **Par level learning** - "Top off the beer cooler" → infer quantities
- **Schedule patterns** - Which days are delivery days

### Scheduling Agent Learning Bank

**Purpose:** Learn schedule patterns, shift preferences, coverage rules

**Data Collected:**
- Voice recordings of schedule requests
- Shift swap patterns
- Employee availability patterns
- Coverage rules and preferences
- Time-off requests

**Learning Use Cases:**
- **Shift preferences** - Who prefers which shifts
- **Coverage rules** - Minimum staffing by day/time
- **Swap patterns** - Common shift trades
- **Availability inference** - "I can't work Mondays" → recurring pattern

### Forecasting Agent Learning Bank

**Purpose:** Learn sales patterns, event impact, weather correlation

**Data Collected:**
- Historical sales data with context
- Event calendars (holidays, festivals, games)
- Weather data and impact
- User overrides to forecasts

**Learning Use Cases:**
- **Event impact** - How much does a home game increase sales?
- **Weather patterns** - Rain decreases patio sales by X%
- **Seasonal trends** - Summer vs winter patterns
- **User override patterns** - When do managers adjust forecasts?

## Universal Learning Bank Schema

Every learning bank follows this schema:

```json
{
  "domain": "payroll|inventory|ordering|scheduling|forecasting|transrouter",
  "recordings": [
    {
      "id": "unique-id",
      "gcs_path": "gs://mise-production-data/recordings/{domain}/{period}/{file}",
      "metadata": {
        "recorded_at": "ISO 8601 timestamp",
        "period_id": "YYYY-MM-DD",
        "category": "domain-specific category",
        "duration_seconds": 45.2,
        "file_size_bytes": 123456
      },
      "transcript": {
        "text": "Full transcript",
        "confidence": 0.95,
        "model": "whisper-1",
        "asr_corrections": ["original → corrected"]
      },
      "processing": {
        "domain": "detected domain",
        "intent": "specific intent",
        "confidence": 0.92,
        "parsed_output": {},  # Domain-specific parsed result
        "model_used": "claude-sonnet-4",
        "tokens_used": 1234
      },
      "corrections": {
        "user_edited": false,
        "changes": [
          {
            "field": "field_name",
            "original_value": "...",
            "corrected_value": "...",
            "timestamp": "ISO 8601"
          }
        ],
        "feedback": {
          "thumbs_up": true,
          "comment": "optional user comment"
        }
      },
      "annotations": {
        "quality_score": 1-5,
        "difficulty": "easy|medium|hard",
        "edge_cases": ["pack_conversion", "ambiguous_quantity"],
        "parsing_accuracy": "perfect|good|fair|poor",
        "notes": "Manual notes about this recording"
      },
      "usage": {
        "test_case": true,
        "test_case_id": "optional test ID",
        "training_data": true,
        "few_shot_example": true,
        "tags": ["tag1", "tag2"]
      }
    }
  ],
  "patterns": {
    "common_corrections": [
      {
        "pattern": "What users often say wrong",
        "correction": "What it should be",
        "frequency": 15,
        "examples": ["recording_id_1", "recording_id_2"]
      }
    ],
    "edge_cases": {
      "ambiguous_quantities": [...],
      "unit_inference_failures": [...],
      "product_name_mismatches": [...]
    }
  },
  "summary": {
    "total_recordings": 156,
    "date_range": {...},
    "total_duration_hours": 2.3,
    "accuracy_metrics": {
      "perfect_parsing": 85,
      "user_corrections": 12,
      "parsing_failures": 3
    }
  }
}
```

## Brain Architecture

Each agent has a "brain" that uses its learning bank:

### Brain Components

1. **Memory** - Historical patterns and outcomes
2. **Examples** - Few-shot examples for prompting
3. **Corrections** - User feedback and adjustments
4. **Patterns** - Discovered rules and heuristics
5. **Confidence** - What the agent knows well vs. poorly

### Brain Integration Pattern

```python
class DomainAgentBrain:
    """Base class for domain agent brains."""

    def __init__(self, domain: str):
        self.domain = domain
        self.learning_bank = LearningBank(domain)

    def enhance_system_prompt(self, base_prompt: str) -> str:
        """Add learning bank examples to system prompt."""
        examples = self.learning_bank.get_few_shot_examples(n=5)
        corrections = self.learning_bank.get_common_corrections()
        return base_prompt + format_examples(examples, corrections)

    def post_process(self, raw_output: dict) -> dict:
        """Apply learned corrections to raw output."""
        corrections = self.learning_bank.get_applicable_corrections(raw_output)
        return apply_corrections(raw_output, corrections)

    def learn_from_correction(self, original, corrected, user_id):
        """Record user correction for future learning."""
        self.learning_bank.add_correction(original, corrected, user_id)

    def get_confidence(self, input_text: str) -> float:
        """Estimate confidence based on similar past examples."""
        similar = self.learning_bank.find_similar(input_text)
        return calculate_confidence(similar)
```

## Workflow Integration

### 1. During Interaction
```
User → Audio → Transrouter → Domain Agent → Parse → Present to User
                    ↓             ↓           ↓
                Learning      Learning    Learning
                Bank          Bank        Bank
                (intent)      (domain)    (parsing)
```

### 2. User Correction Flow
```
User corrects parsing error
    ↓
Correction logged to learning bank
    ↓
Brain updates patterns
    ↓
Next similar request → Better parsing (learned from correction)
```

### 3. Periodic Learning
```
Nightly/Weekly Job:
1. Analyze new recordings
2. Discover patterns
3. Update agent brains
4. Generate training datasets
5. Fine-tune models (future)
```

## Implementation Phases

### Phase 1: Foundation ✅ (Current)
- ✅ GCS storage for all recordings
- ✅ Inventory learning bank structure
- ⏳ Payroll learning bank structure
- ⏳ Learning bank schema definition
- ⏳ Basic brain integration (few-shot examples)

### Phase 2: Active Learning
- User correction capture UI
- Automatic learning bank updates
- Pattern discovery automation
- Brain enhancement from corrections

### Phase 3: Advanced Intelligence
- Custom ASR fine-tuning per domain
- LLM fine-tuning on corrections
- Cross-domain learning (inventory patterns help ordering)
- Predictive confidence scoring

## Benefits

### For Users
- **Better accuracy** - System learns from every correction
- **Personalization** - Adapts to your phrasings and preferences
- **Faster** - Fewer corrections needed over time

### For Development
- **Regression testing** - Real production test cases
- **Quality metrics** - Track improvement over time
- **Edge case discovery** - Find problems before users do

### For Models
- **Training data** - High-quality labeled data for fine-tuning
- **Domain-specific** - Restaurant vocabulary and patterns
- **Corrections** - Learn what models get wrong

## Maintenance

### Adding Recordings
- **Automatic** - All production audio auto-saved to GCS
- **No manual work** - Recordings collected organically

### Curating Learning Banks
- **Weekly review** - Tag interesting cases
- **Quality scoring** - Rate audio quality
- **Annotation** - Add notes for edge cases

### Using Learning Banks
- **Testing** - Download and run regression tests
- **Training** - Generate datasets for model fine-tuning
- **Prompting** - Extract few-shot examples for agents

## Documentation

- **This doc** - Overall architecture
- **`INVENTORY_LEARNING_BANK.md`** - Inventory-specific details
- **`PAYROLL_LEARNING_BANK.md`** - Payroll-specific details (TBD)
- **Learning bank catalogs** - `tests/learning_banks/*.json`

## Summary

Learning banks are not just test data - they are **the memory and experience of each domain agent.**

Every interaction makes Mise smarter. Every correction teaches the system. Every recording is a learning opportunity.

This is how Mise evolves from a voice processing system into an **intelligent assistant that truly understands your restaurant.**
