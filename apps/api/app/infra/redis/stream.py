from typing import Iterator, Optional
from .client import get_redis_client

redis = get_redis_client()


def stream_key(generation_id: str) -> str:
    return f"stream:{generation_id}"


def append_token(
    generation_id: str,
    *,
    content: str,
    seq: int
) -> str:
    """
    寫入一個 token/chunk 到 Redis Stream
    """
    return redis.xadd(
        stream_key(generation_id),
        {
            "type": "token",
            "content": content,
            "seq": seq,
        }
    )


def read_stream(
    generation_id: str,
    *,
    last_id: str = "0-0",
    block_ms: int = 5000,
) -> Iterator[tuple[str, dict]]:
    """
    從 Redis Stream 讀取資料
    """
    result = redis.xread(
        {stream_key(generation_id): last_id},
        block=block_ms,
        count=10,
    )

    if not result:
        return []

    _, messages = result[0]
    return messages
