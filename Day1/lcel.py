from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

# 1. Create prompt
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words."
)

# 2. Create Groq model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

# 3. Create output parser
parser = StrOutputParser()

# 4. Create LCEL chain
chain = prompt | model | parser

# 5. Run the chain
result = chain.invoke({
    "topic": "RAG"
})

print(result)