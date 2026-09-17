from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
load_dotenv()
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    
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