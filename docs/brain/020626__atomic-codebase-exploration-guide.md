# How to Reach Atomic-Level Understanding of Mise

> **Action on exit:** Save this file to `docs/brain/020626__atomic-codebase-exploration-guide.md`

**Purpose:** A durable, scalable guide for any Claude Code session to reach deep codebase understanding. Structured in two layers: a permanent methodology (Layer 1) and a dated snapshot (Layer 2) that should be updated as the codebase evolves.

---

# LAYER 1: THE METHODOLOGY (Permanent)

This layer describes HOW to explore. It works regardless of what the codebase looks like today.

---

## Step 1: Read the Governance Files (Mandatory — Non-Negotiable)

CLAUDE.md lists mandatory initialization files. Read them ALL, in full. These teach you the RULES: values, search protocol, reasoning framework, agent policy, company context, operational playbooks.

**What this gives you:** How to behave and a high-level map (directory structure, service names, architecture diagram).

**What this does NOT give you:** How any code actually works. You cannot answer must-be-correct questions about system behavior from governance files alone. The gap between "I know the rules" and "I know the system" is enormous.

---

## Step 2: Identify the System Layers

Every well-structured codebase has layers. Before diving into code, identify them. For Mise (or any multi-service system), look for:

1. **The User-Facing Layer** — What serves HTTP requests, renders templates, handles auth
2. **The Orchestration Layer** — What routes requests to the right handler, manages pipelines
3. **The Domain Logic Layer** — The actual business processing (parsing, calculations, validation)
4. **The Storage Layer** — Where data lives, how it's isolated, what format

**Discovery pattern:**
```
Glob **/*.py to see all Python files
Glob **/main.py or **/app.py to find service entry points
Glob **/routes/*.py or **/api/*.py to find HTTP endpoints
Read the Dockerfiles to understand what gets deployed where
Read requirements.txt or pyproject.toml for dependency map
```

---

## Step 3: Launch Parallel Explore Agents (One Per Layer)

Reading 30-60 files sequentially in your main context burns through your context window and is slow. Instead, launch **up to 3 Explore agents in parallel**, one per layer.

### How to Write Effective Explore Agent Prompts:

**Structure each prompt with:**

1. **Context sentence** — "I need to understand [layer name] at the atomic level."
2. **Discovery instructions** — Tell the agent HOW to find the files, not just which files to read:
   ```
   "First, glob [directory]/**/*.py to find all Python files.
    Then read every file found, starting with main.py or __init__.py.
    For each file, document: [what to capture]."
   ```
3. **"Note:" callouts** — For files you KNOW are important (from the governance docs), add specific instructions:
   ```
   "Note: [filename] is the critical file for [reason]. Read it COMPLETELY and document:
    - [specific thing 1]
    - [specific thing 2]"
   ```
4. **Capture template** — Tell the agent what to document for EVERY file:
   ```
   "For each file, document:
    - What it does (one sentence)
    - Key functions/classes and their signatures
    - What it imports from other parts of the codebase
    - Any external service calls (HTTP, API, database)
    - How data flows through it"
   ```
5. **Synthesizing question** — End with a question that forces connection, not just facts:
   ```
   "I need to understand: What is the EXACT code path from [input] to [output]?"
   ```

### Key Prompt Qualities:
- **"VERY thoroughly"** — Signals deep exploration, not skimming
- **Self-discovery first** — "Glob to find files" beats "read file X" (future-proof)
- **"Read COMPLETELY"** — Prevents agents from reading just the first 50 lines
- **Specific "Note:" callouts** — Only for files you ALREADY know are critical
- **End with data-flow question** — Forces the agent to trace execution paths

### What Each Agent Should Cover:

**Agent 1 (User-Facing Layer):**
- Entry point (main.py, app creation, middleware stack)
- All route handlers (glob routes directory, read every file)
- Configuration (settings, env vars, defaults)
- Authentication (how users are identified, session management)
- Templates (what pages exist, what data they need)
- Any bridge/adapter files that connect to other layers

**Agent 2 (Orchestration Layer):**
- Entry point (how requests arrive)
- Pipeline stages (what happens in order: transcription → classification → routing → execution)
- Agent definitions (what agents exist, how they're registered)
- External service clients (API wrappers, database clients)
- Data structures / schemas (what flows between stages)
- Prompt builders (what context gets injected into LLM calls)

**Agent 3 (Domain Logic + Storage):**
- Business processing code (parsers, validators, generators)
- Output format (what gets produced: PDF, CSV, JSON, database rows)
- Storage implementations (where data lives, isolation patterns)
- Canonical business rules (from workflow specs, brain files, config)
- Product catalogs, employee rosters, reference data

---

## Step 4: Synthesize Connections Between Layers

After agents return, the critical step is connecting the layers. Ask yourself:

### Five Connection Questions:

1. **Input → Output:** When a user does [action], what is the EXACT code path through all layers from HTTP request to stored result?

2. **Multiple Paths:** Are there multiple ways the same thing can happen? (e.g., two transcription services, two integration paths, legacy vs modern)

3. **Shared Components:** What do the layers share? (e.g., same agent classes used by both web app and API, same schema format across systems)

4. **Isolation Patterns:** How is data separated? (by user? by tenant? by time period? by domain?)

5. **What's Active vs Dormant?** Which components are actually used in production vs which are legacy/planned/dormant?

---

## Step 5: Self-Test

Write down questions you should be able to answer with certainty. Categories:

- **Architecture:** "What happens when [user action]?" (trace the full code path)
- **Business rules:** "What is the [domain] rule for [situation]?" (cite the source file)
- **Storage:** "Where is [data type] stored and how is it isolated?"
- **Technical:** "What [external service] is used for [purpose] and how is it configured?"
- **Edge cases:** "What happens when [unusual condition]?" (e.g., large file, missing data, conflicting sources)

If you can't answer from memory → you missed something. Go back and read the specific file.

---

## Step 6: Document Pitfalls

After synthesizing, explicitly list things that would mislead a naive reader:
- Components that LOOK active but are dormant
- Multiple systems that do the same thing (which is canonical?)
- Terminology that means different things in different contexts
- Assumptions from governance docs that don't match code reality

---

## Step 7: Update the Snapshot

After completing your exploration, update the Layer 2 snapshot below with:
- Current file structure (key files per layer)
- Current architecture (active paths, dormant components)
- Current business rules (with source citations)
- Date of last update

---

# LAYER 2: DATED SNAPSHOT (As of 2026-02-06)

**Last verified:** February 6, 2026
**Codebase state:** Main branch, commit eadcb47

> This section captures the CURRENT state of the Mise codebase. It will become stale as the code evolves. When it does, re-run the Layer 1 methodology and update this section.

---

## Current System Layers

### Layer A: Web Application (`mise_app/`, port 8000, FastAPI)

**Entry:** `mise_app/main.py`
**Key discovery:** `Glob mise_app/**/*.py` → ~15 files

**Middleware stack (execution order):**
1. SessionMiddleware — 24hr cookie sessions
2. RestaurantContextMiddleware — Injects restaurant_id
3. AuthMiddleware — Blocks unauthenticated (except /login, /health, inventory async endpoints)
4. NoCacheMiddleware — Prevents stale mobile content
5. CORSMiddleware — Explicit origin whitelist

**Routes:**
| Prefix | File | Purpose |
|--------|------|---------|
| `/payroll/period/{period_id}` | `routes/home.py` | Shifty grid, reset |
| `/payroll/period/{period_id}` | `routes/recording.py` | Audio upload, process, approve |
| `/payroll/period/{period_id}` | `routes/totals.py` | Weekly summary |
| `/inventory` | `routes/inventory.py` | Shelfy recording, large file upload, async processing |
| `/login`, `/logout` | `routes/auth.py` | Authentication |

**Bridge file:** `agent_service.py` — Imports agents directly from transrouter, bypasses HTTP

**Auth:** Hardcoded demo users (sowalhouse/mise2026, papasurf/papasurf2026), bcrypt + session cookies

**Config:** `config.py` — PayPeriod (7-day, ref 2026-01-05, 48 max), ShiftyStateManager (14 shifts/week: MAM-SuPM), ShiftyConfig

### Layer B: Orchestration (`transrouter/`, port 8080, FastAPI — CURRENTLY DORMANT for web app)

**Entry:** `transrouter/api/main.py`
**Key discovery:** `Glob transrouter/src/**/*.py` → ~15 files

**Pipeline:** ASR → Intent Classifier (keyword-based, NOT ML) → Entity Extractor (regex) → Domain Router → Agent Handler

**Agent registry:** `{"payroll": handle_payroll_request, "inventory": handle_inventory_request}`

**Claude client:** Model `claude-sonnet-4-20250514`, 8000 output tokens, 15000 input, defensive JSON extraction (3 strategies)

**Brain sync:** Loads workflow specs + brain docs + roster from disk, caches in memory

**Why dormant:** Web app calls agents directly via `agent_service.py` because users already select the domain in UI. The transrouter API still works but isn't called.

### Layer C: Domain Agents

**PayrollAgent** (`transrouter/src/agents/payroll_agent.py`):
- Input: Transcript + pay_period_hint + shift_code
- Output: approval_json (out_base, header, shift_cols, per_shift, cook_tips, weekly_totals, detail_blocks)
- Validates: Required keys, per_shift ↔ weekly_totals consistency (2¢ tolerance)
- Auto-corrects: Fills missing shifts, recalculates totals from detail_blocks
- Multi-turn: `parse_with_clarification()` via ConversationManager

**InventoryAgent** (`transrouter/src/agents/inventory_agent.py`):
- Input: Transcript + category (bar/food/supplies) + area
- Output: inventory_json with items, quantities, units
- Features: 880-product catalog, manual item mappings, conversion enrichment (e.g., "6 × 4 = 24 cans")

### Layer D: Standalone / Legacy Engines

**LPM** (`payroll_agent/LPM/`): Local offline payroll. `build_from_json.py` reads approval JSON → PDF (ReportLab) + Excel (pandas) + Toast CSV

**CPM** (`payroll_agent/CPM/`): Cloud real-time payroll. 1200+ line deterministic parser (NO Claude). Robust Whisper error handling (15+ formats). Exhaustive name normalization (50+ variants). Writes to BigQuery.

**LIM** (`inventory_agent/`): Local inventory parser. Tokenizer → normalizer → catalog matcher → validator → MarginEdge CSV generator + HTML breakdown

### Layer E: Storage

| What | Backend | Path Pattern | Isolation |
|------|---------|-------------|-----------|
| Shifty state | StorageBackend (local/GCS) | `{restaurant_id}/{period_id}/shifty_state.json` | Restaurant + 7-day period |
| Approval queue | StorageBackend | `{restaurant_id}/{period_id}/approval_queue.json` | Restaurant + 7-day period |
| Weekly totals | StorageBackend | `{restaurant_id}/{period_id}/totals.json` | Restaurant + 7-day period |
| Shelfy records | GCS bucket | `periods/{period_id}/shelfies.json` | Monthly period |
| Audio archive | Local + GCS | `recordings/{period_id}/{filename}` | Period (permanent) |

**Environment detection:** `K_SERVICE` env var → production (GCS), else → development (local filesystem)

---

## Current Code Paths

### Payroll Audio Upload
```
POST /payroll/period/{period_id}/process (audio file)
  → recording.py extracts restaurant_id from session
  → agent_service.process_payroll_audio(audio_bytes)
    → transcribe_audio() via ASR (Whisper or OpenAI)
    → PayrollAgent.parse_with_clarification(transcript)
      → Builds system prompt from brain_sync (roster, workflow spec, brain docs)
      → Calls Claude API
      → Validates + auto-corrects approval JSON
  → detect_shifty_from_transcript() — regex for day names + AM/PM
  → save_recording() — local + GCS archive
  → fix_approval_json_shift_codes() — correct Claude's day-of-week errors
  → flatten_approval_json() — convert to table rows
  → LocalApprovalStorage.add_shifty() — store rows
  → ShiftyStateManager.set_status("pending")
  → Return JSON with redirect to approval page
```

### Inventory Audio Upload (Large File >32MB)
```
POST /inventory/get_upload_url → signed GCS v4 URL (1hr expiry)
Client PUTs audio directly to GCS (bypasses 32MB Cloud Run limit)
POST /inventory/process_uploaded → spawns daemon thread:
  → Download from GCS
  → Google Speech-to-Text (long-running, 10min timeout)
  → agent_service.process_inventory_text() → InventoryAgent.parse_transcript()
  → ShelfyStorage.add_shelfy()
  → Update in-memory job status
GET /inventory/status/{job_id} → poll until complete
```

---

## Current Business Rules (With Source Citations)

### Payroll
| Rule | Value | Source |
|------|-------|--------|
| Tip pool default | Always pool unless explicitly said otherwise | `docs/brain/011326__lpm-tipout-from-food-sales.md` |
| Utility tipout | 5% of total shift food sales | `docs/brain/011326__lpm-tipout-from-food-sales.md` |
| Busser tipout | 4% of total shift food sales | `docs/brain/011326__lpm-tipout-from-food-sales.md` |
| Expo tipout | 1% of total shift food sales | `docs/brain/011326__lpm-tipout-from-food-sales.md` |
| AM shift hours | 6.5 hrs (all year, close 4:30 PM) | `docs/brain/011326__lpm-shift-hours.md` |
| DST PM (Mar-Nov) Sun-Thu | 4.5 hrs (close 9:00 PM) | `docs/brain/011326__lpm-shift-hours.md` |
| DST PM (Mar-Nov) Fri-Sat | 5.5 hrs (close 10:00 PM) | `docs/brain/011326__lpm-shift-hours.md` |
| Standard PM (Nov-Mar) Sun-Thu | 3.5 hrs (close 8:00 PM) | `docs/brain/011326__lpm-shift-hours.md` |
| Standard PM (Nov-Mar) Fri-Sat | 4.5 hrs (close 9:00 PM) | `docs/brain/011326__lpm-shift-hours.md` |

### Inventory
| Term | Definition | Source |
|------|------------|--------|
| Subfinal count | Total from ONE shelfy for a product | `CLAUDE.md`, `MISE_MASTER_SPEC.md` |
| Final count | Total from ALL shelfies combined | `CLAUDE.md`, `MISE_MASTER_SPEC.md` |
| Shelfy | A storage location (e.g., "Walk-in") | `CLAUDE.md`, `MISE_MASTER_SPEC.md` |

---

## Current External Services

| Service | Purpose | Used By |
|---------|---------|---------|
| Claude API (Anthropic) | Payroll/inventory parsing | PayrollAgent, InventoryAgent |
| Whisper (OpenAI API) | Small file transcription (≤32MB) | agent_service.py |
| Google Speech-to-Text | Large file transcription (>32MB) | direct_transcription.py |
| Google Cloud Storage | Audio archive + data storage | gcs_audio.py, shelfy_storage.py, storage_backend.py |
| Google Cloud IAM | Signed URL generation | inventory.py |
| BigQuery | CPM shift storage | commit_shift.py |

---

## Current Pitfalls

1. **Transrouter is dormant for the web app** — `agent_service.py` imports agents directly. Don't assume HTTP calls to port 8080.
2. **Three payroll systems exist** — LPM (local/Claude), CPM (cloud/deterministic), web app PayrollAgent (Claude via transrouter agents). Different parsing implementations, compatible schema.
3. **Pay period ≠ inventory period** — Payroll: 7-day periods. Inventory: monthly (last day of month).
4. **Two transcription services** — Whisper (small) and Google STT (large >32MB). Different APIs, different configs.
5. **agent_service.py is the bridge** — Single point connecting web app to transrouter agents. Miss it and you won't understand how layers connect.
6. **Approval JSON gets auto-corrected** — PayrollAgent fixes detail_blocks ↔ per_shift inconsistencies. Stored JSON may differ from Claude's original output.
7. **Brain files drive prompts** — Shift hours and tipout rules are in `docs/brain/`, not hardcoded. PayrollAgent system prompt is built dynamically from brain_sync.

---

## How to Update This Snapshot

When this snapshot becomes stale:

1. Re-run the Layer 1 methodology (3 parallel Explore agents)
2. Compare agent results against this snapshot
3. Update: file lists, architecture, code paths, business rules, pitfalls
4. Update the "Last verified" date and commit hash at the top of Layer 2
5. Remove anything that no longer exists; add new components

Expected update frequency: Every significant architectural change, or quarterly at minimum.