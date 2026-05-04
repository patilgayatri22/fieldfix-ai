// FieldFix AI — TypeScript types mirroring Pydantic schemas exactly.
// Field names match backend/schemas/repair_output.py and safety_output.py.

export type Category =
  | "robotics"
  | "electronics"
  | "emergency_equipment"
  | "household"
  | "safety"
  | "unknown";

export type RiskLevel = "low" | "medium" | "high" | "critical";

export type Difficulty =
  | "beginner"
  | "intermediate"
  | "advanced"
  | "professional";

export interface LikelyCause {
  description: string;
  confidence: number;
  evidence: string;
}

export interface RepairStep {
  step_number: number;
  instruction: string;
  warning?: string | null;
  expected_outcome: string;
}

export interface RetrievedSource {
  title: string;
  source: string;
  relevance_score: number;
}

export interface RepairOutput {
  detected_item: string;
  problem_summary: string;
  category: Category;
  risk_level: RiskLevel;
  repair_difficulty: Difficulty;
  confidence_overall: number;
  visible_observations: string[];
  likely_causes: LikelyCause[];
  clarifying_questions: string[];
  tools_needed: string[];
  next_best_test: string;
  step_by_step_repair: RepairStep[];
  stop_conditions: string[];
  prevention: string[];
  retrieved_sources: RetrievedSource[];
}

export interface SafetyOutput {
  is_safe_to_proceed: boolean;
  risk_level: RiskLevel;
  blocked_reason: string | null;
  warnings: string[];
  emergency_action: string | null;
}

export interface AnalyzeRequest {
  symptom: string;
  category?: Category | null;
  device_id?: string | null;
  image_description?: string | null;
}

export interface HealthResponse {
  status: string;
  mode: string;
  kb_chunks: number;
  model?: string;
}
