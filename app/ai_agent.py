import os
import openai

# Please add your opean-ai key here
openai.api_key = "<please put your open ai key in here>"
async def query_llm(context: str, user_message: str) -> str:
    """
    Query the OpenAI LLM using the conversation history and the user's latest message.
    """
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant that specializes in basic math operations."}
    ]

    # Parse the existing context (User/Agent pairs) into chat messages.
    if context:
        for line in context.split('\n'):
            line = line.strip()
            if line.startswith("User:"):
                user_content = line.replace("User:", "").strip()
                messages.append({"role": "user", "content": user_content})
            elif line.startswith("Agent:"):
                agent_content = line.replace("Agent:", "").strip()
                messages.append({"role": "assistant", "content": agent_content})

    # Append the latest user message:
    messages.append({"role": "user", "content": user_message})

    # Call OpenAI's chat completion API
    # The temperature is kept low(0.3) for deterministic reply as its a math problem
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3
    )

    return completion.choices[0].message["content"]
