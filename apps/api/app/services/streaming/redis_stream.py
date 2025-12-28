# app/services/streaming/redis_stream.py
import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

STREAM_KEY = "llm_stream"

def push_message(message: dict):
    """推送訊息到 Redis stream"""
    return r.xadd(STREAM_KEY, {"data": json.dumps(message)})

def read_messages(last_id="$"):
    """讀取 stream 訊息"""
    return r.xread({STREAM_KEY: last_id}, block=0, count=10)
