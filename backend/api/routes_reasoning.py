from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from backend.models.schemas import (
    ReasoningRequest,
    ReasoningResponse,
    ValidationResult,
    ExplanationResult
)
from backend.models.logic import LogicSchema, ExplanationModeEnum
from backend.models.proof import ProofGraph
from backend.services.pipeline import NeuroSymbolicReasoningService

router = APIRouter(prefix="/api", tags=["Reasoning"])

service = NeuroSymbolicReasoningService()


@router.post("/reason", response_model=ReasoningResponse)
async def reason_query(request: ReasoningRequest):
    """Executes the complete neuro-symbolic pipeline from query to verified, proof-grounded answer."""
    try:
        response = await service.execute_pipeline(
            input_data=request.query,
            mode=request.mode,
            explanation_mode=request.explanation_mode
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/formalize")
async def formalize_text(payload: Dict[str, str]):
    """Translates natural language text into structured logic JSON."""
    text = payload.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text field is required.")
    extracted = await service.extractor.extract(text)
    return extracted


@router.post("/validate", response_model=ValidationResult)
async def validate_representation(schema_dict: Dict[str, Any]):
    """Validates structural and semantic sanity of a logic schema."""
    return service.validator.validate(schema_dict)


@router.post("/prove", response_model=ProofGraph)
async def prove_goal(schema: LogicSchema):
    """Runs deterministic symbolic solver to generate a deductive proof DAG."""
    result, proof, _ = service.reasoning_backend.reason(schema)
    return proof


@router.post("/explain", response_model=ExplanationResult)
async def explain_proof(payload: Dict[str, Any]):
    """Generates a proof-grounded human-readable explanation."""
    try:
        result = payload.get("result", "ENTAILED")
        proof_data = payload.get("proof", {})
        mode_str = payload.get("mode", "DETAILED")
        mode = ExplanationModeEnum(mode_str)
        proof = ProofGraph(**proof_data)
        return service.explainer.generate(result=result, proof=proof, mode=mode)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Explanation generation failed: {str(e)}")
