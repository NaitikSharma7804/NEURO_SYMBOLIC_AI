# Neuro-Symbolic AI Framework for Automated Logical Reasoning, Theorem Proving, and Explainable Decision Making

A modular, reproducible, research-grade neuro-symbolic framework integrating natural language understanding with deterministic symbolic reasoning, explicit representation validation, contradiction analysis, DAG proof generation, independent proof validation, and faithful explainable AI.

---

## 1. Core Architecture

The system strictly enforces the principle:
> **LLM understands → Symbolic system reasons → Verifier checks → XAI explains.**

The LLM is **never** permitted to authoritatively determine the logical answer.

```text
USER QUERY
    ↓
LLM / NLP TRANSLATION LAYER
    ↓
FACT & RULE EXTRACTION
    ↓
NATURAL LANGUAGE → STRUCTURED LOGIC
    ↓
REPRESENTATION VALIDATOR (Structural & Semantic Sanity)
    ↓
KNOWLEDGE BASE
    ↓
SYMBOLIC REASONING ENGINE (Pure Engine / SWI-Prolog)
    ↓
RESULT VERIFICATION
    ↓
ENTAILED / CONTRADICTED / UNKNOWN
    ↓
PROOF GENERATION (DAG Provenance)
    ↓
PROOF VALIDATOR (Independent Step-by-Step Verifier)
    ↓
PROOF-GROUNDED XAI (Faithful Human-Readable Explanation)
```

---

## 2. Research Objectives & Positioning

### Primary Research Question
> Can explicit validation of the natural-language-to-symbolic representation, combined with symbolic verification and proof-grounded explanations, reduce unsupported or logically invalid conclusions compared with LLM-only and simpler neuro-symbolic reasoning pipelines?

### Research Contribution
1. **Explicit Representation Validation**: Bounded iterative correction loops rejecting malformed ASTs and unbound variables before solver invocation.
2. **Three-Way Open-World Semantics**: Robust classification across `ENTAILED`, `CONTRADICTED`, and `UNKNOWN` without closed-world collapse.
3. **Contradiction Analysis**: Dual-query evaluation ($Q$ and $\neg Q$) detecting logical conflicts and preserving counter-evidence.
4. **Independent Proof Validation**: Graph-based verification of derivation steps independent of solver internals.
5. **Faithful Explainability**: Provably grounded natural language explanations derived directly from verified proof DAGs.

---

## 3. Technology Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic v2, Uvicorn, SQLAlchemy / SQLite
- **Symbolic Reasoning**: Pure Deterministic Engine (Phase 1) & SWI-Prolog (Phase 2)
- **LLM Abstraction**: Provider-independent interface (MockProvider for deterministic testing, OpenAIProvider for production)
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons
- **Testing**: Pytest, Pytest-Asyncio, HTTPX

---

## 4. Setup and Installation

### Backend Setup
```bash
# Clone the repository
git clone <repo-url>
cd Neuro_project

# Create and activate Python virtual environment
python -m venv .venv
.venv\Scripts\activate     # On Windows
# source .venv/bin/activate  # On Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default configuration uses `LLM_PROVIDER=mock` so the entire pipeline runs offline and deterministically without external API keys.

### Running Backend
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Running Frontend
```bash
cd frontend
npm install
npm run dev
```

### Running Tests
```bash
pytest
```

---

## 5. API Reference

- `GET /health` : System health, provider details, and active reasoning engine.
- `POST /api/reason` : Full neuro-symbolic reasoning pipeline execution.
- `POST /api/formalize` : Natural language to structured logic schema translation.
- `POST /api/validate` : Logic schema representation validator.
- `POST /api/prove` : Symbolic proof graph derivation and step verification.
- `POST /api/explain` : Proof-grounded explanation generation.
- `POST /api/experiments/run` : Benchmark runner.
- `GET /api/datasets` : Evaluation benchmark suite metadata.

---

## 6. Development Roadmap

- [x] **Phase 0**: Project Initialization, Skeletons, Health Route, CI/Test Setup
- [ ] **Phase 1**: Deterministic Symbolic Engine (Pure Python Forward Chaining & Proof DAG)
- [ ] **Phase 2**: SWI-Prolog Integration & Controlled Logic Compiler
- [ ] **Phase 3**: Strict Structured Logic Schema
- [ ] **Phase 4**: LLM Formalization Layer
- [ ] **Phase 5**: Representation Validator & Recovery Loops
- [ ] **Phase 6**: Complete Integrated Neuro-Symbolic Service
- [ ] **Phase 7**: Contradiction Analysis Engine
- [ ] **Phase 8**: Proof Generator & Graph Visualizer
- [ ] **Phase 9**: Independent Proof Step Validator
- [ ] **Phase 10**: Proof-Grounded Explainable AI (XAI)
- [ ] **Phase 11**: End-to-End Robust Error Handling
- [ ] **Phase 12**: Dataset Ingestion (RuleTaker, ProofWriter, FOLIO, Custom)
- [ ] **Phase 13**: Baseline Implementations (A, B, C, D)
- [ ] **Phase 14**: Comprehensive Evaluation & Metrics
- [ ] **Phase 15**: Ablation Suite (A - F)
- [ ] **Phase 16**: Public API Finalization
- [ ] **Phase 17**: Research Dashboard & Frontend Playground
- [ ] **Phase 18**: Visual Analytics & Proof Exploration UI
- [ ] **Phase 19**: Containerization & CI/CD Pipelines
- [ ] **Phase 20**: Empirical Research Documentation
- [ ] **Phase 21**: Camera-Ready Scientific Paper

---

## 7. Limitations & Ethics

- The framework does not claim universal first-order theorem proving or general intelligence.
- All experimental accuracy claims are subject to empirical evaluation on documented benchmarks; no results are fabricated.
- Closed-world assumption is disabled by default; unprovable propositions without explicit refutation evaluate to `UNKNOWN`.
