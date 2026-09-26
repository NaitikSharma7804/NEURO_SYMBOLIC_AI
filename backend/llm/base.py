from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate text completion from prompt."""
        pass

    @abstractmethod
    async def formalize(self, natural_language_text: str) -> Dict[str, Any]:
        """Formalize natural language text into logic JSON structure."""
        pass
