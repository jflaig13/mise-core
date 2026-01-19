# Shifty Testing & Diagnostics

Drop audio files here to automatically test the full Mise payroll pipeline.

## Quick Start

**1. Start the test watcher:**
```bash
cd /Users/jonathanflaig/mise-core/shifty_tests
python test_shifty.py
```

**2. Drop audio files** into this directory

**3. Watch the diagnostics** in real-time

The script will automatically:
- Detect new `.wav` files
- Send them through the full pipeline
- Log every step with color-coded output
- Identify exactly where failures occur

---

## Usage

### Watch Mode (Automatic)
```bash
python test_shifty.py
```

Monitors the directory and automatically tests any new `.wav` files.

### Test Single File
```bash
python test_shifty.py path/to/audio.wav
```

### Check Services
```bash
python test_shifty.py --check-services
```

Verifies mise_app and transrouter are running.

---

## What It Tests

### Step 1: Direct Transcription
Tests: `transrouter /api/v1/audio/transcribe`
- Checks if audio → text conversion works
- Shows transcript length and preview
- **Diagnoses empty transcript issues**

### Step 2: Full Payroll Processing
Tests: `transrouter /api/v1/audio/process`
- Tests transcription + payroll parsing
- Shows approval JSON structure
- Checks employee/amount extraction

### Step 3: mise_app Integration
Tests: `mise_app /period/{id}/process`
- Full user flow (what the web app does)
- Tests shifty detection (day/shift parsing)
- Shows final redirect URL

---

## Understanding Errors

### ✗ Transcription returned empty string

**Diagnosis:** Transcription service failed to convert speech to text

**Possible causes:**
1. **Audio quality too low** - background noise, too quiet
2. **Audio format issue** - corrupt file, unsupported codec
3. **No speech detected** - silent recording, music only
4. **Transcription service down** - service not running

**How to fix:**
- Re-record with clearer audio
- Check file with: `afplay your_file.wav`
- Verify audio has speech content

### ✗ Could not detect date/shift from recording

**Diagnosis:** Transcript exists but doesn't contain recognizable shifty info

**Possible causes:**
1. Missing day of week (Monday, Tuesday, etc.)
2. Missing shift indicator (AM, PM, morning, evening)
3. Unclear pronunciation

**How to fix:**
Say explicitly:
```
"Monday AM shift. Mike $300, John $250."
```

### ✗ mise_app not accessible

**Diagnosis:** Web app not running

**How to fix:**
```bash
cd /Users/jonathanflaig/mise-core
source .venv/bin/activate
python -m mise_app.main
```

### ✗ Transrouter not accessible

**Diagnosis:** Transrouter API not running

**How to fix:**
```bash
# Check if it's running
lsof -i :8080

# Start transrouter (if you have it set up)
cd /Users/jonathanflaig/mise-core/transrouter
# ... start command ...
```

---

## Output Format

```
[12:34:56] INFO: Testing: monday_am_test.wav
==================================================================

[STEP 1] Testing direct transcription via Transrouter...
  ✓ Transcription successful!
  Transcript: "Monday AM shift. Servers Mike Walton..."

[STEP 2] Testing full payroll processing via Transrouter...
  ✓ Processing successful!
  Approval JSON keys: ['per_shift', 'detail_blocks', 'corrections']

[STEP 3] Testing through mise_app (full user flow)...
  ✓ Full flow successful!
  Shifty code: MAM
  Rows: 3
  Redirect: /period/2026-01-13/approve/MAM
```

---

## Tips

**Good test recording:**
```
"Monday AM shift.
Mike Walton three hundred dollars.
John Neal two fifty.
Kevin Worley two seventy five."
```

**Include:**
- Day of week (Monday, Tuesday, etc.)
- Shift (AM, PM, morning, evening)
- Employee names
- Dollar amounts

**Avoid:**
- Background noise
- Mumbling
- Skipping day/shift
- Ambiguous amounts ("two hundred" vs "$200")

---

## Directory Structure

```
shifty_tests/
├── README.md           # This file
├── test_shifty.py      # Test script
└── *.wav               # Your test audio files (drop here)
```

---

## Advanced Usage

**Enable debug mode (more verbose):**
Edit `test_shifty.py` and add more `log(..., "DEBUG")` statements.

**Test against production:**
Edit the script and change:
```python
MISE_APP_URL = "https://your-production-url.com"
TRANSROUTER_URL = "https://your-transrouter-url.com"
```

**Save test results:**
```bash
python test_shifty.py your_file.wav > test_results.log 2>&1
```

---

## Troubleshooting

**Script not finding services:**
Make sure both mise_app and transrouter are running:
```bash
# Terminal 1: mise_app
cd ~/mise-core
source .venv/bin/activate
python -m mise_app.main

# Terminal 2: transrouter (if separate)
# ... start transrouter ...

# Terminal 3: test watcher
cd ~/mise-core/shifty_tests
python test_shifty.py
```

**Permission denied:**
```bash
chmod +x test_shifty.py
```

**Import errors:**
```bash
cd ~/mise-core
source .venv/bin/activate
pip install requests
```

---

## Next Steps

1. Drop a test `.wav` file into this directory
2. Watch the real-time diagnostics
3. If empty transcript: check audio quality
4. If shifty detection fails: add day/shift to recording
5. Use the detailed logs to fix specific issues
