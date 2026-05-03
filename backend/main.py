import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents import (
    cause_ranker,
    diagnosis_agent,
    question_agent,
    repair_planner,
    verification_agent,
)
from backend.agents.safety_guardrails import classify_safety
from backend.model_runtime.gemma_client import get_client
from backend.rag.ingest import get_collection
from backend.rag.retriever import retrieve
from backend.schemas.repair_output import (
    Category,
    RepairDifficulty,
    RepairOutput,
    RetrievedSource,
    RiskLevel,
)
from backend.memory.device_memory import (
    RepairHistoryResponse,
    clear_history,
    get_history,
    save_repair,
)
from backend.schemas.safety_output import SafetyOutput

DEMOS_DIR = Path(__file__).parent.parent / "demos"

# ── Mode flag ──────────────────────────────────────────────────────────────────
# USE_MOCK=true  → always return demo JSON (fast, no Ollama needed)
# USE_MOCK=false → run full Gemma agent pipeline (falls back to mock on failure)
USE_MOCK: bool = os.environ.get("USE_MOCK", "false").lower() == "true"

app = FastAPI(
    title="FieldFix AI",
    version="0.2.0",
    description="Offline multimodal repair copilot",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict origins before production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request models ─────────────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    symptom: str
    category: Category | None = None
    image_description: str | None = None


class SafetyCheckRequest(BaseModel):
    symptom: str


# ── Demo routing ──────────────────────────────────────────────────────────────

_ROBOTICS_KEYWORDS: tuple[str, ...] = (
    "servo", "buzzing", "robotic", "robot arm", "stepper", "motor driver",
    "encoder", "actuator", "chassis", "robot wheel", "robot not moving",
    "l298n", "l293d", "drv88", "nema",
)

_ELECTRONICS_KEYWORDS: tuple[str, ...] = (
    "raspberry", " rpi ", "arduino", "esp32", "esp8266",
    "microcontroller", "breadboard", "gpio", "i2c", " spi ", "uart",
    "solder", "pcb", "voltage regulator", "lcd screen", "oled",
    "sensor reading", "not booting", "boot loop", "upload failed",
)

_EMERGENCY_KEYWORDS: tuple[str, ...] = (
    "flashlight", "torch", "headlamp", "head lamp",
    "generator", "portable generator",
    "smoke detector", "smoke alarm",
    "power bank", "portable charger",
    "emergency radio", "weather radio",
    "hand crank",
)

_HOUSEHOLD_KEYWORDS: tuple[str, ...] = (
    "hinge", "squeaky door", "door sag",
    "faucet", "tap drip", "leaking tap", "dripping tap",
    "toilet running", "toilet keeps running", "running toilet", "toilet",
    "bike chain", "chain slip", "chain skip",
    "wobbly", "furniture", "cabinet", "chair wobble", "table wobble",
    "clogged drain", "slow drain", "blocked sink", "shower drain",
    "light bulb", "flickering light", "light switch",
    "door lock", "key stiff", "deadbolt",
)

_ALL_KNOWN_KEYWORDS: tuple[str, ...] = (
    *_ROBOTICS_KEYWORDS,
    *_ELECTRONICS_KEYWORDS,
    *_EMERGENCY_KEYWORDS,
    *_HOUSEHOLD_KEYWORDS,
    " pi ",
    "won't boot", "not boot", "wont boot",
)


def _resolve_demo(symptom: str, category: Category | None) -> str:
    s = symptom.lower()
    if category == Category.robotics or any(k in s for k in _ROBOTICS_KEYWORDS):
        return "servo_buzzing"
    if category == Category.electronics or any(
        k in s for k in (*_ELECTRONICS_KEYWORDS, " pi ", "won't boot", "not boot", "wont boot")
    ):
        return "raspberry_pi_not_booting"
    if category == Category.emergency_equipment or any(k in s for k in _EMERGENCY_KEYWORDS):
        return "flashlight_dead"
    if category == Category.household or any(k in s for k in _HOUSEHOLD_KEYWORDS):
        return "household_quick_fix"
    if category == Category.safety:
        return "household_quick_fix"
    return "servo_buzzing"


def _symptom_is_recognisable(symptom: str, category: Category | None) -> bool:
    if category is not None:
        return True
    s = symptom.lower()
    return any(k in s for k in _ALL_KNOWN_KEYWORDS)


def _load_mock(symptom: str, category: Category | None) -> RepairOutput:
    """Load and return the nearest demo JSON as a RepairOutput."""
    demo_name = _resolve_demo(symptom, category)
    mock_path = DEMOS_DIR / demo_name / "mock_output.json"
    raw = json.loads(mock_path.read_text(encoding="utf-8"))
    return RepairOutput.model_validate(raw)


# ── Agent pipeline ────────────────────────────────────────────────────────────

def _run_agent_pipeline(request: AnalyzeRequest) -> RepairOutput:
    """
    Full Gemma-powered repair pipeline.

    Flow:
      1. diagnosis_agent  → list[LikelyCause]
      2. cause_ranker     → list[LikelyCause] (sorted)
      3. repair_planner   → list[RepairStep]
      4. question_agent   → list[str]
      5. verification_agent → (stop_conditions, prevention)
      6. RAG retriever    → list[RetrievedSource]
      7. Assemble RepairOutput

    Falls back to mock if Gemma is unavailable or any stage fails.
    """
    client = get_client()
    category_str = request.category.value if request.category else None

    # ── Stages ──────────────────────────────────────────────────────────────
    causes = diagnosis_agent.run(request.symptom, category=category_str, client=client)
    causes = cause_ranker.run(request.symptom, causes, client=client)
    steps = repair_planner.run(request.symptom, causes, category=category_str, client=client)
    questions = question_agent.run(request.symptom, causes, client=client)
    stop_conditions, prevention = verification_agent.run(
        request.symptom, steps, category=category_str, client=client
    )
    sources = retrieve(request.symptom, category=category_str, top_k=3)

    # ── Derive metadata from top cause ──────────────────────────────────────
    top_confidence = causes[0].confidence if causes else 0.6
    risk_level = _infer_risk(request.symptom, request.category)
    difficulty = _infer_difficulty(request.category)
    tools = _extract_tools(steps)

    # ── Build RepairOutput ───────────────────────────────────────────────────
    return RepairOutput(
        detected_item=_infer_detected_item(request.symptom, request.category),
        problem_summary=f"{request.symptom.strip().rstrip('.')}.",
        category=request.category or Category.unknown,
        risk_level=risk_level,
        repair_difficulty=difficulty,
        confidence_overall=round(top_confidence, 2),
        visible_observations=[request.symptom],
        likely_causes=causes,
        clarifying_questions=questions,
        tools_needed=tools,
        next_best_test=steps[0].instruction if steps else "Inspect visually before proceeding.",
        step_by_step_repair=steps,
        stop_conditions=stop_conditions,
        prevention=prevention,
        retrieved_sources=sources,
    )


# ── Helpers for metadata inference ────────────────────────────────────────────

def _infer_risk(symptom: str, category: Category | None) -> RiskLevel:
    s = symptom.lower()
    if any(k in s for k in ("battery", "electrical", "wiring", "voltage", "heat", "hot")):
        return RiskLevel.medium
    if category == Category.electronics:
        return RiskLevel.medium
    return RiskLevel.low


def _infer_difficulty(category: Category | None) -> RepairDifficulty:
    if category == Category.robotics:
        return RepairDifficulty.intermediate
    if category == Category.electronics:
        return RepairDifficulty.intermediate
    return RepairDifficulty.beginner


def _infer_detected_item(symptom: str, category: Category | None) -> str:
    s = symptom.lower()
    if "servo" in s:
        return "Servo motor"
    if "raspberry" in s or " pi " in s:
        return "Raspberry Pi"
    if "arduino" in s:
        return "Arduino"
    if "flashlight" in s or "torch" in s:
        return "Flashlight / torch"
    if "drain" in s:
        return "Household drain"
    if "faucet" in s or "tap" in s:
        return "Faucet / tap"
    if "hinge" in s:
        return "Door hinge"
    if category:
        return category.value.replace("_", " ").title()
    return "Unknown device"


def _extract_tools(steps) -> list[str]:
    """Pull tool-like nouns from step instructions (simple heuristic)."""
    common_tools = [
        "multimeter", "screwdriver", "wrench", "pliers", "oscilloscope",
        "voltmeter", "soldering iron", "wire stripper", "Allen key",
        "hex key", "drain snake", "plunger", "contact cleaner",
    ]
    found: list[str] = []
    combined = " ".join(s.instruction.lower() for s in steps)
    for tool in common_tools:
        if tool.lower() in combined and tool not in found:
            found.append(tool)
    return found or ["Basic hand tools"]


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict:
    try:
        kb_chunks = get_collection().count()
    except Exception:
        kb_chunks = 0
    client = get_client()
    return {
        "status": "ok",
        "mode": "mock" if USE_MOCK else ("ollama" if client.is_available() else "mock-fallback"),
        "model": client.model,
        "kb_chunks": kb_chunks,
    }


@app.get("/rag/status")
def rag_status() -> dict:
    try:
        collection = get_collection()
        total = collection.count()
        if total == 0:
            return {"status": "empty", "total_chunks": 0, "categories": {}}
        categories = ["robotics", "electronics", "emergency_equipment", "household", "safety"]
        counts: dict[str, int] = {}
        for cat in categories:
            result = collection.get(where={"category": {"$eq": cat}}, include=[])
            counts[cat] = len(result["ids"])
        return {"status": "ready", "total_chunks": total, "categories": counts}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}


@app.post("/rag/search")
def rag_search(body: dict) -> dict:
    query: str = body.get("query", "")
    category: str | None = body.get("category")
    top_k: int = int(body.get("top_k", 5))
    if not query:
        raise HTTPException(status_code=400, detail="query is required")
    sources = retrieve(query, category=category, top_k=top_k)
    return {"query": query, "category": category, "results": [s.model_dump() for s in sources]}


@app.post("/safety/check", response_model=SafetyOutput)
def safety_check(request: SafetyCheckRequest) -> SafetyOutput:
    return classify_safety(request.symptom)


@app.post("/repair/analyze", response_model=RepairOutput)
def analyze(request: AnalyzeRequest) -> RepairOutput:
    """
    Analyze a repair symptom and return structured repair guidance.

    Mode A (USE_MOCK=true):  Return nearest demo JSON instantly.
    Mode B (USE_MOCK=false): Run full Gemma agent pipeline.
                             Auto-falls back to mock if Ollama unreachable.
    """
    # ── 1. Safety pre-check (always runs) ────────────────────────────────────
    safety = classify_safety(request.symptom)
    if not safety.is_safe_to_proceed:
        raise HTTPException(status_code=422, detail=safety.model_dump())

    # ── 2. Category / keyword check ──────────────────────────────────────────
    if not _symptom_is_recognisable(request.symptom, request.category):
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot determine repair category. "
                "Provide a category or describe the symptom with more detail."
            ),
        )

    # ── 3a. Mock mode — fast path ─────────────────────────────────────────────
    if USE_MOCK:
        return _load_mock(request.symptom, request.category)

    # ── 3b. Agent pipeline — full Gemma path ─────────────────────────────────
    client = get_client()
    if not client.is_available():
        # Ollama not running → graceful fallback to mock
        return _load_mock(request.symptom, request.category)

    try:
        return _run_agent_pipeline(request)
    except Exception:
        # Any unexpected pipeline failure → fall back to mock
        return _load_mock(request.symptom, request.category)


# ── Device memory routes ───────────────────────────────────────────────────────

@app.post("/memory/{device_id}")
def memory_save(device_id: str, output: RepairOutput):
    """Save a repair result to device history."""
    entry = save_repair(device_id, output)
    return entry.model_dump()


@app.get("/memory/{device_id}", response_model=RepairHistoryResponse)
def memory_get(device_id: str) -> RepairHistoryResponse:
    """Fetch repair history for a device."""
    entries = get_history(device_id)
    return RepairHistoryResponse(device_id=device_id, total=len(entries), entries=entries)


@app.delete("/memory/{device_id}")
def memory_clear(device_id: str) -> dict:
    """Clear all repair history for a device."""
    count = clear_history(device_id)
    return {"device_id": device_id, "deleted": count}
