"""
Test configuration for the AI Platform API.

This module provides fixtures for testing FastAPI endpoints with:
- Async test client (httpx)
- Mock Redis (fakeredis)
- In-memory SQLite database
"""
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fakeredis import aioredis as fakeredis

# Set test environment before importing app
os.environ["ENVIRONMENT"] = "test"
os.environ["SENTRY_DSN"] = ""  # Disable Sentry in tests
os.environ["ADMIN_IPS"] = ""   # Disable Admin IPs to test rate limits for 127.0.0.1

from app.models.chat import Base
from app.db.database import get_db


# Create in-memory SQLite engine for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop_policy():
    """Use default event loop policy for async tests."""
    import asyncio
    return asyncio.DefaultEventLoopPolicy()


@pytest_asyncio.fixture
async def test_engine():
    """Create a test database engine with in-memory SQLite."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def mock_redis():
    """Create a fake Redis client for testing."""
    redis = fakeredis.FakeRedis(decode_responses=True)
    yield redis
    await redis.aclose()


@pytest_asyncio.fixture
async def client(test_db: AsyncSession, mock_redis) -> AsyncGenerator[AsyncClient, None]:
    """Create a test HTTP client with mocked dependencies."""
    from app.main import app
    from app.core.dependencies import set_redis_client
    from app.api.v1.admin.router import set_redis_client as set_admin_redis
    from app.infra.middleware.rate_limit import GlobalRateLimitMiddleware
    
    # Patch the RateLimit middleware with the mock redis
    # We need to update the middleware in app.user_middleware list
    # and force a rebuild of the middleware stack
    for middleware in app.user_middleware:
        if middleware.cls == GlobalRateLimitMiddleware:
            middleware.kwargs["redis_client"] = mock_redis
    
    # Clear the cached middleware stack so it gets rebuilt with new kwargs
    app.middleware_stack = None
    
    # Override database dependency
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Override Redis client
    set_redis_client(mock_redis)
    set_admin_redis(mock_redis)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    # Clean up overrides
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
async def patch_session_local(test_engine):
    """
    Patch AsyncSessionLocal to use the test engine.
    This ensures background tasks use the test database instead of determining real DB.
    """
    from sqlalchemy.orm import sessionmaker
    from app.db import database
    
    # Create a new session factory using the test engine
    test_session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Patch the global AsyncSessionLocal
    original_session_local = database.AsyncSessionLocal
    database.AsyncSessionLocal = test_session_factory
    
    yield
    
    # Restore original
    database.AsyncSessionLocal = original_session_local


# Configure pytest-asyncio
pytest_plugins = ("pytest_asyncio",)
