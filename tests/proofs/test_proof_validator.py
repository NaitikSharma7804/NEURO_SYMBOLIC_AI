import pytest
from backend.proofs.validator import ProofValidator
from backend.models.proof import ProofGraph, ProofStep, ProofStepType
from backend.models.logic import LogicSchema, FactModel, RuleModel, PredicateModel


@pytest.fixture
def sample_schema():
    return LogicSchema(
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


def test_proof_validator_valid_proof(sample_schema):
    validator = ProofValidator()
    proof = ProofGraph(
        goal="mortal(socrates)",
        status="verified",
        steps=[
            ProofStep(id=1, type=ProofStepType.FACT, statement="human(socrates)"),
            ProofStep(id=2, type=ProofStepType.RULE, statement="human(X) -> mortal(X)"),
            ProofStep(id=3, type=ProofStepType.INFERENCE, statement="mortal(socrates)", from_steps=[1, 2])
        ],
        depth=1
    )
    result = validator.validate_proof(proof, sample_schema)
    assert result.valid is True
    assert len(result.errors) == 0


def test_proof_validator_detects_unsupported_fact(sample_schema):
    validator = ProofValidator()
    proof = ProofGraph(
        goal="mortal(socrates)",
        status="verified",
        steps=[
            ProofStep(id=1, type=ProofStepType.FACT, statement="god(zeus)"),  # Not in schema
            ProofStep(id=2, type=ProofStepType.INFERENCE, statement="mortal(socrates)", from_steps=[1])
        ],
        depth=1
    )
    result = validator.validate_proof(proof, sample_schema)
    assert result.valid is False
    assert any(e.code == "UNSUPPORTED_FACT" for e in result.errors)


def test_proof_validator_detects_unsupported_inference(sample_schema):
    validator = ProofValidator()
    proof = ProofGraph(
        goal="mortal(socrates)",
        status="verified",
        steps=[
            ProofStep(id=1, type=ProofStepType.FACT, statement="human(socrates)"),
            # Inference step with missing parent from_steps
            ProofStep(id=2, type=ProofStepType.INFERENCE, statement="mortal(socrates)", from_steps=[])
        ],
        depth=1
    )
    result = validator.validate_proof(proof, sample_schema)
    assert result.valid is False
    assert any(e.code == "UNSUPPORTED_INFERENCE" for e in result.errors)
