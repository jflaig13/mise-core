# Critical Workflow Paths (CPM, LIM, LPM)
Use this map to stay in the correct workflow and avoid touching unrelated code. Always read the workflow spec before editing anything.

General Rules
- Only edit files listed under the workflow you are working on.
- Do not touch other workflows’ code or specs unless explicitly directed.
- Log workflow changes in the appropriate workflow_changes folder.

Cloud Payroll Machine (CPM)
- Specs: workflow_specs/CPM/README.md
- Base code lives in /mise-core/payroll_agent/CPM
- Engine (API, parsing, validation): payroll_agent/CPM/engine/payroll_engine.py, payroll_agent/CPM/engine/parse_only.py, payroll_agent/CPM/engine/commit_shift.py, payroll_agent/CPM/engine/parse_shift.py, payroll_agent/CPM/engine/normalizer.py, payroll_agent/CPM/engine/tokenizer.py, payroll_agent/CPM/engine/validator.py, payroll_agent/CPM/engine/schemas/payroll_schema.json
- Transcribe service: payroll_agent/CPM/transcribe/app.py, payroll_agent/CPM/transcribe/cleanup/llm_cleanup.py
- Support scripts: scripts/check_shift.sh, scripts/test_transcript.sh, scripts/test_transcript_archive.sh, scripts/convert_m4a_to_wav.sh
- Tests: tests/ (CPM-related cases)
- Change log: workflow_specs/CPM/workflow_changes/
- Do not edit LIM or LPM files when working on CPM.

Local Inventory Machine (LIM)
- Specs: workflow_specs/LIM/README.md
- Base code lives in /mise-core/inventory_agent
- Parser stack: inventory_agent/parser.py, inventory_agent/normalizer.py, inventory_agent/tokenizer.py, inventory_agent/validator.py, inventory_agent/catalog_loader.py, inventory_agent/inventory_schema.json
- CSV generation: inventory_agent/generate_inventory_file.py
- Data/catalog: data/Inventory/<DATE>_Inventory.txt, data/inventory_catalog.json
- Support scripts: scripts/convert_m4a_to_wav.sh, scripts/grow_catalog.py
- Change log: workflow_specs/LIM/workflow_changes/
- Do not edit CPM or LPM files when working on LIM.

Local Payroll Machine (LPM)
- Specs: workflow_specs/LPM/LPM_Workflow_Master.txt, workflow_specs/LPM/README.md
- Base code lives in /mise-core/payroll_agent/LPM
- Runner/watchers: payroll_agent/LPM/local_docs_watcher.sh, payroll_agent/LPM/tipreport_runner.sh, payroll_agent/LPM/build_from_json.py
- Templates/data: payroll_agent/LPM/PayrollExportTemplate.csv, payroll_agent/LPM/Tip_Reports/, payroll_agent/LPM/Whisper_Weekly_Commands_2025_2026.txt
- Change log: workflow_specs/LPM/workflow_changes/
- Do not edit CPM or LIM files when working on LPM.

Transrouter (when implemented)
- Spec: workflow_specs/transrouter/Transrouter_Workflow_Master.txt
- Summary: workflow_specs/transrouter/README.md
- Change log: workflow_specs/transrouter/workflow_changes/
- Intended code path: /mise-core/transrouter/src/ (or equivalent) for orchestrator/ASR/transrouter components (add once implemented) [implemented v1: orchestration, ASR adapters, classifier, entities, routing stubs]
