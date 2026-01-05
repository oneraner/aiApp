from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.health import router as health_router
from app.api.v1.ai.router import router as ai_router
from app.api.v1.models.router import router as models_router
from app.api.v1.admin.router import router as admin_router, set_redis_client
from app.core.logging import setup_logging
from app.infra.middleware.rate_limit import GlobalRateLimitMiddleware
from app.db.migration import run_migrations
from app.core.dependencies import set_redis_client
from dotenv import load_dotenv
import redis.asyncio as redis
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

setup_logging()

app = FastAPI(title="AI Platform API")

# Build allowed origins list
allowed_origins = [
    "http://localhost:3000",  # Local development - Next.js
    "http://localhost:5173",  # Local development - Vite
]

# Add production frontend URL from environment
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Redis client immediately (before adding middleware)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Add rate limiting middleware (must be added before startup)
app.add_middleware(GlobalRateLimitMiddleware, redis_client=redis_client)

# Set redis client for dependency injection and admin router
set_redis_client(redis_client)  # For app.core.dependencies
from app.api.v1.admin.router import set_redis_client as set_admin_redis
set_admin_redis(redis_client)  # For admin router


@app.on_event("startup")
async def startup_event():
    # Run database migrations automatically
    await run_migrations()
    print("✓ Redis connected")
    print("✓ Rate limiting enabled (3 requests/day globally)")


@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()
    print("✓ Redis disconnected")


from app.api.v1.conversations.router import router as conversations_router

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(models_router, prefix="/api/v1/models", tags=["models"])
app.include_router(conversations_router, prefix="/api/v1/conversations", tags=["conversations"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
