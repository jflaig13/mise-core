# Transrouter — Master Specification

**Version:** 1.0
**Last Updated:** 2025-12-19
**Status:** CANONICAL
**Owner:** Jon Flaig, Mise, Inc.

---

## 1. PURPOSE

The Transrouter is Mise's central orchestration layer. It receives voice input from users, transcribes it, classifies intent, extracts entities, and routes requests to the appropriate domain agent (Payroll, Inventory, etc.).

This is the "Router Assistant" from Mise's architecture — the brain that listens and decides where to send each request.

```
User speaks → Transrouter → Domain Agent → Automation Runner → Output
```

---

## 2. CURRENT STATE

The transrouter skeleton exists in `/transrouter/` with the following components:

| Component | File | Status |
|-----------|------|--------|
| Orchestrator | `src/transrouter_orchestrator.py` | Working |
| Intent Classifier | `src/intent_classifier.py` | Working (keyword-based) |
| Entity Extractor | `src/entity_extractor.py` | Working (regex-based) |
| Domain Router | `src/domain_router.py` | **STUB** — agents not implemented |
| ASR Adapter | `src/asr_adapter.py` | Whisper only, needs upgrade |
| Schemas | `src/schemas.py` | Complete |
| Tests | `tests/test_orchestrator.py` | 3 passing |
| Config | `config/default.yaml` | Basic |

### Pipeline Flow (Current)

```
Audio/Text
    → ASR (Whisper local)
    → Intent Classifier (keyword scoring → payroll/inventory)
    → Entity Extractor (regex → dates/numbers/names)
    → Domain Router
    → Agent (STUB - returns "not_implemented")
```

---

## 3. TRANSCRIPTION ARCHITECTURE (DECIDED)

### 3.1 Design Principles

1. **Cost control at scale** — Transcription costs must not grow linearly with usage
2. **Quality parity with Whisper** — No accuracy degradation
3. **Failover resilience** — System works even if primary provider is down
4. **Local-first when possible** — Reduce cloud dependency

### 3.2 Tiered Architecture

**Tier 1: Self-hosted Faster-Whisper (PRIMARY)**
- Faster-Whisper is a CTranslate2-optimized Whisper implementation
- 4x faster than standard Whisper, lower memory usage
- Runs on Mise backend with GPU (T4 or better)
- **Cost model:** Fixed server cost (~$150/month), unlimited transcription
- **Use case:** All production transcription

**Tier 2: Groq Whisper API (FALLBACK)**
- Groq offers Whisper large-v3 at $0.000111/minute (~60x cheaper than OpenAI)
- Extremely fast inference
- **Cost model:** Pay-per-minute, but so cheap it's nearly free
- **Use case:** Failover when self-hosted is unavailable, local development, burst capacity

### 3.3 Cost Comparison

| Volume (min/month) | OpenAI API | Groq API | Self-hosted |
|--------------------|------------|----------|-------------|
| 1,000 | $6 | $0.11 | ~$150 |
| 10,000 | $60 | $1.11 | ~$150 |
| 100,000 | $600 | $11.10 | ~$150 |
| 1,000,000 | $6,000 | $111 | ~$150 |

Self-hosted wins at scale. Groq wins for low volume and development.

### 3.4 Provider Selection Logic

```python
def select_asr_provider(config, context):
    if config.force_provider:
        return config.force_provider

    if context.environment == "development":
        return "groq"  # Don't require local GPU for dev

    if self_hosted_available():
        return "faster_whisper"
    else:
        return "groq"  # Automatic failover
```

---

## 4. IMPLEMENTATION TASKS

### 4.1 ASR Adapter Upgrades (PRIORITY: HIGH)

**Task:** Implement new ASR adapters in `src/asr_adapter.py`

1. **FasterWhisperAdapter**
   - Use `faster-whisper` Python package
   - Support model selection (tiny, base, small, medium, large-v3)
   - Return TranscriptResult with confidence scores
   - Handle GPU/CPU detection automatically

2. **GroqWhisperAdapter**
   - Use Groq API (requires GROQ_API_KEY)
   - Model: whisper-large-v3
   - Implement proper error handling and retry logic
   - Return TranscriptResult matching same schema

3. **Provider Selection Function**
   - `get_asr_provider()` should implement tiered logic
   - Config-driven provider override
   - Automatic failover on error

**Dependencies to add to requirements.txt:**
```
faster-whisper>=1.0.0
groq>=0.4.0
```

### 4.2 Domain Agent Implementation (PRIORITY: HIGH)

**Task:** Wire real agents into `src/domain_router.py`

1. **Payroll Agent**
   - Connect to existing LPM logic for weekly batch payroll
   - Connect to existing CPM logic for single-shift cloud ingestion
   - Determine mode from intent/entities (batch vs single shift)

2. **Inventory Agent**
   - Connect to existing LIM logic
   - Pass transcript + product catalog to parser
   - Return structured inventory JSON

**Note:** Agents should NOT duplicate LPM/CPM/LIM code. They should import and call existing modules.

### 4.3 API Layer (PRIORITY: MEDIUM)

**Task:** Create FastAPI server to expose transrouter as HTTP endpoints

```
POST /transcribe          → Audio in, transcript out
POST /route               → Text in, routed response out
POST /process             → Audio in, full pipeline, agent response out
GET  /health              → Health check
```

This enables mobile app integration.

### 4.4 Intent Classifier Upgrade (PRIORITY: LOW)

**Task:** Replace keyword-based classifier with LLM-based classification

Current classifier uses keyword scoring. Future version should:
- Use Claude Haiku for fast, cheap intent classification
- Support more domains (scheduling, ordering, forecasting, ops)
- Return structured intent with higher confidence

**Defer until:** Basic pipeline is working end-to-end with current classifier.

---

## 5. FILE STRUCTURE (TARGET)

```
transrouter/
├── config/
│   ├── __init__.py
│   └── default.yaml
├── src/
│   ├── __init__.py
│   ├── transrouter_orchestrator.py  # Main pipeline
│   ├── asr_adapter.py               # ASR providers (Faster-Whisper, Groq)
│   ├── intent_classifier.py         # Intent classification
│   ├── entity_extractor.py          # Entity extraction
│   ├── domain_router.py             # Routes to agents
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── payroll_agent.py         # Connects to LPM/CPM
│   │   └── inventory_agent.py       # Connects to LIM
│   ├── schemas.py                   # Data models
│   └── logging_utils.py             # Logging
├── api/
│   ├── __init__.py
│   └── server.py                    # FastAPI endpoints
├── tests/
│   ├── __init__.py
│   ├── test_orchestrator.py
│   ├── test_asr_adapters.py
│   └── test_agents.py
├── TRANSROUTER_SPEC.md              # This file
└── README.md
```

---

## 6. CODING GUIDELINES

### 6.1 Allowed

- Implement new ASR adapters following existing pattern
- Wire agents to existing LPM/CPM/LIM code via imports
- Add new tests for all new functionality
- Update config schema for new providers
- Add FastAPI server in `api/`

### 6.2 Forbidden

- Do NOT duplicate LPM/CPM/LIM logic — import it
- Do NOT change existing schemas without explicit approval
- Do NOT hardcode API keys — use environment variables
- Do NOT remove existing Whisper adapter (keep for compatibility)

### 6.3 Environment Variables

```
GROQ_API_KEY          — Required for Groq fallback
ASR_PROVIDER          — Override: "faster_whisper" | "groq" | "whisper"
FASTER_WHISPER_MODEL  — Model size: "base" | "small" | "medium" | "large-v3"
```

---

## 7. IMMEDIATE NEXT STEPS

**For the next Claude Code session, execute in this order:**

1. **Add dependencies** — Update `requirements.txt` with `faster-whisper` and `groq`

2. **Implement FasterWhisperAdapter** — Add to `asr_adapter.py`
   - Lazy model loading
   - GPU/CPU auto-detection
   - Return TranscriptResult

3. **Implement GroqWhisperAdapter** — Add to `asr_adapter.py`
   - API client setup
   - Error handling with retry
   - Return TranscriptResult

4. **Update get_asr_provider()** — Implement tiered selection logic

5. **Write tests** — Add `tests/test_asr_adapters.py` with unit tests for both adapters

6. **Test end-to-end** — Run `pytest transrouter/tests/` to verify nothing broke

---

## 8. SUCCESS CRITERIA

The transrouter transcription upgrade is complete when:

- [ ] FasterWhisperAdapter transcribes audio correctly
- [ ] GroqWhisperAdapter transcribes audio correctly
- [ ] Provider selection follows tiered logic
- [ ] Automatic failover works (Faster-Whisper down → Groq takes over)
- [ ] All existing tests still pass
- [ ] New adapter tests pass
- [ ] Config can override provider selection

---

## 9. RELATED DOCUMENTATION

- `workflow_specs/LPM/LPM_Workflow_Master.txt` — Local Payroll Machine spec
- `workflow_specs/CPM/CPM_Workflow_Master.txt` — Cloud Payroll Machine spec
- `workflow_specs/LIM/LIM_Workflow_Master.txt` — Local Inventory Machine spec
- `docs/brain/121224__system-truth-how-mise-works.md` — Core system principles
- `CLAUDE.md` — Agent onboarding and safety protocols

---

**END OF TRANSROUTER SPEC**
