"""
Tests for Health API endpoint.
"""
import pytest


@pytest.mark.asyncio
async def test_health_check_returns_ok(client):
    """Test that health check endpoint returns status: ok."""
    response = await client.get("/health/")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_check_no_rate_limit(client, mock_redis):
    """Test that health endpoint is not rate limited."""
    # Make multiple requests - all should succeed
    for _ in range(10):
        response = await client.get("/health/")
        assert response.status_code == 200
