# Conversations API router
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.database import get_db
from app.models.chat import Conversation, Message
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class MessageResponse(BaseModel):
    """Response model for a single message"""
    id: str
    role: str
    content: str
    model_used: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Response model for a conversation with all messages"""
    id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


class ConversationListItem(BaseModel):
    """Response model for conversation list item"""
    id: str
    created_at: datetime
    updated_at: datetime
    message_count: int

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ConversationListItem])
async def list_conversations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all conversations with pagination.
    
    Returns conversations ordered by most recently updated first.
    """
    try:
        # Optimized query using SQL count instead of loading all messages
        query = (
            select(
                Conversation.id,
                Conversation.created_at,
                Conversation.updated_at,
                func.count(Message.id).label('message_count')
            )
            .outerjoin(Message, Message.conversation_id == Conversation.id)
            .group_by(Conversation.id, Conversation.created_at, Conversation.updated_at)
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(query)
        rows = result.all()
        
        conversation_list = [
            ConversationListItem(
                id=row.id,
                created_at=row.created_at,
                updated_at=row.updated_at,
                message_count=row.message_count
            )
            for row in rows
        ]
        
        return conversation_list
    except Exception as e:
        import logging
        logging.error(f"Error listing conversations: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversations: {str(e)}")


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get a specific conversation with all its messages.
    
   Returns 404 if conversation not found.
    """
    try:
        from sqlalchemy.orm import selectinload
        
        result = await db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.error(f"Error getting conversation {conversation_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversation: {str(e)}")


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    """
    Delete a conversation and all its messages.
    
    Returns 404 if conversation not found.
    """
    try:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        await db.delete(conversation)
        await db.commit()
        
        return {"success": True, "message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.error(f"Error deleting conversation {conversation_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")
