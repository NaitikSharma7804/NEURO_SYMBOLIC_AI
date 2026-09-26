"""Pydantic schemas and domain models for logic representations and reasoning results."""
import re
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator


class ReasoningResultEnum(str, Enum):
    ENTAILED = "ENTAILED"
    CONTRADICTED = "CONTRADICTED"
    UNKNOWN = "UNKNOWN"


class ExplanationModeEnum(str, Enum):
    SHORT = "SHORT"
    DETAILED = "DETAILED"
    STEP_BY_STEP = "STEP_BY_STEP"
    TECHNICAL = "TECHNICAL"


def validate_predicate_identifier(v: str) -> str:
    cleaned = v.strip().lower()
    if not cleaned:
        raise ValueError("Predicate identifier cannot be empty.")
    if not re.match(r'^[a-z][a-z0-9_]*$', cleaned):
        raise ValueError(f"Invalid predicate identifier '{cleaned}'. Must be lowercase alphanumeric with underscore.")
    return cleaned


class PredicateModel(BaseModel):
    predicate: str
    arguments: List[str]
    is_negated: bool = False

    @field_validator("predicate")
    @classmethod
    def check_predicate(cls, v: str) -> str:
        return validate_predicate_identifier(v)

    @field_validator("arguments")
    @classmethod
    def check_arguments(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Predicate must have at least one argument.")
        cleaned = [arg.strip() for arg in v]
        for arg in cleaned:
            if not arg:
                raise ValueError("Arguments cannot be empty strings.")
        return cleaned


class FactModel(BaseModel):
    predicate: str
    arguments: List[str]
    is_negated: bool = False

    @field_validator("predicate")
    @classmethod
    def check_predicate(cls, v: str) -> str:
        return validate_predicate_identifier(v)

    @field_validator("arguments")
    @classmethod
    def check_arguments(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Fact must have at least one argument.")
        cleaned = [arg.strip() for arg in v]
        for arg in cleaned:
            if not arg:
                raise ValueError("Fact arguments cannot be empty strings.")
            if arg.isupper():
                raise ValueError(f"Ground facts cannot contain free variables: '{arg}'")
        return cleaned


class RuleModel(BaseModel):
    variables: List[str]
    body: List[PredicateModel]
    head: PredicateModel

    @field_validator("variables")
    @classmethod
    def check_variables(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Rule must declare at least one variable.")
        cleaned = [var.strip().upper() for var in v]
        for var in cleaned:
            if not re.match(r'^[A-Z][A-Z0-9_]*$', var):
                raise ValueError(f"Variable '{var}' must start with an uppercase letter.")
        return cleaned

    @field_validator("body")
    @classmethod
    def check_body(cls, v: List[PredicateModel]) -> List[PredicateModel]:
        if not v:
            raise ValueError("Rule body cannot be empty.")
        return v

    @model_validator(mode="after")
    def check_variable_safety(self) -> "RuleModel":
        body_vars = set()
        for p in self.body:
            for arg in p.arguments:
                if arg.isupper():
                    body_vars.add(arg)

        for arg in self.head.arguments:
            if arg.isupper() and arg not in body_vars:
                raise ValueError(f"Unsafe rule: variable '{arg}' in head is not bound in rule body.")
        return self


class LogicSchema(BaseModel):
    facts: List[FactModel] = Field(default_factory=list)
    rules: List[RuleModel] = Field(default_factory=list)
    query: PredicateModel
