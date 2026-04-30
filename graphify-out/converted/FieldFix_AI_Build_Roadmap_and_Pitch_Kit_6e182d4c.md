<!-- converted from FieldFix_AI_Build_Roadmap_and_Pitch_Kit.docx -->

FieldFix AI Build Roadmap and Pitch Kit
Hackathon execution plan, demo script, milestones, and judging story


# 1. MVP Definition
- A local web app where user uploads an image and describes a symptom.
- The app runs a local repair agent powered by Gemma 4 models and local knowledge base documents.
- The output is structured: detected item, risk level, likely causes, confidence, questions, tools, next test, repair steps, stop conditions, and prevention.
- Guided Repair Mode lets the user proceed step by step and branch based on test results.
- The system can run without internet for the demo.
# 2. Build Milestones

# 3. Suggested 5-Day Hackathon Plan

# 4. Demo Script
## Opening
"When something breaks in the field, people usually need internet, a manual, or a technician. FieldFix AI gives them an offline AI technician powered by Gemma."
## Demo 1: Robotic Arm Servo Buzzing
- Show robotic arm photo/video or prepared image.
- Enter symptom: "Servo 3 makes continuous noise near certain position values."
- Show detected item and visual observations.
- Show ranked causes: mechanical binding, PWM range, power supply drop, gear damage.
- Show next best test: remove load and test neutral position.
- Switch to Guided Repair Mode and walk through 2-3 steps.
- Show prevention: calibrated min/max range and saved device memory.
## Demo 2: Raspberry Pi Not Booting
- Upload photo of Pi setup or wiring.
- Enter symptom: "Raspberry Pi is not turning on."
- Show likely causes: power, SD card, cable, GPIO short, corrupted image.
- Show minimal boot test and safety warning about GPIO shorting.
## Demo 3: Emergency Equipment Offline
- Upload flashlight/generator/radio image.
- Enter symptom: "This is not working and I have no internet."
- Show field troubleshooting plan and stop conditions.
- Emphasize that the knowledge base and model are local.
# 5. UI Cards to Build
- Detected Item Card
- Risk Level + Safety Warning Card
- Likely Causes Ranking Card
- Clarifying Questions Card
- Next Best Test Card
- Tools Needed Card
- Guided Repair Steps Card
- Decision Tree Card
- Stop Conditions Card
- Prevention + Saved Memory Card
# 6. Prompting Strategy
System instruction pattern:
You are FieldFix AI, an offline repair assistant. Your job is to diagnose likely issues, ask minimal clarifying questions, recommend safe verification tests, and guide repairs step by step. Never provide dangerous repair steps for high-risk categories. Always output valid JSON matching the schema.

User context:
- Category: robotics / electronics / emergency equipment / household / unknown
- Symptom: user text
- Available tools: list
- Skill level: beginner / maker / technician / expert
- Image observations: provided by multimodal model
- Retrieved local manual snippets: from local RAG

Required output:
- detected_item
- problem_summary
- risk_level
- repair_difficulty
- likely_causes
- clarifying_questions
- tools_needed
- next_best_test
- step_by_step_repair
- stop_conditions
- prevention
# 7. README Outline
# FieldFix AI
Offline multimodal repair copilot powered by Gemma 4 models.

## Problem
Repairs often happen without internet, manuals, or experts.

## Solution
Take a photo, describe symptoms, and get a safe diagnostic and guided repair plan.

## Features
- Offline inference
- Multimodal diagnosis
- Local RAG over manuals
- Repair decision trees
- Safety guardrails
- Guided repair mode
- Device repair memory

## Demo Scenarios
1. Robotic arm servo buzzing
2. Raspberry Pi not booting
3. Emergency equipment repair

## Architecture
Local frontend + FastAPI backend + Gemma runtime + local vector DB + SQLite memory.

## Run Locally
1. Install dependencies
2. Download/prepare local model runtime
3. Ingest knowledge base
4. Start backend
5. Start frontend
6. Disable internet and run demo
# 8. Judging Story
- Impact: helps people repair critical equipment where internet or experts are unavailable.
- AI depth: uses multimodal reasoning, structured output, RAG, safety classification, and agentic guided troubleshooting.
- Gemma fit: offline/local model capability is central to the product value, not an add-on.
- Demo clarity: judges immediately understand photo -> diagnosis -> verification -> repair.
- Portfolio value: shows robotics, embedded, edge AI, hardware debugging, and software system design.
# 9. Final Pitch Paragraph
FieldFix AI is an offline multimodal repair copilot powered by Gemma 4 models. It helps makers, field technicians, remote users, and everyday people diagnose broken equipment from images and symptoms, retrieve relevant local manuals, reason through likely causes, and follow safe step-by-step repair guidance. Unlike cloud chatbots, FieldFix is built for the moment when help is far away, internet is unavailable, and something important needs to work again.
# 10. Immediate Next Actions
- Finalize name: FieldFix AI or Fix Anything AI.
- Choose frontend: React/Next.js for polish or Streamlit for speed.
- Collect 10-15 local knowledge documents for robotics, electronics, and emergency repair.
- Create three demo datasets with images and expected outputs.
- Implement output schema and render cards before deep model work.
- Build safety guardrails early, not at the end.
| Project identity | FieldFix AI - Fix Anything, Offline. |
| --- | --- |
| Hackathon goal | Deliver a polished offline multimodal repair copilot demo with one technical hero repair and two supporting scenarios. |
| Hero scenario | Robotic arm servo buzzing and calibration repair. |
| Secondary scenarios | Raspberry Pi not booting; emergency flashlight/generator troubleshooting. |
| Milestone | What to Build | Done Criteria |
| --- | --- | --- |
| M1: UI Shell | Upload image, symptom box, category, tool inventory, skill level | User can submit a repair case and see placeholder cards. |
| M2: Structured Repair Agent | Prompt Gemma to produce validated JSON schema | UI renders real diagnosis cards from model output. |
| M3: Safety Guardrails | Risk classifier and stop-condition logic | High-risk cases show warnings and do not give unsafe steps. |
| M4: Local RAG | Ingest focused repair docs and retrieve passages | Model can use local manual context for servo/Pi/flashlight cases. |
| M5: Guided Repair Mode | One-step-at-a-time flow with user confirmation | User can say done/yes/no and receive next branch. |
| M6: Device Memory | Save repair session notes locally | Past device repair info appears in future session. |
| M7: Demo Polish | Risk meter, confidence ranking, decision tree, clean pitch script | Demo feels polished and judge-ready. |
| Day | Focus | Deliverable |
| --- | --- | --- |
| Day 1 | Product skeleton and UX | Working UI with sample outputs and final schemas. |
| Day 2 | Model integration and structured JSON | Gemma output renders in UI for servo and Pi examples. |
| Day 3 | Local RAG and safety layer | Offline manuals searchable; risk warnings working. |
| Day 4 | Guided Repair Mode and memory | Step-by-step branching and saved repair notes. |
| Day 5 | Demo polish, slides, video, README | Compelling 3-scenario demo and final submission assets. |