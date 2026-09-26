from typing import Dict, Any, Optional
from backend.llm.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """Deterministic mock provider for reproducible testing without API calls."""

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        return "Mock LLM output response."

    async def formalize(self, natural_language_text: str) -> Dict[str, Any]:
        text_lower = natural_language_text.lower()
        
        # Scenario 1: Socrates
        if "socrates" in text_lower and "mortal" in text_lower:
            return {
                "facts": [
                    {"predicate": "human", "arguments": ["socrates"], "is_negated": False}
                ],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "human", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "mortal", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "mortal", "arguments": ["socrates"], "is_negated": False}
            }

        # Scenario 2 & 3: Tweety (bird/penguin flies)
        if "tweety" in text_lower:
            if "penguin" in text_lower:
                return {
                    "facts": [
                        {"predicate": "penguin", "arguments": ["tweety"], "is_negated": False}
                    ],
                    "rules": [
                        {
                            "variables": ["X"],
                            "body": [{"predicate": "penguin", "arguments": ["X"], "is_negated": False}],
                            "head": {"predicate": "flies", "arguments": ["X"], "is_negated": True}
                        }
                    ],
                    "query": {"predicate": "flies", "arguments": ["tweety"], "is_negated": False}
                }
            elif "birds fly" in text_lower and "does not fly" in text_lower:
                # Scenario 5: Conflicting knowledge
                return {
                    "facts": [
                        {"predicate": "bird", "arguments": ["tweety"], "is_negated": False},
                        {"predicate": "flies", "arguments": ["tweety"], "is_negated": True}
                    ],
                    "rules": [
                        {
                            "variables": ["X"],
                            "body": [{"predicate": "bird", "arguments": ["X"], "is_negated": False}],
                            "head": {"predicate": "flies", "arguments": ["X"], "is_negated": False}
                        }
                    ],
                    "query": {"predicate": "flies", "arguments": ["tweety"], "is_negated": False}
                }
            else:
                # Scenario 2: Unknown (Tweety is a bird. Query: Tweety flies.)
                return {
                    "facts": [
                        {"predicate": "bird", "arguments": ["tweety"], "is_negated": False}
                    ],
                    "rules": [],
                    "query": {"predicate": "flies", "arguments": ["tweety"], "is_negated": False}
                }

        # Scenario 4: Multi-hop (Alice student -> person -> mortal)
        if "alice" in text_lower:
            return {
                "facts": [
                    {"predicate": "student", "arguments": ["alice"], "is_negated": False}
                ],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "student", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "person", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "person", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "mortal", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "mortal", "arguments": ["alice"], "is_negated": False}
            }

        # Default minimal fallback
        return {
            "facts": [],
            "rules": [],
            "query": {"predicate": "unknown_goal", "arguments": ["entity"], "is_negated": False}
        }
