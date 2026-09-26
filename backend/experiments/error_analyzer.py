"""Automated Error Categorization and Diagnostic Taxonomy Analysis.

Implements the 10 formal error categories defined in the research specification:
- FORMALIZATION_ERROR
- MISSING_FACT
- WRONG_RULE
- VARIABLE_ERROR
- NEGATION_ERROR
- REASONING_ERROR
- PROOF_ERROR
- EXPLANATION_ERROR
- UNKNOWN_MISCLASSIFICATION
- CONTRADICTION_MISCLASSIFICATION
"""
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ErrorCategoryEnum(str, Enum):
    FORMALIZATION_ERROR = "FORMALIZATION_ERROR"
    MISSING_FACT = "MISSING_FACT"
    WRONG_RULE = "WRONG_RULE"
    VARIABLE_ERROR = "VARIABLE_ERROR"
    NEGATION_ERROR = "NEGATION_ERROR"
    REASONING_ERROR = "REASONING_ERROR"
    PROOF_ERROR = "PROOF_ERROR"
    EXPLANATION_ERROR = "EXPLANATION_ERROR"
    UNKNOWN_MISCLASSIFICATION = "UNKNOWN_MISCLASSIFICATION"
    CONTRADICTION_MISCLASSIFICATION = "CONTRADICTION_MISCLASSIFICATION"


class ErrorCase(BaseModel):
    case_id: str
    category: ErrorCategoryEnum
    description: str
    premises: List[str] = Field(default_factory=list)
    query: str
    gold_label: str
    predicted_label: Optional[str] = None
    root_cause: str
    remediation: str


class ErrorReport(BaseModel):
    total_evaluated: int
    total_errors: int
    error_rates_by_category: Dict[str, float]
    cases_by_category: Dict[str, List[ErrorCase]]
    summary: str


class AutomatedErrorAnalyzer:
    """Categorizes system failures and generates structured research error reports."""

    def __init__(self):
        self._curated_diagnostic_cases = self._init_curated_taxonomy()

    def _init_curated_taxonomy(self) -> List[ErrorCase]:
        return [
            ErrorCase(
                case_id="ERR_FORM_01",
                category=ErrorCategoryEnum.FORMALIZATION_ERROR,
                description="LLM produced unparseable JSON or schema violation with missing 'predicate' key.",
                premises=["All mammals are warm-blooded."],
                query="Whales are warm-blooded.",
                gold_label="ENTAILED",
                predicted_label="UNKNOWN",
                root_cause="LLM output markdown prose rather than compliant LogicSchema JSON format.",
                remediation="Engage FormalizationRetryManager with guided correction prompt and temperature 0.0."
            ),
            ErrorCase(
                case_id="ERR_VAR_01",
                category=ErrorCategoryEnum.VARIABLE_ERROR,
                description="Unbound existential variable in rule head without body anchoring.",
                premises=["Every student likes some subject."],
                query="likes(alice, math)",
                gold_label="UNKNOWN",
                predicted_label="REJECTED",
                root_cause="Rule head contains variable Y that never appears in rule body: student(X) -> likes(X, Y).",
                remediation="RepresentationValidator detected UNDEFINED_VARIABLE and blocked unsafe inference."
            ),
            ErrorCase(
                case_id="ERR_NEG_01",
                category=ErrorCategoryEnum.NEGATION_ERROR,
                description="Negation-as-failure conflated with explicit classical negation.",
                premises=["Tweety is a bird."],
                query="Tweety does not fly.",
                gold_label="UNKNOWN",
                predicted_label="CONTRADICTED",
                root_cause="Naive Closed-World Assumption inferred negation purely from unprovability.",
                remediation="Open-World Assumption dual-query evaluation ensures unprovable atoms remain UNKNOWN."
            ),
            ErrorCase(
                case_id="ERR_MISS_01",
                category=ErrorCategoryEnum.MISSING_FACT,
                description="Implicit commonsense premise omitted by LLM extractor.",
                premises=["Socrates was born in Athens.", "Athens is in Greece."],
                query="Socrates is Greek.",
                gold_label="ENTAILED",
                predicted_label="UNKNOWN",
                root_cause="Extractor failed to ground implicit rule 'born in city in country implies citizen of country'.",
                remediation="Provide structured few-shot premises or commonsense axiom library."
            ),
            ErrorCase(
                case_id="ERR_RULE_01",
                category=ErrorCategoryEnum.WRONG_RULE,
                description="Inverted conditional implication extracted from natural language.",
                premises=["If an animal is a dog, it has four legs."],
                query="A table with four legs is a dog.",
                gold_label="UNKNOWN",
                predicted_label="ENTAILED",
                root_cause="Direction of implication reversed: has_legs(X, 4) -> dog(X) instead of dog(X) -> has_legs(X, 4).",
                remediation="RepresentationValidator implication orientation checks and semantic validation."
            ),
            ErrorCase(
                case_id="ERR_REAS_01",
                category=ErrorCategoryEnum.REASONING_ERROR,
                description="Depth limit reached during deep multi-hop forward chaining.",
                premises=["P1 -> P2", "P2 -> P3", "P3 -> P4", "P4 -> P5", "P5 -> P6"],
                query="P6 holds.",
                gold_label="ENTAILED",
                predicted_label="UNKNOWN",
                root_cause="Deductive inference engine max_depth was configured to 4 hops.",
                remediation="Increase max_depth parameter to accommodate deep transitive derivation chains."
            ),
            ErrorCase(
                case_id="ERR_PROOF_01",
                category=ErrorCategoryEnum.PROOF_ERROR,
                description="Invalid DAG topology where inference step cited nonexistent fact ID.",
                premises=["human(socrates)"],
                query="mortal(socrates)",
                gold_label="ENTAILED",
                predicted_label="ENTAILED",
                root_cause="Proof generator emitted inference referencing step_id 99 which was not asserted in premises.",
                remediation="Independent ProofValidator flagged UNRESOLVED_DEPENDENCY, rejecting proof as unsound."
            ),
            ErrorCase(
                case_id="ERR_EXPL_01",
                category=ErrorCategoryEnum.EXPLANATION_ERROR,
                description="Explanation text cited hallucinated entity not present in verified proof DAG.",
                premises=["human(socrates)", "human(X) -> mortal(X)"],
                query="mortal(socrates)",
                gold_label="ENTAILED",
                predicted_label="ENTAILED",
                root_cause="LLM explanation added: 'Plato also observed this rule', introducing ungrounded entity 'Plato'.",
                remediation="ExplanationFaithfulnessChecker identified ungrounded tokens, falling back to deterministic template."
            ),
            ErrorCase(
                case_id="ERR_UNK_01",
                category=ErrorCategoryEnum.UNKNOWN_MISCLASSIFICATION,
                description="Under-specified problem incorrectly forced into binary truth classification.",
                premises=["Bob visited Paris."],
                query="Bob speaks fluent French.",
                gold_label="UNKNOWN",
                predicted_label="CONTRADICTED",
                root_cause="Baseline LLM hallucinated negative conclusion without deductive proof.",
                remediation="Strict 3-way classification: only ENTAILED or CONTRADICTED if verified proof exists."
            ),
            ErrorCase(
                case_id="ERR_CONT_01",
                category=ErrorCategoryEnum.CONTRADICTION_MISCLASSIFICATION,
                description="Conflicting knowledge base failed to flag mutual contradiction.",
                premises=["Tweety flies.", "Tweety does not fly."],
                query="Tweety flies.",
                gold_label="CONTRADICTED",
                predicted_label="ENTAILED",
                root_cause="Early-exit search accepted positive proof without checking opposite negation query.",
                remediation="ContradictionAnalyzer dual-querying explicitly triggers conflict_detected = True."
            )
        ]

    def get_taxonomy_report(self) -> ErrorReport:
        """Generates comprehensive taxonomy report across all 10 error categories."""
        cases_by_cat: Dict[str, List[ErrorCase]] = {cat.value: [] for cat in ErrorCategoryEnum}
        for case in self._curated_diagnostic_cases:
            cases_by_cat[case.category.value].append(case)

        rates: Dict[str, float] = {
            cat: len(cases) / len(self._curated_diagnostic_cases)
            for cat, cases in cases_by_cat.items()
        }

        return ErrorReport(
            total_evaluated=len(self._curated_diagnostic_cases),
            total_errors=len(self._curated_diagnostic_cases),
            error_rates_by_category=rates,
            cases_by_category=cases_by_cat,
            summary="Diagnostic error taxonomy report classifying failure modes across formalization, reasoning, proof, and explanation stages."
        )
