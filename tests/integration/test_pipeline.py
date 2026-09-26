import pytest
from backend.services.pipeline import NeuroSymbolicReasoningService
from backend.models.logic import ReasoningResultEnum, ExplanationModeEnum
from backend.llm.mock_provider import MockLLMProvider


@pytest.fixture
def pipeline_service():
    return NeuroSymbolicReasoningService(llm_provider=MockLLMProvider())


@pytest.mark.asyncio
async def test_scenario_1_simple_entailment(pipeline_service: NeuroSymbolicReasoningService):
    text = "All humans are mortal. Socrates is human. Is Socrates mortal?"
    resp = await pipeline_service.execute_pipeline(text)

    assert resp.result == ReasoningResultEnum.ENTAILED
    assert resp.validation.valid is True
    assert resp.proof is not None
    assert resp.proof.status == "verified"
    assert resp.proof_validation.valid is True
    assert resp.explanation.is_faithful is True
    assert "socrates" in resp.explanation.text.lower()


@pytest.mark.asyncio
async def test_scenario_2_unknown(pipeline_service: NeuroSymbolicReasoningService):
    text = "Tweety is a bird. Does Tweety fly?"
    resp = await pipeline_service.execute_pipeline(text)

    assert resp.result == ReasoningResultEnum.UNKNOWN
    assert resp.validation.valid is True
    assert resp.proof.status == "unverified"
    assert "unknown" in resp.explanation.text.lower()


@pytest.mark.asyncio
async def test_scenario_3_contradiction(pipeline_service: NeuroSymbolicReasoningService):
    text = "Penguins do not fly. Tweety is a penguin. Does Tweety fly?"
    resp = await pipeline_service.execute_pipeline(text)

    assert resp.result == ReasoningResultEnum.CONTRADICTED
    assert resp.contradiction.opposite_provable is True
    assert resp.contradiction.query_provable is False
    assert resp.proof.status == "verified"


@pytest.mark.asyncio
async def test_scenario_4_multi_hop(pipeline_service: NeuroSymbolicReasoningService):
    text = "Alice is a student. Students are people. People are mortal. Is Alice mortal?"
    resp = await pipeline_service.execute_pipeline(text)

    assert resp.result == ReasoningResultEnum.ENTAILED
    assert resp.proof.depth >= 2
    assert resp.proof_validation.valid is True


@pytest.mark.asyncio
async def test_scenario_5_conflicting_knowledge(pipeline_service: NeuroSymbolicReasoningService):
    text = "Tweety is a bird. Birds fly. Tweety does not fly. Does Tweety fly?"
    resp = await pipeline_service.execute_pipeline(text)

    assert resp.result == ReasoningResultEnum.CONTRADICTED
    assert resp.contradiction.conflict_detected is True
    assert resp.contradiction.query_provable is True
    assert resp.contradiction.opposite_provable is True


@pytest.mark.asyncio
async def test_scenario_6_invalid_formalization(pipeline_service: NeuroSymbolicReasoningService):
    # Pass bad representation with unbound variable Y in head
    bad_dict = {
        "facts": [{"predicate": "human", "arguments": ["socrates"]}],
        "rules": [
            {
                "variables": ["X"],
                "body": [{"predicate": "human", "arguments": ["X"]}],
                "head": {"predicate": "mortal", "arguments": ["Y"]}  # Y unbound
            }
        ],
        "query": {"predicate": "mortal", "arguments": ["socrates"]}
    }
    resp = await pipeline_service.execute_pipeline(bad_dict)

    assert resp.validation.valid is False
    assert any(e.code == "UNDEFINED_VARIABLE" for e in resp.validation.errors)


@pytest.mark.asyncio
async def test_explanation_modes(pipeline_service: NeuroSymbolicReasoningService):
    text = "All humans are mortal. Socrates is human. Is Socrates mortal?"

    for mode in [
        ExplanationModeEnum.SHORT,
        ExplanationModeEnum.DETAILED,
        ExplanationModeEnum.STEP_BY_STEP,
        ExplanationModeEnum.TECHNICAL
    ]:
        resp = await pipeline_service.execute_pipeline(text, explanation_mode=mode)
        assert resp.result == ReasoningResultEnum.ENTAILED
        assert resp.explanation.mode == mode
        assert len(resp.explanation.text) > 0
