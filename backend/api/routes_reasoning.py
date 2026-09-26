from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from backend.models.schemas import (
    ReasoningRequest,
    ReasoningResponse,
    ValidationResult,
    ExplanationResult
)
from backend.models.logic import LogicSchema, ExplanationModeEnum
from backend.models.proof import ProofGraph
from backend.services.pipeline import NeuroSymbolicReasoningService
from backend.storage.repositories import SessionRepository

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
        
        # Asynchronously persist session in database repository
        try:
            await SessionRepository.save_session(
                session_id=response.session_id,
                query_text=str(request.query),
                reasoning_result=response.result.value if hasattr(response.result, 'value') else str(response.result),
                formalization=response.formalization.model_dump() if response.formalization else None,
                validation_result=response.validation.model_dump() if response.validation else None,
                proof_trace=response.proof.model_dump() if response.proof else None,
                explanation_text=response.explanation.explanation if response.explanation else None,
                llm_provider=response.metadata.get("llm_provider"),
                latency_ms=response.metadata.get("latency_ms")
            )
        except Exception:
            # Storage failure should never crash the reasoning response
            pass

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions")
async def list_recent_sessions(limit: int = 50, offset: int = 0):
    """Retrieves history of persisted reasoning sessions from SQLite database."""
    try:
        sessions = await SessionRepository.list_sessions(limit=limit, offset=offset)
        return {
            "total": len(sessions),
            "sessions": [
                {
                    "session_id": s.session_id,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                    "query_text": s.query_text,
                    "reasoning_result": s.reasoning_result,
                    "llm_provider": s.llm_provider,
                    "latency_ms": s.latency_ms
                }
                for s in sessions
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sessions: {str(e)}")


@router.get("/sessions/{session_id}")
async def get_session_detail(session_id: str):
    """Retrieves complete recorded details for a specific reasoning session."""
    session = await SessionRepository.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {
        "session_id": session.session_id,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "query_text": session.query_text,
        "reasoning_result": session.reasoning_result,
        "formalization": session.formalization,
        "validation_result": session.validation_result,
        "proof_trace": session.proof_trace,
        "explanation_text": session.explanation_text,
        "llm_provider": session.llm_provider,
        "latency_ms": session.latency_ms
    }


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
