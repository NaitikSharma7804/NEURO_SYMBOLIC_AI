import pytest
from backend.models.logic import (
    LogicSchema,
    FactModel,
    RuleModel,
    PredicateModel,
    ReasoningResultEnum
)
from backend.reasoning.z3_backend import Z3Backend


def test_z3_backend_initialization_and_validation():
    backend = Z3Backend()
    assert backend.validate() is True


def test_z3_backend_entailment_reasoning():
    backend = Z3Backend()
    # Socrates is human, all humans are mortal -> mortal(socrates)
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
    result, proof, meta = backend.reason(schema)
    assert result == ReasoningResultEnum.ENTAILED
    assert proof.is_valid is True
    assert "backend" in meta


def test_z3_backend_unknown_reasoning():
    backend = Z3Backend()
    schema = LogicSchema(
        facts=[FactModel(predicate="bird", arguments=["tweety"])],
        rules=[],
        query=PredicateModel(predicate="flies", arguments=["tweety"])
    )
    result, proof, meta = backend.reason(schema)
    assert result == ReasoningResultEnum.UNKNOWN
