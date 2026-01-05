# app/api/v1/ai_stream.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import redis.asyncio as redis
import asyncio
from app.core.dependencies import get_redis

router = APIRouter()

@router.get("/{job_id}")  # Changed from "/stream/{job_id}" to "/{job_id}"
async def stream_job(job_id: str, r: redis.Redis = Depends(get_redis)):
    async def event_generator():
        last_id = "$"  # 從最新的訊息開始
        while True:
            try:
                resp = await r.xread({f"ai_results:{job_id}": last_id}, block=1000, count=1)
                if resp:
                    stream_name, messages = resp[0]
                    for msg_id, msg in messages:
                        last_id = msg_id
                        chunk = msg.get("chunk", "")
                        yield f"data: {chunk}\n\n"

                        if chunk == "[DONE]":
                            return
                else:
                    await asyncio.sleep(0.1)
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"
                return

    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )
