# app/api/v1/ai_trigger.py
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from uuid import uuid4
import json
import redis.asyncio as redis
from typing import Any, Dict, cast
# LLM provider
from app.services.llm.gemini_provider import GeminiProvider

router = APIRouter()
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

class AITriggerRequest(BaseModel):
    model: str
    contents: list  # [{"type":"text","content":"你好"}]

@router.post("/trigger")
async def trigger_ai(req: AITriggerRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())

    job_data: Dict[str, str] = {
        "job_id": job_id,
        "model": req.model,
        "contents": json.dumps(req.contents),
        "status": "pending"
    }
    await r.xadd("ai_jobs", fields=cast(Any, job_data))

    # 啟動背景 worker
    background_tasks.add_task(process_job, job_id, req.model, req.contents)

    return {"job_id": job_id}


async def process_job(job_id: str, model: str, contents: list):
    """
    背景 worker，將 LLM 生成的內容逐 chunk 寫入 Redis Stream
    """
    provider = GeminiProvider()

    # 將多段內容組合成 prompt
    prompt = "\n".join([c.get("content", "") for c in contents])

    # 逐 chunk 生成
    async for chunk in provider.stream(model=model, prompt=prompt):
        await r.xadd(f"ai_results:{job_id}", fields={"chunk": chunk})

    # 最後標記完成
    await r.xadd(f"ai_results:{job_id}", fields={"chunk": "[DONE]"})
