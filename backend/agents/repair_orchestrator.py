"""
Repair orchestrator — coordinates all agents into a single RepairOutput.

Pipeline:
  1. Safety pre-check (deterministic, always first)
  2. RAG retrieval
  3. Diagnosis agent
  4. Cause ranker
  5. Repair planner  (skipped if risk is critical/high)
  6. Question agent
  7. Verification agent
  8. Assemble RepairOutput
  9. Safety post-check
  10. Save to device memory
  11. Return
"""

import json
import os
from pathlib import Path

from backend.agents import (
    cause_ranker,
    diagnosis_agent,
    question_agent,
    repair_planner,
    verification_agent,
)
from backend.agents.safety_guardrails import classify_safety
from backend.memory.device_memory import save_repair
from backend.model_runtime.gemma_client import get_client
from backend.rag.retriever import retrieve, retrieve_context
from backend.schemas.repair_output import (
    Category,
    LikelyCause,
    RepairDifficulty,
    RepairOutput,
    RepairStep,
    RetrievedSource,
    RiskLevel,
)
from backend.schemas.safety_output import SafetyOutput

_DEMOS_DIR = Path(__file__).parent.parent.parent / "demos"

# keyword → demo slug (mirrors main.py routing, kept local to avoid circular import)
_ROBOTICS_KW = ("servo", "buzzing", "robotic", "robot arm", "stepper", "motor driver",
                 "encoder", "actuator", "chassis", "l298n", "l293d", "drv88", "nema")
_ELECTRONICS_KW = ("raspberry", " rpi ", "arduino", "esp32", "esp8266",
                   "microcontroller", "gpio", "i2c", " spi ", "uart",
                   "oled", "not booting", "boot loop", "upload failed")
_EMERGENCY_KW = ("flashlight", "torch", "headlamp", "generator", "smoke detector",
                 "smoke alarm", "power bank", "emergency radio")
_HOUSEHOLD_KW = ("hinge", "faucet", "tap drip", "toilet", "bike chain",
                 "wobbly", "furniture", "clogged drain", "slow drain",
                 "flickering light", "deadbolt", "door lock")


class RepairOrchestrator:
    """Stateless orchestrator. Call run() per request."""

    # ── Public entry point ─────────────────────────────────────────────────────

    async def run(
        self,
        symptom: str,
        category: str | None = None,
        device_id: str | None = None,
        use_mock: bool | None = None,
    ) -> RepairOutput:
        """
        Full repair pipeline from symptom to RepairOutput.

        Args:
            symptom:   User-reported symptom string.
            category:  Optional category slug (robotics/electronics/…).
            device_id: Optional device ID for history persistence.
            use_mock:  Override env USE_MOCK flag when explicitly set.
        """
        force_mock = use_mock if use_mock is not None else (
            os.environ.get("USE_MOCK", "false").lower() == "true"
        )

        # ── 1. Safety pre-check ────────────────────────────────────────────────
        safety: SafetyOutput = classify_safety(symptom)
        if not safety.is_safe_to_proceed:
            output = self._hard_stop_output(safety, symptom)
            if device_id:
                try:
                    save_repair(device_id, output)
                except Exception:
                    pass
            return output

        # ── 2. Mock path ───────────────────────────────────────────────────────
        if force_mock:
            cat_enum = self._parse_category(category)
            output = self._load_mock(symptom, cat_enum)
            if device_id:
                try:
                    save_repair(device_id, output)
                except Exception:
                    pass
            return output

        # ── 3. Gemma path ──────────────────────────────────────────────────────
        client = get_client()
        if not client.is_available():
            # graceful fallback if Ollama not running
            cat_enum = self._parse_category(category)
            output = self._load_mock(symptom, cat_enum)
            if device_id:
                try:
                    save_repair(device_id, output)
                except Exception:
                    pass
            return output

        # ── RAG retrieval ──────────────────────────────────────────────────────
        context_str: str = retrieve_context(symptom, category=category, top_k=4)
        sources: list[RetrievedSource] = retrieve(symptom, category=category, top_k=4)

        # ── Diagnosis ──────────────────────────────────────────────────────────
        causes: list[LikelyCause] = diagnosis_agent.run(
            symptom, category=category, client=client
        )

        # ── Cause ranking ──────────────────────────────────────────────────────
        causes = cause_ranker.run(symptom, causes, client=client)

        # ── Repair planning (skip if safety would block it) ────────────────────
        risk = safety.risk_level
        steps: list[RepairStep]
        if risk in (RiskLevel.critical, RiskLevel.high):
            steps = []
        else:
            steps = repair_planner.run(
                symptom, causes, category=category, client=client
            )

        # ── Clarifying questions ───────────────────────────────────────────────
        questions: list[str] = question_agent.run(symptom, causes, client=client)

        # ── Verification ───────────────────────────────────────────────────────
        stop_conditions, prevention = verification_agent.run(
            symptom, steps, category=category, client=client
        )

        # ── Assemble RepairOutput ──────────────────────────────────────────────
        cat_enum = self._parse_category(category)
        difficulty = self._infer_difficulty(risk, steps)
        confidence = self._compute_confidence(causes, sources)

        output = RepairOutput(
            detected_item=self._infer_detected_item(symptom, cat_enum),
            problem_summary=f"{symptom.strip().rstrip('.')}.",
            category=cat_enum,
            risk_level=risk,
            repair_difficulty=difficulty,
            confidence_overall=confidence,
            visible_observations=[symptom],
            likely_causes=causes,
            clarifying_questions=questions,
            tools_needed=self._extract_tools(steps),
            next_best_test=(
                steps[0].instruction if steps
                else "Consult a professional — this repair is beyond safe DIY scope."
            ),
            step_by_step_repair=steps,
            stop_conditions=stop_conditions,
            prevention=prevention,
            retrieved_sources=sources,
        )

        # ── Safety post-check ──────────────────────────────────────────────────
        post_safety = classify_safety(output.problem_summary)
        if not post_safety.is_safe_to_proceed:
            output = self._hard_stop_output(post_safety, symptom)

        # ── Persist to device memory ───────────────────────────────────────────
        if device_id:
            try:
                save_repair(device_id, output)
            except Exception:
                pass

        return output

    # ── Hard stop ──────────────────────────────────────────────────────────────

    def _hard_stop_output(self, safety: SafetyOutput, symptom: str) -> RepairOutput:
        """Return a valid RepairOutput with no repair steps when safety blocks."""
        stop = []
        if safety.blocked_reason:
            stop.append(safety.blocked_reason)
        if safety.emergency_action:
            stop.append(safety.emergency_action)
        if not stop:
            stop = ["This repair is unsafe — consult a professional."]

        return RepairOutput(
            detected_item=self._infer_detected_item(symptom, None),
            problem_summary=symptom.strip().rstrip(".") + ".",
            category=Category.safety,
            risk_level=RiskLevel.critical,
            repair_difficulty=RepairDifficulty.professional,
            confidence_overall=0.0,
            visible_observations=[symptom],
            likely_causes=[],
            clarifying_questions=[],
            tools_needed=[],
            next_best_test=(
                safety.emergency_action or
                "Do not attempt — contact emergency services or a qualified professional."
            ),
            step_by_step_repair=[],
            stop_conditions=stop,
            prevention=list(safety.warnings),
            retrieved_sources=[],
        )

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _load_mock(self, symptom: str, category: Category | None) -> RepairOutput:
        demo_name = self._resolve_demo(symptom, category)
        mock_path = _DEMOS_DIR / demo_name / "mock_output.json"
        raw = json.loads(mock_path.read_text(encoding="utf-8"))
        return RepairOutput.model_validate(raw)

    def _resolve_demo(self, symptom: str, category: Category | None) -> str:
        s = symptom.lower()
        if category == Category.robotics or any(k in s for k in _ROBOTICS_KW):
            return "servo_buzzing"
        if category == Category.electronics or any(
            k in s for k in (*_ELECTRONICS_KW, " pi ", "won't boot", "not boot")
        ):
            return "raspberry_pi_not_booting"
        if category == Category.emergency_equipment or any(k in s for k in _EMERGENCY_KW):
            return "flashlight_dead"
        if category in (Category.household, Category.safety) or any(
            k in s for k in _HOUSEHOLD_KW
        ):
            return "household_quick_fix"
        return "servo_buzzing"  # default

    @staticmethod
    def _parse_category(category: str | None) -> Category:
        if category is None:
            return Category.unknown
        try:
            return Category(category)
        except ValueError:
            return Category.unknown

    @staticmethod
    def _infer_difficulty(risk: RiskLevel, steps: list[RepairStep]) -> RepairDifficulty:
        if risk in (RiskLevel.critical, RiskLevel.high):
            return RepairDifficulty.professional
        if len(steps) > 6:
            return RepairDifficulty.intermediate
        return RepairDifficulty.beginner

    @staticmethod
    def _infer_detected_item(symptom: str, category: Category | None) -> str:
        s = symptom.lower()
        if "servo" in s:
            return "Servo motor"
        if "raspberry" in s or " pi " in s:
            return "Raspberry Pi"
        if "arduino" in s:
            return "Arduino"
        if "esp32" in s or "esp8266" in s:
            return "ESP32 / ESP8266"
        if "flashlight" in s or "torch" in s:
            return "Flashlight / torch"
        if "headlamp" in s:
            return "Headlamp"
        if "generator" in s:
            return "Portable generator"
        if "smoke detector" in s or "smoke alarm" in s:
            return "Smoke detector"
        if "co detector" in s or "carbon monoxide" in s:
            return "CO detector"
        if "faucet" in s or "tap" in s:
            return "Faucet / tap"
        if "hinge" in s:
            return "Door hinge"
        if "toilet" in s:
            return "Toilet"
        if "drain" in s:
            return "Drain"
        if "bike chain" in s:
            return "Bike chain"
        if category and category != Category.unknown:
            return category.value.replace("_", " ").title()
        return "Unknown device"

    @staticmethod
    def _compute_confidence(
        causes: list[LikelyCause],
        sources: list[RetrievedSource],
    ) -> float:
        if not causes:
            return 0.0
        cause_conf = sum(c.confidence for c in causes) / len(causes)
        source_boost = min(len(sources) * 0.05, 0.15)
        return round(min(cause_conf + source_boost, 0.95), 3)

    @staticmethod
    def _extract_tools(steps: list[RepairStep]) -> list[str]:
        common_tools = [
            "multimeter", "screwdriver", "wrench", "pliers", "oscilloscope",
            "voltmeter", "soldering iron", "wire stripper", "allen key",
            "hex key", "drain snake", "plunger", "contact cleaner",
        ]
        combined = " ".join(s.instruction.lower() for s in steps)
        found = [t for t in common_tools if t in combined]
        return found or ["Basic hand tools"]
