import os
import redis

def get_redis_client() -> redis.Redis:
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.Redis.from_url(
        url,
        decode_responses=True  # 很重要，避免 bytes 問題
    )
