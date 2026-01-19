# CPM Local Development Environment

Complete local Docker testing environment for the CPM (Cloud Payroll Machine) payroll engine.

## ⚠️ IMPORTANT: When to Use This

**CPM Docker is for ISOLATED payroll engine testing ONLY.**

### ❌ DON'T Use CPM Docker When:
- Running the full Mise web app
- Using mise_app + transrouter
- Testing end-to-end shifty flows

**Why:** CPM Docker uses port 8080, which conflicts with transrouter.

### ✅ DO Use CPM Docker When:
- Testing payroll parsing logic changes in isolation
- Debugging database backends (BigQuery ↔ PostgreSQL)
- Running payroll-specific unit/integration tests
- NOT using the full Mise app

### Clean Architecture Check

Before starting CPM Docker, verify no conflicts:
```bash
# From mise-core root
scripts/check-ports

# If transrouter is running, you'll see a warning
# Stop CPM before using full Mise:
cd payroll_agent/CPM
make down
```

See `/Users/jonathanflaig/mise-core/START_MISE.md` for the correct full Mise setup.

---

## Quick Start

```bash
cd payroll_agent/CPM
make up              # Start all services
make test            # Run tests
make logs            # View logs
```

The payroll engine will be available at `http://localhost:8080`.

## Architecture

```
┌─────────────────────────────────────────┐
│  Payroll Engine (FastAPI)               │
│  Port: 8080                              │
│  ├─ /ping          Health check         │
│  ├─ /parse_only    Preview (no commit)  │
│  └─ /commit_shift  Save to database     │
└──────────┬──────────────────────────────┘
           │
           ├──→ Mock Transcriber (Port: 8081)
           │    Returns fixture-based transcripts
           │
           └──→ PostgreSQL (Port: 5432)
                Local database for shifts
```

## Services

### 1. Payroll Engine (`localhost:8080`)
FastAPI application with database abstraction layer.
- **Production**: Uses BigQuery backend
- **Local**: Uses PostgreSQL backend

### 2. Mock Transcriber (`localhost:8081`)
Returns pre-recorded transcripts from fixture files.
- Eliminates dependency on real transcription service
- Deterministic testing with known outputs

### 3. PostgreSQL (`localhost:5432`)
Local database mirroring BigQuery schema exactly.
- User: `payroll_user`
- Password: `payroll_pass`
- Database: `payroll`

## Development Workflow

### 1. Start Services
```bash
make up
```

Wait ~30 seconds for all services to be healthy.

### 2. Test a Fixture
```bash
# Create test audio file (name matches fixture)
touch /tmp/monday_am_simple.wav

# Parse without committing
curl -X POST http://localhost:8080/parse_only \
  -F "audio=@/tmp/monday_am_simple.wav" \
  -F "shift=AM"
```

### 3. Make Code Changes
Source code is mounted as a volume - changes trigger hot reload:
- Edit `payroll_agent/CPM/engine/payroll_engine.py`
- Wait ~2 seconds for reload
- Test immediately

### 4. Run Tests
```bash
make test              # All tests
make test-integration  # Integration tests only
```

### 5. View Logs
```bash
make logs                                        # All services
docker-compose logs -f payroll_engine           # Engine only
docker-compose logs -f mock_transcriber         # Transcriber only
```

### 6. Database Operations
```bash
make db-shell          # Connect to PostgreSQL
make reset             # Delete all data
```

Inside `db-shell`:
```sql
SELECT * FROM shifts_summary LIMIT 10;
SELECT employee, SUM(amount_final) FROM shifts GROUP BY employee;
```

## Test Fixtures

Fixtures are JSON files in `local_dev/fixtures/`:

### Available Fixtures

| Fixture | Description | Expected Rows |
|---------|-------------|---------------|
| `monday_am_simple.json` | Simple 3-server shift | 3 |
| `tuesday_pm_with_utility.json` | Servers + utility | 3 |
| `complex_roles.json` | Multiple roles (expo, busser, etc.) | 6 |
| `whisper_hallucinations.json` | Name normalization tests | 4 |
| `edge_case_amounts.json` | Amount parsing edge cases | 4 |
| `real_test_123025_AM.json` | Real test case from logs | 3 |

### Creating New Fixtures

1. Create JSON file in `local_dev/fixtures/`:
```json
{
  "description": "Your test case",
  "filename": "your_test.wav",
  "expected_rows": 3,
  "transcript": "Monday AM. Mike $300, John $250, Kevin $275."
}
```

2. Create matching WAV file (mock transcriber matches by filename):
```bash
touch /tmp/your_test.wav
```

3. Test it:
```bash
curl -X POST http://localhost:8080/parse_only \
  -F "audio=@/tmp/your_test.wav" \
  -F "shift=AM"
```

## Environment Variables

All configuration is in `docker-compose.yml`:

| Variable | Local Value | Production Value |
|----------|-------------|------------------|
| `DATABASE_BACKEND` | `postgres` | `bigquery` |
| `POSTGRES_HOST` | `postgres` | N/A |
| `TRANSCRIBE_BASE` | `http://mock_transcriber:8081` | Cloud Run URL |
| `PROJECT_ID` | `local-dev` | GCP project ID |

## Common Tasks

### Add a New Employee to Roster
1. Edit `workflow_specs/roster/employee_roster.json`
2. Add name variants → canonical name mapping
3. Restart services: `make down && make up`

### Debug Parsing Logic
1. Add print statements to `payroll_engine.py`
2. Save file (hot reload triggers)
3. View logs: `make logs`

### Reset Everything
```bash
make clean   # Removes containers and volumes
make up      # Fresh start
```

## Troubleshooting

### Services Won't Start
```bash
# Check if ports are in use
lsof -i :8080
lsof -i :8081
lsof -i :5432

# View detailed logs
docker-compose logs
```

### Database Connection Errors
```bash
# Verify PostgreSQL is healthy
docker-compose ps

# Check database logs
docker-compose logs postgres

# Connect manually
make db-shell
```

### Mock Transcriber Not Matching Fixtures
The mock transcriber matches by filename stem:
- `monday_am_simple.wav` → matches `monday_am_simple.json`
- `hallucinations.wav` → matches `hallucinations.json`

Ensure your WAV filename (without extension) matches a fixture filename.

### Hot Reload Not Working
Volume mounts must be correct in `docker-compose.yml`:
```yaml
volumes:
  - ../../../payroll_agent:/app/payroll_agent
  - ../../../roster:/app/roster
```

Restart services: `make down && make up`

## Production Deployment

This local setup is **separate** from Cloud Run deployment.

To deploy to production:
```bash
cd payroll_agent/CPM/engine
./deploy.sh
```

Production uses:
- `DATABASE_BACKEND=bigquery`
- Real transcriber service
- Standard `Dockerfile` (not `Dockerfile.local`)

## Performance Benchmarks

- **Full stack startup**: ~30 seconds
- **Parse request**: <1 second
- **Hot reload**: ~2 seconds
- **Integration test suite**: ~10 seconds

Compare to Cloud Run deployment: 5+ minutes per iteration.

## Success Criteria

✅ Parse logic changes testable in <10 seconds
✅ Full stack startup in <30 seconds
✅ 6+ test fixtures covering edge cases
✅ PostgreSQL schema matches BigQuery exactly
✅ Zero impact on Cloud Run deployment
