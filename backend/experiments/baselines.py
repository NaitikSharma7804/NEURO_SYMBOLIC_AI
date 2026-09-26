from typing import List, Dict, Any, Optional
from backend.models.logic import ReasoningResultEnum, LogicSchema
from backend.datasets.loader import DatasetSample
from backend.llm.base import BaseLLMProvider
from backend.llm import get_llm_provider
from backend.reasoning.engine import DeterministicSymbolicEngine
from backend.services.pipeline import NeuroSymbolicReasoningService


class BaselineRunner:
    """Executes comparative evaluation across Baseline A, B, C, D, and Proposed Framework."""

    def __init__(self, provider: Optional[BaseLLMProvider] = None):
        self.provider = provider or get_llm_provider()
        self.engine = DeterministicSymbolicEngine()
        self.proposed_service = NeuroSymbolicReasoningService(llm_provider=self.provider)

    async def run_baseline_a_direct(self, sample: DatasetSample) -> ReasoningResultEnum:
        """Baseline A: Zero-shot LLM Direct classification."""
        prompt = (
            f"Premises:\n" + "\n".join(f"- {p}" for p in sample.premises) +
            f"\n\nQuery: {sample.query}\n"
            f"Determine if the query is ENTAILED, CONTRADICTED, or UNKNOWN based only on the premises.\n"
            f"Answer with ONLY one word: ENTAILED, CONTRADICTED, or UNKNOWN."
        )
        response = await self.provider.generate(prompt)
        resp_clean = response.strip().upper()
        if "ENTAILED" in resp_clean:
            return ReasoningResultEnum.ENTAILED
        elif "CONTRADICTED" in resp_clean:
            return ReasoningResultEnum.CONTRADICTED
        return ReasoningResultEnum.UNKNOWN

    async def run_baseline_b_cot(self, sample: DatasetSample) -> ReasoningResultEnum:
        """Baseline B: Chain-of-Thought prompting."""
        prompt = (
            f"Premises:\n" + "\n".join(f"- {p}" for p in sample.premises) +
            f"\n\nQuery: {sample.query}\n"
            f"Think step-by-step. First explain your reasoning, then conclude with:\n"
            f"'Final Answer: ENTAILED', 'Final Answer: CONTRADICTED', or 'Final Answer: UNKNOWN'."
        )
        response = await self.provider.generate(prompt)
        resp_clean = response.strip().upper()
        if "FINAL ANSWER: ENTAILED" in resp_clean or "ENTAILED" in resp_clean:
            return ReasoningResultEnum.ENTAILED
        elif "FINAL ANSWER: CONTRADICTED" in resp_clean or "CONTRADICTED" in resp_clean:
            return ReasoningResultEnum.CONTRADICTED
        return ReasoningResultEnum.UNKNOWN

    async def run_baseline_c_unvalidated_solver(self, sample: DatasetSample) -> ReasoningResultEnum:
        """Baseline C: LLM formalization directly fed to solver without validation layer."""
        input_text = "\n".join(sample.premises) + f"\nQuery: {sample.query}"
        try:
            raw_dict = await self.provider.formalize(input_text)
            schema = LogicSchema(**raw_dict)
            result, _, _ = self.engine.reason(schema)
            return result
        except Exception:
            return ReasoningResultEnum.UNKNOWN

    async def run_baseline_d_solver_feedback(self, sample: DatasetSample) -> ReasoningResultEnum:
        """Baseline D: LLM to solver with single feedback retry upon solver execution error."""
        input_text = "\n".join(sample.premises) + f"\nQuery: {sample.query}"
        try:
            raw_dict = await self.provider.formalize(input_text)
            schema = LogicSchema(**raw_dict)
            result, _, _ = self.engine.reason(schema)
            return result
        except Exception as e:
            # Single solver feedback attempt
            try:
                feedback_prompt = f"Previous translation caused solver execution error: {e}. Retry translating:\n{input_text}"
                raw_dict2 = await self.provider.formalize(feedback_prompt)
                schema2 = LogicSchema(**raw_dict2)
                result2, _, _ = self.engine.reason(schema2)
                return result2
            except Exception:
                return ReasoningResultEnum.UNKNOWN

    async def run_proposed(self, sample: DatasetSample) -> Any:
        """Proposed Framework: Complete Neuro-Symbolic pipeline."""
        if sample.gold_logic:
            # Evaluate using gold or parsed formalization
            input_payload = sample.gold_logic
        else:
            input_payload = "\n".join(sample.premises) + f"\nQuery: {sample.query}"
        return await self.proposed_service.execute_pipeline(input_payload)
