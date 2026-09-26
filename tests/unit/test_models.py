import pytest
from pydantic import ValidationError
from backend.models.logic import (
    PredicateModel,
    FactModel,
    RuleModel,
    LogicSchema,
    ReasoningResultEnum,
)
from backend.models.proof import ProofStep, ProofGraph


def test_predicate_and_fact_models():
    fact = FactModel(predicate="human", arguments=["socrates"], is_negated=False)
    assert fact.predicate == "human"
    assert fact.arguments == ["socrates"]
    assert not fact.is_negated


def test_rule_model_validation():
    rule = RuleModel(
        variables=["X"],
        body=[PredicateModel(predicate="human", arguments=["X"], is_negated=False)],
        head=PredicateModel(predicate="mortal", arguments=["X"], is_negated=False)
    )
    assert len(rule.variables) == 1
    assert rule.head.predicate == "mortal"


def test_logic_schema_creation():
    schema = LogicSchema(
        facts=[FactModel(predicate="human", arguments=["socrates"])],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="human", arguments=["X"])],
                head=PredicateModel(predicate="mortal", arguments=["X"])
            )
        ],
        query=PredicateModel(predicate="mortal", arguments=["socrates"])
    )
    assert len(schema.facts) == 1
    assert len(schema.rules) == 1
    assert schema.query.arguments == ["socrates"]


def test_proof_graph_model():
    step1 = ProofStep(id=1, type="FACT", statement="human(socrates)")
    step2 = ProofStep(id=2, type="RULE", statement="human(X) -> mortal(X)")
    step3 = ProofStep(id=3, type="INFERENCE", statement="mortal(socrates)", from_steps=[1, 2])

    graph = ProofGraph(goal="mortal(socrates)", steps=[step1, step2, step3], depth=1)
    assert graph.status == "verified"
    assert len(graph.steps) == 3
