from langchain_core.messages import HumanMessage, AIMessage

# Store conversation history
messages = []


# Save user message
def save_user_message(message):
    messages.append(HumanMessage(content=message))


# Save AI message
def save_ai_message(message):
    messages.append(AIMessage(content=message))


# Get conversation history
def get_memory():
    return messages