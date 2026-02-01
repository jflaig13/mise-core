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

3. **`transrouter/src/prompts/payroll_prompt.py`** - Partial tipout calculation fix
   - Added complete worked example for support staff taking a break on AM shift
   - Clarified: Server only pays support staff's EARNED portion, NOT full tipout
   - Example: Ryan takes 2hr break → works 69.2% → gets 69.2% of tipout
   - Austin pays $6.65 (Ryan's earned portion), NOT $9.60 (full tipout)

4. **`transrouter/src/agents/payroll_agent.py`** - Filter invalid employee names
   - Added filter to reject names starting with "So", "And", "But", "Wait", "Actually", etc.
   - Prevents chain-of-thought phrases like "So Austin" being parsed as employee names

5. **`transrouter/src/prompts/payroll_prompt.py`** - No chain-of-thought in detail_blocks
   - Added explicit instruction: detail_blocks must contain ONLY clean calculations
   - NO "Wait, let me recalculate...", "Actually...", "Hmm...", etc.

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
5. Test partial tipout: "Thursday AM, utility was Ryan, he took a 2 hour break, Austin $44.95, food sales $192"
   - Ryan should get $6.65 (69.2% of $9.60), NOT $3.84
   - Austin should get $38.30 ($44.95 - $6.65), NOT $35.35
   - Only 2 employees should appear (Austin + Ryan), NOT 3 (no "So Austin")
6. Verify detail_blocks show clean calculations, NOT chain-of-thought reasoning
