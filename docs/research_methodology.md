# Research Methodology

## Central Research Question
> Can explicit validation of the natural-language-to-symbolic representation, combined with symbolic verification and proof-grounded explanations, reduce unsupported or logically invalid conclusions compared with LLM-only and simpler neuro-symbolic reasoning pipelines?

## Core Hypotheses
1. **Hypothesis 1 (Representation Validation Effect)**: Explicit structural & semantic validation with correction loops reduces execution errors and invalid inferences caused by hallucinated or ill-formed representations.
2. **Hypothesis 2 (Contradiction & Open-World Grounding)**: Dual-query evaluation (testing $\phi$ and $\neg \phi$) resolves ambiguities and accurately detects conflicts under an open-world setting.
3. **Hypothesis 3 (Proof Faithfulness)**: Independent step-by-step verification eliminates hallucinated reasoning steps in generated natural language explanations.

## Baselines
- **Baseline A (LLM Direct)**: Zero-shot/Few-shot standard prompting.
- **Baseline B (LLM + Chain-of-Thought)**: Natural language rationale generation prior to answering.
- **Baseline C (LLM → Symbolic Solver)**: Unchecked translation directly passed to solver.
- **Baseline D (LLM → Symbolic Solver with Solver Feedback)**: Iterative refinement driven solely by solver execution failures.
- **Proposed Framework**: LLM formalizer → Representation Validator & Recovery → Deterministic Solver → Contradiction Analysis → Proof Engine → Proof Validator → Proof-Grounded XAI.
