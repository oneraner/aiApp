# app/api/v1/ai_stream.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import redis.asyncio as redis
import asyncio
from app.core.dependencies import get_redis

router = APIRouter()

import json

# ... (imports)

@router.get("/{job_id}")
async def stream_job(job_id: str, r: redis.Redis = Depends(get_redis)):
    async def event_generator():
        last_id = "0-0"
        timeout_count = 0
        max_timeouts = 30
        
        while timeout_count < max_timeouts:
            try:
                resp = await r.xread({f"ai_results:{job_id}": last_id}, block=1000, count=10)
                if resp:
                    stream_name, messages = resp[0]
                    for msg_id, msg in messages:
                        last_id = msg_id
                        chunk = msg.get("chunk", "")
                        
                        if chunk == "[DONE]":
                            yield f"data: {chunk}\n\n"
                            return
                        
                        # JSON encode to handle newlines safely
                        # Browser will receive: data: "Hello\nWorld"
                        safe_chunk = json.dumps(chunk)
                        yield f"data: {safe_chunk}\n\n"

                    timeout_count = 0
                else:
                    timeout_count += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                # JSON encode error message too
                error_msg = json.dumps(f"Error: {str(e)}")
                yield f"data: {error_msg}\n\n"
                return
        
        # Timeout reached
        yield "data: ❌ 連接超時\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )
