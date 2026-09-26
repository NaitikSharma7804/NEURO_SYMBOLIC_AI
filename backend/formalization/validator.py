import re
from typing import Dict, Any, List, Set
from backend.models.schemas import ValidationResult, ValidationIssue
from backend.models.logic import LogicSchema


class RepresentationValidator:
    """Rigorous structural and semantic validator for formal logic representations."""

    def validate(self, schema_dict: Dict[str, Any]) -> ValidationResult:
        errors: List[ValidationIssue] = []
        warnings: List[ValidationIssue] = []

        if not isinstance(schema_dict, dict):
            return ValidationResult(
                valid=False,
                errors=[ValidationIssue(code="TYPE_ERROR", message="Representation root must be a JSON object.")],
                warnings=[]
            )

        # 1. Pydantic schema validation
        try:
            schema = LogicSchema(**schema_dict)
        except Exception as e:
            # Parse Pydantic validation errors into structured issues
            msg = str(e)
            if "Unsafe rule: variable" in msg or "not bound in rule body" in msg:
                code = "UNDEFINED_VARIABLE"
            elif "cannot be empty" in msg or "at least one" in msg:
                code = "EMPTY_FIELD"
            elif "Must be lowercase alphanumeric" in msg:
                code = "INVALID_PREDICATE_NAME"
            else:
                code = "SCHEMA_VALIDATION_ERROR"

            return ValidationResult(
                valid=False,
                errors=[ValidationIssue(code=code, message=msg, severity="ERROR")],
                warnings=[]
            )

        # 2. Arity consistency tracking across predicates
        predicate_arities: Dict[str, int] = {}

        for f_idx, fact in enumerate(schema.facts):
            pred = fact.predicate
            arity = len(fact.arguments)
            if pred in predicate_arities and predicate_arities[pred] != arity:
                errors.append(ValidationIssue(
                    code="INCONSISTENT_ARITY",
                    message=f"Predicate '{pred}' has inconsistent arity: expected {predicate_arities[pred]}, but fact {f_idx+1} has {arity}.",
                    severity="ERROR"
                ))
            else:
                predicate_arities[pred] = arity

        # 3. Rule checks
        for r_idx, rule in enumerate(schema.rules):
            declared_vars = set(rule.variables)
            body_vars: Set[str] = set()

            for p in rule.body:
                pred = p.predicate
                arity = len(p.arguments)
                if pred in predicate_arities and predicate_arities[pred] != arity:
                    errors.append(ValidationIssue(
                        code="INCONSISTENT_ARITY",
                        message=f"Predicate '{pred}' in body of rule {r_idx+1} has arity {arity}, expected {predicate_arities[pred]}.",
                        severity="ERROR"
                    ))
                else:
                    predicate_arities[pred] = arity

                for arg in p.arguments:
                    if arg.isupper():
                        body_vars.add(arg)

            # Check variable binding in head
            for arg in rule.head.arguments:
                if arg.isupper() and arg not in body_vars:
                    errors.append(ValidationIssue(
                        code="UNDEFINED_VARIABLE",
                        message=f"Variable '{arg}' in head of rule {r_idx+1} is not bound in rule body.",
                        severity="ERROR"
                    ))

            # Warning if variable declared but not used in body
            for var in declared_vars:
                if var not in body_vars and var not in rule.head.arguments:
                    warnings.append(ValidationIssue(
                        code="UNUSED_VARIABLE",
                        message=f"Variable '{var}' is declared in rule {r_idx+1} but never used.",
                        severity="WARNING"
                    ))

        # 4. Query arity consistency
        q_pred = schema.query.predicate
        q_arity = len(schema.query.arguments)
        if q_pred in predicate_arities and predicate_arities[q_pred] != q_arity:
            errors.append(ValidationIssue(
                code="INCONSISTENT_ARITY",
                message=f"Query predicate '{q_pred}' has arity {q_arity}, but knowledge base uses {predicate_arities[q_pred]}.",
                severity="ERROR"
            ))

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
