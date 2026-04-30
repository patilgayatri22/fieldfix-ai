# Graph Report - .  (2026-04-29)

## Corpus Check
- Corpus is ~2,746 words - fits in a single context window. You may not need a graph.

## Summary
- 55 nodes · 69 edges · 13 communities detected
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Backend RAG & Agent Pipeline|Backend RAG & Agent Pipeline]]
- [[_COMMUNITY_Safety Policy & Guardrails|Safety Policy & Guardrails]]
- [[_COMMUNITY_Diagnosis & Schema Layer|Diagnosis & Schema Layer]]
- [[_COMMUNITY_Gemma Model & Prompting|Gemma Model & Prompting]]
- [[_COMMUNITY_Device Memory & Persistence|Device Memory & Persistence]]
- [[_COMMUNITY_MVP Build Milestones|MVP Build Milestones]]
- [[_COMMUNITY_Product Vision & Frontend|Product Vision & Frontend]]
- [[_COMMUNITY_Guided Repair Mode|Guided Repair Mode]]
- [[_COMMUNITY_Robotics Demo|Robotics Demo]]
- [[_COMMUNITY_Electronics Demo|Electronics Demo]]
- [[_COMMUNITY_Demo Polish|Demo Polish]]
- [[_COMMUNITY_Target Users|Target Users]]
- [[_COMMUNITY_Deployment Strategy|Deployment Strategy]]

## God Nodes (most connected - your core abstractions)
1. `FieldFix AI` - 15 edges
2. `FastAPI Backend` - 13 edges
3. `FieldFix AI MVP` - 6 edges
4. `Chroma RAG Vector Store` - 5 edges
5. `Safety Guardrails Agent` - 5 edges
6. `Device Memory Module` - 5 edges
7. `Safety Rules Policy` - 5 edges
8. `Gemma Model Runtime` - 4 edges
9. `Repair Output Schema` - 4 edges
10. `SQLite Storage` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Item Identifier Agent Module` --semantically_similar_to--> `Diagnosis Agent`  [INFERRED] [semantically similar]
  docs/FieldFix_AI_Technical_Architecture.pdf → Claude.md
- `Safety Rules Policy` --semantically_similar_to--> `Safety Layer Component`  [INFERRED] [semantically similar]
  Claude.md → docs/FieldFix_AI_Technical_Architecture.pdf
- `Guided Repair Mode` --semantically_similar_to--> `Guided Repair Component`  [INFERRED] [semantically similar]
  graphify-out/converted/FieldFix_AI_Build_Roadmap_and_Pitch_Kit_6e182d4c.md → docs/FieldFix_AI_Technical_Architecture.pdf
- `API Endpoints` --implements--> `FastAPI Backend`  [INFERRED]
  docs/FieldFix_AI_Technical_Architecture.pdf → Claude.md
- `Guided Repair Component` --references--> `Verification Agent`  [INFERRED]
  docs/FieldFix_AI_Technical_Architecture.pdf → Claude.md

## Hyperedges (group relationships)
- **Core Offline Repair Pipeline** — claudemd_core_repair_flow, claudemd_gemma_model, claudemd_chroma_rag, claudemd_safety_guardrails, claudemd_repair_planner, claudemd_device_memory [EXTRACTED 0.95]
- **Agent Module Ensemble** — claudemd_diagnosis_agent, claudemd_question_agent, claudemd_cause_ranker, claudemd_repair_planner, claudemd_safety_guardrails, claudemd_verification_agent [EXTRACTED 0.95]
- **Demo Scenarios to Knowledge Base Mapping** — roadmap_demo_servo_buzzing, roadmap_demo_raspberry_pi, roadmap_demo_emergency_equipment, claudemd_kb_robotics, claudemd_kb_embedded_electronics, claudemd_kb_emergency_equipment [INFERRED 0.85]

## Communities

### Community 0 - "Backend RAG & Agent Pipeline"
Cohesion: 0.22
Nodes (11): API Endpoints, RAG Retriever Component, Cause Ranker Agent, Chroma RAG Vector Store, FastAPI Backend, Question Agent, RAG Ingest Module, RAG Retriever Module (+3 more)

### Community 1 - "Safety Policy & Guardrails"
Cohesion: 0.32
Nodes (8): Safety Layer Component, Technical Risks and Mitigations, Core Repair Flow, Safety Guardrails Agent, Safety Rules Policy, Repair Reasoning Loop, Risk Level Classification, Milestone M3: Safety Guardrails

### Community 2 - "Diagnosis & Schema Layer"
Cohesion: 0.4
Nodes (6): Item Identifier Agent Module, Output Schema (Structured JSON), Diagnosis Agent, Pydantic Schemas, Repair Output Schema, Safety Output Schema

### Community 3 - "Gemma Model & Prompting"
Cohesion: 0.4
Nodes (5): High-Level Architecture, Gemma Client Wrapper, Gemma Model Runtime, Skill Level Adaptation, Prompting Strategy

### Community 4 - "Device Memory & Persistence"
Cohesion: 0.5
Nodes (5): Device Memory Component, Memory Agent Module, Device Memory Module, SQLite Storage, Milestone M6: Device Memory

### Community 5 - "MVP Build Milestones"
Cohesion: 0.4
Nodes (5): Emergency Equipment Knowledge Base, Demo: Emergency Equipment Offline, Milestone M2: Structured Repair Agent, Milestone M1: UI Shell, FieldFix AI MVP

### Community 6 - "Product Vision & Frontend"
Cohesion: 0.4
Nodes (5): FieldFix AI, Household Repair Knowledge Base, Safety Guides Knowledge Base, Next.js Frontend, Product Vision: Offline Multimodal Repair Copilot

### Community 7 - "Guided Repair Mode"
Cohesion: 0.67
Nodes (3): Guided Repair Component, Guided Repair Mode, Milestone M5: Guided Repair Mode

### Community 8 - "Robotics Demo"
Cohesion: 1.0
Nodes (2): Robotics Knowledge Base, Demo: Robotic Arm Servo Buzzing

### Community 9 - "Electronics Demo"
Cohesion: 1.0
Nodes (2): Embedded / Electronics Knowledge Base, Demo: Raspberry Pi Not Booting

### Community 10 - "Demo Polish"
Cohesion: 1.0
Nodes (1): Milestone M7: Demo Polish

### Community 11 - "Target Users"
Cohesion: 1.0
Nodes (1): Target Users

### Community 12 - "Deployment Strategy"
Cohesion: 1.0
Nodes (1): Offline Deployment Levels

## Knowledge Gaps
- **21 isolated node(s):** `Next.js Frontend`, `Question Agent`, `Cause Ranker Agent`, `Repair Planner Agent`, `Household Repair Knowledge Base` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Robotics Demo`** (2 nodes): `Robotics Knowledge Base`, `Demo: Robotic Arm Servo Buzzing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Electronics Demo`** (2 nodes): `Embedded / Electronics Knowledge Base`, `Demo: Raspberry Pi Not Booting`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Demo Polish`** (1 nodes): `Milestone M7: Demo Polish`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Target Users`** (1 nodes): `Target Users`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Deployment Strategy`** (1 nodes): `Offline Deployment Levels`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FieldFix AI` connect `Product Vision & Frontend` to `Backend RAG & Agent Pipeline`, `Safety Policy & Guardrails`, `Gemma Model & Prompting`, `Device Memory & Persistence`, `MVP Build Milestones`, `Robotics Demo`, `Electronics Demo`?**
  _High betweenness centrality (0.518) - this node is a cross-community bridge._
- **Why does `FastAPI Backend` connect `Backend RAG & Agent Pipeline` to `Safety Policy & Guardrails`, `Diagnosis & Schema Layer`, `Gemma Model & Prompting`, `Device Memory & Persistence`, `Product Vision & Frontend`?**
  _High betweenness centrality (0.467) - this node is a cross-community bridge._
- **Why does `FieldFix AI MVP` connect `MVP Build Milestones` to `Robotics Demo`, `Electronics Demo`, `Product Vision & Frontend`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Chroma RAG Vector Store` (e.g. with `RAG Ingest Module` and `RAG Retriever Module`) actually correct?**
  _`Chroma RAG Vector Store` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Safety Guardrails Agent` (e.g. with `Safety Rules Policy` and `Safety Output Schema`) actually correct?**
  _`Safety Guardrails Agent` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Next.js Frontend`, `Question Agent`, `Cause Ranker Agent` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._