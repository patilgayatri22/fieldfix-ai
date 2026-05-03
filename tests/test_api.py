"""End-to-end API tests via FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


# ── Health ────────────────────────────────────────────────────────────────────

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "mode" in data
    assert "kb_chunks" in data
    assert data["kb_chunks"] > 0


# ── Safety check endpoint ─────────────────────────────────────────────────────

def test_safety_check_critical():
    r = client.post("/safety/check", json={"symptom": "gas smell in kitchen"})
    assert r.status_code == 200
    data = r.json()
    assert data["is_safe_to_proceed"] is False
    assert data["risk_level"] == "critical"
    assert data["emergency_action"] is not None


def test_safety_check_low():
    r = client.post("/safety/check", json={"symptom": "servo buzzing"})
    assert r.status_code == 200
    data = r.json()
    assert data["is_safe_to_proceed"] is True
    assert data["risk_level"] == "low"


def test_safety_check_high():
    r = client.post("/safety/check", json={"symptom": "swollen lipo battery"})
    assert r.status_code == 200
    data = r.json()
    assert data["is_safe_to_proceed"] is False
    assert data["risk_level"] == "high"


# ── Repair analyze — mock path ────────────────────────────────────────────────

@pytest.mark.parametrize("symptom,category", [
    ("servo buzzing but not moving",   "robotics"),
    ("raspberry pi not booting",       "electronics"),
    ("flashlight completely dead",     "emergency_equipment"),
    ("door hinge squeaking badly",     "household"),
])
def test_repair_analyze_returns_valid_output(symptom, category):
    r = client.post("/repair/analyze", json={"symptom": symptom, "category": category})
    assert r.status_code == 200
    data = r.json()
    # Required RepairOutput fields
    assert "detected_item" in data
    assert "problem_summary" in data
    assert "risk_level" in data
    assert "likely_causes" in data
    assert "step_by_step_repair" in data
    assert "stop_conditions" in data
    assert "retrieved_sources" in data
    assert isinstance(data["likely_causes"], list)
    assert isinstance(data["step_by_step_repair"], list)
    assert len(data["step_by_step_repair"]) >= 1


def test_repair_analyze_critical_safety_blocked():
    r = client.post("/repair/analyze", json={"symptom": "gas smell in kitchen"})
    assert r.status_code == 422
    detail = r.json()["detail"]
    assert detail["is_safe_to_proceed"] is False
    assert detail["risk_level"] == "critical"


def test_repair_analyze_high_risk_blocked():
    r = client.post("/repair/analyze", json={"symptom": "swollen lipo battery on my robot"})
    assert r.status_code == 422
    detail = r.json()["detail"]
    assert detail["is_safe_to_proceed"] is False
    assert detail["risk_level"] == "high"


def test_repair_analyze_unknown_symptom_400():
    r = client.post("/repair/analyze", json={"symptom": "xyzzy frobnicator broken"})
    assert r.status_code == 400


def test_repair_analyze_no_symptom_422():
    r = client.post("/repair/analyze", json={})
    assert r.status_code == 422  # Pydantic validation error


# ── RAG endpoints ─────────────────────────────────────────────────────────────

def test_rag_status_ready():
    r = client.get("/rag/status")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ready"
    assert data["total_chunks"] == 295
    assert set(data["categories"].keys()) == {
        "robotics", "electronics", "emergency_equipment", "household", "safety"
    }


def test_rag_search_returns_results():
    r = client.post("/rag/search", json={
        "query": "servo motor buzzing at angle",
        "category": "robotics",
        "top_k": 3
    })
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert len(data["results"]) >= 1
    assert "relevance_score" in data["results"][0]


def test_rag_search_missing_query_400():
    r = client.post("/rag/search", json={"category": "robotics"})
    assert r.status_code == 400


# ── Repair output schema integrity ───────────────────────────────────────────

def test_repair_output_step_numbers_sequential():
    r = client.post("/repair/analyze", json={
        "symptom": "servo buzzing", "category": "robotics"
    })
    steps = r.json()["step_by_step_repair"]
    numbers = [s["step_number"] for s in steps]
    assert numbers == list(range(1, len(numbers) + 1))


def test_repair_output_confidence_in_range():
    r = client.post("/repair/analyze", json={
        "symptom": "servo buzzing", "category": "robotics"
    })
    data = r.json()
    assert 0.0 <= data["confidence_overall"] <= 1.0
    for cause in data["likely_causes"]:
        assert 0.0 <= cause["confidence"] <= 1.0


def test_repair_output_retrieved_sources_have_score():
    r = client.post("/repair/analyze", json={
        "symptom": "servo buzzing", "category": "robotics"
    })
    for src in r.json()["retrieved_sources"]:
        assert 0.0 <= src["relevance_score"] <= 1.0
