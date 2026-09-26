import re
import json
from typing import Dict, Any


def parse_logic_json(raw_text: str) -> Dict[str, Any]:
    """Extract and parse JSON object from LLM response string."""
    cleaned = raw_text.strip()
    
    # Strip markdown code fence if present
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if fence_match:
        cleaned = fence_match.group(1).strip()
    
    # Try finding outer JSON braces
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end+1]
        
    return json.loads(cleaned)
