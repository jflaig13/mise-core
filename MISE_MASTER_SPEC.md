# MISE MASTER SPEC

**The Complete Context Document for Mise, Inc.**

**Version:** 1.0
**Last Updated:** February 7, 2026
**Purpose:** Enable any new team member, AI agent, or stakeholder to understand the complete state of Mise — business, legal, technical, and operational — from a single document.

---

## TABLE OF CONTENTS

1. [Company Overview](#1-company-overview)
2. [Ownership & Equity](#2-ownership--equity)
3. [Financial Infrastructure](#3-financial-infrastructure)
4. [Legal Formation](#4-legal-formation)
5. [Domain & Service Accounts](#5-domain--service-accounts)
6. [Insurance Status](#6-insurance-status)
7. [Production Status](#7-production-status)
8. [Architecture Overview](#8-architecture-overview)
9. [Codebase Structure](#9-codebase-structure)
10. [Workflow Specifications](#10-workflow-specifications)
11. [Safety & Governance](#11-safety--governance)
12. [Brain Files Index](#12-brain-files-index)
13. [Fundraising Status](#13-fundraising-status)
14. [Customer & Market](#14-customer--market)
15. [Team](#15-team)
16. [Key File Reference](#16-key-file-reference)
17. [Action Items & Gaps](#17-action-items--gaps)

---

## 1. COMPANY OVERVIEW

### Legal Entity
- **Name:** Mise, Inc.
- **Type:** Delaware C-Corporation
- **EIN:** 41-2726158
- **Date of Incorporation:** November 19, 2025
- **Registered Agent:** ZenBusiness Inc., 611 South DuPont Highway Suite 102, Dover, DE 19901

### Official Address
```
7901 4th St. North #9341
St. Petersburg, FL 33702
```

### Mission
**The Voice-First Operating System for Hospitality**

Mise helps restaurant managers handle payroll, inventory, and ops just by talking. What used to take hours of paperwork, counting, and data entry now takes a 30-second voice memo.

### Brand Voice
Casual, conversational, like talking in a restaurant. No startup jargon. No "leverage," "optimize," "streamline," "empower." Direct and warm.

### Primary Axiom (from VALUES_CORE.md)
> "Mise helps humanity by refusing to operate in ways that degrade it."

This axiom governs ALL decisions including product design, marketing, growth mechanics, UX, analytics, and sales.

---

## 2. OWNERSHIP & EQUITY

### Cap Table (via Carta)

| Shareholder | Shares | Percentage | Role |
|-------------|--------|------------|------|
| Jonathan Flaig | 7,000,000 | 70% | Founder, President & CEO |
| Austin Miett | 3,000,000 | 30% | Co-founder, Secretary & Treasurer |
| **Total Authorized** | **10,000,000** | **100%** | |

### Vesting
- **Status:** Fully vested (no vesting restrictions per Shareholder Agreement)
- **83(b) Elections:** TBD — verify if needed given full vesting

### Board of Directors
- **Authorized Directors:** 2
- **Current Directors:** Jonathan Flaig, Austin Miett

### Officers
- **President & CEO:** Jonathan Flaig
- **Secretary & Treasurer:** Austin Miett

### Equity Management
- **Platform:** Carta
- **Stock Certificates:** ❌ MISSING — need formal stock ledger entries

---

## 3. FINANCIAL INFRASTRUCTURE

### Banking
| Account | Institution | Type | Status |
|---------|-------------|------|--------|
| Operating Account | Mercury | Checking | ✅ Active |
| Reserve Account | Mercury | Savings | ✅ Active |

### Credit
| Application | Institution | Type | Status |
|-------------|-------------|------|--------|
| Business Credit Card | Chase | Ink Unlimited | ⏳ Applied Jan 29, 2026 |
| Credit Line | UBS | Line of Credit | ⏳ Awaiting approval |

### Billing
| Expense | Payment Method | Notes |
|---------|----------------|-------|
| API Costs (Anthropic, OpenAI) | Jon's Mise Debit Card | |
| Google Workspace | Jon's Mise Debit Card | |
| Cloud Infrastructure | Jon's Mise Debit Card | |

### Reimbursements Pending
| Amount | Description | Status |
|--------|-------------|--------|
| $5.00 | OpenAI API (initial setup) | Pending |
| ~$5.00 | Anthropic API (initial setup) | TBD - need to verify |

---

## 4. LEGAL FORMATION

### Document Location
**Google Drive:** `/Docs/Legal/Formation`

### Formation Documents Status

| Document | Status | Date | Notes |
|----------|--------|------|-------|
| Certificate of Incorporation | ✅ Present | Nov 19, 2025 | Filed with Delaware |
| Corporate Bylaws | ✅ Present | Nov 21, 2025 (updated Jan 22, 2026) | |
| EIN Confirmation (SS-4) | ✅ Present | Nov 21, 2025 | EIN: 41-2726158 |
| Shareholder Agreement | ✅ Present | Jan 22, 2026 | Signed via DocuSign |
| Corporate Operating Agreement | ✅ Present | | |
| Initial Board Resolutions | ✅ Present | | `legal/documents/Initial_Board_Resolutions_Mise.pdf` |
| Stock Ledger/Certificates | ❌ MISSING | | **ACTION REQUIRED** |
| Founder IP Assignment | ✅ Present | | `legal/documents/IP_Assignment_Jonathan_Flaig.pdf`, `IP_Assignment_Austin_Miett.pdf` |
| 83(b) Elections | ❓ Verify | | May not be needed (fully vested) |
| Written Consent Actions | ❌ MISSING | | Template needed |

### Agreements Executed

| Agreement | Party | Date | Location |
|-----------|-------|------|----------|
| Mutual NDA | Timmy McNulty | | fundraising/NDA_Timmy_McNulty.md |
| Mutual NDA | Grady Kittrell | | fundraising/NDA_Grady_Kittrell.md |
| Mutual NDA | Boyd Barrow | | fundraising/NDA_Boyd_Barrow.md |

### Missing Legal Documents (HIGH PRIORITY)
1. **Terms of Service** — ✅ Created (`legal/documents/Terms_of_Service_Mise.pdf`)
2. **Privacy Policy** — ✅ Created (`legal/documents/Privacy_Policy_Mise.pdf`)
3. **Initial Board Resolutions** — ✅ Created (`legal/documents/Initial_Board_Resolutions_Mise.pdf`)
4. **Founder IP Assignment** — ✅ Created (`legal/documents/IP_Assignment_Jonathan_Flaig.pdf`, `IP_Assignment_Austin_Miett.pdf`)

---

## 5. DOMAIN & SERVICE ACCOUNTS

### Domain
- **Primary Domain:** getmise.io
- **Registrar:** (TBD - document registrar and renewal date)

### Email & Workspace
- **Provider:** Google Workspace
- **Domain:** @getmise.io
- **Admin:** jon@getmise.io

### Service Accounts

| Service | Purpose | Billing | Status |
|---------|---------|---------|--------|
| Google Cloud Platform | BigQuery, Cloud Run, Storage | Mise Debit | ✅ Active |
| Anthropic API | Claude for parsing/reasoning | Mise Debit | ✅ Active |
| OpenAI API | Whisper for transcription | Mise Debit | ✅ Active |
| GitHub | Code repository | (verify) | ✅ Active |
| Carta | Equity management | (verify) | ✅ Active |
| Mercury | Banking | N/A | ✅ Active |
| DocuSign | Document signing | (verify) | ✅ Active |

### Credentials Management
- **Location:** (Document where API keys/secrets are stored - NOT the actual values)
- **Best Practice:** Use environment variables, never commit secrets to repo

---

## 6. INSURANCE STATUS

### Current Coverage
**❌ NONE — No business insurance currently in place**

### Required Insurance (AGI Recommendations)

| Type | Priority | Purpose | Estimated Cost |
|------|----------|---------|----------------|
| D&O Insurance | **HIGH** | Protects directors/officers from personal liability. Required before taking investor money. | $1,000-3,000/yr |
| Cyber Insurance | **HIGH** | Critical for handling payroll/financial data. Covers data breaches, ransomware. | $1,000-5,000/yr |
| E&O Insurance | MEDIUM | Protects against professional mistakes/negligence | $500-2,000/yr |
| General Liability | MEDIUM | Basic business protection | $500-1,500/yr |

**ACTION REQUIRED:** At minimum, obtain D&O insurance before closing any investment round.

---

## 7. PRODUCTION STATUS

### Live Deployments

| Client | Status | Since | Workflows Active |
|--------|--------|-------|------------------|
| Papa Surf | ✅ PRODUCTION | Q3 2025 | Payroll (LPM), Inventory (LIM — testing) |

### Production Metrics
- **Consecutive Payroll Runs:** 20+ weeks
- **Payroll Errors:** Zero (0)
- **System of Record:** Yes — Papa Surf has fully replaced manual payroll with Mise

### Pipeline

| Client | Status | Expected | Notes |
|--------|--------|----------|-------|
| Down Island | Pilot Queued | T3 | First external pilot |
| SoWal House | Pilot Queued | TBD | |

---

## 8. ARCHITECTURE OVERVIEW

### System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MISE: Voice-First Operating System                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ↓               ↓               ↓
              ┌──────────┐   ┌──────────┐   ┌──────────┐
              │   LPM    │   │   LIM    │   │   CPM    │
              │ (Local   │   │ (Local   │   │ (Cloud   │
              │ Payroll) │   │ Inventory)│   │ Payroll) │
              └──────────┘   └──────────┘   └──────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
                      ┌───────────────────┐
                      │   Transrouter     │
                      │  (API Gateway +   │
                      │   Orchestration)  │
                      └─────────┬─────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
  ┌──────────────┐   ┌──────────────┐
  │  Mise App    │   │   External   │
  │  (Web UI)    │   │   Services   │
  └──────────────┘   └──────────────┘
```

### Service Ports

| Port | Service | Purpose |
|------|---------|---------|
| 8000 | mise_app | Web UI (FastAPI) |
| 8080 | Transrouter | API Gateway |
| 5432 | PostgreSQL | Database (optional) |

### Data Flow

1. **Recording:** Manager captures audio on phone
2. **Ingestion:** Audio uploaded to Mise (mise_app or Transrouter)
3. **Transcription:** Whisper (local or cloud) produces text
4. **Cleanup:** Optional LLM normalization (CPM)
5. **Routing:** Intent classifier routes to correct domain agent
6. **Processing:**
   - **LPM:** Approval JSON → build_from_json.py → PDF/XLSX/CSV
   - **LIM:** Parse → catalog match → MarginEdge CSV
   - **CPM:** Parse → BigQuery writes
7. **Output:** Reports, exports, database records

---

## 9. CODEBASE STRUCTURE

### Repository
- **Location:** `/Users/jonathanflaig/mise-core`
- **Version Control:** Git
- **Remote:** GitHub (private)

### Top-Level Directory Structure

```
mise-core/
├── AI_Configs/              # AI model configurations
├── Branding/                # Brand assets (fonts, logos, colors)
├── clients/                 # Client-specific configurations
│   ├── papasurf/
│   ├── downisland/
│   ├── sowalhouse/
│   └── new_client_onboarding/
├── claude_commands/         # Numbered shell commands (see CLAUDE_PLAYBOOKS.md)
├── config/                  # Configuration files
├── data/                    # Data files
├── .claude/                 # Claude Code configuration
│   └── skills/              # 14 custom slash-command skills
├── docs/                    # Documentation hub
│   ├── brain/               # System truth, memory rules
│   ├── changelogs/          # Version history
│   ├── internal_mise_docs/  # IMDs (Internal Mise Documents)
│   └── onboarding/          # Client onboarding docs
├── fundraising/             # Investor materials
├── inventory_agent/         # LIM implementation
├── legal/                   # Legal documents (local copies)
│   ├── documents/           # Generated legal PDFs (Board Resolutions, IP, ToS, Privacy)
│   └── templates/           # Legal document generation scripts
├── logs/                    # Application logs
├── mise_app/                # Web UI (Flask/FastAPI)
├── payroll_agent/           # CPM & LPM implementations
│   ├── CPM/                 # Cloud Payroll Machine
│   └── LPM/                 # Local Payroll Machine
├── recordings/              # Audio archives
├── roster/                  # Employee rosters
├── scripts/                 # Utility scripts
├── tests/                   # Test suites
├── transcripts/             # Transcript archives
├── transrouter/             # API gateway & orchestration
├── workflow_specs/          # Canonical workflow specifications
│   ├── CPM/
│   ├── LIM/
│   ├── LPM/
│   ├── transrouter/
│   └── roster/
└── [Root Files]
    ├── CLAUDE.md            # Agent initialization
    ├── CLAUDE_PLAYBOOKS.md  # Operational playbooks (command runner, CPM watcher)
    ├── ONBOARDING.md        # Session onboarding
    ├── SEARCH_FIRST.md      # Mandatory search protocol
    ├── AGI_STANDARD.md      # Reasoning framework
    ├── VALUES_CORE.md       # Immutable constraints
    ├── AGENT_POLICY.md      # Agent scope & boundaries
    ├── START_MISE.md        # Service startup guide
    ├── MISE_MASTER_SPEC.md  # This document
    └── requirements.txt     # Python dependencies
```

### Key Implementation Files

#### Payroll Agent (LPM)
| File | Purpose |
|------|---------|
| `payroll_agent/LPM/build_from_json.py` | Main runner: builds PDF/XLSX/CSV from approval JSON |
| `payroll_agent/LPM/tipreport_runner.sh` | Shell wrapper for build process |
| `payroll_agent/LPM/PayrollExportTemplate.csv` | Employee roster with Toast IDs |

#### Payroll Agent (CPM)
| File | Purpose |
|------|---------|
| `payroll_agent/CPM/engine/payroll_engine.py` | Main engine entrypoint |
| `payroll_agent/CPM/engine/parse_shift.py` | Shift extraction logic |
| `payroll_agent/CPM/engine/commit_shift.py` | BigQuery validation & writes |
| `payroll_agent/CPM/transcribe/app.py` | Whisper ASR service |

#### Inventory Agent (LIM)
| File | Purpose |
|------|---------|
| `inventory_agent/parser.py` | Main parser entrypoint |
| `inventory_agent/normalizer.py` | SKU normalization |
| `inventory_agent/generate_inventory_file.py` | MarginEdge CSV generation |
| `inventory_agent/inventory_catalog.json` | Product database |

#### Transrouter
| File | Purpose |
|------|---------|
| `transrouter/api/main.py` | FastAPI app entrypoint |
| `transrouter/src/transrouter_orchestrator.py` | Main orchestrator |
| `transrouter/src/intent_classifier.py` | Intent detection |
| `transrouter/src/domain_router.py` | Route to domain agents |
| `transrouter/src/prompts/payroll_prompt.py` | Payroll interpretation logic |

#### Web Application
| File | Purpose |
|------|---------|
| `mise_app/main.py` | FastAPI app entrypoint (port 8000) |
| `mise_app/routes/` | Route handlers |
| `mise_app/templates/` | Jinja2 HTML templates |
| `mise_app/storage_backend.py` | Multi-tenant storage abstraction |

---

## 10. WORKFLOW SPECIFICATIONS

### Master Specification Files

| Workflow | Master File | Purpose |
|----------|-------------|---------|
| **LPM** | `workflow_specs/LPM/LPM_Workflow_Master.txt` | Local Payroll Machine |
| **CPM** | `workflow_specs/CPM/CPM_Workflow_Master.txt` | Cloud Payroll Machine |
| **LIM** | `workflow_specs/LIM/LIM_Workflow_Master.txt` | Local Inventory Machine |
| **Transrouter** | `workflow_specs/transrouter/Transrouter_Workflow_Master.txt` | API Gateway |

### LPM (Local Payroll Machine)
- **Purpose:** Fully offline weekly payroll processing
- **Input:** Weekly payroll audio (.m4a/.wav) + Whisper transcript (.txt)
- **Output:**
  - Tip Report PDF
  - Excel Summary
  - Toast Payroll CSV
  - Approval JSON
- **Pipeline:** Record → Whisper transcribe → Claude parse → Manager approves → Runner generates outputs

### CPM (Cloud Payroll Machine)
- **Purpose:** Real-time cloud payroll audio ingestion
- **Pipeline:** Audio ingestion → Whisper → LLM cleanup → Parsing → Validation → BigQuery writes
- **Key Feature:** LLM transcript normalization for better accuracy

### LIM (Local Inventory Machine)
- **Purpose:** Convert inventory audio into MarginEdge-ready CSV
- **Pipeline:** Record → Whisper transcribe → Parse → Normalize → Validate → Generate CSV
- **Key Feature:** Fuzzy matching to product catalog

---

## 11. SAFETY & GOVERNANCE

### Core Documentation Files

| File | Purpose | Priority |
|------|---------|----------|
| `CLAUDE.md` | Agent initialization, command runner convention | READ FIRST |
| `SEARCH_FIRST.md` | Mandatory search protocol before ANY changes | MANDATORY |
| `AGI_STANDARD.md` | AGI-level reasoning framework (5 questions) | MANDATORY |
| `VALUES_CORE.md` | Primary axiom, immutable constraints | MANDATORY |
| `AGENT_POLICY.md` | Agent scope, boundaries, safety rules | READ |
| `CLAUDE_PLAYBOOKS.md` | Operational playbooks (command runner, CPM watcher) | MANDATORY |
| `docs/brain/020626__atomic-codebase-exploration-guide.md` | Deep codebase exploration methodology + snapshot | MANDATORY |
| `docs/brain/020726__engineering-risk-classification.md` | Engineering risk tiers and difficulty grades | MANDATORY |
| `ONBOARDING.md` | New session onboarding checklist | READ |

### Key Safety Principles

1. **File-Based Intelligence:** Chat is transient, files are cognition, git is memory
2. **Workflow Primacy:** Workflows are foundational truth; override intuition
3. **No Ephemeral Learning:** If it's not in a file, it doesn't exist
4. **Search First:** Never write code without searching for existing implementations
5. **AGI Reasoning:** Ask 5 questions before any significant decision

### The 5 AGI Questions
1. Are we solving the right problem?
2. What are we NOT considering?
3. What would break this?
4. Is there a simpler solution?
5. What does success actually look like?

---

## 12. BRAIN FILES INDEX

**Location:** `docs/brain/`

| File | Purpose |
|------|---------|
| `121224__system-truth-how-mise-works.md` | FILE-BASED INTELLIGENCE (CANONICAL) |
| `121224__workflow-primacy-directive.md` | WORKFLOWS ARE FOUNDATIONAL TRUTH |
| `121224__absolute-memory-rule.md` | NO EPHEMERAL LEARNING |
| `121224__brain-ingest-protocol.md` | How to create brain documents |
| `121224__claude-code-onboarding.md` | Claude Code initialization |
| `121725__new-trigger-initialization.md` | New trigger initialization protocol |
| `011326__lpm-shift-hours.md` | LPM shift hour calculations |
| `011326__lpm-tipout-from-food-sales.md` | Tipout percentage rules |
| `011826__founder-story-pitch-pillar.md` | Origin story + pitch architecture (CANONICAL) |
| `020626__api-keys-reference.md` | API keys storage reference |
| `020626__atomic-codebase-exploration-guide.md` | Deep codebase exploration methodology + dated snapshot |
| `020726__engineering-risk-classification.md` | Engineering risk tiers (S/A/B/C) and difficulty grades (EDG-0–4) |
| `020726__misessessment-master-spec.md` | Misessessment format spec — standardized research output for media analysis |
| `020726__scribe-enforcement-protocol.md` | Scribe skill enforcement rules |
| `LEARNING_BANKS_ARCHITECTURE.md` | Learning system architecture |

### Brain File Naming Convention
```
mmddyy__<slug>.md
```
Example: `011826__founder-story-pitch-pillar.md` = January 18, 2026

---

## 13. FUNDRAISING STATUS

### Current Round
- **Target:** $250,000
- **Verbal Commitment:** $50,000 received (as of Feb 2026)
- **Valuation:** $3M pre-money (7.7% equity) or $2.5M (10% if pushed)
- **Structure:** Common stock, advisory role (non-voting)
- **Use of Funds:**
  - Engineering (52%): $130K
  - Security/SOC 2 (14%): $35K
  - Infrastructure (8%): $20K
  - QA (6%): $15K
  - Sales/Onboarding (4.8%): $12K
  - Legal (4%): $10K
  - Contingency (8%): $20K

### Investor Materials
**Location:** `fundraising/`

| Document | File |
|----------|------|
| Executive Summary | `EXECUTIVE_SUMMARY.md` |
| Pitch Deck V3 | `PITCH_DECK_V3.md` |
| Moat Memo | `MISE_MOAT_MEMO.md` |
| AGI Defensibility | `MISE_AGI_DEFENSIBILITY.md` |
| Investor Questions (150) | `INVESTOR_QUESTIONS.md` |
| Budget Breakdown | `BUDGET_BREAKDOWN_250K.md` |
| Term Proposal | `TERM_PROPOSAL_DRAFT.md` |

### Advisor Pipeline
| Advisor | Status | Equity | Notes |
|---------|--------|--------|-------|
| Boyd Barrow | NDA Signed | 2% (proposed) | |
| Grady Kittrell | NDA Signed | 2% (proposed) | |
| Timmy McNulty | NDA Signed | | |

### 12-Month Milestones (Post-Funding)
- T1-T2: Engineer onboarded, security hardening
- T3: Down Island live (Pilot #2)
- T4: First paying customer, billing live
- T5-T6: 5 restaurants, ~$1.5-2K MRR
- T7-T8: SOC 2 Type 1 complete
- T9-T10: 10 restaurants, ~$3-4K MRR
- T11: Inventory workflow launches
- T12: 15-20 restaurants, $6-8K MRR, Jon full-time, Series A ready

---

## 14. CUSTOMER & MARKET

### Target Customer
- **Type:** Single-location, owner-operator restaurants
- **Size:** 8-25 employees (complex enough for tip pools, small enough for no back-office staff)
- **Concept:** Full-service, tip-heavy
- **POS:** Toast/Square (not paper, not enterprise)
- **Pain:** Spending 2+ hours/week on payroll personally; drowning in admin

### Market Size
| Metric | Value |
|--------|-------|
| TAM | $7.2B (US restaurant back-office software) |
| SAM | $800M (single-location, owner-operated) |
| SOM | $8M (initial target: 500 restaurants × $149/mo × 12) |

### Pricing
| Plan | Price | Includes |
|------|-------|----------|
| Payroll Only | $149/month | Voice-to-payroll automation |
| Full Suite | $249/month | Payroll + Inventory + Scheduling (future) |

### Unit Economics
| Metric | Value |
|--------|-------|
| CAC | $500 (direct sales, word-of-mouth) |
| LTV | $3,600 (24-month retention at $149/mo) |
| LTV:CAC | 7:1 |
| Gross Margin | 90%+ |
| Break-even | ~35 restaurants |

---

## 15. TEAM

### Founders

**Jonathan Flaig** — Founder, President & CEO
- Owner of Papa Surf (restaurant)
- Builder of Mise (wrote the code)
- Uses Mise every week for his own payroll
- Founder-market fit: IS a restaurant owner, not a consultant

**Austin Miett** — Co-founder, Secretary & Treasurer
- Equity partner (30%)
- Operations and business development
- Technical onboarding in progress (see `docs/internal_mise_docs/md_files/IMD_Austin_Onboarding_Plan.md`)

### Hiring Plan
- **First Hire:** Senior Full-Stack Engineer ($130K allocated in budget)
- **Timeline:** T1 (Month 1 post-funding)
- **Job Posting:** `fundraising/SENIOR_ENGINEER_JOB_POSTING.md`

---

## 16. KEY FILE REFERENCE

### Root-Level Files (Read These First)
| File | Purpose |
|------|---------|
| `CLAUDE.md` | Agent initialization, command runner |
| `CLAUDE_PLAYBOOKS.md` | Operational playbooks (command runner, CPM watcher) |
| `ONBOARDING.md` | Session onboarding checklist |
| `SEARCH_FIRST.md` | Mandatory search protocol |
| `AGI_STANDARD.md` | Reasoning framework |
| `VALUES_CORE.md` | Primary axiom, constraints |
| `AGENT_POLICY.md` | Agent scope & boundaries |
| `START_MISE.md` | Service startup guide |
| `MISE_MASTER_SPEC.md` | This document |

### Configuration
| File | Purpose |
|------|---------|
| `config/settings.example.yaml` | Configuration template |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Git ignore rules |

### Deployment
| File | Purpose |
|------|---------|
| `Dockerfile` | Container definition |
| `mise_app/DEPLOY.md` | Web app deployment guide |
| `transrouter/deploy/cloudbuild.yaml` | Cloud Build config |

### Testing
| Directory | Purpose |
|-----------|---------|
| `tests/` | Unit and regression tests |
| `tests/test_data/` | Test fixtures |
| `shifty_tests/` | Integration testing |

---

## 17. ACTION ITEMS & GAPS

### Legal (HIGH PRIORITY)
- [x] Create Initial Board Resolutions template — `legal/documents/Initial_Board_Resolutions_Mise.pdf`
- [x] Create Founder IP Assignment agreements (Jon & Austin) — `legal/documents/IP_Assignment_*.pdf`
- [x] Create Terms of Service for mise_app — `legal/documents/Terms_of_Service_Mise.pdf`
- [x] Create Privacy Policy (CCPA/GDPR compliant) — `legal/documents/Privacy_Policy_Mise.pdf`
- [ ] Create Written Consent template for future board actions
- [ ] Verify 83(b) election requirements

### Insurance (HIGH PRIORITY)
- [ ] Obtain D&O Insurance (before investor close)
- [ ] Obtain Cyber Insurance (payroll data protection)
- [ ] Evaluate E&O and General Liability

### Financial
- [ ] Follow up on Chase Ink Unlimited application
- [ ] Follow up on UBS credit line
- [ ] Process OpenAI reimbursement ($5.00)
- [ ] Verify Anthropic reimbursement amount

### Documentation
- [ ] Document all API keys/secrets storage location
- [ ] Document domain registrar and renewal dates
- [ ] Export formal stock ledger from Carta

---

## APPENDIX A: INVENTORY TERMINOLOGY

| Term | Definition |
|------|------------|
| **Subfinal Count** | Total count from ONE shelfy for a given product |
| **Final Count** | Total count from ALL shelfies combined for a given product |
| **Shelfy** | A storage location (e.g., "The Office", "Walk-in") |

---

## APPENDIX B: BRAND COLORS

| Name | Hex | Usage |
|------|-----|-------|
| Navy | `#1B2A4E` | Body text, h1, h3, accent line, table headers |
| Red | `#B5402F` | h2 headers, blockquote borders, links |
| Cream | `#F9F6F1` | Table alternating rows, horizontal rules |

---

## APPENDIX C: COMMAND RUNNER CONVENTION

When Jon says **"Run command #N"**:
1. Look in `claude_commands/`
2. Find the file starting with `N_`
3. Read the file contents
4. Execute the shell commands
5. Report results

---

*Mise: Everything in its place.*
