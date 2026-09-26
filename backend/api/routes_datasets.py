from fastapi import APIRouter
from backend.experiments.runner import ExperimentRunner

router = APIRouter(prefix="/api/datasets", tags=["Datasets"])

runner = ExperimentRunner()


@router.get("/")
async def list_datasets():
    """Lists available datasets and sample counts."""
    return {
        "datasets": [
            {
                "id": "custom",
                "name": "Custom Diagnostic Suite",
                "description": "Hand-crafted benchmark covering entailment, contradiction, unknown, multi-hop, and conflicting knowledge.",
                "sample_count": len(runner.get_dataset_samples("custom"))
            },
            {
                "id": "ruletaker",
                "name": "RuleTaker",
                "description": "Multi-hop depth reasoning with depth stratification.",
                "sample_count": len(runner.get_dataset_samples("ruletaker"))
            },
            {
                "id": "proofwriter",
                "name": "ProofWriter",
                "description": "Synthetic multi-hop natural language proofs with step annotations.",
                "sample_count": len(runner.get_dataset_samples("proofwriter"))
            },
            {
                "id": "folio",
                "name": "FOLIO",
                "description": "First-Order Logic natural language reasoning.",
                "sample_count": len(runner.get_dataset_samples("folio"))
            }
        ]
    }


@router.get("/{dataset_id}/samples")
async def get_dataset_samples(dataset_id: str):
    """Returns sample instances for a dataset."""
    samples = runner.get_dataset_samples(dataset_id)
    return {"dataset": dataset_id, "count": len(samples), "samples": [s.model_dump() for s in samples]}
