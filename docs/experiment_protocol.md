# Experiment Protocol

## Evaluation Metrics
1. **Answer Accuracy**: Exact match on 3-way classification (`ENTAILED`, `CONTRADICTED`, `UNKNOWN`).
2. **Formalization Accuracy**: Syntactic and semantic validity of generated logic ASTs.
3. **Contradiction Detection F1**: Precision, recall, and harmonic mean on explicit/implicit contradiction benchmarks.
4. **Unknown Detection Accuracy**: Performance on underspecified cases without Closed-World Assumption collapse.
5. **Proof Accuracy**: Precision of derived proof DAGs against gold step annotations.
6. **Unsupported Conclusion Rate**: Percentage of queries where a positive or negative conclusion is reached without a valid proof path.
7. **Explanation Faithfulness**: Correlation between proof steps and text statements (checking for ungrounded entities or claims).
8. **Latency and Token Efficiency**: Wall-clock runtime per step and inference token consumption.

## Reproducibility Standards
- Fixed seeds for all generative components where applicable.
- Explicit recording of prompt templates, temperature, model snapshots, and solver versions.
- Raw outputs saved as structured JSON logs in `experiments/runs/` alongside metadata.
- Automated evaluation runner executing uniform splits across all models.
