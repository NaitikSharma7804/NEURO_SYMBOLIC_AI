import json
from pathlib import Path
from typing import List, Optional
from backend.datasets.loader import DatasetLoader, DatasetSample
from backend.models.logic import ReasoningResultEnum


class RuleTakerLoader(DatasetLoader):
    """Loader for the RuleTaker benchmark family."""

    def __init__(self, data_path: Optional[Path] = None):
        super().__init__(data_path=data_path or Path("datasets/ruletaker/examples.json"))

    def load(self) -> List[DatasetSample]:
        if self.data_path and self.data_path.exists():
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [DatasetSample(**item) for item in data]
            except Exception:
                pass

        # Diagnostic fallback
        return [
            DatasetSample(
                id="ruletaker-d1",
                category="DEPTH_1",
                premises=["Bob is quiet.", "Quiet people are smart."],
                query="Bob is smart.",
                gold_label=ReasoningResultEnum.ENTAILED,
                difficulty=1,
                depth=1,
                source="ruletaker"
            )
        ]


class ProofWriterLoader(DatasetLoader):
    """Loader for ProofWriter multi-hop proofs."""

    def __init__(self, data_path: Optional[Path] = None):
        super().__init__(data_path=data_path or Path("datasets/proofwriter/examples.json"))

    def load(self) -> List[DatasetSample]:
        if self.data_path and self.data_path.exists():
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [DatasetSample(**item) for item in data]
            except Exception:
                pass

        return [
            DatasetSample(
                id="proofwriter-01",
                category="MULTI_HOP_PROOF",
                premises=["Dave is round.", "Round things are red.", "Red things are rough."],
                query="Dave is rough.",
                gold_label=ReasoningResultEnum.ENTAILED,
                difficulty=2,
                depth=2,
                source="proofwriter"
            )
        ]


class FolioLoader(DatasetLoader):
    """Loader for the FOLIO first-order logic reasoning benchmark."""

    def __init__(self, data_path: Optional[Path] = None):
        super().__init__(data_path=data_path or Path("datasets/folio/examples.json"))

    def load(self) -> List[DatasetSample]:
        if self.data_path and self.data_path.exists():
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [DatasetSample(**item) for item in data]
            except Exception:
                pass

        return [
            DatasetSample(
                id="folio-01",
                category="FOL_REASONING",
                premises=["All Greek philosophers are mortal.", "Aristotle is a Greek philosopher."],
                query="Aristotle is mortal.",
                gold_label=ReasoningResultEnum.ENTAILED,
                difficulty=1,
                depth=1,
                source="folio"
            )
        ]
