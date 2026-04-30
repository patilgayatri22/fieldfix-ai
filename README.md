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
| GET | `/health` | Health check — returns `{"status":"ok","mode":"mock"}` |
| POST | `/repair/analyze` | Submit symptom + optional category, returns `RepairOutput` JSON |

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
