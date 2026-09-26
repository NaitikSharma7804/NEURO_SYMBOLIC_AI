# API Specification

## Endpoints

### 1. Health Check
`GET /health`
- **Response**: `{"status": "ok", "version": "0.1.0"}`

### 2. Neuro-Symbolic Reasoning
`POST /api/reason`
- **Request Body**:
  ```json
  {
    "query": "All humans are mortal. Socrates is human. Is Socrates mortal?",
    "mode": "full",
    "explanation_mode": "DETAILED"
  }
  ```
- **Response**:
  ```json
  {
    "result": "ENTAILED",
    "formalization": {},
    "validation": {},
    "proof": {},
    "proof_validation": {},
    "explanation": {},
    "metadata": {}
  }
  ```

### 3. Formalization
`POST /api/formalize`
- Translates natural language into structured logic representation.

### 4. Representation Validation
`POST /api/validate`
- Validates syntax, predicates, variables, rules, and semantic sanity of logic schemas.

### 5. Proof Engine
`POST /api/prove`
- Runs symbolic solver and generates validated DAG proof traces.

### 6. Explainable AI
`POST /api/explain`
- Generates proof-grounded human-readable explanations across 4 modes: `SHORT`, `DETAILED`, `STEP_BY_STEP`, `TECHNICAL`.

### 7. Experiments
`POST /api/experiments/run`
`GET /api/experiments/{id}`
- Executes and monitors reproducible benchmark runs across baselines and ablations.

### 8. Datasets
`GET /api/datasets`
- Lists available evaluation benchmarks (RuleTaker, ProofWriter, FOLIO, Custom).
