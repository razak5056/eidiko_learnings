from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq

# Prompt
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple words."
)

# Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

# RunnableSequence
chain = RunnableSequence(
    prompt,
    model
)

# Run
response = chain.invoke({"topic": "RAG"})

print(response.content)