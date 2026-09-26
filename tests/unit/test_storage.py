import pytest
import uuid
from backend.storage.database import engine, Base
from backend.storage.repositories import SessionRepository, ExperimentRepository
from backend.models.evaluation import EvaluationMetrics


@pytest.mark.asyncio
async def test_session_repository_save_and_retrieve():
    # Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_id = f"test_sess_{uuid.uuid4().hex[:8]}"
    saved = await SessionRepository.save_session(
        session_id=session_id,
        query_text="Is Socrates mortal?",
        reasoning_result="ENTAILED",
        formalization={"facts": [{"predicate": "human", "arguments": ["socrates"]}]},
        validation_result={"valid": True, "errors": []},
        proof_trace={"goal": "mortal(socrates)", "is_valid": True},
        explanation_text="Socrates is mortal because he is human.",
        llm_provider="mock",
        latency_ms=12.5
    )
    assert saved is not None
    assert saved.session_id == session_id

    # Retrieve
    retrieved = await SessionRepository.get_session(session_id)
    assert retrieved is not None
    assert retrieved.reasoning_result == "ENTAILED"
    assert retrieved.query_text == "Is Socrates mortal?"

    # List
    all_sessions = await SessionRepository.list_sessions(limit=10)
    assert len(all_sessions) >= 1
    assert any(s.session_id == session_id for s in all_sessions)


@pytest.mark.asyncio
async def test_experiment_repository_save_and_retrieve():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    exp_id = f"test_exp_{uuid.uuid4().hex[:8]}"
    metrics = {
        "answer_accuracy": 1.0,
        "formalization_accuracy": 1.0,
        "logical_validity": 1.0,
        "contradiction_precision": 1.0,
        "contradiction_recall": 1.0,
        "contradiction_f1": 1.0,
        "unknown_accuracy": 1.0,
        "proof_accuracy": 1.0,
        "unsupported_conclusion_rate": 0.0,
        "explanation_faithfulness": 1.0,
        "mean_latency_ms": 15.0
    }
    saved = await ExperimentRepository.save_run(
        experiment_id=exp_id,
        dataset="custom",
        model="mock",
        baseline="proposed",
        metrics=metrics
    )
    assert saved.experiment_id == exp_id

    retrieved = await ExperimentRepository.get_run(exp_id)
    assert retrieved is not None
    assert retrieved.dataset == "custom"
    assert retrieved.metrics["answer_accuracy"] == 1.0
