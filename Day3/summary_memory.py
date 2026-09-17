from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

messages = []
summary = ""

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(HumanMessage(content=user_input))

    # Include previous summary
    prompt = []

    if summary:
        prompt.append(
            HumanMessage(
                content=f"Previous conversation summary: {summary}"
            )
        )

    prompt.extend(messages)

    response = model.invoke(prompt)

    print("AI:", response.content)

    messages.append(AIMessage(content=response.content))

    # Create/update summary
    summary_prompt = [
        HumanMessage(
            content=f"""
Summarize the following conversation briefly.
Keep important user information and context.

Conversation:
{messages}
"""
        )
    ]

    summary_response = model.invoke(summary_prompt)
    summary = summary_response.content