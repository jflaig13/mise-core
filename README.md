# Mise Core – Agent Onboarding

This repo houses multiple workflows. Read the relevant workflow doc before making changes and obey its rules.

Workflows
- Cloud Payroll Machine (CPM): transcribe/README.md
- Local Inventory Machine (LIM): mise_inventory/README.md
- Local Payroll Machine (LPM): transcripts/LPM_Workflow_Master.txt

Spec Template
- Generate a new machine spec: `./get_workflow "Machine Name" > docs/<machine>.md` (create docs/ as needed).

Change Logs
- LPM: transcripts/workflow_changes/
- CPM: transcribe/workflow_changes/ (create as needed)
- LIM: mise_inventory/workflow_changes/ (create as needed)

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
