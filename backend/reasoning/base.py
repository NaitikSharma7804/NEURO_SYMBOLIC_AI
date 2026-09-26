from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from backend.models.logic import LogicSchema, ReasoningResultEnum
from backend.models.proof import ProofGraph


class ReasoningBackend(ABC):
    """Abstract base class for symbolic reasoning backends (Pure Python, SWI-Prolog, Z3, etc.)."""

    @abstractmethod
    def reason(self, schema: LogicSchema) -> Tuple[ReasoningResultEnum, ProofGraph]:
        """Perform symbolic inference and return (Result, ProofGraph)."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Check if backend engine is operational and responsive."""
        pass
