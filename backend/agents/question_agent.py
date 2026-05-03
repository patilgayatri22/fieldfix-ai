"""Question agent — generate clarifying questions for the user.

After initial diagnosis, Gemma generates targeted questions that would
help narrow down the root cause further. Used by the frontend to drive
a conversational repair flow.
"""

from __future__ import annotations

import logging

from backend.model_runtime.gemma_client import GemmaClient, get_client
from backend.schemas.repair_output import LikelyCause

logger = logging.getLogger(__name__)

_SYSTEM = """\
You are FieldFix AI. Generate targeted diagnostic questions for the user.

Rules:
- Questions must help distinguish between the listed possible causes.
- Ask about observable symptoms only — what the user can see, hear, or measure.
- 2–4 questions maximum. Keep each under 20 words.
- Do not ask the user to open devices, touch live wires, or do anything unsafe.
- Respond ONLY with valid JSON — no prose, no markdown.

JSON format:
{
  "questions": [
    "Does the issue happen only at a specific angle or position?",
    "..."
  ]
}"""


def run(
    symptom: str,
    causes: list[LikelyCause],
    client: GemmaClient | None = None,
) -> list[str]:
    """
    Generate clarifying questions based on symptom and ranked causes.

    Args:
        symptom: User-reported symptom.
        causes:  Ranked causes from cause_ranker.
        client:  GemmaClient instance (uses singleton if None).

    Returns:
        List of question strings. Returns generic fallback if Gemma unavailable.
    """
    if client is None:
        client = get_client()

    causes_text = "\n".join(
        f"- {c.description}" for c in causes[:3]
    )

    prompt = f"""\
Symptom: {symptom}

Possible causes:
{causes_text}

Generate 2–4 diagnostic questions to help narrow down the cause. JSON only."""

    data = client.generate_json(prompt, system=_SYSTEM)
    questions = data.get("questions", [])

    if not questions or not isinstance(questions, list):
        return _fallback_questions()

    return [str(q) for q in questions if q]


def _fallback_questions() -> list[str]:
    return [
        "When did this problem first appear?",
        "Does the issue happen consistently or only sometimes?",
        "Have you made any recent changes to the device or its connections?",
    ]
