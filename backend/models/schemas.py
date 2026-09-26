"""API request and response schemas."""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from backend.models.logic import LogicSchema, ReasoningResultEnum, ExplanationModeEnum
from backend.models.proof import ProofGraph


class ReasoningRequest(BaseModel):
    query: str
    mode: str = "full"
    explanation_mode: ExplanationModeEnum = ExplanationModeEnum.DETAILED


class ValidationIssue(BaseModel):
    code: str
    message: str
    severity: str = "ERROR"  # "ERROR" | "WARNING"


class ValidationResult(BaseModel):
    valid: bool
    errors: List[ValidationIssue] = Field(default_factory=list)
    warnings: List[ValidationIssue] = Field(default_factory=list)


class ContradictionAnalysis(BaseModel):
    query_status: ReasoningResultEnum
    query_provable: bool
    opposite_provable: bool
    conflict_detected: bool
    query_proof: Optional[ProofGraph] = None
    opposite_proof: Optional[ProofGraph] = None


class ExplanationResult(BaseModel):
    mode: ExplanationModeEnum
    text: str
    is_faithful: bool
    grounded_steps: List[int] = Field(default_factory=list)
    unsupported_claims: List[str] = Field(default_factory=list)


class ReasoningResponse(BaseModel):
    result: ReasoningResultEnum
    formalization: Optional[LogicSchema] = None
    validation: Optional[ValidationResult] = None
    contradiction: Optional[ContradictionAnalysis] = None
    proof: Optional[ProofGraph] = None
    proof_validation: Optional[ValidationResult] = None
    explanation: Optional[ExplanationResult] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
