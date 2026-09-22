from graph import app


user_input = input("Enter text: ")


initial_state = {
    "user_input": user_input,
    "processed_text": "",
    "response": ""
}


result = app.invoke(initial_state)


print("\nFinal Result:")
print(result["response"])