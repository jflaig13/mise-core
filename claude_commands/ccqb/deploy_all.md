# Deploy Both Services - Transrouter + Mise

**CRITICAL: Deploy both mise-transrouter AND mise. Do not skip either.**

## Service 1: mise-transrouter

**Changes made to transrouter:**

1. **`transrouter/src/agents/payroll_agent.py`** - Tipout calculation fix
   - `_check_detail_block_consistency()` and `_auto_correct_approval_json()` now extract AFTER tipout amounts
   - Old: matched `"Austin Kelley: $155.13"` (before tipout)
   - New: matches `"Austin Kelley: $155.13 - $16.50 = $138.63"` and extracts `$138.63` (after tipout)

2. **`transrouter/src/prompts/payroll_prompt.py`** - Calendar fix for day-of-week
   - Added `detect_date_from_transcript()` function that uses Python's calendar
   - Updated `build_payroll_user_prompt()` to tell Claude the ACTUAL day-of-week
   - Example: "January 19, 2026 is a MONDAY. Use MPM for PM shift."
   - Claude can no longer guess dates wrong

**Deploy command:**
```bash
cd /Users/jonathanflaig/mise-core/transrouter
gcloud builds submit --tag us-central1-docker.pkg.dev/automation-station-478103/mise-registry/mise-transrouter:latest
gcloud run deploy mise-transrouter --image us-central1-docker.pkg.dev/automation-station-478103/mise-registry/mise-transrouter:latest --region us-central1 --project automation-station-478103
```

## Service 2: mise

**Changes made to mise_app:**

1. **`mise_app/routes/recording.py`** - Shift code remapping safety net
   - Added `fix_approval_json_shift_codes()` function
   - If Claude still returns wrong shift codes, mise remaps them to the correct one

2. **`mise_app/templates/approve.html`** - Show Calculations UI
   - Collapsible "Show Calculations" section displaying detail_blocks

3. **`mise_app/local_storage.py`** - Store detail_blocks
   - `add_shifty()` now accepts and stores `detail_blocks` parameter

**Deploy command:**
```bash
cd /Users/jonathanflaig/mise-core/mise_app
gcloud builds submit --tag us-central1-docker.pkg.dev/automation-station-478103/mise-registry/mise:latest
gcloud run deploy mise --image us-central1-docker.pkg.dev/automation-station-478103/mise-registry/mise:latest --region us-central1 --project automation-station-478103
```

## Environment Variables (VERIFY THESE ARE SET)

**mise-transrouter:**
- `ANTHROPIC_API_KEY` - for Claude
- `OPENAI_API_KEY` - for Whisper transcription

**mise:**
- `TRANSROUTER_URL=https://mise-transrouter-147422626167.us-central1.run.app`

## Verification After Deploy

1. Record a test shifty saying "January 20th PM shift" (today is Tuesday)
2. Verify it detects as **TPM** (Tuesday PM), not some other day
3. Verify tipout amounts show AFTER tipout (e.g., $138.63 not $155.13)
4. Verify "Show Calculations" section appears on approval page
