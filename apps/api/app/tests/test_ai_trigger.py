"""
Tests for AI Trigger API endpoint.
"""
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_trigger_creates_job_and_conversation(client, mock_redis):
    """Test that trigger endpoint creates a job and returns job_id and conversation_id."""
    # Mock the LLM provider to avoid actual API calls
    with patch("app.api.v1.ai.trigger.GeminiProvider") as mock_provider:
        mock_instance = AsyncMock()
        mock_provider.return_value = mock_instance
        
        # Mock the stream to return immediately
        async def mock_stream(*args, **kwargs):
            yield "Hello"
            yield " World"
        mock_instance.stream = mock_stream
        
        response = await client.post(
            "/api/v1/ai/trigger",
            json={
                "model": "gemini-1.5-flash",
                "contents": [{"type": "text", "content": "Hello"}]
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert "conversation_id" in data
    assert len(data["job_id"]) > 0
    assert len(data["conversation_id"]) > 0


@pytest.mark.asyncio
async def test_trigger_validates_input_length(client, mock_redis):
    """Test that trigger endpoint validates input length (max 300 chars)."""
    long_content = "x" * 350  # Exceeds 300 char limit
    
    response = await client.post(
        "/api/v1/ai/trigger",
        json={
            "model": "gemini-1.5-flash",
            "contents": [{"type": "text", "content": long_content}]
        }
    )
    
    assert response.status_code == 400
    assert "字數" in response.json()["detail"] or "300" in response.json()["detail"]


@pytest.mark.asyncio
async def test_trigger_uses_existing_conversation(client, test_db, mock_redis):
    """Test that trigger can use an existing conversation."""
    from app.models.chat import Conversation
    
    # Create existing conversation
    conversation = Conversation()
    test_db.add(conversation)
    await test_db.commit()
    await test_db.refresh(conversation)
    
    with patch("app.api.v1.ai.trigger.GeminiProvider") as mock_provider:
        mock_instance = AsyncMock()
        mock_provider.return_value = mock_instance
        
        async def mock_stream(*args, **kwargs):
            yield "Response"
        mock_instance.stream = mock_stream
        
        response = await client.post(
            "/api/v1/ai/trigger",
            json={
                "model": "gemini-1.5-flash",
                "contents": [{"type": "text", "content": "Hi"}],
                "conversation_id": conversation.id
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == conversation.id


@pytest.mark.asyncio
async def test_trigger_requires_model(client):
    """Test that trigger endpoint requires model field."""
    response = await client.post(
        "/api/v1/ai/trigger",
        json={
            "contents": [{"type": "text", "content": "Hello"}]
        }
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_trigger_requires_contents(client):
    """Test that trigger endpoint requires contents field."""
    response = await client.post(
        "/api/v1/ai/trigger",
        json={
            "model": "gemini-1.5-flash"
        }
    )
    
    assert response.status_code == 422  # Validation error
