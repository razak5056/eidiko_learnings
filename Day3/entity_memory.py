from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

entity_memory = {}

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    prompt = f"""
Extract important entities and facts from this message.

Current memory:
{entity_memory}

User message:
{user_input}

Return the updated entity memory.
"""

    response = model.invoke(prompt)

    entity_memory["latest"] = response.content

    print("AI:", response.content)
    print("Memory:", entity_memory)