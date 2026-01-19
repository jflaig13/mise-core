# Mise Audio Archive

**⚠️ PERMANENT STORAGE — NEVER DELETE FILES FROM THIS DIRECTORY**

## Purpose

This directory contains a **complete archive of every audio recording** ever made in Mise. These files serve as:

1. **Audit Trail** — Proof of what was recorded and when
2. **Dispute Resolution** — Can re-listen to original audio if there's a question about payroll
3. **Re-processing** — If parsing logic improves, we can reprocess old recordings
4. **Historical Analysis** — Data for training future models
5. **Legal Protection** — Evidence of accurate record-keeping

## Organization

```
recordings/
├── 2025-01-12/          # Pay period (Sunday start date)
│   ├── MAM_20260118_193000.wav
│   ├── TPM_20260118_194500.wav
│   └── ...
├── 2025-01-19/
│   └── ...
└── README.md (this file)
```

**Directory naming:** Pay period start date (Sunday) in `YYYY-MM-DD` format

**File naming:** `{shifty_code}_{timestamp}.{ext}`
- `shifty_code`: MAM, TAM, WAM, ThAM, FAM, SaAM, SuAM, MPM, TPM, etc.
- `timestamp`: YYYYMMDD_HHMMSS (when uploaded, not when shift occurred)
- `ext`: .wav, .webm, .m4a, .mp3

## Retention Policy

**NEVER DELETE FILES FROM THIS DIRECTORY.**

- Even old recordings should be kept indefinitely
- Disk space is cheap compared to lost data
- These files are excluded from git (via .gitignore)
- Consider backing up to external drive quarterly

## Size Management

If disk space becomes an issue:

1. **Compress old recordings** (zip by year, keep in same directory)
2. **Move to external storage** (NAS, external drive, cloud backup)
3. **DO NOT DELETE** — move, don't remove

## Backup Strategy

**Local archive (this directory):**
- Primary storage
- Fast access for recent recordings

**Future cloud backup (optional):**
- Google Drive: `Papa Staff Resources/Payroll Voice Recordings/`
- S3 or similar for long-term archival
- Automated backup after each recording

## Access

These files are:
- ✅ Safe to listen to (for verification)
- ✅ Safe to copy (for backup)
- ✅ Safe to compress (for space savings)
- ❌ **NEVER delete or modify**

## File Integrity

Each recording is written once and never modified. If you need to verify a file hasn't been tampered with, check:

1. **File size** — Should match what's in logs
2. **Timestamp** — Should match upload time in logs
3. **Audio duration** — Listen to verify it plays correctly

## Questions?

If you're unsure whether to delete something from this directory:

**DON'T DELETE IT.**

Contact Jon first.

---

**Created:** 2026-01-18
**Last Updated:** 2026-01-18
