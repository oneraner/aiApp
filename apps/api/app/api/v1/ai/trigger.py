# app/api/v1/ai_trigger.py
from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel
from uuid import uuid4
import json
import redis.asyncio as redis
from typing import Any, Dict, cast
from sqlalchemy.ext.asyncio import AsyncSession
# LLM provider
from app.services.llm.gemini_provider import GeminiProvider
from app.db.database import get_db
from app.models.chat import Conversation, Message

router = APIRouter()
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

class AITriggerRequest(BaseModel):
    model: str
    contents: list  # [{"type":"text","content":"你好"}]
    conversation_id: str | None = None  # Optional: existing conversation ID

@router.post("")  # Changed from "/trigger" to "" because parent router has prefix="/trigger"
async def trigger_ai(req: AITriggerRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    job_id = str(uuid4())
    
    # Get or create conversation
    if req.conversation_id:
        conversation = await db.get(Conversation, req.conversation_id)
        if not conversation:
            # Create new if not found
            conversation = Conversation(id=req.conversation_id)
            db.add(conversation)
    else:
        # Create new conversation
        conversation = Conversation()
        db.add(conversation)
    
    await db.flush()  # Get the conversation ID
    
    # Extract user message content
    user_content = "\n".join([c.get("content", "") for c in req.contents])
    
    # Save user message to database
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=user_content,
        model_used=None
    )
    db.add(user_message)
    await db.commit()
    
    # Add to Redis job queue
    job_data: Dict[str, str] = {
        "job_id": job_id,
        "model": req.model,
        "contents": json.dumps(req.contents),
        "conversation_id": conversation.id,
        "status": "pending"
    }
    await r.xadd("ai_jobs", fields=cast(Any, job_data))

    # 啟動背景 worker
    background_tasks.add_task(process_job, job_id, req.model, req.contents, conversation.id)

    return {
        "job_id": job_id,
        "conversation_id": conversation.id
    }


async def process_job(job_id: str, model: str, contents: list, conversation_id: str):
    """
    背景 worker，將 LLM 生成的內容逐 chunk 寫入 Redis Stream
    並在完成後將完整回應存入資料庫
    """
    try:
        print(f"[Background Task] Starting job {job_id} with model {model}")
        
        provider = GeminiProvider()
        print(f"[Background Task] GeminiProvider initialized")

        # 將多段內容組合成 prompt
        prompt = "\n".join([c.get("content", "") for c in contents])
        print(f"[Background Task] Prompt: {prompt[:50]}...")

        # Collect full response for database
        full_response = ""

        # 逐 chunk 生成
        chunk_count = 0
        async for chunk in provider.stream(model=model, prompt=prompt):
            await r.xadd(f"ai_results:{job_id}", fields={"chunk": chunk})
            full_response += chunk
            chunk_count += 1
            if chunk_count % 10 == 0:
                print(f"[Background Task] Received {chunk_count} chunks")

        print(f"[Background Task] Streaming complete. Total chunks: {chunk_count}")

        # 最後標記完成
        await r.xadd(f"ai_results:{job_id}", fields={"chunk": "[DONE]"})
        print(f"[Background Task] Sent [DONE] signal")
        
        # Save assistant message to database
        from app.db.database import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            assistant_message = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=full_response,
                model_used=model
            )
            db.add(assistant_message)
            await db.commit()
            print(f"[Background Task] Saved to database. Response length: {len(full_response)}")
    
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Log full error on backend
        print(f"[Background Task ERROR] Job {job_id} failed: {error_type}: {error_msg}")
        import traceback
        traceback.print_exc()
        
        # Determine user-friendly error message
        user_message = "處理請求時發生錯誤"
        
        if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
            user_message = f"API 配額已用完，請稍後再試"
            if "gemini-2.0-flash-exp" in error_msg:
                user_message += " (建議切換到 gemini-1.5-flash 模型)"
        elif "PERMISSION_DENIED" in error_msg or "403" in error_msg:
            user_message = "API 金鑰無效或權限不足"
        elif "INVALID_ARGUMENT" in error_msg or "400" in error_msg:
            user_message = "請求參數錯誤"
        elif "UNAUTHENTICATED" in error_msg or "401" in error_msg:
            user_message = "API 金鑰未設置或無效"
        else:
            # Generic error - show first 100 chars
            user_message = f"處理失敗: {error_msg[:100]}"
        
        # Send user-friendly error to stream
        try:
            await r.xadd(f"ai_results:{job_id}", fields={"chunk": f"❌ {user_message}"})
            await r.xadd(f"ai_results:{job_id}", fields={"chunk": "[DONE]"})
        except Exception as redis_error:
            print(f"[Background Task ERROR] Failed to write error to Redis: {redis_error}")

