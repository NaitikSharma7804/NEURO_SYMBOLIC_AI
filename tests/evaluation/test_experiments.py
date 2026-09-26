import pytest
from backend.experiments.runner import ExperimentRunner
from backend.experiments.metrics import MetricsCalculator
from backend.models.logic import ReasoningResultEnum


@pytest.mark.asyncio
async def test_experiment_runner_custom_dataset():
    runner = ExperimentRunner()
    record = await runner.run_experiment(dataset_name="custom", baseline_or_variant="proposed")

    assert record.dataset == "custom"
    assert record.metrics.answer_accuracy >= 0.8
    assert record.metrics.proof_accuracy >= 0.6
    assert (runner.runs_dir / f"{record.experiment_id}.json").exists()


@pytest.mark.asyncio
async def test_baseline_evaluations():
    runner = ExperimentRunner()
    record_b = await runner.run_experiment(dataset_name="custom", baseline_or_variant="baseline_b")
    assert record_b.baseline == "baseline_b"
    assert record_b.metrics is not None


@pytest.mark.asyncio
async def test_ablation_evaluations():
    runner = ExperimentRunner()
    record_ab = await runner.run_experiment(dataset_name="custom", baseline_or_variant="ablation_b")
    assert record_ab.baseline == "ablation_b"


def test_metrics_calculator_comprehensive():
    gold = [ReasoningResultEnum.ENTAILED, ReasoningResultEnum.CONTRADICTED, ReasoningResultEnum.UNKNOWN]
    pred = [ReasoningResultEnum.ENTAILED, ReasoningResultEnum.CONTRADICTED, ReasoningResultEnum.UNKNOWN]
    valid_forms = [True, True, True]
    proof_accs = [True, True, False]
    faith = [True, True, True]
    latencies = [15.0, 20.0, 10.0]

    metrics = MetricsCalculator.calculate(
        gold_labels=gold,
        predicted_labels=pred,
        valid_formalizations=valid_forms,
        proof_accuracies=proof_accs,
        faithfulness_scores=faith,
        latencies_ms=latencies
    )

    assert metrics.answer_accuracy == 1.0
    assert metrics.contradiction_f1 == 1.0
    assert metrics.unknown_accuracy == 1.0
    assert metrics.unsupported_conclusion_rate == 0.0
