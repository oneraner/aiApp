# app/api/v1/models/router.py
from fastapi import APIRouter
from typing import List
from app.api.v1.models.schemas import ModelInfo
from app.services.llm.factory import get_all_models  # 工廠方法拿所有 provider 模型

router = APIRouter()


@router.get("/", response_model=List[ModelInfo], summary="列出平台支援的所有模型")
async def list_models():
    """
    回傳平台目前支援的所有 LLM 模型列表，
    每個模型包含名稱、提供者、capabilities（如 stream / chat / code）
    """
    models = await get_all_models()
    return models
