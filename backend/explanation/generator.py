from typing import Optional
from backend.models.logic import ExplanationModeEnum, ReasoningResultEnum
from backend.models.proof import ProofGraph
from backend.models.schemas import ExplanationResult
from backend.explanation.templates import (
    format_short_explanation,
    format_detailed_explanation,
    format_step_by_step_explanation,
    format_technical_explanation,
)
from backend.explanation.faithfulness import FaithfulnessChecker


class ExplanationGenerator:
    """Generates proof-grounded human-readable explanations across four configurable modes."""

    def __init__(self, checker: Optional[FaithfulnessChecker] = None):
        self.checker = checker or FaithfulnessChecker()

    def generate(
        self,
        result: ReasoningResultEnum,
        proof: ProofGraph,
        mode: ExplanationModeEnum = ExplanationModeEnum.DETAILED
    ) -> ExplanationResult:
        goal = proof.goal

        if mode == ExplanationModeEnum.SHORT:
            step_statements = [s.statement for s in proof.steps]
            text = format_short_explanation(result, goal, step_statements)
        elif mode == ExplanationModeEnum.STEP_BY_STEP:
            text = format_step_by_step_explanation(result, goal, proof)
        elif mode == ExplanationModeEnum.TECHNICAL:
            text = format_technical_explanation(result, goal, proof)
        else:
            text = format_detailed_explanation(result, goal, proof)

        is_faithful, grounded_steps, unsupported = self.checker.check(text, proof)

        return ExplanationResult(
            mode=mode,
            text=text,
            is_faithful=is_faithful,
            grounded_steps=grounded_steps,
            unsupported_claims=unsupported
        )
