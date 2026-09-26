from typing import List, Dict, Tuple, Optional, Set
from backend.reasoning.knowledge_base import (
    KnowledgeBase,
    Rule,
    PatternAtom,
    GroundAtom,
    FactOrigin,
)


class ForwardChainingEngine:
    """Deterministic forward-chaining deduction engine with provenance tracking and cycle termination."""

    def __init__(self, max_iterations: int = 100, max_depth: int = 50):
        self.max_iterations = max_iterations
        self.max_depth = max_depth

    def infer(self, kb: KnowledgeBase) -> int:
        """Run forward-chaining inference over the knowledge base until fixed point.
        
        Returns total number of newly derived facts.
        """
        total_derived = 0
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            new_in_iteration = 0
            current_facts = kb.get_facts()

            for rule in kb.get_rules():
                matches = self._match_rule_body(
                    patterns=rule.body,
                    declared_variables=set(rule.variables),
                    current_bindings={},
                    current_premises=[],
                    kb=kb,
                    current_facts=current_facts
                )

                for bindings, supporting_facts in matches:
                    head_atom = rule.head.substitute(bindings)
                    
                    # Calculate inference depth
                    premise_depths = [
                        kb.facts[p].depth for p in supporting_facts if p in kb.facts
                    ]
                    current_depth = 1 + (max(premise_depths) if premise_depths else 0)

                    if current_depth > self.max_depth:
                        continue

                    origin = FactOrigin(
                        id=0,  # Will be assigned by kb.add_fact
                        is_derived=True,
                        depth=current_depth,
                        rule=rule,
                        premise_atoms=supporting_facts,
                        substitutions=bindings
                    )

                    if kb.add_fact(head_atom, origin):
                        new_in_iteration += 1
                        total_derived += 1

            if new_in_iteration == 0:
                break

        return total_derived

    def _match_rule_body(
        self,
        patterns: Tuple[PatternAtom, ...],
        declared_variables: Set[str],
        current_bindings: Dict[str, str],
        current_premises: List[GroundAtom],
        kb: KnowledgeBase,
        current_facts: List[GroundAtom]
    ) -> List[Tuple[Dict[str, str], List[GroundAtom]]]:
        """Recursively matches conjunction of rule body patterns against known ground facts."""
        if not patterns:
            return [(current_bindings, current_premises)]

        first_pattern = patterns[0]
        remaining_patterns = patterns[1:]
        successful_matches: List[Tuple[Dict[str, str], List[GroundAtom]]] = []

        for fact in current_facts:
            # Check predicate name and polarity
            if fact.predicate != first_pattern.predicate or fact.is_negated != first_pattern.is_negated:
                continue

            if len(fact.arguments) != len(first_pattern.arguments):
                continue

            # Try unifying arguments
            bindings_copy = dict(current_bindings)
            unification_possible = True

            for p_arg, f_arg in zip(first_pattern.arguments, fact.arguments):
                is_var = (p_arg in declared_variables) or (p_arg.isupper() and len(p_arg) <= 3)
                
                if is_var:
                    if p_arg in bindings_copy:
                        if bindings_copy[p_arg] != f_arg:
                            unification_possible = False
                            break
                    else:
                        bindings_copy[p_arg] = f_arg
                else:
                    # Constant matching
                    if p_arg != f_arg:
                        unification_possible = False
                        break

            if unification_possible:
                sub_matches = self._match_rule_body(
                    patterns=remaining_patterns,
                    declared_variables=declared_variables,
                    current_bindings=bindings_copy,
                    current_premises=current_premises + [fact],
                    kb=kb,
                    current_facts=current_facts
                )
                successful_matches.extend(sub_matches)

        return successful_matches
