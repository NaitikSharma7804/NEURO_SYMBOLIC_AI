"""Controlled Prolog Compiler for translating validated LogicSchema into safe Prolog code."""
import re
from typing import List, Tuple
from backend.models.logic import LogicSchema, FactModel, RuleModel, PredicateModel


def sanitize_prolog_atom(identifier: str) -> str:
    """Sanitize and quote atom identifier if needed for Prolog syntax."""
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', identifier.strip())
    if not clean:
        clean = "atom"
    # Atoms in Prolog must start with lowercase letter
    if clean[0].isupper() or clean[0].isdigit():
        clean = f"c_{clean}"
    return clean.lower()


def sanitize_prolog_var(var_name: str) -> str:
    """Ensure Prolog variable starts with uppercase letter."""
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', var_name.strip())
    if not clean:
        clean = "X"
    if clean[0].islower():
        clean = clean.capitalize()
    return clean


class PrologCompiler:
    """Compiles validated abstract logic schemas into verifiable Prolog source code."""

    def compile_schema(self, schema: LogicSchema) -> str:
        """Translate a validated LogicSchema into a complete Prolog knowledge base file content."""
        lines: List[str] = [
            ":- dynamic fact/2.",
            ":- dynamic neg_fact/2.",
            ":- dynamic rule/3.",
            ""
        ]

        # 1. Compile facts
        for fact in schema.facts:
            pred = sanitize_prolog_atom(fact.predicate)
            args = [f"'{sanitize_prolog_atom(a)}'" for a in fact.arguments]
            args_list = f"[{', '.join(args)}]"
            if fact.is_negated:
                lines.append(f"neg_fact('{pred}', {args_list}).")
                # Also define direct negated clause
                lines.append(f"not_{pred}({', '.join(args)}).")
            else:
                lines.append(f"fact('{pred}', {args_list}).")
                lines.append(f"{pred}({', '.join(args)}).")

        lines.append("")

        # 2. Compile rules
        for idx, rule in enumerate(schema.rules):
            rule_id = f"r{idx+1}"
            
            # Direct clause generation
            head_pred = sanitize_prolog_atom(rule.head.predicate)
            if rule.head.is_negated:
                head_pred = f"not_{head_pred}"
            head_args = [sanitize_prolog_var(a) if a.isupper() else f"'{sanitize_prolog_atom(a)}'" for a in rule.head.arguments]
            head_str = f"{head_pred}({', '.join(head_args)})"

            body_clauses = []
            for b in rule.body:
                b_pred = sanitize_prolog_atom(b.predicate)
                if b.is_negated:
                    b_pred = f"not_{b_pred}"
                b_args = [sanitize_prolog_var(a) if a.isupper() else f"'{sanitize_prolog_atom(a)}'" for a in b.arguments]
                body_clauses.append(f"{b_pred}({', '.join(b_args)})")

            clause = f"{head_str} :- {', '.join(body_clauses)}."
            lines.append(f"% Rule {rule_id}")
            lines.append(clause)

        return "\n".join(lines)

    def compile_query_goals(self, query: PredicateModel) -> Tuple[str, str]:
        """Generate Prolog goals for evaluating target query and its negation.
        
        Returns (pos_goal, neg_goal).
        """
        pred = sanitize_prolog_atom(query.predicate)
        args = [f"'{sanitize_prolog_atom(a)}'" for a in query.arguments]
        args_str = ", ".join(args)

        if query.is_negated:
            pos_goal = f"not_{pred}({args_str})"
            neg_goal = f"{pred}({args_str})"
        else:
            pos_goal = f"{pred}({args_str})"
            neg_goal = f"not_{pred}({args_str})"

        return pos_goal, neg_goal
