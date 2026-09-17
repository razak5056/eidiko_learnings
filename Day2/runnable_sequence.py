from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
# Prompt
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple words."
)

# Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    
)

# RunnableSequence
chain = RunnableSequence(
    prompt,
    model
)

# Run
response = chain.invoke({"topic": "RAG"})

print(response.content)