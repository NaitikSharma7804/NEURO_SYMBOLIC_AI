import json
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from backend.llm.base import BaseLLMProvider
from backend.config.settings import settings


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider for formalization and explanation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.LLM_MODEL
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        if not self.client:
            raise ValueError("OPENAI_API_KEY is not configured.")
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.0),
        )
        return response.choices[0].message.content or ""

    async def formalize(self, natural_language_text: str) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("OPENAI_API_KEY is not configured.")
        from backend.llm.prompts import FORMALIZATION_SYSTEM_PROMPT
        content = await self.generate(
            prompt=f"Translate this reasoning problem into the specified JSON format:\n\n{natural_language_text}",
            system_prompt=FORMALIZATION_SYSTEM_PROMPT,
            temperature=0.0
        )
        from backend.llm.parser import parse_logic_json
        return parse_logic_json(content)
