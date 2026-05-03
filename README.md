# FieldFix AI
Offline multimodal repair copilot — Fix Anything, Offline.

---

## Backend (FastAPI — Mock Mode)

### Prerequisites
- Python 3.13
- Virtual environment at `.venv/` (already initialized)

### Install
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### API Docs
Open in browser after starting: `http://localhost:8000/docs`

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check — returns status, mode, kb_chunks |
| GET | `/rag/status` | RAG collection stats (total chunks, per-category counts) |
| POST | `/rag/search` | Semantic search over knowledge base |
| POST | `/safety/check` | Safety classifier — returns `SafetyOutput` |
| POST | `/repair/analyze` | Submit symptom + optional category, returns `RepairOutput` JSON |
| POST | `/memory/{device_id}` | Save repair result to device history |
| GET | `/memory/{device_id}` | Fetch repair history for a device |
| DELETE | `/memory/{device_id}` | Clear repair history for a device |

### Request body (`POST /repair/analyze`)
```json
{
  "symptom": "string (required)",
  "category": "robotics | electronics | emergency_equipment | household | safety | unknown (optional)",
  "image_description": "string (optional)"
}
```

### Mock routing

| Keyword(s) or category | Demo returned |
|------------------------|---------------|
| `"servo"`, `"buzzing"`, `"robotic"`, or `category=robotics` | `demos/servo_buzzing/` |
| `"raspberry"`, `" pi "`, `"boot"`, `"rpi"` | `demos/raspberry_pi_not_booting/` |
| `"flashlight"`, `"generator"`, `"emergency"`, `"torch"` | `demos/flashlight_dead/` |
| `"hinge"`, `"faucet"`, `"cabinet"`, `"furniture"`, or `category=household` | `demos/household_quick_fix/` |

Returns `400` if no category or keyword match is found.
Returns `422` with `SafetyOutput` body if symptom is critical or high risk.

---

## Running with Gemma (Ollama)

### One-time setup
```bash
brew install ollama
ollama pull gemma3:4b      # ~2.5 GB, downloads once
ollama serve               # runs on http://localhost:11434
```

### Start backend (Gemma mode)
```bash
source .venv/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
# Backend auto-detects Ollama and switches to "ollama" mode
```

### Fast demo (no Ollama required)
```bash
USE_MOCK=true uvicorn backend.main:app --reload
# Returns pre-built demo JSON instantly — no model needed
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_MOCK` | `false` | `true` = always return demo JSON, skip Gemma |
| `GEMMA_MODEL` | `gemma3:4b` | Ollama model name |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server base URL |
| `GEMMA_TIMEOUT` | `60` | Request timeout in seconds |

Copy `.env.example` → `.env` and adjust as needed.

---

## Running Tests
```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

### Example requests
```bash
curl -X POST http://localhost:8000/repair/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptom": "servo is buzzing near certain angles", "category": "robotics"}'

curl -X POST http://localhost:8000/repair/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptom": "raspberry pi not booting"}'

curl -X POST http://localhost:8000/repair/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptom": "flashlight dead in field"}'

curl -X POST http://localhost:8000/repair/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptom": "cabinet hinge is loose", "category": "household"}'
```
