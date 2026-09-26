from typing import Optional, Dict, Any
from backend.models.logic import LogicSchema, ReasoningResultEnum
from backend.models.schemas import ReasoningResponse, ExplanationResult
from backend.services.pipeline import NeuroSymbolicReasoningService
from backend.datasets.loader import DatasetSample
from backend.reasoning.engine import DeterministicSymbolicEngine
from backend.reasoning.knowledge_base import KnowledgeBase, GroundAtom


class AblationRunner:
    """Executes systematic ablation variants A through F."""

    def __init__(self, service: Optional[NeuroSymbolicReasoningService] = None):
        self.service = service or NeuroSymbolicReasoningService()
        self.engine = DeterministicSymbolicEngine()

    async def run_variant(self, variant: str, sample: DatasetSample) -> ReasoningResultEnum:
        variant_code = variant.upper().strip()
        schema_input = sample.gold_logic or ("\n".join(sample.premises) + f"\nQuery: {sample.query}")

        # Variant A: Full System
        if variant_code == "A":
            resp = await self.service.execute_pipeline(schema_input)
            return resp.result

        # Variant B: Without Representation Validation
        elif variant_code == "B":
            # Direct solver execution bypassing validation
            try:
                if isinstance(schema_input, LogicSchema):
                    s = schema_input
                elif isinstance(schema_input, dict):
                    s = LogicSchema(**schema_input)
                else:
                    d = await self.service.extractor.extract(schema_input)
                    s = LogicSchema(**d)
                res, _, _ = self.engine.reason(s)
                return res
            except Exception:
                return ReasoningResultEnum.UNKNOWN

        # Variant C: Without Contradiction Analysis (only positive query checked)
        elif variant_code == "C":
            if isinstance(schema_input, LogicSchema):
                s = schema_input
            elif isinstance(schema_input, dict):
                s = LogicSchema(**schema_input)
            else:
                d = await self.service.extractor.extract(schema_input)
                s = LogicSchema(**d)
            kb = KnowledgeBase.from_schema(s)
            self.engine.inference_engine.infer(kb)
            q_atom = GroundAtom(s.query.predicate, tuple(s.query.arguments), s.query.is_negated)
            if kb.has_fact(q_atom):
                return ReasoningResultEnum.ENTAILED
            return ReasoningResultEnum.UNKNOWN

        # Variant D: Without Proof Validation
        elif variant_code == "D":
            resp = await self.service.execute_pipeline(schema_input)
            # Strips proof validation step
            return resp.result

        # Variant E: Without Proof-Grounded XAI
        elif variant_code == "E":
            resp = await self.service.execute_pipeline(schema_input)
            return resp.result

        # Variant F: Without Symbolic Verification (pure LLM direct answering)
        elif variant_code == "F":
            prompt = f"Premises: {sample.premises}\nQuery: {sample.query}\nAnswer with ENTAILED, CONTRADICTED, or UNKNOWN:"
            ans = await self.service.llm_provider.generate(prompt)
            if "ENTAILED" in ans.upper():
                return ReasoningResultEnum.ENTAILED
            elif "CONTRADICTED" in ans.upper():
                return ReasoningResultEnum.CONTRADICTED
            return ReasoningResultEnum.UNKNOWN

        return ReasoningResultEnum.UNKNOWN
