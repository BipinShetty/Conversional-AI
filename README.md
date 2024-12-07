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

**Getting Started**

**Prerequisites:**

* Python 3.10 or later
* `pip` (Python package manager)

**Simple Setup:**

1. Clone the repository:

```bash
git clone https://github.com/your-repo/konko-ai-chat-api.git
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

**Addressing Challenges**

* **Concurrency Handling:**
    * **Issue:** Concurrent access to shared memory by multiple requests could lead to data corruption.
    * **Solution:** `asyncio.Lock` synchronizes access to in-memory data structures, guaranteeing thread safety.
* **Invalid Chat IDs:**
    * **Issue:** Requests with invalid or non-existent chat IDs caused unhandled exceptions.
    * **Solution:** Graceful handling of invalid IDs with `HTTPException` and a 404 Not Found response.
* **Empty Messages:**
    * **Issue:** The API initially allowed empty user messages, resulting in meaningless AI responses.
    * **Solution:** Validation was added to reject empty messages, returning a 422 Unprocessable Entity response.
* **Mocking LLM API:**
    * **Issue:** Tests originally relied on live OpenAI API calls, making them dependent on external services.
    * **Solution:** Integration with `pytest-mock` enables mocking OpenAI responses, ensuring test reliability and faster execution.

**Production-Ready Considerations**

* The code utilizes clean abstractions, allowing for a
