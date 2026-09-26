# Automated Error Taxonomy and Diagnostic Analysis

This taxonomy categorizes logical and neural failure modes across benchmark evaluations:

| Error Code | Description | Diagnostic Example | Mitigation Mechanism |
| :--- | :--- | :--- | :--- |
| `FORMALIZATION_ERROR` | Syntax failure or unparseable JSON from LLM | Missing closing brackets, non-JSON output | Strict regex parser + prompt retry manager |
| `MISSING_FACT` | Premise stated in text was omitted from AST | Text: "Tweety is a bird." AST: facts=[] | Prompt explicit instruction + entity recall |
| `WRONG_RULE` | Inverted direction of implication | "If bird then flies" translated as `flies(X) -> bird(X)` | AST body/head distinction checks |
| `VARIABLE_ERROR` | Unbound or undefined variable in rule head | `human(X) -> mortal(Y)` | `RepresentationValidator` intercepts before solver |
| `NEGATION_ERROR` | Polarity flip or neglected negation prefix | "Penguins do not fly" translated as `flies(X)` | Dual polarity normalization (`not_` / `is_negated`) |
| `REASONING_ERROR` | Solver timeout or recursion depth limit | Infinite circular rules without termination | Cycle deduplication + max depth bound (50) |
| `PROOF_ERROR` | Disconnected or ungrounded proof step | Inference node referencing nonexistent parent | Independent `ProofValidator` DAG verification |
| `EXPLANATION_ERROR` | Explanation introduces ungrounded entities | Explaining Socrates mortality by mentioning Aristotle | `FaithfulnessChecker` step-token grounding check |
| `UNKNOWN_MISCLASSIFICATION` | Classifying unprovable proposition as False | Assuming Tweety cannot fly simply because unstated | Three-Way OWA decision procedure |
| `CONTRADICTION_MISCLASSIFICATION` | Silent discard of conflicting knowledge | KB derives both $P$ and $\neg P$; picking one arbitrarily | Dual-branch contradiction analyzer with conflict flag |
