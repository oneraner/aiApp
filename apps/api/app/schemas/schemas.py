from pydantic import BaseModel
from typing import List, Dict, Any

class AIRequest(BaseModel):
    model: str
    # contents 直接就是前端傳的 list[dict]，完全對應 Gemini SDK
    contents: List[Dict[str, Any]]
