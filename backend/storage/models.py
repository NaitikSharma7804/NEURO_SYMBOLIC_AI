"""SQLAlchemy database models for reasoning sessions and experiment records."""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from datetime import datetime, timezone
from backend.storage.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class ReasoningSessionModel(Base):
    __tablename__ = "reasoning_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, index=True)
    created_at = Column(DateTime, default=utc_now)
    query_text = Column(Text, nullable=False)
    formalization = Column(JSON, nullable=True)
    validation_result = Column(JSON, nullable=True)
    reasoning_result = Column(String(32), nullable=True)
    proof_trace = Column(JSON, nullable=True)
    explanation_text = Column(Text, nullable=True)
    llm_provider = Column(String(32), nullable=True)
    latency_ms = Column(Float, nullable=True)


class ExperimentRunModel(Base):
    __tablename__ = "experiment_runs"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String(64), unique=True, index=True)
    timestamp = Column(DateTime, default=utc_now)
    dataset = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    baseline = Column(String(64), nullable=False)
    metrics = Column(JSON, nullable=False)
