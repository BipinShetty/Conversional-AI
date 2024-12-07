from typing import Dict, List
from uuid import UUID
from asyncio import Lock
from app.models import ChatSession, ChatMessage


class MemoryStorage:
    """
    In-memory storage for chat sessions and messages.
    """

    def __init__(self):
        self._chats: Dict[UUID, ChatSession] = {}
        self._messages: Dict[UUID, List[ChatMessage]] = {}
        self._lock = Lock()

    async def list_chats(self) -> List[ChatSession]:
        async with self._lock:
            return list(self._chats.values())

    async def create_chat(self) -> ChatSession:
        async with self._lock:
            chat = ChatSession()
            self._chats[chat.id] = chat
            self._messages[chat.id] = []
            return chat

    async def get_chat(self, chat_id: UUID) -> ChatSession:
        """
        Retrieve a chat session by its ID.
        """
        async with self._lock:
            chat = self._chats.get(chat_id)
            if not chat:
                raise ValueError(f"Chat with ID {chat_id} does not exist.")
            return chat

    async def list_messages(self, chat_id: UUID) -> List[ChatMessage]:
        async with self._lock:
            return self._messages.get(chat_id, [])

    async def add_message(self, chat_id: UUID, message: ChatMessage):
        async with self._lock:
            if chat_id not in self._messages:
                raise ValueError(f"Chat with ID {chat_id} does not exist.")
            self._messages[chat_id].append(message)

    async def delete_chat(self, chat_id: UUID) -> bool:
        async with self._lock:
            if chat_id in self._chats:
                del self._chats[chat_id]
                del self._messages[chat_id]
                return True
            return False

    async def get_chat_summary(self, chat_id: UUID) -> Dict[str, any]:
        async with self._lock:
            chat = self._chats.get(chat_id)
            if not chat:
                raise ValueError(f"Chat with ID {chat_id} does not exist.")

            messages = self._messages.get(chat_id, [])
            user_msgs = [m.content for m in messages if m.sender == "user"]
            assistant_msgs = [m.content for m in messages if m.sender == "assistant"]

            return {
                "chat_id": str(chat_id),
                "total_messages": len(messages),
                "user_message_count": len(user_msgs),
                "assistant_message_count": len(assistant_msgs),
                "summary": " | ".join(user_msgs[:3]),
            }
