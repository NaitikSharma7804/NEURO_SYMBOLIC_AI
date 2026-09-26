from typing import Tuple, Dict, Any, Optional
from backend.models.logic import LogicSchema, ReasoningResultEnum, PredicateModel
from backend.models.proof import ProofGraph
from backend.reasoning.base import ReasoningBackend
from backend.reasoning.knowledge_base import KnowledgeBase, GroundAtom
from backend.reasoning.inference import ForwardChainingEngine
from backend.reasoning.contradiction import ContradictionAnalyzer
from backend.proofs.generator import ProofGenerator


class DeterministicSymbolicEngine(ReasoningBackend):
    """Deterministic forward-chaining symbolic engine with contradiction analysis and proof DAG generation."""

    def __init__(
        self,
        max_iterations: int = 100,
        max_depth: int = 50,
        proof_generator: Optional[ProofGenerator] = None
    ):
        self.inference_engine = ForwardChainingEngine(
            max_iterations=max_iterations,
            max_depth=max_depth
        )
        self.proof_generator = proof_generator or ProofGenerator()
        self.contradiction_analyzer = ContradictionAnalyzer(proof_generator=self.proof_generator)

    def reason(self, schema: LogicSchema) -> Tuple[ReasoningResultEnum, ProofGraph, Dict[str, Any]]:
        # 1. Populate KnowledgeBase
        kb = KnowledgeBase.from_schema(schema)

        # 2. Run forward-chaining saturation
        facts_derived = self.inference_engine.infer(kb)

        # 3. Formulate ground query
        query_atom = GroundAtom(
            predicate=schema.query.predicate,
            arguments=tuple(schema.query.arguments),
            is_negated=schema.query.is_negated
        )

        # 4. Perform open-world contradiction and entailment analysis
        result, contradiction_analysis, primary_proof = self.contradiction_analyzer.analyze(query_atom, kb)

        metadata: Dict[str, Any] = {
            "contradiction": contradiction_analysis,
            "facts_derived": facts_derived,
            "total_facts": len(kb.facts),
            "backend": "deterministic_pure_solver"
        }

        return result, primary_proof, metadata

    def validate(self) -> bool:
        """Run self-diagnostic validation check."""
        try:
            from backend.models.logic import FactModel, RuleModel
            test_schema = LogicSchema(
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
            result, proof, _ = self.reason(test_schema)
            return result == ReasoningResultEnum.ENTAILED and proof.is_valid
        except Exception:
            return False
