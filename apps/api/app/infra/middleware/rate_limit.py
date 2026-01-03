# app/infra/middleware/rate_limit.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timezone
import redis.asyncio as redis
import os


class GlobalRateLimitMiddleware(BaseHTTPMiddleware):
    """
    Global rate limiting middleware - limits total requests across all IPs
    Protects against API cost explosion from many different sources
    """
    
    def __init__(self, app, redis_client: redis.Redis):
        super().__init__(app)
        self.redis = redis_client
        self.daily_limit = 3  # Total requests per day for entire server
        self.admin_ips = set(
            ip.strip() 
            for ip in os.getenv("ADMIN_IPS", "127.0.0.1,::1").split(",")
            if ip.strip()
        )
        
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for admin endpoints and health checks
        if request.url.path.startswith("/admin") or request.url.path.startswith("/health"):
            return await call_next(request)
        
        # Only apply to AI trigger endpoint
        if not request.url.path.startswith("/api/v1/ai/trigger"):
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Check if admin IP (bypass rate limit)
        if client_ip in self.admin_ips:
            # Admin requests don't count towards global limit
            response = await call_next(request)
            response.headers["X-RateLimit-Admin"] = "true"
            return response
        
        # Check global rate limit
        count_key = "global_request_count"
        reset_key = "global_request_reset_time"
        
        # Get current count and reset time
        current_count = await self.redis.get(count_key)
        reset_time = await self.redis.get(reset_key)
        
        # Initialize if not exists
        if current_count is None:
            current_count = 0
            # Set reset time to end of day (UTC)
            now = datetime.now(timezone.utc)
            end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            ttl = int((end_of_day - now).total_seconds())
            
            await self.redis.setex(count_key, ttl, 0)
            await self.redis.setex(reset_key, ttl, end_of_day.isoformat())
            reset_time = end_of_day.isoformat()
        else:
            current_count = int(current_count)
        
        # Check if exceeded
        if current_count >= self.daily_limit:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "今日配額已用完",
                    "message": f"整個服務每日限制 {self.daily_limit} 次請求，請明日再試",
                    "reset_time": reset_time,
                    "used": current_count,
                    "limit": self.daily_limit
                }
            )
        
        # Increment counter
        await self.redis.incr(count_key)
        current_count += 1
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.daily_limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, self.daily_limit - current_count))
        response.headers["X-RateLimit-Reset"] = reset_time
        
        return response
