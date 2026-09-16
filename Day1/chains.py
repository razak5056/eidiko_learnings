from langchain_groq import ChatGroq

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

chain = model

response = chain.invoke("Explain Python in simple words")

print(response.content)