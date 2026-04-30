import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.schemas.repair_output import Category, RepairOutput

DEMOS_DIR = Path(__file__).parent.parent / "demos"

app = FastAPI(
    title="FieldFix AI",
    version="0.1.0",
    description="Offline multimodal repair copilot",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict origins before production
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    symptom: str
    category: Category | None = None
    image_description: str | None = None


def _resolve_demo(symptom: str, category: Category | None) -> str:
    s = symptom.lower()
    if category == Category.robotics or any(k in s for k in ("servo", "buzzing", "robotic")):
        return "servo_buzzing"
    if any(k in s for k in ("raspberry", " pi ", "boot", "rpi")):
        return "raspberry_pi_not_booting"
    if any(k in s for k in ("flashlight", "generator", "emergency", "torch")):
        return "flashlight_dead"
    if category == Category.household or any(k in s for k in ("hinge", "faucet", "cabinet", "furniture", "wobbly")):
        return "household_quick_fix"
    return "servo_buzzing"


_KNOWN_KEYWORDS = (
    "servo", "buzzing", "robotic",
    "raspberry", " pi ", "boot", "rpi",
    "flashlight", "generator", "emergency", "torch",
    "hinge", "faucet", "cabinet", "furniture", "wobbly",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": "mock"}


@app.post("/repair/analyze", response_model=RepairOutput)
def analyze(request: AnalyzeRequest) -> RepairOutput:
    if request.category is None:
        s = request.symptom.lower()
        if not any(k in s for k in _KNOWN_KEYWORDS):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Cannot determine repair category. "
                    "Provide a category or use more specific symptom keywords."
                ),
            )
    demo_name = _resolve_demo(request.symptom, request.category)
    mock_path = DEMOS_DIR / demo_name / "mock_output.json"
    raw = json.loads(mock_path.read_text(encoding="utf-8"))
    return RepairOutput.model_validate(raw)
