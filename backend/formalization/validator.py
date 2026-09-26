"""Representation validator for Phase 5."""
from typing import Dict, Any, List
from backend.models.schemas import ValidationResult, ValidationIssue
from backend.models.logic import LogicSchema


class RepresentationValidator:
    """Validates structural and semantic sanity of logic schemas."""

    def validate(self, schema_dict: Dict[str, Any]) -> ValidationResult:
        errors: List[ValidationIssue] = []
        warnings: List[ValidationIssue] = []

        try:
            schema = LogicSchema(**schema_dict)
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[ValidationIssue(code="SCHEMA_INVALID", message=str(e), severity="ERROR")],
                warnings=[]
            )

        # Rule variable consistency
        for r_idx, rule in enumerate(schema.rules):
            declared_vars = set(rule.variables)
            body_vars = set()
            for pred in rule.body:
                for arg in pred.arguments:
                    if arg.isupper():
                        body_vars.add(arg)
            
            for arg in rule.head.arguments:
                if arg.isupper() and arg not in body_vars:
                    errors.append(ValidationIssue(
                        code="UNDEFINED_VARIABLE",
                        message=f"Variable '{arg}' in head of rule {r_idx+1} is not bound in rule body.",
                        severity="ERROR"
                    ))

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
