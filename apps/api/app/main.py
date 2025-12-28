from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.api.v1.ai.router import router as ai_router
from app.api.v1.models.router import router as models_router
from app.core.logging import setup_logging
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

setup_logging()

app = FastAPI(title="AI Platform API")

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(models_router, prefix="/api/v1", tags=["models"])
