import pytest
from pydantic import ValidationError
from backend.models.logic import (
    LogicSchema,
    FactModel,
    RuleModel,
    PredicateModel,
    ReasoningResultEnum,
)
from backend.reasoning.engine import DeterministicSymbolicEngine
from backend.proofs.graph import ProofDAG


@pytest.fixture
def engine():
    return DeterministicSymbolicEngine()


def test_1_simple_entailment(engine: DeterministicSymbolicEngine):
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

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.ENTAILED
    assert proof.status == "verified"
    assert proof.is_valid
    assert proof.depth == 1
    assert len(proof.steps) == 3
    dag = ProofDAG(proof)
    assert dag.is_dag()


def test_2_simple_contradiction(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[FactModel(predicate="penguin", arguments=["tweety"])],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="penguin", arguments=["X"])],
                head=PredicateModel(predicate="flies", arguments=["X"], is_negated=True)
            )
        ],
        query=PredicateModel(predicate="flies", arguments=["tweety"], is_negated=False)
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.CONTRADICTED
    contradiction_info = meta["contradiction"]
    assert not contradiction_info.query_provable
    assert contradiction_info.opposite_provable
    assert not contradiction_info.conflict_detected
    assert proof.status == "verified"


def test_3_unknown(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[FactModel(predicate="bird", arguments=["tweety"])],
        rules=[],
        query=PredicateModel(predicate="flies", arguments=["tweety"])
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.UNKNOWN
    contradiction_info = meta["contradiction"]
    assert not contradiction_info.query_provable
    assert not contradiction_info.opposite_provable
    assert not contradiction_info.conflict_detected
    assert proof.status == "unverified"


def test_4_multi_hop_reasoning(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[FactModel(predicate="student", arguments=["alice"])],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="student", arguments=["X"])],
                head=PredicateModel(predicate="person", arguments=["X"])
            ),
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="person", arguments=["X"])],
                head=PredicateModel(predicate="mortal", arguments=["X"])
            )
        ],
        query=PredicateModel(predicate="mortal", arguments=["alice"])
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.ENTAILED
    assert proof.status == "verified"
    assert proof.depth == 2
    statements = [s.statement for s in proof.steps]
    assert "student(alice)" in statements
    assert "person(alice)" in statements
    assert "mortal(alice)" in statements


def test_5_multiple_variables(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[
            FactModel(predicate="parent", arguments=["john", "mary"]),
            FactModel(predicate="parent", arguments=["mary", "alice"]),
        ],
        rules=[
            RuleModel(
                variables=["X", "Y", "Z"],
                body=[
                    PredicateModel(predicate="parent", arguments=["X", "Y"]),
                    PredicateModel(predicate="parent", arguments=["Y", "Z"]),
                ],
                head=PredicateModel(predicate="grandparent", arguments=["X", "Z"])
            )
        ],
        query=PredicateModel(predicate="grandparent", arguments=["john", "alice"])
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.ENTAILED
    assert proof.status == "verified"
    inf_step = [s for s in proof.steps if s.statement == "grandparent(john, alice)"][0]
    assert inf_step.substitutions == {"X": "john", "Y": "mary", "Z": "alice"}


def test_6_multiple_rules(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[FactModel(predicate="canary", arguments=["tweety"])],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="canary", arguments=["X"])],
                head=PredicateModel(predicate="bird", arguments=["X"])
            ),
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="bird", arguments=["X"])],
                head=PredicateModel(predicate="animal", arguments=["X"])
            ),
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="animal", arguments=["X"])],
                head=PredicateModel(predicate="organism", arguments=["X"])
            )
        ],
        query=PredicateModel(predicate="organism", arguments=["tweety"])
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.ENTAILED
    assert proof.depth == 3


def test_7_explicit_negation(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[FactModel(predicate="vegetarian", arguments=["alice"])],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="vegetarian", arguments=["X"])],
                head=PredicateModel(predicate="eats_meat", arguments=["X"], is_negated=True)
            )
        ],
        query=PredicateModel(predicate="eats_meat", arguments=["alice"], is_negated=False)
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.CONTRADICTED
    contradiction_info = meta["contradiction"]
    assert contradiction_info.opposite_provable
    assert not contradiction_info.query_provable


def test_8_conflicting_knowledge(engine: DeterministicSymbolicEngine):
    # Both flies(tweety) and not flies(tweety) derivable
    schema = LogicSchema(
        facts=[
            FactModel(predicate="bird", arguments=["tweety"]),
            FactModel(predicate="flies", arguments=["tweety"], is_negated=True)
        ],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="bird", arguments=["X"])],
                head=PredicateModel(predicate="flies", arguments=["X"], is_negated=False)
            )
        ],
        query=PredicateModel(predicate="flies", arguments=["tweety"], is_negated=False)
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.CONTRADICTED
    contradiction_info = meta["contradiction"]
    assert contradiction_info.conflict_detected
    assert contradiction_info.query_provable
    assert contradiction_info.opposite_provable
    assert contradiction_info.query_proof is not None
    assert contradiction_info.opposite_proof is not None


def test_9_no_applicable_rule(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[FactModel(predicate="cat", arguments=["felix"])],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="dog", arguments=["X"])],
                head=PredicateModel(predicate="barks", arguments=["X"])
            )
        ],
        query=PredicateModel(predicate="barks", arguments=["felix"])
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.UNKNOWN
    assert proof.status == "unverified"


def test_10_invalid_input():
    with pytest.raises(ValidationError):
        # Missing required arguments or predicate
        FactModel(predicate="human")  # type: ignore

    with pytest.raises(ValidationError):
        LogicSchema(
            facts=[],
            rules=[],
            query=None  # type: ignore
        )


def test_11_cyclic_rules(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[FactModel(predicate="p", arguments=["a"])],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="p", arguments=["X"])],
                head=PredicateModel(predicate="q", arguments=["X"])
            ),
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="q", arguments=["X"])],
                head=PredicateModel(predicate="p", arguments=["X"])
            )
        ],
        query=PredicateModel(predicate="q", arguments=["a"])
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.ENTAILED
    assert proof.status == "verified"
    assert proof.depth == 1


def test_12_duplicate_facts(engine: DeterministicSymbolicEngine):
    schema = LogicSchema(
        facts=[
            FactModel(predicate="human", arguments=["socrates"]),
            FactModel(predicate="human", arguments=["socrates"]),
            FactModel(predicate="human", arguments=["socrates"])
        ],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="human", arguments=["X"])],
                head=PredicateModel(predicate="mortal", arguments=["X"])
            )
        ],
        query=PredicateModel(predicate="mortal", arguments=["socrates"])
    )

    result, proof, meta = engine.reason(schema)

    assert result == ReasoningResultEnum.ENTAILED
    # Should only contain 1 fact step for human(socrates)
    fact_steps = [s for s in proof.steps if s.type == "FACT"]
    assert len(fact_steps) == 1
    assert fact_steps[0].statement == "human(socrates)"


def test_engine_self_validation(engine: DeterministicSymbolicEngine):
    assert engine.validate() is True
