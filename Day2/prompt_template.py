from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# 1. Create prompt
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple words."
)

# 2. Create model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

# 3. Connect prompt + model
chain = prompt | model

# 4. Run chain
response = chain.invoke({"topic": "RAG"})

print(response.content)