import time
from typing import Optional, Dict, Any, Union
from backend.models.logic import LogicSchema, ReasoningResultEnum, ExplanationModeEnum
from backend.models.schemas import (
    ReasoningRequest,
    ReasoningResponse,
    ValidationResult,
    ContradictionAnalysis,
    ExplanationResult,
    ValidationIssue
)
from backend.llm.base import BaseLLMProvider
from backend.llm import get_llm_provider
from backend.llm.retry import FormalizationRetryManager
from backend.formalization.extractor import LogicExtractor
from backend.formalization.validator import RepresentationValidator
from backend.reasoning.base import ReasoningBackend
from backend.reasoning.engine import DeterministicSymbolicEngine
from backend.proofs.validator import ProofValidator
from backend.explanation.generator import ExplanationGenerator
from backend.config.settings import settings


class NeuroSymbolicReasoningService:
    """Core orchestration service integrating LLM formalization, representation validation,
    symbolic inference, contradiction analysis, independent proof validation, and faithful XAI.
    """

    def __init__(
        self,
        llm_provider: Optional[BaseLLMProvider] = None,
        reasoning_backend: Optional[ReasoningBackend] = None,
        validator: Optional[RepresentationValidator] = None,
        proof_validator: Optional[ProofValidator] = None,
        explainer: Optional[ExplanationGenerator] = None,
        max_retries: int = 2
    ):
        self.llm_provider = llm_provider or get_llm_provider()
        self.extractor = LogicExtractor(provider=self.llm_provider)
        self.validator = validator or RepresentationValidator()
        self.reasoning_backend = reasoning_backend or DeterministicSymbolicEngine()
        self.proof_validator = proof_validator or ProofValidator()
        self.explainer = explainer or ExplanationGenerator()
        self.retry_manager = FormalizationRetryManager(provider=self.llm_provider, max_retries=max_retries)
        self.max_retries = max_retries

    async def execute_pipeline(
        self,
        input_data: Union[str, Dict[str, Any], LogicSchema],
        mode: str = "full",
        explanation_mode: ExplanationModeEnum = ExplanationModeEnum.DETAILED
    ) -> ReasoningResponse:
        start_time = time.perf_counter()
        retries_used = 0
        raw_schema_dict: Optional[Dict[str, Any]] = None

        # 1. Formalization Step
        if isinstance(input_data, LogicSchema):
            raw_schema_dict = input_data.model_dump()
        elif isinstance(input_data, dict):
            raw_schema_dict = input_data
        else:
            # Natural language string
            raw_schema_dict = await self.extractor.extract(input_data)

        # 2. Representation Validation & Error Recovery
        val_result = self.validator.validate(raw_schema_dict)

        if not val_result.valid and isinstance(input_data, str) and self.max_retries > 0:
            while not val_result.valid and retries_used < self.max_retries:
                retries_used += 1
                error_messages = [e.message for e in val_result.errors]
                corrected_dict = await self.retry_manager.attempt_correction(input_data, error_messages)
                val_result = self.validator.validate(corrected_dict)
                if val_result.valid:
                    raw_schema_dict = corrected_dict
                    break

        if not val_result.valid:
            latency_ms = (time.perf_counter() - start_time) * 1000
            return ReasoningResponse(
                result=ReasoningResultEnum.UNKNOWN,
                formalization=None,
                validation=val_result,
                contradiction=None,
                proof=None,
                proof_validation=None,
                explanation=ExplanationResult(
                    mode=explanation_mode,
                    text=f"Validation failed: {', '.join(e.message for e in val_result.errors)}",
                    is_faithful=False
                ),
                metadata={
                    "error_stage": "REPRESENTATION_VALIDATION",
                    "retries_used": retries_used,
                    "latency_ms": latency_ms
                }
            )

        schema = LogicSchema(**raw_schema_dict)

        # 3. Deterministic Symbolic Reasoning
        result, proof, meta = self.reasoning_backend.reason(schema)

        # 4. Independent Proof Validation
        proof_val_result = self.proof_validator.validate_proof(proof, schema)

        # 5. Proof-Grounded Explainable AI
        explanation = self.explainer.generate(result, proof, mode=explanation_mode)

        latency_ms = (time.perf_counter() - start_time) * 1000

        # Construct final unified response
        contradiction_analysis: Optional[ContradictionAnalysis] = meta.get("contradiction")

        return ReasoningResponse(
            result=result,
            formalization=schema,
            validation=val_result,
            contradiction=contradiction_analysis,
            proof=proof,
            proof_validation=proof_val_result,
            explanation=explanation,
            metadata={
                **meta,
                "latency_ms": round(latency_ms, 2),
                "retries_used": retries_used,
                "llm_provider": settings.LLM_PROVIDER
            }
        )
