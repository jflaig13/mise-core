# Local Payroll Machine (LPM)

Purpose / Scope
- Fully offline weekly payroll processing pipeline for Papa Surf
- Converts single weekly payroll audio recording into Toast-ready CSV, Tip Report PDF, and Excel summary
- Human-in-the-loop workflow: Jon records → Whisper transcribes → Claude calculates → Jon approves → Runner generates outputs
- Production workflow for weekly payroll operations

Repo Location
- payroll_agent/LPM/
  - approvals/ — drop approve_MMDDYY_MMDDYY.approve.json here
  - Tip_Reports/ — generated outputs (PDF, XLSX, PayrollExport CSV)
  - PayrollExportTemplate.csv — roster file (Employee IDs mapping)
  - venv311/ — Python environment for runner
  - local_docs_watcher.sh — fswatch-based approval file watcher
  - tipreport_runner.sh — generates all outputs from approval JSON
  - build_from_json.py — Python script that builds reports
- workflow_specs/LPM/
  - LPM_Workflow_Master.txt — canonical specification

Main Entry Points / Scripts
1) transcribe command (local Whisper)
   - Usage: `transcribe <audio-file>`
   - Outputs .txt transcript to configured base directory
   - Depends on `.venv/bin/whisper` (install: `.venv/bin/pip install openai-whisper`)

2) Claude Code (LPM project)
   - Reads transcript, parses shifts, calculates all payroll math
   - Presents breakdown for review
   - Generates approval JSON on final approval

3) local_docs_watcher.sh
   - Watches approvals/ folder for new .approve.json files
   - Automatically triggers tipreport_runner.sh

4) tipreport_runner.sh
   - Reads approval JSON
   - Generates Tip Report PDF, Excel Summary, Toast Payroll CSV

Key Inputs
- Weekly payroll audio file (.m4a or .wav)
- Whisper transcript (.txt)
- Approval JSON: approve_MMDDYY_MMDDYY.approve.json
- PayrollExportTemplate.csv (employee roster with IDs)

Key Outputs
- approve_MMDDYY_MMDDYY.approve.json — structured payroll approval file
- TipReport_MMDDYY_MMDDYY.pdf — formatted tip report
- TipReport_MMDDYY_MMDDYY.xlsx — Excel summary workbook
- PayrollExport_MMDDYY_MMDDYY.csv — Toast import file

DO NOT CONFUSE WITH LIM INVENTORY JSON
- LPM uses payroll approval JSON: `approve_MMDDYY_MMDDYY.approve.json` with keys: out_base, header, shift_cols, per_shift, cook_tips, weekly_totals, detail_blocks.
- LIM uses inventory JSON: `MMDDYY_Inventory.json` with metadata, categories, unmapped_items. Never emit LIM JSON for LPM flows.

Environment Variables
- LPM_TRANSCRIPTS_BASE — override base directory (default: /Users/jonathanflaig/mise-core/payroll_agent/LPM)
  - Fallbacks: /Users/jonathanflaig/transcripts or /Users/jonathanflaig/Transcripts

Execution Flow
1) Record weekly payroll audio (Bluetooth mic + Motiv Audio app)
2) AirDrop audio file to Mac
3) Run: `transcribe <audio-file>`
4) Drag .txt transcript into Claude Code (LPM project)
5) Claude calculates and presents payroll breakdown
6) Review numbers, request corrections as needed
7) Say "Approved" when all numbers are correct
8) Claude generates approval JSON
9) Save approval JSON to approvals/ folder
10) Runner automatically generates PDF, XLSX, and CSV outputs
11) Import PayrollExport CSV into Toast Payroll

Notes
- Fully offline workflow (no cloud services)
- Local Whisper transcription
- Claude handles all payroll calculations and validation
- Approval JSON must conform to strict schema (see LPM_Workflow_Master.txt)
- Runner uses PayrollExportTemplate.csv to map employee names to Toast IDs
