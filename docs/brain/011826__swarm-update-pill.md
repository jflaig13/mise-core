TITLE
SWARM UPDATE PILL — Canonical Mise State Synchronization

STATUS
CANONICAL

DATE ADDED
2026-01-18 (mmddyy filename: 011826)

SOURCE
Jon — direct instruction ("swarm update pill" for multi-window coordination)

PURPOSE
Provide a single canonical document that any Claude Code window (ccw) can ingest to become fully synchronized with Mise's current state, architecture, goals, and development context. This is the "onboarding pill" for swarm coordination.

TRIGGER PHRASE
When Jon says "take your swarm update pill", read this document and all referenced files below.

---

## WHAT THIS DOCUMENT IS

This is your **complete synchronization checkpoint** for working on Mise as part of a multi-window development swarm.

**Reading this document means you will know:**
- What Mise is and what problem it solves
- Current technical architecture (services, ports, dependencies)
- Active development priorities
- Investor demo deadline and fundraising context
- Engineering standards and guardrails
- Your role in the 6-window swarm
- How to start services and verify they're working
- Common pitfalls and how to avoid them

**After ingesting this pill, you will be ready to:**
- Write production-grade code for your assigned domain
- Coordinate with other windows safely
- Follow enterprise-grade engineering standards
- Avoid port conflicts and architectural mistakes
- Maintain clean, non-duplicative code

---

## CRITICAL CONTEXT — READ FIRST

### 1. Investor Demo Deadline

**Date:** Tuesday, January 20th, 2026 @ 1PM
**Time Until Demo:** ~45 hours from now (as of 2026-01-18 evening)
**Implication:** All work must be demo-ready, stable, and presentable

### 2. Fundraising Context

**Raising:** $250,000
**Timeline:** 12 months (T1-T12)
**Goal:** 10-20 paying restaurant customers, enterprise-grade platform, SOC 2 ready

### 3. Current Production Status

**Mise is LIVE in production at Papa Surf Burger Bar since Q3 2025.**
- Jon runs real payroll weekly using this system
- This is NOT a prototype or demo
- Real money, real employees, real restaurant operations

### 4. Multi-Window Swarm

**6 Claude Code windows active:**
- **ccqb (Window #1):** Coordinator & Transrouter — enterprise architecture, API gateway, orchestration
- **ccw2 (Window #2):** Frontend (mise_app) — UI/UX, templates, user flows
- **ccw3 (Window #3):** Payroll Agent — tip pooling logic, approval JSON, business rules
- **ccw4 (Window #4):** Testing & QA — test suites, CI/CD, quality assurance
- **ccw5 (Window #5):** Demo Prep & Documentation — pitch materials, investor demo, docs
- **ccw6 (Window #6):** Backend & Infrastructure — database, deployment, monitoring

---

## REQUIRED READING — INGEST THESE FILES

**Read these files in order to be fully synchronized:**

### 1. Complete Mise State Report (MUST READ FIRST)
**File:** `/Users/jonathanflaig/mise-core/docs/MISE_STATE_COMPLETE.md`

**Contains:**
- The Mise Web App — what it is, what workflows it contains
- FastAPI explanation
- Pitch deck insights
- Fundraising ask ($250K breakdown)
- 12-month roadmap (T1-T12)
- Enterprise-grade engineering standards
- Current technical architecture
- Port 8080 conflict explanation
- CPM deprecation plan
- Dev environment startup & verification
- Health checks usage guide

**Read this FIRST — it's the comprehensive state of the entire system.**

### 2. System Truth — How Mise Works (Foundational)
**File:** `/Users/jonathanflaig/mise-core/docs/brain/121224__system-truth-how-mise-works.md`

**Core principle:**
- Mise is a FILE-BASED INTELLIGENCE SYSTEM
- Knowledge only exists if written to files
- Chat is transient, files are cognition, git history is memory
- IF IT IS NOT IN A FILE, IT DOES NOT EXIST

### 3. Workflow Primacy Directive
**File:** `/Users/jonathanflaig/mise-core/docs/brain/121224__workflow-primacy-directive.md`

**Core principle:**
- Workflows are foundational truth
- Load workflows before reasoning
- Never re-ask questions already answered in workflow specs
- Workflows override intuition

### 4. Service Startup Guide
**File:** `/Users/jonathanflaig/mise-core/START_MISE.md`

**Contains:**
- Correct architecture (mise_app:8000, transrouter:8080)
- How to start services
- How to verify they're working
- Common mistakes to avoid

### 5. Port Cleanup Summary
**File:** `/Users/jonathanflaig/mise-core/PORT_CLEANUP_SUMMARY.md`

**Contains:**
- What the port 8080 conflict was
- Why it happened
- How it's fixed
- How to prevent it

### 6. LPM Workflow Master (Payroll Rules)
**File:** `/Users/jonathanflaig/mise-core/workflow_specs/LPM/LPM_Workflow_Master.txt`

**Contains:**
- Payroll workflow end-to-end
- Tip pooling rules (DEFAULT for 2+ servers)
- Tipout percentages (Utility 5%, Busser 4%, Expo 1%)
- Shift hours (DST-aware)
- Approval JSON schema

### 7. Pitch Deck (Context for Investor Demo)
**File:** `/Users/jonathanflaig/mise-core/docs/Mise_PitchDeck_v2.pdf`

**Contains:**
- Vision: "Virtual Executive Assistant for Hospitality"
- Problem: Disconnected systems, spoken data never captured
- Solution: Voice-first operational intelligence
- Competitive advantage
- Team
- Roadmap

---

## CORE ARCHITECTURE — QUICK REFERENCE

### The Mise Web App (Port 8000)

**What it is:**
- FastAPI-based web application
- Mobile-first, voice-driven interface
- **Center of gravity** — all user interactions flow through here

**Current workflows:**
- ✅ Payroll (live in production)
- 🔨 Inventory (in development)
- 📋 Scheduling, Ordering, Forecasting, Ops (planned)

**Dependencies:**
- Transrouter API (Port 8080) — REQUIRED
- Local storage (SQLite)
- LLM provider (Claude API via Transrouter)

**Key files:**
```
mise_app/
├── main.py                    # FastAPI app entry
├── config.py                  # ShiftyConfig, PayPeriod
├── local_storage.py           # Approval data storage
├── routes/
│   ├── home.py               # Dashboard
│   ├── recording.py          # Audio processing
│   └── totals.py             # Weekly totals
└── templates/                # Jinja2 HTML
```

### Transrouter API (Port 8080)

**What it is:**
- FastAPI-based API gateway
- Routes requests to domain-specific agents
- Handles audio transcription + AI interpretation

**Endpoints:**
- `GET /api/v1/health` — Health check
- `POST /api/v1/audio/process` — Upload audio → transcribe → parse → JSON
- `POST /api/v1/audio/transcribe` — Transcribe only
- `POST /api/v1/payroll/parse` — Parse transcript → approval JSON

**Authentication:** X-API-Key header

**Key files:**
```
transrouter/
├── api/
│   ├── main.py                         # FastAPI app
│   ├── auth.py                         # API key validation
│   └── routes/
│       ├── audio.py                    # Audio endpoints
│       └── payroll.py                  # Payroll endpoints
└── src/
    ├── transrouter_orchestrator.py    # Request routing
    ├── brain_sync.py                  # Load workflows/roster
    ├── claude_client.py               # LLM provider wrapper
    ├── asr_adapter.py                 # Whisper transcription
    └── agents/
        └── payroll_agent.py           # Payroll interpretation
```

### Architecture Diagram

```
┌─────────────────────────────────────────┐
│  MISE WEB APP (Port 8000)              │
│  - User Interface                       │
│  - Workflow Orchestration               │
└──────────────┬──────────────────────────┘
               │
               │ HTTP API
               ↓
┌─────────────────────────────────────────┐
│  TRANSROUTER (Port 8080)               │
│  - Domain Routing                       │
│  - Audio Transcription                  │
│  - AI Interpretation                    │
└──────────────┬──────────────────────────┘
               │
               ├──→ Payroll Agent (live)
               ├──→ Inventory Agent (planned)
               └──→ Other agents (planned)
```

---

## ENTERPRISE-GRADE ENGINEERING STANDARDS

**Every piece of code must be:**

1. **Enterprise-Grade** — Production-ready, not prototype quality
2. **Safe by Default** — Security and stability first
3. **Clean Architecture** — Clear separation of concerns
4. **Non-Duplicative** — Single source of truth
5. **Minimal Clutter** — Only what's necessary
6. **Predictable** — Local dev matches production
7. **Rollback-Ready** — Every deploy can be reverted
8. **Auditable** — Full logging and traceability

### Guardrails (Enforced)

**Code Standards:**
- Python: black (formatting), flake8 (linting), mypy (type checking), isort (imports)
- Type hints required for all new functions
- No `Any` types without justification

**CI/CD:**
- All checks must pass before merge to main
- Unit tests with >80% coverage
- Integration tests
- Security scans
- Dependency vulnerability checks

**Port Ownership:**
| Port | Service | Status |
|------|---------|--------|
| 8000 | mise_app | Active |
| 8080 | transrouter | Active |
| 5432 | PostgreSQL (dev only) | Dev only |

**NO other services bind to these ports.**

**File Ownership:**
| Path | Owner | Modify? |
|------|-------|---------|
| `mise_app/` | ccw2 (Frontend) | ✅ Yes |
| `transrouter/api/` | ccqb (Coordinator) | ⚠️ Notify first |
| `transrouter/src/agents/payroll_agent.py` | ccw3 (Payroll) | ✅ Yes |
| `workflow_specs/` | ccqb (Coordinator) | ❌ No (canonical) |
| `docs/brain/` | ccqb (Coordinator) | ❌ No (system truth) |
| `scripts/` | ccw6 (Infrastructure) | ✅ Yes |

**Anti-Clutter:**
- Single source of truth for all concepts
- No duplicate docs
- No commented-out code
- Delete unused imports immediately
- Archive or delete, never accumulate

---

## CRITICAL PITFALLS TO AVOID

### 1. Port 8080 Conflict

**Problem:** CPM Docker and Transrouter both try to use port 8080

**Symptom:** "Could not detect date/shift" errors in Mise Web App

**Fix:**
```bash
# Stop CPM Docker
cd payroll_agent/CPM && make down

# Verify clean state
./scripts/check-ports
```

**Prevention:** Always run `./scripts/check-ports` before starting work

### 2. Breaking Workflows

**Problem:** Modifying canonical workflow specs without coordination

**Symptom:** Payroll calculations wrong, tip pooling broken

**Prevention:**
- Workflows in `workflow_specs/` are canonical truth
- Do NOT modify without explicit instruction from Jon
- When in doubt, ask first

### 3. Ephemeral Learning

**Problem:** Saying "I'll remember this" without creating a brain file

**Symptom:** Knowledge lost between sessions, repeated questions

**Prevention:**
- ALL permanent knowledge goes in `docs/brain/` with `mmddyy__slug.md` naming
- Chat is transient, files are memory
- If it's not in a file, it doesn't exist

### 4. Duplicate Code/Docs

**Problem:** Creating redundant files or functionality

**Symptom:** Confusion about which is the "real" version

**Prevention:**
- Check for existing implementations before creating new ones
- Single source of truth locations defined (see MISE_STATE_COMPLETE.md §6)
- Delete aggressively

### 5. Starting Services in Wrong Order

**Problem:** Starting mise_app before transrouter

**Symptom:** mise_app fails to connect, timeout errors

**Prevention:**
```bash
# Correct order:
# 1. Start Transrouter (Port 8080)
# 2. Start Mise App (Port 8000)
# 3. Verify with ./scripts/check-ports
```

---

## HOW TO START WORKING (CHECKLIST)

### 1. Verify Environment

```bash
cd /Users/jonathanflaig/mise-core

# Check services are running
./scripts/check-ports

# Expected output:
# ✅ All services configured correctly!
# Active services:
#   - mise_app:    http://localhost:8000
#   - transrouter: http://localhost:8080
```

### 2. If Services Not Running

**Terminal 1 (Transrouter):**
```bash
cd /Users/jonathanflaig/mise-core
source .venv/bin/activate
export ANTHROPIC_API_KEY="sk-ant-api03-..."
export MISE_API_KEYS="mise-core:mise"
uvicorn transrouter.api.main:app --port 8080 --host 0.0.0.0 --reload
```

**Terminal 2 (Mise App):**
```bash
cd /Users/jonathanflaig/mise-core
source .venv/bin/activate
python -m mise_app.main
```

**Terminal 3 (Verification):**
```bash
cd /Users/jonathanflaig/mise-core
./scripts/check-ports
```

### 3. Understand Your Role

**Find your window assignment:**
- ccqb (Window #1): Coordinator & Transrouter
- ccw2 (Window #2): Frontend (mise_app)
- ccw3 (Window #3): Payroll Agent
- ccw4 (Window #4): Testing & QA
- ccw5 (Window #5): Demo Prep & Documentation
- ccw6 (Window #6): Backend & Infrastructure

**Work only on files you own** (see File Ownership matrix above)

### 4. Before Making Changes

**Check:**
- ✅ Is this file in my ownership domain?
- ✅ Am I following enterprise-grade standards?
- ✅ Is there a single source of truth I should update instead?
- ✅ Will this change affect other windows? (coordinate first)
- ✅ Do I have tests for this change?

### 5. After Making Changes

**Verify:**
```bash
# Run linters
black .
flake8 .
mypy .
isort .

# Run tests
pytest

# Verify services still work
./scripts/check-ports
curl http://localhost:8000/health
curl http://localhost:8080/api/v1/health

# Commit with clear message
git add <files>
git commit -m "Clear description of change"
```

---

## COMMON TASKS — QUICK REFERENCE

### Check System Health
```bash
./scripts/check-ports
```

### View Logs
```bash
tail -f logs/transrouter.log
tail -f logs/transcripts.log
```

### Test Audio Processing
```bash
curl -X POST http://localhost:8080/api/v1/audio/process \
  -H "X-API-Key: mise-core" \
  -F "file=@test.wav"
```

### Run Tests
```bash
pytest
pytest tests/test_payroll_agent.py  # Specific test
pytest -v  # Verbose
pytest --cov  # With coverage
```

### Update Dependencies
```bash
pip-compile requirements.in
pip install -r requirements.txt
```

### Create Brain Document
```bash
# Naming: mmddyy__slug.md
# Location: docs/brain/
# Example: docs/brain/011826__new-feature.md
```

---

## KEY METRICS & GOALS

### Investor Demo (45 hours away)

**Must work flawlessly:**
- ✅ Voice recording on mobile
- ✅ Audio upload and processing
- ✅ Auto-detection of day/shift
- ✅ Tip pooling calculations
- ✅ Shift approval workflow
- ✅ Weekly totals dashboard

**Demo flow:**
1. Jon records payroll shift on phone
2. Uploads to Mise Web App
3. Shows auto-detected shift data
4. Reviews and approves
5. Shows weekly totals updating
6. Shows Toast-ready output

### T1-T12 Milestones

- **T1:** Hire lead engineer, establish standards
- **T2:** Security hardening, infrastructure
- **T3:** Down Island onboarding (pilot #2)
- **T4:** First paying customer
- **T5-T6:** Scale to 5 restaurants (~$1.5K-$2K MRR)
- **T7-T8:** SOC 2 compliance prep
- **T9-T10:** Scale to 10 restaurants (~$3K-$4K MRR)
- **T11:** Inventory workflow launch
- **T12:** Jon full-time, 15-20 restaurants (~$6K-$8K MRR)

### Quality Standards

**Code:**
- 80%+ test coverage
- All type hints present
- No linting errors
- No security vulnerabilities

**Architecture:**
- Clear separation of concerns
- Single source of truth
- Predictable local dev environment
- Rollback-ready deployments

**Performance:**
- Health endpoints respond <100ms
- Audio processing <10 seconds
- Page load <2 seconds

---

## CANONICAL REFERENCES

**When you need to look something up:**

| Topic | File |
|-------|------|
| Complete system state | `/Users/jonathanflaig/mise-core/docs/MISE_STATE_COMPLETE.md` |
| Payroll rules | `/Users/jonathanflaig/mise-core/workflow_specs/LPM/LPM_Workflow_Master.txt` |
| System truth principles | `/Users/jonathanflaig/mise-core/docs/brain/121224__system-truth-how-mise-works.md` |
| Workflow primacy | `/Users/jonathanflaig/mise-core/docs/brain/121224__workflow-primacy-directive.md` |
| Service startup | `/Users/jonathanflaig/mise-core/START_MISE.md` |
| Port conflict history | `/Users/jonathanflaig/mise-core/PORT_CLEANUP_SUMMARY.md` |
| Employee roster | `/Users/jonathanflaig/mise-core/roster/employee_roster.json` |
| API schemas | `/Users/jonathanflaig/mise-core/transrouter/src/schemas.py` |

---

## CONFIRMATION — YOU ARE NOW SYNCHRONIZED

**After reading this document and the required files, you should be able to answer:**

1. ✅ What is Mise? (Voice-first virtual executive assistant for restaurants)
2. ✅ What's the investor demo deadline? (Tuesday Jan 20 @ 1PM, ~45 hours away)
3. ✅ What are the two main services? (mise_app:8000, transrouter:8080)
4. ✅ What was the port 8080 conflict? (CPM Docker vs Transrouter)
5. ✅ What's the fundraising ask? ($250K for 12-month runway)
6. ✅ What's your window role? (Check assignment above)
7. ✅ What files do you own? (Check ownership matrix)
8. ✅ How do you verify services are healthy? (`./scripts/check-ports`)
9. ✅ What's the tip pooling rule? (DEFAULT for 2+ servers)
10. ✅ Where does permanent knowledge go? (`docs/brain/` with mmddyy naming)

**If you can't answer these, re-read:**
- `docs/MISE_STATE_COMPLETE.md`
- This document

**If you can answer these, you are ready to work.**

---

## VERSION CONTROL

**This document version:** 2026-01-18 (Initial creation)

**Update triggers:**
- Major architecture changes
- New services added/removed
- Fundraising round completed
- Milestone achieved (T1, T2, etc.)
- Investor demo completed
- Critical bugs fixed that change workflows

**How to update this document:**
1. Create a new brain document with today's date: `mmddyy__swarm-update-pill.md`
2. Archive the old one: `mv docs/brain/011826__swarm-update-pill.md docs/brain/archive/`
3. Update references in other docs to point to new pill

**Last updated by:** ccqb (Window #1)
**Changelog:** Initial creation for 6-window swarm coordination

---

## FINAL INSTRUCTION

**When Jon says "take your swarm update pill":**

1. Read this document (docs/brain/011826__swarm-update-pill.md)
2. Read docs/MISE_STATE_COMPLETE.md
3. Read docs/brain/121224__system-truth-how-mise-works.md
4. Read docs/brain/121224__workflow-primacy-directive.md
5. Read START_MISE.md
6. Confirm services are running: `./scripts/check-ports`
7. Respond: "Swarm update pill ingested. Ready to work as [your window role]."

**You are now synchronized with the swarm and ready to build enterprise-grade Mise.**
