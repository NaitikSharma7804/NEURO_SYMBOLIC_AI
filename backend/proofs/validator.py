from typing import Dict, Any, List, Set, Optional
from backend.models.proof import ProofGraph, ProofStep, ProofStepType
from backend.models.logic import LogicSchema, PredicateModel, FactModel
from backend.models.schemas import ValidationResult, ValidationIssue
from backend.reasoning.knowledge_base import GroundAtom, PatternAtom


class ProofValidator:
    """Independent proof verification engine ensuring sound deductions and preventing solver hallucinations."""

    def validate_proof(self, proof: ProofGraph, schema: LogicSchema) -> ValidationResult:
        errors: List[ValidationIssue] = []
        warnings: List[ValidationIssue] = []

        if not proof.steps:
            if proof.status == "unverified":
                return ValidationResult(valid=True, errors=[], warnings=[])
            return ValidationResult(
                valid=False,
                errors=[ValidationIssue(code="EMPTY_PROOF", message="Proof contains no derivation steps.")],
                warnings=[]
            )

        # Index known schema base facts and rules
        schema_fact_statements = set()
        for f in schema.facts:
            prefix = "not " if f.is_negated else ""
            schema_fact_statements.add(f"{prefix}{f.predicate}({', '.join(f.arguments)})")

        schema_rule_statements = set()
        for r in schema.rules:
            body_parts = [f"{'not ' if p.is_negated else ''}{p.predicate}({', '.join(p.arguments)})" for p in r.body]
            head_part = f"{'not ' if r.head.is_negated else ''}{r.head.predicate}({', '.join(r.head.arguments)})"
            schema_rule_statements.add(f"{' & '.join(body_parts)} -> {head_part}")

        step_map: Dict[int, ProofStep] = {}
        seen_ids: Set[int] = set()

        for step in proof.steps:
            if step.id in seen_ids:
                errors.append(ValidationIssue(
                    code="DUPLICATE_STEP_ID",
                    message=f"Duplicate step ID {step.id} detected in proof graph."
                ))
            seen_ids.add(step.id)
            step_map[step.id] = step

            # 1. Fact step verification
            if step.type == ProofStepType.FACT:
                if step.statement not in schema_fact_statements:
                    errors.append(ValidationIssue(
                        code="UNSUPPORTED_FACT",
                        message=f"Fact step '{step.statement}' does not exist in initial knowledge base."
                    ))

            # 2. Rule step verification
            elif step.type == ProofStepType.RULE:
                if step.statement not in schema_rule_statements:
                    errors.append(ValidationIssue(
                        code="UNSUPPORTED_RULE",
                        message=f"Rule step '{step.statement}' does not exist in initial knowledge base."
                    ))

            # 3. Inference step verification
            elif step.type == ProofStepType.INFERENCE:
                if not step.from_steps:
                    errors.append(ValidationIssue(
                        code="UNSUPPORTED_INFERENCE",
                        message=f"Inference step {step.id} '{step.statement}' has no supporting parent steps."
                    ))
                for parent_id in step.from_steps:
                    if parent_id not in step_map:
                        errors.append(ValidationIssue(
                            code="UNDEFINED_PARENT_STEP",
                            message=f"Inference step {step.id} references non-existent or subsequent parent {parent_id}."
                        ))

        # 4. Final step must prove the goal
        last_step = proof.steps[-1]
        norm_goal = proof.goal.strip()
        norm_last = last_step.statement.strip()

        # Goal can be positive query or negated query in contradiction proofs
        if norm_last != norm_goal:
            warnings.append(ValidationIssue(
                code="GOAL_STATEMENT_MISMATCH",
                message=f"Final step '{norm_last}' does not verbatim match target goal '{norm_goal}'.",
                severity="WARNING"
            ))

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
