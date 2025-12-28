# app/api/v1/models/schemas.py
from pydantic import BaseModel
from typing import List

class ModelInfo(BaseModel):
    name: str
    provider: str
    capabilities: List[str] = []  # 例如 ["stream", "chat", "code"]
