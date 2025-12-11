# Critical Workflow Paths (CPM, LIM, LPM)
Use this map to stay in the correct workflow and avoid touching unrelated code. Always read the workflow spec before editing anything.

General Rules
- Only edit files listed under the workflow you are working on.
- Do not touch other workflows’ code or specs unless explicitly directed.
- Log workflow changes in the appropriate workflow_changes folder.

Cloud Payroll Machine (CPM)
- Specs: workflow_specs/CPM/README.md
- Base code lives in /mise-core/engine
- Engine (API, parsing, validation): engine/payroll_engine.py, engine/parse_only.py, engine/commit_shift.py, engine/parse_shift.py, engine/normalizer.py, engine/tokenizer.py, engine/validator.py, engine/schemas/payroll_schema.json
- Support scripts: scripts/check_shift.sh, scripts/test_transcript.sh, scripts/test_transcript_archive.sh, scripts/convert_m4a_to_wav.sh
- Tests: tests/ (CPM-related cases)
- Change log: workflow_specs/CPM/workflow_changes/
- Do not edit LIM or LPM files when working on CPM.

Local Inventory Machine (LIM)
- Specs: workflow_specs/LIM/README.md
- Base code lives in /mise-core/mise_inventory
- Parser stack: mise_inventory/parser.py, mise_inventory/normalizer.py, mise_inventory/tokenizer.py, mise_inventory/validator.py, mise_inventory/catalog_loader.py, mise_inventory/inventory_schema.json
- CSV generation: mise_inventory/generate_inventory_file.py
- Data/catalog: data/Inventory/<DATE>_Inventory.txt, data/inventory_catalog.json
- Support scripts: scripts/convert_m4a_to_wav.sh, scripts/grow_catalog.py
- Change log: workflow_specs/LIM/workflow_changes/
- Do not edit CPM or LPM files when working on LIM.

Local Payroll Machine (LPM)
- Specs: workflow_specs/LPM/LPM_Workflow_Master.txt, workflow_specs/LPM/LPM_workflow_120925.txt
- Base code lives in /mise-core/transcribe
- Runner/watchers: transcripts/local_docs_watcher.sh, transcripts/tipreport_runner.sh, transcripts/build_from_json.py
- Templates/data: transcripts/PayrollExportTemplate.csv, transcripts/Tip_Reports/, transcripts/Whisper_Weekly_Commands_2025_2026.txt
- Change log: workflow_specs/LPM/workflow_changes/
- Do not edit CPM or LIM files when working on LPM.

Transrouter (when implemented)
- Spec: workflow_specs/transrouter/Transrouter_Workflow_Master.txt
- Summary: workflow_specs/transrouter/README.md
- Change log: workflow_specs/transrouter/workflow_changes/
- Intended code path: /mise-core/transrouter/src/ (or equivalent) for orchestrator/ASR/transrouter components (add once implemented) [implemented v1: orchestration, ASR adapters, classifier, entities, routing stubs]
