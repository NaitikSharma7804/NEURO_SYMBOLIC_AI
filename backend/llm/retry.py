from typing import Dict, Any, List, Optional
from backend.llm.base import BaseLLMProvider
from backend.llm.prompts import CORRECTION_PROMPT_TEMPLATE
from backend.llm.parser import parse_logic_json


class FormalizationRetryManager:
    """Manages iterative correction of formalization errors with bounded retries."""

    def __init__(self, provider: BaseLLMProvider, max_retries: int = 2):
        self.provider = provider
        self.max_retries = max_retries

    async def attempt_correction(
        self, original_input: str, errors: List[str]
    ) -> Dict[str, Any]:
        formatted_errors = "\n".join(f"- {e}" for e in errors)
        prompt = CORRECTION_PROMPT_TEMPLATE.format(
            errors=formatted_errors,
            original_input=original_input
        )
        response_text = await self.provider.generate(prompt)
        return parse_logic_json(response_text)
