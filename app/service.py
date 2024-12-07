from uuid import UUID
from app.models import ChatMessage, ChatSession
from app.storage import MemoryStorage
from app.ai_agent import query_llm

class ChatService:
    def __init__(self, storage: MemoryStorage):
        self.storage = storage

    async def list_chats(self) -> list[ChatSession]:
        return await self.storage.list_chats()

    async def create_chat(self) -> ChatSession:
        return await self.storage.create_chat()

    async def add_user_message(self, chat_id: UUID, content: str) -> ChatMessage:
        if not content.strip():
            raise ValueError("Message content cannot be empty.")

        user_message = ChatMessage(sender="user", content=content)
        await self.storage.add_message(chat_id, user_message)

        context = await self._build_conversation_context(chat_id)
        assistant_response = await query_llm(context, content)

        assistant_message = ChatMessage(sender="assistant", content=assistant_response)
        await self.storage.add_message(chat_id, assistant_message)
        return assistant_message

    async def list_messages(self, chat_id: UUID) -> list[ChatMessage]:
        return await self.storage.list_messages(chat_id)

    async def get_chat_summary(self, chat_id: UUID) -> dict:
        return await self.storage.get_chat_summary(chat_id)

    async def delete_chat(self, chat_id: UUID) -> bool:
        return await self.storage.delete_chat(chat_id)

    async def _build_conversation_context(self, chat_id: UUID) -> str:
        messages = await self.storage.list_messages(chat_id)
        return "\n".join(
            f"{m.sender.capitalize()}: {m.content}" for m in messages
        )
