"""Diagnosis agent — symptom → likely causes.

Uses Gemma + RAG context to identify the most probable causes
for a reported symptom. Falls back to a generic response if
Gemma is unavailable (mock mode safe).
"""

from __future__ import annotations

import logging

from backend.model_runtime.gemma_client import GemmaClient, get_client
from backend.rag.retriever import retrieve_context
from backend.schemas.repair_output import LikelyCause

logger = logging.getLogger(__name__)

_SYSTEM = """\
You are FieldFix AI, an expert offline repair diagnostic assistant.
Your job: identify the most likely causes of a reported hardware or household problem.

Rules:
- Base your answer ONLY on the symptom and provided knowledge base context.
- List 2–4 causes, most likely first.
- Confidence must be a float between 0.0 and 1.0.
- Evidence must reference an observable detail (not a theory).
- Never suggest unsafe actions.
- Respond ONLY with valid JSON — no prose, no markdown fences.

JSON format:
{
  "causes": [
    {"description": "...", "confidence": 0.85, "evidence": "..."},
    ...
  ]
}"""


def run(
    symptom: str,
    category: str | None = None,
    client: GemmaClient | None = None,
) -> list[LikelyCause]:
    """
    Identify likely causes for the given symptom.

    Args:
        symptom:  User-reported symptom string.
        category: Optional KB category slug for focused RAG retrieval.
        client:   GemmaClient instance (uses singleton if None).

    Returns:
        List of LikelyCause objects, best match first.
        Returns a safe fallback list if Gemma is unavailable.
    """
    if client is None:
        client = get_client()

    # Pull relevant KB context
    context = retrieve_context(symptom, category=category, top_k=3)

    prompt = f"""\
Knowledge base context:
{context}

User symptom: {symptom}

Identify the most likely causes. Respond with JSON only."""

    data = client.generate_json(prompt, system=_SYSTEM)
    raw_causes = data.get("causes", [])

    causes: list[LikelyCause] = []
    for item in raw_causes:
        try:
            causes.append(
                LikelyCause(
                    description=str(item.get("description", "Unknown cause")),
                    confidence=float(item.get("confidence", 0.5)),
                    evidence=str(item.get("evidence", "No evidence provided")),
                )
            )
        except Exception as exc:
            logger.debug("Skipping malformed cause: %s — %s", item, exc)

    if not causes:
        logger.warning("diagnosis_agent: Gemma returned no causes, using fallback")
        causes = _fallback_causes(symptom)

    return causes


def _fallback_causes(symptom: str) -> list[LikelyCause]:
    """Generic fallback when Gemma is unavailable."""
    return [
        LikelyCause(
            description="Component fault or misconfiguration",
            confidence=0.5,
            evidence=f"Symptom reported: {symptom[:80]}",
        ),
        LikelyCause(
            description="Power supply or connection issue",
            confidence=0.4,
            evidence="Loose connections and power faults are common first causes.",
        ),
    ]
