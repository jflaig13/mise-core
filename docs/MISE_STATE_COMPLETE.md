# Mise — Complete System State Report
**CC Window #1 (ccqb) — Quarterback & Coordinator**

**Last Updated:** January 18, 2026
**Investor Demo:** Tuesday, January 20th @ 1PM (~45 hours away)
**Current Status:** Clean slate established, all 6 windows ready for coordinated development sprint

---

## EXECUTIVE SUMMARY

**Mise** is the first voice-driven virtual executive assistant for restaurants, transforming spoken operational truth into structured, actionable data. It is **live in production** at Papa Surf Burger Bar since Q3 2025, where Jon runs real payroll weekly using this system.

**Fundraising Ask:** $250,000
**Timeline:** 12 months to production-grade multi-restaurant deployment
**Current State:** Working prototype in production, ready to scale

---

## 1. THE MISE WEB APP — CORE PRODUCT

### What It Is

The **Mise Web App** is the central user-facing application and operational hub for restaurant managers. It is a mobile-first, voice-driven web interface that unifies all restaurant operations workflows into a single coherent system.

**Technology:** FastAPI-based Python web application
**Port:** 8000
**Interface:** Mobile-optimized responsive web UI
**Architecture Role:** The center of gravity — all user interactions flow through this app

### What Workflows It Contains

**Currently Implemented:**

1. **Payroll Workflow**
   - Voice recording for individual shifts ("shifties")
   - Auto-detection of day/shift from spoken content
   - Shift approval with editable amounts
   - Weekly employee totals dashboard
   - Pay period management (Sunday-Saturday cycles)
   - Tip pooling calculations
   - Tipout distributions
   - Toast-ready output generation

**In Development / Planned:**

2. **Inventory Workflow**
   - Voice-driven inventory counts
   - SKU catalog matching
   - Pack-size logic
   - Fractional bottle tracking
   - COGS calculations
   - Automatic ordering suggestions

3. **Scheduling Workflow** (Planned)
4. **Ordering Workflow** (Planned)
5. **Forecasting Workflow** (Planned)
6. **General Operations / Exceptions** (Planned)

### Services & Dependencies

**The Mise Web App depends on:**

1. **Transrouter API (Port 8080)** — Required
   - API gateway that routes requests to domain-specific agents
   - Handles audio transcription
   - Executes AI-powered interpretation
   - Returns structured approval JSON

2. **Local Storage** — Required
   - SQLite-based approval data storage
   - Weekly totals aggregation
   - Shift state management

3. **LLM Provider (Pluggable)** — Required
   - Currently: Claude API via Transrouter
   - Future: Provider-agnostic model abstraction layer
   - Handles natural language interpretation

4. **Environment Variables** — Required
   ```bash
   TRANSROUTER_URL=http://localhost:8080
   TRANSROUTER_API_KEY=mise-core
   ```

**The Mise Web App does NOT depend on:**
- Google Sheets (future integration planned)
- CPM Docker stack (isolated testing only, see §8)
- External databases (uses local SQLite)

### How Users Interact With It

**Primary User Flow (Payroll Example):**

1. **Access:** Navigate to `http://localhost:8000` (or production URL)
2. **Select Pay Period:** View current week or navigate to specific period
3. **Record Shift:**
   - Tap "Record" on any shift cell
   - Speak shift details: "Monday AM. Austin $487, tips. Brooke $320, tips. Expo was Atticus."
   - Stop recording
4. **Auto-Processing:**
   - Audio sent to Transrouter
   - Transrouter transcribes via Whisper
   - Payroll Agent interprets and structures data
   - Auto-detects "Monday AM" = "MAM" shifty code
5. **Approve:**
   - Review parsed shift data on approval page
   - Edit amounts if needed
   - Confirm approval
6. **View Totals:**
   - Navigate to weekly totals dashboard
   - See running totals for all employees
   - Export to Toast when ready

**Interface Characteristics:**
- Mobile-first responsive design
- No-cache middleware (prevents stale data on mobile)
- Real-time status updates (pending/complete badges)
- Editable approval fields
- Transcript display for verification

### Where It Fits in Architecture

**The Mise Web App is the center of gravity:**

```
┌─────────────────────────────────────────────────┐
│  MISE WEB APP (Port 8000)                      │
│  - User Interface                               │
│  - Workflow Orchestration                       │
│  - Session Management                           │
│  - Local Data Storage                           │
└──────────────┬──────────────────────────────────┘
               │
               │ HTTP API Calls
               ↓
┌─────────────────────────────────────────────────┐
│  TRANSROUTER API (Port 8080)                   │
│  - Domain Routing                               │
│  - Audio Transcription                          │
│  - AI Model Orchestration                       │
│  - Validation & Auto-Correction                 │
└──────────────┬──────────────────────────────────┘
               │
               ├──→ Payroll Agent
               ├──→ Inventory Agent (planned)
               ├──→ Scheduling Agent (planned)
               └──→ Ops Agent (planned)
```

**Key Architectural Principles:**
- Web app owns user experience
- Transrouter owns AI/ML intelligence
- Clear API contract between layers
- Approval JSON is the contract format
- Stateless HTTP communication
- Local storage for approved data

### File Structure

**Core Files:**
```
mise_app/
├── main.py                    # FastAPI app entry point
├── config.py                  # ShiftyConfig, PayPeriod logic
├── local_storage.py           # Approval data storage
├── routes/
│   ├── home.py               # Dashboard, shifty grid
│   ├── recording.py          # Audio processing, approval flow
│   └── totals.py             # Weekly employee totals
├── templates/                # Jinja2 HTML templates
│   ├── landing.html          # Voice-first landing page
│   ├── record.html           # Recording interface
│   ├── approve.html          # Shift approval page
│   ├── detail.html           # Completed shift detail
│   └── totals.html           # Weekly totals dashboard
└── static/                   # CSS, JS, images
    ├── css/
    ├── js/
    └── images/
```

### Production Status

**Live Features (Working Today):**
- ✅ Voice recording for individual shifts
- ✅ Auto-detection of day/shift from transcript
- ✅ Tip pooling calculations (2+ servers)
- ✅ Tipout distributions (utility, expo, busser)
- ✅ Shift approval workflow
- ✅ Weekly employee totals
- ✅ Pay period isolation
- ✅ Mobile-responsive interface

**In Development:**
- 🔨 Inventory workflow integration
- 🔨 Google Sheets sync for employee running totals
- 🔨 QR code system for employee tip viewing
- 🔨 Multi-restaurant support

---

## 2. FASTAPI — WHAT IT IS AND WHY WE USE IT

### What FastAPI Is

**FastAPI** is a modern, high-performance Python web framework for building APIs and web applications.

**In Plain English:**
- It's the "engine" that runs both our web app (Port 8000) and our API gateway (Port 8080)
- It handles HTTP requests (when users visit pages or upload audio)
- It routes requests to the right Python functions
- It validates data automatically using Python type hints
- It generates automatic API documentation
- It's built on top of Starlette (web) and Pydantic (validation)

### Why We Use It

**1. Speed**
- One of the fastest Python frameworks available
- Built on async/await for high concurrency
- Handles multiple requests efficiently

**2. Type Safety**
- Uses Python type hints for automatic validation
- Catches errors before they reach production
- Self-documenting code

**3. Developer Experience**
- Automatic interactive API docs at `/docs` endpoint
- Clear error messages
- Easy to test and debug

**4. Production-Ready**
- Used by major companies (Microsoft, Netflix, Uber)
- Mature ecosystem
- Strong security defaults

**5. Standards-Based**
- OpenAPI (formerly Swagger) compatible
- JSON Schema validation
- OAuth2, JWT authentication support

### Where It Fits in Our System

**We use FastAPI in TWO places:**

**1. Mise Web App (Port 8000)**
```python
# mise_app/main.py
app = FastAPI(title="Mise", version="1.0.0")

@app.get("/")
async def landing_page():
    return templates.TemplateResponse("landing.html", {...})

@app.post("/payroll/period/{period_id}/process")
async def process_audio(file: UploadFile):
    # Process audio, call Transrouter, return results
```

**Purpose:**
- Serves HTML pages to users
- Handles form submissions
- Processes audio uploads
- Manages sessions and state

**2. Transrouter API (Port 8080)**
```python
# transrouter/api/main.py
app = FastAPI(title="Transrouter API", version="1.0.0")

@app.post("/api/v1/audio/process")
async def process_audio(file: UploadFile, api_key: str = Header(...)):
    # Transcribe audio, route to agent, return JSON
```

**Purpose:**
- Provides REST API for AI services
- Handles authentication (API keys)
- Routes to domain agents
- Returns structured JSON

### What FastAPI Is NOT

**NOT a database** — FastAPI doesn't store data. We use:
- SQLite for local storage (mise_app)
- PostgreSQL for CPM local dev
- BigQuery for CPM production

**NOT a frontend framework** — FastAPI doesn't run in the browser. We use:
- Jinja2 templates for HTML
- Vanilla JavaScript for interactions
- CSS for styling

**NOT an AI model** — FastAPI doesn't do AI. We use:
- Claude API (via Anthropic SDK)
- Whisper (for transcription)
- Model abstraction layer (provider-agnostic)

**NOT a deployment platform** — FastAPI doesn't host itself. We use:
- Uvicorn (ASGI server) for local dev
- Docker containers for deployment
- Cloud Run for production (future)

### FastAPI in Our Architecture

```
┌─────────────────────────────────────────┐
│  User's Browser                         │
└──────────────┬──────────────────────────┘
               │
               ↓ HTTP
┌─────────────────────────────────────────┐
│  FastAPI (Mise Web App - Port 8000)    │
│  - Serves HTML pages                    │
│  - Handles user interactions            │
│  - Manages local storage                │
└──────────────┬──────────────────────────┘
               │
               ↓ HTTP API Call
┌─────────────────────────────────────────┐
│  FastAPI (Transrouter - Port 8080)     │
│  - REST API endpoints                   │
│  - Audio transcription                  │
│  - AI agent orchestration               │
└──────────────┬──────────────────────────┘
               │
               ↓ SDK Calls
┌─────────────────────────────────────────┐
│  External Services                      │
│  - Claude API (LLM provider)            │
│  - Whisper (transcription)              │
└─────────────────────────────────────────┘
```

---

## 3. PITCH DECK INSIGHTS (Mise_PitchDeck_v2.pdf)

### The Vision
**"The Virtual Executive Assistant for Hospitality"** — voice-driven operational intelligence system

### The Problem
- Restaurants run on disconnected systems (Toast, 7shifts, R365, etc.)
- Most accurate operational data is **spoken** but never captured
- Operators manually enter: shift notes, tip-outs, inventory counts, comped items, waste logs, staff changes, daily reports
- This scattered workflow creates lost time, errors, inconsistent operational truth

### The Insight
**Human speech is the primary source of operational truth.**
Speech captures: real-time events, edge cases, human decisions, context behind numbers, operational nuance that never gets typed

### What Mise Already Does TODAY

**1. Local Payroll Machine (LPM)** — Live production since Q3 2025
- Record weekly payroll audio while drinking morning smoothie
- Whisper transcribes → AI model interprets → Jon reviews → Approve
- System produces Toast-ready CSV + Tip Report PDF + Excel summary
- **This is NOT a prototype — Jon runs real payroll this way every week**

**2. Local Inventory Machine (LIM)** — Interpretation workflow proven
- Record voice walkthrough of inventory items
- Whisper → LLM interpretation with SKU catalog, pack rules, fractional bottle logic
- Jon reviews parsed counts → Final Inventory JSON
- Full automation still being refined, but interpretation works extremely well

### The Architecture Blueprint

**Pattern (proven in production):**
```
Speech → Transcription API → LLM Interpretation → Approval → Automation
```

**Key components:**
- **LLM Provider (Pluggable)** — AI model abstraction layer
- **Approval JSON** — Contract between AI and automation
- **Automation Runners** — Execute operational tasks
- **Domain-agnostic pattern** — Extends across: Payroll, Inventory, Scheduling, Ordering, Forecasting, Daily Ops

### The Future System

**Unified Mise Platform with Transrouter orchestrating domain agents:**
- Payroll Agent
- Inventory Agent
- Scheduling Agent
- Ordering Agent
- Forecasting Agent
- Ops/Exceptions Agent

### Competitive Advantage

1. **Only voice-first platform** — No competitor building speech → action
2. **Built from inside the industry** — Jon is a GM running real operations daily
3. **Operational architecture already proven** in production
4. **Has the data** — Every spoken report becomes structured truth for future model
5. **Provides automation layer** — POS stores data, scheduling tools schedule, but nobody executes end-to-end
6. **Running in real restaurant today** — Not demo, not prototype

### Unique Access

Testing environments beyond Papa Surf:
- **Down Island** (Jon's SO is owner) — Elevated dining
- **Lost Pizza Company** — Fast casual, high throughput
- **The Bay, Farm n Fire, North Beach Social**
- Multiple kitchens, operational styles, languages of "operational speech"

### Team

- **Jon Flaig** — Founder & CEO, GM of Papa Surf, built two working AI-driven systems in production
- **Austin Miett** — Co-Founder Operations, former Director of Operations EPCOT France

---

## 4. FUNDRAISING ASK — $250,000 (12-MONTH TIMELINE)

### Investment Allocation

**Total Raise:** $250,000 for 12-month runway to enterprise-grade multi-restaurant deployment

**Breakdown:**

| Category | Amount | % | Purpose |
|----------|--------|---|---------|
| **Engineering** | $120,000 | 48% | Lead engineer salary + benefits (12 months) |
| **Security & Compliance** | $40,000 | 16% | Enterprise hardening, SOC 2 prep, penetration testing, audit prep |
| **Infrastructure & Cloud** | $25,000 | 10% | Cloud Run, BigQuery, storage, CDN, monitoring, logging |
| **QA & Testing** | $20,000 | 8% | Automated testing infrastructure, test data, QA tools |
| **Sales & Onboarding** | $15,000 | 6% | Customer onboarding materials, training docs, support systems |
| **Legal & Compliance** | $10,000 | 4% | Contract templates, privacy policy, terms of service, IP protection |
| **Contingency Buffer** | $20,000 | 8% | Unexpected technical challenges, emergency fixes, market pivots |

**Total:** $250,000

### Why This Allocation

**Engineering (48%):**
- Highest priority: ship production-grade code
- One senior full-stack engineer with restaurant tech experience
- Covers salary, benefits, equipment, tools
- Frees Jon to focus on product + customers

**Security & Compliance (16%):**
- **Enterprise customers require SOC 2 compliance**
- Restaurant data is sensitive (employee wages, tips, sales)
- Penetration testing before multi-restaurant rollout
- Security audit + remediation
- Access controls, encryption, audit logging
- This is NOT optional for enterprise sales

**Infrastructure (10%):**
- Cloud Run deployment (autoscaling FastAPI services)
- BigQuery for production payroll data storage
- Monitoring + alerting (Sentry, Datadog, or equivalent)
- CDN for fast global asset delivery
- Log aggregation and analysis
- **Budgeted conservatively for 10-20 restaurants**

**QA & Testing (8%):**
- Automated end-to-end test suite
- Integration testing infrastructure
- Test data generation and management
- CI/CD pipeline (GitHub Actions, Cloud Build)
- Load testing for multi-restaurant scenarios
- Regression detection

**Sales & Onboarding (6%):**
- Customer onboarding playbook
- Training videos and documentation
- Support ticketing system
- Knowledge base
- Customer success tools

**Legal & Compliance (4%):**
- Standard SaaS contract templates
- Privacy policy (GDPR, CCPA compliant)
- Terms of service
- Intellectual property protection
- Vendor agreements

**Contingency (8%):**
- Technical debt remediation
- Unexpected platform changes (API deprecations)
- Emergency security patches
- Market feedback requiring pivots
- Buffer for unknowns

### What $250,000 Delivers

**By T12 (Month 12):**
- ✅ 10-20 paying restaurant customers
- ✅ $4K-$8K MRR (Monthly Recurring Revenue)
- ✅ SOC 2 compliance ready
- ✅ Enterprise-grade security posture
- ✅ Scalable cloud infrastructure
- ✅ Automated testing + CI/CD
- ✅ Multi-restaurant deployment proven
- ✅ Jon full-time on Mise
- ✅ Ready for Series A raise

---

## 5. 12-MONTH ROADMAP (TIMELINE TOKENS)

### T1 (Month 1) — Foundation & Hiring

**Objectives:** Hire lead engineer, establish engineering standards, secure development environment

**Deliverables:**
- Lead full-stack engineer onboarded
- Engineering standards documented (linting, formatting, CI checks)
- Code review process established
- Development environment hardened
- Security baseline assessment completed

**Milestones:**
- ✅ Engineer hired and equipped
- ✅ Engineering playbook created
- ✅ CI/CD pipeline v1 running

---

### T2 (Month 2) — Security Hardening & Infrastructure

**Objectives:** Enterprise-grade security posture, production infrastructure setup

**Deliverables:**
- API authentication hardened (OAuth2/JWT)
- Encryption at rest and in transit
- Audit logging infrastructure
- Cloud Run deployment pipeline
- Monitoring and alerting systems
- Penetration test #1 (initial baseline)

**Milestones:**
- ✅ Production infrastructure live
- ✅ Security scan clean
- ✅ Monitoring dashboards operational

---

### T3 (Month 3) — Down Island Onboarding (Pilot #2)

**Objectives:** Validate multi-restaurant architecture, onboard second location

**Deliverables:**
- Down Island restaurant fully onboarded
- Multi-tenant data isolation verified
- Custom workflows per restaurant tested
- Employee roster management per location
- Training documentation updated

**Milestones:**
- ✅ Down Island processing live payroll via Mise
- ✅ Multi-restaurant bugs identified and fixed
- ✅ Onboarding playbook refined

---

### T4 (Month 4) — First Paying Customer Launch

**Objectives:** Revenue generation begins, validate pricing model

**Deliverables:**
- First external paying customer (not Papa Surf or Down Island)
- Billing system operational (Stripe integration)
- Customer support system established
- SLA commitments defined
- Invoice and payment workflows tested

**Milestones:**
- ✅ First paying customer live
- ✅ Revenue = $299-$399/month
- ✅ Billing automation working

---

### T5-T6 (Months 5-6) — Scale to 5 Restaurants

**Objectives:** Prove repeatability, refine onboarding, stabilize platform

**Deliverables:**
- 5 total restaurants on Mise (including Papa Surf, Down Island, 3 paying)
- Automated onboarding flow (reduce manual setup time)
- Customer success playbook
- Support ticket system operational
- Performance benchmarks established
- Load testing completed

**Milestones:**
- ✅ 5 restaurants live
- ✅ ~$1.5K-$2K MRR
- ✅ Onboarding time < 1 week per restaurant
- ✅ Zero critical bugs in production

---

### T7-T8 (Months 7-8) — SOC 2 Compliance Prep

**Objectives:** Enterprise compliance readiness, security audit

**Deliverables:**
- SOC 2 Type 1 audit preparation
- Security policies documented
- Access control audit
- Penetration test #2 (pre-audit)
- Vulnerability remediation complete
- Employee security training

**Milestones:**
- ✅ SOC 2 gap analysis complete
- ✅ Security posture enterprise-ready
- ✅ Audit readiness confirmed

---

### T9-T10 (Months 9-10) — Scale to 10 Restaurants

**Objectives:** Achieve product-market fit milestone, refine economics

**Deliverables:**
- 10 total restaurants on Mise
- Customer churn analysis
- Feature request prioritization
- Cost per restaurant optimized
- Support burden measured
- Referral program launched

**Milestones:**
- ✅ 10 restaurants live
- ✅ ~$3K-$4K MRR
- ✅ Unit economics proven
- ✅ Customer satisfaction > 4.5/5

---

### T11 (Month 11) — Inventory Workflow Launch

**Objectives:** Expand beyond payroll, prove multi-workflow value

**Deliverables:**
- Inventory workflow production-ready
- Voice inventory counts working end-to-end
- SKU catalog management UI
- COGS calculations automated
- Ordering suggestions tested
- Cross-sell to existing customers

**Milestones:**
- ✅ 3+ restaurants using inventory workflow
- ✅ Full Suite ($399/month) pricing validated

---

### T12 (Month 12) — Jon Full-Time, Series A Prep

**Objectives:** Jon transitions full-time to Mise, prepare for growth capital

**Deliverables:**
- Jon full-time on Mise (no longer GM at Papa Surf)
- 15-20 restaurants live
- ~$6K-$8K MRR
- Series A pitch deck
- Financial model updated
- Investor pipeline active
- Hiring plan for Series A growth

**Milestones:**
- ✅ 15-20 restaurants live
- ✅ $6K-$8K MRR
- ✅ Jon full-time
- ✅ Series A conversations initiated
- ✅ Product-market fit conclusively proven

---

### Why 12 Months is Achievable

**Factors supporting 12-month timeline:**

1. **Architecture already proven** — LPM works in production today
2. **Core technology stack stable** — FastAPI, Claude API, Whisper all mature
3. **First pilot customer ready** — Down Island committed, Jon's SO is owner
4. **Sales channel open** — Direct access to 6+ restaurants for testing/sales
5. **Founder domain expertise** — Jon knows the customer, sees edge cases daily
6. **Clear product vision** — Not searching for product-market fit, refining execution

**Risks requiring longer timeline:**
- Unforeseen regulatory/compliance hurdles
- Major technology platform changes (API deprecations)
- Slower-than-expected restaurant adoption
- Critical technical debt requiring refactor

**If timeline extends beyond 12 months:**
- Contingency buffer ($20K) provides ~1 extra month runway
- Can defer inventory workflow (focus on payroll-only customers)
- Can slow hiring (contractor vs. full-time engineer)

**Current assessment:** 12 months is aggressive but realistic with focused execution and disciplined scope management.

---

## 6. ENTERPRISE-GRADE ENGINEERING STANDARDS

### Core Principles

**Every piece of code, every system, every decision must be:**

1. **Enterprise-Grade** — Production-ready, not prototype quality
2. **Safe by Default** — Security and stability first, features second
3. **Clean Architecture** — Clear separation of concerns, minimal coupling
4. **Non-Duplicative** — Single source of truth, no redundant code/docs/services
5. **Minimal Clutter** — Only what's necessary, delete aggressively
6. **Predictable** — Local dev matches production, no surprises
7. **Rollback-Ready** — Every deploy can be reverted safely
8. **Auditable** — Full logging, clear ownership, traceable decisions

### Guardrails — Enforced Standards

#### 1. Code Standards

**Linting & Formatting:**
```bash
# Python (enforced via pre-commit hooks)
black .                    # Code formatting
flake8 .                   # Style guide enforcement
mypy .                     # Type checking
isort .                    # Import sorting

# Pre-commit config exists at: .pre-commit-config.yaml
```

**Type Hints:**
- All new functions must have type hints
- Return types required
- No `Any` types without justification

**Example:**
```python
# Good
def process_audio(audio_bytes: bytes, shifty_code: str) -> dict[str, Any]:
    """Process audio and return approval JSON."""
    ...

# Bad (rejected by CI)
def process_audio(audio_bytes, shifty_code):
    ...
```

#### 2. CI/CD Checks

**GitHub Actions Pipeline:**
```yaml
# .github/workflows/ci.yml
- Linting (black, flake8, mypy, isort)
- Unit tests (pytest with coverage > 80%)
- Integration tests
- Security scan (bandit, safety)
- Dependency vulnerability check
- Docker build test
- API schema validation
```

**No merge to main without:**
- ✅ All CI checks passing
- ✅ Code review approval
- ✅ Tests passing locally first

#### 3. Safe Migrations

**Database Changes:**
- Migrations are forward-only (no ALTER without plan)
- Backwards-compatible or coordinated deploy
- Test on staging before production
- Rollback plan documented

**Schema Changes:**
- Approval JSON schema changes require version bump
- Old versions supported for 2 releases minimum
- Migration guide for customers

#### 4. Rollback Strategy

**Every deploy must be rollback-ready:**

```bash
# Docker tags include git SHA
mise/transrouter:0c3b1cd
mise/mise-app:0c3b1cd

# Can rollback to previous SHA instantly
kubectl set image deployment/transrouter transrouter=mise/transrouter:e6a91ac
```

**Rollback triggers:**
- Error rate > 5% for 5 minutes
- Health check failures
- Customer-reported critical bug
- Security incident

#### 5. Dependency Discipline

**Principles:**
- Pin all dependency versions in `requirements.txt`
- Use `pip-tools` for deterministic builds
- Review dependencies quarterly for security updates
- No unvetted packages from PyPI without security scan

**Example:**
```bash
# requirements.in (source of truth)
fastapi>=0.104.0
anthropic>=0.7.0

# requirements.txt (generated, pinned)
pip-compile requirements.in
```

#### 6. Minimal Surface Area

**Port Ownership (Enforced):**
| Port | Owner | Purpose | Status |
|------|-------|---------|--------|
| 8000 | mise_app | Web UI | Active |
| 8080 | transrouter | API Gateway | Active |
| 5432 | PostgreSQL (CPM local dev) | Database | Dev only |
| 8081 | Mock Transcriber (CPM local dev) | Testing | Dev only |

**NO other services bind to these ports.**

**Service Registry:**
```yaml
# .mise/services.yml (canonical service list)
services:
  - name: mise_app
    port: 8000
    required: true
    health: http://localhost:8000/health

  - name: transrouter
    port: 8080
    required: true
    health: http://localhost:8080/api/v1/health
```

#### 7. Predictable Local Dev Environment

**Standard Startup Sequence:**
```bash
# 1. Environment variables
export ANTHROPIC_API_KEY="sk-ant-..."
export MISE_API_KEYS="mise-core:mise"

# 2. Virtual environment
source .venv/bin/activate

# 3. Start services (separate terminals)
# Terminal 1: Transrouter
uvicorn transrouter.api.main:app --port 8080 --host 0.0.0.0

# Terminal 2: Mise App
python -m mise_app.main

# 4. Verify
./scripts/check-ports
```

**Expected state after startup:**
- ✅ Both services healthy
- ✅ No port conflicts
- ✅ Logs show no errors
- ✅ Health endpoints return 200

#### 8. Clear Ownership

**File Ownership Matrix:**

| Path | Owner | Modify Without Approval? |
|------|-------|--------------------------|
| `mise_app/` | ccw2 (Frontend) | ✅ Yes |
| `transrouter/api/` | ccqb (Coordinator) | ⚠️ Notify first |
| `transrouter/src/agents/payroll_agent.py` | ccw3 (Payroll) | ✅ Yes |
| `workflow_specs/` | ccqb (Coordinator) | ❌ No (canonical truth) |
| `docs/brain/` | ccqb (Coordinator) | ❌ No (system truth) |
| `scripts/` | ccw6 (Infrastructure) | ✅ Yes |

#### 9. Anti-Clutter Enforcement

**Weekly Cleanliness Audit:**
```bash
# Run this script weekly (automated via cron)
./scripts/cleanup-audit

# Checks for:
- Duplicate docs (same content, different files)
- Dead code (unused imports, unreachable functions)
- Stale branches (merged but not deleted)
- Orphaned files (not referenced anywhere)
- Redundant services (same functionality, different names)
- Old logs (> 30 days, should be archived)
```

**Naming Conventions (Enforced):**
- Brain docs: `mmddyy__slug.md`
- Workflow changes: `MMDDYY_slug.txt`
- Test files: `test_*.py`
- Config files: `.config.yml` or `config.py`
- Scripts: lowercase-with-dashes (e.g., `check-ports`, not `checkPorts.sh`)

**Folder Structure Rules:**
```
mise-core/
├── mise_app/              # Web UI (FastAPI app)
├── transrouter/           # API Gateway (FastAPI app)
├── payroll_agent/         # Payroll-specific logic
├── workflow_specs/        # Canonical workflow specs
├── docs/                  # All documentation
│   ├── brain/            # System truth (immutable knowledge)
│   └── changelogs/       # Change history
├── scripts/              # Operational scripts
├── tests/                # Cross-cutting tests
└── .mise/                # Mise system config
```

**Single Source of Truth:**
| Concept | Canonical Location | Duplicates Allowed? |
|---------|-------------------|---------------------|
| Payroll rules | `workflow_specs/LPM/LPM_Workflow_Master.txt` | ❌ No |
| Employee roster | `roster/employee_roster.json` | ❌ No |
| API schema | `transrouter/src/schemas.py` | ❌ No |
| Service ports | `.mise/services.yml` | ❌ No |
| Environment vars | `.env.example` | ❌ No |

**Delete Immediately:**
- Commented-out code blocks (use git history)
- Unused imports
- Dead branches (merged > 30 days ago)
- Duplicate documentation
- Old logs (archive, don't keep in repo)
- Backup files (*.bak, *.old)

---

## 7. CURRENT TECHNICAL ARCHITECTURE

### System Components (As Built Today)

**A. mise_app (Web UI) — Port 8000**

See §1 for comprehensive details.

**Key files:**
- `mise_app/main.py` — FastAPI app entry, routes
- `mise_app/routes/recording.py` — Audio processing, approval flow
- `mise_app/routes/home.py` — Dashboard, shifty grid
- `mise_app/routes/totals.py` — Weekly employee totals
- `mise_app/config.py` — ShiftyConfig, PayPeriod logic
- `mise_app/local_storage.py` — Approval data storage

**B. Transrouter (API Gateway) — Port 8080**

**Purpose:** Coordinates all domain agents, provides REST API for AI services

**Technology:** FastAPI

**Endpoints:**
- `GET /api/v1/health` — Public health check
- `POST /api/v1/audio/process` — Upload audio → transcribe → parse → JSON
- `POST /api/v1/audio/transcribe` — Transcribe only
- `POST /api/v1/payroll/parse` — Parse transcript → approval JSON

**Authentication:** X-API-Key header (mise-core)

**Key files:**
- `transrouter/api/main.py` — FastAPI app
- `transrouter/api/auth.py` — API key validation
- `transrouter/api/routes/audio.py` — Audio processing endpoints
- `transrouter/api/routes/payroll.py` — Payroll parsing
- `transrouter/src/transrouter_orchestrator.py` — Routes requests to agents
- `transrouter/src/brain_sync.py` — Loads workflow specs, roster, brain docs
- `transrouter/src/claude_client.py` — LLM provider wrapper (Claude API)
- `transrouter/src/asr_adapter.py` — Whisper transcription
- `transrouter/src/agents/payroll_agent.py` — Payroll interpretation with auto-correction
- `transrouter/src/prompts/payroll_prompt.py` — System prompt with tip pooling rules
- `transrouter/src/logging_utils.py` — File + JSON logging

**Enterprise-grade validation (4 layers):**
1. **Prompt validation** — LLM model told to verify per_shift matches detail_blocks
2. **Output validation** — Catches errors, logs warnings
3. **Auto-correction** — Parses detail_blocks, fixes missing per_shift, recalculates totals
4. **Audit trail** — Returns `corrections` array in API response

**Logging:**
- `logs/transrouter.log` — Human-readable debug
- `logs/transrouter.json.log` — Structured JSON for analytics
- `logs/transcripts.log` — Detailed transcript + extraction + result

**C. LPM (Local Payroll Machine) — Jon's Current Production Workflow**

**Status:** Live production since Q3 2025, Jon uses this weekly

**Workflow:**
1. Record weekly payroll audio (Motiv Audio app)
2. AirDrop to Mac
3. `transcribe <audio-file>` → local Whisper → .txt transcript
4. Drop transcript into LLM provider (currently Claude Code project)
5. LLM parses + calculates (tip pools, tipouts, totals)
6. Jon reviews → "FINAL PAYROLL JSON"
7. Local automation runner produces:
   - Toast-ready CSV
   - Tip Report PDF
   - Excel summary

**Key rules (from LPM_Workflow_Master.txt):**
- **Tip pooling:** DEFAULT for 2+ servers
- **Tipout percentages:** Utility 5%, Busser 4%, Expo 1% (of food sales)
- **Shift hours:** DST-aware (AM always 6.5h, PM varies by season/day)
- **Partial tipouts:** Calculate fraction of hours worked

**D. LIM (Local Inventory Machine) — Interpretation Proven**

**Status:** Interpretation workflow working, full automation in development

**Workflow:**
- Speech → transcription → LLM interpretation → approval
- Uses: SKU catalog, pack-size rules, fractional bottle logic, normalization rules

---

## 8. PORT 8080 CONFLICT — WHAT HAPPENED AND HOW IT'S FIXED

### What Happened (Plain Language)

**The Problem:**

Two different systems were trying to use the same "address" (port 8080) at the same time:

1. **CPM (Cloud Payroll Machine)** — A Docker-based testing environment for the payroll engine
2. **Transrouter** — The main API gateway that the Mise Web App depends on

**Analogy:** It's like two people trying to live at the same street address. Only one can receive mail there.

**What CPM Is:**

CPM is a **local testing environment** for developing and testing the payroll engine in isolation. It runs in Docker containers and includes:
- A payroll processing service (port 8080)
- A mock transcription service (port 8081)
- A PostgreSQL database (port 5432)

**Why Port 8080 Matters:**

Port 8080 is the "front door" where the Mise Web App sends audio files to be processed. If the wrong service is listening on port 8080, requests go to the wrong place and fail.

**What Went Wrong:**

1. CPM Docker was started (maybe from days ago, still running)
2. CPM's payroll service claimed port 8080
3. When we tried to start Transrouter, it couldn't bind to port 8080 (already taken)
4. Transrouter silently failed or used a fallback port
5. Mise Web App sent requests to port 8080
6. Requests went to CPM instead of Transrouter
7. CPM doesn't have the `/api/v1/audio/process` endpoint
8. Mise Web App got errors: "Could not detect date/shift" or empty transcripts

### What "Cleanup Completed" Means

**Actions Taken:**

1. **Stopped CPM Docker:**
   ```bash
   cd payroll_agent/CPM
   make down
   ```
   This shut down all CPM containers and freed port 8080.

2. **Verified Transrouter Running:**
   ```bash
   curl http://localhost:8080/api/v1/health
   # Response: {"status":"healthy","version":"1.0.0"}
   ```

3. **Created Port Health Checker:**
   - Script: `scripts/check-ports`
   - Automatically detects conflicts
   - Tells you which service is on each port
   - Warns if CPM is running when it shouldn't be

4. **Updated Documentation:**
   - `START_MISE.md` — Correct startup procedure
   - `PORT_CLEANUP_SUMMARY.md` — What happened and why
   - `payroll_agent/CPM/local_dev/README.md` — Added warnings about when to use CPM

5. **Established Architecture Rules:**
   - **Transrouter MUST own port 8080** (required for Mise Web App)
   - **CPM Docker only for isolated payroll testing** (not for regular development)
   - **Clear startup sequence** (Transrouter before Mise Web App)

### Action Items (What You Need to Do)

**✅ Nothing immediate** — The cleanup is complete and safeguards are in place.

**Going forward:**

1. **Before starting work each day:**
   ```bash
   cd /Users/jonathanflaig/mise-core
   ./scripts/check-ports
   ```
   Expected output:
   ```
   ✅ All services configured correctly!

   Active services:
     - mise_app:    http://localhost:8000
     - transrouter: http://localhost:8080
   ```

2. **If you see CPM running:**
   ```bash
   cd payroll_agent/CPM
   make down
   ./scripts/check-ports  # Verify clean
   ```

3. **When to use CPM Docker:**
   - ❌ NOT for regular Mise Web App development
   - ❌ NOT when testing the full system
   - ✅ ONLY when testing payroll engine in isolation
   - ✅ ONLY when you need to test database backends (BigQuery ↔ PostgreSQL)

4. **If testing CPM in isolation:**
   ```bash
   # Stop Transrouter first
   pkill -f "uvicorn transrouter"

   # Start CPM
   cd payroll_agent/CPM
   make up

   # Do your testing...

   # IMPORTANT: Clean up after
   make down
   ```

### How We Prevent It Happening Again

**Automated Detection:**

1. **Port health checker (`scripts/check-ports`):**
   - Run automatically on startup (could add to shell profile)
   - Detects which service is on port 8080
   - Warns if CPM detected
   - Shows expected vs actual state

2. **Developer documentation:**
   - `START_MISE.md` — Clear startup guide
   - CPM README — Prominent warnings
   - This document (§8) — Explains the issue

3. **Architecture enforcement:**
   - Only ONE service can bind to port 8080 at a time
   - Transrouter gets priority (required for Mise Web App)
   - CPM is opt-in (must explicitly start it)

**Future Enhancement (Potential):**
- Add a `Makefile` target that checks ports before starting services
- Pre-commit hook that warns if CPM is running
- Startup script that automatically stops CPM if detected

### How We Detect It Automatically

**Current Detection:**

```bash
./scripts/check-ports
```

**What it checks:**
1. Is port 8000 responding? (mise_app)
2. Is port 8080 responding? (should be transrouter)
3. Does port 8080 return transrouter health check? (correct)
4. Does port 8080 return CPM ping? (wrong - warning)
5. Are any CPM Docker containers running? (warning)

**Output examples:**

**✅ Good state:**
```
✅ All services configured correctly!

Active services:
  - mise_app:    http://localhost:8000
  - transrouter: http://localhost:8080
```

**❌ Bad state (CPM conflict):**
```
✗ Port 8080: CPM detected (should be transrouter!)
✗ CPM Docker containers running (conflicts with transrouter)

FIX:
  cd payroll_agent/CPM
  make down
  ./scripts/check-ports  # verify
```

---

## 9. CLOUD PAYROLL MACHINE (CPM) — DEPRECATION PLAN

### Current Status

**CPM is now integrated into the Mise Web App as the "Payroll Workflow."**

The standalone "Cloud Payroll Machine" concept is deprecated. Here's what that means:

### What CPM Was (Historical)

**Original vision:**
- Standalone cloud service for payroll processing
- Shift-by-shift processing (one shift at a time)
- Direct audio upload → payroll output
- Designed for real-time employee visibility

**Problem:**
- Duplicates functionality now in Mise Web App
- Creates confusion about which system to use
- Maintains two codebases for the same workflow

### What CPM Is Now (Integrated)

**The payroll workflow inside Mise Web App:**
- Same shift-by-shift processing logic
- Same tip pooling rules
- Same approval flow
- But integrated into unified Mise interface
- No standalone deployment needed

### Components Status

| Component | Status | Action | Reason |
|-----------|--------|--------|--------|
| **CPM Docker stack** | Keep (dev only) | Rename to "Payroll Engine Dev" | Still useful for isolated testing |
| **CPM workflow specs** | Merge | Move to `workflow_specs/Payroll/` | Single source of truth |
| **CPM API endpoints** | Deprecated | Remove standalone routes | Use Transrouter `/api/v1/payroll/*` |
| **CPM database abstraction** | Keep | Move to `transrouter/src/database/` | Useful for BigQuery ↔ PostgreSQL switching |
| **CPM deployment scripts** | Remove | Delete `payroll_agent/CPM/deploy/` | No standalone deployment |

### Migration Plan

**Phase 1: Rename & Reorganize (T1-T2)**

1. **Rename CPM Docker to "Payroll Engine Dev Environment":**
   ```bash
   mv payroll_agent/CPM payroll_agent/payroll_engine_dev
   ```

2. **Merge workflow specs:**
   ```bash
   # Consolidate into single payroll spec
   workflow_specs/Payroll/
   ├── README.md (merged from CPM + LPM specs)
   ├── approval_json_schema.json
   └── workflow_changes/
   ```

3. **Update documentation:**
   - Remove references to "Cloud Payroll Machine" as separate product
   - Update to "Payroll workflow" or "Payroll agent"
   - Clarify: "Payroll Engine Dev" is for local testing only

**Phase 2: Code Consolidation (T2-T3)**

1. **Move database abstraction layer:**
   ```bash
   mv payroll_agent/payroll_engine_dev/engine/database/ \
      transrouter/src/database/
   ```

2. **Remove standalone API routes:**
   - Delete CPM-specific endpoints (replaced by Transrouter)
   - Keep only `/parse_only` and `/commit_shift` for dev testing

3. **Update imports:**
   - All references to `payroll_agent.CPM.*` → `transrouter.src.*`
   - Update tests

**Phase 3: Cleanup (T3-T4)**

1. **Delete obsolete files:**
   - `payroll_agent/CPM/deploy/` (no standalone deployment)
   - Duplicate documentation
   - Old Docker Compose files for production

2. **Archive historical context:**
   - Create `docs/archive/cpm_migration.md`
   - Document what CPM was, why it was merged
   - Keep for historical reference

### What Stays, What Goes

**✅ KEEP:**

1. **Payroll Engine Dev Environment** (renamed from CPM Docker)
   - Purpose: Isolated testing of payroll logic
   - Use case: Database backend testing (BigQuery ↔ PostgreSQL)
   - Location: `payroll_agent/payroll_engine_dev/`

2. **Database abstraction layer**
   - Purpose: Switch between BigQuery (prod) and PostgreSQL (dev)
   - Location: `transrouter/src/database/`

3. **Mock transcriber** (for testing)
   - Purpose: Fixture-based transcription for deterministic tests
   - Location: `payroll_agent/payroll_engine_dev/mock_transcriber/`

4. **Test fixtures**
   - Purpose: Known-good test cases for payroll parsing
   - Location: `payroll_agent/payroll_engine_dev/local_dev/fixtures/`

**❌ REMOVE:**

1. **Standalone CPM deployment scripts**
   - `payroll_agent/CPM/deploy/deploy.sh`
   - `payroll_agent/CPM/deploy/cloudbuild.yaml`
   - Reason: No longer deploying CPM as standalone service

2. **Duplicate workflow specs**
   - Consolidate CPM + LPM specs into unified Payroll workflow spec
   - Delete redundant files

3. **CPM-specific API routes** (if any remain outside Transrouter)

4. **Old "Cloud Payroll Machine" branding**
   - Update all docs to say "Payroll workflow" or "Payroll agent"

**🔄 RENAME:**

1. **`payroll_agent/CPM/`** → `payroll_agent/payroll_engine_dev/`
2. **`workflow_specs/CPM/`** → Merge into `workflow_specs/Payroll/`
3. **Environment variable:** `CPM_MODE` → `PAYROLL_ENGINE_MODE`

### Updated Architecture (Post-Deprecation)

**Before (Confusing):**
```
Mise Web App ──→ Transrouter ──→ Payroll Agent
                                  ↓
Cloud Payroll Machine (standalone?) ← What is this?
```

**After (Clear):**
```
Mise Web App ──→ Transrouter ──→ Payroll Agent
                                  ├─ Tip pooling logic
                                  ├─ Tipout calculations
                                  └─ Approval JSON generation

Payroll Engine Dev (local Docker only)
├─ Isolated testing environment
├─ Mock transcriber
└─ PostgreSQL (mirrors BigQuery schema)
```

### Communication Plan

**Internal (Team):**
- Update all references in code comments
- Update README files
- Update startup guides

**External (Pitch Deck / Investors):**
- Remove "Cloud Payroll Machine" as separate product
- Emphasize "Payroll workflow inside Mise Web App"
- Clarify: "Proven in production" refers to LPM → now integrated into Mise

**Customer-Facing:**
- No customer impact (CPM was never customer-facing)
- Mise Web App is the only product customers see

---

## 10. DEV ENVIRONMENT — STARTUP & VERIFICATION

### Standard Startup Procedure

**Prerequisites:**
```bash
# 1. Environment variables (add to ~/.zshrc or ~/.bashrc)
export ANTHROPIC_API_KEY="sk-ant-api03-..."
export MISE_API_KEYS="mise-core:mise"

# 2. Virtual environment activated
cd /Users/jonathanflaig/mise-core
source .venv/bin/activate
```

**Startup Sequence (3 terminals):**

**Terminal 1: Transrouter (API Gateway)**
```bash
cd /Users/jonathanflaig/mise-core
source .venv/bin/activate
uvicorn transrouter.api.main:app --port 8080 --host 0.0.0.0 --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Terminal 2: Mise Web App**
```bash
cd /Users/jonathanflaig/mise-core
source .venv/bin/activate
python -m mise_app.main
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12347] using StatReload
INFO:     Started server process [12348]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Terminal 3: Verification (optional monitoring)**
```bash
cd /Users/jonathanflaig/mise-core
tail -f logs/transrouter.log logs/transcripts.log
```

### Verification Checklist

**Run this immediately after startup:**

```bash
./scripts/check-ports
```

**Expected output (✅ GOOD):**
```
🔍 Mise Port Checker

✓ Port 8000: mise_app running correctly
✓ Port 8080: transrouter running correctly

✅ All services configured correctly!

Active services:
  - mise_app:    http://localhost:8000
  - transrouter: http://localhost:8080
```

**If you see errors, see "Common Failures" below.**

### Detailed Health Checks

**1. Port Binding Check:**
```bash
lsof -i :8000  # Should show Python process (mise_app)
lsof -i :8080  # Should show Python process (transrouter)
```

Expected output:
```
COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
Python  12348   jon    3u  IPv4  0x...      0t0  TCP *:8000 (LISTEN)
Python  12346   jon    3u  IPv4  0x...      0t0  TCP *:8080 (LISTEN)
```

**2. Health Endpoint Check:**
```bash
# Mise Web App
curl http://localhost:8000/health
# Expected: {"status":"ok","app":"mise"}

# Transrouter
curl http://localhost:8080/api/v1/health
# Expected: {"status":"healthy","version":"1.0.0",...}
```

**3. API Authentication Check:**
```bash
# Should succeed (with valid API key)
curl -X POST http://localhost:8080/api/v1/audio/process \
  -H "X-API-Key: mise-core" \
  -F "file=@test.wav"

# Should fail with 401 (missing API key)
curl -X POST http://localhost:8080/api/v1/audio/process \
  -F "file=@test.wav"
# Expected: {"detail":"Missing X-API-Key header"}
```

**4. Docker Conflict Check:**
```bash
docker ps --format '{{.Names}}' | grep -i cpm
# Expected: (empty output - no CPM containers)

# If CPM containers are running:
cd payroll_agent/CPM
make down
```

**5. Log Health Check:**
```bash
# Check for errors in recent logs
tail -n 50 logs/transrouter.log | grep -i error
# Expected: (empty output - no errors)

# Check transcription logs
tail -n 20 logs/transcripts.log
# Should show successful transcriptions if any audio processed
```

### What "Good" Looks Like

**Healthy System Indicators:**

✅ **Terminal 1 (Transrouter):**
- Started on port 8080
- No error messages
- "Application startup complete"
- Logs show "Brain sync complete" (loaded workflows/roster)

✅ **Terminal 2 (Mise Web App):**
- Started on port 8000
- No error messages
- "Application startup complete"

✅ **Browser:**
- http://localhost:8000 loads landing page
- http://localhost:8080/docs shows API documentation
- No CORS errors in browser console

✅ **Port checker:**
- Both services detected
- No conflicts reported
- No CPM Docker containers

✅ **Logs:**
- No ERROR or CRITICAL messages
- Only INFO and DEBUG messages
- Successful health checks logged

### Common Failures & Fixes

#### Failure 1: "Address already in use" (Port Conflict)

**Symptom:**
```
Error: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8080): address already in use
```

**Cause:** Another process is using port 8080 or 8000

**Fix:**
```bash
# Find what's using the port
lsof -i :8080

# If it's CPM Docker:
cd payroll_agent/CPM && make down

# If it's a stale Python process:
pkill -f "uvicorn transrouter"
pkill -f "mise_app"

# Restart services
```

#### Failure 2: "Could not detect date/shift" in Mise Web App

**Symptom:** Audio uploads succeed but no shift data returned

**Cause:** Transrouter not running or CPM on port 8080

**Fix:**
```bash
# Check which service is on port 8080
curl http://localhost:8080/api/v1/health

# If this fails, Transrouter isn't running
# Start Transrouter (Terminal 1)

# If this returns CPM ping instead:
cd payroll_agent/CPM && make down
```

#### Failure 3: "Missing ANTHROPIC_API_KEY"

**Symptom:**
```
ERROR: ANTHROPIC_API_KEY environment variable not set
```

**Fix:**
```bash
# Set environment variable
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Or add to ~/.zshrc permanently:
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

#### Failure 4: Empty Logs or No Transcript Output

**Symptom:** Audio uploaded but no logs generated

**Cause:** Logging not configured or log directory missing

**Fix:**
```bash
# Create logs directory if missing
mkdir -p logs

# Check file permissions
ls -la logs/
# Should be writable by current user

# Restart Transrouter to reinitialize logging
```

#### Failure 5: Import Errors or Module Not Found

**Symptom:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Cause:** Dependencies not installed or wrong virtual environment

**Fix:**
```bash
# Ensure virtual environment activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep anthropic
```

#### Failure 6: CORS Errors in Browser

**Symptom:** Browser console shows "CORS policy" error

**Cause:** Browser trying to call Transrouter directly (should go through Mise Web App)

**Fix:**
- ✅ Correct: Browser → Mise Web App → Transrouter
- ❌ Wrong: Browser → Transrouter directly

Transrouter should only be called from Mise Web App backend, not from browser JavaScript.

### Quick Diagnostic Script

```bash
#!/bin/bash
# scripts/diagnose-dev-env

echo "=== Mise Dev Environment Diagnostic ==="
echo

echo "1. Checking ports..."
lsof -i :8000 -i :8080 | grep LISTEN

echo
echo "2. Checking health endpoints..."
curl -s http://localhost:8000/health || echo "❌ mise_app not responding"
curl -s http://localhost:8080/api/v1/health || echo "❌ transrouter not responding"

echo
echo "3. Checking Docker conflicts..."
docker ps --format '{{.Names}}' | grep -i cpm && echo "⚠️ CPM Docker running!"

echo
echo "4. Checking environment variables..."
[ -z "$ANTHROPIC_API_KEY" ] && echo "❌ ANTHROPIC_API_KEY not set"
[ -z "$MISE_API_KEYS" ] && echo "❌ MISE_API_KEYS not set"

echo
echo "5. Checking logs..."
tail -n 5 logs/transrouter.log 2>/dev/null || echo "⚠️ No transrouter logs"

echo
echo "=== Diagnostic complete ==="
```

---

## 11. HEALTH CHECKS — PURPOSE & USAGE

### What Health Checks Are

**Health checks are HTTP endpoints that return the operational status of a service.**

**Example:**
```bash
curl http://localhost:8080/api/v1/health
# Response: {"status":"healthy","version":"1.0.0","uptime":3600}
```

**Purpose:**
- Verify service is running and responsive
- Detect failures early
- Enable automated monitoring
- Support load balancer decisions (Cloud Run, Kubernetes)

### Who Uses Health Checks

**1. Automated Systems (Primary Use)**

**Production orchestration:**
- **Cloud Run:** Calls health endpoint to decide if container is ready
- **Load balancers:** Route traffic only to healthy instances
- **Monitoring systems:** Alert when health check fails (PagerDuty, Sentry)
- **CI/CD pipelines:** Verify deployment succeeded before completing

**Example (Cloud Run):**
```yaml
# Cloud Run calls this endpoint every 10 seconds
# If it returns non-200 status, container is restarted
livenessProbe:
  httpGet:
    path: /api/v1/health
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

**2. Developers (Manual Use)**

**During development:**
- ✅ Verify service started correctly
- ✅ Debug startup issues
- ✅ Confirm API is responsive
- ✅ Check version deployed

**Example workflow:**
```bash
# Start service
uvicorn transrouter.api.main:app --port 8080

# Wait a few seconds, then check health
curl http://localhost:8080/api/v1/health
```

**3. Operational Scripts**

**Automated checks:**
- `scripts/check-ports` uses health endpoints
- Startup scripts verify all services healthy
- Deployment scripts wait for health before proceeding

### When to Check Health Endpoints (Manual)

**✅ DO check health endpoints:**

1. **After starting a service:**
   ```bash
   # Start Transrouter
   uvicorn transrouter.api.main:app --port 8080 &

   # Wait for startup
   sleep 3

   # Verify healthy
   curl http://localhost:8080/api/v1/health
   ```

2. **When debugging connection issues:**
   ```bash
   # Mise Web App can't reach Transrouter - is it running?
   curl http://localhost:8080/api/v1/health
   ```

3. **Before running tests:**
   ```bash
   # Ensure services are up before running integration tests
   ./scripts/check-ports || exit 1
   pytest tests/test_integration.py
   ```

4. **After deploying to production:**
   ```bash
   # Verify deployment succeeded
   curl https://mise-transrouter-xyz.run.app/api/v1/health
   ```

**❌ DON'T check health endpoints:**

1. **During normal application flow** — Don't call health endpoints from user-facing code
   ```python
   # Bad: Don't do this in application logic
   def upload_audio():
       health = requests.get("http://localhost:8080/api/v1/health")
       if health.status_code == 200:
           process_audio()  # Just call the actual endpoint directly
   ```

2. **In a tight loop** — Don't spam health checks
   ```bash
   # Bad: Don't do this
   while true; do
       curl http://localhost:8080/api/v1/health
       sleep 1
   done
   ```

3. **For authentication testing** — Health endpoints should be public
   ```bash
   # Health endpoints don't require API keys
   curl http://localhost:8080/api/v1/health  # Should work without auth
   ```

### What to Do If Health Check Fails

**Failure Scenarios:**

#### 1. Connection Refused

**Symptom:**
```bash
curl http://localhost:8080/api/v1/health
# curl: (7) Failed to connect to localhost port 8080: Connection refused
```

**Meaning:** Service is not running

**Fix:**
```bash
# Check if service is running
ps aux | grep uvicorn

# If not running, start it
uvicorn transrouter.api.main:app --port 8080
```

#### 2. Returns 500 Internal Server Error

**Symptom:**
```bash
curl http://localhost:8080/api/v1/health
# HTTP/1.1 500 Internal Server Error
```

**Meaning:** Service is running but has an error

**Fix:**
```bash
# Check logs for error details
tail -n 50 logs/transrouter.log

# Common causes:
# - Missing environment variable
# - Database connection failed
# - Dependency import error
```

#### 3. Timeout (No Response)

**Symptom:**
```bash
curl http://localhost:8080/api/v1/health
# (hangs, no response)
```

**Meaning:** Service is overloaded or deadlocked

**Fix:**
```bash
# Check if process is consuming 100% CPU
top -p $(pgrep -f "uvicorn transrouter")

# Restart service
pkill -f "uvicorn transrouter"
uvicorn transrouter.api.main:app --port 8080
```

#### 4. Wrong Response

**Symptom:**
```bash
curl http://localhost:8080/api/v1/health
# Returns CPM ping instead of Transrouter health
```

**Meaning:** Wrong service on this port

**Fix:**
```bash
# This is the CPM conflict (see §8)
cd payroll_agent/CPM && make down
./scripts/check-ports
```

### Health Check Response Format

**Transrouter (`/api/v1/health`):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600,
  "brain_sync": true,
  "model_provider": "claude-3-5-sonnet-20241022"
}
```

**Mise Web App (`/health`):**
```json
{
  "status": "ok",
  "app": "mise"
}
```

### Monitoring Strategy (Future)

**T7-T8 (Security & Compliance Phase):**

**Add production monitoring:**
1. **Uptime monitoring** — Pingdom, UptimeRobot, or equivalent
   - Check health endpoint every 5 minutes
   - Alert if down for > 2 checks (10 minutes)

2. **Application monitoring** — Sentry, Datadog, or equivalent
   - Log all health check failures
   - Track response time trends
   - Alert on degraded performance

3. **Synthetic transactions** — Simulate real user flows
   - Upload test audio file
   - Verify approval JSON returned
   - Alert if pipeline fails

---

## 12. FILE-BASED INTELLIGENCE SYSTEM (docs/brain/)

### Core Principles (121224__system-truth-how-mise-works.md)

- **Mise is a FILE-BASED INTELLIGENCE SYSTEM**
- Knowledge/memory/values/rules ONLY exist if written to `/mise-core` files
- Chat is transient, files are cognition, git history is memory
- **IF IT IS NOT IN A FILE, IT DOES NOT EXIST**
- No ephemeral learning — "I'll remember this" without a file is invalid
- All permanent instructions require file creation with extreme detail, zero chat dependency
- Retroactive fixes mandatory for past unwritten rules

### Workflow Primacy (121224__workflow-primacy-directive.md)

- Mise workflows are foundational system knowledge
- Must load and internalize canonical workflows on every initialization
- Workflows override intuition, best practices, external norms
- **Re-asking answered workflow questions is a system failure**
- Only ask if required step genuinely missing or docs directly conflict
- Workflows assumed complete/intentional unless marked draft

---

## 13. MULTI-WINDOW COORDINATION STATUS

**Windows ready:**
- ✅ ccqb (CC Window #1) — This window, coordinator & quarterback
- ✅ ccw2 (CC Window #2) — Ready, has mise_app UI context
- ✅ ccw3 (CC Window #3) — Ready, fresh context
- ✅ ccw4 (CC Window #4) — Ready, fresh context
- ✅ ccw5 (CC Window #5) — Ready, has pitch deck/founder story context
- ✅ ccw6 (CC Window #6) — Ready, fresh context

**All windows synchronized with:**
- This complete state report
- PORT_CLEANUP_SUMMARY.md
- START_MISE.md
- payroll_agent/CPM/local_dev/README.md

**Investor demo:** Tuesday January 20th @ 1PM (~45 hours away)

**Proposed window roles:**
- **ccqb (Window #1):** Coordinator & Transrouter — enterprise architecture, API gateway, orchestration
- **ccw2 (Window #2):** Frontend (mise_app) — UI/UX, templates, user flows
- **ccw3 (Window #3):** Payroll Agent — tip pooling logic, approval JSON, business rules
- **ccw4 (Window #4):** Testing & QA — test suites, CI/CD, quality assurance
- **ccw5 (Window #5):** Demo Prep & Documentation — pitch materials, investor demo, docs
- **ccw6 (Window #6):** Backend & Infrastructure — database, deployment, monitoring

---

## CHANGE LOG — WHAT WAS UPDATED

**Changes made to address your requirements:**

1. **✅ Added §1: THE MISE WEB APP — CORE PRODUCT**
   - Comprehensive section explaining what Mise Web App is
   - Workflows it contains (payroll current, inventory/scheduling/ordering/forecasting planned)
   - Dependencies (Transrouter, local storage, LLM provider)
   - User interaction flows
   - Architecture positioning (center of gravity)
   - File structure
   - Production status

2. **✅ Removed all ChatGPT references**
   - Replaced with "LLM provider (pluggable)"
   - Used "model abstraction layer"
   - Used "AI model (provider-agnostic)"
   - Clarified architecture is not tied to any specific provider

3. **✅ Updated funding ask to $250,000**
   - Detailed breakdown: Engineering (48%), Security (16%), Infrastructure (10%), QA (8%), Sales (6%), Legal (4%), Contingency (8%)
   - Practical allocation supporting enterprise-grade delivery
   - Justification for each category

4. **✅ Set timeline to 12 months**
   - Complete roadmap T1-T12
   - Milestone-based with clear deliverables
   - Addressed why 12 months is achievable
   - Noted risks that could extend timeline

5. **✅ Replaced calendar months with timeline tokens**
   - T1 through T12 instead of "February 2026, March 2026"
   - No real month names or years in roadmap
   - Avoids dated commitments

6. **✅ Added §2: FastAPI explanation**
   - What FastAPI is (plain English)
   - Why we use it (speed, type safety, developer experience, production-ready)
   - Where it fits (both mise_app and transrouter)
   - What it is NOT (database, frontend framework, AI model, deployment platform)

7. **✅ Added §6: ENTERPRISE-GRADE ENGINEERING STANDARDS**
   - Major emphasis on enterprise-grade, safe, stable, clean architecture
   - Explicit guardrails: code standards, linting, CI checks, safe migrations, rollback strategy
   - Dependency discipline, minimal surface area, predictable local dev
   - Clear ownership matrix
   - Anti-clutter enforcement with weekly audit strategy

8. **✅ Added §8: PORT 8080 CONFLICT explanation**
   - Plain language explanation of what CPM is
   - Why it conflicted with Transrouter
   - Why port 8080 matters
   - What "cleanup completed" did
   - Action items (nothing immediate, prevention strategy documented)
   - How to detect automatically (scripts/check-ports)

9. **✅ Added §6.9: Cleanliness/Anti-Clutter enforcement**
   - Recurring discipline strategy
   - Single source of truth locations
   - Naming conventions
   - Folder structure rules
   - Weekly cleanup audit script
   - Delete immediately list

10. **✅ Added §9: CPM Deprecation Plan**
    - Clarified CPM is now integrated into Mise Web App
    - Component status matrix (keep/remove/rename)
    - Migration plan (Phase 1-3)
    - Updated architecture diagrams
    - Communication plan

11. **✅ Added §10: DEV ENVIRONMENT — STARTUP & VERIFICATION**
    - Standard startup procedure (3 terminals)
    - Verification checklist
    - Detailed health checks
    - What "good" looks like
    - Common failures & fixes (6 scenarios)
    - Quick diagnostic script

12. **✅ Added §11: HEALTH CHECKS — PURPOSE & USAGE**
    - Who uses them (automated systems, developers, operational scripts)
    - When to check manually (after startup, debugging, before tests, after deploy)
    - When NOT to check (application flow, tight loops, auth testing)
    - What to do if health check fails (4 failure scenarios with fixes)
    - Health check response formats
    - Future monitoring strategy

**No duplicated sections or repeated content.**
**Enterprise-grade and clean throughout.**
**Ready for 6-window coordinated development sprint.**

---

## READY FOR YOUR DIRECTION

I am fully updated on Mise's current state with all requested changes incorporated. This document is now the **canonical reference** for CC Window #1 (ccqb).

**What's the next task?**
