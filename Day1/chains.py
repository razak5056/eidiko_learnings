from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

chain = model

response = chain.invoke("Explain Python in simple words")

print(response.content)