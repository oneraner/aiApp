"""
AI Platform API - FastAPI Backend
"""
import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import redis.asyncio as redis
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# App routers
from app.api.v1.health import router as health_router
from app.api.v1.ai.router import router as ai_router
from app.api.v1.models.router import router as models_router
from app.api.v1.admin.router import router as admin_router
from app.api.v1.admin.router import set_redis_client as set_admin_redis
from app.api.v1.conversations.router import router as conversations_router

# Core modules
from app.core.logging import setup_logging
from app.core.dependencies import set_redis_client
from app.infra.middleware.rate_limit import GlobalRateLimitMiddleware
from app.db.migration import run_migrations

# Load environment variables
load_dotenv()

# Setup
logger = logging.getLogger(__name__)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
setup_logging()

# Initialize Sentry (only if DSN provided)
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
            LoggingIntegration(
                level=logging.INFO,        # Capture info and above as breadcrumbs
                event_level=logging.WARNING  # Capture warning and above as events
            ),
        ],
        traces_sample_rate=0.1,  # 10% of transactions
        profiles_sample_rate=0.1,
        environment=os.getenv("ENVIRONMENT", "development"),
    )

# Create FastAPI app
app = FastAPI(title="AI Platform API")

# Build allowed origins list
allowed_origins = [
    "http://localhost:3000",  # Local development - Next.js (web)
    "http://localhost:3002",  # Local development - ai-web
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

# Add rate limiting middleware
app.add_middleware(GlobalRateLimitMiddleware, redis_client=redis_client)

# Set redis client for dependency injection
set_redis_client(redis_client)
set_admin_redis(redis_client)


from starlette.exceptions import HTTPException as StarletteHTTPException

# Global exception handler for better error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that returns detailed error information.
    In production, you may want to hide internal details.
    """
    # Let FastAPI/Starlette handle HTTPExceptions (like 429, 404, etc.)
    if isinstance(exc, StarletteHTTPException):
        raise exc

    error_id = os.urandom(4).hex()
    
    # Log the full error with traceback
    logger.error(
        f"[{error_id}] Unhandled exception on {request.method} {request.url.path}: {exc}",
        exc_info=True
    )
    
    # Determine error type and message
    error_type = type(exc).__name__
    error_message = str(exc)
    
    # Common error patterns with helpful messages
    if "connection" in error_message.lower() or "connect" in error_message.lower():
        detail = {
            "error": "Database connection failed",
            "hint": "Check if PostgreSQL is running and DATABASE_URL is configured correctly",
            "error_id": error_id,
        }
    elif "does not exist" in error_message.lower() or "relation" in error_message.lower():
        detail = {
            "error": "Database table not found",
            "hint": "Run database migrations or check if tables are created",
            "error_id": error_id,
        }
    elif "redis" in error_message.lower():
        detail = {
            "error": "Redis connection failed",
            "hint": "Check if Redis is running and REDIS_URL is configured correctly",
            "error_id": error_id,
        }
    else:
        # Generic error - include type for debugging
        detail = {
            "error": error_message,
            "type": error_type,
            "error_id": error_id,
        }
    
    return JSONResponse(
        status_code=500,
        content={"detail": detail}
    )


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


# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(models_router, prefix="/api/v1/models", tags=["models"])
app.include_router(conversations_router, prefix="/api/v1/conversations", tags=["conversations"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
