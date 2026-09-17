from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    
)

summary_prompt = ChatPromptTemplate.from_template(
    "Summarize this topic: {topic}"
)

question_prompt = ChatPromptTemplate.from_template(
    "Give 3 interview questions about: {topic}"
)

chain = RunnableParallel(
    summary=summary_prompt | model,
    questions=question_prompt | model
)

result = chain.invoke({"topic": "RAG"})

print("Summary:", result["summary"].content)
print("Questions:", result["questions"].content)