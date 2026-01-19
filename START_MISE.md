# Starting Mise - Clean Setup Guide

## ✅ Correct Architecture (What You Should Have Running)

```
┌─────────────────────────────────────────┐
│  Port 8000: mise_app (Web UI)           │
│  - User interface                        │
│  - Forms, approval pages, totals         │
└──────────┬──────────────────────────────┘
           │
           │ HTTP calls
           ↓
┌─────────────────────────────────────────┐
│  Port 8080: Transrouter (API Gateway)   │
│  - Routes to domain agents               │
│  - Handles audio/text processing         │
│  - Payroll, Inventory, Scheduling, etc.  │
└─────────────────────────────────────────┘
```

**CPM Docker: NOT RUNNING** (only for isolated payroll testing)

---

## 🚀 Quick Start (Every Time)

### 1. Check Ports (Safety Check)

```bash
/Users/jonathanflaig/mise-core/scripts/check-ports
```

**Expected output:**
```
✅ All services configured correctly!

Active services:
  - mise_app:    http://localhost:8000
  - transrouter: http://localhost:8080
```

**If you see errors:**
- CPM Docker running? → `cd payroll_agent/CPM && make down`
- mise_app not running? → Start it (see below)
- Transrouter not running? → Start it (see below)

---

### 2. Start Services (If Not Running)

**mise_app (Web UI):**
```bash
cd /Users/jonathanflaig/mise-core
source .venv/bin/activate
python -m mise_app.main

# Keep this terminal running
# Access: http://localhost:8000
```

**Transrouter (API Gateway):**
```bash
cd /Users/jonathanflaig/mise-core
source .venv/bin/activate
uvicorn transrouter.api.main:app --port 8080 --host 0.0.0.0

# Keep this terminal running
# Access: http://localhost:8080/api/v1/health
```

---

### 3. Verify Full Stack

```bash
# Check all services
/Users/jonathanflaig/mise-core/scripts/check-ports

# Test shifty pipeline
cd /Users/jonathanflaig/mise-core/shifty_tests
./watch
# Drop a .wav file and verify diagnostics show all green
```

---

## ⚠️ Common Mistakes to Avoid

### ❌ DON'T: Start CPM Docker with Transrouter

**Wrong:**
```bash
# DON'T DO THIS when running mise_app
cd payroll_agent/CPM
make up  # ← This conflicts with transrouter!
```

**Why:** CPM Docker uses port 8080, which transrouter needs.

**When to use CPM Docker:**
- ONLY when testing payroll engine in isolation
- NOT when using the full Mise web app

---

### ❌ DON'T: Forget to Stop CPM Before Using Mise

**Wrong:**
```bash
# CPM is running from yesterday...
# Now try to use mise_app
# → Empty transcripts, errors
```

**Fix:**
```bash
cd payroll_agent/CPM
make down
scripts/check-ports  # Verify clean
```

---

## 🔧 When to Use What

### Normal Mise Development (Most Common)

**Use:**
- mise_app on 8000 ✅
- Transrouter on 8080 ✅
- CPM Docker STOPPED ❌

**For:**
- Testing full web app
- End-to-end shifty processing
- Normal restaurant operations

**Start:**
```bash
# Terminal 1: mise_app
python -m mise_app.main

# Terminal 2: transrouter
uvicorn transrouter.api.main:app --port 8080

# Terminal 3: test watcher
cd shifty_tests && ./watch
```

---

### CPM Payroll Engine Testing (Isolated)

**Use:**
- CPM Docker on 8080 ✅
- Transrouter STOPPED ❌
- mise_app STOPPED ❌

**For:**
- Testing CPM parsing logic changes
- Quick payroll-only iterations
- Database backend testing

**Start:**
```bash
# Stop transrouter first!
pkill -f "uvicorn transrouter"

# Start CPM
cd payroll_agent/CPM
make up

# Test directly
curl http://localhost:8080/ping
```

**Remember to clean up after:**
```bash
cd payroll_agent/CPM
make down
```

---

## 📋 Daily Workflow Checklist

**Morning (starting work):**
- [ ] Run `scripts/check-ports`
- [ ] Start mise_app if needed
- [ ] Start transrouter if needed
- [ ] Verify: `scripts/check-ports` shows all green

**During development:**
- [ ] Drop test files in `shifty_tests/`
- [ ] Watch diagnostics for issues
- [ ] Make code changes
- [ ] Test immediately

**Evening (ending work):**
- [ ] Commit code changes
- [ ] Stop services (or leave running overnight)
- [ ] If stopping: just close terminals

---

## 🆘 Troubleshooting

### "Empty transcript" errors

**Check:**
```bash
scripts/check-ports
```

**Fix:**
- If CPM detected on 8080 → `cd payroll_agent/CPM && make down`
- If transrouter not running → Start it
- Run port check again

### Services not responding

**Check what's actually running:**
```bash
lsof -i :8000  # mise_app
lsof -i :8080  # transrouter
docker ps | grep cpm  # CPM Docker (should be empty)
```

**Restart everything:**
```bash
# Stop CPM if running
cd payroll_agent/CPM && make down

# Kill any stray processes
pkill -f "uvicorn"
pkill -f "mise_app"

# Start clean
# Terminal 1: mise_app
python -m mise_app.main

# Terminal 2: transrouter
uvicorn transrouter.api.main:app --port 8080

# Verify
scripts/check-ports
```

---

## 🎯 Clean State Guarantee

**To guarantee a clean state anytime:**

```bash
cd /Users/jonathanflaig/mise-core

# Kill everything
pkill -f "mise_app"
pkill -f "uvicorn"
cd payroll_agent/CPM && make down && cd ../..

# Start fresh
# Terminal 1
source .venv/bin/activate
python -m mise_app.main

# Terminal 2
source .venv/bin/activate
uvicorn transrouter.api.main:app --port 8080 --host 0.0.0.0

# Verify
scripts/check-ports
```

---

## 📊 Service Health Dashboard

**Quick status check:**
```bash
echo "mise_app:    $(curl -s http://localhost:8000/health | jq -r .status)"
echo "transrouter: $(curl -s http://localhost:8080/api/v1/health | jq -r .status)"
echo "CPM Docker:  $(docker ps | grep -q cpm && echo 'RUNNING (wrong!)' || echo 'stopped (correct)')"
```

---

## 📝 Remember

1. **CPM Docker is for isolated testing only**
2. **Always run `check-ports` when things seem weird**
3. **Full Mise = mise_app + transrouter, NO CPM Docker**
4. **shifty_tests/watch will tell you if something's wrong**

Keep this guide handy! Bookmark: `/Users/jonathanflaig/mise-core/START_MISE.md`
