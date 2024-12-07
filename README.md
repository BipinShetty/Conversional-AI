## Konko AI Chat API: A FastAPI Powerhouse for Conversational AI

This repository offers the Konko AI Chat API, a powerful tool built with FastAPI. It excels at managing chat sessions and integrates seamlessly with an LLM (Large Language Model API) to deliver AI-powered responses. The project prioritizes robust handling of concurrent requests, gracefully manages unexpected inputs, and provides a well-defined approach for in-memory state management.

**Key Features**

* **Core Functionality:**
    * Effortlessly retrieve existing chat sessions along with their details.
    * Start fresh chat sessions with ease.
    * Add user messages and receive AI-generated responses that enhance the conversation.
    * Access all messages within a specific chat session for review.
    * Generate informative chat summaries, including message counts and key highlights.
* **Technical Highlights:**
    * Asynchronous programming ensures efficient handling of concurrent requests, maximizing performance.
    * Thread-safe in-memory storage, implemented using `asyncio.Lock`, safeguards data integrity.
    * Mocking capabilities streamline testing of OpenAI API interactions.
    * Comprehensive error handling gracefully addresses invalid inputs and edge cases.
* **Addressing Requirements:**
    * Manages concurrency edge cases effectively, preventing data corruption.
    * Services multiple simultaneous conversations seamlessly, avoiding interference.
    * Delivers context-aware AI responses to follow-up messages, maintaining a natural flow.

**Here's a formatted version of the provided requirement table:**

| Requirement | Implemented? | Details |
|---|---|---|
| **Functional Requirements** | | |
| Retrieve a collection of chat conversations | ✅ | Implemented via GET /chats API endpoint. |
| Start a new separate conversation | ✅ | Implemented via POST /chats API endpoint. |
| Create a new message within a conversation | ✅ | Implemented via POST /chats/{chat_id}/messages API endpoint. |
| Retrieve all messages in a conversation | ✅ | Implemented via GET /chats/{chat_id}/messages API endpoint. |
| **API Needs** | | |
| Properly handle potential concurrency edge cases | ✅ | Implemented using asyncio.Lock to ensure thread safety. |
| Service multiple simultaneous conversations | ✅ | Asynchronous architecture and in-memory storage support this feature. |
| Handle follow-up messages clarifying earlier questions | ✅ | Implemented by building conversation context and passing it to the LLM for continuity. |
| Be configured with an LLM for AI agent | ✅ | OpenAI integration is configured for the AI agent functionality. |
| **Implementation Requirements** | | |
| Runtime: Python 3 with async concurrency | ✅ | Built using FastAPI with Python 3’s asynchronous capabilities. |
| Distribution: Version-controlled on GitHub | ✅ | Assumes the repository is version-controlled as specified. |
| Codebase close to production state | ✅ | Modularized, clean code with clear abstractions (e.g., services, models, storage). |
| Tests: A test suite is expected | ✅ | Comprehensive test suite covering all major functionalities. |
| State: Keep state in memory with abstraction | ✅ | In-memory storage implemented with an abstract interface (MemoryStorage). |
| 3rd-party services: Only an LLM API provider | ✅ | OpenAI API is the only 3rd-party service used. |

**Would you like me to format it in a different way, or perhaps create a report-style document?** 


**Getting Started**

**Prerequisites:**

* Python 3.10 or later
* `pip` (Python package manager)

**Simple Setup:**

1. Clone the repository:

```bash
git clone https://github.com/BipinShetty/konko-ai-chat-api.git
cd konko-ai-chat-api
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set the OpenAI API key environment variable:

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

5. Run the application:

```bash
uvicorn app.main:app --reload
```

6. Explore the API documentation at:

```
http://127.0.0.1:8000/docs
```

**Project Structure:**


**Ensuring Quality**

**Running the Tests:**

First, install the testing dependencies:

```bash
pip install pytest pytest-mock
```

Then, execute the test suite:

```bash
pytest -v
```

**Test Coverage:**

The test suite comprehensively covers essential functionality, including:

* Creation of chat sessions
* Retrieval of all chats and messages
* Adding messages and verifying AI responses
* Handling invalid chat IDs gracefully
* Ensuring thread safety during concurrent message handling
* Mocking OpenAI API calls for isolated and reliable testing

