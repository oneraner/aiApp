# app/infra/middleware/rate_limit.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis
import os


# Rate limit configuration
RATE_LIMIT_CONFIG = {
    "max_requests_per_day": 3,
    "max_input_tokens_per_day": 2000,
    "max_output_tokens_per_day": 5000,
    "max_input_chars": 1000,
    "max_output_tokens": 1000,
}


class GlobalRateLimitMiddleware(BaseHTTPMiddleware):
    """
    Enhanced rate limiting middleware with token tracking.
    
    Limits:
    - Request count per IP per day
    - Input tokens per IP per day
    - Output tokens per IP per day
    """
    
    def __init__(self, app, redis_client: redis.Redis):
        super().__init__(app)
        self.redis = redis_client
        self.admin_ips = set(
            ip.strip() 
            for ip in os.getenv("ADMIN_IPS", "127.0.0.1,::1").split(",")
            if ip.strip()
        )
        
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for admin endpoints and health checks
        if request.url.path.startswith("/api/v1/admin") or request.url.path.startswith("/health"):
            return await call_next(request)
        
        # Only apply to AI trigger endpoint
        if not request.url.path.startswith("/api/v1/ai/trigger"):
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Check if admin IP (bypass rate limit)
        if client_ip in self.admin_ips:
            response = await call_next(request)
            response.headers["X-RateLimit-Admin"] = "true"
            return response
        
        # Check request count limit
        request_key = f"rate_limit:{client_ip}:requests"
        request_count = await self.redis.get(request_key)
        request_count = int(request_count) if request_count else 0
        
        if request_count >= RATE_LIMIT_CONFIG["max_requests_per_day"]:
            return JSONResponse(
                status_code=429,
                content={"detail": f"每日請求次數已達上限（{RATE_LIMIT_CONFIG['max_requests_per_day']} 次），請明日再試"}
            )
        
        # Check input token limit
        input_token_key = f"rate_limit:{client_ip}:input_tokens"
        input_tokens_used = await self.redis.get(input_token_key)
        input_tokens_used = int(input_tokens_used) if input_tokens_used else 0
        
        if input_tokens_used >= RATE_LIMIT_CONFIG["max_input_tokens_per_day"]:
            return JSONResponse(
                status_code=429,
                content={"detail": "每日輸入用量已達上限，請明日再試"}
            )
        
        # Increment request counter
        await self.redis.incr(request_key)
        await self.redis.expire(request_key, 86400)  # 24 hours
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Requests-Limit"] = str(RATE_LIMIT_CONFIG["max_requests_per_day"])
        response.headers["X-RateLimit-Requests-Remaining"] = str(max(0, RATE_LIMIT_CONFIG["max_requests_per_day"] - request_count - 1))
        
        return response
