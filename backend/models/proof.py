"""Proof trace models and graph representations."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ProofStepType(str):
    FACT = "FACT"
    RULE = "RULE"
    INFERENCE = "INFERENCE"


class ProofStep(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    type: str  # FACT, RULE, INFERENCE
    statement: str
    from_steps: List[int] = Field(default_factory=list, alias="from")
    rule_applied: Optional[str] = None
    substitutions: Dict[str, str] = Field(default_factory=dict)
    depth: int = 0


class ProofGraph(BaseModel):
    goal: str
    status: str = "verified"  # verified, unverified, failed
    steps: List[ProofStep] = Field(default_factory=list)
    depth: int = 0
    is_valid: bool = True
    validation_errors: List[str] = Field(default_factory=list)
