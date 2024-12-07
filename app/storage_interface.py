from abc import ABC, abstractmethod
from typing import List, Dict, Any
from uuid import UUID

from .models import ChatSession, ChatMessage

class ChatStorage(ABC):
    """
    Abstract base class defining the required interface for any chat storage implementation.
    This can be extended to support different storage backends (e.g., in-memory, database).
    """

    @abstractmethod
    async def list_chats(self) -> List[ChatSession]:
        """
        Retrieve all active chat sessions.
        Returns:
            List[ChatSession]: A list of all stored chat sessions.
        """
        pass

    @abstractmethod
    async def create_chat(self) -> ChatSession:
        """
        Create and store a new chat session.
        Returns:
            ChatSession: The newly created chat session object.
        """
        pass

    @abstractmethod
    async def get_chat(self, chat_id: UUID) -> ChatSession:
        """
        Fetch a specific chat session by its unique ID.
        Args:
            chat_id (UUID): The unique identifier for the chat session.
        Returns:
            ChatSession: The chat session object if found.
        """
        pass

    @abstractmethod
    async def list_messages(self, chat_id: UUID) -> List[ChatMessage]:
        """
        Retrieve all messages from a specific chat session.
        Args:
            chat_id (UUID): The unique identifier for the chat session.
        Returns:
            List[ChatMessage]: A list of all messages in the session.
        """
        pass

    @abstractmethod
    async def add_message(self, chat_id: UUID, message: ChatMessage):
        """
        Add a new message to an existing chat session.
        Args:
            chat_id (UUID): The unique identifier for the chat session.
            message (ChatMessage): The message object to add.
        """
        pass

    @abstractmethod
    async def delete_chat(self, chat_id: UUID) -> bool:
        """
        Delete a specific chat session along with all its messages.
        Args:
            chat_id (UUID): The unique identifier for the chat session.
        Returns:
            bool: True if the chat session was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    async def get_chat_summary(self, chat_id: UUID) -> Dict[str, Any]:
        """
        Generate a summary for a specific chat session.
        Args:
            chat_id (UUID): The unique identifier for the chat session.
        Returns:
            Dict[str, Any]: A dictionary containing summary details such as message counts.
        """
        pass
