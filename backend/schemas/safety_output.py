from pydantic import BaseModel

from backend.schemas.repair_output import RiskLevel


class SafetyOutput(BaseModel):
    is_safe_to_proceed: bool
    risk_level: RiskLevel
    blocked_reason: str | None = None
    warnings: list[str]
    emergency_action: str | None = None
