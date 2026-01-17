# app/services/streaming/worker.py
import redis.asyncio as redis
from app.services.llm.factory import get_llm_provider
import json

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

async def run_worker():
    while True:
        jobs = await r.xread({"ai_jobs": "0-0"}, block=1000, count=1)
        if jobs:
            for stream, messages in jobs:
                for msg_id, msg in messages:
                    job_id = msg["job_id"]
                    model = msg["model"]
                    contents = json.loads(msg["contents"])
                    provider = get_llm_provider(model)

                    async for chunk in provider.generate_content(model, contents):
                        await r.xadd(f"ai_results:{job_id}", {"chunk": chunk})
