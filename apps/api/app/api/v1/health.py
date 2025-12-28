# app/api/v1/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    """
    簡單的健康檢查 API
    回傳 {"status": "ok"} 表示服務正常
    """
    return {"status": "ok"}
