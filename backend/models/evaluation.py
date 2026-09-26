"""Evaluation and experiment metrics schemas."""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class EvaluationMetrics(BaseModel):
    total_samples: int = 0
    answer_accuracy: float = 0.0
    formalization_accuracy: float = 0.0
    logical_validity: float = 0.0
    contradiction_precision: float = 0.0
    contradiction_recall: float = 0.0
    contradiction_f1: float = 0.0
    unknown_accuracy: float = 0.0
    proof_accuracy: float = 0.0
    unsupported_conclusion_rate: float = 0.0
    explanation_faithfulness: float = 0.0
    average_latency_ms: float = 0.0
    average_tokens_used: float = 0.0


class ExperimentRunRecord(BaseModel):
    experiment_id: str
    timestamp: str
    dataset: str
    dataset_version: str
    model: str
    model_version: str
    prompt_version: str
    temperature: float
    max_tokens: int
    system_configuration: Dict[str, Any] = Field(default_factory=dict)
    baseline: str
    metrics: EvaluationMetrics
