import ssl
import certifi
import aiohttp
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from uuid import UUID

# Importing internal modules for data models and services
from .models import (
    CreateChatRequest,
    CreateMessageRequest,
    ChatSession,
    ChatMessage,
    ChatSummaryResponse,
)
from .service import ChatService
from .storage import MemoryStorage

# Initializing the FastAPI application
app = FastAPI(title="Human Interaction Chat API")

# Setting up storage and service layer dependencies
storage = MemoryStorage()
chat_service = ChatService(storage=storage)


@app.on_event("startup")
async def on_startup():
    """
    Triggered when the application starts.
    Sets up an HTTP client session with secure SSL configurations.
    """
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))


@app.on_event("shutdown")
async def on_shutdown():
    """
    Triggered during application shutdown.
    Cleans up any active HTTP client sessions.
    """
    session = aiohttp.ClientSession()
    await session.close()


@app.get("/chats", response_model=List[ChatSession])
async def get_chats():
    """
    Retrieve all active chat sessions.
    """
    return await chat_service.list_chats()


@app.post("/chats", response_model=ChatSession, status_code=201)
async def create_chat(payload: CreateChatRequest):
    """
    Create a new chat session.
    """
    return await chat_service.create_chat()


@app.get("/chats/{chat_id}/messages", response_model=List[ChatMessage])
async def get_messages(chat_id: UUID):
    """
    Retrieve messages from a specific chat session.
    """
    chat = await storage.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return await chat_service.list_messages(chat_id)


@app.post("/chats/{chat_id}/messages", response_model=ChatMessage, status_code=201)
async def add_message(chat_id: UUID, payload: CreateMessageRequest):
    """
    Add a new message to an existing chat session.
    """
    chat = await storage.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return await chat_service.add_user_message(chat_id, payload.content)


@app.delete("/chats/{chat_id}", status_code=204)
async def delete_chat(chat_id: UUID):
    """
    Delete a specific chat session along with its messages.
    """
    deleted = await storage.delete_chat(chat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"message": "Chat session deleted successfully."}


@app.get("/chats/{chat_id}/summary", response_model=ChatSummaryResponse)
async def get_chat_summary(chat_id: UUID):
    """
    Generate a summary for a specific chat session.
    """
    try:
        summary = await storage.get_chat_summary(chat_id)
        return {
            "chat_id": str(summary["chat_id"]),
            "total_messages": str(summary["total_messages"]),
            "user_message_count": str(summary["user_message_count"]),
            "assistant_message_count": str(summary["assistant_message_count"]),
            "summary": summary.get("summary", ""),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
