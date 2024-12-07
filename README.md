This repository contains the Konko AI Chat API, a FastAPI-based application designed to manage chat sessions and integrate with an LLM (Language Model API) for generating AI-assisted responses. The project addresses concurrency issues, handles invalid inputs gracefully, and provides a clean abstraction for in-memory state management.

Features
Core Functionality:

Retrieve Chat Sessions: Fetch all chat sessions and their attributes.
Start a New Chat: Create a separate chat session.
Add Messages: Add user messages and receive AI-generated responses.
Fetch Messages: Retrieve all messages within a chat session.
Chat Summaries: Retrieve a summary of a chat, including counts and highlights.
Technical Highlights:

Asynchronous programming for efficient handling of concurrent requests.
Thread-safe in-memory storage using asyncio.Lock.
Mocking support for seamless testing of OpenAI API calls.
Comprehensive error handling for invalid inputs and edge cases.
Compliance with Requirements:

Properly handles concurrency edge cases.
Services multiple simultaneous conversations without interference.
Addresses follow-up messages with an AI-powered context-aware response.
Installation
Prerequisites
Python 3.10 or higher
pip (Python package manager)
Steps
Clone the repository:

bash
Copy code
uvicorn app.main:app --reload
Access the API documentation at:

arduino
Copy code
http://127.0.0.1:8000/docs
Project Structure
bash
Copy code
konko-ai/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI application definition
│   ├── models.py          # Data models for chat sessions and messages
│   ├── storage.py         # In-memory storage implementation
│   ├── query_llm.py       # OpenAI API integration
│   └── service.py         # Business logic for chat operations
├── test/
│   ├── test_api.py        # Comprehensive test suite for API functionality
│   └── ...
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
Testing
Run Tests
Install testing dependencies:


Creation of chat sessions.
Retrieval of all chats and messages.
Adding messages and verifying AI responses.
Handling invalid chat IDs.
Concurrent message handling to ensure thread safety.
Mocking OpenAI API calls for isolated testing.
Addressed Concerns
Concurrency Handling
Issue: Risk of data corruption when multiple requests access shared memory.
Solution: Used asyncio.Lock to synchronize access to in-memory data structures, ensuring thread safety.
Invalid Chat IDs
Issue: Requests with invalid or non-existent chat IDs resulted in unhandled exceptions.
Solution: Graceful handling of invalid IDs with HTTPException and returning 404 Not Found.
Empty Messages
Issue: API allowed empty user messages, leading to meaningless AI responses.
Solution: Added validation to reject empty messages with 422 Unprocessable Entity.
Mocking LLM API
Issue: Tests relied on live OpenAI API calls, making them dependent on external services.
Solution: Integrated pytest-mock to mock OpenAI responses, ensuring test reliability and faster execution.
Production Readiness
Clean abstractions in the code allow for easy replacement of in-memory storage with a database.
Structured logging can be integrated for better observability in production environments.
Future Enhancements
Database Integration: Replace in-memory storage with a persistent database like PostgreSQL or MongoDB.


Enhanced Summaries: Improve chat summaries with sentiment analysis or topic extraction.

Scalability: Optimize for distributed deployment using message queues (e.g., RabbitMQ) and caching layers (e.g., Redis).
