from typing import Dict, List, Set, Optional, Tuple
from backend.reasoning.knowledge_base import KnowledgeBase, GroundAtom, Rule, FactOrigin
from backend.models.proof import ProofGraph, ProofStep, ProofStepType


class ProofGenerator:
    """Constructs a normalized DAG proof trace from a populated KnowledgeBase."""

    def generate_proof(self, goal: GroundAtom, kb: KnowledgeBase) -> ProofGraph:
        goal_str = goal.to_statement()

        if not kb.has_fact(goal):
            return ProofGraph(
                goal=goal_str,
                status="unverified",
                steps=[],
                depth=0,
                is_valid=False,
                validation_errors=["Goal atom not derivable from current knowledge base."]
            )

        origin = kb.get_origin(goal)
        if origin is None:
            return ProofGraph(
                goal=goal_str,
                status="unverified",
                steps=[],
                depth=0,
                is_valid=False,
                validation_errors=["Missing origin provenance for goal atom."]
            )

        # Topological sorting to construct steps in deductive order
        step_id_counter = 1
        atom_to_step_id: Dict[GroundAtom, int] = {}
        rule_to_step_id: Dict[str, int] = {}
        proof_steps: List[ProofStep] = []

        def collect_dependencies(current_atom: GroundAtom):
            curr_origin = kb.get_origin(current_atom)
            if curr_origin is None:
                return

            if curr_origin.is_derived:
                for premise in curr_origin.premise_atoms:
                    if premise not in atom_to_step_id:
                        collect_dependencies(premise)

                # Ensure rule step exists
                if curr_origin.rule:
                    r_str = curr_origin.rule.to_statement()
                    if r_str not in rule_to_step_id:
                        nonlocal step_id_counter
                        rule_step = ProofStep(
                            id=step_id_counter,
                            type=ProofStepType.RULE,
                            statement=r_str,
                            from_steps=[],
                            depth=0
                        )
                        rule_to_step_id[r_str] = step_id_counter
                        step_id_counter += 1
                        proof_steps.append(rule_step)

                # Create inference step
                premise_step_ids = [
                    atom_to_step_id[p] for p in curr_origin.premise_atoms if p in atom_to_step_id
                ]
                if curr_origin.rule and curr_origin.rule.to_statement() in rule_to_step_id:
                    premise_step_ids.append(rule_to_step_id[curr_origin.rule.to_statement()])

                inference_step = ProofStep(
                    id=step_id_counter,
                    type=ProofStepType.INFERENCE,
                    statement=current_atom.to_statement(),
                    from_steps=premise_step_ids,
                    rule_applied=curr_origin.rule.to_statement() if curr_origin.rule else None,
                    substitutions=curr_origin.substitutions,
                    depth=curr_origin.depth
                )
                atom_to_step_id[current_atom] = step_id_counter
                step_id_counter += 1
                proof_steps.append(inference_step)

            else:
                # Base fact
                fact_step = ProofStep(
                    id=step_id_counter,
                    type=ProofStepType.FACT,
                    statement=current_atom.to_statement(),
                    from_steps=[],
                    depth=0
                )
                atom_to_step_id[current_atom] = step_id_counter
                step_id_counter += 1
                proof_steps.append(fact_step)

        collect_dependencies(goal)

        max_depth = max((s.depth for s in proof_steps), default=0)
        return ProofGraph(
            goal=goal_str,
            status="verified",
            steps=proof_steps,
            depth=max_depth,
            is_valid=True,
            validation_errors=[]
        )
