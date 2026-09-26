import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.models.logic import LogicSchema, ReasoningResultEnum


class DatasetSample(BaseModel):
    id: str
    category: str
    premises: List[str]
    query: str
    gold_label: ReasoningResultEnum
    gold_logic: Optional[Dict[str, Any]] = None
    difficulty: int = 1
    depth: int = 1
    source: str = "custom"


class DatasetLoader:
    """Base dataset loader class."""

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path

    def load(self) -> List[DatasetSample]:
        raise NotImplementedError
