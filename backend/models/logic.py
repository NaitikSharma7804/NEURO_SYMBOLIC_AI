"""Pydantic schemas and domain models for logic representations and reasoning results."""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ReasoningResultEnum(str, Enum):
    ENTAILED = "ENTAILED"
    CONTRADICTED = "CONTRADICTED"
    UNKNOWN = "UNKNOWN"


class ExplanationModeEnum(str, Enum):
    SHORT = "SHORT"
    DETAILED = "DETAILED"
    STEP_BY_STEP = "STEP_BY_STEP"
    TECHNICAL = "TECHNICAL"


class PredicateModel(BaseModel):
    predicate: str
    arguments: List[str]
    is_negated: bool = False


class FactModel(BaseModel):
    predicate: str
    arguments: List[str]
    is_negated: bool = False


class RuleModel(BaseModel):
    variables: List[str]
    body: List[PredicateModel]
    head: PredicateModel


class LogicSchema(BaseModel):
    facts: List[FactModel] = Field(default_factory=list)
    rules: List[RuleModel] = Field(default_factory=list)
    query: PredicateModel
