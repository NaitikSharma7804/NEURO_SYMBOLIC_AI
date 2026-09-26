from typing import Optional
from backend.llm.base import BaseLLMProvider
from backend.llm.mock_provider import MockLLMProvider
from backend.llm.openai_provider import OpenAIProvider
from backend.llm.retry import FormalizationRetryManager
from backend.llm.parser import parse_logic_json
from backend.config.settings import settings


def get_llm_provider(provider_type: Optional[str] = None) -> BaseLLMProvider:
    provider = (provider_type or settings.LLM_PROVIDER).lower()
    if provider == "openai":
        return OpenAIProvider()
    return MockLLMProvider()


__all__ = [
    "BaseLLMProvider",
    "MockLLMProvider",
    "OpenAIProvider",
    "FormalizationRetryManager",
    "parse_logic_json",
    "get_llm_provider",
]
