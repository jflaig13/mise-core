# Mise Core – Agent Onboarding

This repo houses multiple workflows. Read the relevant workflow doc before making changes and obey its rules. First: learn my rules → see AGENT_POLICY.md.

Workflows
- Cloud Payroll Machine (CPM): workflow_specs/CPM/README.md
- Local Inventory Machine (LIM): workflow_specs/LIM/README.md
- Local Payroll Machine (LPM): workflow_specs/LPM/LPM_Workflow_Master.txt

Critical paths map: workflow_specs/CRITICAL_PATHS.md
Workflow rules (all workflows): workflow_specs/README.md

Spec Template
- Generate a new machine spec: `./get_workflow "Machine Name" > docs/<machine>.md` (create docs/ as needed).

Change Logs
- LPM: workflow_specs/LPM/workflow_changes/
- CPM: workflow_specs/CPM/workflow_changes/
- LIM: workflow_specs/LIM/workflow_changes/

Defaults and Bases
- Transcripts base (LPM): ~/mise-core/transcripts (override with LPM_TRANSCRIPTS_BASE)
- Transcription outputs: ~/mise-core/transcripts
- Inventory assets: data/Inventory/, mise_inventory/
- Cloud payroll: engine/, transcribe/

Agent Checklist (Claude/Gemini/Codex/etc.)
- Read the workflow doc for the system you touch.
- Do not change schemas or workflows unless explicitly directed.
- Respect naming conventions and base paths.
- Log workflow changes in the appropriate workflow_changes folder.
- Keep secrets out of git; use env vars or ignored .env files.

Quick setup for new agents (local):
- python3 -m venv .venv
- .venv/bin/pip install -r requirements.txt openai-whisper
