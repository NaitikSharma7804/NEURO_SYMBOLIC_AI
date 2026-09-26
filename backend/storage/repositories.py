"""Data repositories for reasoning sessions and experiment records using SQLAlchemy."""
from typing import List, Optional, Dict, Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from backend.storage.models import ReasoningSessionModel, ExperimentRunModel
from backend.storage.database import AsyncSessionLocal
from datetime import datetime, timezone


class SessionRepository:
    """Repository handling persistence and retrieval of reasoning sessions."""

    @staticmethod
    async def save_session(
        session_id: str,
        query_text: str,
        reasoning_result: str,
        formalization: Optional[Dict[str, Any]] = None,
        validation_result: Optional[Dict[str, Any]] = None,
        proof_trace: Optional[Dict[str, Any]] = None,
        explanation_text: Optional[str] = None,
        llm_provider: Optional[str] = None,
        latency_ms: Optional[float] = None
    ) -> ReasoningSessionModel:
        async with AsyncSessionLocal() as session:
            model = ReasoningSessionModel(
                session_id=session_id,
                created_at=datetime.now(timezone.utc),
                query_text=query_text,
                formalization=formalization,
                validation_result=validation_result,
                reasoning_result=reasoning_result,
                proof_trace=proof_trace,
                explanation_text=explanation_text,
                llm_provider=llm_provider,
                latency_ms=latency_ms
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model

    @staticmethod
    async def get_session(session_id: str) -> Optional[ReasoningSessionModel]:
        async with AsyncSessionLocal() as session:
            stmt = select(ReasoningSessionModel).where(ReasoningSessionModel.session_id == session_id)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    @staticmethod
    async def list_sessions(limit: int = 50, offset: int = 0) -> List[ReasoningSessionModel]:
        async with AsyncSessionLocal() as session:
            stmt = select(ReasoningSessionModel).order_by(desc(ReasoningSessionModel.created_at)).limit(limit).offset(offset)
            res = await session.execute(stmt)
            return list(res.scalars().all())


class ExperimentRepository:
    """Repository handling persistence of benchmark evaluation experiment runs."""

    @staticmethod
    async def save_run(
        experiment_id: str,
        dataset: str,
        model: str,
        baseline: str,
        metrics: Dict[str, Any],
        timestamp: Optional[datetime] = None
    ) -> ExperimentRunModel:
        async with AsyncSessionLocal() as session:
            model_record = ExperimentRunModel(
                experiment_id=experiment_id,
                timestamp=timestamp or datetime.now(timezone.utc),
                dataset=dataset,
                model=model,
                baseline=baseline,
                metrics=metrics
            )
            session.add(model_record)
            await session.commit()
            await session.refresh(model_record)
            return model_record

    @staticmethod
    async def get_run(experiment_id: str) -> Optional[ExperimentRunModel]:
        async with AsyncSessionLocal() as session:
            stmt = select(ExperimentRunModel).where(ExperimentRunModel.experiment_id == experiment_id)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    @staticmethod
    async def list_runs(limit: int = 50) -> List[ExperimentRunModel]:
        async with AsyncSessionLocal() as session:
            stmt = select(ExperimentRunModel).order_by(desc(ExperimentRunModel.timestamp)).limit(limit)
            res = await session.execute(stmt)
            return list(res.scalars().all())
