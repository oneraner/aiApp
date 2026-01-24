"""
Tests for Rate Limiter middleware.
"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_rate_limit_allows_under_limit(client, mock_redis):
    """Test that requests under rate limit are allowed."""
    with patch("app.api.v1.ai.trigger.GeminiProvider") as mock_provider:
        from unittest.mock import AsyncMock
        mock_instance = AsyncMock()
        mock_provider.return_value = mock_instance
        
        async def mock_stream(*args, **kwargs):
            yield "OK"
        mock_instance.stream = mock_stream
        
        # First request should succeed
        response = await client.post(
            "/api/v1/ai/trigger",
            json={
                "model": "gemini-1.5-flash",
                "contents": [{"type": "text", "content": "Hi"}]
            }
        )
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_rate_limit_blocks_when_exceeded(client, mock_redis):
    """Test that requests are blocked when rate limit is exceeded."""
    # Simulate exceeded rate limit by setting request count above limit
    await mock_redis.set("rate_limit:127.0.0.1:requests", "10")
    
    with patch("app.api.v1.ai.trigger.GeminiProvider"):
        response = await client.post(
            "/api/v1/ai/trigger",
            json={
                "model": "gemini-1.5-flash",
                "contents": [{"type": "text", "content": "Hi"}]
            }
        )
    
    if response.status_code != 429:
        print(f"DEBUG: Status={response.status_code}")
        print(f"DEBUG: Headers={response.headers}")
        print(f"DEBUG: Body={response.json()}")
        
    assert response.status_code == 429
    assert "上限" in response.json()["detail"] or "limit" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_rate_limit_blocks_when_token_exceeded(client, mock_redis):
    """Test that requests are blocked when input token limit is exceeded."""
    # Simulate exceeded token limit
    await mock_redis.set("rate_limit:127.0.0.1:input_tokens", "1000")
    
    with patch("app.api.v1.ai.trigger.GeminiProvider"):
        response = await client.post(
            "/api/v1/ai/trigger",
            json={
                "model": "gemini-1.5-flash",
                "contents": [{"type": "text", "content": "Hi"}]
            }
        )
    
    assert response.status_code == 429


@pytest.mark.asyncio
async def test_health_endpoint_bypasses_rate_limit(client, mock_redis):
    """Test that health endpoint is not affected by rate limit."""
    # Set high request count
    await mock_redis.set("rate_limit:127.0.0.1:requests", "100")
    
    # Health endpoint should still work
    response = await client.get("/health/")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_conversations_endpoint_bypasses_rate_limit(client, mock_redis):
    """Test that conversations endpoint bypasses rate limit."""
    # Set high request count
    await mock_redis.set("rate_limit:127.0.0.1:requests", "100")
    
    # Conversations endpoint should still work
    response = await client.get("/api/v1/conversations/")
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_rate_limit_increments_counter(client, mock_redis):
    """Test that successful requests increment the rate limit counter."""
    initial_count = await mock_redis.get("rate_limit:127.0.0.1:requests")
    initial_count = int(initial_count) if initial_count else 0
    
    with patch("app.api.v1.ai.trigger.GeminiProvider") as mock_provider:
        from unittest.mock import AsyncMock
        mock_instance = AsyncMock()
        mock_provider.return_value = mock_instance
        
        async def mock_stream(*args, **kwargs):
            yield "OK"
        mock_instance.stream = mock_stream
        
        await client.post(
            "/api/v1/ai/trigger",
            json={
                "model": "gemini-1.5-flash",
                "contents": [{"type": "text", "content": "Hi"}]
            }
        )
    
    new_count = await mock_redis.get("rate_limit:127.0.0.1:requests")
    new_count = int(new_count) if new_count else 0
    
    assert new_count == initial_count + 1
