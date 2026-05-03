"""Cause ranker — re-rank diagnosed causes by likelihood.

Takes the output of diagnosis_agent and uses Gemma to reconsider
confidence scores given the full symptom context. Lightweight agent —
if Gemma unavailable, returns causes sorted by existing confidence.
"""

from __future__ import annotations

import logging

from backend.model_runtime.gemma_client import GemmaClient, get_client
from backend.schemas.repair_output import LikelyCause

logger = logging.getLogger(__name__)

_SYSTEM = """\
You are FieldFix AI. Re-rank a list of possible repair causes by likelihood.

Rules:
- Adjust confidence scores based on the symptom details provided.
- Keep all causes — do not add or remove any.
- Return them ordered from highest confidence to lowest.
- Respond ONLY with valid JSON — no prose, no markdown.

JSON format:
{
  "ranked_causes": [
    {"description": "...", "confidence": 0.92, "evidence": "..."},
    ...
  ]
}"""


def run(
    symptom: str,
    causes: list[LikelyCause],
    client: GemmaClient | None = None,
) -> list[LikelyCause]:
    """
    Re-rank causes by confidence for the given symptom.

    Args:
        symptom: Original user symptom.
        causes:  Causes from diagnosis_agent.
        client:  GemmaClient instance (uses singleton if None).

    Returns:
        Causes re-ranked highest confidence first.
        Falls back to simple sort if Gemma unavailable.
    """
    if client is None:
        client = get_client()

    if not causes:
        return causes

    # Serialize current causes for the prompt
    causes_text = "\n".join(
        f"{i+1}. {c.description} (confidence={c.confidence:.2f}) — {c.evidence}"
        for i, c in enumerate(causes)
    )

    prompt = f"""\
Symptom: {symptom}

Current causes:
{causes_text}

Re-rank these causes by likelihood for this specific symptom. Respond with JSON only."""

    data = client.generate_json(prompt, system=_SYSTEM)
    raw = data.get("ranked_causes", [])

    ranked: list[LikelyCause] = []
    for item in raw:
        try:
            ranked.append(
                LikelyCause(
                    description=str(item.get("description", "")),
                    confidence=float(item.get("confidence", 0.5)),
                    evidence=str(item.get("evidence", "")),
                )
            )
        except Exception as exc:
            logger.debug("Skipping malformed ranked cause: %s — %s", item, exc)

    if not ranked:
        # Fallback: sort original causes by confidence descending
        return sorted(causes, key=lambda c: c.confidence, reverse=True)

    return ranked
