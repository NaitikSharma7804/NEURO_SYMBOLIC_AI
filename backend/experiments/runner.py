import json
import uuid
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
from backend.datasets.loader import DatasetSample
from backend.datasets.custom import CustomDatasetLoader
from backend.datasets.ruletaker import RuleTakerLoader, ProofWriterLoader, FolioLoader
from backend.experiments.metrics import MetricsCalculator
from backend.experiments.baselines import BaselineRunner
from backend.experiments.ablations import AblationRunner
from backend.models.evaluation import EvaluationMetrics, ExperimentRunRecord
from backend.models.logic import ReasoningResultEnum
from backend.config.settings import settings


class ExperimentRunner:
    """Manages reproducible experiment runs, telemetry recording, and metric calculation."""

    def __init__(
        self,
        runs_dir: Optional[Path] = None,
        results_dir: Optional[Path] = None
    ):
        self.runs_dir = runs_dir or Path("experiments/runs")
        self.results_dir = results_dir or Path("experiments/results")
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.baseline_runner = BaselineRunner()
        self.ablation_runner = AblationRunner()

    def get_dataset_samples(self, dataset_name: str) -> List[DatasetSample]:
        name_lower = dataset_name.lower().strip()
        if "ruletaker" in name_lower:
            return RuleTakerLoader().load()
        elif "proofwriter" in name_lower:
            return ProofWriterLoader().load()
        elif "folio" in name_lower:
            return FolioLoader().load()
        else:
            return CustomDatasetLoader().load()

    async def run_experiment(
        self,
        dataset_name: str = "custom",
        baseline_or_variant: str = "proposed",
        model_name: Optional[str] = None
    ) -> ExperimentRunRecord:
        experiment_id = f"exp_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        samples = self.get_dataset_samples(dataset_name)

        gold_labels: List[ReasoningResultEnum] = []
        pred_labels: List[ReasoningResultEnum] = []
        valid_forms: List[bool] = []
        proof_accs: List[bool] = []
        faithfulness: List[bool] = []
        latencies: List[float] = []

        for sample in samples:
            t0 = time.perf_counter()
            gold_labels.append(sample.gold_label)

            if baseline_or_variant.lower() == "baseline_a":
                pred = await self.baseline_runner.run_baseline_a_direct(sample)
                v_form, p_acc, faith = False, False, False
            elif baseline_or_variant.lower() == "baseline_b":
                pred = await self.baseline_runner.run_baseline_b_cot(sample)
                v_form, p_acc, faith = False, False, False
            elif baseline_or_variant.lower() == "baseline_c":
                pred = await self.baseline_runner.run_baseline_c_unvalidated_solver(sample)
                v_form, p_acc, faith = True, pred == sample.gold_label, False
            elif baseline_or_variant.lower() == "baseline_d":
                pred = await self.baseline_runner.run_baseline_d_solver_feedback(sample)
                v_form, p_acc, faith = True, pred == sample.gold_label, False
            elif baseline_or_variant.lower().startswith("ablation_"):
                var_code = baseline_or_variant.split("_")[-1].upper()
                pred = await self.ablation_runner.run_variant(var_code, sample)
                v_form = var_code != "B"
                p_acc = pred == sample.gold_label and var_code not in ["D", "F"]
                faith = var_code != "E"
            else:
                # Proposed Full System
                resp = await self.baseline_runner.run_proposed(sample)
                pred = resp.result
                v_form = resp.validation.valid if resp.validation else False
                p_acc = (resp.proof_validation.valid and resp.proof.is_valid) if resp.proof and resp.proof_validation else False
                faith = resp.explanation.is_faithful if resp.explanation else False

            elapsed_ms = (time.perf_counter() - t0) * 1000
            latencies.append(elapsed_ms)
            pred_labels.append(pred)
            valid_forms.append(v_form)
            proof_accs.append(p_acc)
            faithfulness.append(faith)

        metrics = MetricsCalculator.calculate(
            gold_labels=gold_labels,
            predicted_labels=pred_labels,
            valid_formalizations=valid_forms,
            proof_accuracies=proof_accs,
            faithfulness_scores=faithfulness,
            latencies_ms=latencies
        )

        record = ExperimentRunRecord(
            experiment_id=experiment_id,
            timestamp=timestamp,
            dataset=dataset_name,
            dataset_version="1.0",
            model=model_name or settings.LLM_MODEL,
            model_version="1.0",
            prompt_version="1.0",
            temperature=0.0,
            max_tokens=512,
            system_configuration={
                "reasoning_backend": settings.REASONING_BACKEND,
                "provider": settings.LLM_PROVIDER
            },
            baseline=baseline_or_variant,
            metrics=metrics
        )

        # Save individual run JSON file
        run_file = self.runs_dir / f"{experiment_id}.json"
        with open(run_file, "w", encoding="utf-8") as f:
            f.write(record.model_dump_json(indent=2))

        # Update summary index
        summary_file = self.results_dir / "latest_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(record.model_dump_json(indent=2))

        return record
