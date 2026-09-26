import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel
from backend.experiments.runner import ExperimentRunner
from backend.models.evaluation import ExperimentRunRecord

router = APIRouter(prefix="/api/experiments", tags=["Experiments"])

runner = ExperimentRunner()


class ExperimentRunRequest(BaseModel):
    dataset: str = "custom"
    baseline: str = "proposed"  # baseline_a, baseline_b, baseline_c, baseline_d, proposed, ablation_b, etc.
    model: Optional[str] = None


@router.post("/run", response_model=ExperimentRunRecord)
async def run_experiment_endpoint(req: ExperimentRunRequest):
    """Executes a benchmark evaluation and records all metrics."""
    try:
        record = await runner.run_experiment(
            dataset_name=req.dataset,
            baseline_or_variant=req.baseline,
            model_name=req.model
        )
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{experiment_id}", response_model=ExperimentRunRecord)
async def get_experiment(experiment_id: str):
    """Retrieves saved experiment record by ID."""
    run_file = runner.runs_dir / f"{experiment_id}.json"
    if not run_file.exists():
        raise HTTPException(status_code=404, detail="Experiment record not found.")
    with open(run_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ExperimentRunRecord(**data)


@router.get("/")
async def list_experiments():
    """Lists summary of all executed experiment runs."""
    runs = []
    for p in sorted(runner.runs_dir.glob("*.json"), reverse=True):
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
                runs.append({
                    "experiment_id": d.get("experiment_id"),
                    "timestamp": d.get("timestamp"),
                    "dataset": d.get("dataset"),
                    "baseline": d.get("baseline"),
                    "accuracy": d.get("metrics", {}).get("answer_accuracy", 0.0),
                    "f1": d.get("metrics", {}).get("contradiction_f1", 0.0)
                })
        except Exception:
            continue
    return {"experiments": runs}
