from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

class ChatMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    sender: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatSummaryResponse(BaseModel):
    chat_id: str
    total_messages: str
    user_message_count: str
    assistant_message_count: str
    summary: Optional[str]

class CreateChatRequest(BaseModel):
    pass

class CreateMessageRequest(BaseModel):
    content: str
