import json
from pathlib import Path
from typing import List, Optional
from backend.datasets.loader import DatasetLoader, DatasetSample


class CustomDatasetLoader(DatasetLoader):
    """Loader for the custom diagnostic neuro-symbolic benchmark."""

    def __init__(self, data_path: Optional[Path] = None):
        default_path = Path("datasets/custom/examples.json")
        super().__init__(data_path=data_path or default_path)

    def load(self) -> List[DatasetSample]:
        if not self.data_path or not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        samples = []
        for item in data:
            samples.append(DatasetSample(**item))
        return samples
