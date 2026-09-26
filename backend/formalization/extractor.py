from typing import Dict, Any, Optional
from backend.llm.base import BaseLLMProvider
from backend.llm import get_llm_provider
from backend.llm.prompts import FORMALIZATION_SYSTEM_PROMPT
from backend.llm.parser import parse_logic_json


class LogicExtractor:
    """Extracts formal logical representations from natural language text using an LLM provider."""

    def __init__(self, provider: Optional[BaseLLMProvider] = None):
        self.provider = provider or get_llm_provider()

    async def extract(self, natural_language_text: str) -> Dict[str, Any]:
        """Translates natural language text into a structured logic dictionary."""
        # Use provider formalize if implemented or generate + parse
        return await self.provider.formalize(natural_language_text)
