# Transrouter — Shelved (Not Deleted)

**Date:** 2026-02-06
**Reason:** mise_app now calls domain agents directly via `mise_app/agent_service.py`.

## What's Still Actively Used

The following code is imported directly by `mise_app/agent_service.py`:

- `src/agents/payroll_agent.py` — PayrollAgent (parses payroll transcripts)
- `src/agents/inventory_agent.py` — InventoryAgent (parses inventory transcripts)
- `src/prompts/payroll_prompt.py` — Payroll system prompt builder
- `src/prompts/inventory_prompt.py` — Inventory system prompt builder
- `src/claude_client.py` — ClaudeClient (Anthropic API wrapper)
- `src/asr_adapter.py` — ASR provider (Whisper / OpenAI Whisper API)
- `src/conversation_manager.py` — Multi-turn clarification flow
- `src/schemas.py` — Shared data schemas

## What's Dormant

These components are preserved but no longer called at runtime:

- `src/transrouter_orchestrator.py` — Audio pipeline (transcribe → classify → route)
- `src/intent_classifier.py` — Intent classification
- `src/entity_extractor.py` — Entity extraction
- `src/domain_router.py` — Domain routing
- `api/` — FastAPI HTTP layer (routes, middleware, app factory)

## Why Shelved

The user already selects the domain (Payroll or Inventory) in the UI — there's
nothing to route. Direct Python imports are faster and simpler than HTTP round-trips
to a separate service.

## Revival Plan

The orchestrator, intent classifier, and domain router will be revived when
Mise moves to a voice-first architecture where the user speaks naturally and
the system must determine intent from speech alone.
