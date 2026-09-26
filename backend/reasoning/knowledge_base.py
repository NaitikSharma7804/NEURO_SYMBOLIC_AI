from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Optional, Set, Any
from backend.models.logic import LogicSchema, FactModel, RuleModel, PredicateModel


def normalize_predicate_negation(pred: str, is_negated: bool) -> Tuple[str, bool]:
    """Normalize predicates starting with 'not_' or explicit is_negated flag.
    
    Examples:
      normalize_predicate_negation('flies', False) -> ('flies', False)
      normalize_predicate_negation('flies', True) -> ('flies', True)
      normalize_predicate_negation('not_flies', False) -> ('flies', True)
      normalize_predicate_negation('not_flies', True) -> ('flies', False)
    """
    clean_pred = pred.strip()
    if clean_pred.startswith("not_"):
        base_pred = clean_pred[4:]
        return base_pred, not is_negated
    return clean_pred, is_negated


@dataclass(frozen=True)
class GroundAtom:
    """An instantiated ground logical atom with no free variables."""
    predicate: str
    arguments: Tuple[str, ...]
    is_negated: bool = False

    def __post_init__(self):
        norm_pred, norm_neg = normalize_predicate_negation(self.predicate, self.is_negated)
        object.__setattr__(self, "predicate", norm_pred)
        object.__setattr__(self, "arguments", tuple(arg.strip() for arg in self.arguments))
        object.__setattr__(self, "is_negated", norm_neg)

    def opposite(self) -> "GroundAtom":
        """Return the logical negation of this ground atom."""
        return GroundAtom(
            predicate=self.predicate,
            arguments=self.arguments,
            is_negated=not self.is_negated
        )

    def to_statement(self) -> str:
        prefix = "not " if self.is_negated else ""
        args_str = ", ".join(self.arguments)
        return f"{prefix}{self.predicate}({args_str})"

    def __str__(self) -> str:
        return self.to_statement()


@dataclass(frozen=True)
class PatternAtom:
    """A logical atom in a rule body or head, which may contain variables."""
    predicate: str
    arguments: Tuple[str, ...]
    is_negated: bool = False

    def __post_init__(self):
        norm_pred, norm_neg = normalize_predicate_negation(self.predicate, self.is_negated)
        object.__setattr__(self, "predicate", norm_pred)
        object.__setattr__(self, "arguments", tuple(arg.strip() for arg in self.arguments))
        object.__setattr__(self, "is_negated", norm_neg)

    def substitute(self, bindings: Dict[str, str]) -> GroundAtom:
        """Apply variable substitution bindings to produce a GroundAtom."""
        ground_args = tuple(bindings.get(arg, arg) for arg in self.arguments)
        return GroundAtom(
            predicate=self.predicate,
            arguments=ground_args,
            is_negated=self.is_negated
        )

    def to_statement(self) -> str:
        prefix = "not " if self.is_negated else ""
        args_str = ", ".join(self.arguments)
        return f"{prefix}{self.predicate}({args_str})"

    def __str__(self) -> str:
        return self.to_statement()


@dataclass
class Rule:
    """A logical deduction rule: body -> head."""
    variables: Tuple[str, ...]
    body: Tuple[PatternAtom, ...]
    head: PatternAtom
    id: Optional[str] = None

    def to_statement(self) -> str:
        body_str = " & ".join(p.to_statement() for p in self.body)
        head_str = self.head.to_statement()
        return f"{body_str} -> {head_str}"

    def __str__(self) -> str:
        return self.to_statement()


@dataclass
class FactOrigin:
    """Provenance tracking for a ground atom."""
    id: int
    is_derived: bool
    depth: int = 0
    rule: Optional[Rule] = None
    premise_atoms: List[GroundAtom] = field(default_factory=list)
    substitutions: Dict[str, str] = field(default_factory=dict)


class KnowledgeBase:
    """Stores ground facts and inference rules with full provenance tracking."""

    def __init__(self):
        self.facts: Dict[GroundAtom, FactOrigin] = {}
        self.rules: List[Rule] = []
        self._next_id: int = 1

    def add_fact(self, atom: GroundAtom, origin: Optional[FactOrigin] = None) -> bool:
        """Add a ground fact. If already present, preserves existing (or lower-depth) origin.
        
        Returns True if the fact is new or updated with lower depth, False if duplicate.
        """
        if atom in self.facts:
            existing_origin = self.facts[atom]
            if origin and origin.depth < existing_origin.depth:
                self.facts[atom] = origin
                return True
            return False

        if origin is None:
            origin = FactOrigin(
                id=self._next_id,
                is_derived=False,
                depth=0,
                rule=None,
                premise_atoms=[],
                substitutions={}
            )
            self._next_id += 1
        else:
            if origin.id == 0:
                origin.id = self._next_id
                self._next_id += 1

        self.facts[atom] = origin
        return True

    def add_rule(self, rule: Rule) -> None:
        """Add a deduction rule to the knowledge base."""
        if rule.id is None:
            rule.id = f"R{len(self.rules) + 1}"
        self.rules.append(rule)

    def has_fact(self, atom: GroundAtom) -> bool:
        """Check if a ground atom is currently established in the KB."""
        return atom in self.facts

    def get_origin(self, atom: GroundAtom) -> Optional[FactOrigin]:
        """Retrieve origin metadata for a ground atom."""
        return self.facts.get(atom)

    def get_facts(self) -> List[GroundAtom]:
        """Return list of all current ground atoms."""
        return list(self.facts.keys())

    def get_rules(self) -> List[Rule]:
        """Return list of all registered rules."""
        return list(self.rules)

    @classmethod
    def from_schema(cls, schema: LogicSchema) -> "KnowledgeBase":
        """Instantiate and populate KnowledgeBase from a Pydantic LogicSchema."""
        kb = cls()
        
        for fact_model in schema.facts:
            atom = GroundAtom(
                predicate=fact_model.predicate,
                arguments=tuple(fact_model.arguments),
                is_negated=fact_model.is_negated
            )
            kb.add_fact(atom)

        for rule_model in schema.rules:
            body_patterns = tuple(
                PatternAtom(
                    predicate=p.predicate,
                    arguments=tuple(p.arguments),
                    is_negated=p.is_negated
                )
                for p in rule_model.body
            )
            head_pattern = PatternAtom(
                predicate=rule_model.head.predicate,
                arguments=tuple(rule_model.head.arguments),
                is_negated=rule_model.head.is_negated
            )
            rule = Rule(
                variables=tuple(rule_model.variables),
                body=body_patterns,
                head=head_pattern
            )
            kb.add_rule(rule)

        return kb
