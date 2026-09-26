from typing import Tuple, Dict, Any, Optional
from backend.reasoning.knowledge_base import KnowledgeBase, GroundAtom
from backend.proofs.generator import ProofGenerator
from backend.models.logic import ReasoningResultEnum
from backend.models.schemas import ContradictionAnalysis
from backend.models.proof import ProofGraph


class ContradictionAnalyzer:
    """Analyzes query provability under Open-World Assumption and detects explicit contradictions/conflicts."""

    def __init__(self, proof_generator: Optional[ProofGenerator] = None):
        self.proof_generator = proof_generator or ProofGenerator()

    def analyze(self, query: GroundAtom, kb: KnowledgeBase) -> Tuple[ReasoningResultEnum, ContradictionAnalysis, ProofGraph]:
        opposite_query = query.opposite()

        query_provable = kb.has_fact(query)
        opposite_provable = kb.has_fact(opposite_query)

        query_proof: Optional[ProofGraph] = None
        opposite_proof: Optional[ProofGraph] = None

        if query_provable:
            query_proof = self.proof_generator.generate_proof(query, kb)
        if opposite_provable:
            opposite_proof = self.proof_generator.generate_proof(opposite_query, kb)

        # 1. Conflicting Knowledge: both Q and not-Q derivable
        if query_provable and opposite_provable:
            result = ReasoningResultEnum.CONTRADICTED
            conflict_detected = True
            # For primary proof in conflict, provide opposite proof which contradicts the query
            primary_proof = opposite_proof or query_proof or ProofGraph(goal=query.to_statement(), status="conflict")

        # 2. Query is provable and not contradicted
        elif query_provable and not opposite_provable:
            result = ReasoningResultEnum.ENTAILED
            conflict_detected = False
            primary_proof = query_proof or ProofGraph(goal=query.to_statement(), status="verified")

        # 3. Explicit negation is provable (query is contradicted)
        elif not query_provable and opposite_provable:
            result = ReasoningResultEnum.CONTRADICTED
            conflict_detected = False
            primary_proof = opposite_proof or ProofGraph(goal=opposite_query.to_statement(), status="verified")

        # 4. Neither is provable (Open-World Assumption -> UNKNOWN)
        else:
            result = ReasoningResultEnum.UNKNOWN
            conflict_detected = False
            primary_proof = ProofGraph(
                goal=query.to_statement(),
                status="unverified",
                steps=[],
                depth=0,
                is_valid=False,
                validation_errors=["Neither query nor explicit negation derivable from knowledge base."]
            )

        analysis = ContradictionAnalysis(
            query_status=result,
            query_provable=query_provable,
            opposite_provable=opposite_provable,
            conflict_detected=conflict_detected,
            query_proof=query_proof,
            opposite_proof=opposite_proof
        )

        return result, analysis, primary_proof
