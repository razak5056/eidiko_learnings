from chatbot import chatbot


print("================================")
print("       AI MEMORY CHATBOT")
print("================================")
print("Type 'exit' to stop the chatbot")


while True:

    # Get user input
    user_input = input("\nYou: ")

    # Stop chatbot
    if user_input.lower() == "exit":
        print("AI: Goodbye!")
        break

    # Get AI response
    response = chatbot(user_input)

    # Print AI response
    print("AI:", response)