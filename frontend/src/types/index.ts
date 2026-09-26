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

export interface HealthStatus {
  status: string;
  app_name: string;
  version: string;
  llm_provider: string;
  reasoning_backend: string;
}
