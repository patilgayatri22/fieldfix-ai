# FieldFix AI 🔧
> Offline AI repair copilot — powered by Gemma 3

## What it does

Imagine a field technician with a broken servo on a robotic arm, standing in a warehouse with no internet access. They open FieldFix AI on their phone, speak or type the symptom, and within seconds receive a structured diagnosis: the likely causes ranked by confidence, step-by-step repair instructions pulled from a local knowledge base, the tools needed, and clear stop conditions if anything looks dangerous. No cloud. No connectivity. Just answers.

FieldFix AI runs entirely on a laptop (or any local machine), serves its Next.js UI over WiFi to any phone on the same network, and uses Gemma 3 4B via Ollama for all reasoning. The knowledge base contains 37 expert-authored repair documents (2,450+ lines) chunked into 295 semantic pieces and stored in ChromaDB. Every repair request passes through a deterministic safety guardrail before any AI is involved.

## Demo — 4 scenarios

| Demo | Symptom | Risk | Output |
|------|---------|------|--------|
| Servo buzzing | "servo motor is buzzing and won't hold position" | Medium | Calibration + PWM diagnosis sequence |
| Pi not booting | "raspberry pi not booting, no display, red LED only" | Low | SD card, power rail, and boot config checks |
| Dead flashlight | "flashlight completely dead, new batteries installed" | Low | Battery contact, switch, and LED diagnosis |
| Loose hinge | "cabinet door hinge is loose, door won't stay closed" | Low | Screw tightening and anchor repair steps |

## Hackathon track alignment

| Track | How FieldFix qualifies |
|-------|----------------------|
| Digital Equity | Offline-first, no cloud dependency — serves field workers in zero-connectivity zones |
| Global Resilience | Agricultural and industrial repair guidance for low-connectivity environments |
| Safety | Deterministic safety guardrails run before any AI; 9 hard-stop categories block dangerous advice |

## Architecture

```
User (phone browser)
      │
      ▼  iOS Safari, WiFi to laptop IP
Next.js frontend  (TypeScript, Tailwind, shadcn/ui)
      │
      ▼  REST API  http://localhost:8000
FastAPI backend
      ├── Safety guardrails    (deterministic keywords, no model)
      ├── RepairOrchestrator   (coordinates all agents)
      │     ├── diagnosis_agent      → LikelyCause list
      │     ├── cause_ranker         → ranked causes
      │     ├── repair_planner       → RepairStep list (RAG-augmented)
      │     ├── question_agent       → clarifying questions
      │     └── verification_agent  → stop_conditions + prevention
      ├── RAG retriever        (ChromaDB, 295 chunks, all-MiniLM-L6-v2)
      └── Device memory        (SQLite, per-device repair history)
                    │
                    ▼
              Gemma 3 4B via Ollama  (runs locally, Metal GPU on Mac)
```

## Safety policy

FieldFix AI blocks repair guidance for 9 hard-stop categories. These checks run deterministically — no AI involved — before any agent pipeline is triggered.

| Category | Action |
|----------|--------|
| Gas leak / smell of gas | Block + evacuate instruction |
| Carbon monoxide alarm | Block + evacuate instruction |
| Electrical fire / smoke from wiring | Block + evacuate instruction |
| Fuel leak | Block + evacuate instruction |
| Swollen / puffed lithium battery | Block — fire risk, no disassembly |
| Live / bare wire exposure | Block — electrocution risk |
| Mains / high-voltage electricity | Block — professional only |
| Electric shock received | Block — seek medical attention |
| Microwave internal repair | Block — lethal capacitor charge |

Medium-risk symptoms (overheating, sparks, standard electrical faults) proceed with mandatory warnings attached.

## Quick start

```bash
git clone https://github.com/sagarbpatel31/fieldfix-ai
cd fieldfix-ai

# Backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python backend/rag/ingest.py        # build ChromaDB from KB docs
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd frontend && npm install && npm run dev

# Demo without Gemma (instant mock responses)
python backend/scripts/demo_run.py --demo all

# Install Gemma (one-time, ~2.5 GB)
brew install ollama
ollama pull gemma3:4b
ollama serve
```

Access from phone: open `http://<laptop-ip>:3000` in iOS Safari.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Status, mode, kb_chunks count |
| GET | `/rag/status` | 295 total chunks, per-category breakdown |
| POST | `/rag/search` | Semantic search: `{query, category?, top_k?}` |
| POST | `/safety/check` | Returns `SafetyOutput` for any symptom |
| POST | `/repair/analyze` | Main endpoint — returns full `RepairOutput` |
| POST | `/memory/{device_id}` | Save repair to device history |
| GET | `/memory/{device_id}` | Fetch repair history for device |
| DELETE | `/memory/{device_id}` | Clear device repair history |

## Knowledge base

| Category | Documents | Topics |
|----------|-----------|--------|
| Robotics | 9 | Servo, stepper, DC motor, motor driver, robotic arm, encoder, chassis, sensors, power |
| Electronics | 9 | Raspberry Pi, Arduino, ESP32/8266, I2C/SPI, power supply, battery, LCD/OLED, PCB, sensors |
| Emergency Equipment | 7 | Flashlight, headlamp, generator, smoke detector, CO detector, power bank, emergency radio |
| Household | 7 | Door hinge, faucet, wobbly furniture, clogged drain, bike chain, door lock, light fixture |
| Safety Guides | 5 | Electrical safety, battery safety, fire/chemical, tool safety, emergency procedures |

## Tests

```bash
# Full suite (115 + 9 orchestrator tests)
pytest tests/ -v

# Quick pass/fail summary
pytest tests/ -q

# Demo runner (no Ollama required)
python backend/scripts/demo_run.py --demo all

# Live Gemma validation (after ollama pull gemma3:4b)
python backend/scripts/validate_live.py
```

## Project structure

```
fieldfix-ai/
├── backend/
│   ├── agents/
│   │   ├── safety_guardrails.py   # deterministic 4-tier safety classifier
│   │   ├── repair_orchestrator.py # coordinates all agents into RepairOutput
│   │   ├── diagnosis_agent.py     # Gemma → likely causes
│   │   ├── cause_ranker.py        # Gemma → ranked causes
│   │   ├── repair_planner.py      # Gemma + RAG → repair steps
│   │   ├── question_agent.py      # Gemma → clarifying questions
│   │   └── verification_agent.py  # Gemma → stop conditions + prevention
│   ├── rag/
│   │   ├── ingest.py              # chunk KB docs → ChromaDB
│   │   └── retriever.py           # semantic search → RetrievedSource list
│   ├── memory/
│   │   └── device_memory.py       # SQLite repair history per device
│   ├── model_runtime/
│   │   └── gemma_client.py        # Ollama REST client + mock fallback
│   ├── schemas/
│   │   ├── repair_output.py       # RepairOutput (15 fields), enums
│   │   └── safety_output.py       # SafetyOutput (5 fields)
│   ├── scripts/
│   │   ├── demo_run.py            # CLI demo runner (4 scenarios)
│   │   └── validate_live.py       # live Gemma validation
│   └── main.py                    # FastAPI app, 8 endpoints
├── frontend/
│   ├── app/page.tsx               # main page, two-panel layout
│   ├── components/
│   │   ├── DiagnoseForm.tsx        # symptom input + speech + category
│   │   ├── RepairCard.tsx          # full repair output display
│   │   ├── RiskBadge.tsx           # colored risk level pill
│   │   └── SessionHistory.tsx      # device repair history list
│   ├── lib/api.ts                  # typed fetch wrappers for all endpoints
│   └── types/repair.ts             # TypeScript interfaces matching Pydantic schemas
├── knowledge_base/                 # 37 markdown docs, 5 categories
├── demos/                          # 4 hero + 2 safety mock JSON outputs
├── tests/                          # 124 pytest tests, all passing
├── .env.example                    # all env vars documented
└── requirements.txt
```
