#!/usr/bin/env python3
"""
Live Gemma validation script.
Only run AFTER `ollama pull gemma3:4b` finishes downloading.

Checks:
  1. Ollama server reachable
  2. gemma3:4b model is pulled
  3. Full orchestrator pipeline runs (USE_MOCK=false)
  4. RepairOutput is valid Pydantic object
  5. step_by_step_repair >= 3 steps
  6. confidence_overall > 0
  7. retrieved_sources non-empty
  8. likely_causes non-empty

Usage:
  python backend/scripts/validate_live.py
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

# Force Gemma mode
os.environ["USE_MOCK"] = "false"

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import urllib.request  # noqa: E402

from backend.agents.repair_orchestrator import RepairOrchestrator  # noqa: E402
from backend.schemas.repair_output import RepairOutput  # noqa: E402

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
GEMMA_MODEL = os.environ.get("GEMMA_MODEL", "gemma3:4b")

DEMO = {
    "symptom": "servo motor is buzzing and won't hold position",
    "category": "robotics",
    "device_id": "validate-live-001",
}

_passed = 0
_failed = 0


def check(label: str, ok: bool, detail: str = "") -> bool:
    global _passed, _failed
    status = "[PASS]" if ok else "[FAIL]"
    suffix = f" — {detail}" if detail else ""
    print(f"  {status} {label}{suffix}")
    if ok:
        _passed += 1
    else:
        _failed += 1
    return ok


def check_ollama_reachable() -> bool:
    try:
        req = urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5)
        data = json.loads(req.read())
        return check("Ollama server reachable", True, f"{OLLAMA_URL}")
    except Exception as e:
        return check("Ollama server reachable", False, str(e))


def check_model_pulled() -> bool:
    try:
        req = urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5)
        data = json.loads(req.read())
        models = [m.get("name", "") for m in data.get("models", [])]
        pulled = any(GEMMA_MODEL in m for m in models)
        return check(
            f"Model {GEMMA_MODEL!r} pulled",
            pulled,
            f"found: {models[:3]}" if not pulled else "",
        )
    except Exception as e:
        return check(f"Model {GEMMA_MODEL!r} pulled", False, str(e))


async def run_pipeline() -> RepairOutput | None:
    orc = RepairOrchestrator()
    t0 = time.perf_counter()
    try:
        output = await orc.run(
            symptom=DEMO["symptom"],
            category=DEMO["category"],
            device_id=DEMO["device_id"],
            use_mock=False,
        )
        elapsed = time.perf_counter() - t0
        check("Pipeline ran successfully", True, f"{elapsed:.1f}s")
        return output
    except Exception as e:
        elapsed = time.perf_counter() - t0
        check("Pipeline ran successfully", False, str(e))
        return None


def validate_output(output: RepairOutput) -> None:
    check(
        "RepairOutput is valid Pydantic object",
        isinstance(output, RepairOutput),
    )
    check(
        "step_by_step_repair >= 3 steps",
        len(output.step_by_step_repair) >= 3,
        f"got {len(output.step_by_step_repair)}",
    )
    check(
        "confidence_overall > 0",
        output.confidence_overall > 0,
        f"got {output.confidence_overall}",
    )
    check(
        "retrieved_sources non-empty",
        len(output.retrieved_sources) > 0,
        f"got {len(output.retrieved_sources)}",
    )
    check(
        "likely_causes non-empty",
        len(output.likely_causes) > 0,
        f"got {len(output.likely_causes)}",
    )


async def main() -> int:
    print(f"\nFieldFix AI — Live Gemma Validation")
    print(f"Model: {GEMMA_MODEL}  |  Ollama: {OLLAMA_URL}\n")

    # Steps 1-2: connectivity
    if not check_ollama_reachable():
        print("\n  Ollama not running. Start it with: ollama serve")
        return 1
    if not check_model_pulled():
        print(f"\n  Pull the model first: ollama pull {GEMMA_MODEL}")
        return 1

    # Step 3: pipeline
    output = await run_pipeline()
    if output is None:
        return 1

    # Steps 4-8: validate fields
    validate_output(output)

    # Summary
    print(f"\n{'─' * 50}")
    print(f"  {_passed} passed / {_failed} failed")

    if _failed == 0:
        print("\n  First 1000 chars of output:")
        print("  " + output.model_dump_json(indent=2)[:1000])

    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
