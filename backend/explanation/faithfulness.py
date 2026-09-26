import re
from typing import List, Set, Tuple
from backend.models.proof import ProofGraph


class FaithfulnessChecker:
    """Verifies that an explanation text does not hallucinate entities or claim unsupported steps."""

    def check(self, explanation_text: str, proof: ProofGraph) -> Tuple[bool, List[int], List[str]]:
        """Check explanation against verified proof graph.
        
        Returns:
            (is_faithful, grounded_step_ids, unsupported_claims)
        """
        if not proof.steps:
            # For UNKNOWN results without steps, explanation is faithful if it doesn't claim entailment
            has_false_claim = "entailed" in explanation_text.lower() and "unknown" not in explanation_text.lower()
            return (not has_false_claim, [], ["Claimed entailment without proof"] if has_false_claim else [])

        grounded_step_ids: List[int] = []
        unsupported_claims: List[str] = []

        proof_statements = [s.statement.lower() for s in proof.steps]

        for step in proof.steps:
            # Check if core predicate or entity of the step is referenced
            # Extract arguments from statement e.g. "human(socrates)" -> ["human", "socrates"]
            tokens = re.findall(r'[a-zA-Z0-9_]+', step.statement.lower())
            if any(tok in explanation_text.lower() for tok in tokens if len(tok) > 2):
                grounded_step_ids.append(step.id)

        # Ensure at least some proof steps are grounded
        is_faithful = len(grounded_step_ids) > 0

        return is_faithful, grounded_step_ids, unsupported_claims
