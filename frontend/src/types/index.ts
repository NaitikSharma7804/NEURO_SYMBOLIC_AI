export type ReasoningResult = 'ENTAILED' | 'CONTRADICTED' | 'UNKNOWN';

export type ExplanationMode = 'SHORT' | 'DETAILED' | 'STEP_BY_STEP' | 'TECHNICAL';

export interface Predicate {
  predicate: string;
  arguments: string[];
  is_negated?: boolean;
}

export interface Rule {
  variables: string[];
  body: Predicate[];
  head: Predicate;
}

export interface LogicSchema {
  facts: Predicate[];
  rules: Rule[];
  query: Predicate;
}

export interface ProofStep {
  id: number;
  type: 'FACT' | 'RULE' | 'INFERENCE';
  statement: string;
  from?: number[];
  from_steps?: number[];
  rule_applied?: string;
  substitutions?: Record<string, string>;
  depth?: number;
}

export interface ProofGraph {
  goal: string;
  status: string;
  steps: ProofStep[];
  depth: number;
  is_valid: boolean;
  validation_errors: string[];
}

export interface ValidationIssue {
  code: string;
  message: string;
  severity: string;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationIssue[];
  warnings: ValidationIssue[];
}

export interface ContradictionAnalysis {
  query_status: ReasoningResult;
  query_provable: boolean;
  opposite_provable: boolean;
  conflict_detected: boolean;
  query_proof?: ProofGraph;
  opposite_proof?: ProofGraph;
}

export interface ExplanationResult {
  mode: ExplanationMode;
  text: string;
  is_faithful: boolean;
  grounded_steps: number[];
  unsupported_claims: string[];
}

export interface ReasoningResponse {
  result: ReasoningResult;
  formalization?: LogicSchema;
  validation?: ValidationResult;
  contradiction?: ContradictionAnalysis;
  proof?: ProofGraph;
  proof_validation?: ValidationResult;
  explanation?: ExplanationResult;
  metadata: Record<string, any>;
}

export interface EvaluationMetrics {
  answer_accuracy: number;
  formalization_accuracy: number;
  logical_validity: number;
  contradiction_precision: number;
  contradiction_recall: number;
  contradiction_f1: number;
  unknown_accuracy: number;
  proof_accuracy: number;
  unsupported_conclusion_rate: number;
  explanation_faithfulness: number;
  average_latency_ms: number;
  average_tokens_used: number;
}

export interface ExperimentRunRecord {
  experiment_id: string;
  timestamp: string;
  dataset: string;
  dataset_version: string;
  model: string;
  model_version: string;
  prompt_version: string;
  temperature: number;
  max_tokens: number;
  system_configuration: Record<string, any>;
  baseline: string;
  metrics: EvaluationMetrics;
}

export interface HealthStatus {
  status: string;
  app_name: string;
  version: string;
  llm_provider: string;
  reasoning_backend: string;
}
