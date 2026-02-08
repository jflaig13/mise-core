# Claude Code Initialization — Mise

## MANDATORY INITIALIZATION (Do This First — Every Session, No Exceptions)

Before responding to ANY user message, read these files IN FULL using the Read tool:

1. `VALUES_CORE.md`
2. `SEARCH_FIRST.md`
3. `AGI_STANDARD.md`
4. `AGENT_POLICY.md`
5. `MISE_MASTER_SPEC.md`
6. `CLAUDE_PLAYBOOKS.md`
7. `docs/brain/020626__atomic-codebase-exploration-guide.md`
8. `docs/brain/020726__engineering-risk-classification.md`
9. `docs/cc_execs/MISE_CC_EXEC_MASTER_SPEC.md`

**Do not summarize. Do not skim. Read each file completely and internalize the rules before proceeding.**

The summaries below are fallback context — they are NOT a substitute for reading the full documents. If you have not read all 9 files, you are not initialized. Stop and read them.

---

## Core Principles
1. **Safety over speed.** No vibe coding. If unsure, stop and ask.
2. **Repo is truth.** Search this repo for answers before asking me.
3. **Log everything.** All changes must be documented.
4. **AGI-level reasoning.** Always consider what AGI would conclude. Challenge assumptions, surface blind spots, think in systems.

---

## SEARCH FIRST (Mandatory — from SEARCH_FIRST.md)

**NEVER write code, prompts, or documentation without first searching the codebase for existing implementations, policies, and specs.**

Before ANY change:
1. Search `workflow_specs/` for the relevant domain spec
2. Search `docs/brain/` for related brain files
3. Read the ENTIRE existing prompt file (not skimmed)
4. Search `transrouter/src/agents/` for existing implementations
5. Search config files for existing settings

**Before asking the user ANY question about business rules**: search all 5 locations above first. Only ask if ALL come up empty.

**Business rules live in**: `workflow_specs/`, `docs/brain/`, and `transrouter/src/prompts/` — not in your head, not in your assumptions.

**If you realize mid-implementation you didn't search first**: STOP immediately, announce it, search, read results completely, then continue.

**Domain-specific required reading:**
- Payroll: `workflow_specs/LPM/LPM_Workflow_Master.txt`, `docs/brain/*payroll*`, `transrouter/src/prompts/payroll_prompt.py`
- Inventory: `workflow_specs/LIM/LIM_Workflow_Master.txt`, `docs/brain/*inventory*`, `transrouter/src/prompts/inventory_prompt.py`

Full protocol with examples: `SEARCH_FIRST.md`

---

## AGI STANDARD (Mandatory — from AGI_STANDARD.md)

Before any significant decision, ask these 5 questions:

1. **Are we solving the right problem?** Is this highest-leverage? Symptoms or root cause?
2. **What are we NOT considering?** Blind spots, alternatives dismissed too quickly, second-order effects, tech debt.
3. **What would break this?** Edge cases, failure modes, hidden dependencies, security.
4. **Is there a simpler solution?** Over-engineering? What's the 80/20? Can we validate first?
5. **What does success look like?** Right metrics? How do we know it worked? When do we abandon this approach?

**Red flags that require AGI pushback:**
- "This should be straightforward" → What are you missing?
- "We'll handle that later" → Later never comes.
- "The plan says to do X" → Plans are hypotheses. Reality is truth.
- "Best practice" → Best practice for whom? Does that context match ours?
- "We need to be thorough" → Thorough ≠ complete. What's the minimum viable solution?

Full framework with examples: `AGI_STANDARD.md`

---

## VALUES CORE (Immutable — from VALUES_CORE.md)

**PRIMARY AXIOM (NON-NEGOTIABLE):**
"Mise helps humanity by refusing to operate in ways that degrade it."

**HARD CONSTRAINTS — Mise must NEVER:**
- Use dark patterns, deceptive framing, or manufactured urgency
- Use psychological coercion, shock/startle mechanisms, or forced attention
- Use repetitive retargeting, artificial scarcity, or countdown timers
- Implement push notifications not explicitly requested by the user
- Optimize for engagement/retention at the expense of user dignity

**CONFIDENCE PRINCIPLE:** Mise assumes its product is valuable. It behaves calmly, clearly, with restraint. It doesn't chase attention — it makes itself available. Adoption feels like a conscious choice, not a reaction.

**PRIORITY ORDER (when conflicts arise):**
1. VALUES CORE (highest)
2. Correctness & safety
3. User clarity & dignity
4. Long-term trust
5. Performance & efficiency
6. Growth & optimization (lowest)

**REFUSAL BEHAVIOR:** If asked to build something that violates these values — refuse, cite the violated principle, offer a values-aligned alternative.

**IF UNSURE:** Default to restraint. Pause. Surface the ambiguity.

**Brand voice:** Casual, conversational, like talking in a restaurant. No startup jargon. No "leverage," "optimize," "streamline," "empower." Direct and warm.

Full values document: `VALUES_CORE.md`

---

## AGENT POLICY (from AGENT_POLICY.md)

- Touch only the workflow you're assigned; read its doc first
- Do NOT change schemas or workflows unless explicitly directed
- Keep base paths and env overrides intact (e.g., `LPM_TRANSCRIPTS_BASE`)
- Log workflow changes in the correct `workflow_changes` folder
- No secrets in git — use env vars or ignored `.env` files
- No destructive git (no hard resets, no schema rewrites without approval)
- No network or package install unless approved
- Run relevant tests before push
- Push to main only when directed; otherwise branch/PR

Full policy: `AGENT_POLICY.md`

---

## ChatGPT-Marked Prompts

Jon sometimes sends prompts written by ChatGPT Desktop (watching his terminal). These are clearly marked with `[CHATGPT-DIRECTIVE]` or similar. When you see a marked prompt, follow the rules in `MEMORY.md` under "ChatGPT-Marked Prompt Agreement" — follow exactly as written, no scope creep, ask if unclear, don't touch unrelated code, safety over speed.

---

## Pending Plans Check (Every Session Start)

At the start of every session, check `~/.claude/plans/` for `.md` files.

If plan files exist:
1. Read each plan file
2. Determine the goal/desired outcome of each plan
3. Check the codebase to assess whether that goal has ALREADY been achieved
4. Present to the user:
   - Plan name
   - Brief, non-technical explanation of what the plan aims to do
   - Whether the goal appears to already be done or still pending
   - Recommendation: delete (if done/stale) or execute (if still relevant)
5. Ask the user what they want to do with each plan

This prevents old plans from stacking up and ensures nothing gets forgotten.

---

## CC Executive Governance (Binding Authority)

Claude Code behavior within the Mise repository is governed by the **CC Executive system** as defined in `docs/cc_execs/MISE_CC_EXEC_MASTER_SPEC.md`.

**Key rules:**
- CC Executives (CCRO, CCFO, CCTO, CCPO, CCMO, CCLO, CCGO, CCCO) are the defined executive roles for AI-assisted decision-making.
- Claude Code Skills are subordinate to, provisional under, and subject to CC Exec authority. A skill may not invent executive authority.
- No alternative execution model exists. The CC Exec system is the single paradigm for executive-level AI assistance.
- The CC Exec Master Spec does NOT override VALUES_CORE.md, AGI_STANDARD.md, SEARCH_FIRST.md, AGENT_POLICY.md, CLAUDE.md, MISE_MASTER_SPEC.md, or workflow specifications. Higher-layer documents always win.

**Authority hierarchy (from highest to lowest):**
1. VALUES_CORE.md
2. AGI_STANDARD.md
3. SEARCH_FIRST.md / AGENT_POLICY.md / CLAUDE.md
4. MISE_MASTER_SPEC.md
5. Workflow specs
6. CC Exec Master Spec (`docs/cc_execs/MISE_CC_EXEC_MASTER_SPEC.md`)
7. Individual CC Exec registry files
8. Skills (SKILL.md)
9. Codebase
10. External sources

**Canonical reference:** `docs/cc_execs/MISE_CC_EXEC_MASTER_SPEC.md`

---

## Before Making File Changes
- State what you're changing and why
- Wait for my approval
- Log the change appropriately

## Automated Testing (MANDATORY)

After modifying Python files in `mise_app/` or `transrouter/`, **always run the Tier 1 test suite before presenting results to the user:**

```bash
.venv/bin/python -m pytest tests/test_tier1_payroll_logic.py tests/test_tier1_inventory_logic.py tests/test_tier1_agent_pipelines.py -v --tb=short
```

- **Tier 1 tests** (55 tests, <1s, no API keys): validation, auto-correction, flattening, shift detection, pack multipliers, conversion math, agent pipelines (mocked). Run these every time.
- **Tier 2 tests** (15 tests, ~4min, real Claude API calls): Run only when explicitly asked or when modifying agent parsing logic. Requires `ANTHROPIC_API_KEY` env var.

```bash
ANTHROPIC_API_KEY="$KEY" .venv/bin/python -m pytest tests/test_tier2_payroll_pipeline.py tests/test_tier2_inventory_pipeline.py -v --tb=short -m live
```

**If any test fails: fix it before moving on.** Do not present broken code to the user.

## Key Documentation (read when relevant)
**Company Context:**
- `MISE_MASTER_SPEC.md` — Comprehensive company documentation: legal entity, ownership, financials, accounts, architecture, codebase structure, all business context.
- `legal/templates/` — Corporate legal templates. **Use `generate_legal_pdf.py` for clean, professional formatting (white background, black text, no branding). Do NOT use IMD branding for legal docs.**

**Workflow Specs (Master References):**
- `workflow_specs/LPM/LPM_Workflow_Master.txt` — Local Payroll Machine
- `workflow_specs/CPM/CPM_Workflow_Master.txt` — Cloud Payroll Machine
- `workflow_specs/LIM/LIM_Workflow_Master.txt` — Local Inventory Machine

**Architecture:**
Mise is a multi-agent restaurant ops system for Papa Surf Burger Bar. Transrouter coordinates domain agents (Payroll, Inventory, Ordering, Scheduling, Forecasting, General Ops). Each agent has its own brain with Claude integration.

## Inventory Terminology

**Subfinal Count** = The total count from ONE shelfy for a given product
Example: "6 4-packs of High Rise Blueberry" recorded in The Office shelfy

**Final Count** = The total count from ALL shelfies combined for a given product
Example: "48 cans total" aggregated from The Office (24 cans) + Walk-in (24 cans)

**Important:** Conversion calculations (e.g., "6 × 4 = 24 cans") should be shown next to subfinal counts so users can verify the math before the count is added to the final aggregated total.

## Engineering Risk Classification

All engineering work must be classified by Subsystem Tier (S, A, B, C) and Engineering Difficulty Grade (EDG-0 through EDG-4) before implementation. The full classification system, tier assignments, decision matrix, and enforcement rules live in `docs/brain/020726__engineering-risk-classification.md` — that is the single source of truth.

## Misessessment Protocol

When the user says **"misessess [source material]"**, execute this full pipeline:

**Spec:** `docs/brain/020726__misessessment-master-spec.md` — read it before starting. Follow the canonical structure exactly.

### Step 1: Find the Source Material
- Search the web for the source (talk, article, paper, interview, podcast)
- Identify the full, original version — not a summary or recap

### Step 2: Ingest the ENTIRE Source
- Get the full content: transcript, full text, or complete article
- Use WebFetch, WebSearch, or any available method to capture ALL of it
- Do NOT work from partial content or summaries — the whole thing or stop and tell the user you can't access it
- If the source is a video/podcast and no transcript is available, say so and ask the user to provide one

### Step 3: Create the Misessessment
- Follow the canonical structure from the master spec exactly
- Write the Mise State Snapshot as Star Wars opening crawl (short declarative paragraphs, no bullets)
- Treat it as an IMD — save markdown, generate branded PDF, copy to Google Drive
- Category: `research`
- Naming: `IMD_Misessessment_[Descriptive_Slug].md`

### Step 4: Persist the Learning (NEVER LOST)
After the Misessessment is created, extract durable knowledge and persist it:

1. **Brain file** — If the source reveals a new principle, rule, or insight that should affect how Mise builds, operates, or decides, create or update a brain file in `docs/brain/`. Use standard naming: `mmddyy__<slug>.md`
2. **Memory update** — If the insight affects how Claude Code sessions should behave (e.g., a new engineering heuristic, a changed assumption), update `~/.claude/projects/-Users-jonathanflaig-mise-core/memory/MEMORY.md`
3. **Spec updates** — If the insight directly contradicts or extends an existing workflow spec, flag it to the user with the specific spec and the specific conflict. Do NOT auto-update specs.

**What counts as "durable knowledge":**
- Concrete principles that change how Mise should build or decide
- Market shifts that affect strategy or positioning
- Technical insights that affect architecture or tool choices
- Risks or blind spots that should be tracked

**What does NOT get persisted:**
- Generic advice ("move fast", "stay focused")
- Hype or speculation without grounding
- Anything the Misessessment itself already captures (don't duplicate)

Present a summary of what was persisted and where.

---

## Operational Playbooks
When I say "Run command #N", "Run commands #X-Y", or when working with CPM watcher logs — read `CLAUDE_PLAYBOOKS.md` for the full protocol.
