"""Orchestrator tests — all run in mock mode, no Ollama required."""

import os

os.environ["USE_MOCK"] = "true"

import pytest

from backend.agents.repair_orchestrator import RepairOrchestrator
from backend.schemas.repair_output import RepairOutput

_orc = RepairOrchestrator()


@pytest.mark.asyncio
async def test_servo_demo():
    output = await _orc.run(
        symptom="servo motor is buzzing and won't hold position",
        category="robotics",
        device_id="test-servo",
        use_mock=True,
    )
    assert isinstance(output, RepairOutput)
    assert output.detected_item


@pytest.mark.asyncio
async def test_pi_demo():
    output = await _orc.run(
        symptom="raspberry pi is not booting, no display, red LED only",
        category="electronics",
        device_id="test-pi",
        use_mock=True,
    )
    assert isinstance(output, RepairOutput)
    assert output.detected_item


@pytest.mark.asyncio
async def test_flashlight_demo():
    output = await _orc.run(
        symptom="flashlight completely dead, new batteries installed",
        category="emergency_equipment",
        device_id="test-flashlight",
        use_mock=True,
    )
    assert isinstance(output, RepairOutput)
    assert output.detected_item


@pytest.mark.asyncio
async def test_household_demo():
    output = await _orc.run(
        symptom="cabinet door hinge is loose, door won't stay closed",
        category="household",
        device_id="test-household",
        use_mock=True,
    )
    assert isinstance(output, RepairOutput)
    assert output.detected_item


@pytest.mark.asyncio
async def test_hard_stop_gas():
    output = await _orc.run(
        symptom="I smell gas in the kitchen",
        category=None,
        use_mock=True,
    )
    assert output.risk_level.value == "critical"
    assert output.step_by_step_repair == []
    assert output.confidence_overall == 0.0


@pytest.mark.asyncio
async def test_hard_stop_swollen_battery():
    output = await _orc.run(
        symptom="swollen lipo battery on drone",
        category=None,
        use_mock=True,
    )
    assert output.risk_level.value == "critical"
    assert output.step_by_step_repair == []


@pytest.mark.asyncio
async def test_confidence_range():
    for symptom, category in [
        ("servo buzzing", "robotics"),
        ("raspberry pi not booting", "electronics"),
        ("flashlight dead", "emergency_equipment"),
        ("hinge squeaking", "household"),
    ]:
        output = await _orc.run(symptom=symptom, category=category, use_mock=True)
        assert 0.0 <= output.confidence_overall <= 1.0, (
            f"confidence out of range for {symptom!r}: {output.confidence_overall}"
        )


@pytest.mark.asyncio
async def test_pydantic_validation():
    output = await _orc.run(
        symptom="servo motor buzzing",
        category="robotics",
        use_mock=True,
    )
    d = output.model_dump()
    assert "detected_item" in d


@pytest.mark.asyncio
async def test_returns_repair_output_type():
    output = await _orc.run(
        symptom="door hinge squeaking",
        category="household",
        use_mock=True,
    )
    assert isinstance(output, RepairOutput) is True
