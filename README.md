# Mise Core

This repository hosts the core services for Mise, the hospitality-focused assistant. The codebase is split into small, purpose-driven modules so it is easy to reason about and deploy.

## Project layout

- `engine/` — FastAPI payroll engine exposed as `engine.app:app`.
- `transcribe/` — Whisper-based transcription service served from `transcribe/app.py`.
- `*.sh` at the repo root — Shell helpers for local automation (watchers, converters, and deployment scripts).
- `data/` — Structured inputs such as JSON inventories (kept at the repo root today).

If you move files, remember to adjust any scripts or Docker COPY statements that reference their paths.

## Running the services

### Payroll engine (FastAPI)
- Entrypoint: `engine.app:app`.
- Container build: `docker build -t payroll-engine .` (uses the root `Dockerfile`).
- Runtime command (from the Dockerfile): `uvicorn engine.app:app --host 0.0.0.0 --port 8080`.

### Transcriber (Whisper)
- Entrypoint: `app:app` inside `transcribe/app.py`.
- Container build: `docker build -t payroll-transcribe transcribe` (uses `transcribe/Dockerfile`).
- Runtime command (from that Dockerfile): `uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1`.

## Local utilities

- `redeploy.sh` now resolves its working directory from the script location so it can be run from any folder after cloning `mise-core`.
- `watcher_approval.sh` defaults to `PYTHON_BIN=$HOME/mise-core/venv/bin/python3`; set `PYTHON_BIN` if your virtual environment lives elsewhere.

These scripts watch audio folders, preview payroll ingests, and push refreshed containers to Cloud Run. Keep their path variables in sync with any future directory changes.
