# FieldFix AI - Claude Code Instructions

## Product
FieldFix AI is an offline multimodal repair copilot powered by Gemma models.

Core flow:
image/symptom -> safety pre-check -> local RAG -> structured diagnosis -> guided repair -> device memory.

## MVP Knowledge Bases
Build 5 local knowledge bases:
1. Robotics
2. Embedded / Electronics
3. Emergency Equipment
4. Household Repair
5. Safety Guides

## Demo Priority
Primary hero demo:
- Robotic arm servo buzzing and calibration

Supporting demos:
- Raspberry Pi not booting
- Flashlight/generator troubleshooting
- Household quick fix: loose hinge, leaking faucet, bike chain, or wobbly furniture

## Stack
Frontend: Next.js + Tailwind + shadcn/ui
Backend: FastAPI
Schemas: Pydantic
RAG: Chroma
Storage: SQLite
Model runtime: local Gemma wrapper with mock fallback

## Required Backend Modules
backend/main.py
backend/agents/diagnosis_agent.py
backend/agents/question_agent.py
backend/agents/cause_ranker.py
backend/agents/repair_planner.py
backend/agents/safety_guardrails.py
backend/agents/verification_agent.py
backend/rag/ingest.py
backend/rag/retriever.py
backend/memory/device_memory.py
backend/model_runtime/gemma_client.py
backend/schemas/repair_output.py
backend/schemas/safety_output.py

## Safety Rules
Never provide dangerous repair steps for:
- mains electricity
- gas leaks
- swollen lithium batteries
- smoke/fire
- microwave internals
- fuel leaks
- carbon monoxide risk
- severe shock risk
- exposed high-voltage wiring

For high-risk cases:
- external diagnosis only
- no disassembly steps
- recommend trained professional

For critical-risk cases:
- stop repair guidance
- advise emergency action or evacuation if appropriate

## Output Requirements
Every repair answer must include:
- detected_item
- problem_summary
- category
- risk_level
- repair_difficulty
- confidence_overall
- visible_observations
- likely_causes
- clarifying_questions
- tools_needed
- next_best_test
- step_by_step_repair
- stop_conditions
- prevention
- retrieved_sources

## Coding Rules
- Build schema first.
- Keep API contracts stable.
- Add mock outputs before model integration.
- Every model response must validate against Pydantic schemas.
- Every repair answer must pass safety post-check.
- Keep demo reproducible offline.
- Never hardcode secrets.
- Use small focused files.
- Do not expand scope beyond the 5 knowledge bases and 4 demo flows.
