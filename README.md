## Konko AI Chat API

This repository holds the Konko AI Chat API, a FastAPI application designed to manage chat sessions and integrate with an LLM (Large Language Model) to generate AI-assisted responses. The project prioritizes concurrency issues, gracefully handles unexpected inputs, and provides a well-defined approach for managing in-memory state.

**Features**

* **Core Functionality:**
    * Retrieve existing chat sessions and their details.
    * Start new chat sessions.
    * Add user messages and receive AI-generated responses.
    * Fetch all messages within a chat session.
    * Get chat summaries with message counts and highlights.
* **Technical Highlights:**
    * Asynchronous programming for efficient concurrent request handling.
    * Thread-safe in-memory storage via `asyncio.Lock`.
    * Mocking support for streamlined testing of OpenAI API interactions.
    * Detailed error handling for invalid inputs and edge cases.
* **Compliance with Requirements:**
    * Manages concurrency edge cases effectively.
    * Handles multiple simultaneous conversations without interference.
    * Handles follow-up messages with context-aware AI responses.

**Installation**

**Prerequisites**

* Python 3.10 or later
* `pip` (Python package manager)

**Steps**

1. Clone the repository:

```bash
git clone https://github.com/your-repo/konko-ai-chat-api.git
cd konko-ai-chat-api
```

2. Create and activate a virtual environment:

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

6. Access the API documentation at:

```
http://127.0.0.1:8000/docs
```

**Project Structure**

```
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
```

**Testing**

**Run Tests**

Install testing dependencies:

```bash
pip install pytest pytest-mock
```

Execute the test suite:

```bash
pytest -v
```

**Test Coverage**

The test suite includes test cases for:

* Creation of chat sessions
* Retrieval of all chats and messages
* Adding messages and verifying AI responses
* Handling invalid chat IDs
* Concurrent message handling (thread safety)
* Mocking OpenAI API calls for isolated testing

**Addressed Concerns**

* **Concurrency Handling:**
    * **Issue:** Shared memory access by multiple requests could lead to data corruption.
    * **Solution:** `asyncio.Lock` is used to synchronize access to in-memory data structures, ensuring thread safety.
* **Invalid Chat IDs:**
    * **Issue:** Requests with invalid or non-existent chat IDs caused unhandled exceptions.
    * **Solution:** Graceful handling of invalid IDs with `HTTPException` and a 404 Not Found response.
* **Empty Messages:**
    * **Issue:** API allowed empty user messages, leading to meaningless AI responses.
    * **Solution:** Validation added to reject empty messages with a 422 Unprocessable Entity response.
* **Mocking LLM API:**
    * **Issue:** Tests relied on live OpenAI API calls, making them dependent on external services.
    * **Solution:** `pytest-mock` integrated to mock OpenAI responses, ensuring test reliability and faster execution.

**Production Readiness**

* Clean abstractions in the code enable easy replacement of in-memory storage with a database.
* Structured logging can be integrated for better observability in production environments.

**Future Enhancements**

* **Database Integration:**
    * Replace in-memory storage with a persistent database like PostgreSQL or MongoDB.
* **Rate Limiting:**
    * Implement throttling to prevent abuse of API endpoints.
* **Enhanced Summaries:**
    * Improve
