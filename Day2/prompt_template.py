from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv  
load_dotenv()
# 1. Create prompt
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple words."
)

# 2. Create model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
   
)

# 3. Connect prompt + model
chain = prompt | model

# 4. Run chain
response = chain.invoke({"topic": "RAG"})

print(response.content)