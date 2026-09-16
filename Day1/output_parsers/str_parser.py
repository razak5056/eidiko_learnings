from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

# Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

# Output parser
parser = StrOutputParser()

# Chain
chain = model | parser

# Run
result = chain.invoke("What is RAG? Explain in one sentence.")

print(result)