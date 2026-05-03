"""Safety pre-check agent — keyword-based tier classification.

No model required. Pure deterministic logic.

Tiers:
  critical  — stop everything, emergency action required (gas, CO, active fire)
  high      — no disassembly, no hands-on steps (swollen battery, live wire, shock)
  medium    — proceed with warnings (battery work, electrical, soldering)
  low       — safe to proceed
"""

from backend.schemas.repair_output import RiskLevel
from backend.schemas.safety_output import SafetyOutput

# ── Critical ──────────────────────────────────────────────────────────────────
# Life-threatening. Block all repair. Advise evacuation or emergency call.

_CRITICAL_KEYWORDS: tuple[str, ...] = (
    "gas leak", "smell gas", "smells like gas", "gas smell", "smell of gas",
    "rotten egg smell", "sulfur smell",
    "carbon monoxide", "co alarm", "co detector alarm", "co detector going off",
    "electrical fire", "fire from outlet", "fire from wall",
    "smoke from wall", "smoke from outlet", "smoke from wiring", "wiring fire",
    "smoke from breaker", "smoke from panel",
    "fuel leak", "petrol smell", "gasoline smell", "diesel smell",
)

# Maps keyword fragments to human-readable emergency actions
_EMERGENCY_ACTIONS: tuple[tuple[str, str], ...] = (
    (
        "gas",
        "Evacuate immediately. Do NOT operate any electrical switch or device. "
        "Leave door open as you exit. Call the gas emergency line from outside "
        "or a neighbor's phone. Do not re-enter until declared safe.",
    ),
    (
        "carbon monoxide",
        "Evacuate immediately — CO is odorless and acts fast. "
        "Call emergency services (911) from outside. Do not re-enter until "
        "authorities confirm safe CO levels.",
    ),
    (
        "co alarm",
        "Treat CO alarm as real. Evacuate immediately. "
        "Call emergency services from outside.",
    ),
    (
        "fire",
        "Do NOT use water on electrical fire. Evacuate and close doors. "
        "Call fire services (911). Use a Class C or ABC extinguisher only "
        "if fire is very small and you have a clear exit.",
    ),
    (
        "fuel",
        "Fuel leak is a fire and explosion hazard. Remove all ignition sources. "
        "Ventilate area. Evacuate if smell is strong. Call emergency services.",
    ),
)

# ── High risk ─────────────────────────────────────────────────────────────────
# No disassembly. No component contact. External observation only.

_HIGH_KEYWORDS: tuple[str, ...] = (
    "swollen battery", "swollen lipo", "puffed battery", "bulging battery",
    "puffy battery", "battery swollen", "lipo swollen",
    "battery fire", "lipo fire", "battery smoke", "lipo smoke",
    "battery leaking", "battery venting", "battery hissing",
    "live wire", "exposed wire", "bare wire", "mains wire",
    "mains electricity", "mains power", "240v", "120v", "high voltage",
    "microwave internal", "inside microwave", "microwave capacitor",
    "electric shock", "got shocked", "shocked myself", "shock from",
    "arc flash", "severe burn", "electrocuted",
    "swollen capacitor",
)

# ── Medium risk ───────────────────────────────────────────────────────────────
# Proceed with standard safety precautions.

_MEDIUM_KEYWORDS: tuple[str, ...] = (
    "battery", "lithium", "lipo", "18650", "li-ion",
    "electrical", "wiring", "circuit breaker", "outlet", "socket",
    "soldering", "solder", "flux",
    "overheating", "very hot", "smoking", "sparking", "sparks",
    "capacitor", "transformer",
)


def _match_first(text: str, keywords: tuple[str, ...]) -> str | None:
    """Return first matched keyword phrase, or None."""
    for kw in keywords:
        if kw in text:
            return kw
    return None


def _emergency_action(symptom: str) -> str:
    """Pick the most specific emergency action string for the symptom."""
    for fragment, action in _EMERGENCY_ACTIONS:
        if fragment in symptom:
            return action
    return (
        "This situation may be life-threatening. "
        "Evacuate the area and call emergency services (911) if unsure."
    )


def classify_safety(symptom: str) -> SafetyOutput:
    """
    Classify symptom into a safety tier.

    Args:
        symptom: Raw user-supplied symptom string.

    Returns:
        SafetyOutput with is_safe_to_proceed, risk_level, warnings, etc.
    """
    s = symptom.lower()

    # ── Critical — block repair entirely ──────────────────────────────────────
    if _match_first(s, _CRITICAL_KEYWORDS):
        return SafetyOutput(
            is_safe_to_proceed=False,
            risk_level=RiskLevel.critical,
            blocked_reason=(
                "Symptom indicates a potentially life-threatening hazard. "
                "Repair guidance is blocked for your safety."
            ),
            warnings=[
                "Do NOT attempt any repair, inspection, or disassembly.",
                "Evacuate the area immediately if any active hazard is present.",
                "Do not operate electrical switches near a gas or fuel leak.",
                "Call emergency services if the situation is active or unresolved.",
            ],
            emergency_action=_emergency_action(s),
        )

    # ── High — external observation only, no hands-on ─────────────────────────
    if _match_first(s, _HIGH_KEYWORDS):
        return SafetyOutput(
            is_safe_to_proceed=False,
            risk_level=RiskLevel.high,
            blocked_reason=(
                "Symptom involves high-voltage wiring, swollen/venting lithium cells, "
                "or severe electrical shock risk. "
                "Hands-on repair steps cannot be provided safely."
            ),
            warnings=[
                "Do not open, probe, or disassemble this device.",
                "Do not touch exposed wiring, battery cells, or capacitors.",
                "Power off and disconnect from all power sources before approaching.",
                "Consult a qualified technician for physical inspection.",
            ],
            emergency_action=None,
        )

    # ── Medium — proceed with standard precautions ────────────────────────────
    if _match_first(s, _MEDIUM_KEYWORDS):
        return SafetyOutput(
            is_safe_to_proceed=True,
            risk_level=RiskLevel.medium,
            blocked_reason=None,
            warnings=[
                "Power off and disconnect all power sources before touching any component.",
                "Work on a non-conductive, anti-static surface.",
                "Allow device to cool fully before handling if recently in use.",
                "Have a Class C fire extinguisher accessible when working with batteries.",
            ],
            emergency_action=None,
        )

    # ── Low — safe to proceed ─────────────────────────────────────────────────
    return SafetyOutput(
        is_safe_to_proceed=True,
        risk_level=RiskLevel.low,
        blocked_reason=None,
        warnings=[],
        emergency_action=None,
    )
