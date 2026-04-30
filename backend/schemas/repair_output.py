from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    robotics = "robotics"
    electronics = "electronics"
    emergency_equipment = "emergency_equipment"
    household = "household"
    safety = "safety"
    unknown = "unknown"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class RepairDifficulty(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    professional = "professional"


class LikelyCause(BaseModel):
    description: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str


class RepairStep(BaseModel):
    step_number: int = Field(ge=1)
    instruction: str
    warning: str | None = None
    expected_outcome: str


class RetrievedSource(BaseModel):
    title: str
    source: str
    relevance_score: float = Field(ge=0.0, le=1.0)


class RepairOutput(BaseModel):
    detected_item: str
    problem_summary: str
    category: Category
    risk_level: RiskLevel
    repair_difficulty: RepairDifficulty
    confidence_overall: float = Field(ge=0.0, le=1.0)
    visible_observations: list[str]
    likely_causes: list[LikelyCause]
    clarifying_questions: list[str]
    tools_needed: list[str]
    next_best_test: str
    step_by_step_repair: list[RepairStep]
    stop_conditions: list[str]
    prevention: list[str]
    retrieved_sources: list[RetrievedSource]
