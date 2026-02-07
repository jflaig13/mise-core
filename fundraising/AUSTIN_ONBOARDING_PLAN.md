# Austin Onboarding Plan

**Co-Founder Technical Ramp-Up | February 2026**

---

## Overview

**Mise: The Voice-First Operating System for Hospitality.**
Mise helps restaurant managers handle payroll, inventory, and ops just by talking. What used to take hours of paperwork, counting, and data entry now takes a 30-second voice memo.

This is your plan for getting up to speed on Mise's codebase, tools, and workflows. You have zero technical background — that's fine. The tools we use (Claude Code, NotebookLM, AI transcription) are designed to close that gap. This plan is structured as self-directed learning with regular check-ins with Jon.

The goal: by the end of this onboarding, you can navigate the codebase, run Mise's core systems, generate IMDs (Internal Mise Documents), and contribute meaningfully — all using AI tools.

---

## Where Mise Is Right Now

Before diving into setup, here's what actually exists today so you know what you're looking at:

### What's Live in Production

**Mise Web App** — a mobile-friendly web application at **app.getmise.io**, hosted on Google Cloud. This is what a restaurant manager opens on their phone to use Mise. It currently has two working modules:

**Payroll (fully working):**
A manager opens the app and sees a weekly grid of **shifties** — individual shift records (e.g., "Monday AM," "Tuesday PM"). They tap a shifty, record a voice memo describing who worked, their tips, and food sales, and Mise does the rest: transcribes the audio, parses out all the employee names and dollar amounts, calculates tip pools, tipouts, and hours, then shows a preview for the manager to approve. One tap and it's done. This replaces 3+ hours of weekly spreadsheet work with a 30-second recording. Jon uses this every week at Papa Surf.

**Inventory (in development):**
Same voice-first approach. A manager walks through storage locations like the walk-in cooler, dry storage, or behind the bar, recording a **shelfy** (one individual count for that location) as they go: "Walk-in: 24 cans High Rise Blueberry, 12 bottles Aperol, 3 cases Topo Chico." Mise transcribes, matches products against a catalog of 65,000+ items, handles unit conversions (cases to cans, etc.), and generates a structured count sheet. This module is functional but still being refined.

### What's Planned (Not Built Yet)

- **Scheduling** — voice-to-schedule for weekly employee shifts
- **Ordering** — voice-to-order for vendor purchasing
- **Forecasting** — predict revenue, food costs, and labor needs based on historical data
- **General Ops** — catch-all for operational questions and exception handling

### The Architecture (Plain English)

Mise has four main pieces:

1. **The Web App** (`mise_app/`) — what the user sees and interacts with. Built with Python and FastAPI. Mobile-friendly.
2. **The Transrouter** (`transrouter/`) — the "brain" that sits behind the app. When someone records audio, the Transrouter transcribes it, figures out what the person is asking for (payroll? inventory? something else?), and routes it to the right agent.
3. **The Payroll Agent** (`payroll_agent/`) — handles all payroll math. Calculates tip pools, tipouts, hours, overtime. Has two versions: LPM (Local Payroll Machine — runs on Jon's computer) and CPM (Cloud Payroll Machine — runs in the cloud for the web app).
4. **The Inventory Agent** (`inventory_agent/`) — handles inventory parsing. Matches spoken product names to the catalog, converts units, validates quantities.

When a manager speaks into their phone, the audio flows: **Web App → Transrouter → Domain Agent → back to Web App** with structured, verified data.

### How the "Machines" Fit In (LPM, CPM, LIM)

You'll see the terms LPM, CPM, and LIM throughout the codebase. Here's how they relate to the web app:

**The original approach (LPM — Local Payroll Machine):**
Jon built payroll processing first as a local tool on his own computer. He'd record one long audio file covering the entire week's payroll, run it through Whisper (speech-to-text) locally, then feed the transcript into Claude to parse and calculate everything. This still works and is what Jon uses weekly at Papa Surf. It's fast and fully offline.

**The cloud version (CPM — Cloud Payroll Machine):**
To make payroll available through the web app (so any manager at any restaurant can use it, not just Jon on his laptop), the same payroll logic was rebuilt as a cloud service. The CPM runs on Google Cloud behind the web app. Instead of one big audio file for the whole week, the CPM processes individual shifties in real time as managers record them. Same math, same rules — different delivery method.

**Inventory (LIM — Local Inventory Machine):**
Same pattern. The LIM processes inventory audio locally. The inventory module in the web app uses the same parsing and catalog-matching logic but runs it in the cloud.

**The big picture:** The "machines" (LPM, CPM, LIM) are the processing engines. The web app is the interface that users interact with. The Transrouter connects them. Think of it like a car: the web app is the steering wheel and dashboard, the Transrouter is the transmission, and the machines are the engine. Jon built the engine first, then built everything else around it.

---

## Phase 1: Tool Setup (Tonight / Day 1)

Do all of this before our first check-in.

### 1.1 — Claude Max Subscription

- Jon will sign you up for Claude Max and send you login credentials once funding comes through
- This gives you access to Claude's most capable models with high usage limits
- Bookmark [claude.ai](https://claude.ai) — you'll use this daily
- In the meantime, you can use the free tier of Claude to start getting familiar with it

### 1.2 — Claude Code (CLI Tool)

Claude Code is how Jon builds Mise. It's a command-line AI that can read, write, and understand the entire codebase. Think of it as a coding partner that lives inside your terminal — you describe what you want in plain English, and it reads the code, understands it, and makes changes. You'll use it the same way Jon does.

**What is a "CLI" / "command line"?**

A CLI (Command Line Interface) is a text-based way to interact with your computer. Instead of clicking icons, you type commands. It looks like a black or blue window with text. PowerShell on Windows is a CLI. Don't be intimidated — you'll mostly be typing simple commands or talking to Claude Code in plain English.

**Install steps (Windows PC):**

1. Open PowerShell (search "PowerShell" in the Start menu, right-click, "Run as Administrator")
2. Install Node.js if you don't have it: go to [nodejs.org](https://nodejs.org), download the Windows LTS installer, run it
3. Close and reopen PowerShell, then run this command:
   ```
   npm install -g @anthropic-ai/claude-code
   ```
4. Navigate to the Mise repo (after you've cloned it — see section 1.4):
   ```
   cd C:\Users\Austin\mise-core
   ```
5. Launch Claude Code:
   ```
   claude
   ```
6. It will ask you to authenticate — log in with your Claude account
7. You should see a prompt. Type: "Read CLAUDE.md and tell me what this project is"
8. If it responds with a description of Mise, you're set up

### 1.3 — NotebookLM

NotebookLM is Google's AI research tool. You upload documents, and it lets you ask questions across all of them at once. It can also generate podcast-style audio summaries of everything you upload — two AI hosts discuss your docs in a conversational format, which is a great way to absorb a lot of information fast.

- Go to [notebooklm.google.com](https://notebooklm.google.com)
- Sign in with your Google account
- Create a new notebook called "Mise"
- Upload these files as sources (find them in `C:\Users\Austin\mise-core\`):
  - `CLAUDE.md`
  - `ONBOARDING.md`
  - `AGI_STANDARD.md`
  - `SEARCH_FIRST.md`
  - `VALUES_CORE.md`
  - `AGENT_POLICY.md`
  - `docs\INTERNAL_MISE_DOC_STANDARD.md`
  - `docs\MISE_STATE_COMPLETE.md` — comprehensive snapshot of the entire system state, including the web app
  - `workflow_specs\LPM\LPM_Workflow_Master.txt`
  - `workflow_specs\LIM\LIM_Workflow_Master.txt`
  - `workflow_specs\CPM\CPM_Workflow_Master.txt`
  - `workflow_specs\transrouter\Transrouter_Workflow_Master.txt`
  - `AI_Configs\Claude\system_instructions.md`
  - `docs\brain\011826__founder-story-pitch-pillar.md`
- NotebookLM will let you ask questions about all of these docs at once. Use it to understand Mise's architecture, principles, and workflows without having to read everything linearly.
- Use the **"Audio Overview"** feature — it generates a podcast-style summary of your uploaded docs. Listen to it.
- **Pro tip:** Click the little hand emoji on the Audio Overview. This lets you actually **join the conversation** — you can chime in and ask the AI hosts questions while they're discussing. Use this to dig deeper into anything that's unclear. It's like having a conversation with two people who've read everything.

### 1.4 — Git & GitHub

**What is GitHub?**

GitHub is where Mise's code lives. Think of it like Google Drive, but specifically designed for code. Every change anyone makes to the code gets tracked — who changed what, when, and why. This means:

- You can always see the history of every file
- If something breaks, we can roll back to a previous version
- Jon and you (and eventually the contractor) can all work on the code without overwriting each other's work
- There's always one "source of truth" version of the code that everyone pulls from

**What is a "repo"?**

"Repo" is short for "repository." It's just a folder of code that Git tracks. The Mise repo is the entire mise-core folder — all the code, docs, specs, everything. When you "clone" a repo, you're downloading a complete copy of that folder to your computer.

**Git** is the tool that syncs your local copy of the code with GitHub. When you "pull," you're downloading the latest changes. When you "push," you're uploading your changes for others to see.

**How to get Mise's code on your computer:**

1. Download Git for Windows: [git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer — use all the default options
3. Open PowerShell and verify it worked by typing:
   ```
   git --version
   ```
   You should see a version number like "git version 2.43.0"
4. Jon will add you as a collaborator on the Mise GitHub repo and send you the link
5. Clone the repo — this downloads the entire Mise codebase to your computer:
   ```
   cd C:\Users\Austin
   git clone [URL Jon sends you]
   ```
   This creates a `mise-core` folder on your computer with everything in it.
6. Going forward, before you start working each day, pull the latest changes:
   ```
   cd C:\Users\Austin\mise-core
   git pull
   ```

This ensures you always have the most up-to-date version of the code before you start working.

---

## Phase 2: Understand the System (Days 2–4)

This is all self-directed. Use Claude Code and NotebookLM. Take notes. Write down every question you have — bring them to our first check-in.

### 2.1 — Read the Core Docs

Open Claude Code in the `C:\Users\Austin\mise-core` directory and ask it to explain each of these. Don't just read them — have a conversation with Claude about them:

**Start with these (in order):**

1. `CLAUDE.md` — How Claude Code sessions work in this repo
2. `ONBOARDING.md` — The step-by-step initialization protocol
3. `AGI_STANDARD.md` — How we make decisions (the 5 questions)
4. `SEARCH_FIRST.md` — Why we search before we build
5. `VALUES_CORE.md` — Mise's non-negotiable principles and competitive advantages

**Then these:**

6. `AGENT_POLICY.md` — Rules and boundaries for all coding agents
7. `AI_Configs\Claude\system_instructions.md` — Claude's operating instructions for Mise
8. `docs\brain\121224__system-truth-how-mise-works.md` — How the system actually works
9. `docs\brain\011826__founder-story-pitch-pillar.md` — The Mise origin story and pitch framing

**Ask Claude Code things like:**
- "Explain CLAUDE.md to me like I'm not a developer"
- "What is the AGI Standard and why does it matter?"
- "How does the Transrouter work? Draw me the flow."
- "What agents exist in Mise and what does each one do?"
- "What is the Primary Axiom in VALUES_CORE.md and what does it mean for how we build?"

### 2.2 — Understand the Architecture

Ask Claude Code:

- "Explain Mise's architecture at a high level. What are all the components and how do they connect?"
- "What is the Transrouter and why is it important?"
- "What is the Local Payroll Machine vs the Cloud Payroll Machine?"
- "What is the Inventory Agent and how does it work?"
- "What does a manager's workflow look like from speaking into the phone to seeing a payroll preview?"
- "What is a domain agent? List all the domain agents in Mise."
- "What does the web app at app.getmise.io look like? What screens does a user see?"

Write up what you learn. This becomes your reference doc.

### 2.3 — Understand the Workflows

Read these workflow specs (or ask Claude Code to explain them):

- `workflow_specs\LPM\LPM_Workflow_Master.txt` — Local Payroll Machine
- `workflow_specs\LIM\LIM_Workflow_Master.txt` — Local Inventory Machine
- `workflow_specs\CPM\CPM_Workflow_Master.txt` — Cloud Payroll Machine
- `workflow_specs\transrouter\Transrouter_Workflow_Master.txt` — How audio gets routed
- `workflow_specs\SWARM\SWARM_Workflow_Master.txt` — How Jon runs multiple Claude Code windows in parallel

**What to understand:**
- What triggers each workflow?
- What data goes in? What comes out?
- Where does voice audio get processed?
- How does payroll go from a voice recording to a calculated pay stub?

---

## Phase 3: Run the System (Days 5–7)

Now you actually use Mise. Jon will pair with you on the first run, then you do it solo.

### 3.1 — Run a Payroll Test

Jon will walk you through:

1. Processing a test audio file through the payroll engine
2. Seeing the transcript, parsed shifts, and calculated pay
3. Reviewing the output for accuracy
4. Understanding what the approval flow looks like

After the walkthrough, do it yourself with a different test file.

### 3.2 — Run an Inventory Test

Jon will walk you through:

1. Processing a test inventory audio file
2. Seeing how voice gets parsed into product counts
3. Understanding shelfies, subfinal counts, and final counts
4. Reviewing the generated inventory spreadsheet

### 3.3 — Generate an IMD (Internal Mise Document)

**Important distinction:** There are two types of documents at Mise:

1. **IMDs (Internal Mise Documents)** — branded PDF documents that we generate for internal purposes: pitch decks, investment proposals, onboarding plans (like this one), strategy docs. These are created using Claude Code + our PDF generator and follow the IMD Standard (branded with our colors, logo, and fonts). You're reading one right now.

2. **Mise Docs** — deliverables that the Mise product generates for restaurant managers. For example: a weekly payroll summary, a monthly inventory report, a tip report. These are the output of Mise's workflows — the thing the customer actually receives and uses.

For this exercise, you're learning to create **IMDs.**

Learn the IMD pipeline:

1. Open any existing markdown file in `C:\Users\Austin\mise-core\fundraising\` (try `FAMILY_INVESTMENT_ASK.md`)
2. In Claude Code, ask: "Explain how generate_branded_pdf.py works"
3. Run the PDF generator (Jon will help you set up Python on your first run):
   ```
   cd C:\Users\Austin\mise-core\fundraising
   python generate_branded_pdf.py
   ```
4. Open the generated PDF and compare it to the markdown source
5. Understand: markdown source → HTML → branded PDF → archived to Google Drive

**Your task:** Create a short test IMD about anything (even just "Austin's Notes on Mise Architecture") and generate the PDF yourself.

---

## Phase 4: Build Your Knowledge Base (Ongoing)

### 4.1 — NotebookLM as Your Second Brain

As you learn, keep adding documents to your Mise notebook in NotebookLM:
- Your own notes
- Workflow specs you've read
- Meeting notes with Jon
- Any new docs created in the repo

Use NotebookLM to:
- Generate audio summaries of new docs (listen during commute, etc.)
- Join the Audio Overview conversation (✋) to ask questions about new material
- Ask cross-document questions ("How does payroll connect to inventory?")
- Prep for meetings by asking "What are the open questions about X?"

### 4.2 — Claude Code as Your Daily Tool

Every day you work on Mise, start by opening Claude Code in `C:\Users\Austin\mise-core` and asking:
- "What changed since yesterday?" (it can check git log)
- "What are the open issues or TODOs?"
- "Explain [whatever you're working on today]"

Get in the habit of asking Claude before Googling. Claude has full context on the Mise codebase. Google doesn't.

### 4.3 — AI Transcription & Summarization

When you and Jon have meetings or working sessions:

1. Record the audio
2. Use the transcription tools in the repo (`scripts\convert_m4a_to_wav.sh` to convert audio, then process through Whisper)
3. Feed the transcript into NotebookLM or Claude for summarization
4. Save key decisions and action items as docs in the repo

This creates a record of everything discussed and decided. Nothing gets lost.

---

## Check-In Schedule

| When | What | Format |
|------|------|--------|
| After Phase 1 | "I'm set up, here's what worked / didn't" | Text Jon |
| After Phase 2 | "Here's what I understand, here are my questions" | Meet with Jon (30–60 min) |
| After Phase 3 | "I ran payroll and inventory, here's what I saw" | Meet with Jon (30–60 min) |
| Weekly ongoing | Status update, questions, blockers | Standing weekly meeting |

---

## What You're Working Toward

By the end of this onboarding, you should be able to:

- Navigate the Mise codebase using Claude Code
- Run payroll and inventory processing end-to-end
- Generate branded IMDs (markdown → PDF → Google Drive)
- Explain Mise's architecture to someone else
- Use NotebookLM as a knowledge base for all Mise documentation
- Transcribe and summarize meetings and working sessions
- Identify bugs or issues during testing and describe them clearly
- Ask Claude Code to make small changes and understand what it did

You don't need to write code from scratch. You need to understand the system, operate the tools, and work effectively with Claude Code. That's the skill.

---

## Quick Reference: Key File Locations

All paths below are relative to your mise-core folder (`C:\Users\Austin\mise-core\`):

| What | Where |
|------|-------|
| Core project docs | `CLAUDE.md`, `ONBOARDING.md`, `AGI_STANDARD.md`, `SEARCH_FIRST.md`, `VALUES_CORE.md` |
| Agent policy | `AGENT_POLICY.md` |
| System architecture | `docs\brain\121224__system-truth-how-mise-works.md` |
| Founder story | `docs\brain\011826__founder-story-pitch-pillar.md` |
| Payroll workflow | `workflow_specs\LPM\LPM_Workflow_Master.txt` |
| Inventory workflow | `workflow_specs\LIM\LIM_Workflow_Master.txt` |
| Cloud payroll workflow | `workflow_specs\CPM\CPM_Workflow_Master.txt` |
| Transrouter workflow | `workflow_specs\transrouter\Transrouter_Workflow_Master.txt` |
| SWARM workflow | `workflow_specs\SWARM\SWARM_Workflow_Master.txt` |
| Web app code | `mise_app\` |
| Transrouter code | `transrouter\` |
| Payroll agent code | `payroll_agent\` |
| Inventory agent code | `inventory_agent\` |
| PDF generator | `fundraising\generate_branded_pdf.py` |
| IMD standard | `docs\INTERNAL_MISE_DOC_STANDARD.md` |
| Claude system instructions | `AI_Configs\Claude\system_instructions.md` |
| Fundraising docs | `fundraising\` |
| Scripts | `scripts\` |
| Google Drive archive | Shared Mise Google Drive → `docs` → `mise_library` |

---

## Glossary: Key Terminology

This is a complete reference of terms you'll encounter. Don't memorize these — refer back as needed.

### Mise-Specific Terms

| Term | What It Means |
|------|--------------|
| **Shelfy** | One individual inventory count for a storage location. A shelfy is to inventory what a shifty is to payroll — the building block. You record one shelfy per location (walk-in cooler, dry storage, behind the bar, etc.), and Mise combines them all into the final count. |
| **Shifty** | A work shift record for an employee — who worked, when, what role, tips earned, food sales, etc. The building block of payroll. |
| **Subfinal Count** | The inventory count from ONE shelfy for a given product. Example: "24 cans of High Rise Blueberry in the walk-in." |
| **Final Count** | The total inventory count across ALL shelfies for a given product. Example: "48 cans total" (24 from walk-in + 24 from office). |
| **Transrouter** | Mise's "brain" — the system that receives audio from the web app, transcribes it, figures out what the user is asking for (payroll? inventory?), and routes the request to the correct domain agent. |
| **Domain Agent** | A specialized module that handles one area of restaurant operations. Mise has a Payroll Agent and an Inventory Agent today, with Scheduling, Ordering, and Forecasting agents planned. Each agent knows everything about its domain. |
| **LPM (Local Payroll Machine)** | The version of the payroll system that runs on Jon's computer. Jon records one audio file covering the entire week, and LPM processes it locally. This is what Jon uses weekly at Papa Surf. |
| **CPM (Cloud Payroll Machine)** | The cloud version of the payroll system. This is what runs behind the web app — it processes individual shifts in real time as managers record them. |
| **LIM (Local Inventory Machine)** | The local version of the inventory system. Processes inventory audio recordings and generates structured count sheets. |
| **SWARM** | A workflow for running multiple Claude Code windows in parallel. Jon uses this to work on different parts of Mise simultaneously (one window for code, one for testing, one for docs, etc.). |
| **IMD (Internal Mise Document)** | A branded PDF document generated using our PDF generator — pitch decks, investment proposals, strategy docs, onboarding plans. Uses Mise colors, logo, and fonts. When someone says "make this an IMD," this is what they mean. |
| **Mise Doc** | A report or summary that the Mise product generates for a restaurant manager — weekly payroll summary, monthly inventory report, tip report. This is product output, not internal. |
| **Tip Pool** | When 2+ servers work the same shift, their tips are combined and split evenly. Mise detects this automatically. |
| **Tipout** | A percentage of food sales that goes to support staff (expo, busser, utility). Mise calculates these automatically based on Papa Surf's rules. |
| **Approval Flow** | The step where a manager reviews what Mise parsed from their recording before it becomes final. Mise never commits data without human approval. |
| **Workflow Spec** | A master document that defines exactly how a system works — every rule, every edge case, every calculation. These are the source of truth. If a workflow spec says it, that's how it works. |
| **Brain Docs** | Files in `docs\brain\` that contain immutable system rules. These override everything else. They define how Mise thinks, remembers, and makes decisions. |

### General Tech Terms

| Term | What It Means |
|------|--------------|
| **Repo / Repository** | A folder of code tracked by Git. The Mise repo is the entire `mise-core` folder. |
| **Codebase** | All the code that makes up Mise. Same thing as the repo, just a different word. |
| **Clone** | Downloading a complete copy of a repo from GitHub to your computer. You do this once. After that, you "pull" to get updates. |
| **Pull** | Downloading the latest changes from GitHub to your local copy. Do this every day before working. |
| **Push** | Uploading your changes from your computer to GitHub so others can see them. |
| **Commit** | A saved snapshot of changes. Like "saving" a document, but with a description of what you changed and why. |
| **CLI (Command Line Interface)** | A text-based way to interact with your computer. PowerShell is a CLI. You type commands instead of clicking icons. |
| **API (Application Programming Interface)** | A way for two pieces of software to talk to each other. When the web app sends audio to the Transrouter, it uses an API. You don't need to understand the details — just know it means "systems communicating." |
| **Frontend** | The part of the app the user sees and touches — buttons, screens, forms. The Mise web app interface is the frontend. |
| **Backend** | The part of the app that runs behind the scenes — processing data, running calculations, storing information. The Transrouter and agents are backend. |
| **Deploy / Deployment** | Putting code into production so real users can use it. When Jon deploys Mise, it goes live at app.getmise.io. |
| **Cloud** | Servers run by someone else (Google, Amazon, etc.) instead of your own computer. Mise runs on Google Cloud. |
| **Multi-Tenant** | One system serving multiple separate customers. Each restaurant's data is isolated — Papa Surf can't see SoWal House's data and vice versa. |
| **Python** | The programming language Mise is written in. You don't need to learn Python — Claude Code handles the code for you. |
| **FastAPI** | The framework (set of pre-built tools) used to build Mise's web app. Built on Python. |
| **Whisper** | OpenAI's speech-to-text AI model. This is what transcribes the voice recordings into text. |
| **LLM (Large Language Model)** | The type of AI that Claude is. It understands and generates human language. Mise uses LLMs to interpret what managers say and extract structured data from it. |
| **Markdown** | A simple formatting language for text documents. Uses symbols like `#` for headings and `**` for bold. All IMDs start as markdown files before being converted to PDFs. |
| **JSON** | A standard format for structured data. When Mise parses a payroll recording, the result is stored as JSON — a structured list of who worked, their tips, their hours, etc. |

---

*Mise: Everything in its place.*
