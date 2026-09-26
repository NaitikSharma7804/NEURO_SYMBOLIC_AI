# System Architecture

## Neuro-Symbolic AI Framework for Automated Logical Reasoning, Theorem Proving, and Explainable Decision Making

### Overview

This framework implements a modular neuro-symbolic reasoning architecture where natural language understanding is decoupled from logical inference and verification:

```text
USER QUERY
    ↓
LLM / NLP (Translation Layer)
    ↓
FACT & RULE EXTRACTION
    ↓
NATURAL LANGUAGE → STRUCTURED LOGIC
    ↓
REPRESENTATION VALIDATOR (Structural & Semantic Verification)
    ↓
KNOWLEDGE BASE
    ↓
SYMBOLIC REASONING ENGINE (Deterministic Solver: SWI-Prolog / Pure Solver)
    ↓
RESULT VERIFICATION
    ↓
ENTAILED / CONTRADICTED / UNKNOWN
    ↓
PROOF GENERATION (DAG Proof Trace)
    ↓
PROOF VALIDATOR (Independent Step-by-Step Verification)
    ↓
PROOF-GROUNDED XAI (Faithful Natural Language Explanation)
```

### Architectural Principles

1. **Separation of Concerns**: The LLM acts solely as a natural-language formalizer and natural-language explainer. It **never** determines the authoritative logical conclusion.
2. **Deterministic Grounding**: Symbolic solvers compute truth values, multi-hop chains, and contradiction status.
3. **Multi-Stage Validation**: 
   - *Stage 1*: Representation Validation rejects malformed ASTs, unbound variables, and arity mismatches before solver execution.
   - *Stage 2*: Proof Validation checks every deduction step, variable substitution, and provenance link independently of the solver output.
4. **Three-Way Logic**: The system enforces three-way classification (`ENTAILED`, `CONTRADICTED`, `UNKNOWN`) under an open-world assumption, resisting false negatives and hallucinated negative proofs.
5. **Faithful Explainability**: Explanations are strictly grounded in validated proof traces, guaranteeing zero hallucinated derivation steps.

### Layered Structure

```text
Transport Layer (FastAPI routes)
       ↓
Application Services (NeuroSymbolicReasoningService, ExperimentRunner)
       ↓
Domain Services (Formalization, Validation, Symbolic Engine, Proof, XAI)
       ↓
Infrastructure Layer (LLM Providers, SWI-Prolog Engine, SQLite/PostgreSQL)
```
