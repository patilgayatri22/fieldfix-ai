#!/usr/bin/env python3
"""
Demo runner — exercises all 4 hero demos via RepairOrchestrator in mock mode.

Usage:
  python backend/scripts/demo_run.py --demo servo
  python backend/scripts/demo_run.py --demo pi
  python backend/scripts/demo_run.py --demo flashlight
  python backend/scripts/demo_run.py --demo household
  python backend/scripts/demo_run.py --demo all
"""

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path

# Ensure mock mode before any imports that read USE_MOCK
os.environ["USE_MOCK"] = "true"

# Make sure repo root is on path when run as a script
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.agents.repair_orchestrator import RepairOrchestrator  # noqa: E402
from backend.schemas.repair_output import RepairOutput  # noqa: E402

_DEMOS: dict[str, dict] = {
    "servo": {
        "symptom": "servo motor is buzzing and won't hold position",
        "category": "robotics",
        "device_id": "demo-servo-001",
    },
    "pi": {
        "symptom": "raspberry pi is not booting, no display, red LED only",
        "category": "electronics",
        "device_id": "demo-pi-001",
    },
    "flashlight": {
        "symptom": "flashlight completely dead, new batteries installed",
        "category": "emergency_equipment",
        "device_id": "demo-flashlight-001",
    },
    "household": {
        "symptom": "cabinet door hinge is loose, door won't stay closed",
        "category": "household",
        "device_id": "demo-household-001",
    },
}


async def run_demo(name: str, params: dict, orc: RepairOrchestrator) -> bool:
    t0 = time.perf_counter()
    try:
        output: RepairOutput = await orc.run(
            symptom=params["symptom"],
            category=params["category"],
            device_id=params["device_id"],
            use_mock=True,
        )
        elapsed = time.perf_counter() - t0
        assert isinstance(output, RepairOutput), "output not RepairOutput"
        assert output.detected_item, "detected_item empty"
        print(
            f"  [PASS] {name:<12} | {elapsed:.2f}s | "
            f"item={output.detected_item!r} | "
            f"risk={output.risk_level.value} | "
            f"conf={output.confidence_overall:.2f} | "
            f"steps={len(output.step_by_step_repair)} | "
            f"sources={len(output.retrieved_sources)}"
        )
        return True
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        print(f"  [FAIL] {name:<12} | {elapsed:.2f}s | {exc}")
        return False


async def main() -> int:
    parser = argparse.ArgumentParser(description="FieldFix AI demo runner")
    parser.add_argument(
        "--demo",
        choices=[*_DEMOS.keys(), "all"],
        default="all",
        help="Which demo to run (default: all)",
    )
    args = parser.parse_args()

    to_run = list(_DEMOS.items()) if args.demo == "all" else [(args.demo, _DEMOS[args.demo])]
    orc = RepairOrchestrator()

    print(f"\nFieldFix AI — Demo Runner (USE_MOCK=true)")
    print(f"Running: {args.demo}\n")

    t_total = time.perf_counter()
    results = []
    for name, params in to_run:
        ok = await run_demo(name, params, orc)
        results.append(ok)

    total_elapsed = time.perf_counter() - t_total
    passed = sum(results)
    total = len(results)
    print(f"\n{'─' * 60}")
    print(f"Result: {passed}/{total} passed in {total_elapsed:.2f}s")

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
