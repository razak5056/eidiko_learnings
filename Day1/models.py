from langchain_groq import ChatGroq

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

response = model.invoke("What is Python?")
print(response.content)