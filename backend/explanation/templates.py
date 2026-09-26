from typing import List
from backend.models.logic import ExplanationModeEnum, ReasoningResultEnum
from backend.models.proof import ProofGraph


def format_short_explanation(result: ReasoningResultEnum, goal: str, steps: List[str]) -> str:
    if result == ReasoningResultEnum.ENTAILED:
        return f"{goal} is logically ENTAILED based on the provided premises."
    elif result == ReasoningResultEnum.CONTRADICTED:
        return f"{goal} is CONTRADICTED by the premises."
    else:
        return f"The status of {goal} is UNKNOWN because neither it nor its negation can be proven from the premises."


def format_step_by_step_explanation(result: ReasoningResultEnum, goal: str, proof: ProofGraph) -> str:
    if result == ReasoningResultEnum.UNKNOWN or not proof.steps:
        return (
            f"Result: UNKNOWN\n\n"
            f"Under an open-world assumption, the available premises do not contain sufficient "
            f"information to establish either '{goal}' or its explicit negation."
        )

    lines = [f"Result: {result.value}\nGoal: {goal}\n\nDerivation Steps:"]
    for step in proof.steps:
        parent_str = f" [from steps {', '.join(map(str, step.from_steps))}]" if step.from_steps else ""
        lines.append(f"  {step.id}. ({step.type}) {step.statement}{parent_str}")

    return "\n".join(lines)


def format_detailed_explanation(result: ReasoningResultEnum, goal: str, proof: ProofGraph) -> str:
    if result == ReasoningResultEnum.UNKNOWN or not proof.steps:
        return (
            f"The status of proposition '{goal}' is UNKNOWN because it cannot be determined from the provided knowledge base. "
            f"Neither the goal nor any contradictory statement can be deduced through forward chaining."
        )

    facts = [s.statement for s in proof.steps if s.type == "FACT"]
    rules = [s.statement for s in proof.steps if s.type == "RULE"]
    inferences = [s.statement for s in proof.steps if s.type == "INFERENCE"]

    parts = [f"The proposition '{goal}' is {result.value}."]
    if facts:
        parts.append(f"We begin from the established ground facts: {', '.join(facts)}.")
    if rules:
        parts.append(f"Applying the deductive rules ({'; '.join(rules)}),")
    if inferences:
        parts.append(f"we successively derive {', '.join(inferences)}.")

    return " ".join(parts)


def format_technical_explanation(result: ReasoningResultEnum, goal: str, proof: ProofGraph) -> str:
    lines = [
        f"LOGICAL RESOLUTION REPORT",
        f"=======================",
        f"Goal: {goal}",
        f"Classification: {result.value}",
        f"Proof Depth: {proof.depth}",
        f"Steps Count: {len(proof.steps)}",
        f"Proof Validated: {proof.is_valid}",
        "",
        "PROOF DAG TRACE:"
    ]
    for s in proof.steps:
        sub_str = f" sub={s.substitutions}" if s.substitutions else ""
        lines.append(f"[{s.id}] {s.type}: {s.statement} (parents={s.from_steps}){sub_str}")

    return "\n".join(lines)
