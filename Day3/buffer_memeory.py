from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(HumanMessage(content=user_input))

    response = model.invoke(messages)

    messages.append(AIMessage(content=response.content))

    print("AI:", response.content)