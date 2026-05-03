"""Repair planner — causes + context → step-by-step repair instructions.

Most critical agent for demo. Generates numbered, safety-aware repair
steps grounded in the knowledge base. Falls back to generic safe steps
if Gemma is unavailable.
"""

from __future__ import annotations

import logging

from backend.model_runtime.gemma_client import GemmaClient, get_client
from backend.rag.retriever import retrieve_context
from backend.schemas.repair_output import LikelyCause, RepairStep

logger = logging.getLogger(__name__)

_SYSTEM = """\
You are FieldFix AI, an expert offline repair assistant.
Generate a clear, safe, step-by-step repair guide for a non-expert user.

Rules:
- Start with the simplest, safest check. Escalate gradually.
- Each step must have a concrete, single action.
- Add a warning ONLY if that specific step has a real safety risk.
- expected_outcome describes what the user should observe if the step succeeds.
- Generate 3–6 steps. Do not over-explain.
- Never include steps involving mains electricity, gas, swollen batteries,
  or any component explicitly flagged as unsafe in the context.
- Respond ONLY with valid JSON — no prose, no markdown fences.

JSON format:
{
  "steps": [
    {
      "step_number": 1,
      "instruction": "...",
      "warning": null,
      "expected_outcome": "..."
    },
    ...
  ]
}"""


def run(
    symptom: str,
    causes: list[LikelyCause],
    category: str | None = None,
    client: GemmaClient | None = None,
) -> list[RepairStep]:
    """
    Generate repair steps for the top-ranked causes.

    Args:
        symptom:  User-reported symptom.
        causes:   Ranked causes from cause_ranker.
        category: KB category for focused RAG retrieval.
        client:   GemmaClient instance (uses singleton if None).

    Returns:
        List of RepairStep objects in execution order.
        Returns safe generic fallback steps if Gemma unavailable.
    """
    if client is None:
        client = get_client()

    context = retrieve_context(symptom, category=category, top_k=4)

    # Summarise top 3 causes for prompt
    top_causes = "\n".join(
        f"- {c.description} (confidence={c.confidence:.2f})"
        for c in causes[:3]
    )

    prompt = f"""\
Knowledge base context:
{context}

User symptom: {symptom}

Most likely causes:
{top_causes}

Generate safe, numbered repair steps for a non-expert. Respond with JSON only."""

    data = client.generate_json(prompt, system=_SYSTEM)
    raw_steps = data.get("steps", [])

    steps: list[RepairStep] = []
    for i, item in enumerate(raw_steps):
        try:
            steps.append(
                RepairStep(
                    step_number=int(item.get("step_number", i + 1)),
                    instruction=str(item.get("instruction", "")),
                    warning=item.get("warning") or None,
                    expected_outcome=str(item.get("expected_outcome", "")),
                )
            )
        except Exception as exc:
            logger.debug("Skipping malformed step: %s — %s", item, exc)

    if not steps:
        logger.warning("repair_planner: Gemma returned no steps, using fallback")
        steps = _fallback_steps(symptom)

    return steps


def _fallback_steps(symptom: str) -> list[RepairStep]:
    """Safe generic fallback steps."""
    return [
        RepairStep(
            step_number=1,
            instruction="Power off the device and disconnect all power sources before proceeding.",
            warning="Never work on powered equipment.",
            expected_outcome="Device is fully powered off and safe to inspect.",
        ),
        RepairStep(
            step_number=2,
            instruction="Visually inspect all cables, connectors, and visible components for damage.",
            warning=None,
            expected_outcome="Any obvious physical damage, loose wires, or burn marks identified.",
        ),
        RepairStep(
            step_number=3,
            instruction="Check all electrical connections are fully seated and secure.",
            warning=None,
            expected_outcome="All connectors click in firmly with no play.",
        ),
        RepairStep(
            step_number=4,
            instruction="Power on and retest. If symptom persists, consult the relevant knowledge base section.",
            warning=None,
            expected_outcome=f"Symptom '{symptom[:60]}' resolved or narrowed to a specific component.",
        ),
    ]
