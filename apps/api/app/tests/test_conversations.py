"""
Tests for Conversations API endpoints.
"""
import pytest
from app.models.chat import Conversation, Message


@pytest.mark.asyncio
async def test_list_conversations_empty(client):
    """Test that listing conversations returns empty list when no data."""
    response = await client.get("/api/v1/conversations/")
    
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_conversations_with_data(client, test_db):
    """Test that listing conversations returns data correctly."""
    # Create test conversation
    conversation = Conversation()
    test_db.add(conversation)
    await test_db.commit()
    await test_db.refresh(conversation)
    
    response = await client.get("/api/v1/conversations/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == conversation.id
    assert data[0]["message_count"] == 0


@pytest.mark.asyncio
async def test_get_conversation_success(client, test_db):
    """Test getting a specific conversation with messages."""
    # Create conversation with message
    conversation = Conversation()
    test_db.add(conversation)
    await test_db.commit()
    await test_db.refresh(conversation)
    
    message = Message(
        conversation_id=conversation.id,
        role="user",
        content="Hello, test!",
        model_used=None
    )
    test_db.add(message)
    await test_db.commit()
    
    response = await client.get(f"/api/v1/conversations/{conversation.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation.id
    assert len(data["messages"]) == 1
    assert data["messages"][0]["content"] == "Hello, test!"
    assert data["messages"][0]["role"] == "user"


@pytest.mark.asyncio
async def test_get_nonexistent_conversation_returns_404(client):
    """Test that accessing non-existent conversation returns 404."""
    response = await client.get("/api/v1/conversations/nonexistent-id")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_delete_conversation_success(client, test_db):
    """Test deleting a conversation."""
    # Create conversation
    conversation = Conversation()
    test_db.add(conversation)
    await test_db.commit()
    await test_db.refresh(conversation)
    
    # Delete it
    response = await client.delete(f"/api/v1/conversations/{conversation.id}")
    
    assert response.status_code == 200
    assert response.json()["success"] is True
    
    # Verify it's gone
    get_response = await client.get(f"/api/v1/conversations/{conversation.id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_conversation_returns_404(client):
    """Test that deleting non-existent conversation returns 404."""
    response = await client.delete("/api/v1/conversations/nonexistent-id")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_conversations_pagination(client, test_db):
    """Test pagination for conversation list."""
    # Create 5 conversations
    for _ in range(5):
        conversation = Conversation()
        test_db.add(conversation)
    await test_db.commit()
    
    # Test limit
    response = await client.get("/api/v1/conversations/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Test skip
    response = await client.get("/api/v1/conversations/?skip=3&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 2  # 5 - 3 = 2 remaining
