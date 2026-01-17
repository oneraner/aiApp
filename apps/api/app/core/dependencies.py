# app/core/dependencies.py
"""
Shared dependencies for FastAPI routes
"""
import redis.asyncio as redis

# Global Redis client (initialized in main.py)
_redis_client: redis.Redis | None = None


def set_redis_client(client: redis.Redis):
    """Set the global Redis client instance"""
    global _redis_client
    _redis_client = client


async def get_redis() -> redis.Redis:
    """
    Dependency to get Redis client for route handlers
    
    Usage:
        @router.get("/endpoint")
        async def endpoint(r: redis.Redis = Depends(get_redis)):
            await r.set("key", "value")
    """
    if _redis_client is None:
        raise RuntimeError("Redis client not initialized. Call set_redis_client() first.")
    return _redis_client
