#!/usr/bin/env python3
"""
Shifty Testing & Diagnostics Tool

Drop audio files into /Users/jonathanflaig/mise-core/shifty_tests/
This script will:
1. Detect new audio files
2. Send them through the full pipeline (mise_app → transrouter → transcription)
3. Log every step with detailed diagnostics
4. Identify exactly where transcription failures occur
"""

import json
import sys
import time
from pathlib import Path
from datetime import date

import requests

# Configuration
MISE_APP_URL = "http://localhost:8000"
TRANSROUTER_URL = "http://localhost:8080"  # Might be transrouter OR CPM depending on what's running
TRANSROUTER_API_KEY = "mise-core"
SHIFTY_DIR = Path("/Users/jonathanflaig/mise-core/shifty_tests")
CURRENT_PERIOD = date.today().isoformat()  # Simplified - use current date

# Auto-detect what's running on port 8080
def detect_service_on_8080():
    """Detect if port 8080 is transrouter or CPM payroll engine."""
    try:
        r = requests.get(f"{TRANSROUTER_URL}/api/v1/health", timeout=2)
        if r.status_code == 200:
            return "transrouter"
    except:
        pass

    try:
        r = requests.get(f"{TRANSROUTER_URL}/ping", timeout=2)
        if r.status_code == 200 and "database" in r.json():
            return "cpm"
    except:
        pass

    return "unknown"


def log(message, level="INFO"):
    """Log with timestamp and color."""
    colors = {
        "INFO": "\033[36m",      # Cyan
        "SUCCESS": "\033[32m",   # Green
        "ERROR": "\033[31m",     # Red
        "WARNING": "\033[33m",   # Yellow
        "DEBUG": "\033[90m",     # Gray
    }
    reset = "\033[0m"
    timestamp = time.strftime("%H:%M:%S")
    color = colors.get(level, "")
    print(f"{color}[{timestamp}] {level}: {message}{reset}")


def test_services():
    """Test that all services are running."""
    log("Testing service connectivity...", "INFO")

    # Test mise_app
    try:
        r = requests.get(f"{MISE_APP_URL}/health", timeout=5)
        if r.status_code == 200:
            log(f"✓ mise_app is running on {MISE_APP_URL}", "SUCCESS")
        else:
            log(f"✗ mise_app returned {r.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"✗ mise_app not accessible: {e}", "ERROR")
        return False

    # Detect what's on port 8080
    service_type = detect_service_on_8080()

    if service_type == "transrouter":
        log(f"✓ Transrouter is running on {TRANSROUTER_URL}", "SUCCESS")
        log(f"  (Full pipeline testing available)", "INFO")
        return True
    elif service_type == "cpm":
        log(f"⚠ CPM payroll engine detected on {TRANSROUTER_URL}", "WARNING")
        log(f"  (Transrouter not running - limited testing)", "WARNING")
        log(f"  Note: mise_app is configured to use transrouter at this URL", "WARNING")
        log(f"  You may see 'Could not detect date/shift' errors", "WARNING")
        return True
    else:
        log(f"✗ No service detected on {TRANSROUTER_URL}", "ERROR")
        log(f"  Start either transrouter OR CPM on port 8080", "WARNING")
        return False


def test_audio_file(audio_path: Path):
    """Test a single audio file through the full pipeline."""
    log(f"\n{'=' * 70}", "INFO")
    log(f"Testing: {audio_path.name}", "INFO")
    log(f"{'=' * 70}", "INFO")

    # Read audio file
    try:
        audio_bytes = audio_path.read_bytes()
        log(f"✓ Read {len(audio_bytes)} bytes from {audio_path.name}", "SUCCESS")
    except Exception as e:
        log(f"✗ Failed to read audio file: {e}", "ERROR")
        return

    # Step 1: Test direct transcription via transrouter
    log("\n[STEP 1] Testing direct transcription via Transrouter...", "INFO")
    try:
        response = requests.post(
            f"{TRANSROUTER_URL}/api/v1/audio/transcribe",
            headers={"X-API-Key": TRANSROUTER_API_KEY},
            files={"file": (audio_path.name, audio_bytes, "audio/wav")},
            timeout=120,
        )
        log(f"  Status: {response.status_code}", "DEBUG")

        if response.status_code == 200:
            result = response.json()
            transcript = result.get("transcript", "")

            if transcript:
                log(f"✓ Transcription successful!", "SUCCESS")
                log(f"  Transcript length: {len(transcript)} chars", "DEBUG")
                log(f"  Transcript preview: {transcript[:100]}...", "DEBUG")
            else:
                log(f"✗ Transcription returned empty string", "ERROR")
                log(f"  Full response: {json.dumps(result, indent=2)}", "DEBUG")
                log("\n🔍 DIAGNOSIS: Transcription service returned empty transcript", "WARNING")
                log("  Possible causes:", "WARNING")
                log("    1. Audio quality too low", "WARNING")
                log("    2. Audio file format not supported", "WARNING")
                log("    3. Transcription service error", "WARNING")
                log("    4. Audio contains no speech", "WARNING")
        else:
            log(f"✗ Transcription failed: {response.status_code}", "ERROR")
            log(f"  Response: {response.text[:500]}", "DEBUG")
    except Exception as e:
        log(f"✗ Transcription API error: {e}", "ERROR")
        return

    # Step 2: Test full payroll processing via transrouter
    log("\n[STEP 2] Testing full payroll processing via Transrouter...", "INFO")
    try:
        response = requests.post(
            f"{TRANSROUTER_URL}/api/v1/audio/process",
            headers={"X-API-Key": TRANSROUTER_API_KEY},
            files={"file": (audio_path.name, audio_bytes, "audio/wav")},
            timeout=120,
        )
        log(f"  Status: {response.status_code}", "DEBUG")

        if response.status_code == 200:
            result = response.json()
            transcript = result.get("transcript", "")
            approval_json = result.get("approval_json", {})

            if result.get("status") == "success":
                log(f"✓ Processing successful!", "SUCCESS")
                log(f"  Transcript: {transcript[:100]}...", "DEBUG")
                log(f"  Approval JSON keys: {list(approval_json.keys())}", "DEBUG")
            else:
                log(f"✗ Processing failed", "ERROR")
                log(f"  Error: {result.get('error')}", "ERROR")
                log(f"  Full response: {json.dumps(result, indent=2)}", "DEBUG")
        else:
            log(f"✗ Processing request failed: {response.status_code}", "ERROR")
            log(f"  Response: {response.text[:500]}", "DEBUG")
    except Exception as e:
        log(f"✗ Processing API error: {e}", "ERROR")

    # Step 3: Test through mise_app
    log("\n[STEP 3] Testing through mise_app (full user flow)...", "INFO")
    try:
        # Get current period ID
        period_response = requests.get(f"{MISE_APP_URL}/", allow_redirects=False, timeout=5)
        if period_response.status_code == 302:
            redirect_url = period_response.headers.get("Location", "")
            period_id = redirect_url.split("/")[-1] if "/" in redirect_url else CURRENT_PERIOD
            log(f"  Using period: {period_id}", "DEBUG")
        else:
            period_id = CURRENT_PERIOD
            log(f"  Using default period: {period_id}", "DEBUG")

        # Process audio
        response = requests.post(
            f"{MISE_APP_URL}/period/{period_id}/process",
            files={"file": (audio_path.name, audio_bytes, "audio/wav")},
            timeout=120,
        )
        log(f"  Status: {response.status_code}", "DEBUG")

        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                log(f"✓ Full flow successful!", "SUCCESS")
                log(f"  Shifty code: {result.get('shifty_code')}", "DEBUG")
                log(f"  Transcript: {result.get('transcript', '')[:100]}...", "DEBUG")
                log(f"  Rows: {len(result.get('rows', []))}", "DEBUG")
                log(f"  Redirect: {result.get('redirect_url')}", "DEBUG")
            else:
                error = result.get("error", "Unknown error")
                log(f"✗ Processing failed: {error}", "ERROR")

                if "Could not detect date/shift" in error:
                    log("\n🔍 DIAGNOSIS: Shifty detection failed", "WARNING")
                    log("  The transcript didn't contain recognizable day/shift info", "WARNING")
                    log("  Make sure your recording says:", "WARNING")
                    log("    - Day of week (Monday, Tuesday, etc.)", "WARNING")
                    log("    - Shift (AM, PM, morning, evening, etc.)", "WARNING")
                    log(f"  Actual transcript: {result.get('transcript', '(empty)')}", "DEBUG")
        else:
            log(f"✗ Request failed: {response.status_code}", "ERROR")
            try:
                error_data = response.json()
                log(f"  Error: {error_data.get('error')}", "ERROR")
            except:
                log(f"  Response: {response.text[:500]}", "DEBUG")
    except Exception as e:
        log(f"✗ mise_app API error: {e}", "ERROR")

    log(f"\n{'=' * 70}\n", "INFO")


def watch_mode():
    """Watch directory for new audio files."""
    log("=" * 70, "INFO")
    log("Shifty Test Watcher - Monitoring for audio files", "INFO")
    log("=" * 70, "INFO")
    log(f"Drop .wav files into: {SHIFTY_DIR}", "INFO")
    log("Watching for changes (Ctrl+C to stop)...\n", "INFO")

    # Test services first
    if not test_services():
        log("\n✗ Services not ready. Fix issues and try again.", "ERROR")
        return

    log("\n✓ All services ready!", "SUCCESS")
    log("Waiting for audio files...\n", "INFO")

    processed = set()

    try:
        while True:
            # Find new WAV files
            wav_files = list(SHIFTY_DIR.glob("*.wav"))

            for wav_file in wav_files:
                if wav_file not in processed:
                    processed.add(wav_file)
                    test_audio_file(wav_file)

            time.sleep(2)
    except KeyboardInterrupt:
        log("\n\nStopped watching.", "INFO")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Test shifty audio files")
    parser.add_argument("file", nargs="?", help="Audio file to test (or watch mode if omitted)")
    parser.add_argument("--check-services", action="store_true", help="Just check if services are running")

    args = parser.parse_args()

    if args.check_services:
        test_services()
        return

    if args.file:
        # Test single file
        audio_path = Path(args.file)
        if not audio_path.exists():
            log(f"File not found: {audio_path}", "ERROR")
            sys.exit(1)

        if not test_services():
            log("\n✗ Services not ready. Fix issues and try again.", "ERROR")
            sys.exit(1)

        test_audio_file(audio_path)
    else:
        # Watch mode
        watch_mode()


if __name__ == "__main__":
    main()
