# Transrouter Workflow (Summary)

Purpose
- Universal voice-to-intent front door for Mise: ingest audio → transcribe → interpret → route to the correct domain agent (payroll, inventory, scheduling, ordering, general assistant, etc.).
- Acts like NotebookLM’s podcast interaction layer: hears, understands, and routes intelligently.

Core Responsibilities
- Audio ingestion: accept raw audio payloads.
- Transcription: run ASR (Whisper/Amazon Transcribe/other) internally to produce clean text.
- Interpretation & routing: classify intent, pick domain agent, extract entities, and dispatch; never emit the wrong schema.

Key Artifacts (see Transrouter_Workflow_Master.txt for full spec)
- Input contract: audio_bytes + format + metadata; output transcript with confidence.
- RoutingDecision: { domain_agent, intent_type, entities, raw_transcript, confidence }.
- AgentRequest/Response: wraps routing decision and calls the domain agent.
- Brains: transrouter_brain plus cloned domain brains under /brains (never mutates canonical domain brains).

Safety Boundaries
- Do not mix domains; wrong schema must never be emitted.
- Ambiguity → ask for clarification or route to general_assistant.
- Financial sensitivity: payroll interpretations must be strict.
- Non-destructive: transrouter does not modify domain data.

Non-Goals
- Does not generate approval JSON/PDF/CSV or perform payroll/inventory math.
- Only: Transcribe → Understand → Route.

Layout
- Master spec: Transrouter_Workflow_Master.txt
- Change log: workflow_changes/ (dated entries)
- Critical paths: add transrouter entry to workflow_specs/CRITICAL_PATHS.md when code paths are defined.
