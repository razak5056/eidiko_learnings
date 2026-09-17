from langchain_groq import ChatGroq
from memory import save_user_message, save_ai_message, get_memory

from dotenv import load_dotenv
load_dotenv()
# Create Groq model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# Chatbot function
def chatbot(user_input):

    # Save user message
    save_user_message(user_input)

    # Get previous conversation
    messages = get_memory()

    # Send conversation to model
    response = model.invoke(messages)

    # Save AI response
    save_ai_message(response.content)

    # Return AI response
    return response.content