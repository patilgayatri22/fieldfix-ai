"""Verification agent — generate stop conditions and prevention tips.

Runs after repair planning. Produces the safety stop conditions
(when to halt repair) and prevention tips (avoid recurrence).
These are critical for safety-first UX.
"""

from __future__ import annotations

import logging

from backend.model_runtime.gemma_client import GemmaClient, get_client
from backend.rag.retriever import retrieve_context
from backend.schemas.repair_output import RepairStep

logger = logging.getLogger(__name__)

_SYSTEM = """\
You are FieldFix AI. Generate safety stop conditions and prevention tips
for a repair task.

Rules:
- Stop conditions: specific observable signs that mean the user must STOP immediately.
  Focus on safety-critical signals (smoke, heat, sparks, wrong voltage, etc.).
  2–4 stop conditions.
- Prevention: practical tips to avoid the same problem in the future.
  2–4 tips. Concrete and actionable.
- Respond ONLY with valid JSON — no prose, no markdown.

JSON format:
{
  "stop_conditions": [
    "STOP if the device becomes hot to touch during testing.",
    "..."
  ],
  "prevention": [
    "Lubricate all moving joints annually.",
    "..."
  ]
}"""


def run(
    symptom: str,
    steps: list[RepairStep],
    category: str | None = None,
    client: GemmaClient | None = None,
) -> tuple[list[str], list[str]]:
    """
    Generate stop conditions and prevention tips for the repair.

    Args:
        symptom:  User-reported symptom.
        steps:    Repair steps from repair_planner.
        category: KB category for RAG context.
        client:   GemmaClient instance (uses singleton if None).

    Returns:
        Tuple of (stop_conditions, prevention) — both lists of strings.
        Falls back to safe generic lists if Gemma unavailable.
    """
    if client is None:
        client = get_client()

    context = retrieve_context(symptom, category=category, top_k=2)

    steps_text = "\n".join(
        f"Step {s.step_number}: {s.instruction}" for s in steps
    )

    prompt = f"""\
Knowledge base context:
{context}

Symptom: {symptom}

Repair steps planned:
{steps_text}

Generate stop conditions and prevention tips. JSON only."""

    data = client.generate_json(prompt, system=_SYSTEM)

    stop_conditions: list[str] = data.get("stop_conditions", [])
    prevention: list[str] = data.get("prevention", [])

    if not stop_conditions:
        stop_conditions = _fallback_stop_conditions()
    if not prevention:
        prevention = _fallback_prevention()

    return (
        [str(s) for s in stop_conditions],
        [str(p) for p in prevention],
    )


def _fallback_stop_conditions() -> list[str]:
    return [
        "STOP if you smell burning or see smoke at any point.",
        "STOP if any component becomes too hot to touch.",
        "STOP if you hear crackling, popping, or arcing sounds.",
        "STOP if the symptom worsens after any step — do not continue.",
    ]


def _fallback_prevention() -> list[str]:
    return [
        "Inspect all connections and fasteners periodically.",
        "Keep components clean and free from moisture and debris.",
        "Do not exceed rated load or voltage specifications.",
    ]
