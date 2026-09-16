from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

memory = InMemoryChatMessageHistory()

chat = RunnableWithMessageHistory(
    model,
    lambda session_id: memory
)

response = chat.invoke(
    "My name is John",
    config={"configurable": {"session_id": "user1"}}
)

print(response.content)

response = chat.invoke(
    "What is my name?",
    config={"configurable": {"session_id": "user1"}}
)

print(response.content)