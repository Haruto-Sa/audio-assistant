from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid


class Message(BaseModel):
    """
    メッセージモデル
    """
    id: Optional[int] = None
    conversation_id: str
    user_id: Optional[str] = "anonymous"
    role: str  # "user" または "assistant"
    content: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class Conversation(BaseModel):
    """
    会話モデル
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = "anonymous"
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    messages: List[Message] = Field(default_factory=list)

    class Config:
        orm_mode = True


class ConversationSummary(BaseModel):
    """
    会話履歴の要約
    """
    conversation_id: str
    title: Optional[str] = None
    last_message: Optional[str] = None
    message_count: int = 0
    updated_at: datetime


# SQL定義（PostgreSQL用）
CONVERSATION_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    title TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
"""

MESSAGE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT fk_conversation FOREIGN KEY (conversation_id) 
        REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
""" 