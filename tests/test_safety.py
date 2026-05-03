"""Tests for safety_guardrails classifier."""

import pytest
from backend.agents.safety_guardrails import classify_safety
from backend.schemas.repair_output import RiskLevel


# ── Critical cases ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("symptom", [
    "gas smell in kitchen",
    "smells like gas near stove",
    "smell of gas coming from wall",
    "carbon monoxide alarm going off",
    "co detector alarm sounding",
    "electrical fire from outlet",
    "smoke from wall socket",
    "wiring fire behind panel",
    "fuel leak under car",
    "petrol smell in garage",
])
def test_critical_blocks_repair(symptom):
    result = classify_safety(symptom)
    assert result.risk_level == RiskLevel.critical
    assert result.is_safe_to_proceed is False
    assert result.blocked_reason is not None
    assert result.emergency_action is not None
    assert len(result.warnings) >= 1


# ── High risk cases ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("symptom", [
    "swollen lipo battery on drone",
    "puffed battery in phone",
    "battery swollen and puffy",
    "lipo fire starting",
    "live wire exposed in wall",
    "bare wire near circuit",
    "mains electricity running to device",
    "electric shock from outlet",
    "got shocked by appliance",
    "shock from device casing",
    "microwave internal repair",
    "inside microwave capacitor",
])
def test_high_risk_blocks_repair(symptom):
    result = classify_safety(symptom)
    assert result.risk_level == RiskLevel.high
    assert result.is_safe_to_proceed is False
    assert result.blocked_reason is not None
    assert result.emergency_action is None  # no evacuation needed
    assert len(result.warnings) >= 1


# ── Medium risk — safe to proceed with warnings ───────────────────────────────

@pytest.mark.parametrize("symptom", [
    "battery overheating during charge",
    "lithium battery getting warm",
    "electrical outlet not working",
    "circuit breaker keeps tripping",
    "soldering iron not heating up",
    "component overheating on board",
    "sparks from connection",
])
def test_medium_risk_proceeds_with_warnings(symptom):
    result = classify_safety(symptom)
    assert result.risk_level == RiskLevel.medium
    assert result.is_safe_to_proceed is True
    assert result.blocked_reason is None
    assert len(result.warnings) >= 1


# ── Low risk — clean proceed ──────────────────────────────────────────────────

@pytest.mark.parametrize("symptom", [
    "servo buzzing at 90 degrees",
    "door hinge squeaking",
    "raspberry pi not booting",
    "arduino upload failed",
    "flashlight not working",
    "drain clogged in shower",
    "bike chain slipping",
    "smoke detector chirping",
    "wobbly chair leg",
    "faucet dripping slowly",
])
def test_low_risk_clean_proceed(symptom):
    result = classify_safety(symptom)
    assert result.risk_level == RiskLevel.low
    assert result.is_safe_to_proceed is True
    assert result.blocked_reason is None
    assert result.emergency_action is None


# ── Schema integrity ──────────────────────────────────────────────────────────

def test_safety_output_fields_always_present():
    result = classify_safety("servo motor making noise")
    assert hasattr(result, "is_safe_to_proceed")
    assert hasattr(result, "risk_level")
    assert hasattr(result, "blocked_reason")
    assert hasattr(result, "warnings")
    assert hasattr(result, "emergency_action")
    assert isinstance(result.warnings, list)
