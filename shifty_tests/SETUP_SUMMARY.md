# Shifty Testing Setup - Summary

## ✅ What You Have Now

A complete testing system for diagnosing Mise payroll audio processing issues.

**Location:** `/Users/jonathanflaig/mise-core/shifty_tests/`

---

## 🚀 Quick Start (2 commands)

```bash
cd /Users/jonathanflaig/mise-core/shifty_tests
./watch
```

Then drop `.wav` audio files into this folder and watch real-time diagnostics.

---

## 📁 Files Created

```
shifty_tests/
├── watch                # Quick start script
├── test_shifty.py       # Main diagnostic tool
├── README.md            # Full documentation
└── SETUP_SUMMARY.md     # This file
```

---

## 🔍 What It Diagnoses

When you drop a `.wav` file, it tests:

1. **Transcription** - Did audio → text conversion work?
2. **Payroll Parsing** - Did it extract employees/amounts?
3. **Shifty Detection** - Did it detect the day/shift?
4. **Full Pipeline** - Does the complete flow work?

**Shows exactly where failures occur** with color-coded output.

---

## 🐛 Diagnosing Empty Transcript Issue

**The problem you mentioned:**
> "mise web app returns no transcription whatsoever, returns '', says 'try speaking a bit more clearly'"

**How this tool helps:**

```bash
# Drop your problematic audio file into shifty_tests/
# The tool will show:

[STEP 1] Testing direct transcription...
  ✗ Transcription returned empty string  ← ROOT CAUSE FOUND

🔍 DIAGNOSIS: Transcription service returned empty transcript
  Possible causes:
    1. Audio quality too low
    2. Audio file format not supported
    3. Transcription service error
    4. Audio contains no speech
```

It pinpoints **exactly which service failed** and **why**.

---

## 🎯 Current Setup Detected

Your current configuration:
- ✓ **mise_app** running on port 8000 (web UI)
- ⚠ **CPM payroll engine** running on port 8080
- ⚠ **Transrouter NOT running**

**Note:** mise_app expects transrouter on port 8080, but CPM is there instead.
This might cause "Could not detect date/shift" errors in the web app.

---

## 🔧 To Fix Empty Transcript Issues

### Scenario 1: Audio Quality Problem

**Test:**
```bash
cd shifty_tests
./watch
# Drop your .wav file
# Check Step 1 output
```

**If it says "empty transcript":**
- Re-record with clearer audio
- Reduce background noise
- Speak louder and more clearly

### Scenario 2: Service Not Running

**Test:**
```bash
python test_shifty.py --check-services
```

**If transrouter shows error:**
- Start transrouter (if you have it configured)
- OR accept limited functionality with CPM only

### Scenario 3: API Configuration

**Check:**
```python
# mise_app/config.py line 97-98
transrouter_url: str = "http://localhost:8080"
transrouter_api_key: str = "mise-core"
```

Make sure this matches your actual setup.

---

## 📝 Example Session

```bash
$ cd shifty_tests
$ ./watch

🎤 Shifty Test Watcher
Drop .wav files into: /Users/jonathanflaig/mise-core/shifty_tests

[01:46:32] INFO: Testing service connectivity...
[01:46:32] SUCCESS: ✓ mise_app is running
[01:46:32] WARNING: ⚠ CPM detected on port 8080
[01:46:32] INFO: ✓ All services ready!
[01:46:32] INFO: Waiting for audio files...

# You drop monday_am.wav into the folder

[01:47:15] INFO: Testing: monday_am.wav
==================================================================
[STEP 1] Testing direct transcription...
  ✓ Transcription successful!
  Transcript: "Monday AM shift. Mike three hundred..."

[STEP 2] Testing payroll processing...
  ✓ Processing successful!
  Rows: 3 employees found

[STEP 3] Testing mise_app integration...
  ✓ Full flow successful!
  Redirect: /period/2026-01-13/approve/MAM
```

---

## 🆘 Getting Help

**If you see errors:**

1. Check the color-coded output
2. Read the DIAGNOSIS section
3. Follow the suggestions
4. Check README.md for detailed troubleshooting

**Common fixes:**
- Empty transcript → Better audio quality
- Service not running → Start mise_app/transrouter
- Shifty detection failed → Say day/shift clearly

---

## 📚 More Info

- **Full documentation:** `README.md`
- **Test single file:** `python test_shifty.py your_file.wav`
- **Check services:** `python test_shifty.py --check-services`

---

**Now go drop an audio file in `shifty_tests/` and see the diagnostics!** 🎤
