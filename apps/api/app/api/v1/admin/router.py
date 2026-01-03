# app/api/v1/admin/router.py
from fastapi import APIRouter, HTTPException, Request
import redis.asyncio as redis
import os

router = APIRouter()

# Admin IPs that can access these endpoints
ADMIN_IPS = set(
    ip.strip() 
    for ip in os.getenv("ADMIN_IPS", "127.0.0.1,::1").split(",")
    if ip.strip()
)

# Redis client (will be set on startup)
redis_client: redis.Redis = None


def set_redis_client(client: redis.Redis):
    global redis_client
    redis_client = client


def check_admin_ip(request: Request):
    """Check if request is from admin IP"""
    client_ip = request.client.host if request.client else "unknown"
    if client_ip not in ADMIN_IPS:
        raise HTTPException(
            status_code=403,
            detail="只有管理員可以存取此端點"
        )


@router.post("/reset-limit")
async def reset_rate_limit(request: Request):
    """
    手動重置全域限流計數器
    只有管理員 IP 可以呼叫
    """
    check_admin_ip(request)
    
    count_key = "global_request_count"
    reset_key = "global_request_reset_time"
    
    await redis_client.delete(count_key)
    await redis_client.delete(reset_key)
    
    return {
        "success": True,
        "message": "限流計數器已重置",
        "note": "下次請求時會重新初始化計數器"
    }


@router.get("/limit-status")
async def get_rate_limit_status(request: Request):
    """
    查看當前限流狀態
    只有管理員 IP 可以呼叫
    """
    check_admin_ip(request)
    
    count_key = "global_request_count"
    reset_key = "global_request_reset_time"
    
    current_count = await redis_client.get(count_key)
    reset_time = await redis_client.get(reset_key)
    
    limit = 3  # Daily limit
    
    if current_count is None:
        return {
            "initialized": False,
            "message": "計數器尚未初始化（還沒有任何請求）",
            "limit": limit
        }
    
    return {
        "initialized": True,
        "used": int(current_count),
        "remaining": max(0, limit - int(current_count)),
        "limit": limit,
        "reset_time": reset_time,
        "is_exceeded": int(current_count) >= limit
    }
