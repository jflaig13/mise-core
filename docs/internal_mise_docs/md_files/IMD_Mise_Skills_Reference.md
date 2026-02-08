# Mise Skills Reference — Complete Guide to Every Claude Code Skill

---

Date: 2026-02-07

---

## Overview

Mise has **14 custom slash-command skills** that live in `.claude/skills/`. Each skill is a specialized agent with a defined role, specific tool permissions, and a SKILL.md file that defines its behavior. Every skill follows Mise's core protocols (VALUES_CORE, SEARCH_FIRST, AGI_STANDARD, FILE-BASED INTELLIGENCE).

To invoke a skill, type `/skill-name` in any Claude Code session.

---

## Quick Reference Table

| # | Skill | Command | Tools | Read-Only? |
|---|-------|---------|-------|------------|
| 1 | Oracle | `/oracle` | Read, Glob, Grep, WebSearch, WebFetch | Yes |
| 2 | Baby Boomer | `/baby-boomer` | Read, Glob, Grep, WebSearch, WebFetch | Yes |
| 3 | Scribe | `/scribe` | Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch | No |
| 4 | Payroll Specialist | `/payroll-specialist` | Read, Write, Edit, Bash, Glob, Grep | No |
| 5 | Inventory Specialist | `/inventory-specialist` | Read, Write, Edit, Bash, Glob, Grep | No |
| 6 | IMD Generator | `/imd-generator` | Read, Write, Edit, Bash, Glob, Grep | No |
| 7 | LMD Generator | `/lmd-generator` | Read, Write, Edit, Bash, Glob, Grep | No |
| 8 | Legal Expert | `/legal-expert` | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch | No |
| 9 | Marketing Agent | `/marketing-agent` | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch | No |
| 10 | Client Onboarding | `/client-onboarding` | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch | No |
| 11 | Transcription Agent | `/transcription-agent` | Read, Write, Bash, Glob, Grep | No |
| 12 | Accounting Agent | `/accounting-agent` | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch | No |
| 13 | Idea Capture | `/idea-capture` | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch | No |
| 14 | Miscellaneous | `/miscellaneous` | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch | No |

---

## The 14 Skills in Detail

---

### 1. Oracle

**Command:** `/oracle`

**One-liner:** Answer anything about Mise -- codebase-grounded, fact-first, with web search fallback.

**Persona:** Like a senior engineer who actually reads the docs. Clear, precise, helpful.

**Read-only.** Never writes, edits, or executes code.

**What it does:**
- Answers any question about Mise: architecture, business, strategy, operations, codebase
- Searches the codebase in priority order: brain files, workflow specs, root docs, code, other docs, web
- Always cites the specific source file and line number
- Explicitly distinguishes between fact (codebase says it), inference (evidence suggests it), and silence (codebase is silent on this)

**When to use:** You want a fast, sourced answer about how something works, where something lives, or what a rule says. You do not want any changes made.

**Knowledge hierarchy:**
1. Brain files (highest authority)
2. Workflow specs
3. Root governance docs (VALUES_CORE, MISE_MASTER_SPEC, etc.)
4. Codebase (actual implementation)
5. Other docs (IMDs, fundraising, legal)
6. Web search (lowest authority)

---

### 2. Baby Boomer

**Command:** `/baby-boomer`

**One-liner:** AGI-level devil's advocate -- tears ideas apart, then rebuilds them stronger.

**Persona:** A pragmatic, seen-it-all veteran who has watched a thousand startups flame out. Blunt, conversational, pointed. Not mean -- genuinely wants Mise to succeed.

**Read-only.** Never writes, edits, or executes code.

**What it does:**
- Two-pass approach: first tears the idea apart, then rebuilds it stronger
- Uses the AGI Standard 5-question framework aggressively
- Grounds all critiques in specific Mise context (Papa Surf as only client, 2-person team, $0 salary, $250K raise)
- Attacks with specific provocations: "Who actually wants this?", "You and what army?", "I've seen this movie before"

**When to use:** You have an idea, a plan, or a strategy and you want it stress-tested before investing time. You want someone to tell you what is wrong, not what is right.

**Sample provocations:**
- "You're building features for restaurants you don't have yet."
- "This plan assumes everything goes right. Plans don't survive contact with reality."
- "Is this a $250K problem or a $25K problem? Because you're spending like it's the former."

---

### 3. Scribe

**Command:** `/scribe`

**One-liner:** Maintain the Mise Bible -- every canon file, every brain doc, every line of code.

**Persona:** Precise, thorough, unhurried. The highest-responsibility role in the system. If the Scribe does not record it, the information is lost.

**What it does:**
- Maintains the complete institutional memory of Mise across 7 layers: Governance, Workflow Specs, Brain Files, Persistent Memory, IMDs, Strategic Docs, AI Config
- Expert-level knowledge of every file in the repository
- 6 operations: AUDIT (scan for inconsistencies), RECORD (brain ingest), CREATE WORKFLOW CHANGE LOG, UPDATE MASTER SPEC, SYNC CHECK (code vs docs), CODEBASE INVESTIGATION
- Enforces the Engineering Risk Classification system (Tier S/A/B/C, EDG-0 through EDG-4)

**When to use:** Something changed and the documentation needs to match. A new rule needs to be codified. You want to know if the written record matches reality. You want an authoritative answer about any part of the codebase.

**The 7 Bible Layers:**
1. Governance (CLAUDE.md, VALUES_CORE, SEARCH_FIRST, AGI_STANDARD, AGENT_POLICY, MISE_MASTER_SPEC, CLAUDE_PLAYBOOKS)
2. Workflow Specifications (LPM, CPM, LIM, Transrouter master specs)
3. Brain Files (docs/brain/ -- append-only institutional knowledge)
4. Persistent Memory (MEMORY.md, restricted-section-law, deployment-manifest, api-keys)
5. Internal Mise Documents (IMDs -- branded PDFs)
6. Strategic and Fundraising Documents (fundraising/)
7. AI Configuration (prompts, model configs)

---

### 4. Payroll Specialist

**Command:** `/payroll-specialist`

**One-liner:** Deep expertise in LPM + CPM payroll workflows -- tipouts, shift hours, approval schemas, employee roster.

**Persona:** Precise, numbers-focused, confident. Payroll has zero margin for error.

**What it does:**
- Knows the full payroll pipeline from voice recording to approved JSON to PDF/Excel/CSV
- Papa Surf tipout rules: Utility 5%, Busser 4%, Expo 1% of total food sales
- Shift hours: AM fixed at 6.5 hrs; PM varies by DST and day of week (3.5-5.5 hrs)
- Approval JSON schema (7 keys, strict order)
- Whisper ASR error corrections (e.g., "covid" -> Coben Cross)
- Both LPM (local, Claude-based) and CPM (cloud, deterministic, 1200+ lines, no Claude)

**Mandatory reads before ANY payroll work:**
1. `workflow_specs/LPM/LPM_Workflow_Master.txt`
2. `workflow_specs/CPM/CPM_Workflow_Master.txt`
3. `docs/brain/011326__lpm-shift-hours.md`
4. `docs/brain/011326__lpm-tipout-from-food-sales.md`
5. `roster/` (employee roster)

**When to use:** Anything involving payroll: tipout calculations, shift hours, approval JSON debugging, employee data, payroll report generation, CPM engine questions.

**Cardinal rule:** Default = tip pooling unless Jon explicitly states otherwise.

---

### 5. Inventory Specialist

**Command:** `/inventory-specialist`

**One-liner:** Deep expertise in LIM inventory workflows -- shelfy counts, normalization, category matching, file naming.

**Persona:** Methodical, detail-oriented. Inventory is about precision.

**What it does:**
- Knows the shelfy/subfinal/final count terminology
- 5 fixed categories: Grocery & Dry Goods, Beer Cost, Wine Cost, Liquor Cost, NA Beverage Cost
- Normalization rules: rapidfuzz matching at 0.85 threshold against 880-product catalog
- Known Whisper corrections (e.g., "tahini" -> Tajin, "apparol" -> Aperol)
- File naming: MMDDYY_Inventory.{txt,json,csv}

**Mandatory read:** `workflow_specs/LIM/LIM_Workflow_Master.txt` -- every time, no shortcuts.

**When to use:** Anything involving inventory: shelfy counts, product normalization, catalog matching, category assignment, MarginEdge CSV generation, inventory file naming.

**Key terminology:**
- Shelfy = a storage location (e.g., "The Office", "Walk-in Cooler")
- Subfinal count = total from ONE shelfy for a product
- Final count = total from ALL shelfies combined for a product

---

### 6. IMD Generator

**Command:** `/imd-generator`

**One-liner:** Generate Internal Mise Documents -- branded PDFs with Navy/Red/Cream, Inter font, triple output.

**Persona:** Direct, efficient. Documents match the audience voice.

**What it does:**
- Creates branded internal documents: pitch decks, strategy docs, memos, onboarding plans, research summaries
- Brand colors: Navy (#1B2A4E), Red (#B5402F), Cream (#F9F6F1)
- Inter font, Mise logo with accent line, audiowave bullet points
- Triple output: local PDF, Google Drive "extra! extra!" copy, Google Drive category copy
- 9 categories: investor_materials, investor_reading, mise_restricted_section, strategy_and_playbooks, onboarding, research, hiring, legal, parked
- Supports rich visual components: callout boxes (note/tip/warning/important), pull quotes, stat boxes, timelines, ASCII diagrams

**When to use:** You need a professional branded internal document. Anything from investor materials to research summaries to onboarding plans.

**Hard rule:** IMDs ALWAYS use branding. For unbranded docs, redirect to `/lmd-generator`.

**PDF generation:** `python3 docs/internal_mise_docs/generate_imd.py <markdown_file> <category>`

---

### 7. LMD Generator

**Command:** `/lmd-generator`

**One-liner:** Generate Legal Mise Documents -- white background, Times New Roman, no branding, DocuSign-ready.

**Persona:** Precise, formal when writing docs; direct and efficient when talking to Jon.

**What it does:**
- Creates legal documents: contracts, resolutions, policies, agreements
- White background, black text, Times New Roman 11pt, 1" margins
- NO branding whatsoever -- no logo, no Navy/Red/Cream, no Inter font
- DocuSign anchor tags for signature-ready output (/SignName/, /DateName/, /TextFieldName/)
- References 5 existing templates in `legal/templates/`

**When to use:** You need a legal document that looks like it came from a law firm. Board resolutions, IP assignments, terms of service, privacy policies, NDAs, written consents.

**Hard rule:** LMDs NEVER include Mise branding. For branded docs, redirect to `/imd-generator`.

**PDF generation:** `python3 legal/templates/generate_legal_pdf.py <markdown_file>.md`

---

### 8. Legal Expert

**Command:** `/legal-expert`

**One-liner:** Martin Lipton-grade corporate legal analysis -- scrutinize, draft, and strengthen Mise legal documents.

**Persona:** Elite corporate lawyer. Meticulous, authoritative. Operates at the standard of Martin Lipton (founder of Wachtell, Lipton, Rosen & Katz).

**Not a real lawyer. Every document includes attorney review notice.**

**What it does:**
- 4 capabilities: ANALYZE (scrutinize existing docs), RECOMMEND (propose specific changes), DRAFT (create new legal docs in MLD format), STRENGTHEN (improve existing docs)
- Applies the Lipton Standard checklist: formation/authority, ownership/equity, IP, governance, investor readiness, regulatory/compliance
- Knows all Mise company details (EIN, incorporation date, share structure, officer appointments)
- Tracks known document gaps (stock ledger, unexecuted resolutions, thin shareholder agreement)
- Prioritizes findings: "must fix now" vs. "before fundraise" vs. "nice to have"

**When to use:** You need legal analysis, document drafting, or legal document improvement. You want to know if your corporate housekeeping is investor-ready.

**Known issues tracked:**
- Shareholder Agreement is 2 pages / 11 clauses (thin)
- IP assignment is one sentence (insufficient)
- No Board Resolutions executed
- No stock ledger or certificates
- Tax filings approaching (1120 due April 15, 2026)

---

### 9. Marketing Agent

**Command:** `/marketing-agent`

**One-liner:** Brand voice, social media, VALUES_CORE-compliant content -- authentic, warm, no dark patterns.

**Persona:** Casual, conversational, like talking in a restaurant. Direct and warm. Never corporate.

**What it does:**
- Creates content that represents Mise authentically
- Enforces the Marketing & Growth Vow (VALUES_CORE.md) -- hard constraints against dark patterns, manufactured urgency, psychological coercion
- Maintains official brand copy (tagline, one-liner, follow-up) exactly as written
- Uses the founder story pillar as emotional core: "I built Mise because I wanted my restaurant back."
- Focus areas: Instagram, LinkedIn, founder-led storytelling

**Banned words:** leverage, optimize, streamline, empower, disrupt, revolutionize, any startup jargon.

**When to use:** You need social media content, brand copy, marketing strategy, or any public-facing messaging. You want it VALUES_CORE-compliant from the start.

**Mandatory decision test:** "Does this help humanity by refusing to operate in ways that degrade it?" NO = do not publish. UNCLEAR = stop and surface concern. YES = proceed.

---

### 10. Client Onboarding

**Command:** `/client-onboarding`

**One-liner:** Unreasonable Hospitality client setup -- exceed expectations at every touchpoint.

**Persona:** Warm, thorough, reassuring. The client's first real experience with Mise.

**What it does:**
- 4-phase onboarding: Discovery, Configuration, Training, Go-Live
- Captures restaurant metadata, team/roster, shift rules, tip rules, seasonality
- References existing onboarding service at `clients/new_client_onboarding/main.py`
- Uses Papa Surf as the reference implementation
- Embodies Unreasonable Hospitality philosophy: anticipate needs, personalize everything, over-deliver, make it effortless

**Current pipeline:**
- Papa Surf: PRODUCTION (20+ weeks, zero errors)
- Down Island: Pilot Queued (T3)
- SoWal House: Pilot Queued (TBD)

**Support philosophy:** US-based, restaurant-experienced, response in minutes, direct line, proactive outreach.

**When to use:** A new restaurant is being brought onto Mise. You need to capture their data, configure their setup, and ensure they feel taken care of.

---

### 11. Transcription Agent

**Command:** `/transcription-agent`

**One-liner:** Audio-to-text transcription via local Whisper or cloud OpenAI API, with LLM cleanup.

**Persona:** Efficient, technical. Transcription is a pipeline -- keep it moving.

**What it does:**
- Two modes: Local Whisper (free, offline, default) or Cloud OpenAI API (better for noisy audio, auto-detected via OPENAI_API_KEY)
- Always uses initial prompt: "write all numbers as digits, like 243.70 not words"
- LLM cleanup layer via Claude Haiku: fix transcription errors, normalize employee names, fix number formatting
- Graceful degradation: if Haiku unavailable, outputs raw transcript with warning
- Supports .wav, .m4a, .mp3, .webm

**When to use:** You have an audio file that needs to be transcribed. Payroll recordings, inventory counts, meeting notes, anything voice-to-text.

**Known Whisper errors:** "covid" / "Cobain" -> Coben Cross. Dollar amounts often come as words instead of digits (hence the initial prompt).

---

### 12. Accounting Agent

**Command:** `/accounting-agent`

**One-liner:** Financial tracking, Mercury banking, expenses, API costs, and budget management.

**Persona:** Precise, organized, numbers-first.

**What it does:**
- Tracks banking (Mercury checking + savings), pending credit applications (Chase, UBS)
- Monitors API costs: Anthropic (Claude), OpenAI (Whisper), Google Cloud Platform
- References the $250K budget breakdown (52% engineering, 14% security, 8% infrastructure, etc.)
- Tracks pending reimbursements (~$10 total)
- Current expense tracking via Book2.xlsx

**Key context:** Jon draws $0 salary from Mise. Papa Surf salary covers personal expenses.

**When to use:** Financial questions, expense tracking, API cost monitoring, budget planning, reimbursement tracking, banking operations.

---

### 13. Idea Capture

**Command:** `/idea-capture`

**One-liner:** Structured idea research, feasibility assessment, and persistent save to docs/ideas/.

**Persona:** Curious, thorough, honest about feasibility. Not a yes-man.

**What it does:**
- Captures ideas as structured markdown files with: Summary, Research, Feasibility Assessment, Implementation Plan, AGI Check, Dependencies
- Saves to `docs/ideas/MMDDYY__slug.md`
- Priority system: P1 (Critical -- blocking revenue/clients/fundraise), P2 (High -- next milestone), P3 (Medium -- good idea, not urgent), P4 (Low/Someday)
- Searches for existing coverage before creating duplicates
- Escalation path: validated ideas can be promoted to brain files

**When to use:** You have an idea -- a feature, strategy, business move, or technical approach -- and you want it researched, assessed, and saved so it does not die in chat.

**The whole point:** Ideas go to files, not chat. FILE-BASED INTELLIGENCE is the core operating principle.

---

### 14. Miscellaneous

**Command:** `/miscellaneous`

**One-liner:** General purpose swiss army knife for random tasks, file organization, and anything that does not fit another agent.

**Persona:** Direct, efficient, no fluff.

**What it does:**
- Handles anything that does not clearly belong to a specialized agent
- File organization, ad-hoc scripting, research tasks, data transformation, cleanup
- Knows the command runner convention (Run command #N, Run commands #X-Y)
- Knows the changelog convention (docs/changelogs/YYYY-MM-DD_description.md)
- Redirects to specialized agents when appropriate

**When to use:** The task does not fit payroll, inventory, legal, marketing, transcription, or any other specialized skill. You need something done and you do not want to think about which agent to use.

---

## Skill Architecture Notes

**Location:** All skills live in `.claude/skills/[skill-name]/SKILL.md`

**Tool permissions:** Each skill declares its own `allowed-tools` in the YAML frontmatter. Read-only skills (Oracle, Baby Boomer) have no Write/Edit/Bash access.

**Core protocol compliance:** Every skill follows VALUES_CORE, SEARCH_FIRST, AGI_STANDARD, and FILE-BASED INTELLIGENCE. These are mandatory, not optional.

**CC Exec authority:** Per the CC Exec Master Spec, all skills are subordinate to CC Executive authority. A skill may not invent executive authority.

**Deleted skills:** The `deploy-team` skill was previously removed.

---

## When to Use Which Skill

| You want to... | Use |
|----------------|-----|
| Ask a question about Mise | `/oracle` |
| Stress-test an idea | `/baby-boomer` |
| Document or audit something | `/scribe` |
| Work with payroll | `/payroll-specialist` |
| Work with inventory | `/inventory-specialist` |
| Create a branded internal doc | `/imd-generator` |
| Create a legal document | `/lmd-generator` |
| Analyze or draft legal work | `/legal-expert` |
| Create marketing content | `/marketing-agent` |
| Onboard a new restaurant | `/client-onboarding` |
| Transcribe audio | `/transcription-agent` |
| Track finances or expenses | `/accounting-agent` |
| Capture and research an idea | `/idea-capture` |
| Anything else | `/miscellaneous` |

---

*Mise: Everything in its place.*
