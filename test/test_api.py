import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.main import app
from app.ai_agent import query_llm


# Initialize the test client for the FastAPI app
client = TestClient(app)


def test_create_chat():
    """
    Test that a new chat session can be created successfully.
    """
    response = client.post("/chats", json={})
    assert response.status_code == 201, "Failed to create a chat session"

    data = response.json()
    # Check that the response includes expected fields
    assert "id" in data, "Chat session ID is missing in the response"
    assert "created_at" in data, "Chat session creation timestamp is missing in the response"


def test_list_chats():
    """
    Test that chat sessions can be listed after creation.
    """
    # Create a chat session
    response = client.post("/chats", json={})
    assert response.status_code == 201, "Failed to create a chat session"
    chat_id = response.json()["id"]

    # Fetch the list of chat sessions
    response = client.get("/chats")
    assert response.status_code == 200, "Failed to fetch chat sessions"

    data = response.json()
    # Verify the created chat session is in the list
    assert any(d["id"] == chat_id for d in data), "Created chat session is not listed"


def test_add_message_to_chat():
    """
    Test adding a user message to a chat session and receiving a response.
    """
    # Create a chat session
    response = client.post("/chats", json={})
    assert response.status_code == 201, "Failed to create a chat session"
    chat_id = response.json()["id"]

    # Add a user message to the chat session
    message_payload = {"content": "What's 7 plus 5?"}
    response = client.post(f"/chats/{chat_id}/messages", json=message_payload)
    assert response.status_code == 201, "Failed to add a message to the chat session"

    data = response.json()
    # Verify the assistant's response
    assert data["sender"] == "assistant", "Assistant response is missing or incorrect"
    assert data["content"], "Assistant response content is missing"


def test_get_messages_from_chat():
    """
    Test retrieving messages for a specific chat session.
    """
    # Create a chat session
    response = client.post("/chats", json={})
    assert response.status_code == 201, "Failed to create a chat session"
    chat_id = response.json()["id"]

    # Add a user message
    client.post(f"/chats/{chat_id}/messages", json={"content": "What's 8 times 6?"})

    # Retrieve the messages for the chat session
    response = client.get(f"/chats/{chat_id}/messages")
    assert response.status_code == 200, "Failed to fetch messages for the chat session"

    data = response.json()
    # Check that both user and assistant messages are present
    assert len(data) == 2, "Unexpected number of messages retrieved"
    senders = [m["sender"] for m in data]
    assert "user" in senders, "User message is missing in the retrieved messages"
    assert "assistant" in senders, "Assistant response is missing in the retrieved messages"


def test_delete_chat():
    """
    Test deleting a chat session and verifying it no longer exists.
    """
    # Create a chat session
    response = client.post("/chats", json={})
    assert response.status_code == 201, "Failed to create a chat session"
    chat_id = response.json()["id"]

    # Delete the chat session
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204, "Failed to delete the chat session"

    # Verify the chat session no longer exists
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 405, "Chat session still exists after deletion"


def test_get_chat_summary():
    """
    Test retrieving a summary of messages for a chat session.
    """
    # Create a chat session
    response = client.post("/chats", json={})
    assert response.status_code == 201, "Failed to create a chat session"
    chat_id = response.json()["id"]

    # Add multiple messages
    client.post(f"/chats/{chat_id}/messages", json={"content": "Hello!"})
    client.post(f"/chats/{chat_id}/messages", json={"content": "What is AI?"})

    # Retrieve the chat summary
    response = client.get(f"/chats/{chat_id}/summary")
    assert response.status_code == 200, "Failed to fetch chat summary"

    data = response.json()
    assert data["chat_id"] == chat_id, "Chat ID mismatch in the summary"
    assert "total_messages" in data, "Total messages count is missing in the summary"
    assert "user_message_count" in data, "User message count is missing in the summary"
    assert "assistant_message_count" in data, "Assistant message count is missing in the summary"
    assert "summary" in data, "Summary is missing in the response"


def test_invalid_chat_id():
    """
    Test handling of invalid chat session IDs.
    """
    invalid_id = "00000000-0000-0000-0000-000000000000"

    # Try deleting a non-existent chat session
    response = client.delete(f"/chats/{invalid_id}")
    assert response.status_code == 404, "Expected 404 for non-existent chat session"

@pytest.fixture
def mock_openai(mocker):
    """
    Mock the OpenAI API response for testing purposes.
    """
    mocker.patch(
        "app.ai_agent.query_llm",
        new=AsyncMock(return_value="This is a mocked assistant response."),
    )

def test_concurrent_message_addition(mock_openai):
    """
    Test concurrent message additions to a chat session.
    """
    from concurrent.futures import ThreadPoolExecutor

    # Create a chat session
    response = client.post("/chats", json={})
    assert response.status_code == 201, f"Failed to create a chat session: {response.json()}"
    chat_id = response.json()["id"]

    def add_message():
        return client.post(f"/chats/{chat_id}/messages", json={"content": "Hi"})

    # Simulate concurrent requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        responses = list(executor.map(lambda _: add_message(), range(5)))

    # Check all responses
    assert all(r.status_code == 201 for r in responses), "One or more requests failed"
