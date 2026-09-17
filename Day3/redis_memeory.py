from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_redis import RedisChatMessageHistory

# Load variables from .env file
load_dotenv()

# Create the Groq LLM
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# Connect to Redis
# session_id identifies this user's conversation
history = RedisChatMessageHistory(
    session_id="razak",
    redis_url="redis://localhost:6379"
)

# Keep chatting until the user types exit
while True:

    # Get input from the user
    user_input = input("You: ")

    # Stop the program
    if user_input.lower() == "exit":
        break

    # Store the user's message in Redis
    history.add_user_message(user_input)

    # Get previous conversation from Redis
    messages = history.messages

    # Send conversation history + new message to the model
    response = model.invoke(messages)

    # Store AI response in Redis
    history.add_ai_message(response.content)

    # Display AI response
    print("AI:", response.content)